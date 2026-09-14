from __future__ import annotations

import argparse
import hashlib
from collections import defaultdict

from morph_kem.tdc_prange_isd import (
    TDC3B_PARAMETER_SETS,
    generate_tdc3b_instance,
    recover_tdc3b_weight,
)


def seed_for(name: str, index: int) -> bytes:
    return hashlib.sha256(
        f"MORPH-KEM TDC3b sweep {name} seed {index} v1".encode("ascii")
    ).digest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(TDC3B_PARAMETER_SETS), default=None)
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 32:
        raise SystemExit("--seeds must be in 1..32")

    params_list = (
        (TDC3B_PARAMETER_SETS[args.params],)
        if args.params is not None
        else tuple(TDC3B_PARAMETER_SETS.values())
    )
    print(
        "set,seed,weight,"
        "top_first,top_attempts,top_deficient,top_tested,top_xors,top_scans,top_swaps,top_match,"
        "rnd_first,rnd_attempts,rnd_deficient,rnd_tested,rnd_xors,rnd_scans,rnd_swaps,rnd_match"
    )
    budget_summary: dict[tuple[str, int, int], list[int]] = defaultdict(lambda: [0, 0, 0])
    work_summary: dict[str, list[int]] = defaultdict(lambda: [0] * 13)

    for params in params_list:
        for index in range(args.seeds):
            instance = generate_tdc3b_instance(params, seed_for(params.name, index))
            for weight in instance.params.error_weights:
                result = recover_tdc3b_weight(instance, weight)
                print(
                    f"{params.name},{index},{weight},"
                    f"{result.topology.first_success_trial or 0},{result.topology.trials_attempted},"
                    f"{result.topology.rank_deficient_trials},{result.topology.candidate_solutions_tested},"
                    f"{result.topology.total_row_xors},{result.topology.total_pivot_scans},"
                    f"{result.topology.total_row_swaps},{int(result.topology_matches_planted_after_public_success)},"
                    f"{result.matched_random.first_success_trial or 0},{result.matched_random.trials_attempted},"
                    f"{result.matched_random.rank_deficient_trials},{result.matched_random.candidate_solutions_tested},"
                    f"{result.matched_random.total_row_xors},{result.matched_random.total_pivot_scans},"
                    f"{result.matched_random.total_row_swaps},{int(result.random_matches_planted_after_public_success)}"
                )
                top_budgets = dict(result.topology.success_by_budget)
                rnd_budgets = dict(result.matched_random.success_by_budget)
                for budget in params.trial_budgets:
                    row = budget_summary[(params.name, weight, budget)]
                    row[0] += int(top_budgets[budget])
                    row[1] += int(rnd_budgets[budget])
                    row[2] += 1

                work = work_summary[params.name]
                work[0] += result.topology.trials_attempted
                work[1] += result.matched_random.trials_attempted
                work[2] += result.topology.rank_deficient_trials
                work[3] += result.matched_random.rank_deficient_trials
                work[4] += result.topology.candidate_solutions_tested
                work[5] += result.matched_random.candidate_solutions_tested
                work[6] += result.topology.total_row_xors
                work[7] += result.matched_random.total_row_xors
                work[8] += result.topology.total_pivot_scans
                work[9] += result.matched_random.total_pivot_scans
                work[10] += result.topology.total_row_swaps
                work[11] += result.matched_random.total_row_swaps
                work[12] += 1

    print("summary,set,weight,budget,top_success,rnd_success,delta,cases")
    for (name, weight, budget), row in sorted(budget_summary.items()):
        print(
            f"summary,{name},{weight},{budget},{row[0]},{row[1]},{row[0]-row[1]},{row[2]}"
        )

    print(
        "work,set,"
        "top_attempts,rnd_attempts,attempt_delta,"
        "top_deficient,rnd_deficient,deficient_delta,"
        "top_tested,rnd_tested,tested_delta,"
        "top_row_xors,rnd_row_xors,xor_delta,"
        "top_pivot_scans,rnd_pivot_scans,scan_delta,"
        "top_row_swaps,rnd_row_swaps,swap_delta,cases"
    )
    for name, row in sorted(work_summary.items()):
        print(
            f"work,{name},"
            f"{row[0]},{row[1]},{row[0]-row[1]},"
            f"{row[2]},{row[3]},{row[2]-row[3]},"
            f"{row[4]},{row[5]},{row[4]-row[5]},"
            f"{row[6]},{row[7]},{row[6]-row[7]},"
            f"{row[8]},{row[9]},{row[8]-row[9]},"
            f"{row[10]},{row[11]},{row[10]-row[11]},{row[12]}"
        )


if __name__ == "__main__":
    main()
