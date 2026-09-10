from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import combinations

from .gluing import (
    DualEdge,
    GluingExperimentError,
    GluingPublicInstance,
    Tetrahedron,
    TetrahedronGroup,
    Triangle,
    _BASE_PORTS,
    _BASE_TETRAHEDRA,
    _DeterministicRng,
    _UnionFind,
    _face_incidence,
    _normalize_groups,
    _piece_is_valid,
)


@dataclass(frozen=True, slots=True)
class CycleGluingParameters:
    name: str
    piece_count: int

    def validate(self) -> None:
        if self.piece_count < 3 or self.piece_count > 64:
            raise GluingExperimentError("G1 cycle piece count outside toy bounds")


G1_PARAMETER_SETS = {
    "g1-3": CycleGluingParameters("g1-3", 3),
    "g1-5": CycleGluingParameters("g1-5", 5),
    "g1-8": CycleGluingParameters("g1-8", 8),
}


@dataclass(frozen=True, slots=True)
class CycleGluingReference:
    groups: tuple[TetrahedronGroup, ...]
    cycle_edges: tuple[DualEdge, ...]
    swap_bits: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class CycleGluingValidation:
    valid: bool
    reason: str
    piece_count: int
    cross_faces: int
    component_sizes: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class CycleStructure:
    vertices: int
    edges: int
    faces: int
    tetrahedra: int
    boundary_faces: int
    max_face_incidence: int
    euler_characteristic: int
    dual_edges: int
    bridges: tuple[DualEdge, ...]
    articulation_vertices: tuple[int, ...]
    dual_degree_histogram: tuple[tuple[int, int], ...]
    vertex_tetrahedron_degree_histogram: tuple[tuple[int, int], ...]
    face_occurrences: int
    dfs_edge_scans: int


@dataclass(frozen=True, slots=True)
class ExactCoverResult:
    groups: tuple[TetrahedronGroup, ...] | None
    nodes: int
    backtracks: int
    solutions: int
    exhausted: bool
    validation: CycleGluingValidation


@dataclass(frozen=True, slots=True)
class StarRecovery:
    candidate_vertices: int
    valid_candidates: tuple[TetrahedronGroup, ...]
    exact_cover: ExactCoverResult
    matches_reference: bool


@dataclass(frozen=True, slots=True)
class K4Recovery:
    subset_checks: int
    clique_candidates: int
    valid_candidates: tuple[TetrahedronGroup, ...]
    exact_cover: ExactCoverResult
    matches_reference: bool


def _dual_graph(
    public: GluingPublicInstance,
) -> tuple[list[set[int]], dict[DualEdge, Triangle], int]:
    faces, occurrences = _face_incidence(public.tetrahedra)
    adjacency = [set() for _ in public.tetrahedra]
    edge_faces: dict[DualEdge, Triangle] = {}

    for face, owners in faces.items():
        if len(owners) > 2:
            raise GluingExperimentError("G1 public face incidence exceeds two")
        if len(owners) != 2:
            continue
        left, right = sorted(owners)
        edge = (left, right)
        if edge in edge_faces:
            raise GluingExperimentError("G1 tetrahedra share multiple triangular faces")
        edge_faces[edge] = face
        adjacency[left].add(right)
        adjacency[right].add(left)

    return adjacency, edge_faces, occurrences


def _bridges_and_articulations(
    adjacency: list[set[int]],
) -> tuple[tuple[DualEdge, ...], tuple[int, ...], int]:
    discovery = [-1] * len(adjacency)
    low = [-1] * len(adjacency)
    parent = [-1] * len(adjacency)
    bridges: set[DualEdge] = set()
    articulations: set[int] = set()
    timer = 0
    edge_scans = 0

    def visit(vertex: int) -> None:
        nonlocal timer, edge_scans
        discovery[vertex] = low[vertex] = timer
        timer += 1
        children = 0

        for neighbor in sorted(adjacency[vertex]):
            edge_scans += 1
            if discovery[neighbor] < 0:
                parent[neighbor] = vertex
                children += 1
                visit(neighbor)
                low[vertex] = min(low[vertex], low[neighbor])
                if low[neighbor] > discovery[vertex]:
                    bridges.add(tuple(sorted((vertex, neighbor))))
                if parent[vertex] < 0 and children > 1:
                    articulations.add(vertex)
                if parent[vertex] >= 0 and low[neighbor] >= discovery[vertex]:
                    articulations.add(vertex)
            elif neighbor != parent[vertex]:
                low[vertex] = min(low[vertex], discovery[neighbor])

    for vertex in range(len(adjacency)):
        if discovery[vertex] < 0:
            visit(vertex)

    return tuple(sorted(bridges)), tuple(sorted(articulations)), edge_scans


