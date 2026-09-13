from __future__ import annotations

import argparse
import hashlib

from morph_kem.tdc_rank_matched import (
    TDC2F_PARAMETER_SETS,
    generate_tdc2f_instance,
    recover_tdc2f,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--params", choices=sorted(TDC2F_PARAMETER_SETS), default="tdc2f-n10"
    )
    args = parser.parse_args()
    params = TDC2F_PARAMETER_SETS[args.params]
    seed = hashlib.sha256(
        f"MORPH-KEM TDC2f fixed baseline {params.name} v1".encode("ascii")
    ).digest()
    instance = generate_tdc2f_instance(params, seed)
    recovery = recover_tdc2f(instance)

    print(f"parameters: {params.name}")
    print(f"target rank: {instance.target_rank}")
    print(f"rank profiles equal: {recovery.rank_profile_equal}")
    print(f"dimension profiles equal: {recovery.dimension_profile_equal}")
    for label, metrics in (
        ("topology", recovery.topology),
        ("random", recovery.matched_random),
    ):
        print(f"{label} rows/columns: {metrics.rows}/{metrics.columns}")
        print(
            f"{label} rank/dimension/rate: "
            f"{metrics.rank}/{metrics.dimension}/{metrics.rate:.6f}"
        )
        print(
            f"{label} row/column mixing operations: "
            f"{metrics.row_scramble_operations}/{metrics.column_mixing_operations}"
        )
        print(
            f"{label} rejected column-mixing candidates: "
            f"{metrics.rejected_column_mixing_candidates}"
        )
        print(
            f"{label} control generation attempts: "
            f"{metrics.control_generation_attempts}"
        )
        print(f"{label} row weights: {metrics.row_weight_histogram}")
        print(f"{label} column weights: {metrics.column_weight_histogram}")
        print(f"{label} minimum weight <=6: {metrics.minimum_weight_leq6}")
        print(f"{label} minimum-weight multiplicity: {metrics.minimum_weight_multiplicity}")
        print(f"{label} minimum weight <=8: {metrics.minimum_weight_leq8}")
        print(f"{label} <=8 witness support: {metrics.weight8_witness_support}")
        print(
            f"{label} <=8 triple/four subsets: "
            f"{metrics.triple_subsets_indexed}/{metrics.four_subsets_scanned}"
        )
        print(
            f"{label} <=8 collision candidates tested: "
            f"{metrics.collision_candidates_tested}"
        )
        print(
            f"{label} pair/triple collision buckets: "
            f"{metrics.pair_syndrome_collision_buckets}/"
            f"{metrics.triple_syndrome_collision_buckets}"
        )
        print(f"{label} Tanner 4-cycles: {metrics.tanner_four_cycles}")


if __name__ == "__main__":
    main()
