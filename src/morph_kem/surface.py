from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from statistics import mean

from .complex import Simplex, SimplicialComplex
from .morse import (
    GreedyMatchingSurvey,
    MorsePair,
    MorseValidation,
    greedy_matching_survey,
    validate_morse_matching,
)


class SurfaceExperimentError(ValueError):
    """Raised when an M4 closed-surface experiment input is invalid."""


@dataclass(frozen=True, slots=True)
class SurfaceParameters:
    name: str
    rows: int
    cols: int

    def validate(self) -> None:
        if self.rows < 3 or self.rows > 32:
            raise SurfaceExperimentError("M4 rows must be in [3, 32]")
        if self.cols < 3 or self.cols > 32:
            raise SurfaceExperimentError("M4 cols must be in [3, 32]")


SURFACE_PARAMETER_SETS = {
    "torus-3x3": SurfaceParameters("torus-3x3", 3, 3),
    "torus-4x4": SurfaceParameters("torus-4x4", 4, 4),
    "torus-5x5": SurfaceParameters("torus-5x5", 5, 5),
    "torus-6x6": SurfaceParameters("torus-6x6", 6, 6),
    "torus-7x7": SurfaceParameters("torus-7x7", 7, 7),
}


@dataclass(frozen=True, slots=True)
class SurfacePublicInstance:
    parameters: SurfaceParameters
    target: SimplicialComplex
    critical_target: tuple[int, ...] = (1, 2, 1)
    version: int = 1

    def __post_init__(self) -> None:
        self.parameters.validate()
        if self.version != 1:
            raise SurfaceExperimentError("unsupported M4 public-instance version")
        expected_vertices = self.parameters.rows * self.parameters.cols
        if self.target.vertices != tuple(range(expected_vertices)):
            raise SurfaceExperimentError("M4 target must use the canonical public vertex universe")
        if self.target.dimension != 2:
            raise SurfaceExperimentError("M4 target must be two-dimensional")
        if self.critical_target != (1, 2, 1):
            raise SurfaceExperimentError("M4 torus target must be (1, 2, 1)")

    def encode(self) -> bytes:
        payload = {
            "critical_target": list(self.critical_target),
            "parameters": {
                "cols": self.parameters.cols,
                "name": self.parameters.name,
                "rows": self.parameters.rows,
            },
            "target": self.target.encode().hex(),
            "version": self.version,
        }
        return json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")

    @property
    def fingerprint(self) -> bytes:
        return hashlib.sha256(
            b"MORPH-KEM M4 public fingerprint v1\x00" + self.encode()
        ).digest()


@dataclass(frozen=True, slots=True)
class SurfaceTrapdoor:
    planted_matching: tuple[MorsePair, ...]
    public_fingerprint: bytes
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise SurfaceExperimentError("unsupported M4 trapdoor version")
        if len(self.public_fingerprint) != 32:
            raise SurfaceExperimentError("M4 trapdoor binding must be 32 bytes")

    def encode(self) -> bytes:
        payload = {
            "planted_matching": [
                [list(lower), list(upper)]
                for lower, upper in self.planted_matching
            ],
            "public_fingerprint": self.public_fingerprint.hex(),
            "version": self.version,
        }
        return json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")


@dataclass(frozen=True, slots=True)
class SurfaceIncidence:
    vertices: int
    edges: int
    triangles: int
    min_triangles_per_edge: int
    max_triangles_per_edge: int


@dataclass(frozen=True, slots=True)
class TreeCotreeResult:
    matching: tuple[MorsePair, ...]
    validation: MorseValidation
    primal_tree_edges: int
    dual_tree_edges: int
    critical_edges: int


@dataclass(frozen=True, slots=True)
class TreeCotreeSurvey:
    trials: int
    target_hits: int
    unique_matchings: int
    mean_critical_edges: float


class _DeterministicRng:
    def __init__(self, seed: bytes):
        self._seed = seed
        self._counter = 0

    def _block(self) -> bytes:
        block = hashlib.sha256(
            b"MORPH-KEM M4 deterministic rng v1\x00"
            + self._seed
            + self._counter.to_bytes(8, "big")
        ).digest()
        self._counter += 1
        return block

    def randbelow(self, upper: int) -> int:
        if upper <= 0:
            raise ValueError("upper bound must be positive")
        limit = (1 << 256) - ((1 << 256) % upper)
        while True:
            candidate = int.from_bytes(self._block(), "big")
            if candidate < limit:
                return candidate % upper


def _shuffle(items: list, seed: bytes) -> None:
    rng = _DeterministicRng(seed)
    for index in range(len(items) - 1, 0, -1):
        other = rng.randbelow(index + 1)
        items[index], items[other] = items[other], items[index]


def _vertex(rows: int, cols: int, row: int, col: int) -> int:
    return (row % rows) * cols + (col % cols)


