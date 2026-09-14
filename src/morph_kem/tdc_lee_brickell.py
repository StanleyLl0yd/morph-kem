from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from .tdc_cycle_code import _gf2_rank
from .tdc_decoder_work import (
    TDC3Instance,
    TDC3_PARAMETER_SETS,
    generate_tdc3_instance,
    planted_error_mask,
    syndrome,
)
from .tdc_prange_isd import information_set
from .tdc_sparse_faces import SparseFaceCode


class TDC3CError(ValueError):
    """Raised when a TDC3c Lee-Brickell experiment is malformed."""


@dataclass(frozen=True, slots=True)
class TDC3CParameters:
    name: str
    base_name: str
    trial_budgets: tuple[int, ...] = (1, 4, 16)
    outside_orders: tuple[int, ...] = (0, 1, 2)

    def validate(self) -> None:
        if self.base_name not in TDC3_PARAMETER_SETS:
            raise TDC3CError("unknown TDC3 base parameter set")
        if self.trial_budgets != (1, 4, 16):
            raise TDC3CError("TDC3c fixes trial budgets at 1/4/16")
        if self.outside_orders != (0, 1, 2):
            raise TDC3CError("TDC3c fixes outside orders at 0/1/2")


TDC3C_PARAMETER_SETS = {
    "tdc3c-n8": TDC3CParameters("tdc3c-n8", "tdc3-n8"),
    "tdc3c-n9": TDC3CParameters("tdc3c-n9", "tdc3-n9"),
    "tdc3c-n10": TDC3CParameters("tdc3c-n10", "tdc3-n10"),
}


@dataclass(frozen=True, slots=True)
class BasisCoordinateMap:
    full_rank: bool
    inverse_rows: tuple[int, ...]
    row_xors: int
    pivot_scans: int
    row_swaps: int


@dataclass(frozen=True, slots=True)
class WorkCheckpoint:
    budget: int
    trials_attempted: int
    rank_deficient_trials: int
    full_rank_maps: int
    row_xors: int
    pivot_scans: int
    row_swaps: int
    outside0_subsets: int
    outside1_subsets: int
    outside2_subsets: int
    candidate_weight_tests: int
    verifier_calls: int


@dataclass(frozen=True, slots=True)
class LeeBrickellRecovery:
    accepted: bool
    recovered_error_mask: int
    recovered_weight: int
    first_success_trial: int | None
    first_success_outside_order: int | None
    first_success_work: WorkCheckpoint | None
    first_exact_order_trials: tuple[tuple[int, int | None], ...]
    success_grid: tuple[tuple[int, int, bool], ...]
    work_by_budget: tuple[WorkCheckpoint, ...]


@dataclass(frozen=True, slots=True)
class LeeBrickellPairRecovery:
    planted_weight: int
    topology: LeeBrickellRecovery
    matched_random: LeeBrickellRecovery
    topology_matches_planted_after_public_success: bool
    random_matches_planted_after_public_success: bool


def _require_full_row_rank(code: SparseFaceCode) -> int:
    rank = _gf2_rank(list(code.columns))
    if rank != code.row_count:
        raise TDC3CError("TDC3c requires the fixed full-row-rank public ensemble")
    if rank > len(code.columns):
        raise TDC3CError("TDC3c code has fewer columns than rank")
    return rank


def generate_tdc3c_instance(params: TDC3CParameters, master_seed: bytes) -> TDC3Instance:
    params.validate()
    instance = generate_tdc3_instance(TDC3_PARAMETER_SETS[params.base_name], master_seed)
    _require_full_row_rank(instance.pair.topology)
    _require_full_row_rank(instance.pair.matched_random)
    return instance


def build_basis_coordinate_map(
    code: SparseFaceCode,
    selected: tuple[int, ...],
) -> BasisCoordinateMap:
    rank = _require_full_row_rank(code)
    if len(selected) != rank or len(set(selected)) != rank:
        raise TDC3CError("TDC3c information set has wrong size")

    # Low r bits are the selected-column coefficient matrix M. High r bits
    # start as I. Gauss-Jordan row operations produce [I | M^-1].
    rows: list[int] = []
    for equation in range(rank):
        left = 0
        for local_index, column_index in enumerate(selected):
            if (code.columns[column_index] >> equation) & 1:
                left |= 1 << local_index
        rows.append(left | (1 << (rank + equation)))

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
            return BasisCoordinateMap(False, (), row_xors, pivot_scans, row_swaps)
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

    left_mask = (1 << rank) - 1
    for row_index, row in enumerate(rows):
        if row & left_mask != 1 << row_index:
            raise TDC3CError("TDC3c Gauss-Jordan map did not reduce to identity")
    inverse_rows = tuple((row >> rank) & left_mask for row in rows)
    return BasisCoordinateMap(True, inverse_rows, row_xors, pivot_scans, row_swaps)


def solve_with_basis_map(inverse_rows: tuple[int, ...], target_syndrome: int) -> int:
    local = 0
    for output_index, inverse_row in enumerate(inverse_rows):
        if (inverse_row & target_syndrome).bit_count() & 1:
            local |= 1 << output_index
    return local


def _expand_solution(selected: tuple[int, ...], local_mask: int) -> int:
    result = 0
    for local_index, column_index in enumerate(selected):
        if (local_mask >> local_index) & 1:
            result |= 1 << column_index
    return result


