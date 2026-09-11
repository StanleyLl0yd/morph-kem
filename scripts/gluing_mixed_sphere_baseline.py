from __future__ import annotations

import argparse

from morph_kem.gluing_mixed_sphere import (
    G15_PARAMETER_SETS,
    generate_mixed_sphere_instance,
    recover_mixed_sphere,
)
from morph_kem.gluing_surface_hypercover import toroidal_hypercover_incidence


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(G15_PARAMETER_SETS), default="g15-72")
    parser.add_argument("--solution-cap", type=int, default=64)
    args = parser.parse_args()

    params = G15_PARAMETER_SETS[args.params]
    public, reference = generate_mixed_sphere_instance(params, MASTER_SEED)
    incidence = toroidal_hypercover_incidence(public)
    recovery = recover_mixed_sphere(public, reference=reference, solution_cap=args.solution_cap)

    print(f"parameters: {params.name}")
    print(f"growth steps: {reference.growth_steps}")
    print(
        "successful flips / rejected proposals / generation retries: "
        f"{reference.successful_flips}/{reference.rejected_flip_proposals}/{reference.generation_retries}"
    )
    print(f"public V/E/F: {incidence.vertices}/{incidence.edges}/{incidence.triangles}")
    print(f"Euler characteristic: {incidence.euler_characteristic}")
    print(
        "edge triangle incidence min/max: "
        f"{incidence.min_triangles_per_edge}/{incidence.max_triangles_per_edge}"
    )
    print(f"primal vertex-degree histogram: {recovery.primal_vertex_degree_histogram}")
    print(f"initial degree-three vertices: {recovery.initial_degree_three_vertices}")
    print(f"initial reverse-stacking candidates: {recovery.initial_reverse_candidates}")
    print(f"reverse-stacking moves: {recovery.reverse_moves}")
    print(
        "reverse terminal V/E/F / reached tetrahedron: "
        f"{recovery.reverse_terminal_vertices}/{recovery.reverse_terminal_edges}/"
        f"{recovery.reverse_terminal_triangles}/{recovery.reverse_reached_tetrahedron}"
    )
    print(f"normalization-improving legal flips: {recovery.normalization_improving_flips}")
    print(f"dual vertices/edges: {incidence.triangles}/{recovery.dual_edges}")
    print(f"dual degree histogram: {recovery.dual_degree_histogram}")
    print(f"dual bipartite: {recovery.dual_bipartite}")
    print(f"bridges/articulation points: {recovery.bridge_count}/{len(recovery.articulation_points)}")
    print(
        "dual short cycles triangle/four: "
        f"{recovery.dual_triangle_cycles}/{recovery.dual_four_cycles}"
    )
    print(f"local signature classes: {recovery.local_signature_classes}")
    print(
        "local signature class-size histogram: "
        f"{recovery.local_signature_class_size_histogram}"
    )
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
        f"{recovery.exact_cover_nodes}/{recovery.exact_cover_decisions}/"
        f"{recovery.exact_cover_backtracks}"
    )
    print(f"accepted public solutions: {recovery.accepted_solutions}")
    print(f"accepted non-reference solutions: {recovery.nonreference_accepted_solutions}")


if __name__ == "__main__":
    main()
