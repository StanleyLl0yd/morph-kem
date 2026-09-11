from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass
import hashlib
from itertools import combinations

from .complex import SimplicialComplex
from .gluing import GluingExperimentError
from .gluing_cohomology_cycle import (
    CohomologyCyclePublicInstance,
    CycleWitness,
    Edge,
    _edges,
    _nullspace_basis,
    _pairing,
    _public_spanning_forest,
    _reduce_by_rowspace,
    _rref,
    _tree_path_edges,
    validate_cohomology_cycle_witness,
)
from .gluing_irregular_hypercover import (
    _final_relabel,
    _flip_surface,
    _normalization_improving_flip_count,
    _primal_vertex_degree_histogram,
)
from .gluing_matching import _bridges_and_articulations
from .gluing_surface_hypercover import (
    ToroidalHypercoverPublicInstance,
    toroidal_hypercover_incidence,
)
from .surface import SurfaceParameters, generate_surface_instance


Triangle = tuple[int, int, int]


@dataclass(frozen=True, slots=True)
class GenusTwoMulticurveParameters:
    name: str
    rows: int
    cols: int
    successful_flips: int
    max_generation_retries: int = 16

    def validate(self) -> None:
        if self.rows < 4 or self.rows > 12 or self.cols < 4 or self.cols > 12:
            raise GluingExperimentError("G20 torus dimensions outside toy bounds")
        base_triangles = 4 * self.rows * self.cols - 2
        if self.successful_flips < 1 or self.successful_flips > 8 * base_triangles:
            raise GluingExperimentError("G20 successful-flip target outside toy bounds")
        if self.max_generation_retries < 0 or self.max_generation_retries > 64:
            raise GluingExperimentError("G20 generation retry cap outside toy bounds")


G20_PARAMETER_SETS = {
    "g20-4x4": GenusTwoMulticurveParameters("g20-4x4", 4, 4, 124),
    "g20-6x6": GenusTwoMulticurveParameters("g20-6x6", 6, 6, 284),
    "g20-6x9": GenusTwoMulticurveParameters("g20-6x9", 6, 9, 428),
}


@dataclass(frozen=True, slots=True)
class GenusTwoMulticurvePublicInstance:
    name: str
    target: SimplicialComplex
    alpha: tuple[int, ...]
    beta: tuple[int, ...]
    max_alpha_length: int
    max_beta_length: int


@dataclass(frozen=True, slots=True)
class GenusTwoMulticurveWitness:
    alpha_cycle: CycleWitness
    beta_cycle: CycleWitness


@dataclass(frozen=True, slots=True)
class GenusTwoMulticurveReference:
    witness: GenusTwoMulticurveWitness
    generation_retries: int
    reference_tree_attempts: int


@dataclass(frozen=True, slots=True)
class GenusTwoMulticurveValidation:
    valid: bool
    reason: str
    alpha_length: int
    beta_length: int
    alpha_signature: tuple[int, int]
    beta_signature: tuple[int, int]
    shared_vertices: int


@dataclass(frozen=True, slots=True)
class GenusTwoMulticurveRecovery:
    vertices: int
    edges: int
    triangles: int
    euler_characteristic: int
    min_triangles_per_edge: int
    max_triangles_per_edge: int
    successful_flips: int
    generation_retries: int
    primal_vertex_degree_histogram: tuple[tuple[int, int], ...]
    normalization_improving_flips: int
    h1_dimension: int
    alpha_weight: int
    beta_weight: int
    max_alpha_length: int
    max_beta_length: int
    reference_alpha_length: int | None
    reference_beta_length: int | None
    articulation_points: tuple[int, ...]
    two_vertex_separator_count: int
    separating_triangle_count: int
    first_separating_triangle: tuple[int, int, int] | None
    first_separating_component_sizes: tuple[int, ...]
    four_sheet_states: int
    alpha_roots: int
    alpha_queue_pops: int
    alpha_edge_scans: int
    alpha_candidates: int
    alpha_length_histogram: tuple[tuple[int, int], ...]
    alpha_candidates_attempted: int
    beta_stage_calls: int
    beta_roots: int
    beta_reachable_roots: int
    beta_queue_pops: int
    beta_edge_scans: int
    beta_candidates: int
    selected_deleted_vertices: int
    selected_deleted_edges: int
    selected_alpha_length: int
    selected_beta_length: int
    selected_alpha_signature: tuple[int, int]
    selected_beta_signature: tuple[int, int]
    selected_shared_vertices: int
    selected_accepted: bool
    selected_matches_reference: bool | None
    independent_alpha_cycles: int
    independent_beta_cycles: int
    independent_pair_tests: int
    independent_pair_found: bool
    independent_pair_accepted: bool


