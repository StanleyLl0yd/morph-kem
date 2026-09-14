from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib
from itertools import combinations

from .tdc_cycle_code import _gf2_rank
from .tdc_sparse_faces import (
    SparseFaceCode,
    TDC2SparseError,
    TDC2_SPARSE_PARAMETER_SETS,
    _low_weight_leq6,
    _row_degrees,
    generate_tdc2_sparse_instance,
)
from .tdc_sparse_mixing import (
    SparseMixingReference,
    _mixed_columns,
    _public_relabel,
    _tanner_four_cycles,
)


class TDC2FError(TDC2SparseError):
    """Raised when a TDC2f rank-matched control is malformed."""


@dataclass(frozen=True, slots=True)
class TDC2FParameters:
    name: str
    base_name: str
    row_scramble_rounds: int = 2
    column_mixing_rounds: int = 2
    max_control_attempts: int = 256

    def validate(self) -> None:
        if self.base_name not in TDC2_SPARSE_PARAMETER_SETS:
            raise TDC2FError("unknown TDC2b base parameter set")
        if self.row_scramble_rounds not in (1, 2, 3, 4):
            raise TDC2FError("TDC2f row-scramble rounds outside toy bounds")
        if self.column_mixing_rounds not in (1, 2, 3, 4):
            raise TDC2FError("TDC2f column-mixing rounds outside toy bounds")
        if self.max_control_attempts < 1 or self.max_control_attempts > 4096:
            raise TDC2FError("TDC2f control attempt cap outside toy bounds")


TDC2F_PARAMETER_SETS = {
    "tdc2f-n8": TDC2FParameters("tdc2f-n8", "tdc2b-n8"),
    "tdc2f-n9": TDC2FParameters("tdc2f-n9", "tdc2b-n9"),
    "tdc2f-n10": TDC2FParameters("tdc2f-n10", "tdc2b-n10"),
}


@dataclass(frozen=True, slots=True)
class RankMatchedCode:
    code: SparseFaceCode
    row_scramble_operations: int
    column_mixing_reference: SparseMixingReference
    control_generation_attempts: int


@dataclass(frozen=True, slots=True)
class TDC2FInstance:
    topology: RankMatchedCode
    matched_random: RankMatchedCode
    target_rank: int


@dataclass(frozen=True, slots=True)
class BoundedKernel8:
    minimum_weight_leq8: int | None
    witness_support: tuple[int, ...]
    triple_subsets_indexed: int
    four_subsets_scanned: int
    collision_candidates_tested: int


@dataclass(frozen=True, slots=True)
class TDC2FMetrics:
    rows: int
    columns: int
    rank: int
    dimension: int
    rate: float
    row_scramble_operations: int
    column_mixing_operations: int
    rejected_column_mixing_candidates: int
    control_generation_attempts: int
    row_weight_histogram: tuple[tuple[int, int], ...]
    column_weight_histogram: tuple[tuple[int, int], ...]
    minimum_weight_leq6: int | None
    minimum_weight_multiplicity: int
    minimum_weight_leq8: int | None
    weight8_witness_support: tuple[int, ...]
    triple_subsets_indexed: int
    four_subsets_scanned: int
    collision_candidates_tested: int
    pair_syndrome_collision_buckets: int
    triple_syndrome_collision_buckets: int
    tanner_four_cycles: int


@dataclass(frozen=True, slots=True)
class TDC2FRecovery:
    topology: TDC2FMetrics
    matched_random: TDC2FMetrics
    rank_profile_equal: bool
    dimension_profile_equal: bool


def _digest(domain: bytes, seed: bytes, name: str, counter: int = 0) -> bytes:
    return hashlib.sha256(
        domain + b"\x00" + seed + name.encode("ascii") + counter.to_bytes(8, "big")
    ).digest()


def _row_masks(code: SparseFaceCode) -> list[int]:
    rows = [0] * code.row_count
    for column_index, column in enumerate(code.columns):
        for row in range(code.row_count):
            if (column >> row) & 1:
                rows[row] |= 1 << column_index
    return rows


def _independent_row_basis(code: SparseFaceCode) -> SparseFaceCode:
    pivots: dict[int, int] = {}
    for original in _row_masks(code):
        value = original
        while value:
            pivot = value.bit_length() - 1
            existing = pivots.get(pivot)
            if existing is None:
                pivots[pivot] = value
                break
            value ^= existing
    basis = tuple(pivots[pivot] for pivot in sorted(pivots, reverse=True))
    rank = len(basis)
    if rank != _gf2_rank(list(code.columns)):
        raise TDC2FError("TDC2f row-basis rank mismatch")

    columns: list[int] = []
    for column_index in range(len(code.columns)):
        value = 0
        for row_index, row_mask in enumerate(basis):
            if (row_mask >> column_index) & 1:
                value |= 1 << row_index
        columns.append(value)
    compressed = SparseFaceCode(code.name + "-rowspace", rank, tuple(columns))
    if any(column == 0 for column in compressed.columns):
        raise TDC2FError("TDC2f row compression created a zero column")
    if len(set(compressed.columns)) != len(compressed.columns):
        raise TDC2FError("TDC2f row compression created duplicate columns")
    if _gf2_rank(list(compressed.columns)) != rank:
        raise TDC2FError("TDC2f compressed topology lost rank")
    return compressed


