from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass
import hashlib

from .gluing import GluingExperimentError
from .gluing_cohomology_cycle import (
    _Tree,
    _cochain_metrics,
    _edges,
    _fundamental_odd_cycle,
    _tree_path_edges,
)
from .gluing_irregular_hypercover import (
    _final_relabel,
    _flip_surface,
    _normalization_improving_flip_count,
    _primal_vertex_degree_histogram,
)
from .gluing_surface_hypercover import (
    ToroidalHypercoverPublicInstance,
    toroidal_hypercover_incidence,
)
from .gluing_symplectic_cycle_pair import (
    DualEdge,
    Edge,
    SymplecticCyclePairWitness,
    _cycle_from_indices,
    _degree_histogram,
    _dual_data,
    _pair_from_leftover,
    _tree_cotree_data,
    validate_symplectic_cycle_pair_witness,
)
from .surface import SurfaceParameters, generate_surface_instance


@dataclass(frozen=True, slots=True)
class LengthBoundedPairParameters:
    name: str
    rows: int
    cols: int
    successful_flips: int

    def validate(self) -> None:
        if self.rows < 4 or self.rows > 12 or self.cols < 4 or self.cols > 12:
            raise GluingExperimentError("G18 torus dimensions outside toy bounds")
        triangle_count = 2 * self.rows * self.cols
        if self.successful_flips < 1 or self.successful_flips > triangle_count:
            raise GluingExperimentError("G18 successful-flip target outside toy bounds")


G18_PARAMETER_SETS = {
    "g18-6x6": LengthBoundedPairParameters("g18-6x6", 6, 6, 36),
    "g18-6x9": LengthBoundedPairParameters("g18-6x9", 6, 9, 54),
    "g18-8x9": LengthBoundedPairParameters("g18-8x9", 8, 9, 72),
}


@dataclass(frozen=True, slots=True)
class LengthBoundedPairPublicInstance:
    name: str
    target: object
    max_primal_length: int
    max_dual_length: int


@dataclass(frozen=True, slots=True)
class LengthBoundedPairReference:
    witness: SymplecticCyclePairWitness
    generation_primal_tree_edges: int
    generation_dual_tree_edges: int
    generation_leftovers: int


@dataclass(frozen=True, slots=True)
class LengthBoundedPairValidation:
    valid: bool
    reason: str
    primal_length: int
    dual_length: int
    crossing_count: int


@dataclass(frozen=True, slots=True)
class LengthBoundedPairRecovery:
    vertices: int
    edges: int
    triangles: int
    euler_characteristic: int
    min_triangles_per_edge: int
    max_triangles_per_edge: int
    successful_flips: int
    primal_vertex_degree_histogram: tuple[tuple[int, int], ...]
    dual_vertex_degree_histogram: tuple[tuple[int, int], ...]
    normalization_improving_flips: int
    max_primal_length: int
    max_dual_length: int
    reference_primal_length: int | None
    reference_dual_length: int | None
    alpha_weight: int
    h1_dimension: int
    parity_cover_vertices: int
    parity_cover_directed_arcs: int
    cover_roots_attempted: int
    cover_queue_pops: int
    cover_edge_scans: int
    cover_walk_length_min: int
    cover_support_edges_min: int
    decomposition_cycles_tested: int
    decomposition_path_scans: int
    distinct_primal_candidates: int
    primal_candidates_within_bound: int
    dual_connector_calls: int
    dual_connector_queue_pops: int
    dual_connector_edge_scans: int
    selected_primal_length: int
    selected_dual_length: int
    selected_crossing_count: int
    selected_accepted: bool
    selected_matches_reference: bool | None
    canonical_treecotree_leftovers: int
    canonical_treecotree_primal_length: int
    canonical_treecotree_dual_length: int
    canonical_treecotree_crossing_count: int
    canonical_treecotree_within_bounds: bool
    canonical_treecotree_accepted: bool
    canonical_treecotree_matches_reference: bool | None


@dataclass(frozen=True, slots=True)
class _BfsResult:
    edge_indices: tuple[int, ...]
    queue_pops: int
    edge_scans: int


