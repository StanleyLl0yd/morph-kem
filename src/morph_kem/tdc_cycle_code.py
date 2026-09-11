from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib

from .complex import SimplicialComplex
from .surface import SurfaceParameters, generate_surface_instance


class TDCError(ValueError):
    """Raised when a TDC toy-control input is invalid."""


@dataclass(frozen=True, slots=True)
class TDCParameters:
    name: str
    rows: int
    cols: int

    def validate(self) -> None:
        if self.rows < 3 or self.rows > 16 or self.cols < 3 or self.cols > 16:
            raise TDCError("TDC0 torus dimensions outside toy bounds")


TDC0_PARAMETER_SETS = {
    "tdc0-4x4": TDCParameters("tdc0-4x4", 4, 4),
    "tdc0-6x6": TDCParameters("tdc0-6x6", 6, 6),
    "tdc0-8x8": TDCParameters("tdc0-8x8", 8, 8),
}


@dataclass(frozen=True, slots=True)
class TDCPublicCode:
    name: str
    target: SimplicialComplex


@dataclass(frozen=True, slots=True)
class TDCReference:
    planted_error_edge: int


@dataclass(frozen=True, slots=True)
class TDCCycleCodeMetrics:
    vertices: int
    edges: int
    triangles: int
    parity_rank: int
    code_dimension: int
    rate: float
    row_weight_histogram: tuple[tuple[int, int], ...]
    column_weight_histogram: tuple[tuple[int, int], ...]
    triangle_codeword_count: int
    triangle_codeword_weight_histogram: tuple[tuple[int, int], ...]
    exact_minimum_distance: int


@dataclass(frozen=True, slots=True)
class TDCSingleErrorRecovery:
    syndrome: int
    syndrome_weight: int
    lookup_entries: int
    recovered_error_edge: int
    accepted: bool
    matches_reference_after_public_success: bool | None


def _edges(public: TDCPublicCode) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(simplex for simplex in public.target.simplices if len(simplex) == 2))


def _triangles(public: TDCPublicCode) -> tuple[tuple[int, int, int], ...]:
    return tuple(sorted(simplex for simplex in public.target.simplices if len(simplex) == 3))


def _gf2_rank(rows: list[int]) -> int:
    basis: dict[int, int] = {}
    for value in rows:
        row = value
        while row:
            pivot = row.bit_length() - 1
            if pivot in basis:
                row ^= basis[pivot]
            else:
                basis[pivot] = row
                break
    return len(basis)


def _parity_rows(public: TDCPublicCode) -> tuple[int, ...]:
    edges = _edges(public)
    rows: list[int] = []
    for vertex in public.target.vertices:
        row = 0
        for edge_index, edge in enumerate(edges):
            if vertex in edge:
                row |= 1 << edge_index
        rows.append(row)
    return tuple(rows)


def _syndrome(public: TDCPublicCode, error_mask: int) -> int:
    rows = _parity_rows(public)
    syndrome = 0
    for vertex_index, row in enumerate(rows):
        if (row & error_mask).bit_count() & 1:
            syndrome |= 1 << vertex_index
    return syndrome


def cycle_code_metrics(public: TDCPublicCode) -> TDCCycleCodeMetrics:
    edges = _edges(public)
    triangles = _triangles(public)
    rows = _parity_rows(public)
    parity_rank = _gf2_rank(list(rows))

    edge_index = {edge: index for index, edge in enumerate(edges)}
    triangle_weights: list[int] = []
    for triangle in triangles:
        a, b, c = triangle
        boundary = (
            tuple(sorted((a, b))),
            tuple(sorted((a, c))),
            tuple(sorted((b, c))),
        )
        mask = sum(1 << edge_index[edge] for edge in boundary)
        if _syndrome(public, mask) != 0:
            raise TDCError("TDC0 triangle boundary is not a public cycle-code word")
        triangle_weights.append(mask.bit_count())

    row_weights = [row.bit_count() for row in rows]
    column_weights = [0] * len(edges)
    for row in rows:
        for edge_index_value in range(len(edges)):
            column_weights[edge_index_value] += (row >> edge_index_value) & 1

    # The public graph is simple: there are no loops or parallel edges, so a
    # nonzero cycle cannot have weight one or two. Every public triangle gives
    # a weight-three cycle, hence d_min is exactly three.
    if len(set(edges)) != len(edges) or any(left == right for left, right in edges):
        raise TDCError("TDC0 cycle-code control requires a simple public graph")
    if not triangle_weights or min(triangle_weights) != 3:
        raise TDCError("TDC0 expected public weight-three triangle codewords")

    code_dimension = len(edges) - parity_rank
    return TDCCycleCodeMetrics(
        vertices=len(public.target.vertices),
        edges=len(edges),
        triangles=len(triangles),
        parity_rank=parity_rank,
        code_dimension=code_dimension,
        rate=code_dimension / len(edges),
        row_weight_histogram=tuple(sorted(Counter(row_weights).items())),
        column_weight_histogram=tuple(sorted(Counter(column_weights).items())),
        triangle_codeword_count=len(triangles),
        triangle_codeword_weight_histogram=tuple(sorted(Counter(triangle_weights).items())),
        exact_minimum_distance=3,
    )


def generate_tdc0_instance(
    params: TDCParameters,
    master_seed: bytes,
) -> tuple[TDCPublicCode, TDCReference]:
    params.validate()
    if len(master_seed) < 16:
        raise TDCError("TDC0 master seed must contain at least 128 bits")

    surface_seed = hashlib.sha256(
        b"MORPH-KEM TDC0 surface v1\x00" + master_seed + params.name.encode("ascii")
    ).digest()
    surface_public, _ = generate_surface_instance(
        SurfaceParameters(params.name + "-surface", params.rows, params.cols),
        surface_seed,
    )
    public = TDCPublicCode(name=params.name, target=surface_public.target)
    edges = _edges(public)
    error_bytes = hashlib.sha256(
        b"MORPH-KEM TDC0 planted one-edge error v1\x00"
        + master_seed
        + params.name.encode("ascii")
    ).digest()
    planted_error_edge = int.from_bytes(error_bytes[:8], "big") % len(edges)
    return public, TDCReference(planted_error_edge=planted_error_edge)


def recover_single_edge_error(
    public: TDCPublicCode,
    syndrome: int,
    *,
    reference: TDCReference | None = None,
) -> TDCSingleErrorRecovery:
    edges = _edges(public)
    lookup: dict[int, int] = {}
    for edge_index in range(len(edges)):
        edge_syndrome = _syndrome(public, 1 << edge_index)
        if edge_syndrome in lookup:
            raise TDCError("TDC0 single-edge syndromes are not unique")
        lookup[edge_syndrome] = edge_index

    if syndrome not in lookup:
        raise TDCError("TDC0 syndrome is not a public single-edge syndrome")
    recovered = lookup[syndrome]
    accepted = _syndrome(public, 1 << recovered) == syndrome
    matches = None if reference is None else recovered == reference.planted_error_edge
    return TDCSingleErrorRecovery(
        syndrome=syndrome,
        syndrome_weight=syndrome.bit_count(),
        lookup_entries=len(lookup),
        recovered_error_edge=recovered,
        accepted=accepted,
        matches_reference_after_public_success=matches,
    )


def planted_single_edge_syndrome(
    public: TDCPublicCode,
    reference: TDCReference,
) -> int:
    if reference.planted_error_edge < 0 or reference.planted_error_edge >= len(_edges(public)):
        raise TDCError("TDC0 planted error edge is outside public code")
    return _syndrome(public, 1 << reference.planted_error_edge)
