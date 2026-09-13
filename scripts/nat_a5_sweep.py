from __future__ import annotations

import argparse
import hashlib

from morph_kem.nat_a5 import NAT3_PARAMETER_SETS, generate_nat3_instance, recover_nat3


def seed_for(name: str, index: int) -> bytes:
    return hashlib.sha256(
        f"MORPH-KEM NAT3 sweep {name} seed {index} v1".encode("ascii")
    ).digest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 16:
        raise SystemExit("--seeds must be between 1 and 16")

    print(
        "set,seed,weight,V,E,F,defects,support_space,hitting_supports,"
        "propagated,consistent,accepted,cap_hit,first_accepted,support_match,state_match,planted_hitting"
    )
    for params in NAT3_PARAMETER_SETS.values():
        for index in range(args.seeds):
            seed = seed_for(params.name, index)
            for weight in params.noise_weights:
                public, reference = generate_nat3_instance(params, seed, weight)
                recovery = recover_nat3(public, reference=reference)
                print(
                    f"{params.name},{index},{weight},"
                    f"{recovery.vertices},{recovery.edges},{recovery.triangles},"
                    f"{recovery.curvature_defect_faces},"
                    f"{recovery.total_support_combinations},"
                    f"{recovery.curvature_hitting_supports},"
                    f"{recovery.propagated_supports},"
                    f"{recovery.connected_consistent_supports},"
                    f"{recovery.accepted_states},"
                    f"{int(recovery.stored_state_cap_hit)},"
                    f"{int(recovery.first_state_accepted)},"
                    f"{int(bool(recovery.first_support_matches_planted_after_public_success))},"
                    f"{int(bool(recovery.first_state_matches_planted_after_public_success))},"
                    f"{int(bool(recovery.planted_support_is_curvature_hitting))}"
                )


if __name__ == "__main__":
    main()
