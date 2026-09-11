from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
from itertools import combinations

from .complex import SimplicialComplex
from .gluing import GluingExperimentError
from .gluing_cohomology_cycle import (
    _edges,
    _public_spanning_forest,
    _rref,
    _tree_path_edges,
    _triangles,
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
from .surface import SurfaceParameters, generate_surface_instance


Edge = tuple[int, int]
DualEdge = tuple[int, int]
Cycle = tuple[tuple[int, int], ...]


@dataclass(frozen=True, slots=True)
class SymplecticCyclePairParameters:
    name: str
    rows: int
    cols: int
    successful_flips: int

    def validate(self) -> None:
        if self.rows < 4 or self.rows > 12 or self.cols < 4 or self.cols > 12:
            raise GluingExperimentError("G17 torus dimensions outside toy bounds")
        triangle_count = 2 * self.rows * self.cols
        if self.successful_flips < 1 or self.successful_flips > triangle_count:
            raise GluingExperimentError("G17 successful-flip target outside toy bounds")


G17_PARAMETER_SETS = {
    "g17-6x6": SymplecticCyclePairParameters("g17-6x6", 6, 6, 36),
    "g17-6x9": SymplecticCyclePairParameters("g17-6x9", 6, 9, 54),
    "g17-8x9": SymplecticCyclePairParameters("g17-8x9", 8, 9, 72),
}


@dataclass(frozen=True, slots=True)
class SymplecticCyclePairPublicInstance:
    name: str
    target: SimplicialComplex


@dataclass(frozen=True, slots=True)
class SymplecticCyclePairWitness:
    primal_cycle: Cycle
    dual_cycle: Cycle


@dataclass(frozen=True, slots=True)
class SymplecticCyclePairReference:
    witness: SymplecticCyclePairWitness


@dataclass(frozen=True, slots=True)
class SymplecticCyclePairValidation:
    valid: bool
    reason: str
    primal_cycle_length: int
    dual_cycle_length: int
    crossing_count: int
    crossing_parity: int


@dataclass(frozen=True, slots=True)
class SymplecticCyclePairRecovery:
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
    primal_tree_edges: int
    dual_cotree_edges: int
    forbidden_dual_edges: int
    leftover_edges: int
    treecotree_primal_path_scans: int
    treecotree_dual_path_scans: int
    treecotree_primal_cycle_length: int
    treecotree_dual_cycle_length: int
    treecotree_crossing_count: int
    treecotree_crossing_parity: int
    treecotree_accepted: bool
    treecotree_matches_reference: bool | None
    full_primal_cycles: int
    full_dual_cycles: int
    full_primal_cycle_length_histogram: tuple[tuple[int, int], ...]
    full_dual_cycle_length_histogram: tuple[tuple[int, int], ...]
    full_primal_path_scans: int
    full_dual_path_scans: int
    crossing_matrix_rows: int
    crossing_matrix_cols: int
    crossing_matrix_weight: int
    crossing_matrix_rank: int
    crossing_matrix_row_xors: int
    full_basis_pairs_tested: int
    full_basis_primal_cycle_length: int
    full_basis_dual_cycle_length: int
    full_basis_crossing_count: int
    full_basis_accepted: bool


@dataclass(frozen=True, slots=True)
class _DualData:
    triangles: tuple[tuple[int, int, int], ...]
    dual_edges: tuple[DualEdge, ...]


@dataclass(frozen=True, slots=True)
class _BasisData:
    cycles: tuple[tuple[int, ...], ...]
    tree_edges: int
    path_scans: int


def _dual_data(target: SimplicialComplex, primal_edges: tuple[Edge, ...]) -> _DualData:
    triangles = _triangles(target)
    triangle_index = {triangle: index for index, triangle in enumerate(triangles)}
    owners: dict[Edge, list[int]] = {edge: [] for edge in primal_edges}
    for triangle in triangles:
        index = triangle_index[triangle]
        for pair in combinations(triangle, 2):
            edge = tuple(sorted(pair))
            if edge not in owners:
                raise GluingExperimentError("G17 triangle exposes a non-public primal edge")
            owners[edge].append(index)

    dual_edges: list[DualEdge] = []
    for edge in primal_edges:
        edge_owners = sorted(owners[edge])
        if len(edge_owners) != 2 or edge_owners[0] == edge_owners[1]:
            raise GluingExperimentError("G17 carrier is not a closed two-manifold")
        dual_edges.append((edge_owners[0], edge_owners[1]))
    if len(set(dual_edges)) != len(dual_edges):
        raise GluingExperimentError("G17 dual graph contains parallel edges")
    return _DualData(triangles, tuple(dual_edges))


def _degree_histogram(vertex_count: int, edges: tuple[tuple[int, int], ...]) -> tuple[tuple[int, int], ...]:
    degree = [0] * vertex_count
    for left, right in edges:
        degree[left] += 1
        degree[right] += 1
    return tuple(sorted(Counter(degree).items()))


def _cycle_from_indices(edges: tuple[tuple[int, int], ...], indices: tuple[int, ...]) -> Cycle:
    return tuple(sorted(edges[index] for index in indices))


def _cycle_indices(
    witness: Cycle,
    public_edges: tuple[tuple[int, int], ...],
) -> tuple[int, ...] | None:
    edge_to_index = {edge: index for index, edge in enumerate(public_edges)}
    if (
        len(witness) < 3
        or witness != tuple(sorted(witness))
        or len(set(witness)) != len(witness)
    ):
        return None
    indices: list[int] = []
    for edge in witness:
        if edge[0] >= edge[1] or edge not in edge_to_index:
            return None
        indices.append(edge_to_index[edge])
    return tuple(indices)


def _is_one_simple_cycle(
    witness: Cycle,
    public_edges: tuple[tuple[int, int], ...],
) -> bool:
    if _cycle_indices(witness, public_edges) is None:
        return False
    degree: Counter[int] = Counter()
    adjacency: dict[int, set[int]] = defaultdict(set)
    for left, right in witness:
        degree[left] += 1
        degree[right] += 1
        adjacency[left].add(right)
        adjacency[right].add(left)
    if not degree or any(value != 2 for value in degree.values()):
        return False
    start = min(degree)
    seen = {start}
    stack = [start]
    while stack:
        current = stack.pop()
        for neighbor in adjacency[current]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return len(seen) == len(degree)


def validate_symplectic_cycle_pair_witness(
    public: SymplecticCyclePairPublicInstance,
    witness: SymplecticCyclePairWitness,
) -> SymplecticCyclePairValidation:
    primal_edges = _edges(public.target)
    dual = _dual_data(public.target, primal_edges)
    if not _is_one_simple_cycle(witness.primal_cycle, primal_edges):
        return SymplecticCyclePairValidation(
            False, "G17 primal witness is not one public simple cycle", len(witness.primal_cycle), len(witness.dual_cycle), 0, 0
        )
    if not _is_one_simple_cycle(witness.dual_cycle, dual.dual_edges):
        return SymplecticCyclePairValidation(
            False, "G17 dual witness is not one public simple cycle", len(witness.primal_cycle), len(witness.dual_cycle), 0, 0
        )

    primal_indices = set(_cycle_indices(witness.primal_cycle, primal_edges) or ())
    dual_indices = set(_cycle_indices(witness.dual_cycle, dual.dual_edges) or ())
    crossing_count = len(primal_indices & dual_indices)
    parity = crossing_count & 1
    if parity != 1:
        return SymplecticCyclePairValidation(
            False,
            "G17 primal-dual intersection parity is even",
            len(witness.primal_cycle),
            len(witness.dual_cycle),
            crossing_count,
            parity,
        )
    return SymplecticCyclePairValidation(
        True,
        "accepted",
        len(witness.primal_cycle),
        len(witness.dual_cycle),
        crossing_count,
        parity,
    )


def _tree_cotree_data(
    vertex_count: int,
    primal_edges: tuple[Edge, ...],
    triangle_count: int,
    dual_edges: tuple[DualEdge, ...],
) -> tuple[object, object, tuple[int, ...]]:
    primal_tree, primal_components = _public_spanning_forest(vertex_count, primal_edges)
    if primal_components != 1 or len(primal_tree.tree_edges) != vertex_count - 1:
        raise GluingExperimentError("G17 primal spanning tree is incomplete")

    allowed_dual = frozenset(
        index for index in range(len(primal_edges)) if index not in primal_tree.tree_edges
    )
    dual_tree, dual_components = _public_spanning_forest(
        triangle_count, dual_edges, allowed_dual
    )
    if dual_components != 1 or len(dual_tree.tree_edges) != triangle_count - 1:
        raise GluingExperimentError("G17 dual cotree did not span after forbidding primal-tree crossings")

    leftovers = tuple(
        index
        for index in range(len(primal_edges))
        if index not in primal_tree.tree_edges and index not in dual_tree.tree_edges
    )
    return primal_tree, dual_tree, leftovers


def _pair_from_leftover(
    leftover: int,
    primal_edges: tuple[Edge, ...],
    dual_edges: tuple[DualEdge, ...],
    primal_tree: object,
    dual_tree: object,
) -> tuple[SymplecticCyclePairWitness, int, int, int]:
    primal_left, primal_right = primal_edges[leftover]
    primal_path = _tree_path_edges(primal_left, primal_right, primal_tree)
    primal_indices = tuple(sorted(primal_path + (leftover,)))

    dual_left, dual_right = dual_edges[leftover]
    dual_path = _tree_path_edges(dual_left, dual_right, dual_tree)
    dual_indices = tuple(sorted(dual_path + (leftover,)))

    witness = SymplecticCyclePairWitness(
        _cycle_from_indices(primal_edges, primal_indices),
        _cycle_from_indices(dual_edges, dual_indices),
    )
    crossing_count = len(set(primal_indices) & set(dual_indices))
    return witness, len(primal_path), len(dual_path), crossing_count


def _fundamental_basis(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
) -> _BasisData:
    tree, components = _public_spanning_forest(vertex_count, edges)
    if components != 1:
        raise GluingExperimentError("G17 basis graph is disconnected")
    cycles: list[tuple[int, ...]] = []
    scans = 0
    for edge_index in range(len(edges)):
        if edge_index in tree.tree_edges:
            continue
        left, right = edges[edge_index]
        path = _tree_path_edges(left, right, tree)
        scans += len(path)
        cycles.append(tuple(sorted(path + (edge_index,))))
    return _BasisData(tuple(cycles), len(tree.tree_edges), scans)


def _length_histogram(cycles: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(len(cycle) for cycle in cycles).items()))


