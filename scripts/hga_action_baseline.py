#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.hga_actions import (
    HGA0_DIHEDRAL_PARAMETER_SETS,
    HGA0_LINEAR_PARAMETER_SETS,
    generate_dihedral_action_instance,
    generate_linear_action_instance,
    recover_dihedral_action,
    recover_linear_action,
)


MASTER_SEED = bytes.fromhex("f0e1d2c3b4a5968778695a4b3c2d1e0f")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run MORPH-KEM HGA0 deliberately weak action controls."
    )
    parser.add_argument(
        "--linear",
        choices=sorted(HGA0_LINEAR_PARAMETER_SETS),
        default="hga0-linear-24",
    )
    parser.add_argument(
        "--dihedral",
        choices=sorted(HGA0_DIHEDRAL_PARAMETER_SETS),
        default="hga0-dihedral-25",
    )
    args = parser.parse_args()

    linear_public, linear_reference = generate_linear_action_instance(
        HGA0_LINEAR_PARAMETER_SETS[args.linear], MASTER_SEED
    )
    linear = recover_linear_action(linear_public, reference=linear_reference)

    dihedral_public, dihedral_reference = generate_dihedral_action_instance(
        HGA0_DIHEDRAL_PARAMETER_SETS[args.dihedral], MASTER_SEED
    )
    dihedral = recover_dihedral_action(dihedral_public, reference=dihedral_reference)

    print(f"linear parameters: {args.linear}")
    print(f"linear dimension: {linear_public.dimension}")
    print(f"linear recovered word weight: {len(linear.recovered_word)}")
    print(f"linear representation rank: {linear.representation_rank}")
    print(f"linear xor operations: {linear.xor_operations}")
    print(f"linear accepted: {linear.accepted}")
    print(
        "linear matches reference after public success: "
        f"{linear.matches_reference_after_public_success}"
    )
    print(f"dihedral parameters: {args.dihedral}")
    print(f"dihedral polygon size: {len(dihedral_public.labels)}")
    print(f"dihedral candidate elements tested: {dihedral.candidate_elements_tested}")
    print(f"dihedral label checks: {dihedral.label_checks}")
    print(f"dihedral matching elements: {len(dihedral.matching_elements)}")
    print(f"dihedral stabilizer size: {dihedral.stabilizer_size}")
    print(
        "dihedral recovered element: "
        f"rotation={dihedral.recovered_element.rotation},"
        f"reflected={int(dihedral.recovered_element.reflected)}"
    )
    print(f"dihedral accepted: {dihedral.accepted}")
    print(
        "dihedral matches reference after public success: "
        f"{dihedral.matches_reference_after_public_success}"
    )

    return 0 if (
        linear.accepted
        and linear.matches_reference_after_public_success
        and dihedral.accepted
        and dihedral.matches_reference_after_public_success
        and len(dihedral.matching_elements) == 1
        and dihedral.stabilizer_size == 1
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
