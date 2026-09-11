from __future__ import annotations

from dataclasses import dataclass
import hashlib

from .complex import SimplicialComplex
from .gluing import GluingExperimentError
from .gluing_cohomology_cycle import _edges, _rref
from .gluing_genus2_multicurve import (
    GenusTwoMulticurveParameters,
    _cohomology_basis,
    _connected_sum_tori,
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
    Cycle,
    _cycle_indices,
    _degree_histogram,
    _dual_data,
    _fundamental_basis,
    _is_one_simple_cycle,
    _pair_from_leftover,
    _tree_cotree_data,
)


@dataclass(frozen=True, slots=True)
class GenusTwoCrossingBasisParameters:
    name: str
    rows: int
    cols: int
    successful_flips: int

    def validate(self) -> None:
        if self.rows < 4 or self.rows > 12 or self.cols < 4 or self.cols > 12:
            raise GluingExperimentError("G21 torus dimensions outside toy bounds")
        triangle_count = 4 * self.rows * self.cols - 2
        if self.successful_flips < 1 or self.successful_flips > 8 * triangle_count:
            raise GluingExperimentError("G21 successful-flip target outside toy bounds")


G21_PARAMETER_SETS = {
    "g21-4x4": GenusTwoCrossingBasisParameters("g21-4x4", 4, 4, 124),
    "g21-6x6": GenusTwoCrossingBasisParameters("g21-6x6", 6, 6, 284),
    "g21-6x9": GenusTwoCrossingBasisParameters("g21-6x9", 6, 9, 428),
}


@dataclass(frozen=True, slots=True)
class GenusTwoCrossingBasisPublicInstance:
    name: str
    target: SimplicialComplex


@dataclass(frozen=True, slots=True)
class GenusTwoCrossingBasisWitness:
    primal_cycles: tuple[Cycle, ...]
    dual_cycles: tuple[Cycle, ...]


@dataclass(frozen=True, slots=True)
class GenusTwoCrossingBasisValidation:
    valid: bool
    reason: str
    crossing_matrix: tuple[tuple[int, ...], ...]
    primal_lengths: tuple[int, ...]
    dual_lengths: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class GenusTwoCrossingBasisRecovery:
    vertices: int
    edges: int
    triangles: int
    euler_characteristic: int
    min_triangles_per_edge: int
    max_triangles_per_edge: int
    successful_flips: int
    h1_dimension: int
    primal_vertex_degree_histogram: tuple[tuple[int, int], ...]
    dual_vertex_degree_histogram: tuple[tuple[int, int], ...]
    normalization_improving_flips: int
    primal_tree_edges: int
    dual_cotree_edges: int
    forbidden_dual_edges: int
    leftover_edges: int
    primal_path_scans: int
    dual_path_scans: int
    primal_cycle_lengths: tuple[int, ...]
    dual_cycle_lengths: tuple[int, ...]
    exact_crossing_matrix: tuple[tuple[int, ...], ...]
    off_diagonal_nonzero: int
    exact_verifier_accepted: bool
    full_primal_cycles: int
    full_dual_cycles: int
    full_primal_path_scans: int
    full_dual_path_scans: int
    full_crossing_matrix_rows: int
    full_crossing_matrix_cols: int
    full_crossing_matrix_weight: int
    full_crossing_matrix_rank: int
    full_crossing_matrix_row_xors: int


def _crossing_matrix(
    primal_cycles: tuple[Cycle, ...],
    dual_cycles: tuple[Cycle, ...],
    primal_edges: tuple[tuple[int, int], ...],
    dual_edges: tuple[tuple[int, int], ...],
) -> tuple[tuple[int, ...], ...] | None:
    primal_sets: list[set[int]] = []
    dual_sets: list[set[int]] = []
    for cycle in primal_cycles:
        indices = _cycle_indices(cycle, primal_edges)
        if indices is None:
            return None
        primal_sets.append(set(indices))
    for cycle in dual_cycles:
        indices = _cycle_indices(cycle, dual_edges)
        if indices is None:
            return None
        dual_sets.append(set(indices))
    return tuple(
        tuple(len(primal & dual) for dual in dual_sets)
        for primal in primal_sets
    )


