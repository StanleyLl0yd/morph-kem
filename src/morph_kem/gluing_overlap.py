from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
from itertools import combinations
from functools import lru_cache

from .gluing import (
    GluingExperimentError,
    GluingPublicInstance,
    TetrahedronGroup,
    _DeterministicRng,
    _dual_graph,
    _face_incidence,
    _normalize_groups,
    gluing_incidence,
)
from .gluing_matching import (
    MatchingGluingParameters,
    _allowed_pair,
    _bridges_and_articulations,
    generate_matching_gluing_instance,
)


@dataclass(frozen=True, slots=True)
class OverlapGluingParameters:
    name: str
    tetrahedron_count: int
    piece_count: int

    def validate(self) -> None:
        if self.tetrahedron_count < 6 or self.tetrahedron_count > 64:
            raise GluingExperimentError("G9 tetrahedron count outside toy bounds")
        if self.tetrahedron_count % 2:
            raise GluingExperimentError("G9 base cycle requires an even tetrahedron count")
        d2_count = 3 * self.piece_count - self.tetrahedron_count
        d3_count = self.tetrahedron_count - 2 * self.piece_count
        if d2_count < 1 or d3_count < 1 or d2_count + d3_count != self.piece_count:
            raise GluingExperimentError("G9 parameters must require both D2 and D3 pieces")

    @property
    def d2_count(self) -> int:
        return 3 * self.piece_count - self.tetrahedron_count

    @property
    def d3_count(self) -> int:
        return self.tetrahedron_count - 2 * self.piece_count


G9_PARAMETER_SETS = {
    "g9-18": OverlapGluingParameters("g9-18", 18, 7),
    "g9-24": OverlapGluingParameters("g9-24", 24, 9),
    "g9-30": OverlapGluingParameters("g9-30", 30, 11),
}


@dataclass(frozen=True, slots=True)
class OverlapGluingReference:
    groups: tuple[TetrahedronGroup, ...]


@dataclass(frozen=True, slots=True)
class OverlapGluingValidation:
    valid: bool
    reason: str
    piece_count: int
    d2_pieces: int
    d3_pieces: int
    cross_faces: int


@dataclass(frozen=True, slots=True)
class OverlapRecovery:
    accepted_groups: tuple[tuple[TetrahedronGroup, ...], ...]
    dual_edges: int
    dual_degree_histogram: tuple[tuple[int, int], ...]
    bridge_count: int
    articulation_points: tuple[int, ...]
    d2_candidates: int
    d3_candidates: int
    membership_histogram: tuple[tuple[int, int], ...]
    overlap_degree_histogram: tuple[tuple[int, int], ...]
    candidate_incidence_size: int
    exact_cover_solutions: int
    exact_cover_solution_cap: int
    exact_cover_cap_hit: bool
    exact_cover_nodes: int
    exact_cover_backtracks: int
    cycle_dp_states: int
    cycle_dp_transition_checks: int
    cycle_dp_tilings: int
    accepted_solutions: int
    nonreference_accepted_solutions: int
    face_occurrences: int


def _piece_profile(public: GluingPublicInstance, group: TetrahedronGroup) -> tuple[int, int, int, int, int] | None:
    if len(set(group)) != len(group):
        return None
    if any(index < 0 or index >= len(public.tetrahedra) for index in group):
        return None
    tetrahedra = tuple(public.tetrahedra[index] for index in group)
    vertices = {vertex for tetrahedron in tetrahedra for vertex in tetrahedron}
    edges = {
        tuple(sorted(edge))
        for tetrahedron in tetrahedra
        for edge in combinations(tetrahedron, 2)
    }
    faces: dict[tuple[int, int, int], int] = defaultdict(int)
    for tetrahedron in tetrahedra:
        for face in combinations(tetrahedron, 3):
            faces[tuple(sorted(face))] += 1
    internal_faces = sum(count == 2 for count in faces.values())
    if any(count > 2 for count in faces.values()):
        return None
    return len(vertices), len(edges), len(faces), len(tetrahedra), internal_faces


def _allowed_piece(public: GluingPublicInstance, group: TetrahedronGroup) -> bool:
    normalized = tuple(sorted(group))
    if len(normalized) == 2:
        return _allowed_pair(public, normalized) and _piece_profile(public, normalized) == (5, 9, 7, 2, 1)
    if len(normalized) != 3:
        return False
    if _piece_profile(public, normalized) != (6, 12, 10, 3, 2):
        return False
    tetrahedra = [set(public.tetrahedra[index]) for index in normalized]
    intersections = sorted(
        len(tetrahedra[left] & tetrahedra[right])
        for left, right in combinations(range(3), 2)
    )
    return intersections == [2, 3, 3]


