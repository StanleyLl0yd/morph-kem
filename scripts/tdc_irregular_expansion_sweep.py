from __future__ import annotations

import argparse
import hashlib

from morph_kem.tdc_irregular_expansion import (
    TDC2D_PARAMETER_SETS,
    generate_tdc2d_instance,
    recover_tdc2d,
)


def seed_for(name: str, index: int) -> bytes:
    return hashlib.sha256(
        f"MORPH-KEM TDC2d sweep {name} seed {index} v1".encode("ascii")
    ).digest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 16:
        raise SystemExit("--seeds must be between 1 and 16")

    print(
        "set,seed,kind,rows,cols,color_rounds,singletons,max_class,exact_row_fibers,total_row_fibers,"
        "exact_col_fibers,total_col_fibers,min_le6,min_mult,pair_buckets,triple_buckets,row_mults,class_sizes"
    )
    for params in TDC2D_PARAMETER_SETS.values():
        for index in range(args.seeds):
            recovery = recover_tdc2d(
                generate_tdc2d_instance(params, seed_for(params.name, index))
            )
            for kind, metrics in (
                ("topology", recovery.topology),
                ("random", recovery.matched_random),
            ):
                print(
                    f"{params.name},{index},{kind},{metrics.rows},{metrics.columns},"
                    f"{metrics.color_rounds},{metrics.singleton_color_classes},{metrics.maximum_color_class_size},"
                    f"{metrics.exact_row_fibers_recovered_by_color},{metrics.total_row_fibers},"
                    f"{metrics.exact_column_fibers_recovered_by_color},{metrics.total_column_fibers},"
                    f"{metrics.minimum_weight_leq6},{metrics.minimum_weight_multiplicity},"
                    f"{metrics.pair_syndrome_collision_buckets},{metrics.triple_syndrome_collision_buckets},"
                    f"\"{metrics.row_multiplicity_histogram}\",\"{metrics.color_class_size_histogram}\""
                )


if __name__ == "__main__":
    main()
