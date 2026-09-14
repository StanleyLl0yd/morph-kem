from __future__ import annotations

import argparse
import hashlib

from morph_kem.tdc_lee_brickell import (
    TDC3C_PARAMETER_SETS,
    generate_tdc3c_instance,
    recover_tdc3c_weight,
)


def seed_for(name: str) -> bytes:
    return hashlib.sha256(
        f"MORPH-KEM TDC3c baseline {name} v1".encode("ascii")
    ).digest()


def describe(label: str, recovery, planted_match: bool) -> None:
    print(
        f"{label}: accepted={recovery.accepted} first_trial={recovery.first_success_trial} "
        f"outside_order={recovery.first_success_outside_order} "
        f"recovered_weight={recovery.recovered_weight} planted_match={planted_match}"
    )
    print(f"{label} first exact-order trials: {recovery.first_exact_order_trials}")
    print(f"{label} success grid: {recovery.success_grid}")
    if recovery.first_success_work is not None:
        print(f"{label} work to first strongest success: {recovery.first_success_work}")
    print(f"{label} fixed-budget work: {recovery.work_by_budget}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--params", choices=sorted(TDC3C_PARAMETER_SETS), default="tdc3c-n10"
    )
    args = parser.parse_args()

    params = TDC3C_PARAMETER_SETS[args.params]
    instance = generate_tdc3c_instance(params, seed_for(params.name))
    print(f"parameters: {params.name}")
    print(f"trial budgets: {params.trial_budgets}")
    print(f"outside orders: {params.outside_orders}")
    print(
        "public rows/columns: "
        f"{instance.pair.topology.row_count}/{len(instance.pair.topology.columns)}"
    )

    for weight in instance.params.error_weights:
        result = recover_tdc3c_weight(instance, weight)
        print(f"weight={weight}")
        describe(
            "  topology",
            result.topology,
            result.topology_matches_planted_after_public_success,
        )
        describe(
            "  random",
            result.matched_random,
            result.random_matches_planted_after_public_success,
        )


if __name__ == "__main__":
    main()
