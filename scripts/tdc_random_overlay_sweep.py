from __future__ import annotations

import argparse
import hashlib

from morph_kem.tdc_random_overlay import (
    TDC2G_PARAMETER_SETS,
    generate_tdc2g_instance,
    recover_tdc2g,
)


def seed_for(name: str, index: int) -> bytes:
    return hashlib.sha256(
        f"MORPH-KEM TDC2g sweep {name} seed {index} v1".encode("ascii")
    ).digest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(TDC2G_PARAMETER_SETS), default=None)
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 64:
        raise SystemExit("--seeds must be in 1..64")

    params_list = (
        (TDC2G_PARAMETER_SETS[args.params],)
        if args.params is not None
        else tuple(TDC2G_PARAMETER_SETS.values())
    )

    print(
        "set,seed,base_rank,final_rank,extra_rows,overlay_attempts,"
        "top_le6,top_le8,random_le6,random_le8,rank_equal,dimension_equal"
    )
    for params in params_list:
        for index in range(args.seeds):
            instance = generate_tdc2g_instance(params, seed_for(params.name, index))
            recovery = recover_tdc2g(instance)
            print(
                f"{params.name},{index},{recovery.base_rank},{recovery.final_rank},"
                f"{recovery.extra_rows},{recovery.overlay_attempts},"
                f"{recovery.topology.minimum_weight_leq6 or 0},"
                f"{recovery.topology.minimum_weight_leq8 or 0},"
                f"{recovery.matched_random.minimum_weight_leq6 or 0},"
                f"{recovery.matched_random.minimum_weight_leq8 or 0},"
                f"{int(recovery.rank_profile_equal)},{int(recovery.dimension_profile_equal)}"
            )


if __name__ == "__main__":
    main()
