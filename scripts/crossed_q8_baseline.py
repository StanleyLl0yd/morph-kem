#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.crossed_q8 import (
    audit_crossed_module,
    generate_q8_fake_flat_instance,
    public_face_lift_attack,
    validate_fake_flatness,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the MORPH K2.2 Q8 crossed-module fake-flatness calibration."
    )
    parser.add_argument(
        "--master-seed",
        default="40226490aabbccddeeff001122334455",
        help="hex-encoded deterministic K2.2 generation seed",
    )
    args = parser.parse_args()

    audit = audit_crossed_module()
    public, reference = generate_q8_fake_flat_instance(
        bytes.fromhex(args.master_seed)
    )
    attack = public_face_lift_attack(public)

    print(f"Q8 order: {audit.q8_order}")
    print(f"Aut(Q8) order: {audit.automorphism_order}")
    print(f"boundary kernel/image/cokernel cosets: {audit.kernel_size}/{audit.image_size}/{audit.cokernel_cosets}")
    print(f"crossed identity checks: {audit.first_identity_checks}/{audit.second_identity_checks}")
    print(f"crossed identities hold: {audit.identities_hold}")
    print(
        "base V/E/F: "
        f"{len(public.base_map.vertices)}/"
        f"{len(public.base_map.edges)}/"
        f"{len(public.base_map.faces)}"
    )
    print(f"reference accepted: {validate_fake_flatness(public, reference.face_values)}")
    print(f"boundary-image faces: {attack.boundary_image_faces}/{len(public.base_map.faces)}")
    print(f"nonidentity face curvatures: {attack.nonidentity_curvatures}")
    print(f"public fiber sizes: {attack.fiber_sizes}")
    print(f"equivalent fake-flat witnesses: {attack.total_equivalent_witnesses}")
    print(f"public attack accepted: {attack.accepted}")
    print(f"edge compositions: {attack.edge_compositions}")
    print(f"Q8 preimage checks: {attack.q8_preimage_checks}")
    print(f"public attack equals planted representative: {attack.face_values == reference.face_values}")

    return 0 if (
        audit.identities_hold
        and attack.accepted
        and attack.fiber_sizes == (2, 2, 2, 2)
        and attack.total_equivalent_witnesses == 16
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
