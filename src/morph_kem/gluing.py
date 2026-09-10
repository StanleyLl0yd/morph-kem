from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import hashlib
from itertools import combinations


Triangle = tuple[int, int, int]
Tetrahedron = tuple[int, int, int, int]
TetrahedronGroup = tuple[int, ...]
DualEdge = tuple[int, int]


class GluingExperimentError(ValueError):
    """Raised when a G0 construction or witness is malformed."""


@dataclass(frozen=True, slots=True)
class GluingParameters:
    name: str
    piece_count: int
    tree_edges: tuple[DualEdge, ...]

    def validate(self) -> None:
        if self.piece_count < 2 or self.piece_count > 64:
            raise GluingExperimentError("G0 piece count outside toy bounds")
        if len(self.tree_edges) != self.piece_count - 1:
            raise GluingExperimentError("G0 assembly must contain n-1 gluing edges")

        adjacency = [set() for _ in range(self.piece_count)]
        for edge in self.tree_edges:
            if len(edge) != 2:
                raise GluingExperimentError("invalid G0 gluing edge")
            left, right = edge
            if left == right or not (0 <= left < self.piece_count) or not (0 <= right < self.piece_count):
                raise GluingExperimentError("G0 gluing edge endpoint outside piece range")
            if right in adjacency[left]:
                raise GluingExperimentError("duplicate G0 gluing edge")
            adjacency[left].add(right)
            adjacency[right].add(left)

        if any(len(neighbors) > 4 for neighbors in adjacency):
            raise GluingExperimentError("G0 piece exceeds its four boundary ports")

        seen = {0}
        stack = [0]
        while stack:
            current = stack.pop()
            for neighbor in adjacency[current]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        if len(seen) != self.piece_count:
            raise GluingExperimentError("G0 assembly graph must be connected")


G0_PARAMETER_SETS = {
    "g0-3": GluingParameters("g0-3", 3, ((0, 1), (1, 2))),
    "g0-5": GluingParameters("g0-5", 5, ((0, 1), (0, 2), (0, 3), (3, 4))),
    "g0-8": GluingParameters(
        "g0-8",
        8,
        ((0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 6), (3, 7)),
    ),
}


@dataclass(frozen=True, slots=True)
class GluingPublicInstance:
    name: str
    piece_count: int
    tetrahedra: tuple[Tetrahedron, ...]


@dataclass(frozen=True, slots=True)
class GluingReference:
    groups: tuple[TetrahedronGroup, ...]
    tree_edges: tuple[DualEdge, ...]
    port_pairs: tuple[tuple[int, int, int, int], ...]


@dataclass(frozen=True, slots=True)
class GluingIncidence:
    vertices: int
    edges: int
    faces: int
    tetrahedra: int
    boundary_faces: int
    max_face_incidence: int
    euler_characteristic: int
    dual_edges: int


@dataclass(frozen=True, slots=True)
class GluingValidation:
    valid: bool
    reason: str
    piece_count: int
    cross_faces: int
    component_sizes: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class BridgeRecovery:
    groups: tuple[TetrahedronGroup, ...]
    bridges: tuple[DualEdge, ...]
    bridge_faces: tuple[Triangle, ...]
    dual_edges: int
    face_occurrences: int
    dfs_edge_scans: int
    validation: GluingValidation


_BASE_TETRAHEDRA: tuple[Tetrahedron, ...] = (
    (0, 2, 3, 4),
    (0, 1, 3, 4),
    (0, 1, 2, 4),
    (0, 1, 2, 3),
)

# These are precisely the four boundary triangles of the 3-ball obtained by
# deleting the tetrahedron (1,2,3,4) from the boundary of a 4-simplex.
_BASE_PORTS: tuple[Triangle, ...] = (
    (2, 3, 4),
    (1, 3, 4),
    (1, 2, 4),
    (1, 2, 3),
)


class _UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, value: int) -> int:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union(self, left: int, right: int) -> None:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root == right_root:
            return
        if self.rank[left_root] < self.rank[right_root]:
            left_root, right_root = right_root, left_root
        self.parent[right_root] = left_root
        if self.rank[left_root] == self.rank[right_root]:
            self.rank[left_root] += 1