def _canonical_cycle_order(public: GluingPublicInstance) -> tuple[int, ...]:
    adjacency, _, _ = _dual_graph(public)
    if len(adjacency) != len(public.tetrahedra) or len(adjacency) < 3:
        raise GluingExperimentError("G9 public dual graph has invalid size")
    if any(len(neighbors) != 2 for neighbors in adjacency):
        raise GluingExperimentError("G9 public dual graph is not a cycle")

    start = 0
    previous = start
    current = min(adjacency[start])
    order = [start]
    while current != start:
        if current in order:
            raise GluingExperimentError("G9 public dual graph contains a short cycle")
        order.append(current)
        next_vertices = [neighbor for neighbor in adjacency[current] if neighbor != previous]
        if len(next_vertices) != 1:
            raise GluingExperimentError("G9 cycle traversal is ambiguous")
        previous, current = current, next_vertices[0]
    if len(order) != len(adjacency):
        raise GluingExperimentError("G9 public dual graph is disconnected")
    return tuple(order)


def _enumerate_candidates(
    public: GluingPublicInstance,
) -> tuple[tuple[TetrahedronGroup, ...], tuple[TetrahedronGroup, ...], int]:
    adjacency, edge_faces, face_occurrences = _dual_graph(public)
    d2 = tuple(
        tuple(edge)
        for edge in sorted(edge_faces)
        if _allowed_piece(public, tuple(edge))
    )
    d3_set: set[TetrahedronGroup] = set()
    for center, neighbors in enumerate(adjacency):
        if len(neighbors) != 2:
            continue
        candidate = tuple(sorted((neighbors[0], center, neighbors[1])))
        if _allowed_piece(public, candidate):
            d3_set.add(candidate)
    return tuple(sorted(d2)), tuple(sorted(d3_set)), face_occurrences


