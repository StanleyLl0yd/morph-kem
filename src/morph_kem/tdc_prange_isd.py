from __future__ import annotations

from dataclasses import dataclass
import hashlib

from .tdc_decoder_work import (
    TDC3Instance,
    TDC3_PARAMETER_SETS,
    generate_tdc3_instance,
    planted_error_mask,
    syndrome,
)
from .tdc_sparse_faces import SparseFaceCode


class TDC3BError(ValueError):
    """Raised when a TDC3b bounded ISD experiment is malformed."""


@dataclass(frozen=True, slots=True)
class TDC3BParameters:
    name: str
    base_name: str
    trial_budgets: tuple[int, ...] = (8, 32, 128)

    def validate(self) -> None:
        if self.base_name not in TDC3_PARAMETER_SETS:
            raise TDC3BError("unknown TDC3 base parameter set")
        if self.trial_budgets != (8, 32, 128):
            raise TDC3BError("TDC3b fixes trial budgets at 8/32/128")


TDC3B_PARAMETER_SETS = {
    "tdc3b-n8": TDC3BParameters("tdc3b-n8", "tdc3-n8"),
    "tdc3b-n9": TDC3BParameters("tdc3b-n9", "tdc3-n9"),
    "tdc3b-n10": TDC3BParameters("tdc3b-n10", "tdc3-n10"),
}


@dataclass(frozen=True, slots=True)
class LinearSolveResult:
    full_rank: bool
    local_solution_mask: int
    row_xors: int
    pivot_scans: int
    row_swaps: int


@dataclass(frozen=True, slots=True)
class PrangeRecovery:
    accepted: bool
    recovered_error_mask: int
    recovered_weight: int
    first_success_trial: int | None
    trials_attempted: int
    rank_deficient_trials: int
    candidate_solutions_tested: int
    total_row_xors: int
    total_pivot_scans: int
    total_row_swaps: int
    success_by_budget: tuple[tuple[int, bool], ...]


@dataclass(frozen=True, slots=True)
class PrangePairRecovery:
    planted_weight: int
    topology: PrangeRecovery
    matched_random: PrangeRecovery
    topology_matches_planted_after_public_success: bool
    random_matches_planted_after_public_success: bool


def generate_tdc3b_instance(params: TDC3BParameters, master_seed: bytes) -> TDC3Instance:
    params.validate()
    return generate_tdc3_instance(TDC3_PARAMETER_SETS[params.base_name], master_seed)