class _DeterministicRng:
    def __init__(self, domain: bytes, seed: bytes) -> None:
        self._domain = domain
        self._seed = seed
        self._counter = 0

    def randbelow(self, upper: int) -> int:
        if upper <= 0:
            raise ValueError("upper must be positive")
        limit = (1 << 256) - ((1 << 256) % upper)
        while True:
            digest = hashlib.sha256(
                self._domain
                + b"\x00"
                + self._seed
                + self._counter.to_bytes(8, "big")
            ).digest()
            self._counter += 1
            value = int.from_bytes(digest, "big")
            if value < limit:
                return value % upper

    def shuffle(self, values: list[int]) -> None:
        for index in range(len(values) - 1, 0, -1):
            other = self.randbelow(index + 1)
            values[index], values[other] = values[other], values[index]


def _normalize_groups(groups: tuple[TetrahedronGroup, ...]) -> tuple[TetrahedronGroup, ...]:
    return tuple(sorted(tuple(sorted(group)) for group in groups))


def _face_incidence(
    tetrahedra: tuple[Tetrahedron, ...],
) -> tuple[dict[Triangle, list[int]], int]:
    incidence: dict[Triangle, list[int]] = defaultdict(list)
    occurrences = 0
    for tetrahedron_index, tetrahedron in enumerate(tetrahedra):
        if len(tetrahedron) != 4 or len(set(tetrahedron)) != 4:
            raise GluingExperimentError("public G0 tetrahedron is degenerate")
        for face in combinations(tetrahedron, 3):
            incidence[tuple(sorted(face))].append(tetrahedron_index)
            occurrences += 1
    return dict(incidence), occurrences


def gluing_incidence(public: GluingPublicInstance) -> GluingIncidence:
    vertices: set[int] = set()
    edges: set[tuple[int, int]] = set()
    for tetrahedron in public.tetrahedra:
        vertices.update(tetrahedron)
        edges.update(tuple(sorted(edge)) for edge in combinations(tetrahedron, 2))

    faces, _ = _face_incidence(public.tetrahedra)
    max_face_incidence = max((len(owners) for owners in faces.values()), default=0)
    boundary_faces = sum(1 for owners in faces.values() if len(owners) == 1)
    dual_edges = sum(1 for owners in faces.values() if len(owners) == 2)
    tetrahedron_count = len(public.tetrahedra)
    euler = len(vertices) - len(edges) + len(faces) - tetrahedron_count

    return GluingIncidence(
        vertices=len(vertices),
        edges=len(edges),
        faces=len(faces),
        tetrahedra=tetrahedron_count,
        boundary_faces=boundary_faces,
        max_face_incidence=max_face_incidence,
        euler_characteristic=euler,
        dual_edges=dual_edges,
    )


def _piece_is_valid(public: GluingPublicInstance, group: TetrahedronGroup) -> bool:
    if len(group) != 4 or len(set(group)) != 4:
        return False
    if any(index < 0 or index >= len(public.tetrahedra) for index in group):
        return False

    tetrahedra = [set(public.tetrahedra[index]) for index in group]
    vertices = set().union(*tetrahedra)
    if len(vertices) != 5:
        return False

    common = set.intersection(*tetrahedra)
    if len(common) != 1:
        return False

    return all(len(left & right) == 3 for left, right in combinations(tetrahedra, 2))


