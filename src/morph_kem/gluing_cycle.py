from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations

from .gluing import (
    DualEdge,
    GluingExperimentError,
    GluingPublicInstance,
    TetrahedronGroup,
    _BASE_PORTS,
    _BASE_TETRAHEDRA,
    _DeterministicRng,
    _UnionFind,
    _dual_graph,
    _face_incidence,
    _normalize_groups,
    _piece_is_valid,
    gluing_incidence,
)


@dataclass(frozen=True, slots=True)
class CycleGluingParameters:
    name: str
    piece_count: int

    def validate(self) -> None:
        if self.piece_count < 4 or self.piece_count > 16:
            raise GluingExperimentError("G1 piece count outside exhaustive toy bounds")


G1_PARAMETER_SETS = {
    "g1-4": CycleGluingParameters("g1-4", 4),
    "g1-8": CycleGluingParameters("g1-8", 8),
    "g1-12": CycleGluingParameters("g1-12", 12),
}


@dataclass(frozen=True, slots=True)
class CycleGluingReference:
    groups: tuple[TetrahedronGroup, ...]
    cycle_edges: tuple[DualEdge, ...]
    port_pairs: tuple[tuple[int, int, int, int], ...]


@dataclass(frozen=True, slots=True)
class CycleGluingValidation:
    valid: bool
    reason: str
    piece_count: int
    cross_faces: int
    component_sizes: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class CliqueRecovery:
    groups: tuple[TetrahedronGroup, ...]
    dual_edges: int
    face_occurrences: int
    bridge_count: int
    articulation_points: tuple[int, ...]
    two_vertex_separator_pairs: int
    four_subsets_tested: int
    dual_k4_candidates: int
    allowed_piece_candidates: int
    exact_cover_solutions: int
    exact_cover_solution_cap: int
    exact_cover_cap_hit: bool
    exact_cover_nodes: int
    exact_cover_backtracks: int
    validation: CycleGluingValidation


def _cycle_edges(piece_count: int) -> tuple[DualEdge, ...]:
    return tuple((piece, (piece + 1) % piece_count) for piece in range(piece_count))