def _adjacency(vertex_count: int, edges: tuple[tuple[int, int], ...]) -> list[list[tuple[int, int]]]:
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for index, (left, right) in enumerate(edges):
        adjacency[left].append((right, index))
        adjacency[right].append((left, index))
    for row in adjacency:
        row.sort()
    return adjacency


def _parity_cover_bfs(
    root: int,
    edges: tuple[Edge, ...],
    alpha: tuple[int, ...],
    adjacency: list[list[tuple[int, int]]],
) -> _BfsResult:
    vertex_count = len(adjacency)
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
        raise GluingExperimentError("G18 parity cover failed to expose odd closed walk")
    path: list[int] = []
    state = goal
    while state != start:
        edge_index = parent_edge[state]
        if edge_index < 0:
            raise GluingExperimentError("G18 parity-cover reconstruction failed")
        path.append(edge_index)
        state = parent[state]
    path.reverse()
    return _BfsResult(tuple(path), pops, scans)


def _xor_support(path: tuple[int, ...]) -> frozenset[int]:
    support: set[int] = set()
    for edge_index in path:
        if edge_index in support:
            support.remove(edge_index)
        else:
            support.add(edge_index)
    return frozenset(support)


def _shortest_public_odd_candidates(
    vertex_count: int,
    edges: tuple[Edge, ...],
    alpha: tuple[int, ...],
) -> tuple[
    tuple[tuple[int, ...], ...], int, int, int, int, int, int
]:
    adjacency = _adjacency(vertex_count, edges)
    candidates: set[tuple[int, ...]] = set()
    total_pops = 0
    total_scans = 0
    min_walk = 1 << 30
    min_support = 1 << 30
    decomposition_tested = 0
    decomposition_scans = 0
    for root in range(vertex_count):
        result = _parity_cover_bfs(root, edges, alpha, adjacency)
        total_pops += result.queue_pops
        total_scans += result.edge_scans
        min_walk = min(min_walk, len(result.edge_indices))
        support = _xor_support(result.edge_indices)
        if not support:
            raise GluingExperimentError("G18 odd cover walk collapsed to empty support")
        min_support = min(min_support, len(support))
        cycle, tested, scans, _, _ = _fundamental_odd_cycle(
            vertex_count, edges, alpha, allowed_edges=support
        )
        decomposition_tested += tested
        decomposition_scans += scans
        candidates.add(tuple(sorted(cycle)))
    ordered = tuple(sorted(candidates, key=lambda cycle: (len(cycle), cycle)))
    if not ordered:
        raise GluingExperimentError("G18 public parity-cover attack produced no simple odd cycle")
    return (
        ordered,
        total_pops,
        total_scans,
        min_walk,
        min_support,
        decomposition_tested,
        decomposition_scans,
    )


def _constrained_dual_bfs(
    start: int,
    goal: int,
    dual_edges: tuple[DualEdge, ...],
    forbidden_indices: frozenset[int],
) -> _BfsResult | None:
    vertex_count = 1 + max(max(edge) for edge in dual_edges)
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for index, (left, right) in enumerate(dual_edges):
        if index in forbidden_indices:
            continue
        adjacency[left].append((right, index))
        adjacency[right].append((left, index))
    for row in adjacency:
        row.sort()
    parent = [-1] * vertex_count
    parent_edge = [-1] * vertex_count
    parent[start] = start
    queue = deque([start])
    pops = 0
    scans = 0
    while queue:
        current = queue.popleft()
        pops += 1
        if current == goal:
            break
        for neighbor, edge_index in adjacency[current]:
            scans += 1
            if parent[neighbor] != -1:
                continue
            parent[neighbor] = current
            parent_edge[neighbor] = edge_index
            queue.append(neighbor)
    if parent[goal] == -1:
        return None
    path: list[int] = []
    current = goal
    while current != start:
        edge_index = parent_edge[current]
        if edge_index < 0:
            raise GluingExperimentError("G18 dual connector reconstruction failed")
        path.append(edge_index)
        current = parent[current]
    path.reverse()
    return _BfsResult(tuple(path), pops, scans)


