from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math

from .holonomy import HolonomyGraph, HolonomyParameters, generate_holonomy_graph

Edge = tuple[int, int]
Permutation = tuple[int, ...]


class LiftedAtlasError(ValueError):
    """Raised when an H3-E0 lifted-atlas calibration input is invalid."""


@dataclass(frozen=True, slots=True)
class LiftedAtlasParameters:
    name: str
    base_vertices: int
    extra_edges: int
    sheets: int

    def validate(self) -> None:
        if self.base_vertices < 6 or self.base_vertices > 64:
            raise LiftedAtlasError("H3-E0 base vertex count must be in [6, 64]")
        max_extra = self.base_vertices * (self.base_vertices - 1) // 2 - self.base_vertices
        if self.extra_edges <= 0 or self.extra_edges > max_extra:
            raise LiftedAtlasError("H3-E0 extra-edge count is outside the valid range")
        if self.sheets < 2 or self.sheets > 12:
            raise LiftedAtlasError("H3-E0 sheet count must be in [2, 12]")


LIFTED_ATLAS_PARAMETER_SETS = {
    "lift-8x3": LiftedAtlasParameters("lift-8x3", 8, 4, 3),
    "lift-10x4": LiftedAtlasParameters("lift-10x4", 10, 5, 4),
    "lift-12x5": LiftedAtlasParameters("lift-12x5", 12, 6, 5),
    "lift-16x6": LiftedAtlasParameters("lift-16x6", 16, 8, 6),
}


@dataclass(frozen=True, slots=True)
class LiftedAtlasPublic:
    parameters: LiftedAtlasParameters
    graph: HolonomyGraph
    transitions: tuple[Permutation, ...]
    version: int = 1

    def __post_init__(self) -> None:
        self.parameters.validate()
        if self.version != 1:
            raise LiftedAtlasError("unsupported H3-E0 public-instance version")
        if self.graph.vertices != self.parameters.base_vertices:
            raise LiftedAtlasError("H3-E0 graph size does not match parameters")
        if len(self.transitions) != len(self.graph.edges):
            raise LiftedAtlasError("transition count does not match public edges")
        for transition in self.transitions:
            _validate_permutation(transition, self.parameters.sheets)

    def encode(self) -> bytes:
        payload = {
            "graph": json.loads(self.graph.encode().decode("ascii")),
            "parameters": {
                "base_vertices": self.parameters.base_vertices,
                "extra_edges": self.parameters.extra_edges,
                "name": self.parameters.name,
                "sheets": self.parameters.sheets,
            },
            "transitions": [list(value) for value in self.transitions],
            "version": self.version,
        }
        return json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")


@dataclass(frozen=True, slots=True)
class LiftedAtlasReference:
    canonical_transitions: tuple[Permutation, ...]
    secret_fiber_gauges: tuple[Permutation, ...]


@dataclass(frozen=True, slots=True)
class GaugeNormalization:
    public_gauges: tuple[Permutation, ...]
    normalized_transitions: tuple[Permutation, ...]
    tree_identity_edges: int
    chord_edges: int
    permutation_point_ops: int


@dataclass(frozen=True, slots=True)
class ReferenceComparison:
    globally_conjugate: bool
    root_conjugator: Permutation


@dataclass(frozen=True, slots=True)
class LiftEquivariance:
    public_end_sheet: int
    normalized_start_sheet: int
    normalized_end_sheet: int
    expected_normalized_end_sheet: int
    holds: bool


