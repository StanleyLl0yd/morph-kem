from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib
from itertools import combinations

from .gluing import _DeterministicRng
from .tdc_cycle_code import _gf2_rank
from .tdc_sparse_faces import (
    SparseFaceCode,
    TDC2SparseError,
    TDC2_SPARSE_PARAMETER_SETS,
    _low_weight_leq6,
    _row_degrees,
    generate_tdc2_sparse_instance,
)


class TDC2EError(TDC2SparseError):
    """Raised when a TDC2e sparse variable-mixing control is malformed."""


@dataclass(frozen=True, slots=True)
class TDC2EParameters:
    name: str
    base_name: str
    mixing_rounds: int = 2

    def validate(self) -> None:
        if self.base_name not in TDC2_SPARSE_PARAMETER_SETS:
            raise TDC2EError("unknown TDC2b base parameter set")
        if self.mixing_rounds not in (1, 2, 3, 4):
            raise TDC2EError("TDC2e mixing rounds outside declared toy values")


TDC2E_PARAMETER_SETS = {
    "tdc2e-n8": TDC2EParameters("tdc2e-n8", "tdc2b-n8", 2),
    "tdc2e-n9": TDC2EParameters("tdc2e-n9", "tdc2b-n9", 2),
    "tdc2e-n10": TDC2EParameters("tdc2e-n10", "tdc2b-n10", 2),
}


@dataclass(frozen=True, slots=True)
class SparseMixingReference:
    operations: tuple[tuple[int, int], ...]
    rejected_candidates: int


@dataclass(frozen=True, slots=True)
class SparseMixedCode:
    code: SparseFaceCode
    reference: SparseMixingReference
    base_column_weight_histogram: tuple[tuple[int, int], ...]


@dataclass(frozen=True, slots=True)
class TDC2EInstance:
    topology: SparseMixedCode
    matched_random: SparseMixedCode


@dataclass(frozen=True, slots=True)
class TDC2EMetrics:
    rows: int
    columns: int
    rank: int
    dimension: int
    rate: float
    successful_mixing_operations: int
    rejected_mixing_candidates: int
    base_column_weight_histogram: tuple[tuple[int, int], ...]
    public_row_weight_histogram: tuple[tuple[int, int], ...]
    public_column_weight_histogram: tuple[tuple[int, int], ...]
    minimum_weight_leq6: int | None
    minimum_weight_multiplicity: int
    pair_syndrome_collision_buckets: int
    triple_syndrome_collision_buckets: int
    tanner_four_cycles: int
    singleton_weight3_columns: int
    pair_weight3_occurrences: int
    distinct_pair_weight3_atoms: int


@dataclass(frozen=True, slots=True)
class TDC2ERecovery:
    topology: TDC2EMetrics
    matched_random: TDC2EMetrics


def _digest(domain: bytes, seed: bytes, name: str, counter: int = 0) -> bytes:
    return hashlib.sha256(
        domain + b"\x00" + seed + name.encode("ascii") + counter.to_bytes(8, "big")
    ).digest()


def _mixed_columns(
    code: SparseFaceCode,
    rounds: int,
    seed: bytes,
    domain: bytes,
    name: str,
) -> tuple[tuple[int, ...], SparseMixingReference]:
    columns = list(code.columns)
    operations: list[tuple[int, int]] = []
    rejected = 0
    for round_index in range(rounds):
        targets = list(range(len(columns)))
        target_rng = _DeterministicRng(
            domain + b" target order",
            _digest(domain + b" targets", seed, name, round_index),
        )
        target_rng.shuffle(targets)
        for target in targets:
            sources = [index for index in range(len(columns)) if index != target]
            source_rng = _DeterministicRng(
                domain + b" source order",
                _digest(
                    domain + b" sources",
                    seed,
                    name,
                    round_index * len(columns) + target,
                ),
            )
            source_rng.shuffle(sources)
            selected: int | None = None
            for source in sources:
                candidate = columns[target] ^ columns[source]
                if candidate == 0:
                    rejected += 1
                    continue
                if any(
                    index != target and value == candidate
                    for index, value in enumerate(columns)
                ):
                    rejected += 1
                    continue
                selected = source
                columns[target] = candidate
                operations.append((source, target))
                break
            if selected is None:
                raise TDC2EError("TDC2e exhausted local source choices during mixing")
    if len(operations) != rounds * len(code.columns):
        raise TDC2EError("TDC2e did not complete the declared mixing budget")
    if any(value == 0 for value in columns) or len(set(columns)) != len(columns):
        raise TDC2EError("TDC2e mixing produced zero or duplicate columns")
    return tuple(columns), SparseMixingReference(tuple(operations), rejected)


