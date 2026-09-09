from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from collections import deque

from .complex import Simplex, SimplicialComplex

Edge = tuple[int, int]


class KleinBottleError(ValueError):
    """Raised when a K0 Klein-bottle control input is invalid."""


@dataclass(frozen=True, slots=True)
class KleinBottleParameters:
    name: str
    width: int
    height: int

    def validate(self) -> None:
        if self.width < 4 or self.width > 64:
            raise KleinBottleError("K0 width must be in [4, 64]")
        if self.height < 4 or self.height > 64:
            raise KleinBottleError("K0 height must be in [4, 64]")


KLEIN_BOTTLE_PARAMETER_SETS = {
    "klein-bottle-4x4": KleinBottleParameters("klein-bottle-4x4", 4, 4),
    "klein-bottle-5x4": KleinBottleParameters("klein-bottle-5x4", 5, 4),
    "klein-bottle-6x4": KleinBottleParameters("klein-bottle-6x4", 6, 4),
}


@dataclass(frozen=True, slots=True)
class OrientationDualEdge:
    left_face: int
    right_face: int
    primal_edge: Edge
    canonical_transition: int

    def __post_init__(self) -> None:
        if self.left_face < 0 or self.right_face <= self.left_face:
            raise KleinBottleError("dual edge face ordering is invalid")
        if len(self.primal_edge) != 2 or self.primal_edge[0] >= self.primal_edge[1]:
            raise KleinBottleError("primal edge must be canonically ordered")
        if self.canonical_transition not in (0, 1):
            raise KleinBottleError("orientation transition must be a bit")


@dataclass(frozen=True, slots=True)
class KleinBottleScaffold:
    parameters: KleinBottleParameters
    complex: SimplicialComplex
    faces: tuple[Simplex, ...]
    edges: tuple[Edge, ...]
    dual_edges: tuple[OrientationDualEdge, ...]
    version: int = 1

    def __post_init__(self) -> None:
        self.parameters.validate()
        if self.version != 1:
            raise KleinBottleError("unsupported K0 scaffold version")
        expected_vertices = self.parameters.width * self.parameters.height
        if len(self.complex.vertices) != expected_vertices:
            raise KleinBottleError("unexpected K0 vertex count")
        if len(self.faces) != 2 * expected_vertices:
            raise KleinBottleError("unexpected K0 face count")
        if len(self.edges) != 3 * expected_vertices:
            raise KleinBottleError("unexpected K0 edge count")
        if len(self.dual_edges) != len(self.edges):
            raise KleinBottleError("every primal edge must define one dual edge")
        if self.euler_characteristic != 0:
            raise KleinBottleError("K0 quotient must have Euler characteristic zero")
        if self.complex.dimension != 2:
            raise KleinBottleError("K0 scaffold must be two-dimensional")

    @property
    def euler_characteristic(self) -> int:
        return len(self.complex.vertices) - len(self.edges) + len(self.faces)

    @property
    def dual_cycle_rank(self) -> int:
        return len(self.dual_edges) - len(self.faces) + 1

    def encode(self) -> bytes:
        payload = {
            "complex": self.complex.encode().hex(),
            "parameters": {
                "height": self.parameters.height,
                "name": self.parameters.name,
                "width": self.parameters.width,
            },
            "version": self.version,
        }
        return json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")


@dataclass(frozen=True, slots=True)
class KleinBottlePublic:
    scaffold: KleinBottleScaffold
    transitions: tuple[int, ...]
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise KleinBottleError("unsupported K0 public version")
        if len(self.transitions) != len(self.scaffold.dual_edges):
            raise KleinBottleError("public transition count mismatch")
        if any(bit not in (0, 1) for bit in self.transitions):
            raise KleinBottleError("public transitions must be bits")

    def encode(self) -> bytes:
        payload = {
            "scaffold": json.loads(self.scaffold.encode().decode("ascii")),
            "transitions": list(self.transitions),
            "version": self.version,
        }
        return json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")


@dataclass(frozen=True, slots=True)
class KleinBottleReference:
    face_gauges: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class KleinGaugeNormalization:
    gauge: tuple[int, ...]
    tree_edge_indices: tuple[int, ...]
    normalized_transitions: tuple[int, ...]
    fundamental_syndromes: tuple[int, ...]
    nonzero_syndromes: int
    operations: int


@dataclass(frozen=True, slots=True)
class KleinOrientability:
    orientable: bool
    cycle_rank: int
    fundamental_syndromes: tuple[int, ...]
    nonzero_syndromes: int


@dataclass(frozen=True, slots=True)
class KleinGaugeRecovery:
    consistent: bool
    face_gauges_up_to_global: tuple[int, ...]
    edge_checks: int