def _full_basis_cross_check(
    primal_edges: tuple[Edge, ...],
    dual_edges: tuple[DualEdge, ...],
    vertex_count: int,
    triangle_count: int,
) -> tuple[_BasisData, _BasisData, int, int, int, int, SymplecticCyclePairWitness, int]:
    primal_basis = _fundamental_basis(vertex_count, primal_edges)
    dual_basis = _fundamental_basis(triangle_count, dual_edges)

    rows: list[int] = []
    weight = 0
    tested = 0
    selected: tuple[int, int, int] | None = None
    dual_sets = tuple(set(cycle) for cycle in dual_basis.cycles)
    for primal_index, primal_cycle in enumerate(primal_basis.cycles):
        primal_set = set(primal_cycle)
        row = 0
        for dual_index, dual_set in enumerate(dual_sets):
            crossing_count = len(primal_set & dual_set)
            parity = crossing_count & 1
            if parity:
                row |= 1 << dual_index
                weight += 1
            tested += 1
            if selected is None and parity:
                selected = (primal_index, dual_index, crossing_count)
        rows.append(row)

    matrix_rref = _rref(rows, len(dual_basis.cycles))
    if selected is None:
        raise GluingExperimentError("G17 full crossing matrix is identically zero")
    primal_index, dual_index, crossing_count = selected
    witness = SymplecticCyclePairWitness(
        _cycle_from_indices(primal_edges, primal_basis.cycles[primal_index]),
        _cycle_from_indices(dual_edges, dual_basis.cycles[dual_index]),
    )

    # Recompute the row-major work to the first odd entry rather than the full matrix size.
    pairs_to_first = 0
    found = False
    for primal_cycle in primal_basis.cycles:
        primal_set = set(primal_cycle)
        for dual_cycle in dual_sets:
            pairs_to_first += 1
            if len(primal_set & dual_cycle) & 1:
                found = True
                break
        if found:
            break
    return (
        primal_basis,
        dual_basis,
        weight,
        matrix_rref.rank,
        matrix_rref.row_xors,
        pairs_to_first,
        witness,
        crossing_count,
    )