@dataclass(frozen=True, slots=True)
class _CoverSearch:
    candidates: tuple[tuple[int, ...], ...]
    roots_attempted: int
    reachable_roots: int
    queue_pops: int
    edge_scans: int
    decomposition_cycles: int
    decomposition_scans: int


def _triangles(target: SimplicialComplex) -> tuple[Triangle, ...]:
    return tuple(sorted(simplex for simplex in target.simplices if len(simplex) == 3))


def _connected_sum_tori(
    params: GenusTwoMulticurveParameters,
    seed: bytes,
) -> SimplicialComplex:
    left_seed = hashlib.sha256(b"MORPH-KEM G20 left torus v1\x00" + seed).digest()
    right_seed = hashlib.sha256(b"MORPH-KEM G20 right torus v1\x00" + seed).digest()
    left, _ = generate_surface_instance(
        SurfaceParameters(params.name + "-left", params.rows, params.cols), left_seed
    )
    right, _ = generate_surface_instance(
        SurfaceParameters(params.name + "-right", params.rows, params.cols), right_seed
    )
    left_facets = set(_triangles(left.target))
    right_facets = set(_triangles(right.target))
    left_hole = min(left_facets)
    right_hole = min(right_facets)
    left_facets.remove(left_hole)
    right_facets.remove(right_hole)

    offset = len(left.target.vertices)
    right_hole_offset = tuple(vertex + offset for vertex in right_hole)
    seam_map = {
        right_hole_offset[0]: left_hole[0],
        right_hole_offset[1]: left_hole[2],
        right_hole_offset[2]: left_hole[1],
    }
    mapped_right: set[Triangle] = set()
    for triangle in right_facets:
        values = tuple(
            sorted(seam_map.get(vertex + offset, vertex + offset) for vertex in triangle)
        )
        if len(set(values)) != 3:
            raise GluingExperimentError("G20 connected sum produced degenerate triangle")
        mapped_right.add(values)
    combined = left_facets | mapped_right
    if len(combined) != len(left_facets) + len(mapped_right):
        raise GluingExperimentError("G20 connected sum produced duplicate triangles")
    target = SimplicialComplex.from_facets(tuple(sorted(combined)))
    expected_vertices = 2 * params.rows * params.cols - 3
    expected_edges = 6 * params.rows * params.cols - 3
    expected_triangles = 4 * params.rows * params.cols - 2
    incidence = toroidal_hypercover_incidence(
        ToroidalHypercoverPublicInstance(params.name + "-raw", target)
    )
    if (
        incidence.vertices,
        incidence.edges,
        incidence.triangles,
    ) != (expected_vertices, expected_edges, expected_triangles):
        raise GluingExperimentError("G20 connected-sum cell counts differ from expectation")
    if incidence.euler_characteristic != -2:
        raise GluingExperimentError("G20 connected sum does not have Euler characteristic -2")
    if incidence.min_triangles_per_edge != 2 or incidence.max_triangles_per_edge != 2:
        raise GluingExperimentError("G20 connected sum is not closed")
    return target