class _DeterministicBitStream:
    def __init__(self, seed: bytes):
        self._seed = seed
        self._counter = 0

    def bit(self) -> int:
        block = hashlib.sha256(
            b"MORPH-KEM K0 Klein gauge v1\x00"
            + self._seed
            + self._counter.to_bytes(8, "big")
        ).digest()
        self._counter += 1
        return block[0] & 1


def _vertex(width: int, i: int, j: int) -> int:
    return j * width + (i % width)


def _face_edge_direction(face: Simplex, edge: Edge) -> int:
    a, b, c = face
    for source, target in ((a, b), (b, c), (c, a)):
        if tuple(sorted((source, target))) == edge:
            return 0 if (source, target) == edge else 1
    raise KleinBottleError("edge is not in requested face")


def build_klein_bottle(parameters: KleinBottleParameters) -> KleinBottleScaffold:
    parameters.validate()
    width = parameters.width
    height = parameters.height

    facets: set[Simplex] = set()
    for j in range(height):
        for i in range(width):
            a = _vertex(width, i, j)
            b = _vertex(width, i + 1, j)
            if j < height - 1:
                d = _vertex(width, i, j + 1)
                c = _vertex(width, i + 1, j + 1)
            else:
                # (x, height) ~ (-x, 0): the orientation-reversing
                # boundary identification defining the Klein-bottle quotient.
                d = _vertex(width, -i, 0)
                c = _vertex(width, -(i + 1), 0)

            left = tuple(sorted((a, b, c)))
            right = tuple(sorted((a, c, d)))
            if len(set(left)) != 3 or len(set(right)) != 3:
                raise KleinBottleError("degenerate quotient triangle")
            facets.add(left)
            facets.add(right)

    expected_faces = 2 * width * height
    if len(facets) != expected_faces:
        raise KleinBottleError("quotient produced duplicate triangles")

    complex_ = SimplicialComplex.from_facets(sorted(facets))
    faces = tuple(simplex for simplex in complex_.simplices if len(simplex) == 3)
    edges = tuple(simplex for simplex in complex_.simplices if len(simplex) == 2)

    incidences: dict[Edge, list[tuple[int, int]]] = {edge: [] for edge in edges}
    for face_index, face in enumerate(faces):
        a, b, c = face
        for source, target in ((a, b), (b, c), (c, a)):
            edge = tuple(sorted((source, target)))
            direction = 0 if (source, target) == edge else 1
            incidences[edge].append((face_index, direction))

    dual_edges: list[OrientationDualEdge] = []
    for edge in edges:
        incident = incidences[edge]
        if len(incident) != 2:
            raise KleinBottleError("K0 must be closed: every edge needs two faces")
        (first_face, first_direction), (second_face, second_direction) = incident
        if first_face > second_face:
            first_face, second_face = second_face, first_face
            first_direction, second_direction = second_direction, first_direction
        transition = 1 ^ first_direction ^ second_direction
        dual_edges.append(
            OrientationDualEdge(
                first_face,
                second_face,
                edge,
                transition,
            )
        )

    dual_edges.sort(
        key=lambda item: (
            item.left_face,
            item.right_face,
            item.primal_edge,
        )
    )

    scaffold = KleinBottleScaffold(
        parameters=parameters,
        complex=complex_,
        faces=faces,
        edges=edges,
        dual_edges=tuple(dual_edges),
    )

    # Verify the direction helper against every recorded incidence.
    for item in scaffold.dual_edges:
        _face_edge_direction(scaffold.faces[item.left_face], item.primal_edge)
        _face_edge_direction(scaffold.faces[item.right_face], item.primal_edge)

    return scaffold


def _dual_adjacency(
    scaffold: KleinBottleScaffold,
) -> tuple[tuple[tuple[int, int], ...], ...]:
    adjacency: list[list[tuple[int, int]]] = [
        [] for _ in scaffold.faces
    ]
    for edge_index, edge in enumerate(scaffold.dual_edges):
        adjacency[edge.left_face].append((edge.right_face, edge_index))
        adjacency[edge.right_face].append((edge.left_face, edge_index))
    for neighbors in adjacency:
        neighbors.sort()
    return tuple(tuple(neighbors) for neighbors in adjacency)


