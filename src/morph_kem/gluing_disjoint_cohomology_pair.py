from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass
import hashlib

from .complex import SimplicialComplex
from .gluing import GluingExperimentError
from .gluing_cohomology_cycle import (
    CohomologyCyclePublicInstance,
    CycleWitness,
    Edge,
    _cochain_metrics,
    _edges,
    _pairing,
    _public_spanning_forest,
    _tree_path_edges,
    validate_cohomology_cycle_witness,
)
from .gluing_irregular_hypercover import (
    _final_relabel,
    _flip_surface,
    _normalization_improving_flip_count,
    _primal_vertex_degree_histogram,
)
from .gluing_length_bounded_pair import (
    _seeded_spanning_tree,
    _shortest_public_odd_candidates,
)
from .gluing_surface_hypercover import (
    ToroidalHypercoverPublicInstance,
    toroidal_hypercover_incidence,
)
from .surface import SurfaceParameters, generate_surface_instance


@dataclass(frozen=True, slots=True)
class DisjointCohomologyPairParameters:
    name: str
    rows: int
    cols: int
    successful_flips: int

    def validate(self) -> None:
        if self.rows < 4 or self.rows > 12 or self.cols < 4 or self.cols > 12:
            raise GluingExperimentError("G19 torus dimensions outside toy bounds")
        triangle_count = 2 * self.rows * self.cols
        if self.successful_flips < 1 or self.successful_flips > triangle_count:
            raise GluingExperimentError("G19 successful-flip target outside toy bounds")


G19_PARAMETER_SETS = {
    "g19-6x6": DisjointCohomologyPairParameters("g19-6x6", 6, 6, 36),
    "g19-6x9": DisjointCohomologyPairParameters("g19-6x9", 6, 9, 54),
    "g19-8x9": DisjointCohomologyPairParameters("g19-8x9", 8, 9, 72),
}


@dataclass(frozen=True, slots=True)
class DisjointCohomologyPairPublicInstance:
    name: str
    target: SimplicialComplex
    alpha: tuple[int, ...]
    max_short_length: int
    max_long_length: int


@dataclass(frozen=True, slots=True)
class DisjointCohomologyPairWitness:
    first_cycle: CycleWitness
    second_cycle: CycleWitness


@dataclass(frozen=True, slots=True)
class DisjointCohomologyPairReference:
    witness: DisjointCohomologyPairWitness
    generation_retries: int
    reference_tree_attempts: int


@dataclass(frozen=True, slots=True)
class DisjointCohomologyPairValidation:
    valid: bool
    reason: str
    first_length: int
    second_length: int
    first_pairing: int
    second_pairing: int
    shared_vertices: int


@dataclass(frozen=True, slots=True)
class DisjointCohomologyPairRecovery:
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
    alpha_weight: int
    h1_dimension: int
    max_short_length: int
    max_long_length: int
    reference_short_length: int | None
    reference_long_length: int | None
    first_stage_roots: int
    first_stage_queue_pops: int
    first_stage_edge_scans: int
    first_stage_candidates: int
    first_stage_length_histogram: tuple[tuple[int, int], ...]
    first_candidates_attempted: int
    second_stage_calls: int
    second_stage_roots: int
    second_stage_reachable_roots: int
    second_stage_queue_pops: int
    second_stage_edge_scans: int
    second_stage_decomposition_cycles: int
    second_stage_decomposition_scans: int
    second_stage_candidates: int
    selected_deleted_vertices: int
    selected_deleted_edges: int
    selected_short_length: int
    selected_long_length: int
    selected_first_pairing: int
    selected_second_pairing: int
    selected_shared_vertices: int
    selected_accepted: bool
    selected_matches_reference: bool | None
    independent_odd_fundamental_cycles: int
    independent_pair_tests: int
    independent_pair_found: bool
    independent_pair_accepted: bool


@dataclass(frozen=True, slots=True)
class _RestrictedSearch:
    candidates: tuple[tuple[int, ...], ...]
    roots_attempted: int
    reachable_roots: int
    queue_pops: int
    edge_scans: int
    decomposition_cycles: int
    decomposition_scans: int


def _witness_from_indices(edges: tuple[Edge, ...], indices: tuple[int, ...]) -> CycleWitness:
    return tuple(sorted(edges[index] for index in indices))