def _cohomology_basis(
    target: SimplicialComplex,
) -> tuple[tuple[Edge, ...], tuple[int, ...], int]:
    edges = _edges(target)
    edge_index = {edge: index for index, edge in enumerate(edges)}
    triangle_rows: list[int] = []
    for triangle in _triangles(target):
        mask = 0
        for edge in combinations(triangle, 2):
            mask ^= 1 << edge_index[tuple(sorted(edge))]
        triangle_rows.append(mask)
    cocycle_rref = _rref(triangle_rows, len(edges))
    cocycle_basis = _nullspace_basis(cocycle_rref, len(edges))

    vertex_rows: list[int] = []
    for vertex in target.vertices:
        mask = 0
        for index, edge in enumerate(edges):
            if vertex in edge:
                mask ^= 1 << index
        vertex_rows.append(mask)
    coboundary_rref = _rref(vertex_rows, len(edges))

    quotient_vectors = sorted(
        {
            reduced
            for vector in cocycle_basis
            if (reduced := _reduce_by_rowspace(vector, coboundary_rref)) != 0
        }
    )
    pivots: dict[int, int] = {}
    selected: list[int] = []
    for vector in quotient_vectors:
        value = vector
        while value:
            pivot = value.bit_length() - 1
            existing = pivots.get(pivot)
            if existing is None:
                pivots[pivot] = value
                selected.append(vector)
                break
            value ^= existing
    h1_dimension = len(cocycle_basis) - coboundary_rref.rank
    if len(selected) != h1_dimension:
        raise GluingExperimentError("G20 failed to extract full public H1 basis")
    return edges, tuple(selected), h1_dimension


def _bits(mask: int, width: int) -> tuple[int, ...]:
    return tuple((mask >> index) & 1 for index in range(width))


def _cycle_vertices(cycle: CycleWitness) -> frozenset[int]:
    result: set[int] = set()
    for edge in cycle:
        result.update(edge)
    return frozenset(result)


def _witness_from_indices(edges: tuple[Edge, ...], indices: tuple[int, ...]) -> CycleWitness:
    return tuple(sorted(edges[index] for index in indices))


def _signature(
    alpha: tuple[int, ...],
    beta: tuple[int, ...],
    indices: tuple[int, ...],
) -> tuple[int, int]:
    return _pairing(alpha, indices), _pairing(beta, indices)


def _witness_signature(
    public: GenusTwoMulticurvePublicInstance,
    cycle: CycleWitness,
) -> tuple[int, int]:
    edges = _edges(public.target)
    lookup = {edge: index for index, edge in enumerate(edges)}
    try:
        indices = tuple(lookup[edge] for edge in cycle)
    except KeyError:
        return (-1, -1)
    return _signature(public.alpha, public.beta, indices)


def validate_genus2_multicurve_witness(
    public: GenusTwoMulticurvePublicInstance,
    witness: GenusTwoMulticurveWitness,
) -> GenusTwoMulticurveValidation:
    alpha_check = validate_cohomology_cycle_witness(
        CohomologyCyclePublicInstance(public.name, public.target, public.alpha),
        witness.alpha_cycle,
    )
    beta_check = validate_cohomology_cycle_witness(
        CohomologyCyclePublicInstance(public.name, public.target, public.beta),
        witness.beta_cycle,
    )
    alpha_signature = _witness_signature(public, witness.alpha_cycle)
    beta_signature = _witness_signature(public, witness.beta_cycle)
    shared = len(_cycle_vertices(witness.alpha_cycle) & _cycle_vertices(witness.beta_cycle))
    if not alpha_check.valid:
        return GenusTwoMulticurveValidation(
            False, "G20 alpha cycle rejected: " + alpha_check.reason,
            len(witness.alpha_cycle), len(witness.beta_cycle), alpha_signature, beta_signature, shared
        )
    if not beta_check.valid:
        return GenusTwoMulticurveValidation(
            False, "G20 beta cycle rejected: " + beta_check.reason,
            len(witness.alpha_cycle), len(witness.beta_cycle), alpha_signature, beta_signature, shared
        )
    if alpha_signature != (1, 0) or beta_signature != (0, 1):
        return GenusTwoMulticurveValidation(
            False, "G20 cycle signatures do not match public roles",
            len(witness.alpha_cycle), len(witness.beta_cycle), alpha_signature, beta_signature, shared
        )
    if shared:
        return GenusTwoMulticurveValidation(
            False, "G20 cycles are not vertex-disjoint",
            len(witness.alpha_cycle), len(witness.beta_cycle), alpha_signature, beta_signature, shared
        )
    if len(witness.alpha_cycle) > public.max_alpha_length:
        return GenusTwoMulticurveValidation(
            False, "G20 alpha cycle exceeds public bound",
            len(witness.alpha_cycle), len(witness.beta_cycle), alpha_signature, beta_signature, shared
        )
    if len(witness.beta_cycle) > public.max_beta_length:
        return GenusTwoMulticurveValidation(
            False, "G20 beta cycle exceeds public bound",
            len(witness.alpha_cycle), len(witness.beta_cycle), alpha_signature, beta_signature, shared
        )
    return GenusTwoMulticurveValidation(
        True, "accepted", len(witness.alpha_cycle), len(witness.beta_cycle),
        alpha_signature, beta_signature, 0
    )


