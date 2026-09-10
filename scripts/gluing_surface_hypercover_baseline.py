#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.gluing_surface_hypercover import (
    G11_PARAMETER_SETS,
    generate_toroidal_hypercover_instance,
    recover_toroidal_hypercover,
    toroidal_hypercover_incidence,
    validate_toroidal_hypercover_witness,
)


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the MORPH-KEM G11 toroidal P3-hypercover negative control."
    )
    parser.add_argument("--params", choices=sorted(G11_PARAMETER_SETS), default="g11-6x9")
    parser.add_argument("--solution-cap", type=int, default=64)
    args = parser.parse_args()

    params = G11_PARAMETER_SETS[args.params]
    public, reference = generate_toroidal_hypercover_instance(params, MASTER_SEED)
    incidence = toroidal_hypercover_incidence(public)
    recovery = recover_toroidal_hypercover(
        public,
        reference=reference,
        solution_cap=args.solution_cap,
    )
    reference_validation = validate_toroidal_hypercover_witness(public, reference.groups)

    print(f"parameters: {params.name}")
    print(f"torus rows/cols: {params.rows}/{params.cols}")
    print(f"public V/E/F: {incidence.vertices}/{incidence.edges}/{incidence.triangles}")
    print(f"Euler characteristic: {incidence.euler_characteristic}")
    print(
        "edge triangle incidence min/max: "
        f"{incidence.min_triangles_per_edge}/{incidence.max_triangles_per_edge}"
    )
    print(f"witness pieces: {incidence.triangles // 3}")
    print(f"dual vertices/edges: {incidence.triangles}/{recovery.dual_edges}")
    print(f"dual degree histogram: {recovery.dual_degree_histogram}")
    print(f"bridges/articulation points: {recovery.bridge_count}/{len(recovery.articulation_points)}")
    print(f"public bipartition sizes: {recovery.bipartition_sizes}")
    print(f"P3 public candidates: {recovery.candidate_count}")
    print(f"candidate memberships per triangle: {recovery.candidate_membership_histogram}")
    print(f"candidate overlap-degree histogram: {recovery.candidate_overlap_degree_histogram}")
    print(f"candidate/triangle incidence size: {recovery.candidate_triangle_incidence}")
    print(
        "exact-cover solutions/cap: "
        f"{recovery.exact_cover_solutions}/{recovery.exact_cover_solution_cap}"
    )
    print(f"exact-cover cap hit: {recovery.exact_cover_cap_hit}")
    print(
        "exact-cover nodes/decisions/backtracks: "
        f"{recovery.exact_cover_nodes}/{recovery.exact_cover_decisions}/{recovery.exact_cover_backtracks}"
    )
    print(f"accepted public solutions: {recovery.accepted_solutions}")
    print(f"accepted non-reference solutions: {recovery.nonreference_accepted_solutions}")
    print(f"reference witness accepted: {reference_validation.valid}")

    return 0 if (
        reference_validation.valid
        and recovery.accepted_solutions > 0
        and recovery.nonreference_accepted_solutions > 0
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