def _cycle_vertices(edges: tuple[Edge, ...], indices: tuple[int, ...]) -> frozenset[int]:
    vertices: set[int] = set()
    for index in indices:
        vertices.update(edges[index])
    return frozenset(vertices)


def _witness_vertices(cycle: CycleWitness) -> frozenset[int]:
    vertices: set[int] = set()
    for edge in cycle:
        vertices.update(edge)
    return frozenset(vertices)


def _canonical_witness(
    first: CycleWitness,
    second: CycleWitness,
) -> DisjointCohomologyPairWitness:
    ordered = sorted((first, second), key=lambda cycle: (len(cycle), cycle))
    return DisjointCohomologyPairWitness(ordered[0], ordered[1])


def _canonical_index_pair(
    edges: tuple[Edge, ...],
    first: tuple[int, ...],
    second: tuple[int, ...],
) -> DisjointCohomologyPairWitness:
    return _canonical_witness(
        _witness_from_indices(edges, first),
        _witness_from_indices(edges, second),
    )


def validate_disjoint_cohomology_pair_witness(
    public: DisjointCohomologyPairPublicInstance,
    witness: DisjointCohomologyPairWitness,
) -> DisjointCohomologyPairValidation:
    if (len(witness.first_cycle), witness.first_cycle) > (
        len(witness.second_cycle), witness.second_cycle
    ):
        return DisjointCohomologyPairValidation(
            False,
            "G19 witness cycle pair is not canonical",
            len(witness.first_cycle),
            len(witness.second_cycle),
            0,
            0,
            0,
        )
    cycle_public = CohomologyCyclePublicInstance(public.name, public.target, public.alpha)
    first = validate_cohomology_cycle_witness(cycle_public, witness.first_cycle)
    second = validate_cohomology_cycle_witness(cycle_public, witness.second_cycle)
    shared = len(_witness_vertices(witness.first_cycle) & _witness_vertices(witness.second_cycle))
    if not first.valid:
        return DisjointCohomologyPairValidation(
            False,
            "G19 first cycle rejected: " + first.reason,
            first.cycle_length,
            second.cycle_length,
            first.pairing,
            second.pairing,
            shared,
        )
    if not second.valid:
        return DisjointCohomologyPairValidation(
            False,
            "G19 second cycle rejected: " + second.reason,
            first.cycle_length,
            second.cycle_length,
            first.pairing,
            second.pairing,
            shared,
        )
    if shared:
        return DisjointCohomologyPairValidation(
            False,
            "G19 cycles are not vertex-disjoint",
            first.cycle_length,
            second.cycle_length,
            first.pairing,
            second.pairing,
            shared,
        )
    lengths = sorted((first.cycle_length, second.cycle_length))
    if lengths[0] > public.max_short_length or lengths[1] > public.max_long_length:
        return DisjointCohomologyPairValidation(
            False,
            "G19 cycle pair exceeds public length bounds",
            first.cycle_length,
            second.cycle_length,
            first.pairing,
            second.pairing,
            shared,
        )
    return DisjointCohomologyPairValidation(
        True,
        "accepted",
        first.cycle_length,
        second.cycle_length,
        first.pairing,
        second.pairing,
        0,
    )


def _restricted_parity_bfs(
    root: int,
    vertex_count: int,
    edges: tuple[Edge, ...],
    alpha: tuple[int, ...],
    allowed_edges: frozenset[int],
) -> tuple[tuple[int, ...] | None, int, int]:
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for index in allowed_edges:
        left, right = edges[index]
        adjacency[left].append((right, index))
        adjacency[right].append((left, index))
    for row in adjacency:
        row.sort()
    start = 2 * root
    goal = start + 1
    parent = [-1] * (2 * vertex_count)
    parent_edge = [-1] * (2 * vertex_count)
    parent[start] = start
    queue = deque([start])
    pops = 0
    scans = 0
    while queue:
        state = queue.popleft()
        pops += 1
        if state == goal:
            break
        vertex = state // 2
        parity = state & 1
        for neighbor, edge_index in adjacency[vertex]:
            scans += 1
            next_state = 2 * neighbor + (parity ^ alpha[edge_index])
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
            raise GluingExperimentError("G19 restricted parity-cover reconstruction failed")
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