def _seeded_reference_pair(
    vertex_count: int,
    edges: tuple[Edge, ...],
    alpha: tuple[int, ...],
    beta: tuple[int, ...],
    seed: bytes,
    max_attempts: int = 64,
) -> tuple[GenusTwoMulticurveWitness, int]:
    from .gluing_length_bounded_pair import _seeded_spanning_tree

    for attempt in range(max_attempts):
        tree_seed = hashlib.sha256(
            b"MORPH-KEM G20 reference tree v1\x00" + seed + attempt.to_bytes(4, "big")
        ).digest()
        tree = _seeded_spanning_tree(vertex_count, edges, tree_seed)
        alpha_cycles: list[tuple[int, ...]] = []
        beta_cycles: list[tuple[int, ...]] = []
        for edge_index in range(len(edges)):
            if edge_index in tree.tree_edges:
                continue
            left, right = edges[edge_index]
            cycle = tuple(sorted(_tree_path_edges(left, right, tree) + (edge_index,)))
            signature = _signature(alpha, beta, cycle)
            if signature == (1, 0):
                alpha_cycles.append(cycle)
            elif signature == (0, 1):
                beta_cycles.append(cycle)
        alpha_cycles.sort(key=lambda cycle: (len(cycle), cycle))
        beta_cycles.sort(key=lambda cycle: (len(cycle), cycle))
        alpha_vertices = [_cycle_vertices(_witness_from_indices(edges, cycle)) for cycle in alpha_cycles]
        beta_vertices = [_cycle_vertices(_witness_from_indices(edges, cycle)) for cycle in beta_cycles]
        for alpha_index, alpha_cycle in enumerate(alpha_cycles):
            for beta_index, beta_cycle in enumerate(beta_cycles):
                if not alpha_vertices[alpha_index].isdisjoint(beta_vertices[beta_index]):
                    continue
                return (
                    GenusTwoMulticurveWitness(
                        _witness_from_indices(edges, alpha_cycle),
                        _witness_from_indices(edges, beta_cycle),
                    ),
                    attempt + 1,
                )
    raise GluingExperimentError("G20 reference search found no disjoint class pair")


def _primal_adjacency(vertex_count: int, edges: tuple[Edge, ...]) -> list[list[int]]:
    adjacency = [set() for _ in range(vertex_count)]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    return [sorted(values) for values in adjacency]


