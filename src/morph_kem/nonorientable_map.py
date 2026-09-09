from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import hashlib
import json

Edge = tuple[int, int]
Face = tuple[int, ...]


class NonOrientableMapError(ValueError):
    """Raised when a K1 non-orientable regular-map input is invalid."""


@dataclass(frozen=True, slots=True)
class CellDualEdge:
    left_face: int
    right_face: int
    primal_edge: Edge
    canonical_transition: int

    def __post_init__(self) -> None:
        if self.left_face < 0 or self.right_face <= self.left_face:
            raise NonOrientableMapError("dual edge face ordering is invalid")
        if len(self.primal_edge) != 2 or self.primal_edge[0] >= self.primal_edge[1]:
            raise NonOrientableMapError("primal edge must be canonical")
        if self.canonical_transition not in (0, 1):
            raise NonOrientableMapError("orientation transition must be a bit")


@dataclass(frozen=True, slots=True)
class RegularCellMap:
    name: str
    vertices: tuple[int, ...]
    edges: tuple[Edge, ...]
    faces: tuple[Face, ...]
    dual_edges: tuple[CellDualEdge, ...]
    vertex_degrees: tuple[int, ...]
    edge_face_degrees: tuple[int, ...]
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise NonOrientableMapError("unsupported K1 cell-map version")
        if self.vertices != tuple(range(len(self.vertices))):
            raise NonOrientableMapError("cell-map vertices must be canonical")
        if not self.faces:
            raise NonOrientableMapError("cell map must contain faces")
        if len(self.dual_edges) != len(self.edges):
            raise NonOrientableMapError("closed map needs one dual edge per primal edge")
        if any(degree != 2 for degree in self.edge_face_degrees):
            raise NonOrientableMapError("every edge must lie in exactly two faces")

    @property
    def euler_characteristic(self) -> int:
        return len(self.vertices) - len(self.edges) + len(self.faces)

    @property
    def dual_cycle_rank(self) -> int:
        return len(self.dual_edges) - len(self.faces) + 1

    @property
    def face_sizes(self) -> tuple[int, ...]:
        return tuple(len(face) for face in self.faces)

    def encode(self) -> bytes:
        payload = {
            "edges": [list(edge) for edge in self.edges],
            "faces": [list(face) for face in self.faces],
            "name": self.name,
            "version": self.version,
            "vertices": list(self.vertices),
        }
        return json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")


@dataclass(frozen=True, slots=True)
class CellGaugeNormalization:
    gauge: tuple[int, ...]
    tree_edge_indices: tuple[int, ...]
    normalized_transitions: tuple[int, ...]
    fundamental_syndromes: tuple[int, ...]
    nonzero_syndromes: int


@dataclass(frozen=True, slots=True)
class CellOrientability:
    orientable: bool
    cycle_rank: int
    fundamental_syndromes: tuple[int, ...]
    nonzero_syndromes: int


@dataclass(frozen=True, slots=True)
class K1PublicInstance:
    base_map: RegularCellMap
    transitions: tuple[int, ...]

    def __post_init__(self) -> None:
        if len(self.transitions) != len(self.base_map.dual_edges):
            raise NonOrientableMapError("K1 transition count mismatch")
        if any(bit not in (0, 1) for bit in self.transitions):
            raise NonOrientableMapError("K1 transitions must be bits")

    def encode(self) -> bytes:
        payload = {
            "base_map": json.loads(self.base_map.encode().decode("ascii")),
            "transitions": list(self.transitions),
            "version": 1,
        }
        return json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")


@dataclass(frozen=True, slots=True)
class K1Reference:
    face_gauges: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class K1GaugeRecovery:
    consistent: bool
    face_gauges_up_to_global: tuple[int, ...]
    edge_checks: int


@dataclass(frozen=True, slots=True)
class OrientationDoubleCover:
    cover: RegularCellMap
    vertex_projection: tuple[int, ...]
    face_projection: tuple[int, ...]
    reconstructed_from_public_transitions: bool