def _public_relabel(
    code: SparseFaceCode,
    columns: tuple[int, ...],
    seed: bytes,
    domain: bytes,
    name: str,
) -> SparseFaceCode:
    row_map = list(range(code.row_count))
    col_order = list(range(len(columns)))
    row_rng = _DeterministicRng(
        domain + b" row relabel", _digest(domain + b" rows", seed, name)
    )
    col_rng = _DeterministicRng(
        domain + b" column relabel", _digest(domain + b" columns", seed, name)
    )
    row_rng.shuffle(row_map)
    col_rng.shuffle(col_order)
    relabeled: list[int] = []
    for old_col in col_order:
        old_mask = columns[old_col]
        new_mask = 0
        for old_row, new_row in enumerate(row_map):
            if (old_mask >> old_row) & 1:
                new_mask |= 1 << new_row
        relabeled.append(new_mask)
    return SparseFaceCode(name, code.row_count, tuple(relabeled))


def _mix_code(
    code: SparseFaceCode,
    rounds: int,
    seed: bytes,
    domain: bytes,
    name: str,
) -> SparseMixedCode:
    base_hist = tuple(sorted(Counter(column.bit_count() for column in code.columns).items()))
    mixed, reference = _mixed_columns(code, rounds, seed, domain, name)
    public = _public_relabel(code, mixed, seed, domain, name)
    return SparseMixedCode(public, reference, base_hist)


def generate_tdc2e_instance(
    params: TDC2EParameters,
    master_seed: bytes,
) -> TDC2EInstance:
    params.validate()
    if len(master_seed) < 16:
        raise TDC2EError("TDC2e seed must contain at least 128 bits")
    base = generate_tdc2_sparse_instance(
        TDC2_SPARSE_PARAMETER_SETS[params.base_name], master_seed
    )
    topology = _mix_code(
        base.topology_code,
        params.mixing_rounds,
        master_seed,
        b"MORPH-KEM TDC2e topology mixing v1",
        params.name + "-topology",
    )
    random = _mix_code(
        base.matched_random,
        params.mixing_rounds,
        master_seed,
        b"MORPH-KEM TDC2e random mixing v1",
        params.name + "-random",
    )
    return TDC2EInstance(topology, random)


def _tanner_four_cycles(code: SparseFaceCode) -> int:
    count = 0
    for left, right in combinations(code.columns, 2):
        common = (left & right).bit_count()
        if common >= 2:
            count += common * (common - 1) // 2
    return count


def _weight3_atom_metrics(code: SparseFaceCode) -> tuple[int, int, int]:
    singleton = sum(column.bit_count() == 3 for column in code.columns)
    occurrences = 0
    atoms: set[int] = set()
    for left, right in combinations(code.columns, 2):
        value = left ^ right
        if value.bit_count() == 3:
            occurrences += 1
            atoms.add(value)
    return singleton, occurrences, len(atoms)


def _metrics(mixed: SparseMixedCode) -> TDC2EMetrics:
    code = mixed.code
    rank = _gf2_rank(list(code.columns))
    minimum, multiplicity, pair_collisions, triple_collisions = _low_weight_leq6(
        code.columns
    )
    singleton, pair_occurrences, distinct_atoms = _weight3_atom_metrics(code)
    dimension = len(code.columns) - rank
    return TDC2EMetrics(
        rows=code.row_count,
        columns=len(code.columns),
        rank=rank,
        dimension=dimension,
        rate=dimension / len(code.columns),
        successful_mixing_operations=len(mixed.reference.operations),
        rejected_mixing_candidates=mixed.reference.rejected_candidates,
        base_column_weight_histogram=mixed.base_column_weight_histogram,
        public_row_weight_histogram=tuple(sorted(Counter(_row_degrees(code)).items())),
        public_column_weight_histogram=tuple(
            sorted(Counter(column.bit_count() for column in code.columns).items())
        ),
        minimum_weight_leq6=minimum,
        minimum_weight_multiplicity=multiplicity,
        pair_syndrome_collision_buckets=pair_collisions,
        triple_syndrome_collision_buckets=triple_collisions,
        tanner_four_cycles=_tanner_four_cycles(code),
        singleton_weight3_columns=singleton,
        pair_weight3_occurrences=pair_occurrences,
        distinct_pair_weight3_atoms=distinct_atoms,
    )


def recover_tdc2e(instance: TDC2EInstance) -> TDC2ERecovery:
    return TDC2ERecovery(
        topology=_metrics(instance.topology),
        matched_random=_metrics(instance.matched_random),
    )