def validate_genus2_crossing_basis_witness(
    public: GenusTwoCrossingBasisPublicInstance,
    witness: GenusTwoCrossingBasisWitness,
) -> GenusTwoCrossingBasisValidation:
    primal_edges = _edges(public.target)
    dual = _dual_data(public.target, primal_edges)
    primal_lengths = tuple(len(cycle) for cycle in witness.primal_cycles)
    dual_lengths = tuple(len(cycle) for cycle in witness.dual_cycles)
    empty: tuple[tuple[int, ...], ...] = ()

    if len(witness.primal_cycles) != 4 or len(witness.dual_cycles) != 4:
        return GenusTwoCrossingBasisValidation(
            False, "G21 witness must contain four primal and four dual cycles",
            empty, primal_lengths, dual_lengths,
        )
    if len(set(witness.primal_cycles)) != 4 or len(set(witness.dual_cycles)) != 4:
        return GenusTwoCrossingBasisValidation(
            False, "G21 witness cycles must be distinct within each side",
            empty, primal_lengths, dual_lengths,
        )
    if not all(_is_one_simple_cycle(cycle, primal_edges) for cycle in witness.primal_cycles):
        return GenusTwoCrossingBasisValidation(
            False, "G21 primal witness contains a non-simple public cycle",
            empty, primal_lengths, dual_lengths,
        )
    if not all(_is_one_simple_cycle(cycle, dual.dual_edges) for cycle in witness.dual_cycles):
        return GenusTwoCrossingBasisValidation(
            False, "G21 dual witness contains a non-simple public cycle",
            empty, primal_lengths, dual_lengths,
        )

    matrix = _crossing_matrix(
        witness.primal_cycles, witness.dual_cycles, primal_edges, dual.dual_edges
    )
    if matrix is None:
        return GenusTwoCrossingBasisValidation(
            False, "G21 crossing matrix could not be evaluated",
            empty, primal_lengths, dual_lengths,
        )
    identity = tuple(
        tuple(1 if row == column else 0 for column in range(4))
        for row in range(4)
    )
    if matrix != identity:
        return GenusTwoCrossingBasisValidation(
            False, "G21 exact geometric crossing matrix is not identity",
            matrix, primal_lengths, dual_lengths,
        )
    return GenusTwoCrossingBasisValidation(
        True, "accepted", matrix, primal_lengths, dual_lengths
    )


def _full_basis_crossing_metrics(
    vertex_count: int,
    triangle_count: int,
    primal_edges: tuple[tuple[int, int], ...],
    dual_edges: tuple[tuple[int, int], ...],
) -> tuple[int, int, int, int, int, int, int, int]:
    primal_basis = _fundamental_basis(vertex_count, primal_edges)
    dual_basis = _fundamental_basis(triangle_count, dual_edges)
    dual_sets = tuple(set(cycle) for cycle in dual_basis.cycles)
    rows: list[int] = []
    weight = 0
    for primal_cycle in primal_basis.cycles:
        primal_set = set(primal_cycle)
        row = 0
        for dual_index, dual_cycle in enumerate(dual_sets):
            if len(primal_set & dual_cycle) & 1:
                row |= 1 << dual_index
                weight += 1
        rows.append(row)
    reduced = _rref(rows, len(dual_basis.cycles))
    return (
        len(primal_basis.cycles),
        len(dual_basis.cycles),
        primal_basis.path_scans,
        dual_basis.path_scans,
        weight,
        reduced.rank,
        reduced.row_xors,
        len(rows),
    )


