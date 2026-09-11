#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib

from morph_kem.nat_coboundary import (
    NAT0_PARAMETER_SETS,
    generate_nat0_repeated_instance,
    generate_nat0_single_instance,
    recover_nat0_repeated,
    recover_nat0_single,
)


MASTER_SEED = bytes.fromhex("0011aabb2233ccdd4455eeff66778899")


def _seed(name: str, index: int) -> bytes:
    return hashlib.sha256(
        b"MORPH-KEM NAT0 sweep v1\x00"
        + MASTER_SEED
        + name.encode("ascii")
        + index.to_bytes(4, "big")
    ).digest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sweep MORPH-KEM NAT0 noisy coboundary controls."
    )
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 64:
        parser.error("--seeds must be in [1,64]")

    print(
        "set,seed,single_violated,single_accepted,single_match,"
        "samples,noise_weight,majority_votes,repeated_accepted,repeated_match"
    )
    failures = 0
    for name in sorted(NAT0_PARAMETER_SETS):
        params = NAT0_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            seed = _seed(name, seed_index)
            single_public, single_reference = generate_nat0_single_instance(params, seed)
            single = recover_nat0_single(single_public, reference=single_reference)
            repeated_public, repeated_reference = generate_nat0_repeated_instance(params, seed)
            repeated = recover_nat0_repeated(repeated_public, reference=repeated_reference)
            print(
                f"{name},{seed_index},{len(single.violated_triangles)},"
                f"{int(single.accepted)},"
                f"{int(bool(single.matches_reference_after_public_success))},"
                f"{len(repeated_public.observed_edge_masks)},"
                f"{repeated_public.public_noise_weight},"
                f"{repeated.majority_edge_votes},"
                f"{int(repeated.accepted)},"
                f"{int(bool(repeated.matches_reference_after_public_success))}"
            )
            failures += int(
                len(single.violated_triangles) != 2
                or not single.accepted
                or not single.matches_reference_after_public_success
                or not repeated.accepted
                or not repeated.matches_reference_after_public_success
            )

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