def _component_sizes_after_removal(
    adjacency: list[list[int]],
    removed: frozenset[int],
) -> tuple[int, ...]:
    remaining = [vertex for vertex in range(len(adjacency)) if vertex not in removed]
    if not remaining:
        return ()
    seen: set[int] = set()
    sizes: list[int] = []
    for root in remaining:
        if root in seen:
            continue
        stack = [root]
        seen.add(root)
        size = 0
        while stack:
            current = stack.pop()
            size += 1
            for neighbor in adjacency[current]:
                if neighbor in removed or neighbor in seen:
                    continue
                seen.add(neighbor)
                stack.append(neighbor)
        sizes.append(size)
    return tuple(sorted(sizes))


def _separator_metrics(
    vertex_count: int,
    edges: tuple[Edge, ...],
) -> tuple[tuple[int, ...], int, tuple[tuple[int, int, int], ...], tuple[int, ...]]:
    adjacency = _primal_adjacency(vertex_count, edges)
    _, articulations = _bridges_and_articulations(adjacency)
    two_vertex = 0
    for left in range(vertex_count):
        for right in range(left + 1, vertex_count):
            if len(_component_sizes_after_removal(adjacency, frozenset((left, right)))) > 1:
                two_vertex += 1

    neighbor_sets = [set(values) for values in adjacency]
    cycles: set[tuple[int, int, int]] = set()
    for left in range(vertex_count):
        for right in adjacency[left]:
            if left >= right:
                continue
            for third in neighbor_sets[left] & neighbor_sets[right]:
                if right < third:
                    cycles.add((left, right, third))
    separating: list[tuple[int, int, int]] = []
    first_sizes: tuple[int, ...] = ()
    for cycle in sorted(cycles):
        sizes = _component_sizes_after_removal(adjacency, frozenset(cycle))
        if len(sizes) > 1:
            separating.append(cycle)
            if not first_sizes:
                first_sizes = sizes
    return tuple(sorted(articulations)), two_vertex, tuple(separating), first_sizes


def _cover_path(
    root: int,
    target_signature: int,
    vertex_count: int,
    edges: tuple[Edge, ...],
    labels: tuple[int, ...],
    allowed_edges: frozenset[int],
) -> tuple[tuple[int, ...] | None, int, int]:
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for edge_index in allowed_edges:
        left, right = edges[edge_index]
        adjacency[left].append((right, edge_index))
        adjacency[right].append((left, edge_index))
    for row in adjacency:
        row.sort()
    start = 4 * root
    goal = start + target_signature
    parent = [-1] * (4 * vertex_count)
    parent_edge = [-1] * (4 * vertex_count)
    parent[start] = start
    queue = deque([start])
    pops = 0
    scans = 0
    while queue:
        state = queue.popleft()
        pops += 1
        if state == goal:
            break
        vertex = state // 4
        signature = state & 3
        for neighbor, edge_index in adjacency[vertex]:
            scans += 1
            next_state = 4 * neighbor + (signature ^ labels[edge_index])
            if parent[next_state] != -1:
                continue
            parent[next_state] = state
            parent_edge[next_state] = edge_index
            queue.append(next_state)
    if parent[goal] == -1:
        return None, pops, scans
    path: list[int] = []
    state = goal
    while state != start:
        edge_index = parent_edge[state]
        if edge_index < 0:
            raise GluingExperimentError("G20 four-sheet path reconstruction failed")
        path.append(edge_index)
        state = parent[state]
    path.reverse()
    return tuple(path), pops, scans


def _xor_support(path: tuple[int, ...]) -> frozenset[int]:
    support: set[int] = set()
    for edge_index in path:
        if edge_index in support:
            support.remove(edge_index)
        else:
            support.add(edge_index)
    return frozenset(support)


