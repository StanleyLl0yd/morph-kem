from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib

from .tdc_cycle_code import _gf2_rank
from .tdc_rank_matched import (
    TDC2F_PARAMETER_SETS,
    TDC2FError,
    _minimum_weight_leq8,
    generate_tdc2f_instance,
)
from .tdc_sparse_faces import SparseFaceCode, _low_weight_leq6, _row_degrees
from .tdc_sparse_mixing import _tanner_four_cycles


class TDC2GError(TDC2FError):
    """Raised when a TDC2g random-overlay experiment is malformed."""


@dataclass(frozen=True, slots=True)
class TDC2GParameters:
    name: str
    base_name: str
    extra_rows: int = 6
    max_overlay_attempts: int = 4096

    def validate(self) -> None:
        if self.base_name not in TDC2F_PARAMETER_SETS:
            raise TDC2GError("unknown TDC2f base parameter set")
        if self.extra_rows < 1 or self.extra_rows > 16:
            raise TDC2GError("TDC2g extra-row count outside toy bounds")
        if self.max_overlay_attempts < self.extra_rows or self.max_overlay_attempts > 65536:
            raise TDC2GError("TDC2g overlay attempt cap outside toy bounds")


TDC2G_PARAMETER_SETS = {
    "tdc2g-n8": TDC2GParameters("tdc2g-n8", "tdc2f-n8"),
    "tdc2g-n9": TDC2GParameters("tdc2g-n9", "tdc2f-n9"),
    "tdc2g-n10": TDC2GParameters("tdc2g-n10", "tdc2f-n10"),
}


@dataclass(frozen=True, slots=True)
class OverlayPair:
    topology: SparseFaceCode
    matched_random: SparseFaceCode
    base_rank: int
    final_rank: int
    overlay_rows: tuple[int, ...]
    overlay_attempts: int


@dataclass(frozen=True, slots=True)
class TDC2GMetrics:
    rows: int
    columns: int
    rank: int
    dimension: int
    rate: float
    row_weight_histogram: tuple[tuple[int, int], ...]
    column_weight_histogram: tuple[tuple[int, int], ...]
    minimum_weight_leq6: int | None
    minimum_weight_leq8: int | None
    weight8_witness_support: tuple[int, ...]
    tanner_four_cycles: int


@dataclass(frozen=True, slots=True)
class TDC2GRecovery:
    topology: TDC2GMetrics
    matched_random: TDC2GMetrics
    base_rank: int
    final_rank: int
    extra_rows: int
    overlay_attempts: int
    rank_profile_equal: bool
    dimension_profile_equal: bool


def _digest(domain: bytes, seed: bytes, name: str, counter: int) -> bytes:
    return hashlib.sha256(
        domain + b"\x00" + seed + name.encode("ascii") + counter.to_bytes(8, "big")
    ).digest()


def _row_masks(code: SparseFaceCode) -> list[int]:
    rows = [0] * code.row_count
    for column_index, column in enumerate(code.columns):
        for row_index in range(code.row_count):
            if (column >> row_index) & 1:
                rows[row_index] |= 1 << column_index
    return rows


def _append_row(code: SparseFaceCode, row_mask: int) -> SparseFaceCode:
    if row_mask <= 0 or row_mask >= (1 << len(code.columns)):
        raise TDC2GError("TDC2g overlay row mask outside column bounds")
    new_bit = 1 << code.row_count
    columns = tuple(
        column | (new_bit if (row_mask >> index) & 1 else 0)
        for index, column in enumerate(code.columns)
    )
    return SparseFaceCode(code.name + "-overlay", code.row_count + 1, columns)


def _independent_of_rows(code: SparseFaceCode, row_mask: int) -> bool:
    rows = _row_masks(code)
    return _gf2_rank(rows + [row_mask]) == _gf2_rank(rows) + 1


def _common_overlay(
    topology: SparseFaceCode,
    random: SparseFaceCode,
    params: TDC2GParameters,
    seed: bytes,
) -> OverlayPair:
    if len(topology.columns) != len(random.columns):
        raise TDC2GError("TDC2g paired column counts differ")
    if _gf2_rank(list(topology.columns)) != _gf2_rank(list(random.columns)):
        raise TDC2GError("TDC2g base ranks differ")

    base_rank = _gf2_rank(list(topology.columns))
    column_count = len(topology.columns)
    mask_limit = (1 << column_count) - 1
    accepted: list[int] = []
    attempts = 0
    top = topology
    ctl = random

    for counter in range(params.max_overlay_attempts):
        attempts += 1
        digest = _digest(
            b"MORPH-KEM TDC2g common parity overlay v1",
            seed,
            params.name,
            counter,
        )
        row_mask = int.from_bytes(digest, "big") & mask_limit
        if row_mask == 0 or row_mask == mask_limit:
            continue
        if row_mask in accepted:
            continue
        if not _independent_of_rows(top, row_mask):
            continue
        if not _independent_of_rows(ctl, row_mask):
            continue
        top = _append_row(top, row_mask)
        ctl = _append_row(ctl, row_mask)
        accepted.append(row_mask)
        if len(accepted) == params.extra_rows:
            break

    if len(accepted) != params.extra_rows:
        raise TDC2GError("TDC2g common overlay attempt cap exhausted")

    final_rank = base_rank + params.extra_rows
    for code in (top, ctl):
        if _gf2_rank(list(code.columns)) != final_rank:
            raise TDC2GError("TDC2g overlay failed to increase rank as declared")
    return OverlayPair(top, ctl, base_rank, final_rank, tuple(accepted), attempts)


def generate_tdc2g_instance(
    params: TDC2GParameters,
    master_seed: bytes,
) -> OverlayPair:
    params.validate()
    if len(master_seed) < 16:
        raise TDC2GError("TDC2g seed must contain at least 128 bits")
    base = generate_tdc2f_instance(TDC2F_PARAMETER_SETS[params.base_name], master_seed)
    return _common_overlay(
        base.topology.code,
        base.matched_random.code,
        params,
        master_seed,
    )


def _metrics(code: SparseFaceCode) -> TDC2GMetrics:
    rank = _gf2_rank(list(code.columns))
    minimum6, _, _, _ = _low_weight_leq6(code.columns)
    bounded8 = _minimum_weight_leq8(code.columns, minimum6)
    dimension = len(code.columns) - rank
    return TDC2GMetrics(
        rows=code.row_count,
        columns=len(code.columns),
        rank=rank,
        dimension=dimension,
        rate=dimension / len(code.columns),
        row_weight_histogram=tuple(sorted(Counter(_row_degrees(code)).items())),
        column_weight_histogram=tuple(
            sorted(Counter(column.bit_count() for column in code.columns).items())
        ),
        minimum_weight_leq6=minimum6,
        minimum_weight_leq8=bounded8.minimum_weight_leq8,
        weight8_witness_support=bounded8.witness_support,
        tanner_four_cycles=_tanner_four_cycles(code),
    )


def recover_tdc2g(instance: OverlayPair) -> TDC2GRecovery:
    topology = _metrics(instance.topology)
    random = _metrics(instance.matched_random)
    return TDC2GRecovery(
        topology=topology,
        matched_random=random,
        base_rank=instance.base_rank,
        final_rank=instance.final_rank,
        extra_rows=instance.final_rank - instance.base_rank,
        overlay_attempts=instance.overlay_attempts,
        rank_profile_equal=(topology.rows == random.rows and topology.rank == random.rank),
        dimension_profile_equal=(
            topology.columns == random.columns
            and topology.dimension == random.dimension
            and topology.rate == random.rate
        ),
    )