def _torus_complex(parameters: SurfaceParameters) -> SimplicialComplex:
    parameters.validate()
    facets: list[Simplex] = []
    for row in range(parameters.rows):
        for col in range(parameters.cols):
            a = _vertex(parameters.rows, parameters.cols, row, col)
            b = _vertex(parameters.rows, parameters.cols, row + 1, col)
            c = _vertex(parameters.rows, parameters.cols, row, col + 1)
            d = _vertex(parameters.rows, parameters.cols, row + 1, col + 1)
            facets.append(tuple(sorted((a, b, d))))
            facets.append(tuple(sorted((a, d, c))))
    if len(set(facets)) != len(facets):
        raise SurfaceExperimentError("M4 torus triangulation produced duplicate facets")
    return SimplicialComplex.from_facets(facets)


def _permutation(size: int, seed: bytes) -> tuple[int, ...]:
    values = list(range(size))
    _shuffle(values, seed)
    return tuple(values)


def _edge_triangle_incidence(
    complex_: SimplicialComplex,
) -> dict[Simplex, tuple[Simplex, ...]]:
    edges = [simplex for simplex in complex_.simplices if len(simplex) == 2]
    triangles = [simplex for simplex in complex_.simplices if len(simplex) == 3]
    incidence: dict[Simplex, list[Simplex]] = {edge: [] for edge in edges}
    for triangle in triangles:
        triangle_set = set(triangle)
        for edge in edges:
            if set(edge).issubset(triangle_set):
                incidence[edge].append(triangle)
    return {
        edge: tuple(sorted(values))
        for edge, values in incidence.items()
    }


def surface_incidence(public: SurfacePublicInstance) -> SurfaceIncidence:
    incidence = _edge_triangle_incidence(public.target)
    counts = [len(value) for value in incidence.values()]
    return SurfaceIncidence(
        vertices=sum(len(simplex) == 1 for simplex in public.target.simplices),
        edges=sum(len(simplex) == 2 for simplex in public.target.simplices),
        triangles=sum(len(simplex) == 3 for simplex in public.target.simplices),
        min_triangles_per_edge=min(counts),
        max_triangles_per_edge=max(counts),
    )


def _tree_cotree_matching(
    complex_: SimplicialComplex,
    attack_seed: bytes | None,
) -> tuple[tuple[MorsePair, ...], int, int]:
    vertices = list(complex_.vertices)
    edges = [simplex for simplex in complex_.simplices if len(simplex) == 2]
    triangles = [simplex for simplex in complex_.simplices if len(simplex) == 3]
    if not vertices or not triangles:
        raise SurfaceExperimentError("tree-cotree attack requires a 2D connected surface")

    vertex_adjacency: dict[int, list[tuple[int, Simplex]]] = {
        vertex: [] for vertex in vertices
    }
    for edge in edges:
        left, right = edge
        vertex_adjacency[left].append((right, edge))
        vertex_adjacency[right].append((left, edge))

    for vertex, neighbors in vertex_adjacency.items():
        neighbors.sort()
        if attack_seed is not None:
            _shuffle(
                neighbors,
                hashlib.sha256(
                    b"MORPH-KEM M4 primal adjacency v1\x00"
                    + attack_seed
                    + vertex.to_bytes(4, "big")
                ).digest(),
            )

    root_vertex = min(vertices)
    if attack_seed is not None:
        root_vertex = vertices[
            int.from_bytes(
                hashlib.sha256(
                    b"MORPH-KEM M4 primal root v1\x00" + attack_seed
                ).digest(),
                "big",
            )
            % len(vertices)
        ]

    queue = [root_vertex]
    seen_vertices = {root_vertex}
    primal_pairs: list[MorsePair] = []
    primal_tree_edges: set[Simplex] = set()
    while queue:
        parent = queue.pop(0)
        for child, edge in vertex_adjacency[parent]:
            if child in seen_vertices:
                continue
            seen_vertices.add(child)
            queue.append(child)
            primal_tree_edges.add(edge)
            primal_pairs.append(((child,), edge))

    if len(seen_vertices) != len(vertices):
        raise SurfaceExperimentError("M4 primal graph is disconnected")

    incidence = _edge_triangle_incidence(complex_)
    if any(len(adjacent) != 2 for adjacent in incidence.values()):
        raise SurfaceExperimentError("M4 target is not closed at edge/triangle incidence")

    dual_adjacency: dict[Simplex, list[tuple[Simplex, Simplex]]] = {
        triangle: [] for triangle in triangles
    }
    for edge, adjacent in incidence.items():
        if edge in primal_tree_edges:
            continue
        left, right = adjacent
        dual_adjacency[left].append((right, edge))
        dual_adjacency[right].append((left, edge))

    for index, triangle in enumerate(triangles):
        neighbors = dual_adjacency[triangle]
        neighbors.sort()
        if attack_seed is not None:
            _shuffle(
                neighbors,
                hashlib.sha256(
                    b"MORPH-KEM M4 dual adjacency v1\x00"
                    + attack_seed
                    + index.to_bytes(4, "big")
                ).digest(),
            )

    root_triangle = min(triangles)
    if attack_seed is not None:
        root_triangle = triangles[
            int.from_bytes(
                hashlib.sha256(
                    b"MORPH-KEM M4 dual root v1\x00" + attack_seed
                ).digest(),
                "big",
            )
            % len(triangles)
        ]

    queue_triangles = [root_triangle]
    seen_triangles = {root_triangle}
    dual_pairs: list[MorsePair] = []
    dual_tree_edges: set[Simplex] = set()
    while queue_triangles:
        parent = queue_triangles.pop(0)
        for child, edge in dual_adjacency[parent]:
            if child in seen_triangles:
                continue
            seen_triangles.add(child)
            queue_triangles.append(child)
            dual_tree_edges.add(edge)
            dual_pairs.append((edge, child))

    if len(seen_triangles) != len(triangles):
        raise SurfaceExperimentError("M4 dual complement of primal tree is disconnected")

    if primal_tree_edges & dual_tree_edges:
        raise SurfaceExperimentError("M4 primal and dual trees reused an edge")

    return tuple(primal_pairs + dual_pairs), len(primal_tree_edges), len(dual_tree_edges)


