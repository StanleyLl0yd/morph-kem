#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib

from morph_kem.gluing_genus2_same_side import (
    G22_PARAMETER_SETS,
    generate_same_side_instance,
    recover_same_side_witness,
)


MASTER_SEED = bytes.fromhex("a17e0405060708091011121314151617")


def _seed(name: str, index: int) -> bytes:
    return hashlib.sha256(
        b"MORPH-KEM G22 sweep v1\x00"
        + MASTER_SEED
        + name.encode("ascii")
        + index.to_bytes(4, "big")
    ).digest()


def _fmt(values: tuple[int, ...]) -> str:
    return "/".join(str(value) for value in values)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sweep MORPH-KEM G22 same-side multicurve public recovery."
    )
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 64:
        parser.error("--seeds must be in [1,64]")

    print(
        "set,seed,V,E,F,H1,raw,distinct,retained,pairs,pair_tests,"
        "lengths,signatures,rank,accepted"
    )
    failures = 0
    for name in sorted(G22_PARAMETER_SETS):
        params = G22_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            public = generate_same_side_instance(params, _seed(name, seed_index))
            recovery = recover_same_side_witness(public)
            print(
                f"{name},{seed_index},{recovery.vertices},{recovery.edges},{recovery.triangles},"
                f"{recovery.h1_dimension},{recovery.raw_fundamental_cycles},"
                f"{recovery.distinct_cycles},{recovery.retained_candidates},"
                f"{recovery.exact_one_pairs},{recovery.pair_pair_tests},"
                f"{_fmt(recovery.selected_lengths)},{_fmt(recovery.selected_signatures)},"
                f"{recovery.selected_rank},{int(recovery.selected_accepted)}"
            )
            failures += int(
                recovery.euler_characteristic != -2
                or recovery.h1_dimension != 4
                or recovery.selected_rank != 4
                or not recovery.selected_accepted
            )

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