class _DeterministicBitStream:
    def __init__(self, seed: bytes):
        self._seed = seed
        self._counter = 0

    def bit(self) -> int:
        block = hashlib.sha256(
            b"MORPH-KEM K1 map gauge v1\x00"
            + self._seed
            + self._counter.to_bytes(8, "big")
        ).digest()
        self._counter += 1
        return block[0] & 1


class _Dsu:
    def __init__(self) -> None:
        self.parent: dict[tuple[int, int, int], tuple[int, int, int]] = {}

    def add(self, item: tuple[int, int, int]) -> None:
        self.parent.setdefault(item, item)

    def find(self, item: tuple[int, int, int]) -> tuple[int, int, int]:
        parent = self.parent[item]
        if parent != item:
            self.parent[item] = self.find(parent)
        return self.parent[item]

    def union(
        self,
        left: tuple[int, int, int],
        right: tuple[int, int, int],
    ) -> None:
        self.add(left)
        self.add(right)
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root != right_root:
            if left_root < right_root:
                self.parent[right_root] = left_root
            else:
                self.parent[left_root] = right_root


def _build_cell_map(name: str, vertex_count: int, faces: tuple[Face, ...]) -> RegularCellMap:
    if vertex_count <= 0:
        raise NonOrientableMapError("vertex count must be positive")

    edge_incidences: dict[Edge, list[tuple[int, int]]] = {}
    for face_index, face in enumerate(faces):
        if len(face) < 3 or len(set(face)) != len(face):
            raise NonOrientableMapError("cell-map face must be a simple polygon")
        if any(vertex < 0 or vertex >= vertex_count for vertex in face):
            raise NonOrientableMapError("face vertex outside public vertex set")
        for index, source in enumerate(face):
            target = face[(index + 1) % len(face)]
            if source == target:
                raise NonOrientableMapError("face boundary repeats an edge endpoint")
            edge = tuple(sorted((source, target)))
            direction = 0 if (source, target) == edge else 1
            edge_incidences.setdefault(edge, []).append((face_index, direction))

    edges = tuple(sorted(edge_incidences))
    dual_edges: list[CellDualEdge] = []
    for edge in edges:
        incidences = edge_incidences[edge]
        if len(incidences) != 2:
            raise NonOrientableMapError("map is not closed at a primal edge")
        (first_face, first_direction), (second_face, second_direction) = incidences
        if first_face == second_face:
            raise NonOrientableMapError("self-adjacent face edge is unsupported in K1")
        if first_face > second_face:
            first_face, second_face = second_face, first_face
            first_direction, second_direction = second_direction, first_direction
        dual_edges.append(
            CellDualEdge(
                first_face,
                second_face,
                edge,
                1 ^ first_direction ^ second_direction,
            )
        )

    dual_edges.sort(
        key=lambda item: (
            item.left_face,
            item.right_face,
            item.primal_edge,
        )
    )

    degrees = [0] * vertex_count
    for left, right in edges:
        degrees[left] += 1
        degrees[right] += 1

    edge_face_degrees = tuple(
        len(edge_incidences[edge])
        for edge in edges
    )
    return RegularCellMap(
        name=name,
        vertices=tuple(range(vertex_count)),
        edges=edges,
        faces=faces,
        dual_edges=tuple(dual_edges),
        vertex_degrees=tuple(degrees),
        edge_face_degrees=edge_face_degrees,
    )


def generate_n4_6_4_3_map() -> RegularCellMap:
    """Construct N4:{6,4}_3 as the Petrie-dual face system of the octahedron.

    Vertices are the six signed coordinate-axis vertices of the octahedral
    graph K_{2,2,2}. The four six-cycles are its Petrie polygons.
    """
    faces: tuple[Face, ...] = (
        (0, 2, 4, 1, 3, 5),
        (0, 2, 5, 1, 3, 4),
        (0, 3, 4, 1, 2, 5),
        (0, 3, 5, 1, 2, 4),
    )
    result = _build_cell_map("N4:{6,4}_3", 6, faces)
    if len(result.edges) != 12:
        raise NonOrientableMapError("N4 map must have 12 edges")
    if result.euler_characteristic != -2:
        raise NonOrientableMapError("N4 map must have Euler characteristic -2")
    if set(result.vertex_degrees) != {4}:
        raise NonOrientableMapError("N4 map must be 4-valent")
    if set(result.face_sizes) != {6}:
        raise NonOrientableMapError("N4 map must have hexagonal faces")

    opposite = {(0, 1), (2, 3), (4, 5)}
    expected_edges = {
        (left, right)
        for left in range(6)
        for right in range(left + 1, 6)
        if (left, right) not in opposite
    }
    if set(result.edges) != expected_edges:
        raise NonOrientableMapError("N4 skeleton must be K_{2,2,2}")
    return result


