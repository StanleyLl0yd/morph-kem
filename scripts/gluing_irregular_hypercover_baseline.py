#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.gluing_irregular_hypercover import (
    G12_PARAMETER_SETS,
    generate_irregular_hypercover_instance,
    recover_irregular_hypercover,
    validate_irregular_hypercover_witness,
)
from morph_kem.gluing_surface_hypercover import toroidal_hypercover_incidence


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the MORPH-KEM G12 irregular-torus P3 hypercover negative control."
    )
    parser.add_argument("--params", choices=sorted(G12_PARAMETER_SETS), default="g12-8x9")
    parser.add_argument("--solution-cap", type=int, default=64)
    args = parser.parse_args()

    params = G12_PARAMETER_SETS[args.params]
    public, reference = generate_irregular_hypercover_instance(params, MASTER_SEED)
    incidence = toroidal_hypercover_incidence(public)
    recovery = recover_irregular_hypercover(
        public, reference=reference, solution_cap=args.solution_cap
    )
    validation = validate_irregular_hypercover_witness(public, reference.groups)

    print(f"parameters: {params.name}")
    print(f"rows/cols: {params.rows}/{params.cols}")
    print(f"successful flips / generation retries: {reference.successful_flips}/{reference.generation_retries}")
    print(f"public V/E/F: {incidence.vertices}/{incidence.edges}/{incidence.triangles}")
    print(f"Euler characteristic: {incidence.euler_characteristic}")
    print(
        "edge triangle incidence min/max: "
        f"{incidence.min_triangles_per_edge}/{incidence.max_triangles_per_edge}"
    )
    print(f"primal vertex-degree histogram: {recovery.primal_vertex_degree_histogram}")
    print(f"dual vertices/edges: {incidence.triangles}/{recovery.dual_edges}")
    print(f"dual degree histogram: {recovery.dual_degree_histogram}")
    print(f"dual bipartite: {recovery.dual_bipartite}")
    print(f"bridges/articulation points: {recovery.bridge_count}/{len(recovery.articulation_points)}")
    print(f"dual short cycles triangle/four: {recovery.dual_triangle_cycles}/{recovery.dual_four_cycles}")
    print(f"local signature classes: {recovery.local_signature_classes}")
    print(f"local signature class-size histogram: {recovery.local_signature_class_size_histogram}")
    print(f"normalization-improving legal flips: {recovery.normalization_improving_flips}")
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
    print(f"reference witness accepted: {validation.valid}")

    return 0 if validation.valid and recovery.accepted_solutions > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