def _code_digest(code: SparseFaceCode) -> bytes:
    width = max(1, (code.row_count + 7) // 8)
    digest = hashlib.sha256()
    digest.update(b"MORPH-KEM TDC3b public code v1\x00")
    digest.update(code.row_count.to_bytes(4, "big"))
    digest.update(len(code.columns).to_bytes(4, "big"))
    for column in code.columns:
        digest.update(column.to_bytes(width, "big"))
    return digest.digest()


def information_set(
    code: SparseFaceCode,
    target_syndrome: int,
    trial_index: int,
) -> tuple[int, ...]:
    if trial_index < 0:
        raise TDC3BError("TDC3b trial index must be nonnegative")
    if code.row_count > len(code.columns):
        raise TDC3BError("TDC3b code has fewer columns than rows")
    code_hash = _code_digest(code)
    syndrome_width = max(1, (code.row_count + 7) // 8)
    syndrome_bytes = target_syndrome.to_bytes(syndrome_width, "big")
    ranked = []
    for index in range(len(code.columns)):
        score = hashlib.sha256(
            b"MORPH-KEM TDC3b information set v1\x00"
            + code_hash
            + syndrome_bytes
            + trial_index.to_bytes(8, "big")
            + index.to_bytes(4, "big")
        ).digest()
        ranked.append((score, index))
    ranked.sort()
    return tuple(index for _, index in ranked[: code.row_count])


def solve_information_set(
    code: SparseFaceCode,
    selected: tuple[int, ...],
    target_syndrome: int,
) -> LinearSolveResult:
    rank = code.row_count
    if len(selected) != rank or len(set(selected)) != rank:
        raise TDC3BError("TDC3b information set has wrong size")

    rhs_bit = 1 << rank
    rows: list[int] = []
    for equation in range(rank):
        row_mask = 0
        for local_index, column_index in enumerate(selected):
            if (code.columns[column_index] >> equation) & 1:
                row_mask |= 1 << local_index
        if (target_syndrome >> equation) & 1:
            row_mask |= rhs_bit
        rows.append(row_mask)

    row_xors = 0
    pivot_scans = 0
    row_swaps = 0
    for pivot_column in range(rank):
        pivot_row = None
        for row_index in range(pivot_column, rank):
            pivot_scans += 1
            if (rows[row_index] >> pivot_column) & 1:
                pivot_row = row_index
                break
        if pivot_row is None:
            return LinearSolveResult(False, 0, row_xors, pivot_scans, row_swaps)
        if pivot_row != pivot_column:
            rows[pivot_column], rows[pivot_row] = rows[pivot_row], rows[pivot_column]
            row_swaps += 1

        pivot = rows[pivot_column]
        for row_index in range(rank):
            if row_index == pivot_column:
                continue
            if (rows[row_index] >> pivot_column) & 1:
                rows[row_index] ^= pivot
                row_xors += 1

    local_solution = 0
    for row_index in range(rank):
        if (rows[row_index] >> rank) & 1:
            local_solution |= 1 << row_index
    return LinearSolveResult(True, local_solution, row_xors, pivot_scans, row_swaps)


def _expand_solution(selected: tuple[int, ...], local_mask: int) -> int:
    result = 0
    for local_index, column_index in enumerate(selected):
        if (local_mask >> local_index) & 1:
            result |= 1 << column_index
    return result


def prange_decode(
    code: SparseFaceCode,
    target_syndrome: int,
    max_weight: int,
    trial_budgets: tuple[int, ...] = (8, 32, 128),
) -> PrangeRecovery:
    if max_weight < 1:
        raise TDC3BError("TDC3b max weight must be positive")
    if trial_budgets != (8, 32, 128):
        raise TDC3BError("TDC3b decoder requires fixed 8/32/128 budgets")

    maximum = trial_budgets[-1]
    deficient = 0
    tested = 0
    row_xors = 0
    pivot_scans = 0
    row_swaps = 0
    first_success = None
    recovered = 0
    attempted = 0

    for trial in range(maximum):
        attempted = trial + 1
        selected = information_set(code, target_syndrome, trial)
        solved = solve_information_set(code, selected, target_syndrome)
        row_xors += solved.row_xors
        pivot_scans += solved.pivot_scans
        row_swaps += solved.row_swaps
        if not solved.full_rank:
            deficient += 1
            continue
        candidate = _expand_solution(selected, solved.local_solution_mask)
        tested += 1
        if candidate.bit_count() > max_weight:
            continue
        if syndrome(code, candidate) != target_syndrome:
            raise TDC3BError("TDC3b information-set solve failed verification")
        first_success = trial + 1
        recovered = candidate
        break

    success_by_budget = tuple(
        (budget, first_success is not None and first_success <= budget)
        for budget in trial_budgets
    )
    return PrangeRecovery(
        accepted=first_success is not None,
        recovered_error_mask=recovered,
        recovered_weight=recovered.bit_count() if first_success is not None else 0,
        first_success_trial=first_success,
        trials_attempted=attempted,
        rank_deficient_trials=deficient,
        candidate_solutions_tested=tested,
        total_row_xors=row_xors,
        total_pivot_scans=pivot_scans,
        total_row_swaps=row_swaps,
        success_by_budget=success_by_budget,
    )


def recover_tdc3b_weight(
    instance: TDC3Instance,
    weight: int,
) -> PrangePairRecovery:
    planted = planted_error_mask(instance, weight)
    top_target = syndrome(instance.pair.topology, planted)
    rnd_target = syndrome(instance.pair.matched_random, planted)
    top = prange_decode(instance.pair.topology, top_target, weight)
    rnd = prange_decode(instance.pair.matched_random, rnd_target, weight)
    return PrangePairRecovery(
        planted_weight=weight,
        topology=top,
        matched_random=rnd,
        topology_matches_planted_after_public_success=(
            top.accepted and top.recovered_error_mask == planted
        ),
        random_matches_planted_after_public_success=(
            rnd.accepted and rnd.recovered_error_mask == planted
        ),
    )
