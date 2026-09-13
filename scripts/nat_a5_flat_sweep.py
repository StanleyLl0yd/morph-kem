from __future__ import annotations

import argparse
import hashlib

from morph_kem.nat_a5_flat import NAT4_PARAMETER_SETS, generate_nat4_instance, recover_nat4


def seed_for(name: str, index: int) -> bytes:
    return hashlib.sha256(
        f"MORPH-KEM NAT4 sweep {name} seed {index} v1".encode("ascii")
    ).digest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 16:
        raise SystemExit("--seeds must be between 1 and 16")

    print(
        "set,seed,weight,V,E,F,nonidentity_curvature,integration_checks,consistent,"
        "equivalent_lower_bound,accepted,support_match,clean_match,effective_match"
    )
    for params in NAT4_PARAMETER_SETS.values():
        for index in range(args.seeds):
            seed = seed_for(params.name, index)
            for weight in params.deformation_weights:
                public, reference = generate_nat4_instance(params, seed, weight)
                recovery = recover_nat4(public, reference=reference)
                print(
                    f"{params.name},{index},{weight},"
                    f"{recovery.vertices},{recovery.edges},{recovery.triangles},"
                    f"{recovery.nonidentity_face_holonomies},"
                    f"{recovery.integration_edge_checks},"
                    f"{int(recovery.integration_consistent)},"
                    f"{recovery.equivalent_witness_lower_bound},"
                    f"{int(recovery.canonical_witness_accepted)},"
                    f"{int(bool(recovery.canonical_support_matches_planted_after_public_success))},"
                    f"{int(bool(recovery.canonical_clean_state_matches_planted_after_public_success))},"
                    f"{int(bool(recovery.effective_state_matches_reference_after_public_success))}"
                )


if __name__ == "__main__":
    main()
