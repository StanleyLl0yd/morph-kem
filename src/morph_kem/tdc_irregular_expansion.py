from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib

from .gluing import _DeterministicRng
from .tdc_cyclic_lift import _color_refinement
from .tdc_sparse_faces import (
    SparseFaceCode,
    TDC2SparseError,
    TDC2_SPARSE_PARAMETER_SETS,
    _low_weight_leq6,
    _row_degrees,
    generate_tdc2_sparse_instance,
)


class TDC2DError(TDC2SparseError):
    """Raised when a TDC2d irregular incidence expansion is malformed."""


@dataclass(frozen=True, slots=True)
class TDC2DParameters:
    name: str
    base_name: str

    def validate(self) -> None:
        if self.base_name not in TDC2_SPARSE_PARAMETER_SETS:
            raise TDC2DError("unknown TDC2b base parameter set")


TDC2D_PARAMETER_SETS = {
    "tdc2d-n8": TDC2DParameters("tdc2d-n8", "tdc2b-n8"),
    "tdc2d-n9": TDC2DParameters("tdc2d-n9", "tdc2b-n9"),
    "tdc2d-n10": TDC2DParameters("tdc2d-n10", "tdc2b-n10"),
}


@dataclass(frozen=True, slots=True)
class IrregularExpansion:
    code: SparseFaceCode
    row_multiplicities: tuple[int, ...]
    row_fibers: tuple[tuple[int, ...], ...]
    column_fibers: tuple[tuple[int, ...], ...]


@dataclass(frozen=True, slots=True)
class TDC2DInstance:
    topology: IrregularExpansion
    matched_random: IrregularExpansion


@dataclass(frozen=True, slots=True)
class TDC2DMetrics:
    rows: int
    columns: int
    row_multiplicity_histogram: tuple[tuple[int, int], ...]
    row_weight_histogram: tuple[tuple[int, int], ...]
    column_weight_histogram: tuple[tuple[int, int], ...]
    color_rounds: int
    color_class_size_histogram: tuple[tuple[int, int], ...]
    singleton_color_classes: int
    maximum_color_class_size: int
    exact_row_fibers_recovered_by_color: int
    total_row_fibers: int
    exact_column_fibers_recovered_by_color: int
    total_column_fibers: int
    minimum_weight_leq6: int | None
    minimum_weight_multiplicity: int
    pair_syndrome_collision_buckets: int
    triple_syndrome_collision_buckets: int


@dataclass(frozen=True, slots=True)
class TDC2DRecovery:
    topology: TDC2DMetrics
    matched_random: TDC2DMetrics


def _digest(domain: bytes, seed: bytes, name: str, counter: int = 0) -> bytes:
    return hashlib.sha256(
        domain + b"\x00" + seed + name.encode("ascii") + counter.to_bytes(8, "big")
    ).digest()


def _row_multiplicities(row_count: int, seed: bytes, name: str) -> tuple[int, ...]:
    values = []
    for row in range(row_count):
        digest = _digest(b"MORPH-KEM TDC2d row multiplicity v1", seed, name, row)
        values.append(2 + (digest[0] & 1))
    if len(set(values)) == 1 and row_count > 1:
        values[-1] = 3 if values[-1] == 2 else 2
    return tuple(values)


def _expand(
    code: SparseFaceCode,
    row_multiplicities: tuple[int, ...],
    seed: bytes,
    domain: bytes,
    name: str,
) -> IrregularExpansion:
    if len(row_multiplicities) != code.row_count:
        raise TDC2DError("TDC2d row multiplicity count mismatch")
    if any(value not in (2, 3) for value in row_multiplicities):
        raise TDC2DError("TDC2d row multiplicity outside declared values")

    row_offsets: list[int] = []
    total_rows = 0
    for multiplicity in row_multiplicities:
        row_offsets.append(total_rows)
        total_rows += multiplicity

    raw_columns: list[int] = []
    raw_column_fibers: list[tuple[int, int]] = []
    for base_col, mask in enumerate(code.columns):
        fiber: list[int] = []
        for clone in range(2):
            lifted_mask = 0
            for base_row in range(code.row_count):
                if not ((mask >> base_row) & 1):
                    continue
                multiplicity = row_multiplicities[base_row]
                shift = int.from_bytes(
                    _digest(
                        domain + b" incidence shift",
                        seed,
                        name,
                        base_col * code.row_count + base_row,
                    )[:8],
                    "big",
                ) % multiplicity
                row_clone = (clone + shift) % multiplicity
                lifted_row = row_offsets[base_row] + row_clone
                lifted_mask |= 1 << lifted_row
            fiber.append(len(raw_columns))
            raw_columns.append(lifted_mask)
        raw_column_fibers.append((fiber[0], fiber[1]))

    if any(column.bit_count() != 3 for column in raw_columns):
        raise TDC2DError("TDC2d expansion lost column weight three")
    if len(set(raw_columns)) != len(raw_columns):
        raise TDC2DError("TDC2d expansion created duplicate public columns")

    raw_row_fibers = tuple(
        tuple(range(row_offsets[row], row_offsets[row] + row_multiplicities[row]))
        for row in range(code.row_count)
    )

    row_map = list(range(total_rows))
    col_order = list(range(len(raw_columns)))
    row_rng = _DeterministicRng(domain + b" row relabel", _digest(domain + b" rows", seed, name))
    col_rng = _DeterministicRng(domain + b" col relabel", _digest(domain + b" cols", seed, name))
    row_rng.shuffle(row_map)
    col_rng.shuffle(col_order)
    col_new_index = {old: new for new, old in enumerate(col_order)}

    columns: list[int] = []
    for old_col in col_order:
        old_mask = raw_columns[old_col]
        new_mask = 0
        for old_row, new_row in enumerate(row_map):
            if (old_mask >> old_row) & 1:
                new_mask |= 1 << new_row
        columns.append(new_mask)

    row_fibers = tuple(
        tuple(sorted(row_map[old] for old in fiber))
        for fiber in raw_row_fibers
    )
    column_fibers = tuple(
        tuple(sorted(col_new_index[old] for old in fiber))
        for fiber in raw_column_fibers
    )
    return IrregularExpansion(
        SparseFaceCode(name, total_rows, tuple(columns)),
        row_multiplicities,
        row_fibers,
        column_fibers,
    )