def validate_cycle_gluing_witness(
    public: GluingPublicInstance,
    groups: tuple[TetrahedronGroup, ...],
) -> CycleGluingValidation:
    normalized = _normalize_groups(groups)
    if len(normalized) != public.piece_count:
        return CycleGluingValidation(False, "wrong piece count", len(normalized), 0, ())

    flattened = [index for group in normalized for index in group]
    if sorted(flattened) != list(range(len(public.tetrahedra))):
        return CycleGluingValidation(
            False,
            "groups do not partition public tetrahedra",
            len(normalized),
            0,
            (),
        )

    if not all(_piece_is_valid(public, group) for group in normalized):
        return CycleGluingValidation(
            False,
            "a recovered block is not the allowed 3-ball piece",
            len(normalized),
            0,
            (),
        )

    faces, _ = _face_incidence(public.tetrahedra)
    if any(len(owners) > 2 for owners in faces.values()):
        return CycleGluingValidation(
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
        return CycleGluingValidation(
            False,
            "cross-piece shared-face count is not n",
            len(normalized),
            len(cross_pairs),
            tuple(sorted(len(group) for group in normalized)),
        )

    unique_cross_pairs = set(cross_pairs)
    if len(unique_cross_pairs) != public.piece_count:
        return CycleGluingValidation(
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
        return CycleGluingValidation(
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
        return CycleGluingValidation(
            False,
            "cross-piece cycle graph is disconnected",
            len(normalized),
            len(cross_pairs),
            tuple(sorted(len(group) for group in normalized)),
        )

    return CycleGluingValidation(
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


def _count_two_vertex_separator_pairs(adjacency: list[list[int]]) -> int:
    vertex_count = len(adjacency)
    separator_pairs = 0

    for removed_left, removed_right in combinations(range(vertex_count), 2):
        start = next(
            vertex
            for vertex in range(vertex_count)
            if vertex != removed_left and vertex != removed_right
        )
        seen = {start}
        stack = [start]
        while stack:
            current = stack.pop()
            for neighbor in adjacency[current]:
                if neighbor in (removed_left, removed_right) or neighbor in seen:
                    continue
                seen.add(neighbor)
                stack.append(neighbor)

        if len(seen) != vertex_count - 2:
            separator_pairs += 1

    return separator_pairs


def _solve_exact_piece_cover(
    public: GluingPublicInstance,
    candidates: tuple[TetrahedronGroup, ...],
    solution_cap: int,
) -> tuple[tuple[tuple[TetrahedronGroup, ...], ...], int, int]:
    by_tetrahedron: dict[int, list[int]] = defaultdict(list)
    candidate_sets = [frozenset(candidate) for candidate in candidates]
    for candidate_index, candidate in enumerate(candidates):
        for tetrahedron_index in candidate:
            by_tetrahedron[tetrahedron_index].append(candidate_index)

    solutions: list[tuple[TetrahedronGroup, ...]] = []
    nodes = 0
    backtracks = 0

    def search(uncovered: frozenset[int], chosen: tuple[int, ...]) -> None:
        nonlocal nodes, backtracks
        if len(solutions) >= solution_cap:
            return
        nodes += 1

        if not uncovered:
            groups = _normalize_groups(tuple(candidates[index] for index in chosen))
            if validate_cycle_gluing_witness(public, groups).valid:
                solutions.append(groups)
            else:
                backtracks += 1
            return

        def remaining_options(tetrahedron_index: int) -> int:
            return sum(
                1
                for candidate_index in by_tetrahedron[tetrahedron_index]
                if candidate_sets[candidate_index] <= uncovered
            )

        pivot = min(uncovered, key=lambda index: (remaining_options(index), index))
        options = [
            candidate_index
            for candidate_index in by_tetrahedron[pivot]
            if candidate_sets[candidate_index] <= uncovered
        ]
        if not options:
            backtracks += 1
            return

        solutions_before = len(solutions)
        for candidate_index in options:
            search(
                uncovered - candidate_sets[candidate_index],
                chosen + (candidate_index,),
            )
            if len(solutions) >= solution_cap:
                return

        if len(solutions) == solutions_before:
            backtracks += 1

    search(frozenset(range(len(public.tetrahedra))), ())
    return tuple(solutions), nodes, backtracks


def recover_cycle_gluing_by_k4_exact_cover(
    public: GluingPublicInstance,
    *,
    solution_cap: int = 64,
) -> CliqueRecovery:
    if solution_cap < 1 or solution_cap > 1024:
        raise GluingExperimentError("G1 exact-cover solution cap outside toy bounds")

    adjacency, edge_faces, face_occurrences = _dual_graph(public)
    neighbor_sets = [set(neighbors) for neighbors in adjacency]
    bridges, articulations = _bridges_and_articulations(adjacency)
    two_vertex_separator_pairs = _count_two_vertex_separator_pairs(adjacency)

    four_subsets_tested = 0
    dual_k4_candidates = 0
    allowed_piece_candidates: list[TetrahedronGroup] = []

    for candidate in combinations(range(len(public.tetrahedra)), 4):
        four_subsets_tested += 1
        if not all(
            right in neighbor_sets[left]
            for left, right in combinations(candidate, 2)
        ):
            continue
        dual_k4_candidates += 1
        if _piece_is_valid(public, candidate):
            allowed_piece_candidates.append(tuple(candidate))

    candidate_tuple = tuple(allowed_piece_candidates)
    solutions, exact_cover_nodes, exact_cover_backtracks = _solve_exact_piece_cover(
        public,
        candidate_tuple,
        solution_cap,
    )
    groups = solutions[0] if solutions else ()
    validation = validate_cycle_gluing_witness(public, groups)

    return CliqueRecovery(
        groups=groups,
        dual_edges=len(edge_faces),
        face_occurrences=face_occurrences,
        bridge_count=len(bridges),
        articulation_points=tuple(sorted(articulations)),
        two_vertex_separator_pairs=two_vertex_separator_pairs,
        four_subsets_tested=four_subsets_tested,
        dual_k4_candidates=dual_k4_candidates,
        allowed_piece_candidates=len(candidate_tuple),
        exact_cover_solutions=len(solutions),
        exact_cover_solution_cap=solution_cap,
        exact_cover_cap_hit=len(solutions) >= solution_cap,
        exact_cover_nodes=exact_cover_nodes,
        exact_cover_backtracks=exact_cover_backtracks,
        validation=validation,
    )


def cycle_reference_partition_matches(
    reference: CycleGluingReference,
    groups: tuple[TetrahedronGroup, ...],
) -> bool:
    return _normalize_groups(reference.groups) == _normalize_groups(groups)


def generate_cycle_gluing_instance(
    params: CycleGluingParameters,
    master_seed: bytes,
) -> tuple[GluingPublicInstance, CycleGluingReference]:
    params.validate()
    if len(master_seed) < 16:
        raise GluingExperimentError("G1 master seed must contain at least 128 bits")

    local_vertex_count = 5 * params.piece_count
    union_find = _UnionFind(local_vertex_count)

    local_tetrahedra = []
    local_groups: list[TetrahedronGroup] = []
    for piece in range(params.piece_count):
        base = 5 * piece
        group: list[int] = []
        for tetrahedron in _BASE_TETRAHEDRA:
            group.append(len(local_tetrahedra))
            local_tetrahedra.append(tuple(base + vertex for vertex in tetrahedron))
        local_groups.append(tuple(group))

    cycle_edges = _cycle_edges(params.piece_count)
    next_port = [0] * params.piece_count
    port_pairs: list[tuple[int, int, int, int]] = []

    for left_piece, right_piece in cycle_edges:
        left_port = next_port[left_piece]
        right_port = next_port[right_piece]
        next_port[left_piece] += 1
        next_port[right_piece] += 1

        left_face = [5 * left_piece + vertex for vertex in _BASE_PORTS[left_port]]
        right_face = [5 * right_piece + vertex for vertex in _BASE_PORTS[right_port]]
        for left_vertex, right_vertex in zip(left_face, right_face, strict=True):
            union_find.union(left_vertex, right_vertex)

        port_pairs.append((left_piece, left_port, right_piece, right_port))

    if any(port_count != 2 for port_count in next_port):
        raise GluingExperimentError("G1 cycle did not consume exactly two ports per piece")

    roots = sorted({union_find.find(vertex) for vertex in range(local_vertex_count)})
    root_index = {root: index for index, root in enumerate(roots)}

    quotient_tetrahedra = []
    for tetrahedron in local_tetrahedra:
        quotient = tuple(
            sorted(root_index[union_find.find(vertex)] for vertex in tetrahedron)
        )
        if len(set(quotient)) != 4:
            raise GluingExperimentError("G1 gluing produced a degenerate tetrahedron")
        quotient_tetrahedra.append(quotient)

    if len(set(quotient_tetrahedra)) != len(quotient_tetrahedra):
        raise GluingExperimentError("G1 gluing produced duplicate tetrahedra")

    public_labels = list(range(len(roots)))
    label_rng = _DeterministicRng(
        b"MORPH-KEM G1 public-relabel v1/" + params.name.encode("ascii"),
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
    reference = CycleGluingReference(
        groups=reference_groups,
        cycle_edges=cycle_edges,
        port_pairs=tuple(port_pairs),
    )

    incidence = gluing_incidence(public)
    if incidence.max_face_incidence > 2:
        raise GluingExperimentError("G1 generated non-pseudomanifold face incidence")
    if not validate_cycle_gluing_witness(public, reference.groups).valid:
        raise GluingExperimentError("G1 generated reference witness does not validate")

    return public, reference