def _row_scramble(
    code: SparseFaceCode,
    rounds: int,
    seed: bytes,
    domain: bytes,
    name: str,
) -> tuple[SparseFaceCode, int]:
    columns = list(code.columns)
    operations = 0
    for round_index in range(rounds):
        for target in range(code.row_count):
            digest = _digest(
                domain + b" source",
                seed,
                name,
                round_index * code.row_count + target,
            )
            source = int.from_bytes(digest[:8], "big") % (code.row_count - 1)
            if source >= target:
                source += 1
            updated: list[int] = []
            for column in columns:
                if (column >> source) & 1:
                    column ^= 1 << target
                updated.append(column)
            columns = updated
            operations += 1
    scrambled = SparseFaceCode(code.name + "-rowscrambled", code.row_count, tuple(columns))
    if _gf2_rank(list(scrambled.columns)) != code.row_count:
        raise TDC2FError("TDC2f invertible row scrambling changed rank")
    return scrambled, operations


def _random_full_rank_control(
    row_count: int,
    column_count: int,
    seed: bytes,
    name: str,
    max_attempts: int,
) -> tuple[SparseFaceCode, int]:
    if row_count < 2 or column_count <= row_count:
        raise TDC2FError("TDC2f control dimensions outside declared regime")
    mask = (1 << row_count) - 1
    for attempt in range(max_attempts):
        columns: list[int] = []
        seen: set[int] = set()
        valid = True
        for column_index in range(column_count):
            selected = 0
            for retry in range(64):
                digest = _digest(
                    b"MORPH-KEM TDC2f rank-matched control column v1",
                    seed,
                    name,
                    attempt * column_count * 64 + column_index * 64 + retry,
                )
                value = int.from_bytes(digest, "big") & mask
                if value == 0 or value in seen:
                    continue
                selected = value
                break
            if selected == 0:
                valid = False
                break
            seen.add(selected)
            columns.append(selected)
        if not valid:
            continue
        if _gf2_rank(columns) != row_count:
            continue
        return SparseFaceCode(name + "-control", row_count, tuple(columns)), attempt + 1
    raise TDC2FError("TDC2f rank-matched random control attempt cap exhausted")


def _finalize(
    code: SparseFaceCode,
    params: TDC2FParameters,
    seed: bytes,
    domain: bytes,
    name: str,
    control_attempts: int,
) -> RankMatchedCode:
    scrambled, row_operations = _row_scramble(
        code,
        params.row_scramble_rounds,
        seed,
        domain + b" row scramble",
        name,
    )
    mixed, reference = _mixed_columns(
        scrambled,
        params.column_mixing_rounds,
        seed,
        domain + b" column mixing",
        name,
    )
    public = _public_relabel(
        scrambled,
        mixed,
        seed,
        domain + b" public relabel",
        name,
    )
    return RankMatchedCode(public, row_operations, reference, control_attempts)


def generate_tdc2f_instance(
    params: TDC2FParameters,
    master_seed: bytes,
) -> TDC2FInstance:
    params.validate()
    if len(master_seed) < 16:
        raise TDC2FError("TDC2f seed must contain at least 128 bits")

    base = generate_tdc2_sparse_instance(
        TDC2_SPARSE_PARAMETER_SETS[params.base_name], master_seed
    )
    topology_basis = _independent_row_basis(base.topology_code)
    target_rank = topology_basis.row_count
    control, attempts = _random_full_rank_control(
        target_rank,
        len(topology_basis.columns),
        master_seed,
        params.name,
        params.max_control_attempts,
    )
    topology = _finalize(
        topology_basis,
        params,
        master_seed,
        b"MORPH-KEM TDC2f topology v1",
        params.name + "-topology",
        0,
    )
    random = _finalize(
        control,
        params,
        master_seed,
        b"MORPH-KEM TDC2f control v1",
        params.name + "-random",
        attempts,
    )
    for item in (topology.code, random.code):
        if item.row_count != target_rank:
            raise TDC2FError("TDC2f public row count drifted")
        if _gf2_rank(list(item.columns)) != target_rank:
            raise TDC2FError("TDC2f public rank drifted")
    if len(topology.code.columns) != len(random.code.columns):
        raise TDC2FError("TDC2f public column counts differ")
    return TDC2FInstance(topology, random, target_rank)