def generate_tdc2d_instance(
    params: TDC2DParameters,
    master_seed: bytes,
) -> TDC2DInstance:
    params.validate()
    if len(master_seed) < 16:
        raise TDC2DError("TDC2d seed must contain at least 128 bits")
    base = generate_tdc2_sparse_instance(TDC2_SPARSE_PARAMETER_SETS[params.base_name], master_seed)
    row_multiplicities = _row_multiplicities(
        base.topology_code.row_count, master_seed, params.name
    )
    topology = _expand(
        base.topology_code,
        row_multiplicities,
        master_seed,
        b"MORPH-KEM TDC2d topology expansion v1",
        params.name + "-topology",
    )
    random = _expand(
        base.matched_random,
        row_multiplicities,
        master_seed,
        b"MORPH-KEM TDC2d random expansion v1",
        params.name + "-random",
    )
    return TDC2DInstance(topology, random)


def _color_classes(code: SparseFaceCode) -> tuple[dict[int, set[int]], int, tuple[tuple[int, int], ...]]:
    colors, rounds, histogram = _color_refinement(code)
    classes: dict[int, set[int]] = {}
    for node, color in enumerate(colors):
        classes.setdefault(color, set()).add(node)
    return classes, rounds, histogram


def _metrics(expansion: IrregularExpansion) -> TDC2DMetrics:
    code = expansion.code
    classes, rounds, class_hist = _color_classes(code)
    public_sets = set(frozenset(nodes) for nodes in classes.values())

    row_fibers = tuple(frozenset(fiber) for fiber in expansion.row_fibers)
    column_fibers = tuple(
        frozenset(code.row_count + col for col in fiber)
        for fiber in expansion.column_fibers
    )
    exact_rows = sum(fiber in public_sets for fiber in row_fibers)
    exact_cols = sum(fiber in public_sets for fiber in column_fibers)

    minimum, multiplicity, pair_collisions, triple_collisions = _low_weight_leq6(code.columns)
    sizes = [len(nodes) for nodes in classes.values()]
    row_hist = tuple(sorted(Counter(_row_degrees(code)).items()))
    col_hist = tuple(sorted(Counter(column.bit_count() for column in code.columns).items()))
    return TDC2DMetrics(
        rows=code.row_count,
        columns=len(code.columns),
        row_multiplicity_histogram=tuple(sorted(Counter(expansion.row_multiplicities).items())),
        row_weight_histogram=row_hist,
        column_weight_histogram=col_hist,
        color_rounds=rounds,
        color_class_size_histogram=class_hist,
        singleton_color_classes=sum(size == 1 for size in sizes),
        maximum_color_class_size=max(sizes),
        exact_row_fibers_recovered_by_color=exact_rows,
        total_row_fibers=len(row_fibers),
        exact_column_fibers_recovered_by_color=exact_cols,
        total_column_fibers=len(column_fibers),
        minimum_weight_leq6=minimum,
        minimum_weight_multiplicity=multiplicity,
        pair_syndrome_collision_buckets=pair_collisions,
        triple_syndrome_collision_buckets=triple_collisions,
    )


def recover_tdc2d(instance: TDC2DInstance) -> TDC2DRecovery:
    return TDC2DRecovery(
        topology=_metrics(instance.topology),
        matched_random=_metrics(instance.matched_random),
    )