def _four_sheet_candidates(
    vertex_count: int,
    edges: tuple[Edge, ...],
    alpha: tuple[int, ...],
    beta: tuple[int, ...],
    target_signature: int,
    forbidden_vertices: frozenset[int] = frozenset(),
) -> _CoverSearch:
    labels = tuple(alpha[index] | (beta[index] << 1) for index in range(len(edges)))
    allowed_edges = frozenset(
        index
        for index, edge in enumerate(edges)
        if edge[0] not in forbidden_vertices and edge[1] not in forbidden_vertices
    )
    candidates: set[tuple[int, ...]] = set()
    roots_attempted = 0
    reachable = 0
    pops = 0
    scans = 0
    decomposition_cycles = 0
    decomposition_scans = 0
    for root in range(vertex_count):
        if root in forbidden_vertices:
            continue
        roots_attempted += 1
        path, root_pops, root_scans = _cover_path(
            root, target_signature, vertex_count, edges, labels, allowed_edges
        )
        pops += root_pops
        scans += root_scans
        if path is None:
            continue
        reachable += 1
        support = _xor_support(path)
        if not support:
            continue
        tree, _ = _public_spanning_forest(vertex_count, edges, support)
        for edge_index in sorted(support):
            if edge_index in tree.tree_edges:
                continue
            left, right = edges[edge_index]
            tree_path = _tree_path_edges(left, right, tree)
            decomposition_cycles += 1
            decomposition_scans += len(tree_path)
            cycle = tuple(sorted(tree_path + (edge_index,)))
            signature = _signature(alpha, beta, cycle)
            encoded = signature[0] | (signature[1] << 1)
            if encoded == target_signature:
                candidates.add(cycle)
    return _CoverSearch(
        tuple(sorted(candidates, key=lambda cycle: (len(cycle), cycle))),
        roots_attempted,
        reachable,
        pops,
        scans,
        decomposition_cycles,
        decomposition_scans,
    )


def _independent_pair(
    vertex_count: int,
    edges: tuple[Edge, ...],
    alpha: tuple[int, ...],
    beta: tuple[int, ...],
    public: GenusTwoMulticurvePublicInstance,
) -> tuple[int, int, int, GenusTwoMulticurveWitness | None]:
    tree, components = _public_spanning_forest(vertex_count, edges)
    if components != 1:
        raise GluingExperimentError("G20 independent primal graph is disconnected")
    alpha_cycles: list[tuple[int, ...]] = []
    beta_cycles: list[tuple[int, ...]] = []
    for edge_index in range(len(edges)):
        if edge_index in tree.tree_edges:
            continue
        left, right = edges[edge_index]
        cycle = tuple(sorted(_tree_path_edges(left, right, tree) + (edge_index,)))
        signature = _signature(alpha, beta, cycle)
        if signature == (1, 0):
            alpha_cycles.append(cycle)
        elif signature == (0, 1):
            beta_cycles.append(cycle)
    alpha_cycles.sort(key=lambda cycle: (len(cycle), cycle))
    beta_cycles.sort(key=lambda cycle: (len(cycle), cycle))
    tests = 0
    for alpha_cycle in alpha_cycles:
        alpha_witness = _witness_from_indices(edges, alpha_cycle)
        alpha_vertices = _cycle_vertices(alpha_witness)
        for beta_cycle in beta_cycles:
            tests += 1
            beta_witness = _witness_from_indices(edges, beta_cycle)
            if not alpha_vertices.isdisjoint(_cycle_vertices(beta_witness)):
                continue
            witness = GenusTwoMulticurveWitness(alpha_witness, beta_witness)
            if validate_genus2_multicurve_witness(public, witness).valid:
                return len(alpha_cycles), len(beta_cycles), tests, witness
    return len(alpha_cycles), len(beta_cycles), tests, None