def normalize_klein_transitions(
    scaffold: KleinBottleScaffold,
    transitions: tuple[int, ...],
) -> KleinGaugeNormalization:
    if len(transitions) != len(scaffold.dual_edges):
        raise KleinBottleError("transition count mismatch")
    if any(bit not in (0, 1) for bit in transitions):
        raise KleinBottleError("transitions must be bits")

    adjacency = _dual_adjacency(scaffold)
    gauge: list[int | None] = [None] * len(scaffold.faces)
    gauge[0] = 0
    queue: deque[int] = deque([0])
    tree_edges: set[int] = set()

    while queue:
        face = queue.popleft()
        assert gauge[face] is not None
        for neighbor, edge_index in adjacency[face]:
            if gauge[neighbor] is not None:
                continue
            gauge[neighbor] = gauge[face] ^ transitions[edge_index]
            tree_edges.add(edge_index)
            queue.append(neighbor)

    if any(value is None for value in gauge):
        raise KleinBottleError("dual graph is disconnected")

    final_gauge = tuple(int(value) for value in gauge)
    normalized = tuple(
        transition
        ^ final_gauge[edge.left_face]
        ^ final_gauge[edge.right_face]
        for transition, edge in zip(transitions, scaffold.dual_edges)
    )

    if any(normalized[index] for index in tree_edges):
        raise KleinBottleError("tree gauge normalization failed")

    non_tree = tuple(
        normalized[index]
        for index in range(len(normalized))
        if index not in tree_edges
    )

    return KleinGaugeNormalization(
        gauge=final_gauge,
        tree_edge_indices=tuple(sorted(tree_edges)),
        normalized_transitions=normalized,
        fundamental_syndromes=non_tree,
        nonzero_syndromes=sum(non_tree),
        operations=len(tree_edges) + len(scaffold.dual_edges),
    )


def analyze_klein_orientability(
    scaffold: KleinBottleScaffold,
) -> KleinOrientability:
    canonical = tuple(
        edge.canonical_transition
        for edge in scaffold.dual_edges
    )
    normalized = normalize_klein_transitions(scaffold, canonical)
    return KleinOrientability(
        orientable=normalized.nonzero_syndromes == 0,
        cycle_rank=scaffold.dual_cycle_rank,
        fundamental_syndromes=normalized.fundamental_syndromes,
        nonzero_syndromes=normalized.nonzero_syndromes,
    )


def generate_klein_orientation_instance(
    parameters: KleinBottleParameters,
    master_seed: bytes,
) -> tuple[KleinBottlePublic, KleinBottleReference]:
    if not isinstance(master_seed, bytes) or not master_seed:
        raise KleinBottleError("master_seed must be non-empty bytes")

    scaffold = build_klein_bottle(parameters)
    stream = _DeterministicBitStream(
        hashlib.sha256(
            b"MORPH-KEM K0 instance v1\x00"
            + parameters.name.encode("ascii")
            + b"\x00"
            + master_seed
        ).digest()
    )
    gauges = tuple(stream.bit() for _ in scaffold.faces)
    transitions = tuple(
        edge.canonical_transition
        ^ gauges[edge.left_face]
        ^ gauges[edge.right_face]
        for edge in scaffold.dual_edges
    )
    public = KleinBottlePublic(scaffold, transitions)
    reference = KleinBottleReference(gauges)
    if not validate_klein_reference(public, reference):
        raise KleinBottleError("internal K0 reference validation failed")
    return public, reference


def validate_klein_reference(
    public: KleinBottlePublic,
    reference: KleinBottleReference,
) -> bool:
    if len(reference.face_gauges) != len(public.scaffold.faces):
        return False
    if any(bit not in (0, 1) for bit in reference.face_gauges):
        return False
    for transition, edge in zip(
        public.transitions,
        public.scaffold.dual_edges,
    ):
        expected = (
            edge.canonical_transition
            ^ reference.face_gauges[edge.left_face]
            ^ reference.face_gauges[edge.right_face]
        )
        if transition != expected:
            return False
    return True


def recover_klein_gauge(public: KleinBottlePublic) -> KleinGaugeRecovery:
    delta = tuple(
        transition ^ edge.canonical_transition
        for transition, edge in zip(
            public.transitions,
            public.scaffold.dual_edges,
        )
    )
    normalized = normalize_klein_transitions(public.scaffold, delta)
    consistent = not any(normalized.normalized_transitions)
    return KleinGaugeRecovery(
        consistent=consistent,
        face_gauges_up_to_global=normalized.gauge,
        edge_checks=len(public.scaffold.dual_edges),
    )


def reference_gauge_matches(
    recovery: KleinGaugeRecovery,
    reference: KleinBottleReference,
) -> bool:
    if not recovery.consistent:
        return False
    if len(recovery.face_gauges_up_to_global) != len(reference.face_gauges):
        return False
    root = reference.face_gauges[0]
    expected = tuple(bit ^ root for bit in reference.face_gauges)
    return recovery.face_gauges_up_to_global == expected
