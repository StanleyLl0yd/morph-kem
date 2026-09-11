#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib

from morph_kem.hga_actions import (
    HGA0_DIHEDRAL_PARAMETER_SETS,
    HGA0_LINEAR_PARAMETER_SETS,
    generate_dihedral_action_instance,
    generate_linear_action_instance,
    recover_dihedral_action,
    recover_linear_action,
)


MASTER_SEED = bytes.fromhex("f0e1d2c3b4a5968778695a4b3c2d1e0f")


def _seed(family: str, name: str, index: int) -> bytes:
    return hashlib.sha256(
        b"MORPH-KEM HGA0 sweep v1\x00"
        + MASTER_SEED
        + family.encode("ascii")
        + name.encode("ascii")
        + index.to_bytes(4, "big")
    ).digest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sweep MORPH-KEM HGA0 action trivialization controls."
    )
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 64:
        parser.error("--seeds must be in [1,64]")

    print(
        "family,set,seed,size,secret_weight_or_matches,tested,label_checks,"
        "stabilizer,accepted,matches_reference"
    )
    failures = 0

    for name in sorted(HGA0_LINEAR_PARAMETER_SETS):
        params = HGA0_LINEAR_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            public, reference = generate_linear_action_instance(
                params, _seed("linear", name, seed_index)
            )
            recovery = recover_linear_action(public, reference=reference)
            print(
                f"linear,{name},{seed_index},{params.dimension},"
                f"{len(recovery.recovered_word)},1,0,1,"
                f"{int(recovery.accepted)},"
                f"{int(bool(recovery.matches_reference_after_public_success))}"
            )
            failures += int(
                not recovery.accepted
                or not recovery.matches_reference_after_public_success
                or recovery.xor_operations != 1
            )

    for name in sorted(HGA0_DIHEDRAL_PARAMETER_SETS):
        params = HGA0_DIHEDRAL_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            public, reference = generate_dihedral_action_instance(
                params, _seed("dihedral", name, seed_index)
            )
            recovery = recover_dihedral_action(public, reference=reference)
            print(
                f"dihedral,{name},{seed_index},{params.polygon_size},"
                f"{len(recovery.matching_elements)},"
                f"{recovery.candidate_elements_tested},{recovery.label_checks},"
                f"{recovery.stabilizer_size},{int(recovery.accepted)},"
                f"{int(bool(recovery.matches_reference_after_public_success))}"
            )
            failures += int(
                not recovery.accepted
                or not recovery.matches_reference_after_public_success
                or recovery.candidate_elements_tested != 2 * params.polygon_size
                or len(recovery.matching_elements) != 1
                or recovery.stabilizer_size != 1
            )

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