def cycle_structure(public: GluingPublicInstance) -> CycleStructure:
    vertices: set[int] = set()
    edges: set[tuple[int, int]] = set()
    vertex_tetrahedra: dict[int, int] = defaultdict(int)

    for tetrahedron in public.tetrahedra:
        vertices.update(tetrahedron)
        edges.update(tuple(sorted(edge)) for edge in combinations(tetrahedron, 2))
        for vertex in tetrahedron:
            vertex_tetrahedra[vertex] += 1

    faces, face_occurrences = _face_incidence(public.tetrahedra)
    max_face_incidence = max((len(owners) for owners in faces.values()), default=0)
    boundary_faces = sum(1 for owners in faces.values() if len(owners) == 1)
    adjacency, edge_faces, _ = _dual_graph(public)
    bridges, articulations, edge_scans = _bridges_and_articulations(adjacency)

    dual_histogram = Counter(len(neighbors) for neighbors in adjacency)
    vertex_histogram = Counter(vertex_tetrahedra.values())
    tetrahedron_count = len(public.tetrahedra)

    return CycleStructure(
        vertices=len(vertices),
        edges=len(edges),
        faces=len(faces),
        tetrahedra=tetrahedron_count,
        boundary_faces=boundary_faces,
        max_face_incidence=max_face_incidence,
        euler_characteristic=len(vertices) - len(edges) + len(faces) - tetrahedron_count,
        dual_edges=len(edge_faces),
        bridges=bridges,
        articulation_vertices=articulations,
        dual_degree_histogram=tuple(sorted(dual_histogram.items())),
        vertex_tetrahedron_degree_histogram=tuple(sorted(vertex_histogram.items())),
        face_occurrences=face_occurrences,
        dfs_edge_scans=edge_scans,
    )


def validate_cycle_gluing_witness(
    public: GluingPublicInstance,
    groups: tuple[TetrahedronGroup, ...],
) -> CycleGluingValidation:
    normalized = _normalize_groups(groups)
    component_sizes = tuple(sorted(len(group) for group in normalized))
    if len(normalized) != public.piece_count:
        return CycleGluingValidation(False, "wrong piece count", len(normalized), 0, component_sizes)

    flattened = [tetrahedron for group in normalized for tetrahedron in group]
    if sorted(flattened) != list(range(len(public.tetrahedra))):
        return CycleGluingValidation(
            False,
            "groups do not partition public tetrahedra",
            len(normalized),
            0,
            component_sizes,
        )

    if not all(_piece_is_valid(public, group) for group in normalized):
        return CycleGluingValidation(
            False,
            "a recovered block is not the allowed 3-ball piece",
            len(normalized),
            0,
            component_sizes,
        )

    faces, _ = _face_incidence(public.tetrahedra)
    if any(len(owners) > 2 for owners in faces.values()):
        return CycleGluingValidation(
            False,
            "public face has incidence above two",
            len(normalized),
            0,
            component_sizes,
        )

    owner_group: dict[int, int] = {}
    for group_index, group in enumerate(normalized):
        for tetrahedron in group:
            owner_group[tetrahedron] = group_index

    cross_pairs: list[DualEdge] = []
    for owners in faces.values():
        if len(owners) != 2:
            continue
        left = owner_group[owners[0]]
        right = owner_group[owners[1]]
        if left != right:
            cross_pairs.append(tuple(sorted((left, right))))

    if len(cross_pairs) != public.piece_count or len(set(cross_pairs)) != public.piece_count:
        return CycleGluingValidation(
            False,
            "cross-piece shared faces do not form n distinct cycle edges",
            len(normalized),
            len(cross_pairs),
            component_sizes,
        )

    adjacency = [set() for _ in range(public.piece_count)]
    for left, right in cross_pairs:
        adjacency[left].add(right)
        adjacency[right].add(left)

    if any(len(neighbors) != 2 for neighbors in adjacency):
        return CycleGluingValidation(
            False,
            "cross-piece graph is not 2-regular",
            len(normalized),
            len(cross_pairs),
            component_sizes,
        )

    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbor in adjacency[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)

    if len(seen) != public.piece_count:
        return CycleGluingValidation(
            False,
            "cross-piece cycle is disconnected",
            len(normalized),
            len(cross_pairs),
            component_sizes,
        )

    return CycleGluingValidation(
        True,
        "accepted",
        len(normalized),
        len(cross_pairs),
        component_sizes,
    )