def recover_symplectic_cycle_pair(
    public: SymplecticCyclePairPublicInstance,
    *,
    reference: SymplecticCyclePairReference | None = None,
    successful_flips: int = -1,
) -> SymplecticCyclePairRecovery:
    primal_edges = _edges(public.target)
    dual = _dual_data(public.target, primal_edges)
    incidence = toroidal_hypercover_incidence(
        ToroidalHypercoverPublicInstance(public.name, public.target)
    )
    primal_tree, dual_tree, leftovers = _tree_cotree_data(
        incidence.vertices,
        primal_edges,
        incidence.triangles,
        dual.dual_edges,
    )
    if len(leftovers) != 2:
        raise GluingExperimentError(
            f"G17 torus tree-cotree decomposition expected two leftovers, got {len(leftovers)}"
        )

    primary, primal_scans, dual_scans, crossing_count = _pair_from_leftover(
        leftovers[0], primal_edges, dual.dual_edges, primal_tree, dual_tree
    )
    primary_validation = validate_symplectic_cycle_pair_witness(public, primary)
    if not primary_validation.valid or crossing_count != 1:
        raise GluingExperimentError("G17 tree-cotree attack failed exact one-crossing verifier gate")

    matches_reference = None
    if reference is not None:
        matches_reference = primary == reference.witness

    (
        primal_basis,
        dual_basis,
        matrix_weight,
        matrix_rank,
        matrix_row_xors,
        pairs_to_first,
        basis_witness,
        basis_crossings,
    ) = _full_basis_cross_check(
        primal_edges, dual.dual_edges, incidence.vertices, incidence.triangles
    )
    basis_validation = validate_symplectic_cycle_pair_witness(public, basis_witness)
    if not basis_validation.valid:
        raise GluingExperimentError("G17 full-basis cross-check failed exact verifier")

    return SymplecticCyclePairRecovery(
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
        primal_tree_edges=len(primal_tree.tree_edges),
        dual_cotree_edges=len(dual_tree.tree_edges),
        forbidden_dual_edges=len(primal_tree.tree_edges),
        leftover_edges=len(leftovers),
        treecotree_primal_path_scans=primal_scans,
        treecotree_dual_path_scans=dual_scans,
        treecotree_primal_cycle_length=len(primary.primal_cycle),
        treecotree_dual_cycle_length=len(primary.dual_cycle),
        treecotree_crossing_count=primary_validation.crossing_count,
        treecotree_crossing_parity=primary_validation.crossing_parity,
        treecotree_accepted=primary_validation.valid,
        treecotree_matches_reference=matches_reference,
        full_primal_cycles=len(primal_basis.cycles),
        full_dual_cycles=len(dual_basis.cycles),
        full_primal_cycle_length_histogram=_length_histogram(primal_basis.cycles),
        full_dual_cycle_length_histogram=_length_histogram(dual_basis.cycles),
        full_primal_path_scans=primal_basis.path_scans,
        full_dual_path_scans=dual_basis.path_scans,
        crossing_matrix_rows=len(primal_basis.cycles),
        crossing_matrix_cols=len(dual_basis.cycles),
        crossing_matrix_weight=matrix_weight,
        crossing_matrix_rank=matrix_rank,
        crossing_matrix_row_xors=matrix_row_xors,
        full_basis_pairs_tested=pairs_to_first,
        full_basis_primal_cycle_length=len(basis_witness.primal_cycle),
        full_basis_dual_cycle_length=len(basis_witness.dual_cycle),
        full_basis_crossing_count=basis_crossings,
        full_basis_accepted=basis_validation.valid,
    )