def recover_genus2_multicurve(
    public: GenusTwoMulticurvePublicInstance,
    *,
    reference: GenusTwoMulticurveReference | None = None,
    successful_flips: int = -1,
) -> GenusTwoMulticurveRecovery:
    edges, basis, h1_dimension = _cohomology_basis(public.target)
    if h1_dimension != 4 or len(basis) != 4:
        raise GluingExperimentError("G20 expected H1 dimension four")
    alpha_mask = sum(bit << index for index, bit in enumerate(public.alpha))
    beta_mask = sum(bit << index for index, bit in enumerate(public.beta))
    if alpha_mask != basis[0] or beta_mask != basis[1]:
        raise GluingExperimentError("G20 public cocycles are not canonical measured classes")
    incidence = toroidal_hypercover_incidence(
        ToroidalHypercoverPublicInstance(public.name, public.target)
    )
    articulations, two_vertex, separating, first_sizes = _separator_metrics(
        incidence.vertices, edges
    )

    alpha_search = _four_sheet_candidates(
        incidence.vertices, edges, public.alpha, public.beta, 1
    )
    alpha_candidates = tuple(
        cycle for cycle in alpha_search.candidates if len(cycle) <= public.max_alpha_length
    )
    alpha_histogram = tuple(sorted(Counter(map(len, alpha_candidates)).items()))

    attempted = 0
    beta_calls = 0
    beta_roots = 0
    beta_reachable = 0
    beta_pops = 0
    beta_scans = 0
    beta_candidate_total = 0
    selected: GenusTwoMulticurveWitness | None = None
    selected_validation: GenusTwoMulticurveValidation | None = None
    deleted_vertices = 0
    deleted_edges = 0
    for alpha_indices in alpha_candidates:
        attempted += 1
        alpha_cycle = _witness_from_indices(edges, alpha_indices)
        forbidden = _cycle_vertices(alpha_cycle)
        beta_calls += 1
        search = _four_sheet_candidates(
            incidence.vertices, edges, public.alpha, public.beta, 2, forbidden
        )
        beta_roots += search.roots_attempted
        beta_reachable += search.reachable_roots
        beta_pops += search.queue_pops
        beta_scans += search.edge_scans
        beta_candidates = tuple(
            cycle for cycle in search.candidates if len(cycle) <= public.max_beta_length
        )
        beta_candidate_total += len(beta_candidates)
        for beta_indices in beta_candidates:
            witness = GenusTwoMulticurveWitness(
                alpha_cycle,
                _witness_from_indices(edges, beta_indices),
            )
            validation = validate_genus2_multicurve_witness(public, witness)
            if not validation.valid:
                continue
            selected = witness
            selected_validation = validation
            deleted_vertices = len(forbidden)
            deleted_edges = sum(
                edge[0] in forbidden or edge[1] in forbidden for edge in edges
            )
            break
        if selected is not None:
            break
    if selected is None or selected_validation is None:
        raise GluingExperimentError("G20 A-047 found no bounded disjoint class pair")

    independent_alpha, independent_beta, independent_tests, independent = _independent_pair(
        incidence.vertices, edges, public.alpha, public.beta, public
    )
    independent_accepted = (
        independent is not None
        and validate_genus2_multicurve_witness(public, independent).valid
    )
    reference_witness = reference.witness if reference is not None else None
    selected_matches = None if reference_witness is None else selected == reference_witness

    return GenusTwoMulticurveRecovery(
        vertices=incidence.vertices,
        edges=incidence.edges,
        triangles=incidence.triangles,
        euler_characteristic=incidence.euler_characteristic,
        min_triangles_per_edge=incidence.min_triangles_per_edge,
        max_triangles_per_edge=incidence.max_triangles_per_edge,
        successful_flips=successful_flips,
        generation_retries=-1 if reference is None else reference.generation_retries,
        primal_vertex_degree_histogram=_primal_vertex_degree_histogram(public.target),
        normalization_improving_flips=_normalization_improving_flip_count(public.target),
        h1_dimension=h1_dimension,
        alpha_weight=sum(public.alpha),
        beta_weight=sum(public.beta),
        max_alpha_length=public.max_alpha_length,
        max_beta_length=public.max_beta_length,
        reference_alpha_length=None if reference is None else len(reference.witness.alpha_cycle),
        reference_beta_length=None if reference is None else len(reference.witness.beta_cycle),
        articulation_points=articulations,
        two_vertex_separator_count=two_vertex,
        separating_triangle_count=len(separating),
        first_separating_triangle=None if not separating else separating[0],
        first_separating_component_sizes=first_sizes,
        four_sheet_states=4 * incidence.vertices,
        alpha_roots=alpha_search.roots_attempted,
        alpha_queue_pops=alpha_search.queue_pops,
        alpha_edge_scans=alpha_search.edge_scans,
        alpha_candidates=len(alpha_candidates),
        alpha_length_histogram=alpha_histogram,
        alpha_candidates_attempted=attempted,
        beta_stage_calls=beta_calls,
        beta_roots=beta_roots,
        beta_reachable_roots=beta_reachable,
        beta_queue_pops=beta_pops,
        beta_edge_scans=beta_scans,
        beta_candidates=beta_candidate_total,
        selected_deleted_vertices=deleted_vertices,
        selected_deleted_edges=deleted_edges,
        selected_alpha_length=selected_validation.alpha_length,
        selected_beta_length=selected_validation.beta_length,
        selected_alpha_signature=selected_validation.alpha_signature,
        selected_beta_signature=selected_validation.beta_signature,
        selected_shared_vertices=selected_validation.shared_vertices,
        selected_accepted=selected_validation.valid,
        selected_matches_reference=selected_matches,
        independent_alpha_cycles=independent_alpha,
        independent_beta_cycles=independent_beta,
        independent_pair_tests=independent_tests,
        independent_pair_found=independent is not None,
        independent_pair_accepted=independent_accepted,
    )