def _support_mask(indices: tuple[int, ...]) -> int:
    mask = 0
    for index in indices:
        mask |= 1 << index
    return mask


def _mask_support(mask: int) -> tuple[int, ...]:
    return tuple(index for index in range(mask.bit_length()) if (mask >> index) & 1)


def _verify_kernel_support(columns: tuple[int, ...], support: tuple[int, ...]) -> None:
    syndrome = 0
    for index in support:
        syndrome ^= columns[index]
    if syndrome != 0:
        raise TDC2FError("TDC2f bounded-kernel attack produced an invalid support")


def _minimum_weight_leq8(
    columns: tuple[int, ...],
    minimum_leq6: int | None,
) -> BoundedKernel8:
    if minimum_leq6 is not None:
        return BoundedKernel8(minimum_leq6, (), 0, 0, 0)

    triple_buckets: dict[int, list[int]] = {}
    triple_count = 0
    for triple in combinations(range(len(columns)), 3):
        syndrome = columns[triple[0]] ^ columns[triple[1]] ^ columns[triple[2]]
        triple_buckets.setdefault(syndrome, []).append(_support_mask(triple))
        triple_count += 1

    four_buckets: dict[int, list[int]] = {}
    four_count = 0
    collision_checks = 0
    first_weight8_mask: int | None = None

    for four in combinations(range(len(columns)), 4):
        four_mask = _support_mask(four)
        syndrome = (
            columns[four[0]]
            ^ columns[four[1]]
            ^ columns[four[2]]
            ^ columns[four[3]]
        )
        four_count += 1

        for triple_mask in triple_buckets.get(syndrome, ()):
            collision_checks += 1
            if triple_mask & four_mask:
                continue
            support = _mask_support(triple_mask | four_mask)
            if len(support) != 7:
                raise TDC2FError("TDC2f weight-seven support accounting failed")
            _verify_kernel_support(columns, support)
            return BoundedKernel8(7, support, triple_count, four_count, collision_checks)

        if first_weight8_mask is None:
            previous = four_buckets.setdefault(syndrome, [])
            for other_mask in previous:
                collision_checks += 1
                if other_mask & four_mask:
                    continue
                first_weight8_mask = other_mask | four_mask
                break
            previous.append(four_mask)

    if first_weight8_mask is not None:
        support = _mask_support(first_weight8_mask)
        if len(support) != 8:
            raise TDC2FError("TDC2f weight-eight support accounting failed")
        _verify_kernel_support(columns, support)
        return BoundedKernel8(8, support, triple_count, four_count, collision_checks)

    return BoundedKernel8(None, (), triple_count, four_count, collision_checks)


def _metrics(item: RankMatchedCode) -> TDC2FMetrics:
    code = item.code
    rank = _gf2_rank(list(code.columns))
    minimum, multiplicity, pair_collisions, triple_collisions = _low_weight_leq6(
        code.columns
    )
    bounded8 = _minimum_weight_leq8(code.columns, minimum)
    dimension = len(code.columns) - rank
    return TDC2FMetrics(
        rows=code.row_count,
        columns=len(code.columns),
        rank=rank,
        dimension=dimension,
        rate=dimension / len(code.columns),
        row_scramble_operations=item.row_scramble_operations,
        column_mixing_operations=len(item.column_mixing_reference.operations),
        rejected_column_mixing_candidates=item.column_mixing_reference.rejected_candidates,
        control_generation_attempts=item.control_generation_attempts,
        row_weight_histogram=tuple(sorted(Counter(_row_degrees(code)).items())),
        column_weight_histogram=tuple(
            sorted(Counter(column.bit_count() for column in code.columns).items())
        ),
        minimum_weight_leq6=minimum,
        minimum_weight_multiplicity=multiplicity,
        minimum_weight_leq8=bounded8.minimum_weight_leq8,
        weight8_witness_support=bounded8.witness_support,
        triple_subsets_indexed=bounded8.triple_subsets_indexed,
        four_subsets_scanned=bounded8.four_subsets_scanned,
        collision_candidates_tested=bounded8.collision_candidates_tested,
        pair_syndrome_collision_buckets=pair_collisions,
        triple_syndrome_collision_buckets=triple_collisions,
        tanner_four_cycles=_tanner_four_cycles(code),
    )


def recover_tdc2f(instance: TDC2FInstance) -> TDC2FRecovery:
    topology = _metrics(instance.topology)
    random = _metrics(instance.matched_random)
    return TDC2FRecovery(
        topology=topology,
        matched_random=random,
        rank_profile_equal=(
            topology.rows == random.rows and topology.rank == random.rank
        ),
        dimension_profile_equal=(
            topology.columns == random.columns
            and topology.dimension == random.dimension
            and topology.rate == random.rate
        ),
    )