def _restricted_odd_candidates(
    vertex_count: int,
    edges: tuple[Edge, ...],
    alpha: tuple[int, ...],
    forbidden_vertices: frozenset[int],
) -> _RestrictedSearch:
    allowed_edges = frozenset(
        index
        for index, edge in enumerate(edges)
        if edge[0] not in forbidden_vertices and edge[1] not in forbidden_vertices
    )
    allowed_vertices = tuple(
        vertex for vertex in range(vertex_count) if vertex not in forbidden_vertices
    )
    candidates: set[tuple[int, ...]] = set()
    roots_attempted = 0
    reachable_roots = 0
    pops = 0
    scans = 0
    decomposition_cycles = 0
    decomposition_scans = 0
    for root in allowed_vertices:
        roots_attempted += 1
        path, root_pops, root_scans = _restricted_parity_bfs(
            root, vertex_count, edges, alpha, allowed_edges
        )
        pops += root_pops
        scans += root_scans
        if path is None:
            continue
        reachable_roots += 1
        support = _xor_support(path)
        if not support:
            continue
        tree, _ = _public_spanning_forest(vertex_count, edges, support)
        active = tuple(sorted(support))
        found = False
        for edge_index in active:
            if edge_index in tree.tree_edges:
                continue
            left, right = edges[edge_index]
            tree_path = _tree_path_edges(left, right, tree)
            cycle = tuple(sorted(tree_path + (edge_index,)))
            decomposition_cycles += 1
            decomposition_scans += len(tree_path)
            if _pairing(alpha, cycle) == 1:
                candidates.add(cycle)
                found = True
                break
        if not found:
            raise GluingExperimentError(
                "G19 odd restricted parity support exposed no odd simple constituent"
            )
    return _RestrictedSearch(
        tuple(sorted(candidates, key=lambda cycle: (len(cycle), cycle))),
        roots_attempted,
        reachable_roots,
        pops,
        scans,
        decomposition_cycles,
        decomposition_scans,
    )


def _secret_reference_pair(
    vertex_count: int,
    edges: tuple[Edge, ...],
    alpha: tuple[int, ...],
    seed: bytes,
    max_attempts: int = 64,
) -> tuple[DisjointCohomologyPairWitness, int]:
    for attempt in range(max_attempts):
        tree_seed = hashlib.sha256(
            b"MORPH-KEM G19 reference tree v1\x00"
            + seed
            + attempt.to_bytes(4, "big")
        ).digest()
        tree = _seeded_spanning_tree(vertex_count, edges, tree_seed)
        cycles: list[tuple[int, ...]] = []
        for edge_index in range(len(edges)):
            if edge_index in tree.tree_edges:
                continue
            left, right = edges[edge_index]
            cycle = tuple(sorted(_tree_path_edges(left, right, tree) + (edge_index,)))
            if _pairing(alpha, cycle) == 1:
                cycles.append(cycle)
        cycles.sort(
            key=lambda cycle: (
                hashlib.sha256(
                    b"MORPH-KEM G19 reference cycle order v1\x00"
                    + tree_seed
                    + b"".join(index.to_bytes(4, "big") for index in cycle)
                ).digest(),
                cycle,
            )
        )
        vertex_sets = [_cycle_vertices(edges, cycle) for cycle in cycles]
        for first_index, first in enumerate(cycles):
            for second_index in range(first_index + 1, len(cycles)):
                if vertex_sets[first_index].isdisjoint(vertex_sets[second_index]):
                    return _canonical_index_pair(edges, first, cycles[second_index]), attempt + 1
    raise GluingExperimentError("G19 reference search found no vertex-disjoint odd cycle pair")


def _independent_fundamental_pair(
    vertex_count: int,
    edges: tuple[Edge, ...],
    alpha: tuple[int, ...],
    public: DisjointCohomologyPairPublicInstance,
) -> tuple[int, int, DisjointCohomologyPairWitness | None]:
    tree, components = _public_spanning_forest(vertex_count, edges)
    if components != 1:
        raise GluingExperimentError("G19 independent primal graph is disconnected")
    cycles: list[tuple[int, ...]] = []
    for edge_index in range(len(edges)):
        if edge_index in tree.tree_edges:
            continue
        left, right = edges[edge_index]
        cycle = tuple(sorted(_tree_path_edges(left, right, tree) + (edge_index,)))
        if _pairing(alpha, cycle) == 1:
            cycles.append(cycle)
    cycles.sort(key=lambda cycle: (len(cycle), cycle))
    vertices = [_cycle_vertices(edges, cycle) for cycle in cycles]
    tests = 0
    for first_index, first in enumerate(cycles):
        for second_index in range(first_index + 1, len(cycles)):
            tests += 1
            if not vertices[first_index].isdisjoint(vertices[second_index]):
                continue
            witness = _canonical_index_pair(edges, first, cycles[second_index])
            if validate_disjoint_cohomology_pair_witness(public, witness).valid:
                return len(cycles), tests, witness
    return len(cycles), tests, None


