from __future__ import annotations

import argparse
import hashlib

from morph_kem.nat_a5_torus_flat import (
    NAT6_PARAMETER_SETS,
    generate_nat6_instance,
    recover_nat6,
)


def seed_for(name: str, index: int) -> bytes:
    return hashlib.sha256(
        f"MORPH-KEM NAT6 sweep {name} seed {index} v1".encode("ascii")
    ).digest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 16:
        raise SystemExit("--seeds must be between 1 and 16")

    print(
        "set,seed,V,E,F,chi,h1,alpha_weight,beta_weight,face_defects,tree_edges,"
        "non_tree_edges,residual_nonidentity,residual_distinct,pair_candidates,tested,"
        "assignments,accepted,first_accepted,pair_match,gauge_match"
    )
    for params in NAT6_PARAMETER_SETS.values():
        for index in range(args.seeds):
            public, reference = generate_nat6_instance(
                params, seed_for(params.name, index)
            )
            recovery = recover_nat6(public, reference=reference)
            print(
                f"{params.name},{index},{recovery.vertices},{recovery.edges},{recovery.triangles},"
                f"{recovery.euler_characteristic},{recovery.h1_dimension},"
                f"{recovery.alpha_weight},{recovery.beta_weight},"
                f"{recovery.nonidentity_face_holonomies},{recovery.tree_edges},"
                f"{recovery.non_tree_edges},{recovery.normalized_nonidentity_residuals},"
                f"{recovery.normalized_distinct_nonidentity_residuals},"
                f"{recovery.commuting_pair_candidates},{recovery.pair_candidates_tested},"
                f"{recovery.propagation_assignments},{recovery.accepted_decompositions},"
                f"{int(recovery.first_accepted)},"
                f"{int(bool(recovery.first_pair_matches_planted_after_public_success))},"
                f"{int(bool(recovery.first_gauge_matches_planted_after_public_success))}"
            )


if __name__ == "__main__":
    main()
