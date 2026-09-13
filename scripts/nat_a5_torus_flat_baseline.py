from __future__ import annotations

import argparse
import hashlib

from morph_kem.nat_a5_torus_flat import (
    NAT6_PARAMETER_SETS,
    generate_nat6_instance,
    recover_nat6,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--params", choices=sorted(NAT6_PARAMETER_SETS), default="nat6-8x9"
    )
    args = parser.parse_args()
    params = NAT6_PARAMETER_SETS[args.params]
    seed = hashlib.sha256(
        f"MORPH-KEM NAT6 fixed baseline {params.name} v1".encode("ascii")
    ).digest()
    public, reference = generate_nat6_instance(params, seed)
    recovery = recover_nat6(public, reference=reference)

    print(f"parameters: {params.name}")
    print(f"V/E/F: {recovery.vertices}/{recovery.edges}/{recovery.triangles}")
    print(f"Euler characteristic: {recovery.euler_characteristic}")
    print(f"edge incidence min/max: {recovery.min_triangles_per_edge}/{recovery.max_triangles_per_edge}")
    print(f"H1 dimension: {recovery.h1_dimension}")
    print(f"alpha/beta weights: {recovery.alpha_weight}/{recovery.beta_weight}")
    print(f"nonidentity face holonomies: {recovery.nonidentity_face_holonomies}")
    print(f"tree/non-tree edges: {recovery.tree_edges}/{recovery.non_tree_edges}")
    print(f"normalized nonidentity residuals: {recovery.normalized_nonidentity_residuals}")
    print(f"normalized distinct nonidentity residuals: {recovery.normalized_distinct_nonidentity_residuals}")
    print(f"commuting pair candidates: {recovery.commuting_pair_candidates}")
    print(f"pair candidates tested: {recovery.pair_candidates_tested}")
    print(f"propagation assignments: {recovery.propagation_assignments}")
    print(f"accepted decompositions: {recovery.accepted_decompositions}")
    print(f"first accepted: {recovery.first_accepted}")
    print(f"first pair matches planted: {recovery.first_pair_matches_planted_after_public_success}")
    print(f"first gauge matches planted: {recovery.first_gauge_matches_planted_after_public_success}")


if __name__ == "__main__":
    main()
