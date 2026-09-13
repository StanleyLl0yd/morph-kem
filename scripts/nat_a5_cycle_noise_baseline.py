from __future__ import annotations

import argparse
import hashlib

from morph_kem.nat_a5_cycle_noise import (
    NAT5_PARAMETER_SETS,
    generate_nat5_instance,
    recover_nat5,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(NAT5_PARAMETER_SETS), default="nat5-F36")
    args = parser.parse_args()
    params = NAT5_PARAMETER_SETS[args.params]
    seed = hashlib.sha256(
        f"MORPH-KEM NAT5 fixed baseline {params.name} v1".encode("ascii")
    ).digest()
    public, reference = generate_nat5_instance(params, seed)
    recovery = recover_nat5(public, reference=reference)

    print(f"parameters: {params.name}")
    print(f"V/E/F: {recovery.vertices}/{recovery.edges}/{recovery.triangles}")
    print(f"cycle length: {recovery.cycle_length}")
    print(f"enumerated public cycles: {recovery.enumerated_cycles}")
    print(f"nonidentity face holonomies: {recovery.nonidentity_face_holonomies}")
    print(f"curvature-hitting cycles: {recovery.curvature_hitting_cycles}")
    print(f"cycle/value pairs tested: {recovery.cycle_value_pairs_tested}")
    print(f"consistent pairs: {recovery.consistent_pairs}")
    print(f"accepted witnesses / cap: {recovery.accepted_witnesses}/{recovery.accepted_cap_hit}")
    print(f"first accepted: {recovery.first_accepted}")
    print(f"first cycle matches planted: {recovery.first_cycle_matches_planted_after_public_success}")
    print(f"first noise matches planted: {recovery.first_noise_matches_planted_after_public_success}")
    print(f"first state matches planted: {recovery.first_state_matches_planted_after_public_success}")
    print(f"rejected flips: {reference.rejected_flip_proposals}")


if __name__ == "__main__":
    main()