def _checkpoint(
    budget: int,
    deficient: int,
    full_rank_maps: int,
    row_xors: int,
    pivot_scans: int,
    row_swaps: int,
    outside_counts: list[int],
    weight_tests: int,
    verifier_calls: int,
) -> WorkCheckpoint:
    return WorkCheckpoint(
        budget=budget,
        trials_attempted=budget,
        rank_deficient_trials=deficient,
        full_rank_maps=full_rank_maps,
        row_xors=row_xors,
        pivot_scans=pivot_scans,
        row_swaps=row_swaps,
        outside0_subsets=outside_counts[0],
        outside1_subsets=outside_counts[1],
        outside2_subsets=outside_counts[2],
        candidate_weight_tests=weight_tests,
        verifier_calls=verifier_calls,
    )


def lee_brickell_decode(
    code: SparseFaceCode,
    target_syndrome: int,
    max_weight: int,
    trial_budgets: tuple[int, ...] = (1, 4, 16),
    outside_orders: tuple[int, ...] = (0, 1, 2),
) -> LeeBrickellRecovery:
    if max_weight < 1:
        raise TDC3CError("TDC3c max weight must be positive")
    if trial_budgets != (1, 4, 16):
        raise TDC3CError("TDC3c decoder requires fixed 1/4/16 trial budgets")
    if outside_orders != (0, 1, 2):
        raise TDC3CError("TDC3c decoder requires fixed outside orders 0/1/2")
    _require_full_row_rank(code)

    maximum = trial_budgets[-1]
    deficient = 0
    full_rank_maps = 0
    row_xors = 0
    pivot_scans = 0
    row_swaps = 0
    outside_counts = [0, 0, 0]
    weight_tests = 0
    verifier_calls = 0
    first_exact: list[int | None] = [None, None, None]
    first_key: tuple[int, int, tuple[int, ...]] | None = None
    recovered = 0
    first_work: WorkCheckpoint | None = None
    work_by_budget: list[WorkCheckpoint] = []

    for trial_index in range(maximum):
        trial_number = trial_index + 1
        selected = information_set(code, target_syndrome, trial_index)
        selected_set = set(selected)
        outside = tuple(index for index in range(len(code.columns)) if index not in selected_set)
        basis = build_basis_coordinate_map(code, selected)
        row_xors += basis.row_xors
        pivot_scans += basis.pivot_scans
        row_swaps += basis.row_swaps

        if not basis.full_rank:
            deficient += 1
        else:
            full_rank_maps += 1
            target_local = solve_with_basis_map(basis.inverse_rows, target_syndrome)
            outside_local = {
                index: solve_with_basis_map(basis.inverse_rows, code.columns[index])
                for index in outside
            }

            for exact_order in outside_orders:
                if exact_order > max_weight:
                    continue
                for subset in combinations(outside, exact_order):
                    outside_counts[exact_order] += 1
                    weight_tests += 1
                    local = target_local
                    outside_mask = 0
                    for column_index in subset:
                        local ^= outside_local[column_index]
                        outside_mask |= 1 << column_index
                    candidate = _expand_solution(selected, local) | outside_mask
                    if candidate.bit_count() > max_weight:
                        continue
                    verifier_calls += 1
                    if syndrome(code, candidate) != target_syndrome:
                        raise TDC3CError("TDC3c basis completion failed exact syndrome verification")
                    if first_exact[exact_order] is None:
                        first_exact[exact_order] = trial_number
                    key = (trial_number, exact_order, subset)
                    if first_key is None or key < first_key:
                        first_key = key
                        recovered = candidate
                        first_work = _checkpoint(
                            trial_number,
                            deficient,
                            full_rank_maps,
                            row_xors,
                            pivot_scans,
                            row_swaps,
                            outside_counts,
                            weight_tests,
                            verifier_calls,
                        )

        if trial_number in trial_budgets:
            work_by_budget.append(
                _checkpoint(
                    trial_number,
                    deficient,
                    full_rank_maps,
                    row_xors,
                    pivot_scans,
                    row_swaps,
                    outside_counts,
                    weight_tests,
                    verifier_calls,
                )
            )

    success_grid: list[tuple[int, int, bool]] = []
    for max_order in outside_orders:
        candidate_trials = [
            trial for trial in first_exact[: max_order + 1] if trial is not None
        ]
        first_cumulative = min(candidate_trials) if candidate_trials else None
        for budget in trial_budgets:
            success_grid.append(
                (max_order, budget, first_cumulative is not None and first_cumulative <= budget)
            )

    accepted = first_key is not None
    return LeeBrickellRecovery(
        accepted=accepted,
        recovered_error_mask=recovered,
        recovered_weight=recovered.bit_count() if accepted else 0,
        first_success_trial=first_key[0] if first_key is not None else None,
        first_success_outside_order=first_key[1] if first_key is not None else None,
        first_success_work=first_work,
        first_exact_order_trials=tuple((order, first_exact[order]) for order in outside_orders),
        success_grid=tuple(success_grid),
        work_by_budget=tuple(work_by_budget),
    )


def recover_tdc3c_weight(instance: TDC3Instance, weight: int) -> LeeBrickellPairRecovery:
    planted = planted_error_mask(instance, weight)
    top_target = syndrome(instance.pair.topology, planted)
    rnd_target = syndrome(instance.pair.matched_random, planted)
    top = lee_brickell_decode(instance.pair.topology, top_target, weight)
    rnd = lee_brickell_decode(instance.pair.matched_random, rnd_target, weight)
    return LeeBrickellPairRecovery(
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