def validate_gluing_witness(
    public: GluingPublicInstance,
    groups: tuple[TetrahedronGroup, ...],
) -> GluingValidation:
    normalized = _normalize_groups(groups)
    if len(normalized) != public.piece_count:
        return GluingValidation(False, "wrong piece count", len(normalized), 0, ())

    flattened = [index for group in normalized for index in group]
    if sorted(flattened) != list(range(len(public.tetrahedra))):
        return GluingValidation(False, "groups do not partition public tetrahedra", len(normalized), 0, ())

    if not all(_piece_is_valid(public, group) for group in normalized):
        return GluingValidation(False, "a recovered block is not the allowed 3-ball piece", len(normalized), 0, ())

    faces, _ = _face_incidence(public.tetrahedra)
    if any(len(owners) > 2 for owners in faces.values()):
        return GluingValidation(False, "public face has incidence above two", len(normalized), 0, ())

    owner_group: dict[int, int] = {}
    for group_index, group in enumerate(normalized):
        for tetrahedron_index in group:
            owner_group[tetrahedron_index] = group_index

    cross_pairs: list[DualEdge] = []
    for owners in faces.values():
        if len(owners) != 2:
            continue
        left_group = owner_group[owners[0]]
        right_group = owner_group[owners[1]]
        if left_group != right_group:
            cross_pairs.append(tuple(sorted((left_group, right_group))))

    if len(cross_pairs) != public.piece_count - 1:
        return GluingValidation(
            False,
            "cross-piece shared-face count is not n-1",
            len(normalized),
            len(cross_pairs),
            tuple(sorted(len(group) for group in normalized)),
        )

    adjacency = [set() for _ in range(public.piece_count)]
    for left, right in cross_pairs:
        adjacency[left].add(right)
        adjacency[right].add(left)

    seen = {0}
    stack = [0]
    while stack:
        current = stack.pop()
        for neighbor in adjacency[current]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)

    if len(seen) != public.piece_count:
        return GluingValidation(
            False,
            "cross-piece shared-face graph is disconnected",
            len(normalized),
            len(cross_pairs),
            tuple(sorted(len(group) for group in normalized)),
        )

    return GluingValidation(
        True,
        "accepted",
        len(normalized),
        len(cross_pairs),
        tuple(sorted(len(group) for group in normalized)),
    )


def _dual_graph(
    public: GluingPublicInstance,
) -> tuple[list[list[int]], dict[DualEdge, Triangle], int]:
    faces, occurrences = _face_incidence(public.tetrahedra)
    adjacency = [[] for _ in public.tetrahedra]
    edge_faces: dict[DualEdge, Triangle] = {}

    for face, owners in faces.items():
        if len(owners) > 2:
            raise GluingExperimentError("G0 public face incidence exceeds two")
        if len(owners) != 2:
            continue
        left, right = sorted(owners)
        edge = (left, right)
        if edge in edge_faces:
            raise GluingExperimentError("two public tetrahedra share multiple triangular faces")
        edge_faces[edge] = face
        adjacency[left].append(right)
        adjacency[right].append(left)

    for neighbors in adjacency:
        neighbors.sort()
    return adjacency, edge_faces, occurrences


def recover_gluing_by_dual_bridges(public: GluingPublicInstance) -> BridgeRecovery:
    adjacency, edge_faces, face_occurrences = _dual_graph(public)
    discovery = [-1] * len(adjacency)
    low = [-1] * len(adjacency)
    bridges: set[DualEdge] = set()
    timer = 0
    edge_scans = 0

    def visit(vertex: int, parent: int) -> None:
        nonlocal timer, edge_scans
        discovery[vertex] = timer
        low[vertex] = timer
        timer += 1

        for neighbor in adjacency[vertex]:
            edge_scans += 1
            if neighbor == parent:
                continue
            if discovery[neighbor] >= 0:
                low[vertex] = min(low[vertex], discovery[neighbor])
                continue
            visit(neighbor, vertex)
            low[vertex] = min(low[vertex], low[neighbor])
            if low[neighbor] > discovery[vertex]:
                bridges.add(tuple(sorted((vertex, neighbor))))

    for vertex in range(len(adjacency)):
        if discovery[vertex] < 0:
            visit(vertex, -1)

    seen: set[int] = set()
    groups: list[TetrahedronGroup] = []
    for start in range(len(adjacency)):
        if start in seen:
            continue
        seen.add(start)
        stack = [start]
        group: list[int] = []
        while stack:
            vertex = stack.pop()
            group.append(vertex)
            for neighbor in adjacency[vertex]:
                if tuple(sorted((vertex, neighbor))) in bridges or neighbor in seen:
                    continue
                seen.add(neighbor)
                stack.append(neighbor)
        groups.append(tuple(sorted(group)))

    normalized_groups = _normalize_groups(tuple(groups))
    normalized_bridges = tuple(sorted(bridges))
    bridge_faces = tuple(edge_faces[edge] for edge in normalized_bridges)
    validation = validate_gluing_witness(public, normalized_groups)

    return BridgeRecovery(
        groups=normalized_groups,
        bridges=normalized_bridges,
        bridge_faces=bridge_faces,
        dual_edges=len(edge_faces),
        face_occurrences=face_occurrences,
        dfs_edge_scans=edge_scans,
        validation=validation,
    )


