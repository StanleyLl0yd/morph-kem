from __future__ import annotations

import argparse
import hashlib

from morph_kem.tdc_random_overlay import (
    TDC2G_PARAMETER_SETS,
    generate_tdc2g_instance,
    recover_tdc2g,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(TDC2G_PARAMETER_SETS), default="tdc2g-n10")
    args = parser.parse_args()
    params = TDC2G_PARAMETER_SETS[args.params]
    seed = hashlib.sha256(
        f"MORPH-KEM TDC2g fixed baseline {params.name} v1".encode("ascii")
    ).digest()
    instance = generate_tdc2g_instance(params, seed)
    recovery = recover_tdc2g(instance)

    print(f"parameters: {params.name}")
    print(f"base/final rank: {recovery.base_rank}/{recovery.final_rank}")
    print(f"extra rows / overlay attempts: {recovery.extra_rows}/{recovery.overlay_attempts}")
    print(f"rank profiles equal: {recovery.rank_profile_equal}")
    print(f"dimension profiles equal: {recovery.dimension_profile_equal}")
    for label, metrics in (("topology", recovery.topology), ("random", recovery.matched_random)):
        print(f"{label} rows/columns: {metrics.rows}/{metrics.columns}")
        print(f"{label} rank/dimension/rate: {metrics.rank}/{metrics.dimension}/{metrics.rate:.6f}")
        print(f"{label} row weights: {metrics.row_weight_histogram}")
        print(f"{label} column weights: {metrics.column_weight_histogram}")
        print(f"{label} minimum weight <=6: {metrics.minimum_weight_leq6}")
        print(f"{label} minimum weight <=8: {metrics.minimum_weight_leq8}")
        print(f"{label} <=8 witness support: {metrics.weight8_witness_support}")
        print(f"{label} Tanner four-cycles: {metrics.tanner_four_cycles}")


if __name__ == "__main__":
    main()