def recover_disjoint_cohomology_pair(
    public: DisjointCohomologyPairPublicInstance,
    *,
    reference: DisjointCohomologyPairReference | None = None,
    successful_flips: int = -1,
) -> DisjointCohomologyPairRecovery:
    edges = _edges(public.target)
    if len(public.alpha) != len(edges):
        raise GluingExperimentError("G19 public cocycle length mismatch")
    (
        _,
        canonical_alpha_mask,
        _,
        _,
        _,
        h1_dimension,
        _,
        _,
    ) = _cochain_metrics(public.target)
    public_alpha_mask = sum(bit << index for index, bit in enumerate(public.alpha))
    if public_alpha_mask != canonical_alpha_mask:
        raise GluingExperimentError("G19 public cocycle is not the canonical measured class")
    incidence = toroidal_hypercover_incidence(
        ToroidalHypercoverPublicInstance(public.name, public.target)
    )
    (
        first_candidates,
        first_pops,
        first_scans,
        _,
        _,
        _,
        _,
    ) = _shortest_public_odd_candidates(incidence.vertices, edges, public.alpha)
    first_histogram = tuple(sorted(Counter(map(len, first_candidates)).items()))

    attempted = 0
    second_calls = 0
    second_roots = 0
    second_reachable = 0
    second_pops = 0
    second_scans = 0
    second_decomposition_cycles = 0
    second_decomposition_scans = 0
    second_candidate_total = 0
    selected: DisjointCohomologyPairWitness | None = None
    selected_validation: DisjointCohomologyPairValidation | None = None
    selected_deleted_vertices = 0
    selected_deleted_edges = 0

    for first_indices in first_candidates:
        if len(first_indices) > public.max_long_length:
            continue
        attempted += 1
        forbidden_vertices = _cycle_vertices(edges, first_indices)
        deleted_edges = sum(
            edge[0] in forbidden_vertices or edge[1] in forbidden_vertices
            for edge in edges
        )
        second_calls += 1
        restricted = _restricted_odd_candidates(
            incidence.vertices, edges, public.alpha, forbidden_vertices
        )
        second_roots += restricted.roots_attempted
        second_reachable += restricted.reachable_roots
        second_pops += restricted.queue_pops
        second_scans += restricted.edge_scans
        second_decomposition_cycles += restricted.decomposition_cycles
        second_decomposition_scans += restricted.decomposition_scans
        second_candidate_total += len(restricted.candidates)
        for second_indices in restricted.candidates:
            witness = _canonical_index_pair(edges, first_indices, second_indices)
            validation = validate_disjoint_cohomology_pair_witness(public, witness)
            if not validation.valid:
                continue
            selected = witness
            selected_validation = validation
            selected_deleted_vertices = len(forbidden_vertices)
            selected_deleted_edges = deleted_edges
            break
        if selected is not None:
            break

    if selected is None or selected_validation is None:
        raise GluingExperimentError("G19 A-046 found no bounded vertex-disjoint odd cycle pair")

    independent_cycles, independent_tests, independent = _independent_fundamental_pair(
        incidence.vertices, edges, public.alpha, public
    )
    independent_accepted = (
        independent is not None
        and validate_disjoint_cohomology_pair_witness(public, independent).valid
    )
    reference_witness = reference.witness if reference is not None else None
    selected_matches = None if reference_witness is None else selected == reference_witness
    lengths = sorted((selected_validation.first_length, selected_validation.second_length))
    reference_lengths = (
        None
        if reference is None
        else sorted((len(reference.witness.first_cycle), len(reference.witness.second_cycle)))
    )

    return DisjointCohomologyPairRecovery(
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
        alpha_weight=sum(public.alpha),
        h1_dimension=h1_dimension,
        max_short_length=public.max_short_length,
        max_long_length=public.max_long_length,
        reference_short_length=None if reference_lengths is None else reference_lengths[0],
        reference_long_length=None if reference_lengths is None else reference_lengths[1],
        first_stage_roots=incidence.vertices,
        first_stage_queue_pops=first_pops,
        first_stage_edge_scans=first_scans,
        first_stage_candidates=len(first_candidates),
        first_stage_length_histogram=first_histogram,
        first_candidates_attempted=attempted,
        second_stage_calls=second_calls,
        second_stage_roots=second_roots,
        second_stage_reachable_roots=second_reachable,
        second_stage_queue_pops=second_pops,
        second_stage_edge_scans=second_scans,
        second_stage_decomposition_cycles=second_decomposition_cycles,
        second_stage_decomposition_scans=second_decomposition_scans,
        second_stage_candidates=second_candidate_total,
        selected_deleted_vertices=selected_deleted_vertices,
        selected_deleted_edges=selected_deleted_edges,
        selected_short_length=lengths[0],
        selected_long_length=lengths[1],
        selected_first_pairing=selected_validation.first_pairing,
        selected_second_pairing=selected_validation.second_pairing,
        selected_shared_vertices=selected_validation.shared_vertices,
        selected_accepted=selected_validation.valid,
        selected_matches_reference=selected_matches,
        independent_odd_fundamental_cycles=independent_cycles,
        independent_pair_tests=independent_tests,
        independent_pair_found=independent is not None,
        independent_pair_accepted=independent_accepted,
    )


