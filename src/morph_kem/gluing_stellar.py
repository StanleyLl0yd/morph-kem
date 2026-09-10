from __future__ import annotations

import hashlib
from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations

from .gluing import (
    GluingExperimentError,
    GluingPublicInstance,
    Tetrahedron,
    TetrahedronGroup,
    _DeterministicRng,
    _dual_graph,
    _face_incidence,
    _normalize_groups,
    _piece_is_valid,
    gluing_incidence,
)
from .gluing_cycle import (
    CycleGluingParameters,
    CycleGluingValidation,
    _bridges_and_articulations,
    _count_two_vertex_separator_pairs,
    generate_cycle_gluing_instance,
    recover_cycle_gluing_by_k4_exact_cover,
)


@dataclass(frozen=True, slots=True)
class StellarGluingParameters:
    name: str
    piece_count: int

    def validate(self) -> None:
        if self.piece_count < 4 or self.piece_count > 8:
            raise GluingExperimentError("G2 piece count outside stellar toy bounds")


G2_PARAMETER_SETS = {
    "g2-4": StellarGluingParameters("g2-4", 4),
    "g2-6": StellarGluingParameters("g2-6", 6),
    "g2-8": StellarGluingParameters("g2-8", 8),
}


@dataclass(frozen=True, slots=True)
class StellarGluingReference:
    groups: tuple[TetrahedronGroup, ...]
    center_vertices: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class StellarGluingValidation:
    valid: bool
    reason: str
    piece_count: int
    cross_faces: int
    component_sizes: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class _CenterStarCandidate:
    center: int
    macro_tetrahedron: Tetrahedron
    micro_group: TetrahedronGroup


@dataclass(frozen=True, slots=True)
class StellarContractionRecovery:
    groups: tuple[TetrahedronGroup, ...]
    candidate_centers: tuple[int, ...]
    public_vertices: int
    micro_dual_edges: int
    micro_face_occurrences: int
    micro_bridge_count: int
    micro_articulation_points: tuple[int, ...]
    micro_two_vertex_separator_pairs: int
    center_star_candidates: int
    center_cover_solutions: int
    center_cover_solution_cap: int
    center_cover_cap_hit: bool
    center_cover_nodes: int
    center_cover_backtracks: int
    reconstructed_macro_tetrahedra: int
    macro_dual_edges: int
    macro_k4_candidates: int
    macro_allowed_piece_candidates: int
    macro_cover_solutions: int
    macro_cover_nodes: int
    macro_cover_backtracks: int
    validation: StellarGluingValidation


def _center_star_macro(
    tetrahedra: tuple[Tetrahedron, ...],
    center: int,
    owners: TetrahedronGroup,
) -> Tetrahedron | None:
    if len(owners) != 4:
        return None

    base_vertices: set[int] = set()
    observed_faces: set[tuple[int, int, int]] = set()
    for tetrahedron_index in owners:
        tetrahedron = tetrahedra[tetrahedron_index]
        if center not in tetrahedron:
            return None
        other = tuple(vertex for vertex in tetrahedron if vertex != center)
        if len(other) != 3:
            return None
        observed_faces.add(tuple(sorted(other)))
        base_vertices.update(other)

    if len(base_vertices) != 4 or len(observed_faces) != 4:
        return None

    macro = tuple(sorted(base_vertices))
    expected_faces = {tuple(face) for face in combinations(macro, 3)}
    if observed_faces != expected_faces:
        return None
    return macro


def _center_candidates_in_group(
    public: GluingPublicInstance,
    group: TetrahedronGroup,
) -> tuple[_CenterStarCandidate, ...]:
    group_set = set(group)
    by_vertex: dict[int, list[int]] = defaultdict(list)
    for tetrahedron_index in group:
        for vertex in public.tetrahedra[tetrahedron_index]:
            by_vertex[vertex].append(tetrahedron_index)

    candidates: list[_CenterStarCandidate] = []
    for vertex, owners_list in by_vertex.items():
        owners = tuple(sorted(owners_list))
        if len(owners) != 4 or not set(owners) <= group_set:
            continue
        macro = _center_star_macro(public.tetrahedra, vertex, owners)
        if macro is not None:
            candidates.append(_CenterStarCandidate(vertex, macro, owners))

    return tuple(sorted(candidates, key=lambda candidate: (candidate.macro_tetrahedron, candidate.center)))


