from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass

from .gluing import (
    DualEdge,
    GluingExperimentError,
    GluingPublicInstance,
    Tetrahedron,
    TetrahedronGroup,
    _DeterministicRng,
    _UnionFind,
    _dual_graph,
    _face_incidence,
    _normalize_groups,
    gluing_incidence,
)


@dataclass(frozen=True, slots=True)
class MatchingGluingParameters:
    name: str
    piece_count: int

    def validate(self) -> None:
        if self.piece_count < 3 or self.piece_count > 32:
            raise GluingExperimentError("G3 piece count outside toy bounds")


G3_PARAMETER_SETS = {
    "g3-3": MatchingGluingParameters("g3-3", 3),
    "g3-5": MatchingGluingParameters("g3-5", 5),
    "g3-8": MatchingGluingParameters("g3-8", 8),
}


@dataclass(frozen=True, slots=True)
class MatchingGluingReference:
    groups: tuple[TetrahedronGroup, ...]


@dataclass(frozen=True, slots=True)
class MatchingGluingValidation:
    valid: bool
    reason: str
    piece_count: int
    cross_faces: int
    component_sizes: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class MatchingRecovery:
    accepted_groups: tuple[tuple[TetrahedronGroup, ...], ...]
    dual_edges: int
    dual_degree_histogram: tuple[tuple[int, int], ...]
    bridge_count: int
    articulation_points: tuple[int, ...]
    allowed_candidate_edges: int
    vertex_star_candidate_pairs: int
    vertex_tetrahedron_degree_histogram: tuple[tuple[int, int], ...]
    matching_solutions: int
    matching_solution_cap: int
    matching_cap_hit: bool
    matching_nodes: int
    matching_backtracks: int
    accepted_solutions: int
    nonreference_accepted_solutions: int
    face_occurrences: int


_LOCAL_A: Tetrahedron = (0, 1, 2, 3)
_LOCAL_B: Tetrahedron = (0, 1, 2, 4)
# B_i outgoing face is glued to A_{i+1} incoming face. With the canonical
# coordinate identification below, internal and external dual edges have the
# same public two-tetrahedron 3-ball predicate.
_OUT_FACE = (0, 1, 4)
_IN_FACE = (0, 1, 3)


def _allowed_pair(public: GluingPublicInstance, group: TetrahedronGroup) -> bool:
    if len(group) != 2 or len(set(group)) != 2:
        return False
    if any(index < 0 or index >= len(public.tetrahedra) for index in group):
        return False
    left = set(public.tetrahedra[group[0]])
    right = set(public.tetrahedra[group[1]])
    return len(left & right) == 3 and len(left | right) == 5


def validate_matching_gluing_witness(
    public: GluingPublicInstance,
    groups: tuple[TetrahedronGroup, ...],
) -> MatchingGluingValidation:
    normalized = _normalize_groups(groups)
    if len(normalized) != public.piece_count:
        return MatchingGluingValidation(False, "wrong piece count", len(normalized), 0, ())

    flattened = [index for group in normalized for index in group]
    if sorted(flattened) != list(range(len(public.tetrahedra))):
        return MatchingGluingValidation(
            False,
            "groups do not partition public tetrahedra",
            len(normalized),
            0,
            (),
        )

    if not all(_allowed_pair(public, group) for group in normalized):
        return MatchingGluingValidation(
            False,
            "a recovered pair is not the allowed two-tetrahedron 3-ball",
            len(normalized),
            0,
            (),
        )

    faces, _ = _face_incidence(public.tetrahedra)
    if any(len(owners) > 2 for owners in faces.values()):
        return MatchingGluingValidation(
            False,
            "public face has incidence above two",
            len(normalized),
            0,
            (),
        )

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

    if len(cross_pairs) != public.piece_count:
        return MatchingGluingValidation(
            False,
            "cross-piece shared-face count is not n",
            len(normalized),
            len(cross_pairs),
            tuple(sorted(len(group) for group in normalized)),
        )

    unique_cross_pairs = set(cross_pairs)
    if len(unique_cross_pairs) != public.piece_count:
        return MatchingGluingValidation(
            False,
            "cross-piece shared faces do not form a simple graph",
            len(normalized),
            len(cross_pairs),
            tuple(sorted(len(group) for group in normalized)),
        )

    adjacency = [set() for _ in range(public.piece_count)]
    for left, right in unique_cross_pairs:
        adjacency[left].add(right)
        adjacency[right].add(left)

    if any(len(neighbors) != 2 for neighbors in adjacency):
        return MatchingGluingValidation(
            False,
            "cross-piece graph is not 2-regular",
            len(normalized),
            len(cross_pairs),
            tuple(sorted(len(group) for group in normalized)),
        )

    seen = {0}
    stack = [0]
    while stack:
        current = stack.pop()
        for neighbor in adjacency[current]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    if len(seen) != public.piece_count:
        return MatchingGluingValidation(
            False,
            "cross-piece cycle graph is disconnected",
            len(normalized),
            len(cross_pairs),
            tuple(sorted(len(group) for group in normalized)),
        )

    return MatchingGluingValidation(
        True,
        "accepted",
        len(normalized),
        len(cross_pairs),
        tuple(sorted(len(group) for group in normalized)),
    )