def generate_disjoint_cohomology_pair_instance(
    params: DisjointCohomologyPairParameters,
    master_seed: bytes,
    *,
    max_generation_retries: int = 16,
) -> tuple[DisjointCohomologyPairPublicInstance, DisjointCohomologyPairReference]:
    params.validate()
    if len(master_seed) < 16:
        raise GluingExperimentError("G19 master seed must contain at least 128 bits")
    if max_generation_retries < 0 or max_generation_retries > 64:
        raise GluingExperimentError("G19 generation retry cap outside toy bounds")

    for retry in range(max_generation_retries + 1):
        attempt_seed = hashlib.sha256(
            b"MORPH-KEM G19 carrier attempt v1\x00"
            + master_seed
            + params.name.encode("ascii")
            + retry.to_bytes(4, "big")
        ).digest()
        base_seed = hashlib.sha256(b"MORPH-KEM G19 base torus v1\x00" + attempt_seed).digest()
        base_public, _ = generate_surface_instance(
            SurfaceParameters(params.name + "-base", params.rows, params.cols), base_seed
        )
        flip_seed = hashlib.sha256(b"MORPH-KEM G19 flips v1\x00" + attempt_seed).digest()
        target = _flip_surface(base_public.target, params.successful_flips, flip_seed)
        relabel_seed = hashlib.sha256(b"MORPH-KEM G19 relabel v1\x00" + attempt_seed).digest()
        target = _final_relabel(target, relabel_seed)
        edges, alpha_mask, _, _, _, h1_dimension, _, _ = _cochain_metrics(target)
        if h1_dimension != 2:
            raise GluingExperimentError("G19 torus does not expose measured H^1 dimension two")
        alpha = tuple((alpha_mask >> index) & 1 for index in range(len(edges)))
        reference_seed = hashlib.sha256(
            b"MORPH-KEM G19 hidden reference v1\x00" + attempt_seed
        ).digest()
        try:
            reference_witness, reference_tree_attempts = _secret_reference_pair(
                len(target.vertices), edges, alpha, reference_seed
            )
        except GluingExperimentError:
            continue
        lengths = sorted((
            len(reference_witness.first_cycle),
            len(reference_witness.second_cycle),
        ))
        public = DisjointCohomologyPairPublicInstance(
            params.name,
            target,
            alpha,
            lengths[0],
            lengths[1],
        )
        reference = DisjointCohomologyPairReference(
            reference_witness,
            retry,
            reference_tree_attempts,
        )
        validation = validate_disjoint_cohomology_pair_witness(public, reference.witness)
        if not validation.valid:
            raise GluingExperimentError("G19 generated reference pair does not validate")
        return public, reference
    raise GluingExperimentError("G19 exceeded generation retry cap without a disjoint odd pair")