def validate_length_bounded_pair_witness(
    public: LengthBoundedPairPublicInstance,
    witness: SymplecticCyclePairWitness,
) -> LengthBoundedPairValidation:
    base = validate_symplectic_cycle_pair_witness(
        type("_P", (), {"name": public.name, "target": public.target})(), witness
    )
    if not base.valid:
        return LengthBoundedPairValidation(
            False, base.reason, base.primal_cycle_length, base.dual_cycle_length, base.crossing_count
        )
    if base.crossing_count != 1:
        return LengthBoundedPairValidation(
            False,
            "G18 witness does not have exactly one geometric crossing",
            base.primal_cycle_length,
            base.dual_cycle_length,
            base.crossing_count,
        )
    if base.primal_cycle_length > public.max_primal_length:
        return LengthBoundedPairValidation(
            False,
            "G18 primal cycle exceeds public length bound",
            base.primal_cycle_length,
            base.dual_cycle_length,
            base.crossing_count,
        )
    if base.dual_cycle_length > public.max_dual_length:
        return LengthBoundedPairValidation(
            False,
            "G18 dual cycle exceeds public length bound",
            base.primal_cycle_length,
            base.dual_cycle_length,
            base.crossing_count,
        )
    return LengthBoundedPairValidation(
        True, "accepted", base.primal_cycle_length, base.dual_cycle_length, base.crossing_count
    )


def _seeded_spanning_tree(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
    seed: bytes,
    *,
    allowed_edges: frozenset[int] | None = None,
) -> _Tree:
    adjacency = _adjacency(vertex_count, edges)
    root = int.from_bytes(hashlib.sha256(b"root\x00" + seed).digest()[:8], "big") % vertex_count
    parent = [-1] * vertex_count
    parent_edge = [-1] * vertex_count
    depth = [0] * vertex_count
    tree_edges: set[int] = set()
    parent[root] = root
    queue = deque([root])
    while queue:
        current = queue.popleft()
        choices = [
            item
            for item in adjacency[current]
            if allowed_edges is None or item[1] in allowed_edges
        ]
        choices.sort(
            key=lambda item: (
                hashlib.sha256(
                    b"edge-order\x00" + seed + item[1].to_bytes(4, "big") + item[0].to_bytes(4, "big")
                ).digest(),
                item,
            )
        )
        for neighbor, edge_index in choices:
            if parent[neighbor] != -1:
                continue
            parent[neighbor] = current
            parent_edge[neighbor] = edge_index
            depth[neighbor] = depth[current] + 1
            tree_edges.add(edge_index)
            queue.append(neighbor)
    if any(value == -1 for value in parent):
        raise GluingExperimentError("G18 seeded spanning tree failed to span")
    return _Tree(tuple(parent), tuple(parent_edge), tuple(depth), frozenset(tree_edges))


def _generation_reference(
    target: object,
    seed: bytes,
) -> tuple[SymplecticCyclePairWitness, int, int, int]:
    primal_edges = _edges(target)
    dual = _dual_data(target, primal_edges)
    primal_seed = hashlib.sha256(b"MORPH-KEM G18 reference primal tree v1\x00" + seed).digest()
    primal_tree = _seeded_spanning_tree(len(target.vertices), primal_edges, primal_seed)
    allowed_dual = frozenset(
        index for index in range(len(primal_edges)) if index not in primal_tree.tree_edges
    )
    dual_seed = hashlib.sha256(b"MORPH-KEM G18 reference dual tree v1\x00" + seed).digest()
    dual_tree = _seeded_spanning_tree(
        len(dual.triangles), dual.dual_edges, dual_seed, allowed_edges=allowed_dual
    )
    leftovers = tuple(
        index
        for index in range(len(primal_edges))
        if index not in primal_tree.tree_edges and index not in dual_tree.tree_edges
    )
    if len(leftovers) != 2:
        raise GluingExperimentError("G18 seeded tree-cotree expected exactly two leftovers")
    choice_digest = hashlib.sha256(b"MORPH-KEM G18 reference leftover v1\x00" + seed).digest()
    chosen = leftovers[int.from_bytes(choice_digest[:8], "big") & 1]
    witness, _, _, crossings = _pair_from_leftover(
        chosen, primal_edges, dual.dual_edges, primal_tree, dual_tree
    )
    if crossings != 1:
        raise GluingExperimentError("G18 seeded reference pair is not exact-one-crossing")
    return witness, len(primal_tree.tree_edges), len(dual_tree.tree_edges), len(leftovers)