def _bridges_and_articulations(
    adjacency: list[list[int]],
) -> tuple[set[DualEdge], set[int]]:
    discovery = [-1] * len(adjacency)
    low = [-1] * len(adjacency)
    parent = [-1] * len(adjacency)
    bridges: set[DualEdge] = set()
    articulations: set[int] = set()
    timer = 0

    def visit(vertex: int) -> None:
        nonlocal timer
        discovery[vertex] = timer
        low[vertex] = timer
        timer += 1
        child_count = 0

        for neighbor in adjacency[vertex]:
            if discovery[neighbor] < 0:
                parent[neighbor] = vertex
                child_count += 1
                visit(neighbor)
                low[vertex] = min(low[vertex], low[neighbor])
                if low[neighbor] > discovery[vertex]:
                    bridges.add(tuple(sorted((vertex, neighbor))))
                if parent[vertex] < 0 and child_count > 1:
                    articulations.add(vertex)
                if parent[vertex] >= 0 and low[neighbor] >= discovery[vertex]:
                    articulations.add(vertex)
            elif neighbor != parent[vertex]:
                low[vertex] = min(low[vertex], discovery[neighbor])

    for vertex in range(len(adjacency)):
        if discovery[vertex] < 0:
            visit(vertex)
    return bridges, articulations


def _vertex_star_metrics(
    public: GluingPublicInstance,
) -> tuple[tuple[tuple[int, int], ...], int]:
    stars: dict[int, list[int]] = defaultdict(list)
    for tetrahedron_index, tetrahedron in enumerate(public.tetrahedra):
        for vertex in tetrahedron:
            stars[vertex].append(tetrahedron_index)
    histogram = tuple(sorted(Counter(len(star) for star in stars.values()).items()))
    candidate_pairs = {
        tuple(sorted(star))
        for star in stars.values()
        if len(star) == 2 and _allowed_pair(public, tuple(sorted(star)))
    }
    return histogram, len(candidate_pairs)


def _enumerate_matchings(
    vertex_count: int,
    candidate_edges: tuple[DualEdge, ...],
    solution_cap: int,
) -> tuple[tuple[tuple[DualEdge, ...], ...], int, int]:
    by_vertex: dict[int, list[int]] = defaultdict(list)
    edge_sets = [frozenset(edge) for edge in candidate_edges]
    for edge_index, edge in enumerate(candidate_edges):
        for vertex in edge:
            by_vertex[vertex].append(edge_index)

    solutions: list[tuple[DualEdge, ...]] = []
    nodes = 0
    backtracks = 0

    def search(unmatched: frozenset[int], chosen: tuple[int, ...]) -> None:
        nonlocal nodes, backtracks
        if len(solutions) >= solution_cap:
            return
        nodes += 1
        if not unmatched:
            solutions.append(tuple(candidate_edges[index] for index in chosen))
            return

        def remaining_options(vertex: int) -> int:
            return sum(
                1
                for edge_index in by_vertex[vertex]
                if edge_sets[edge_index] <= unmatched
            )

        pivot = min(unmatched, key=lambda vertex: (remaining_options(vertex), vertex))
        options = [
            edge_index
            for edge_index in by_vertex[pivot]
            if edge_sets[edge_index] <= unmatched
        ]
        if not options:
            backtracks += 1
            return

        before = len(solutions)
        for edge_index in options:
            search(unmatched - edge_sets[edge_index], chosen + (edge_index,))
            if len(solutions) >= solution_cap:
                return
        if len(solutions) == before:
            backtracks += 1

    search(frozenset(range(vertex_count)), ())
    return tuple(solutions), nodes, backtracks