def regular_type_is_hyperbolic(face_size: int, vertex_degree: int) -> bool:
    if face_size < 3 or vertex_degree < 3:
        raise NonOrientableMapError("regular type values must be at least three")
    return 2 * (face_size + vertex_degree) < face_size * vertex_degree


def _dual_adjacency(
    cell_map: RegularCellMap,
) -> tuple[tuple[tuple[int, int], ...], ...]:
    adjacency: list[list[tuple[int, int]]] = [
        [] for _ in cell_map.faces
    ]
    for edge_index, edge in enumerate(cell_map.dual_edges):
        adjacency[edge.left_face].append((edge.right_face, edge_index))
        adjacency[edge.right_face].append((edge.left_face, edge_index))
    for neighbors in adjacency:
        neighbors.sort()
    return tuple(tuple(neighbors) for neighbors in adjacency)


def normalize_cell_transitions(
    cell_map: RegularCellMap,
    transitions: tuple[int, ...],
) -> CellGaugeNormalization:
    if len(transitions) != len(cell_map.dual_edges):
        raise NonOrientableMapError("transition count mismatch")
    if any(bit not in (0, 1) for bit in transitions):
        raise NonOrientableMapError("transitions must be bits")

    adjacency = _dual_adjacency(cell_map)
    gauge: list[int | None] = [None] * len(cell_map.faces)
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
        raise NonOrientableMapError("dual graph is disconnected")

    final_gauge = tuple(int(value) for value in gauge)
    normalized = tuple(
        transition
        ^ final_gauge[edge.left_face]
        ^ final_gauge[edge.right_face]
        for transition, edge in zip(transitions, cell_map.dual_edges)
    )
    if any(normalized[index] for index in tree_edges):
        raise NonOrientableMapError("tree gauge normalization failed")

    syndromes = tuple(
        normalized[index]
        for index in range(len(normalized))
        if index not in tree_edges
    )
    return CellGaugeNormalization(
        gauge=final_gauge,
        tree_edge_indices=tuple(sorted(tree_edges)),
        normalized_transitions=normalized,
        fundamental_syndromes=syndromes,
        nonzero_syndromes=sum(syndromes),
    )


def analyze_cell_orientability(cell_map: RegularCellMap) -> CellOrientability:
    canonical = tuple(
        edge.canonical_transition
        for edge in cell_map.dual_edges
    )
    normalized = normalize_cell_transitions(cell_map, canonical)
    return CellOrientability(
        orientable=normalized.nonzero_syndromes == 0,
        cycle_rank=cell_map.dual_cycle_rank,
        fundamental_syndromes=normalized.fundamental_syndromes,
        nonzero_syndromes=normalized.nonzero_syndromes,
    )


def generate_k1_orientation_instance(
    master_seed: bytes,
) -> tuple[K1PublicInstance, K1Reference]:
    if not isinstance(master_seed, bytes) or not master_seed:
        raise NonOrientableMapError("master_seed must be non-empty bytes")

    base_map = generate_n4_6_4_3_map()
    stream = _DeterministicBitStream(
        hashlib.sha256(
            b"MORPH-KEM K1 N4 orientation instance v1\x00"
            + master_seed
        ).digest()
    )
    gauges = tuple(stream.bit() for _ in base_map.faces)
    transitions = tuple(
        edge.canonical_transition
        ^ gauges[edge.left_face]
        ^ gauges[edge.right_face]
        for edge in base_map.dual_edges
    )
    public = K1PublicInstance(base_map, transitions)
    reference = K1Reference(gauges)
    if not validate_k1_reference(public, reference):
        raise NonOrientableMapError("internal K1 reference validation failed")
    return public, reference