class _DeterministicRng:
    def __init__(self, seed: bytes):
        self._seed = seed
        self._counter = 0

    def _block(self) -> bytes:
        block = hashlib.sha256(
            b"MORPH-KEM H3-E0 deterministic rng v1\x00"
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


def _validate_permutation(permutation: Permutation, size: int) -> None:
    if len(permutation) != size or set(permutation) != set(range(size)):
        raise LiftedAtlasError("invalid sheet permutation")


def _identity(size: int) -> Permutation:
    return tuple(range(size))


def _compose(after: Permutation, before: Permutation) -> Permutation:
    if len(after) != len(before):
        raise LiftedAtlasError("cannot compose permutations of different size")
    return tuple(after[before[index]] for index in range(len(before)))


def _inverse(permutation: Permutation) -> Permutation:
    result = [0] * len(permutation)
    for source, target in enumerate(permutation):
        result[target] = source
    return tuple(result)


def _conjugate(permutation: Permutation, conjugator: Permutation) -> Permutation:
    return _compose(
        conjugator,
        _compose(permutation, _inverse(conjugator)),
    )


def _random_permutation(size: int, rng: _DeterministicRng) -> Permutation:
    values = list(range(size))
    for index in range(size - 1, 0, -1):
        other = rng.randbelow(index + 1)
        values[index], values[other] = values[other], values[index]
    return tuple(values)


def _edge_index(graph: HolonomyGraph) -> dict[Edge, int]:
    return {edge: index for index, edge in enumerate(graph.edges)}


def _oriented_transition(
    public: LiftedAtlasPublic,
    source: int,
    target: int,
) -> Permutation:
    edge = (source, target) if source < target else (target, source)
    index = _edge_index(public.graph)[edge]
    transition = public.transitions[index]
    return transition if source < target else _inverse(transition)


def _oriented_from_table(
    graph: HolonomyGraph,
    transitions: tuple[Permutation, ...],
    source: int,
    target: int,
) -> Permutation:
    edge = (source, target) if source < target else (target, source)
    index = _edge_index(graph)[edge]
    transition = transitions[index]
    return transition if source < target else _inverse(transition)


def _monodromy_orbit_size(
    graph: HolonomyGraph,
    canonical_transitions: tuple[Permutation, ...],
    sheets: int,
) -> int:
    tree = set(graph.spanning_tree_edges())
    generators = [
        canonical_transitions[index]
        for index, edge in enumerate(graph.edges)
        if edge not in tree
    ]
    generators += [_inverse(value) for value in generators]

    seen = {0}
    frontier = [0]
    while frontier:
        sheet = frontier.pop()
        for generator in generators:
            target = generator[sheet]
            if target not in seen:
                seen.add(target)
                frontier.append(target)
    return len(seen)


def generate_lifted_atlas(
    parameters: LiftedAtlasParameters,
    master_seed: bytes,
) -> tuple[LiftedAtlasPublic, LiftedAtlasReference]:
    parameters.validate()
    if not isinstance(master_seed, bytes) or not master_seed:
        raise LiftedAtlasError("master_seed must be non-empty bytes")

    graph_parameters = HolonomyParameters(
        f"{parameters.name}-base",
        parameters.base_vertices,
        parameters.extra_edges,
    )

    for attempt in range(512):
        attempt_seed = hashlib.sha256(
            b"MORPH-KEM H3-E0 generation attempt v1\x00"
            + parameters.name.encode("ascii")
            + b"\x00"
            + master_seed
            + attempt.to_bytes(4, "big")
        ).digest()
        graph = generate_holonomy_graph(graph_parameters, attempt_seed)
        tree = set(graph.spanning_tree_edges())

        voltage_rng = _DeterministicRng(
            hashlib.sha256(
                b"MORPH-KEM H3-E0 canonical voltages v1\x00" + attempt_seed
            ).digest()
        )
        canonical: list[Permutation] = []
        for edge in graph.edges:
            if edge in tree:
                canonical.append(_identity(parameters.sheets))
            else:
                canonical.append(
                    _random_permutation(parameters.sheets, voltage_rng)
                )

        canonical_tuple = tuple(canonical)
        if _monodromy_orbit_size(
            graph,
            canonical_tuple,
            parameters.sheets,
        ) != parameters.sheets:
            continue

        gauge_rng = _DeterministicRng(
            hashlib.sha256(
                b"MORPH-KEM H3-E0 secret fiber gauges v1\x00" + attempt_seed
            ).digest()
        )
        gauges = tuple(
            _random_permutation(parameters.sheets, gauge_rng)
            for _ in range(parameters.base_vertices)
        )

        public_transitions: list[Permutation] = []
        for edge, canonical_transition in zip(graph.edges, canonical_tuple):
            left, right = edge
            public_transitions.append(
                _compose(
                    gauges[right],
                    _compose(
                        canonical_transition,
                        _inverse(gauges[left]),
                    ),
                )
            )

        public = LiftedAtlasPublic(
            parameters,
            graph,
            tuple(public_transitions),
        )
        reference = LiftedAtlasReference(
            canonical_tuple,
            gauges,
        )
        return public, reference

    raise LiftedAtlasError("could not generate connected H3-E0 cover")


def canonicalize_public_cover(
    public: LiftedAtlasPublic,
) -> GaugeNormalization:
    """Publicly gauge-fix every spanning-tree transition to identity."""
    sheets = public.parameters.sheets
    identity = _identity(sheets)
    tree_edges = set(public.graph.spanning_tree_edges())
    adjacency: list[list[int]] = [[] for _ in range(public.graph.vertices)]
    for left, right in tree_edges:
        adjacency[left].append(right)
        adjacency[right].append(left)
    for values in adjacency:
        values.sort()

    gauges: list[Permutation | None] = [None] * public.graph.vertices
    gauges[0] = identity
    queue = [0]
    point_ops = 0

    while queue:
        parent = queue.pop(0)
        parent_gauge = gauges[parent]
        assert parent_gauge is not None
        for child in adjacency[parent]:
            if gauges[child] is not None:
                continue
            transition = _oriented_transition(public, parent, child)
            gauges[child] = _compose(
                parent_gauge,
                _inverse(transition),
            )
            point_ops += 2 * sheets
            queue.append(child)

    fixed_gauges = tuple(
        value if value is not None else identity
        for value in gauges
    )

    normalized: list[Permutation] = []
    for edge, transition in zip(public.graph.edges, public.transitions):
        left, right = edge
        normalized.append(
            _compose(
                fixed_gauges[right],
                _compose(
                    transition,
                    _inverse(fixed_gauges[left]),
                ),
            )
        )
        point_ops += 3 * sheets

    tree_identity = sum(
        normalized[index] == identity
        for index, edge in enumerate(public.graph.edges)
        if edge in tree_edges
    )

    return GaugeNormalization(
        fixed_gauges,
        tuple(normalized),
        tree_identity,
        len(public.graph.chord_edges()),
        point_ops,
    )


def compare_to_reference(
    public: LiftedAtlasPublic,
    reference: LiftedAtlasReference,
    normalization: GaugeNormalization,
) -> ReferenceComparison:
    if len(reference.secret_fiber_gauges) != public.graph.vertices:
        raise LiftedAtlasError("reference gauge count does not match public graph")
    root = reference.secret_fiber_gauges[0]
    expected = tuple(
        _conjugate(value, root)
        for value in reference.canonical_transitions
    )
    return ReferenceComparison(
        expected == normalization.normalized_transitions,
        root,
    )


def lift_path(
    graph: HolonomyGraph,
    transitions: tuple[Permutation, ...],
    path: tuple[int, ...],
    start_sheet: int,
) -> int:
    if len(path) < 1:
        raise LiftedAtlasError("path must contain at least one vertex")
    sheet_count = len(transitions[0])
    if start_sheet < 0 or start_sheet >= sheet_count:
        raise LiftedAtlasError("start sheet outside public range")

    neighbors = graph.neighbors()
    current_sheet = start_sheet
    for source, target in zip(path, path[1:]):
        if target not in neighbors[source]:
            raise LiftedAtlasError("path uses a non-edge")
        transition = _oriented_from_table(
            graph,
            transitions,
            source,
            target,
        )
        current_sheet = transition[current_sheet]
    return current_sheet


def check_lift_equivariance(
    public: LiftedAtlasPublic,
    normalization: GaugeNormalization,
    path: tuple[int, ...],
    public_start_sheet: int,
) -> LiftEquivariance:
    if not path:
        raise LiftedAtlasError("path must not be empty")

    public_end = lift_path(
        public.graph,
        public.transitions,
        path,
        public_start_sheet,
    )

    start_vertex = path[0]
    end_vertex = path[-1]
    normalized_start = normalization.public_gauges[start_vertex][public_start_sheet]
    normalized_end = lift_path(
        public.graph,
        normalization.normalized_transitions,
        path,
        normalized_start,
    )
    expected = normalization.public_gauges[end_vertex][public_end]

    return LiftEquivariance(
        public_end,
        normalized_start,
        normalized_end,
        expected,
        normalized_end == expected,
    )


def residual_root_relabelings(public: LiftedAtlasPublic) -> int:
    """Number of global root sheet labels before quotienting cover equivalence."""
    return math.factorial(public.parameters.sheets)