def recover_length_bounded_pair(
    public: LengthBoundedPairPublicInstance,
    *,
    reference: LengthBoundedPairReference | None = None,
    successful_flips: int = -1,
) -> LengthBoundedPairRecovery:
    primal_edges, alpha_mask, _, _, _, h1_dimension, _, _ = _cochain_metrics(public.target)
    alpha = tuple((alpha_mask >> index) & 1 for index in range(len(primal_edges)))
    dual = _dual_data(public.target, primal_edges)
    incidence = toroidal_hypercover_incidence(
        ToroidalHypercoverPublicInstance(public.name, public.target)
    )
    (
        candidates,
        cover_pops,
        cover_scans,
        min_walk,
        min_support,
        decomposition_tested,
        decomposition_scans,
    ) = _shortest_public_odd_candidates(incidence.vertices, primal_edges, alpha)

    within_bound = [cycle for cycle in candidates if len(cycle) <= public.max_primal_length]
    connector_calls = 0
    connector_pops = 0
    connector_scans = 0
    selected: SymplecticCyclePairWitness | None = None
    selected_validation: LengthBoundedPairValidation | None = None
    for primal_cycle in within_bound:
        forbidden = frozenset(primal_cycle)
        for anchor in primal_cycle:
            connector_calls += 1
            left, right = dual.dual_edges[anchor]
            result = _constrained_dual_bfs(
                left, right, dual.dual_edges, forbidden
            )
            if result is None:
                continue
            connector_pops += result.queue_pops
            connector_scans += result.edge_scans
            dual_cycle = tuple(sorted(result.edge_indices + (anchor,)))
            witness = SymplecticCyclePairWitness(
                _cycle_from_indices(primal_edges, primal_cycle),
                _cycle_from_indices(dual.dual_edges, dual_cycle),
            )
            validation = validate_length_bounded_pair_witness(public, witness)
            if not validation.valid:
                continue
            if selected is None or (
                len(witness.primal_cycle), len(witness.dual_cycle), witness.primal_cycle, witness.dual_cycle
            ) < (
                len(selected.primal_cycle), len(selected.dual_cycle), selected.primal_cycle, selected.dual_cycle
            ):
                selected = witness
                selected_validation = validation
        if selected is not None:
            break
    if selected is None or selected_validation is None:
        raise GluingExperimentError("G18 public shortest-cycle/connector attack found no bounded witness")

    selected_matches = None if reference is None else selected == reference.witness

    canonical_primal_tree, canonical_dual_tree, leftovers = _tree_cotree_data(
        incidence.vertices, primal_edges, incidence.triangles, dual.dual_edges
    )
    if len(leftovers) != 2:
        raise GluingExperimentError("G18 canonical tree-cotree expected exactly two leftovers")
    canonical, _, _, canonical_crossings = _pair_from_leftover(
        leftovers[0], primal_edges, dual.dual_edges, canonical_primal_tree, canonical_dual_tree
    )
    canonical_validation = validate_length_bounded_pair_witness(public, canonical)
    canonical_within = (
        len(canonical.primal_cycle) <= public.max_primal_length
        and len(canonical.dual_cycle) <= public.max_dual_length
    )
    canonical_matches = None if reference is None else canonical == reference.witness

    return LengthBoundedPairRecovery(
        vertices=incidence.vertices,
        edges=incidence.edges,
        triangles=incidence.triangles,
        euler_characteristic=incidence.euler_characteristic,
        min_triangles_per_edge=incidence.min_triangles_per_edge,
        max_triangles_per_edge=incidence.max_triangles_per_edge,
        successful_flips=successful_flips,
        primal_vertex_degree_histogram=_primal_vertex_degree_histogram(public.target),
        dual_vertex_degree_histogram=_degree_histogram(incidence.triangles, dual.dual_edges),
        normalization_improving_flips=_normalization_improving_flip_count(public.target),
        max_primal_length=public.max_primal_length,
        max_dual_length=public.max_dual_length,
        reference_primal_length=None if reference is None else len(reference.witness.primal_cycle),
        reference_dual_length=None if reference is None else len(reference.witness.dual_cycle),
        alpha_weight=sum(alpha),
        h1_dimension=h1_dimension,
        parity_cover_vertices=2 * incidence.vertices,
        parity_cover_directed_arcs=4 * incidence.edges,
        cover_roots_attempted=incidence.vertices,
        cover_queue_pops=cover_pops,
        cover_edge_scans=cover_scans,
        cover_walk_length_min=min_walk,
        cover_support_edges_min=min_support,
        decomposition_cycles_tested=decomposition_tested,
        decomposition_path_scans=decomposition_scans,
        distinct_primal_candidates=len(candidates),
        primal_candidates_within_bound=len(within_bound),
        dual_connector_calls=connector_calls,
        dual_connector_queue_pops=connector_pops,
        dual_connector_edge_scans=connector_scans,
        selected_primal_length=selected_validation.primal_length,
        selected_dual_length=selected_validation.dual_length,
        selected_crossing_count=selected_validation.crossing_count,
        selected_accepted=selected_validation.valid,
        selected_matches_reference=selected_matches,
        canonical_treecotree_leftovers=len(leftovers),
        canonical_treecotree_primal_length=len(canonical.primal_cycle),
        canonical_treecotree_dual_length=len(canonical.dual_cycle),
        canonical_treecotree_crossing_count=canonical_crossings,
        canonical_treecotree_within_bounds=canonical_within,
        canonical_treecotree_accepted=canonical_validation.valid,
        canonical_treecotree_matches_reference=canonical_matches,
    )