def generate_genus2_multicurve_instance(
    params: GenusTwoMulticurveParameters,
    master_seed: bytes,
) -> tuple[GenusTwoMulticurvePublicInstance, GenusTwoMulticurveReference]:
    params.validate()
    if len(master_seed) < 16:
        raise GluingExperimentError("G20 master seed must contain at least 128 bits")

    for retry in range(params.max_generation_retries + 1):
        attempt_seed = hashlib.sha256(
            b"MORPH-KEM G20 carrier attempt v1\x00"
            + master_seed
            + params.name.encode("ascii")
            + retry.to_bytes(4, "big")
        ).digest()
        target = _connected_sum_tori(params, attempt_seed)
        target = _flip_surface(
            target,
            params.successful_flips,
            hashlib.sha256(b"MORPH-KEM G20 flips v1\x00" + attempt_seed).digest(),
        )
        target = _final_relabel(
            target,
            hashlib.sha256(b"MORPH-KEM G20 relabel v1\x00" + attempt_seed).digest(),
        )
        incidence = toroidal_hypercover_incidence(
            ToroidalHypercoverPublicInstance(params.name, target)
        )
        if incidence.euler_characteristic != -2:
            raise GluingExperimentError("G20 mixed carrier does not have chi=-2")
        if incidence.min_triangles_per_edge != 2 or incidence.max_triangles_per_edge != 2:
            raise GluingExperimentError("G20 mixed carrier is not closed")
        edges, basis, h1_dimension = _cohomology_basis(target)
        if h1_dimension != 4 or len(basis) != 4:
            raise GluingExperimentError("G20 mixed carrier does not have H1 dimension four")
        alpha = _bits(basis[0], len(edges))
        beta = _bits(basis[1], len(edges))
        reference_seed = hashlib.sha256(
            b"MORPH-KEM G20 hidden reference v1\x00" + attempt_seed
        ).digest()
        try:
            witness, tree_attempts = _seeded_reference_pair(
                incidence.vertices, edges, alpha, beta, reference_seed
            )
        except GluingExperimentError:
            continue
        public = GenusTwoMulticurvePublicInstance(
            params.name,
            target,
            alpha,
            beta,
            len(witness.alpha_cycle),
            len(witness.beta_cycle),
        )
        reference = GenusTwoMulticurveReference(witness, retry, tree_attempts)
        if not validate_genus2_multicurve_witness(public, witness).valid:
            raise GluingExperimentError("G20 generated reference witness does not validate")
        return public, reference
    raise GluingExperimentError("G20 exceeded generation retry cap without reference pair")
