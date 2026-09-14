from __future__ import annotations

import argparse
import hashlib
from collections import defaultdict

from morph_kem.tdc_lee_brickell import (
    TDC3C_PARAMETER_SETS,
    generate_tdc3c_instance,
    recover_tdc3c_weight,
)


def seed_for(name: str, index: int) -> bytes:
    return hashlib.sha256(
        f"MORPH-KEM TDC3c sweep {name} seed {index} v1".encode("ascii")
    ).digest()


def blank_work() -> dict[str, int]:
    return {
        "cases": 0,
        "trials": 0,
        "deficient": 0,
        "maps": 0,
        "xors": 0,
        "scans": 0,
        "swaps": 0,
        "o0": 0,
        "o1": 0,
        "o2": 0,
        "tests": 0,
        "verifier": 0,
    }


def add_checkpoint(row: dict[str, int], cp) -> None:
    row["cases"] += 1
    row["trials"] += cp.trials_attempted
    row["deficient"] += cp.rank_deficient_trials
    row["maps"] += cp.full_rank_maps
    row["xors"] += cp.row_xors
    row["scans"] += cp.pivot_scans
    row["swaps"] += cp.row_swaps
    row["o0"] += cp.outside0_subsets
    row["o1"] += cp.outside1_subsets
    row["o2"] += cp.outside2_subsets
    row["tests"] += cp.candidate_weight_tests
    row["verifier"] += cp.verifier_calls


def add_pair(row: list[int], top_ok: bool, rnd_ok: bool) -> None:
    # top-only, control-only, both, neither
    if top_ok and not rnd_ok:
        row[0] += 1
    elif rnd_ok and not top_ok:
        row[1] += 1
    elif top_ok and rnd_ok:
        row[2] += 1
    else:
        row[3] += 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(TDC3C_PARAMETER_SETS), required=True)
    parser.add_argument("--seeds", type=int, required=True)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 32:
        raise SystemExit("--seeds must be in 1..32")

    params = TDC3C_PARAMETER_SETS[args.params]
    success: dict[tuple[int, int, int], list[int]] = defaultdict(lambda: [0, 0, 0])
    paired: dict[tuple[int, int, int], list[int]] = defaultdict(lambda: [0, 0, 0, 0])
    paired_all_weights: dict[tuple[int, int], list[int]] = defaultdict(lambda: [0, 0, 0, 0])
    work_top = {budget: blank_work() for budget in params.trial_budgets}
    work_rnd = {budget: blank_work() for budget in params.trial_budgets}
    first_work: dict[int, list[int]] = defaultdict(lambda: [0, 0, 0, 0, 0, 0])
    strongest: dict[int, list[int]] = defaultdict(lambda: [0, 0, 0, 0, 0])

    print(
        "set,seed,weight,top_ok,top_first,top_order,top_weight,top_match,"
        "rnd_ok,rnd_first,rnd_order,rnd_weight,rnd_match"
    )

    for seed_index in range(args.seeds):
        instance = generate_tdc3c_instance(params, seed_for(params.name, seed_index))
        for weight in instance.params.error_weights:
            result = recover_tdc3c_weight(instance, weight)
            top = result.topology
            rnd = result.matched_random
            print(
                f"{params.name},{seed_index},{weight},{int(top.accepted)},"
                f"{top.first_success_trial or 0},{top.first_success_outside_order if top.first_success_outside_order is not None else -1},"
                f"{top.recovered_weight},{int(result.topology_matches_planted_after_public_success)},"
                f"{int(rnd.accepted)},{rnd.first_success_trial or 0},"
                f"{rnd.first_success_outside_order if rnd.first_success_outside_order is not None else -1},"
                f"{rnd.recovered_weight},{int(result.random_matches_planted_after_public_success)}"
            )

            top_grid = {(order, budget): ok for order, budget, ok in top.success_grid}
            rnd_grid = {(order, budget): ok for order, budget, ok in rnd.success_grid}
            for order in params.outside_orders:
                for budget in params.trial_budgets:
                    top_ok = top_grid[(order, budget)]
                    rnd_ok = rnd_grid[(order, budget)]
                    row = success[(weight, order, budget)]
                    row[0] += int(top_ok)
                    row[1] += int(rnd_ok)
                    row[2] += 1
                    add_pair(paired[(weight, order, budget)], top_ok, rnd_ok)
                    add_pair(paired_all_weights[(order, budget)], top_ok, rnd_ok)

            for cp in top.work_by_budget:
                add_checkpoint(work_top[cp.budget], cp)
            for cp in rnd.work_by_budget:
                add_checkpoint(work_rnd[cp.budget], cp)

            strongest_row = strongest[weight]
            strongest_row[0] += int(top.accepted)
            strongest_row[1] += int(rnd.accepted)
            strongest_row[2] += int(result.topology_matches_planted_after_public_success)
            strongest_row[3] += int(result.random_matches_planted_after_public_success)
            strongest_row[4] += 1

            fw = first_work[weight]
            if top.first_success_work is not None:
                fw[0] += 1
                fw[2] += top.first_success_work.trials_attempted
                fw[4] += top.first_success_work.row_xors
            if rnd.first_success_work is not None:
                fw[1] += 1
                fw[3] += rnd.first_success_work.trials_attempted
                fw[5] += rnd.first_success_work.row_xors

    print("summary,set,weight,max_order,budget,top_success,rnd_success,delta,cases")
    for (weight, order, budget), row in sorted(success.items()):
        print(
            f"summary,{params.name},{weight},{order},{budget},{row[0]},{row[1]},"
            f"{row[0]-row[1]},{row[2]}"
        )

    print("paired,set,weight,max_order,budget,top_only,control_only,both,neither,discordant_delta")
    for (weight, order, budget), row in sorted(paired.items()):
        print(
            f"paired,{params.name},{weight},{order},{budget},{row[0]},{row[1]},"
            f"{row[2]},{row[3]},{row[0]-row[1]}"
        )

    print("paired_all,set,max_order,budget,top_only,control_only,both,neither,discordant_delta,cases")
    for (order, budget), row in sorted(paired_all_weights.items()):
        print(
            f"paired_all,{params.name},{order},{budget},{row[0]},{row[1]},"
            f"{row[2]},{row[3]},{row[0]-row[1]},{sum(row)}"
        )

    print("strongest,set,weight,top_ok,rnd_ok,top_planted,rnd_planted,cases")
    for weight, row in sorted(strongest.items()):
        print(
            f"strongest,{params.name},{weight},{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}"
        )

    print("firstwork,set,weight,top_ok,rnd_ok,top_trials,rnd_trials,top_xors,rnd_xors")
    for weight, row in sorted(first_work.items()):
        print(
            f"firstwork,{params.name},{weight},{row[0]},{row[1]},{row[2]},{row[3]},"
            f"{row[4]},{row[5]}"
        )

    print(
        "work,set,budget,family,cases,trials,deficient,maps,row_xors,pivot_scans,row_swaps,"
        "outside0,outside1,outside2,weight_tests,verifier_calls"
    )
    for budget in params.trial_budgets:
        for family, row in (("topology", work_top[budget]), ("control", work_rnd[budget])):
            print(
                f"work,{params.name},{budget},{family},{row['cases']},{row['trials']},"
                f"{row['deficient']},{row['maps']},{row['xors']},{row['scans']},{row['swaps']},"
                f"{row['o0']},{row['o1']},{row['o2']},{row['tests']},{row['verifier']}"
            )


if __name__ == "__main__":
    main()
