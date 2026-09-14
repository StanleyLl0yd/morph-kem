from __future__ import annotations

import argparse
import hashlib

from morph_kem.tdc_prange_isd import (
    TDC3B_PARAMETER_SETS,
    generate_tdc3b_instance,
    recover_tdc3b_weight,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(TDC3B_PARAMETER_SETS), default="tdc3b-n10")
    args = parser.parse_args()
    params = TDC3B_PARAMETER_SETS[args.params]
    seed = hashlib.sha256(
        f"MORPH-KEM TDC3b fixed baseline {params.name} v1".encode("ascii")
    ).digest()
    instance = generate_tdc3b_instance(params, seed)

    print(f"parameters: {params.name}")
    print(f"public rows/columns: {instance.pair.topology.row_count}/{len(instance.pair.topology.columns)}")
    print(f"trial budgets: {params.trial_budgets}")
    for weight in instance.params.error_weights:
        result = recover_tdc3b_weight(instance, weight)
        for label, recovery, matched in (
            ("topology", result.topology, result.topology_matches_planted_after_public_success),
            ("random", result.matched_random, result.random_matches_planted_after_public_success),
        ):
            print(
                f"weight={weight} {label}: accepted={recovery.accepted} "
                f"first_trial={recovery.first_success_trial} recovered_weight={recovery.recovered_weight} "
                f"budgets={recovery.success_by_budget} attempts={recovery.trials_attempted} "
                f"rank_deficient={recovery.rank_deficient_trials} candidates={recovery.candidate_solutions_tested} "
                f"row_xors={recovery.total_row_xors} pivot_scans={recovery.total_pivot_scans} "
                f"row_swaps={recovery.total_row_swaps} planted_match={matched}"
            )


if __name__ == "__main__":
    main()