def recover_genus2_crossing_basis(
    public: GenusTwoCrossingBasisPublicInstance,
    *,
    successful_flips: int = -1,
) -> GenusTwoCrossingBasisRecovery:
    primal_edges = _edges(public.target)
    dual = _dual_data(public.target, primal_edges)
    incidence = toroidal_hypercover_incidence(
        ToroidalHypercoverPublicInstance(public.name, public.target)
    )
    _, _, h1_dimension = _cohomology_basis(public.target)
    primal_tree, dual_tree, leftovers = _tree_cotree_data(
        incidence.vertices, primal_edges, incidence.triangles, dual.dual_edges
    )
    if len(leftovers) != 4:
        raise GluingExperimentError(
            f"G21 genus-two tree-cotree decomposition expected four leftovers, got {len(leftovers)}"
        )

    primal_cycles: list[Cycle] = []
    dual_cycles: list[Cycle] = []
    primal_scans = 0
    dual_scans = 0
    for leftover in leftovers:
        pair, left_scans, right_scans, crossing_count = _pair_from_leftover(
            leftover, primal_edges, dual.dual_edges, primal_tree, dual_tree
        )
        if crossing_count != 1:
            raise GluingExperimentError("G21 paired tree-cotree cycle did not cross exactly once")
        primal_cycles.append(pair.primal_cycle)
        dual_cycles.append(pair.dual_cycle)
        primal_scans += left_scans
        dual_scans += right_scans

    witness = GenusTwoCrossingBasisWitness(tuple(primal_cycles), tuple(dual_cycles))
    validation = validate_genus2_crossing_basis_witness(public, witness)
    if not validation.valid:
        raise GluingExperimentError(
            "G21 public tree-cotree family failed exact crossing-matrix verifier: "
            + validation.reason
        )
    off_diagonal = sum(
        value != 0
        for row_index, row in enumerate(validation.crossing_matrix)
        for column_index, value in enumerate(row)
        if row_index != column_index
    )

    (
        full_primal,
        full_dual,
        full_primal_scans,
        full_dual_scans,
        full_weight,
        full_rank,
        full_row_xors,
        full_rows,
    ) = _full_basis_crossing_metrics(
        incidence.vertices, incidence.triangles, primal_edges, dual.dual_edges
    )
    if full_rank != 4:
        raise GluingExperimentError(
            f"G21 full primal-dual crossing matrix expected rank four, got {full_rank}"
        )

    return GenusTwoCrossingBasisRecovery(
        vertices=incidence.vertices,
        edges=incidence.edges,
        triangles=incidence.triangles,
        euler_characteristic=incidence.euler_characteristic,
        min_triangles_per_edge=incidence.min_triangles_per_edge,
        max_triangles_per_edge=incidence.max_triangles_per_edge,
        successful_flips=successful_flips,
        h1_dimension=h1_dimension,
        primal_vertex_degree_histogram=_primal_vertex_degree_histogram(public.target),
        dual_vertex_degree_histogram=_degree_histogram(incidence.triangles, dual.dual_edges),
        normalization_improving_flips=_normalization_improving_flip_count(public.target),
        primal_tree_edges=len(primal_tree.tree_edges),
        dual_cotree_edges=len(dual_tree.tree_edges),
        forbidden_dual_edges=len(primal_tree.tree_edges),
        leftover_edges=len(leftovers),
        primal_path_scans=primal_scans,
        dual_path_scans=dual_scans,
        primal_cycle_lengths=validation.primal_lengths,
        dual_cycle_lengths=validation.dual_lengths,
        exact_crossing_matrix=validation.crossing_matrix,
        off_diagonal_nonzero=off_diagonal,
        exact_verifier_accepted=validation.valid,
        full_primal_cycles=full_primal,
        full_dual_cycles=full_dual,
        full_primal_path_scans=full_primal_scans,
        full_dual_path_scans=full_dual_scans,
        full_crossing_matrix_rows=full_rows,
        full_crossing_matrix_cols=full_dual,
        full_crossing_matrix_weight=full_weight,
        full_crossing_matrix_rank=full_rank,
        full_crossing_matrix_row_xors=full_row_xors,
    )


def generate_genus2_crossing_basis_instance(
    params: GenusTwoCrossingBasisParameters,
    master_seed: bytes,
) -> GenusTwoCrossingBasisPublicInstance:
    params.validate()
    if len(master_seed) < 16:
        raise GluingExperimentError("G21 master seed must contain at least 128 bits")

    carrier_params = GenusTwoMulticurveParameters(
        params.name + "-carrier", params.rows, params.cols, params.successful_flips
    )
    base_seed = hashlib.sha256(
        b"MORPH-KEM G21 connected sum v1\x00" + master_seed + params.name.encode("ascii")
    ).digest()
    target = _connected_sum_tori(carrier_params, base_seed)
    flip_seed = hashlib.sha256(
        b"MORPH-KEM G21 flips v1\x00" + master_seed + params.name.encode("ascii")
    ).digest()
    target = _flip_surface(target, params.successful_flips, flip_seed)
    relabel_seed = hashlib.sha256(
        b"MORPH-KEM G21 relabel v1\x00" + master_seed + params.name.encode("ascii")
    ).digest()
    target = _final_relabel(target, relabel_seed)
    public = GenusTwoCrossingBasisPublicInstance(params.name, target)

    incidence = toroidal_hypercover_incidence(
        ToroidalHypercoverPublicInstance(params.name, target)
    )
    if incidence.euler_characteristic != -2:
        raise GluingExperimentError("G21 generated carrier does not have Euler characteristic -2")
    if incidence.min_triangles_per_edge != 2 or incidence.max_triangles_per_edge != 2:
        raise GluingExperimentError("G21 generated carrier is not closed")
    _, _, h1_dimension = _cohomology_basis(target)
    if h1_dimension != 4:
        raise GluingExperimentError(
            f"G21 generated carrier expected H1 dimension four, got {h1_dimension}"
        )
    recovery = recover_genus2_crossing_basis(
        public, successful_flips=params.successful_flips
    )
    if not recovery.exact_verifier_accepted or recovery.off_diagonal_nonzero:
        raise GluingExperimentError("G21 generated carrier failed public tree-cotree witness gate")
    return public