def _exact_cover_candidates(
    public: GluingPublicInstance,
    candidates: tuple[TetrahedronGroup, ...],
    solution_cap: int = 64,
) -> ExactCoverResult:
    if solution_cap <= 0:
        raise GluingExperimentError("G1 exact-cover solution cap must be positive")

    normalized_candidates = tuple(sorted(set(_normalize_groups(candidates))))
    by_tetrahedron: dict[int, list[int]] = defaultdict(list)
    candidate_sets = [set(group) for group in normalized_candidates]
    for candidate_index, group in enumerate(normalized_candidates):
        for tetrahedron in group:
            by_tetrahedron[tetrahedron].append(candidate_index)

    nodes = 0
    backtracks = 0
    solutions = 0
    first_groups: tuple[TetrahedronGroup, ...] | None = None
    first_validation = CycleGluingValidation(False, "no exact cover", 0, 0, ())
    stopped = False

    def search(covered: set[int], chosen: list[int]) -> None:
        nonlocal nodes, backtracks, solutions, first_groups, first_validation, stopped
        if stopped:
            return
        nodes += 1

        if len(covered) == len(public.tetrahedra):
            groups = _normalize_groups(tuple(normalized_candidates[index] for index in chosen))
            validation = validate_cycle_gluing_witness(public, groups)
            if validation.valid:
                solutions += 1
                if first_groups is None:
                    first_groups = groups
                    first_validation = validation
                if solutions >= solution_cap:
                    stopped = True
            else:
                backtracks += 1
            return

        uncovered = [index for index in range(len(public.tetrahedra)) if index not in covered]
        selected = min(
            uncovered,
            key=lambda tetrahedron: sum(
                1
                for candidate_index in by_tetrahedron.get(tetrahedron, ())
                if not (candidate_sets[candidate_index] & covered)
            ),
        )
        options = [
            candidate_index
            for candidate_index in by_tetrahedron.get(selected, ())
            if not (candidate_sets[candidate_index] & covered)
        ]
        if not options:
            backtracks += 1
            return

        before = solutions
        for candidate_index in options:
            candidate_set = candidate_sets[candidate_index]
            search(covered | candidate_set, chosen + [candidate_index])
            if stopped:
                return
        if solutions == before:
            backtracks += 1

    search(set(), [])
    return ExactCoverResult(
        groups=first_groups,
        nodes=nodes,
        backtracks=backtracks,
        solutions=solutions,
        exhausted=not stopped,
        validation=first_validation,
    )


def recover_cycle_by_vertex_stars(
    public: GluingPublicInstance,
    reference: CycleGluingReference | None = None,
    solution_cap: int = 64,
) -> StarRecovery:
    vertex_tetrahedra: dict[int, list[int]] = defaultdict(list)
    for tetrahedron_index, tetrahedron in enumerate(public.tetrahedra):
        for vertex in tetrahedron:
            vertex_tetrahedra[vertex].append(tetrahedron_index)

    candidates: set[TetrahedronGroup] = set()
    candidate_vertices = 0
    for incident in vertex_tetrahedra.values():
        if len(incident) != 4:
            continue
        candidate_vertices += 1
        group = tuple(sorted(incident))
        if _piece_is_valid(public, group):
            candidates.add(group)

    normalized = tuple(sorted(candidates))
    exact_cover = _exact_cover_candidates(public, normalized, solution_cap=solution_cap)
    matches = bool(
        reference is not None
        and exact_cover.groups is not None
        and _normalize_groups(reference.groups) == _normalize_groups(exact_cover.groups)
    )
    return StarRecovery(
        candidate_vertices=candidate_vertices,
        valid_candidates=normalized,
        exact_cover=exact_cover,
        matches_reference=matches,
    )


def recover_cycle_by_dual_k4(
    public: GluingPublicInstance,
    reference: CycleGluingReference | None = None,
    solution_cap: int = 64,
) -> K4Recovery:
    adjacency, _, _ = _dual_graph(public)
    candidates: list[TetrahedronGroup] = []
    subset_checks = 0
    clique_candidates = 0

    for group in combinations(range(len(public.tetrahedra)), 4):
        subset_checks += 1
        if not all(right in adjacency[left] for left, right in combinations(group, 2)):
            continue
        clique_candidates += 1
        if _piece_is_valid(public, group):
            candidates.append(tuple(group))

    normalized = tuple(sorted(set(candidates)))
    exact_cover = _exact_cover_candidates(public, normalized, solution_cap=solution_cap)
    matches = bool(
        reference is not None
        and exact_cover.groups is not None
        and _normalize_groups(reference.groups) == _normalize_groups(exact_cover.groups)
    )
    return K4Recovery(
        subset_checks=subset_checks,
        clique_candidates=clique_candidates,
        valid_candidates=normalized,
        exact_cover=exact_cover,
        matches_reference=matches,
    )