def generate_symplectic_cycle_pair_instance(
    params: SymplecticCyclePairParameters,
    master_seed: bytes,
) -> tuple[SymplecticCyclePairPublicInstance, SymplecticCyclePairReference]:
    params.validate()
    if len(master_seed) < 16:
        raise GluingExperimentError("G17 master seed must contain at least 128 bits")

    base_seed = hashlib.sha256(
        b"MORPH-KEM G17 base torus v1\x00" + master_seed + params.name.encode("ascii")
    ).digest()
    base_public, _ = generate_surface_instance(
        SurfaceParameters(params.name + "-base", params.rows, params.cols), base_seed
    )
    flip_seed = hashlib.sha256(
        b"MORPH-KEM G17 flips v1\x00" + master_seed + params.name.encode("ascii")
    ).digest()
    target = _flip_surface(base_public.target, params.successful_flips, flip_seed)
    relabel_seed = hashlib.sha256(
        b"MORPH-KEM G17 relabel v1\x00" + master_seed + params.name.encode("ascii")
    ).digest()
    target = _final_relabel(target, relabel_seed)
    public = SymplecticCyclePairPublicInstance(params.name, target)

    primal_edges = _edges(target)
    dual = _dual_data(target, primal_edges)
    primal_tree, dual_tree, leftovers = _tree_cotree_data(
        len(target.vertices), primal_edges, len(dual.triangles), dual.dual_edges
    )
    if len(leftovers) != 2:
        raise GluingExperimentError("G17 reference construction expected exactly two leftovers")
    reference_witness, _, _, crossings = _pair_from_leftover(
        leftovers[1], primal_edges, dual.dual_edges, primal_tree, dual_tree
    )
    reference = SymplecticCyclePairReference(reference_witness)
    validation = validate_symplectic_cycle_pair_witness(public, reference.witness)
    if not validation.valid or crossings != 1:
        raise GluingExperimentError("G17 generated reference pair does not validate")
    return public, reference