def validate_k1_reference(
    public: K1PublicInstance,
    reference: K1Reference,
) -> bool:
    if len(reference.face_gauges) != len(public.base_map.faces):
        return False
    if any(bit not in (0, 1) for bit in reference.face_gauges):
        return False
    for transition, edge in zip(public.transitions, public.base_map.dual_edges):
        expected = (
            edge.canonical_transition
            ^ reference.face_gauges[edge.left_face]
            ^ reference.face_gauges[edge.right_face]
        )
        if transition != expected:
            return False
    return True


def recover_k1_gauge(public: K1PublicInstance) -> K1GaugeRecovery:
    delta = tuple(
        transition ^ edge.canonical_transition
        for transition, edge in zip(
            public.transitions,
            public.base_map.dual_edges,
        )
    )
    normalized = normalize_cell_transitions(public.base_map, delta)
    return K1GaugeRecovery(
        consistent=not any(normalized.normalized_transitions),
        face_gauges_up_to_global=normalized.gauge,
        edge_checks=len(public.base_map.dual_edges),
    )


def k1_reference_gauge_matches(
    recovery: K1GaugeRecovery,
    reference: K1Reference,
) -> bool:
    if not recovery.consistent:
        return False
    root = reference.face_gauges[0]
    expected = tuple(bit ^ root for bit in reference.face_gauges)
    return recovery.face_gauges_up_to_global == expected


def build_orientation_double_cover(
    base_map: RegularCellMap,
    transitions: tuple[int, ...] | None = None,
) -> OrientationDoubleCover:
    if transitions is None:
        transitions = tuple(
            edge.canonical_transition
            for edge in base_map.dual_edges
        )
        reconstructed_from_public = False
    else:
        if len(transitions) != len(base_map.dual_edges):
            raise NonOrientableMapError("double-cover transition count mismatch")
        if any(bit not in (0, 1) for bit in transitions):
            raise NonOrientableMapError("double-cover transitions must be bits")
        reconstructed_from_public = True

    dsu = _Dsu()
    for face_index, face in enumerate(base_map.faces):
        for sheet in (0, 1):
            for vertex in face:
                dsu.add((face_index, sheet, vertex))

    for transition, dual_edge in zip(transitions, base_map.dual_edges):
        for sheet in (0, 1):
            neighbor_sheet = sheet ^ transition
            for vertex in dual_edge.primal_edge:
                dsu.union(
                    (dual_edge.left_face, sheet, vertex),
                    (dual_edge.right_face, neighbor_sheet, vertex),
                )

    groups: dict[
        tuple[int, int, int],
        list[tuple[int, int, int]],
    ] = {}
    for local_vertex in sorted(dsu.parent):
        root = dsu.find(local_vertex)
        groups.setdefault(root, []).append(local_vertex)

    ordered_roots = sorted(
        groups,
        key=lambda root: min(groups[root]),
    )
    root_index = {
        root: index
        for index, root in enumerate(ordered_roots)
    }

    vertex_projection: list[int] = []
    for root in ordered_roots:
        original_vertices = {
            item[2] for item in groups[root]
        }
        if len(original_vertices) != 1:
            raise NonOrientableMapError("orientation cover mixed base vertices")
        vertex_projection.append(next(iter(original_vertices)))

    lifted_faces: list[Face] = []
    face_projection: list[int] = []
    for face_index, face in enumerate(base_map.faces):
        for sheet in (0, 1):
            boundary = face if sheet == 0 else tuple(reversed(face))
            lifted = tuple(
                root_index[dsu.find((face_index, sheet, vertex))]
                for vertex in boundary
            )
            if len(set(lifted)) != len(lifted):
                raise NonOrientableMapError("lifted face is not a simple polygon")
            lifted_faces.append(lifted)
            face_projection.append(face_index)

    cover = _build_cell_map(
        f"orientation-double-cover({base_map.name})",
        len(ordered_roots),
        tuple(lifted_faces),
    )
    return OrientationDoubleCover(
        cover=cover,
        vertex_projection=tuple(vertex_projection),
        face_projection=tuple(face_projection),
        reconstructed_from_public_transitions=reconstructed_from_public,
    )