def generate_cycle_gluing_instance(
    params: CycleGluingParameters,
    master_seed: bytes,
) -> tuple[GluingPublicInstance, CycleGluingReference]:
    params.validate()
    if len(master_seed) < 16:
        raise GluingExperimentError("G1 master seed must contain at least 128 bits")

    piece_count = params.piece_count
    union_find = _UnionFind(5 * piece_count)
    swap_rng = _DeterministicRng(
        b"MORPH-KEM G1 cycle-swap v1/" + params.name.encode("ascii"),
        master_seed,
    )

    swap_bits = [swap_rng.randbelow(2) for _ in range(piece_count - 1)]
    # Ports 0/1 share the local coordinates 3 and 4.  Keeping vertex 1->2
    # fixed and forcing even total 3/4 swap parity closes the cycle without
    # identifying 3 and 4 inside a piece.  This gives seeded face maps while
    # avoiding a rejection-loop that could itself become a hidden condition.
    swap_bits.append(sum(swap_bits) & 1)

    for piece, swap in enumerate(swap_bits):
        next_piece = (piece + 1) % piece_count
        left_face = [5 * piece + vertex for vertex in _BASE_PORTS[1]]
        right_face = [5 * next_piece + vertex for vertex in _BASE_PORTS[0]]
        order = (0, 2, 1) if swap else (0, 1, 2)
        for left_index, right_index in enumerate(order):
            union_find.union(left_face[left_index], right_face[right_index])

    roots = sorted({union_find.find(vertex) for vertex in range(5 * piece_count)})
    root_index = {root: index for index, root in enumerate(roots)}

    quotient_tetrahedra: list[Tetrahedron] = []
    local_groups: list[TetrahedronGroup] = []
    for piece in range(piece_count):
        group: list[int] = []
        for tetrahedron in _BASE_TETRAHEDRA:
            quotient = tuple(
                sorted(root_index[union_find.find(5 * piece + vertex)] for vertex in tetrahedron)
            )
            if len(set(quotient)) != 4:
                raise GluingExperimentError("G1 parity-conditioned gluing produced a degenerate tetrahedron")
            group.append(len(quotient_tetrahedra))
            quotient_tetrahedra.append(quotient)
        local_groups.append(tuple(group))

    if len(set(quotient_tetrahedra)) != len(quotient_tetrahedra):
        raise GluingExperimentError("G1 parity-conditioned gluing produced duplicate tetrahedra")

    face_incidence, _ = _face_incidence(tuple(quotient_tetrahedra))
    if any(len(owners) > 2 for owners in face_incidence.values()):
        raise GluingExperimentError("G1 parity-conditioned gluing exceeds face incidence two")

    labels = list(range(len(roots)))
    label_rng = _DeterministicRng(
        b"MORPH-KEM G1 public-relabel v1/" + params.name.encode("ascii"),
        master_seed,
    )
    label_rng.shuffle(labels)
    relabeled = [
        tuple(sorted(labels[vertex] for vertex in tetrahedron))
        for tetrahedron in quotient_tetrahedra
    ]

    order = sorted(range(len(relabeled)), key=relabeled.__getitem__)
    public_tetrahedra = tuple(relabeled[index] for index in order)
    old_to_public = {old: new for new, old in enumerate(order)}
    reference_groups = _normalize_groups(
        tuple(
            tuple(old_to_public[tetrahedron] for tetrahedron in group)
            for group in local_groups
        )
    )
    cycle_edges = tuple(
        sorted(tuple(sorted((piece, (piece + 1) % piece_count))) for piece in range(piece_count))
    )

    public = GluingPublicInstance(
        name=params.name,
        piece_count=piece_count,
        tetrahedra=public_tetrahedra,
    )
    reference = CycleGluingReference(
        groups=reference_groups,
        cycle_edges=cycle_edges,
        swap_bits=tuple(swap_bits),
    )

    validation = validate_cycle_gluing_witness(public, reference.groups)
    if not validation.valid:
        raise GluingExperimentError(f"G1 generated reference witness rejected: {validation.reason}")

    structure = cycle_structure(public)
    if structure.bridges or structure.articulation_vertices:
        raise GluingExperimentError("G1 failed its bridge/articulation structural gate")
    if structure.dual_edges != 7 * piece_count:
        raise GluingExperimentError("G1 unexpected tetrahedron-dual edge count")

    return public, reference