def generate_length_bounded_pair_instance(
    params: LengthBoundedPairParameters,
    master_seed: bytes,
) -> tuple[LengthBoundedPairPublicInstance, LengthBoundedPairReference]:
    params.validate()
    if len(master_seed) < 16:
        raise GluingExperimentError("G18 master seed must contain at least 128 bits")

    base_seed = hashlib.sha256(
        b"MORPH-KEM G18 base torus v1\x00" + master_seed + params.name.encode("ascii")
    ).digest()
    base_public, _ = generate_surface_instance(
        SurfaceParameters(params.name + "-base", params.rows, params.cols), base_seed
    )
    flip_seed = hashlib.sha256(
        b"MORPH-KEM G18 flips v1\x00" + master_seed + params.name.encode("ascii")
    ).digest()
    target = _flip_surface(base_public.target, params.successful_flips, flip_seed)
    relabel_seed = hashlib.sha256(
        b"MORPH-KEM G18 relabel v1\x00" + master_seed + params.name.encode("ascii")
    ).digest()
    target = _final_relabel(target, relabel_seed)

    reference_seed = hashlib.sha256(
        b"MORPH-KEM G18 hidden reference v1\x00" + master_seed + params.name.encode("ascii")
    ).digest()
    witness, primal_tree_edges, dual_tree_edges, leftovers = _generation_reference(
        target, reference_seed
    )
    public = LengthBoundedPairPublicInstance(
        params.name,
        target,
        len(witness.primal_cycle),
        len(witness.dual_cycle),
    )
    reference = LengthBoundedPairReference(
        witness, primal_tree_edges, dual_tree_edges, leftovers
    )
    validation = validate_length_bounded_pair_witness(public, reference.witness)
    if not validation.valid:
        raise GluingExperimentError("G18 generated bounded reference does not validate")
    return public, reference