def validate_overlap_gluing_witness(
    public: GluingPublicInstance,
    groups: tuple[TetrahedronGroup, ...],
) -> OverlapGluingValidation:
    normalized = _normalize_groups(groups)
    if len(normalized) != public.piece_count:
        return OverlapGluingValidation(False, "wrong G9 piece count", len(normalized), 0, 0, 0)

    flattened = [index for group in normalized for index in group]
    if sorted(flattened) != list(range(len(public.tetrahedra))):
        return OverlapGluingValidation(
            False, "G9 groups do not partition public tetrahedra", len(normalized), 0, 0, 0
        )

    if not all(_allowed_piece(public, group) for group in normalized):
        return OverlapGluingValidation(False, "invalid G9 D2/D3 piece", len(normalized), 0, 0, 0)

    d2_count = sum(len(group) == 2 for group in normalized)
    d3_count = sum(len(group) == 3 for group in normalized)
    if d2_count + d3_count != len(normalized):
        return OverlapGluingValidation(False, "unsupported G9 piece size", len(normalized), d2_count, d3_count, 0)

    faces, _ = _face_incidence(public.tetrahedra)
    if any(len(owners) > 2 for owners in faces.values()):
        return OverlapGluingValidation(False, "public face incidence above two", len(normalized), d2_count, d3_count, 0)

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

    if len(cross_pairs) != public.piece_count or len(set(cross_pairs)) != public.piece_count:
        return OverlapGluingValidation(
            False, "G9 cross-piece faces do not form a simple cycle edge set",
            len(normalized), d2_count, d3_count, len(cross_pairs)
        )

    adjacency = [set() for _ in range(public.piece_count)]
    for left, right in set(cross_pairs):
        adjacency[left].add(right)
        adjacency[right].add(left)
    if any(len(neighbors) != 2 for neighbors in adjacency):
        return OverlapGluingValidation(
            False, "G9 cross-piece graph is not 2-regular",
            len(normalized), d2_count, d3_count, len(cross_pairs)
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
        return OverlapGluingValidation(
            False, "G9 cross-piece graph is disconnected",
            len(normalized), d2_count, d3_count, len(cross_pairs)
        )

    return OverlapGluingValidation(
        True, "accepted", len(normalized), d2_count, d3_count, len(cross_pairs)
    )


def _exact_cover_candidates(
    tetrahedron_count: int,
    piece_count: int,
    candidates: tuple[TetrahedronGroup, ...],
    solution_cap: int,
) -> tuple[tuple[tuple[TetrahedronGroup, ...], ...], int, int]:
    by_tetrahedron: dict[int, list[int]] = defaultdict(list)
    candidate_sets = [frozenset(candidate) for candidate in candidates]
    for candidate_index, candidate in enumerate(candidates):
        for tetrahedron in candidate:
            by_tetrahedron[tetrahedron].append(candidate_index)

    solutions: list[tuple[TetrahedronGroup, ...]] = []
    nodes = 0
    backtracks = 0

    def search(uncovered: frozenset[int], chosen: tuple[int, ...]) -> None:
        nonlocal nodes, backtracks
        if len(solutions) >= solution_cap:
            return
        nodes += 1
        remaining_pieces = piece_count - len(chosen)
        if remaining_pieces < 0 or 2 * remaining_pieces > len(uncovered) or 3 * remaining_pieces < len(uncovered):
            backtracks += 1
            return
        if not uncovered:
            if len(chosen) == piece_count:
                solutions.append(
                    _normalize_groups(tuple(candidates[index] for index in chosen))
                )
            else:
                backtracks += 1
            return

        def options_for(tetrahedron: int) -> tuple[int, ...]:
            return tuple(
                candidate_index
                for candidate_index in by_tetrahedron[tetrahedron]
                if candidate_sets[candidate_index] <= uncovered
            )

        pivot = min(uncovered, key=lambda tetrahedron: (len(options_for(tetrahedron)), tetrahedron))
        options = options_for(pivot)
        if not options:
            backtracks += 1
            return
        before = len(solutions)
        for candidate_index in options:
            search(uncovered - candidate_sets[candidate_index], chosen + (candidate_index,))
            if len(solutions) >= solution_cap:
                return
        if len(solutions) == before:
            backtracks += 1

    search(frozenset(range(tetrahedron_count)), ())
    return tuple(solutions), nodes, backtracks


def _cycle_dp_tilings(
    public: GluingPublicInstance,
    d2_count: int,
    d3_count: int,
) -> tuple[tuple[tuple[TetrahedronGroup, ...], ...], int, int]:
    order = _canonical_cycle_order(public)
    piece_count = d2_count + d3_count
    transitions = 0

    @lru_cache(maxsize=None)
    def sequences(remaining_pieces: int, remaining_length: int, remaining_d2: int) -> tuple[tuple[int, ...], ...]:
        nonlocal transitions
        if remaining_pieces == 0:
            return ((),) if remaining_length == 0 and remaining_d2 == 0 else ()
        result: list[tuple[int, ...]] = []
        for length in (2, 3):
            transitions += 1
            next_d2 = remaining_d2 - (length == 2)
            if next_d2 < 0 or next_d2 > remaining_pieces - 1:
                continue
            if remaining_length < length:
                continue
            for suffix in sequences(remaining_pieces - 1, remaining_length - length, next_d2):
                result.append((length,) + suffix)
        return tuple(result)

    length_sequences = sequences(piece_count, len(order), d2_count)
    covers: set[tuple[TetrahedronGroup, ...]] = set()
    for start in range(len(order)):
        rotated = order[start:] + order[:start]
        for lengths in length_sequences:
            cursor = 0
            groups: list[TetrahedronGroup] = []
            for length in lengths:
                groups.append(tuple(sorted(rotated[cursor : cursor + length])))
                cursor += length
            if cursor == len(order):
                covers.add(_normalize_groups(tuple(groups)))
    return tuple(sorted(covers)), sequences.cache_info().currsize, transitions


def recover_overlap_gluing(
    public: GluingPublicInstance,
    *,
    reference: OverlapGluingReference | None = None,
    solution_cap: int = 1024,
) -> OverlapRecovery:
    if solution_cap < 1 or solution_cap > 4096:
        raise GluingExperimentError("G9 solution cap outside toy bounds")

    adjacency, edge_faces, _ = _dual_graph(public)
    bridges, articulations = _bridges_and_articulations(adjacency)
    degree_histogram = tuple(sorted(Counter(len(neighbors) for neighbors in adjacency).items()))
    d2, d3, face_occurrences = _enumerate_candidates(public)
    candidates = tuple(sorted(d2 + d3, key=lambda group: (len(group), group)))

    memberships = [0] * len(public.tetrahedra)
    for candidate in candidates:
        for tetrahedron in candidate:
            memberships[tetrahedron] += 1
    membership_histogram = tuple(sorted(Counter(memberships).items()))
    incidence_size = sum(len(candidate) for candidate in candidates)

    overlap_degrees: list[int] = []
    candidate_sets = [set(candidate) for candidate in candidates]
    for index, candidate in enumerate(candidate_sets):
        overlap_degrees.append(
            sum(bool(candidate & other) for other_index, other in enumerate(candidate_sets) if other_index != index)
        )
    overlap_degree_histogram = tuple(sorted(Counter(overlap_degrees).items()))

    covers, nodes, backtracks = _exact_cover_candidates(
        len(public.tetrahedra), public.piece_count, candidates, solution_cap
    )
    accepted = tuple(
        groups for groups in covers if validate_overlap_gluing_witness(public, groups).valid
    )

    d2_needed = 3 * public.piece_count - len(public.tetrahedra)
    d3_needed = len(public.tetrahedra) - 2 * public.piece_count
    dp_covers, dp_states, dp_transitions = _cycle_dp_tilings(public, d2_needed, d3_needed)

    reference_groups = _normalize_groups(reference.groups) if reference is not None else None
    nonreference = sum(
        reference_groups is not None and groups != reference_groups
        for groups in accepted
    )

    return OverlapRecovery(
        accepted_groups=accepted,
        dual_edges=len(edge_faces),
        dual_degree_histogram=degree_histogram,
        bridge_count=len(bridges),
        articulation_points=tuple(sorted(articulations)),
        d2_candidates=len(d2),
        d3_candidates=len(d3),
        membership_histogram=membership_histogram,
        overlap_degree_histogram=overlap_degree_histogram,
        candidate_incidence_size=incidence_size,
        exact_cover_solutions=len(covers),
        exact_cover_solution_cap=solution_cap,
        exact_cover_cap_hit=len(covers) >= solution_cap,
        exact_cover_nodes=nodes,
        exact_cover_backtracks=backtracks,
        cycle_dp_states=dp_states,
        cycle_dp_transition_checks=dp_transitions,
        cycle_dp_tilings=len(dp_covers),
        accepted_solutions=len(accepted),
        nonreference_accepted_solutions=nonreference,
        face_occurrences=face_occurrences,
    )


def overlap_reference_partition_matches(
    reference: OverlapGluingReference,
    groups: tuple[TetrahedronGroup, ...],
) -> bool:
    return _normalize_groups(reference.groups) == _normalize_groups(groups)


def generate_overlap_gluing_instance(
    params: OverlapGluingParameters,
    master_seed: bytes,
) -> tuple[GluingPublicInstance, OverlapGluingReference]:
    params.validate()
    if len(master_seed) < 16:
        raise GluingExperimentError("G9 master seed must contain at least 128 bits")

    base_seed = hashlib.sha256(
        b"MORPH-KEM G9 base cycle v1\x00" + master_seed + params.name.encode("ascii")
    ).digest()
    base_public, _ = generate_matching_gluing_instance(
        MatchingGluingParameters(params.name + "-base", params.tetrahedron_count // 2),
        base_seed,
    )
    public = GluingPublicInstance(
        name=params.name,
        piece_count=params.piece_count,
        tetrahedra=base_public.tetrahedra,
    )

    order = _canonical_cycle_order(public)
    lengths = [2] * params.d2_count + [3] * params.d3_count
    tiling_rng = _DeterministicRng(
        b"MORPH-KEM G9 hidden tiling v1/" + params.name.encode("ascii"),
        master_seed,
    )
    tiling_rng.shuffle(lengths)
    offset = tiling_rng.randbelow(len(order))
    rotated = order[offset:] + order[:offset]
    groups: list[TetrahedronGroup] = []
    cursor = 0
    for length in lengths:
        groups.append(tuple(sorted(rotated[cursor : cursor + length])))
        cursor += length
    if cursor != len(rotated):
        raise GluingExperimentError("G9 hidden tiling does not cover the public cycle")
    reference = OverlapGluingReference(groups=_normalize_groups(tuple(groups)))

    incidence = gluing_incidence(public)
    if incidence.max_face_incidence > 2:
        raise GluingExperimentError("G9 generated non-pseudomanifold face incidence")
    validation = validate_overlap_gluing_witness(public, reference.groups)
    if not validation.valid:
        raise GluingExperimentError("G9 generated reference witness does not validate")

    adjacency, _, _ = _dual_graph(public)
    if len(adjacency) != params.tetrahedron_count or any(len(neighbors) != 2 for neighbors in adjacency):
        raise GluingExperimentError("G9 dual graph is not the intended cycle")

    d2, d3, _ = _enumerate_candidates(public)
    if len(d2) != params.tetrahedron_count or len(d3) != params.tetrahedron_count:
        raise GluingExperimentError("G9 public candidate family is not the intended overlap control")
    memberships = Counter(index for candidate in d2 + d3 for index in candidate)
    if any(memberships[index] <= 1 for index in range(params.tetrahedron_count)):
        raise GluingExperimentError("G9 candidate carriers do not overlap at every tetrahedron")

    return public, reference