def recover_matching_gluing(
    public: GluingPublicInstance,
    *,
    reference: MatchingGluingReference | None = None,
    solution_cap: int = 16,
) -> MatchingRecovery:
    if solution_cap < 1 or solution_cap > 1024:
        raise GluingExperimentError("G3 matching solution cap outside toy bounds")

    adjacency, edge_faces, face_occurrences = _dual_graph(public)
    bridges, articulations = _bridges_and_articulations(adjacency)
    degree_histogram = tuple(sorted(Counter(len(neighbors) for neighbors in adjacency).items()))

    candidate_edges = tuple(
        edge
        for edge in sorted(edge_faces)
        if _allowed_pair(public, edge)
    )
    matchings, nodes, backtracks = _enumerate_matchings(
        len(public.tetrahedra), candidate_edges, solution_cap
    )

    accepted: list[tuple[TetrahedronGroup, ...]] = []
    for matching in matchings:
        groups = _normalize_groups(tuple(tuple(edge) for edge in matching))
        if validate_matching_gluing_witness(public, groups).valid:
            accepted.append(groups)

    reference_groups = _normalize_groups(reference.groups) if reference is not None else None
    nonreference = sum(
        1 for groups in accepted if reference_groups is not None and groups != reference_groups
    )
    vertex_histogram, vertex_star_candidate_pairs = _vertex_star_metrics(public)

    return MatchingRecovery(
        accepted_groups=tuple(accepted),
        dual_edges=len(edge_faces),
        dual_degree_histogram=degree_histogram,
        bridge_count=len(bridges),
        articulation_points=tuple(sorted(articulations)),
        allowed_candidate_edges=len(candidate_edges),
        vertex_star_candidate_pairs=vertex_star_candidate_pairs,
        vertex_tetrahedron_degree_histogram=vertex_histogram,
        matching_solutions=len(matchings),
        matching_solution_cap=solution_cap,
        matching_cap_hit=len(matchings) >= solution_cap,
        matching_nodes=nodes,
        matching_backtracks=backtracks,
        accepted_solutions=len(accepted),
        nonreference_accepted_solutions=nonreference,
        face_occurrences=face_occurrences,
    )


def matching_reference_partition_matches(
    reference: MatchingGluingReference,
    groups: tuple[TetrahedronGroup, ...],
) -> bool:
    return _normalize_groups(reference.groups) == _normalize_groups(groups)


def generate_matching_gluing_instance(
    params: MatchingGluingParameters,
    master_seed: bytes,
) -> tuple[GluingPublicInstance, MatchingGluingReference]:
    params.validate()
    if len(master_seed) < 16:
        raise GluingExperimentError("G3 master seed must contain at least 128 bits")

    local_vertex_count = 5 * params.piece_count
    union_find = _UnionFind(local_vertex_count)
    local_tetrahedra: list[Tetrahedron] = []
    local_groups: list[TetrahedronGroup] = []

    for piece in range(params.piece_count):
        base = 5 * piece
        group = (len(local_tetrahedra), len(local_tetrahedra) + 1)
        local_tetrahedra.append(tuple(base + vertex for vertex in _LOCAL_A))
        local_tetrahedra.append(tuple(base + vertex for vertex in _LOCAL_B))
        local_groups.append(group)

    for piece in range(params.piece_count):
        next_piece = (piece + 1) % params.piece_count
        left_face = [5 * piece + vertex for vertex in _OUT_FACE]
        right_face = [5 * next_piece + vertex for vertex in _IN_FACE]
        for left_vertex, right_vertex in zip(left_face, right_face, strict=True):
            union_find.union(left_vertex, right_vertex)

    roots = sorted({union_find.find(vertex) for vertex in range(local_vertex_count)})
    root_index = {root: index for index, root in enumerate(roots)}
    quotient_tetrahedra = [
        tuple(sorted(root_index[union_find.find(vertex)] for vertex in tetrahedron))
        for tetrahedron in local_tetrahedra
    ]
    if any(len(set(tetrahedron)) != 4 for tetrahedron in quotient_tetrahedra):
        raise GluingExperimentError("G3 gluing produced a degenerate tetrahedron")
    if len(set(quotient_tetrahedra)) != len(quotient_tetrahedra):
        raise GluingExperimentError("G3 gluing produced duplicate tetrahedra")

    public_labels = list(range(len(roots)))
    label_rng = _DeterministicRng(
        b"MORPH-KEM G3 public-relabel v1/" + params.name.encode("ascii"),
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
    reference = MatchingGluingReference(groups=reference_groups)

    incidence = gluing_incidence(public)
    if incidence.max_face_incidence > 2:
        raise GluingExperimentError("G3 generated non-pseudomanifold face incidence")
    if not validate_matching_gluing_witness(public, reference.groups).valid:
        raise GluingExperimentError("G3 generated reference witness does not validate")

    adjacency, _, _ = _dual_graph(public)
    if len(adjacency) != 2 * params.piece_count or any(len(neighbors) != 2 for neighbors in adjacency):
        raise GluingExperimentError("G3 dual graph is not the intended even cycle")

    return public, reference