def _stellar_piece_is_valid(
    public: GluingPublicInstance,
    group: TetrahedronGroup,
) -> bool:
    if len(group) != 16 or len(set(group)) != 16:
        return False

    candidates = _center_candidates_in_group(public, group)
    if len(candidates) != 4:
        return False

    owner_counts: dict[int, int] = defaultdict(int)
    for candidate in candidates:
        for tetrahedron_index in candidate.micro_group:
            owner_counts[tetrahedron_index] += 1
    if set(owner_counts) != set(group) or any(count != 1 for count in owner_counts.values()):
        return False

    macros = tuple(candidate.macro_tetrahedron for candidate in candidates)
    if len(set(macros)) != 4:
        return False

    macro_public = GluingPublicInstance(
        name="g2-local-contracted-piece",
        piece_count=1,
        tetrahedra=macros,
    )
    return _piece_is_valid(macro_public, (0, 1, 2, 3))


def validate_stellar_gluing_witness(
    public: GluingPublicInstance,
    groups: tuple[TetrahedronGroup, ...],
) -> StellarGluingValidation:
    normalized = _normalize_groups(groups)
    if len(normalized) != public.piece_count:
        return StellarGluingValidation(False, "wrong piece count", len(normalized), 0, ())

    flattened = [index for group in normalized for index in group]
    if sorted(flattened) != list(range(len(public.tetrahedra))):
        return StellarGluingValidation(
            False,
            "groups do not partition public micro tetrahedra",
            len(normalized),
            0,
            (),
        )

    if not all(_stellar_piece_is_valid(public, group) for group in normalized):
        return StellarGluingValidation(
            False,
            "a recovered block is not the allowed stellar-subdivided piece",
            len(normalized),
            0,
            (),
        )

    faces, _ = _face_incidence(public.tetrahedra)
    if any(len(owners) > 2 for owners in faces.values()):
        return StellarGluingValidation(
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

    cross_pairs: list[tuple[int, int]] = []
    for owners in faces.values():
        if len(owners) != 2:
            continue
        left_group = owner_group[owners[0]]
        right_group = owner_group[owners[1]]
        if left_group != right_group:
            cross_pairs.append(tuple(sorted((left_group, right_group))))

    if len(cross_pairs) != public.piece_count:
        return StellarGluingValidation(
            False,
            "cross-piece shared-face count is not n",
            len(normalized),
            len(cross_pairs),
            tuple(sorted(len(group) for group in normalized)),
        )

    unique_cross_pairs = set(cross_pairs)
    if len(unique_cross_pairs) != public.piece_count:
        return StellarGluingValidation(
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
        return StellarGluingValidation(
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
        return StellarGluingValidation(
            False,
            "cross-piece cycle graph is disconnected",
            len(normalized),
            len(cross_pairs),
            tuple(sorted(len(group) for group in normalized)),
        )

    return StellarGluingValidation(
        True,
        "accepted",
        len(normalized),
        len(cross_pairs),
        tuple(sorted(len(group) for group in normalized)),
    )


def _enumerate_global_center_stars(
    public: GluingPublicInstance,
) -> tuple[_CenterStarCandidate, ...]:
    by_vertex: dict[int, list[int]] = defaultdict(list)
    for tetrahedron_index, tetrahedron in enumerate(public.tetrahedra):
        for vertex in tetrahedron:
            by_vertex[vertex].append(tetrahedron_index)

    candidates: list[_CenterStarCandidate] = []
    for vertex, owners_list in by_vertex.items():
        owners = tuple(sorted(owners_list))
        if len(owners) != 4:
            continue
        macro = _center_star_macro(public.tetrahedra, vertex, owners)
        if macro is not None:
            candidates.append(_CenterStarCandidate(vertex, macro, owners))

    return tuple(sorted(candidates, key=lambda candidate: (candidate.macro_tetrahedron, candidate.center)))


def _center_star_exact_covers(
    tetrahedron_count: int,
    candidates: tuple[_CenterStarCandidate, ...],
    solution_cap: int,
) -> tuple[tuple[tuple[int, ...], ...], int, int]:
    by_tetrahedron: dict[int, list[int]] = defaultdict(list)
    candidate_sets = [frozenset(candidate.micro_group) for candidate in candidates]
    for candidate_index, candidate in enumerate(candidates):
        for tetrahedron_index in candidate.micro_group:
            by_tetrahedron[tetrahedron_index].append(candidate_index)

    solutions: list[tuple[int, ...]] = []
    nodes = 0
    backtracks = 0

    def search(uncovered: frozenset[int], chosen: tuple[int, ...]) -> None:
        nonlocal nodes, backtracks
        if len(solutions) >= solution_cap:
            return
        nodes += 1
        if not uncovered:
            solutions.append(chosen)
            return

        def option_count(tetrahedron_index: int) -> int:
            return sum(
                1
                for candidate_index in by_tetrahedron[tetrahedron_index]
                if candidate_sets[candidate_index] <= uncovered
            )

        pivot = min(uncovered, key=lambda index: (option_count(index), index))
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
            search(uncovered - candidate_sets[candidate_index], chosen + (candidate_index,))
            if len(solutions) >= solution_cap:
                return
        if len(solutions) == solutions_before:
            backtracks += 1

    search(frozenset(range(tetrahedron_count)), ())
    return tuple(solutions), nodes, backtracks


def recover_stellar_gluing_by_center_contraction(
    public: GluingPublicInstance,
    *,
    center_solution_cap: int = 64,
    macro_solution_cap: int = 64,
) -> StellarContractionRecovery:
    if center_solution_cap < 1 or center_solution_cap > 1024:
        raise GluingExperimentError("G2 center-cover solution cap outside toy bounds")

    adjacency, edge_faces, face_occurrences = _dual_graph(public)
    bridges, articulations = _bridges_and_articulations(adjacency)
    two_vertex_separators = _count_two_vertex_separator_pairs(adjacency)

    public_vertices = len({vertex for tetrahedron in public.tetrahedra for vertex in tetrahedron})
    candidates = _enumerate_global_center_stars(public)
    center_solutions, center_nodes, center_backtracks = _center_star_exact_covers(
        len(public.tetrahedra),
        candidates,
        center_solution_cap,
    )

    if not center_solutions:
        validation = validate_stellar_gluing_witness(public, ())
        return StellarContractionRecovery(
            groups=(),
            candidate_centers=tuple(candidate.center for candidate in candidates),
            public_vertices=public_vertices,
            micro_dual_edges=len(edge_faces),
            micro_face_occurrences=face_occurrences,
            micro_bridge_count=len(bridges),
            micro_articulation_points=tuple(sorted(articulations)),
            micro_two_vertex_separator_pairs=two_vertex_separators,
            center_star_candidates=len(candidates),
            center_cover_solutions=0,
            center_cover_solution_cap=center_solution_cap,
            center_cover_cap_hit=False,
            center_cover_nodes=center_nodes,
            center_cover_backtracks=center_backtracks,
            reconstructed_macro_tetrahedra=0,
            macro_dual_edges=0,
            macro_k4_candidates=0,
            macro_allowed_piece_candidates=0,
            macro_cover_solutions=0,
            macro_cover_nodes=0,
            macro_cover_backtracks=0,
            validation=validation,
        )

    chosen_candidates = [candidates[index] for index in center_solutions[0]]
    chosen_candidates.sort(key=lambda candidate: candidate.macro_tetrahedron)
    macro_tetrahedra = tuple(candidate.macro_tetrahedron for candidate in chosen_candidates)
    if len(set(macro_tetrahedra)) != len(macro_tetrahedra):
        validation = StellarGluingValidation(False, "contracted macro tetrahedra are not unique", 0, 0, ())
        return StellarContractionRecovery(
            groups=(),
            candidate_centers=tuple(candidate.center for candidate in candidates),
            public_vertices=public_vertices,
            micro_dual_edges=len(edge_faces),
            micro_face_occurrences=face_occurrences,
            micro_bridge_count=len(bridges),
            micro_articulation_points=tuple(sorted(articulations)),
            micro_two_vertex_separator_pairs=two_vertex_separators,
            center_star_candidates=len(candidates),
            center_cover_solutions=len(center_solutions),
            center_cover_solution_cap=center_solution_cap,
            center_cover_cap_hit=len(center_solutions) >= center_solution_cap,
            center_cover_nodes=center_nodes,
            center_cover_backtracks=center_backtracks,
            reconstructed_macro_tetrahedra=len(macro_tetrahedra),
            macro_dual_edges=0,
            macro_k4_candidates=0,
            macro_allowed_piece_candidates=0,
            macro_cover_solutions=0,
            macro_cover_nodes=0,
            macro_cover_backtracks=0,
            validation=validation,
        )

    macro_public = GluingPublicInstance(
        name=f"{public.name}-contracted",
        piece_count=public.piece_count,
        tetrahedra=macro_tetrahedra,
    )
    macro_recovery = recover_cycle_gluing_by_k4_exact_cover(
        macro_public,
        solution_cap=macro_solution_cap,
    )

    lifted_groups: list[TetrahedronGroup] = []
    for macro_group in macro_recovery.groups:
        micro_indices: list[int] = []
        for macro_index in macro_group:
            micro_indices.extend(chosen_candidates[macro_index].micro_group)
        lifted_groups.append(tuple(sorted(micro_indices)))

    groups = _normalize_groups(tuple(lifted_groups))
    validation = validate_stellar_gluing_witness(public, groups)

    return StellarContractionRecovery(
        groups=groups,
        candidate_centers=tuple(candidate.center for candidate in candidates),
        public_vertices=public_vertices,
        micro_dual_edges=len(edge_faces),
        micro_face_occurrences=face_occurrences,
        micro_bridge_count=len(bridges),
        micro_articulation_points=tuple(sorted(articulations)),
        micro_two_vertex_separator_pairs=two_vertex_separators,
        center_star_candidates=len(candidates),
        center_cover_solutions=len(center_solutions),
        center_cover_solution_cap=center_solution_cap,
        center_cover_cap_hit=len(center_solutions) >= center_solution_cap,
        center_cover_nodes=center_nodes,
        center_cover_backtracks=center_backtracks,
        reconstructed_macro_tetrahedra=len(macro_tetrahedra),
        macro_dual_edges=macro_recovery.dual_edges,
        macro_k4_candidates=macro_recovery.dual_k4_candidates,
        macro_allowed_piece_candidates=macro_recovery.allowed_piece_candidates,
        macro_cover_solutions=macro_recovery.exact_cover_solutions,
        macro_cover_nodes=macro_recovery.exact_cover_nodes,
        macro_cover_backtracks=macro_recovery.exact_cover_backtracks,
        validation=validation,
    )


def stellar_reference_partition_matches(
    reference: StellarGluingReference,
    groups: tuple[TetrahedronGroup, ...],
) -> bool:
    return _normalize_groups(reference.groups) == _normalize_groups(groups)


def generate_stellar_gluing_instance(
    params: StellarGluingParameters,
    master_seed: bytes,
) -> tuple[GluingPublicInstance, StellarGluingReference]:
    params.validate()
    if len(master_seed) < 16:
        raise GluingExperimentError("G2 master seed must contain at least 128 bits")

    macro_seed = hashlib.sha256(
        b"MORPH-KEM G2 macro-cycle v1\x00" + master_seed + params.name.encode("ascii")
    ).digest()
    macro_params = CycleGluingParameters(f"{params.name}-macro", params.piece_count)
    macro_public, macro_reference = generate_cycle_gluing_instance(macro_params, macro_seed)

    macro_vertex_count = len({
        vertex
        for tetrahedron in macro_public.tetrahedra
        for vertex in tetrahedron
    })
    micro_tetrahedra: list[Tetrahedron] = []
    macro_to_micro: list[TetrahedronGroup] = []
    center_vertices: list[int] = []

    for macro_index, macro_tetrahedron in enumerate(macro_public.tetrahedra):
        center = macro_vertex_count + macro_index
        center_vertices.append(center)
        micro_group: list[int] = []
        for face in combinations(macro_tetrahedron, 3):
            micro_group.append(len(micro_tetrahedra))
            micro_tetrahedra.append(tuple(sorted((center, *face))))
        macro_to_micro.append(tuple(micro_group))

    total_vertex_count = macro_vertex_count + len(macro_public.tetrahedra)
    labels = list(range(total_vertex_count))
    label_rng = _DeterministicRng(
        b"MORPH-KEM G2 public-relabel v1/" + params.name.encode("ascii"),
        master_seed,
    )
    label_rng.shuffle(labels)

    relabeled = [
        tuple(sorted(labels[vertex] for vertex in tetrahedron))
        for tetrahedron in micro_tetrahedra
    ]
    order = sorted(range(len(relabeled)), key=relabeled.__getitem__)
    public_tetrahedra = tuple(relabeled[index] for index in order)
    old_to_public = {old: new for new, old in enumerate(order)}

    reference_groups = _normalize_groups(
        tuple(
            tuple(
                old_to_public[micro_index]
                for macro_index in macro_group
                for micro_index in macro_to_micro[macro_index]
            )
            for macro_group in macro_reference.groups
        )
    )
    reference_centers = tuple(sorted(labels[center] for center in center_vertices))

    public = GluingPublicInstance(
        name=params.name,
        piece_count=params.piece_count,
        tetrahedra=public_tetrahedra,
    )
    reference = StellarGluingReference(
        groups=reference_groups,
        center_vertices=reference_centers,
    )

    incidence = gluing_incidence(public)
    if incidence.max_face_incidence > 2:
        raise GluingExperimentError("G2 generated non-pseudomanifold face incidence")
    if not validate_stellar_gluing_witness(public, reference.groups).valid:
        raise GluingExperimentError("G2 generated reference witness does not validate")

    return public, reference