def reference_partition_matches(
    reference: GluingReference,
    groups: tuple[TetrahedronGroup, ...],
) -> bool:
    return _normalize_groups(reference.groups) == _normalize_groups(groups)


def generate_gluing_instance(
    params: GluingParameters,
    master_seed: bytes,
) -> tuple[GluingPublicInstance, GluingReference]:
    params.validate()
    if len(master_seed) < 16:
        raise GluingExperimentError("G0 master seed must contain at least 128 bits")

    local_vertex_count = 5 * params.piece_count
    union_find = _UnionFind(local_vertex_count)

    local_tetrahedra: list[Tetrahedron] = []
    local_groups: list[TetrahedronGroup] = []
    for piece in range(params.piece_count):
        base = 5 * piece
        group: list[int] = []
        for tetrahedron in _BASE_TETRAHEDRA:
            group.append(len(local_tetrahedra))
            local_tetrahedra.append(tuple(base + vertex for vertex in tetrahedron))
        local_groups.append(tuple(group))

    next_port = [0] * params.piece_count
    port_pairs: list[tuple[int, int, int, int]] = []
    face_rng = _DeterministicRng(
        b"MORPH-KEM G0 gluing-map v1/" + params.name.encode("ascii"),
        master_seed,
    )

    for left_piece, right_piece in params.tree_edges:
        left_port = next_port[left_piece]
        right_port = next_port[right_piece]
        next_port[left_piece] += 1
        next_port[right_piece] += 1

        left_face = [5 * left_piece + vertex for vertex in _BASE_PORTS[left_port]]
        right_face = [5 * right_piece + vertex for vertex in _BASE_PORTS[right_port]]
        right_order = [0, 1, 2]
        face_rng.shuffle(right_order)
        for left_index, right_index in enumerate(right_order):
            union_find.union(left_face[left_index], right_face[right_index])

        port_pairs.append((left_piece, left_port, right_piece, right_port))

    roots = sorted({union_find.find(vertex) for vertex in range(local_vertex_count)})
    root_index = {root: index for index, root in enumerate(roots)}

    quotient_tetrahedra: list[Tetrahedron] = []
    for tetrahedron in local_tetrahedra:
        quotient = tuple(sorted(root_index[union_find.find(vertex)] for vertex in tetrahedron))
        if len(set(quotient)) != 4:
            raise GluingExperimentError("G0 gluing produced a degenerate tetrahedron")
        quotient_tetrahedra.append(quotient)

    if len(set(quotient_tetrahedra)) != len(quotient_tetrahedra):
        raise GluingExperimentError("G0 gluing produced duplicate tetrahedra")

    public_labels = list(range(len(roots)))
    label_rng = _DeterministicRng(
        b"MORPH-KEM G0 public-relabel v1/" + params.name.encode("ascii"),
        master_seed,
    )
    label_rng.shuffle(public_labels)

    relabeled = [
        tuple(sorted(public_labels[vertex] for vertex in tetrahedron))
        for tetrahedron in quotient_tetrahedra
    ]
    order = sorted(range(len(relabeled)), key=relabeled.__getitem__)
    public_tetrahedra = tuple(relabeled[index] for index in order)
    old_to_public = {old: new for new, old in enumerate(order)}

    reference_groups = _normalize_groups(
        tuple(
            tuple(old_to_public[tetrahedron_index] for tetrahedron_index in group)
            for group in local_groups
        )
    )

    public = GluingPublicInstance(
        name=params.name,
        piece_count=params.piece_count,
        tetrahedra=public_tetrahedra,
    )
    reference = GluingReference(
        groups=reference_groups,
        tree_edges=tuple(params.tree_edges),
        port_pairs=tuple(port_pairs),
    )

    incidence = gluing_incidence(public)
    if incidence.max_face_incidence > 2:
        raise GluingExperimentError("G0 generated non-pseudomanifold face incidence")
    if not validate_gluing_witness(public, reference.groups).valid:
        raise GluingExperimentError("G0 generated reference witness does not validate")

    return public, reference