def tree_cotree_witness(
    public: SurfacePublicInstance,
    attack_seed: bytes | None = None,
) -> TreeCotreeResult:
    if attack_seed == b"":
        raise SurfaceExperimentError("M4 randomized tree-cotree seed must be non-empty")
    matching, primal_count, dual_count = _tree_cotree_matching(
        public.target,
        attack_seed,
    )
    validation = validate_morse_matching(
        public.target,
        matching,
        public.critical_target,
    )
    critical_edges = validation.critical_vector[1] if validation.critical_vector else -1
    return TreeCotreeResult(
        matching=matching,
        validation=validation,
        primal_tree_edges=primal_count,
        dual_tree_edges=dual_count,
        critical_edges=critical_edges,
    )


def tree_cotree_survey(
    public: SurfacePublicInstance,
    trials: int = 32,
    attack_seed: bytes = b"M4-tree-cotree-survey",
) -> TreeCotreeSurvey:
    if trials <= 0 or trials > 10_000:
        raise SurfaceExperimentError("M4 survey trials must be in [1, 10000]")
    if not attack_seed:
        raise SurfaceExperimentError("M4 survey requires a non-empty seed")

    hits = 0
    matchings: set[tuple[MorsePair, ...]] = set()
    critical_edges: list[int] = []
    for trial in range(trials):
        seed = hashlib.sha256(
            b"MORPH-KEM M4 tree-cotree trial v1\x00"
            + attack_seed
            + trial.to_bytes(8, "big")
        ).digest()
        result = tree_cotree_witness(public, seed)
        hits += int(result.validation.valid)
        matchings.add(tuple(sorted(result.matching)))
        critical_edges.append(result.critical_edges)

    return TreeCotreeSurvey(
        trials=trials,
        target_hits=hits,
        unique_matchings=len(matchings),
        mean_critical_edges=mean(critical_edges),
    )


def generate_surface_instance(
    parameters: SurfaceParameters,
    master_seed: bytes,
) -> tuple[SurfacePublicInstance, SurfaceTrapdoor]:
    parameters.validate()
    if not isinstance(master_seed, bytes) or not master_seed:
        raise SurfaceExperimentError("master_seed must be non-empty bytes")

    hidden = _torus_complex(parameters)
    vertex_count = parameters.rows * parameters.cols
    relabeling = _permutation(
        vertex_count,
        hashlib.sha256(
            b"MORPH-KEM M4 final relabeling v1\x00"
            + parameters.name.encode("ascii")
            + b"\x00"
            + master_seed
        ).digest(),
    )
    target = hidden.relabel(relabeling)
    public = SurfacePublicInstance(parameters=parameters, target=target)

    planted = tree_cotree_witness(public, attack_seed=None)
    if not planted.validation.valid:
        raise SurfaceExperimentError("internal M4 planted witness validation failed")
    trapdoor = SurfaceTrapdoor(
        planted_matching=planted.matching,
        public_fingerprint=public.fingerprint,
    )
    return public, trapdoor


def verify_surface_trapdoor(
    public: SurfacePublicInstance,
    trapdoor: SurfaceTrapdoor,
) -> MorseValidation:
    if public.fingerprint != trapdoor.public_fingerprint:
        raise SurfaceExperimentError("M4 trapdoor is bound to another public instance")
    return validate_morse_matching(
        public.target,
        trapdoor.planted_matching,
        public.critical_target,
    )


def surface_greedy_matching_survey(
    public: SurfacePublicInstance,
    trials: int = 8,
    attack_seed: bytes = b"M4-greedy-survey",
) -> GreedyMatchingSurvey:
    return greedy_matching_survey(
        public,
        trials=trials,
        attack_seed=attack_seed,
    )
