from __future__ import annotations

import argparse
import hashlib

from morph_kem.nat_a5_cycle_noise import (
    NAT5_PARAMETER_SETS,
    generate_nat5_instance,
    recover_nat5,
)


def seed_for(name: str, index: int) -> bytes:
    return hashlib.sha256(
        f"MORPH-KEM NAT5 sweep {name} seed {index} v1".encode("ascii")
    ).digest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 16:
        raise SystemExit("--seeds must be between 1 and 16")

    print(
        "set,seed,L,V,E,F,cycles,defects,hitting,tested,consistent,accepted,cap_hit,first_accepted,"
        "cycle_match,noise_match,state_match"
    )
    for params in NAT5_PARAMETER_SETS.values():
        for index in range(args.seeds):
            public, reference = generate_nat5_instance(
                params, seed_for(params.name, index)
            )
            recovery = recover_nat5(public, reference=reference)
            print(
                f"{params.name},{index},{params.cycle_length},"
                f"{recovery.vertices},{recovery.edges},{recovery.triangles},"
                f"{recovery.enumerated_cycles},{recovery.nonidentity_face_holonomies},"
                f"{recovery.curvature_hitting_cycles},{recovery.cycle_value_pairs_tested},"
                f"{recovery.consistent_pairs},{recovery.accepted_witnesses},"
                f"{int(recovery.accepted_cap_hit)},{int(recovery.first_accepted)},"
                f"{int(bool(recovery.first_cycle_matches_planted_after_public_success))},"
                f"{int(bool(recovery.first_noise_matches_planted_after_public_success))},"
                f"{int(bool(recovery.first_state_matches_planted_after_public_success))}"
            )


if __name__ == "__main__":
    main()
