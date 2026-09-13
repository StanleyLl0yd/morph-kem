from __future__ import annotations

import argparse
import hashlib

from morph_kem.tdc_rank_matched import (
    TDC2F_PARAMETER_SETS,
    generate_tdc2f_instance,
    recover_tdc2f,
)


def seed_for(name: str, index: int) -> bytes:
    return hashlib.sha256(
        f"MORPH-KEM TDC2f sweep {name} seed {index} v1".encode("ascii")
    ).digest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 64:
        raise SystemExit("--seeds must be in 1..64")

    print(
        "set,seed,kind,rows,cols,rank,dimension,rate,row_ops,col_ops,rejected,"
        "control_attempts,min_le6,min_mult,min_le8,witness8,triple_indexed,four_scanned,"
        "collision_checks,pair_buckets,triple_buckets,four_cycles,rank_equal,"
        "dimension_equal,column_weights"
    )
    for params in TDC2F_PARAMETER_SETS.values():
        for index in range(args.seeds):
            instance = generate_tdc2f_instance(params, seed_for(params.name, index))
            recovery = recover_tdc2f(instance)
            for kind, metrics in (
                ("topology", recovery.topology),
                ("random", recovery.matched_random),
            ):
                support = "-".join(str(value) for value in metrics.weight8_witness_support)
                print(
                    f"{params.name},{index},{kind},{metrics.rows},{metrics.columns},"
                    f"{metrics.rank},{metrics.dimension},{metrics.rate:.9f},"
                    f"{metrics.row_scramble_operations},{metrics.column_mixing_operations},"
                    f"{metrics.rejected_column_mixing_candidates},"
                    f"{metrics.control_generation_attempts},{metrics.minimum_weight_leq6},"
                    f"{metrics.minimum_weight_multiplicity},{metrics.minimum_weight_leq8},"
                    f'"{support}",{metrics.triple_subsets_indexed},'
                    f"{metrics.four_subsets_scanned},{metrics.collision_candidates_tested},"
                    f"{metrics.pair_syndrome_collision_buckets},"
                    f"{metrics.triple_syndrome_collision_buckets},"
                    f"{metrics.tanner_four_cycles},"
                    f"{int(recovery.rank_profile_equal)},"
                    f"{int(recovery.dimension_profile_equal)},"
                    f'"{metrics.column_weight_histogram}"'
                )


if __name__ == "__main__":
    main()
