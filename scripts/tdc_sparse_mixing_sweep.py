from __future__ import annotations

import argparse
import hashlib

from morph_kem.tdc_sparse_mixing import (
    TDC2E_PARAMETER_SETS,
    generate_tdc2e_instance,
    recover_tdc2e,
)


def seed_for(name: str, index: int) -> bytes:
    return hashlib.sha256(
        f"MORPH-KEM TDC2e sweep {name} seed {index} v1".encode("ascii")
    ).digest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 16:
        raise SystemExit("--seeds must be between 1 and 16")

    print(
        "set,seed,kind,rows,cols,rank,dimension,rate,mixing_ops,rejected,"
        "min_le6,min_mult,pair_buckets,triple_buckets,four_cycles,"
        "singleton_w3,pair_w3,distinct_pair_w3,column_weights"
    )
    for params in TDC2E_PARAMETER_SETS.values():
        for index in range(args.seeds):
            instance = generate_tdc2e_instance(params, seed_for(params.name, index))
            recovery = recover_tdc2e(instance)
            for kind, result in (
                ("topology", recovery.topology),
                ("random", recovery.matched_random),
            ):
                print(
                    f"{params.name},{index},{kind},{result.rows},{result.columns},"
                    f"{result.rank},{result.dimension},{result.rate:.9f},"
                    f"{result.successful_mixing_operations},{result.rejected_mixing_candidates},"
                    f"{result.minimum_weight_leq6},{result.minimum_weight_multiplicity},"
                    f"{result.pair_syndrome_collision_buckets},{result.triple_syndrome_collision_buckets},"
                    f"{result.tanner_four_cycles},{result.singleton_weight3_columns},"
                    f"{result.pair_weight3_occurrences},{result.distinct_pair_weight3_atoms},"
                    f"\"{result.public_column_weight_histogram}\""
                )


if __name__ == "__main__":
    main()
