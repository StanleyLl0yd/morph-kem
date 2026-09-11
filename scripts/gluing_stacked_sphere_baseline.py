#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.gluing_stacked_sphere import (
    G14_PARAMETER_SETS,
    run_stacked_sphere_experiment,
)


MASTER_SEED = bytes.fromhex("76140450aabbccddeeff001122334455")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the MORPH-KEM G14 stacked-sphere reverse-normalization control."
    )
    parser.add_argument("--params", choices=sorted(G14_PARAMETER_SETS), default="g14-72")
    parser.add_argument("--solution-cap", type=int, default=64)
    args = parser.parse_args()

    params = G14_PARAMETER_SETS[args.params]
    result = run_stacked_sphere_experiment(
        params, MASTER_SEED, solution_cap=args.solution_cap
    )
    normalization = result.normalization
    recovery = result.hypercover

    print(f"parameters: {params.name}")
    print(f"stacking steps: {params.stacking_steps}")
    print(
        "public V/E/F: "
        f"{normalization.initial_vertices}/{normalization.initial_edges}/{normalization.initial_triangles}"
    )
    print(f"primal degree histogram: {normalization.initial_degree_histogram}")
    print(f"initial degree-three vertices: {normalization.initial_degree_three_vertices}")
    print(f"reverse-stacking moves: {normalization.reverse_moves}")
    print(f"reverse candidate counts: {normalization.candidate_counts}")
    print(f"max simultaneous reverse candidates: {normalization.max_candidates}")
    print(
        "terminal V/E/F: "
        f"{normalization.terminal_vertices}/{normalization.terminal_edges}/{normalization.terminal_triangles}"
    )
    print(f"terminal Euler characteristic: {normalization.terminal_euler_characteristic}")
    print(f"reached tetrahedron boundary: {normalization.reached_tetrahedron_boundary}")
    print(f"dual edges: {recovery.dual_edges}")
    print(f"dual degree histogram: {recovery.dual_degree_histogram}")
    print(f"dual bipartite: {recovery.dual_bipartite}")
    print(f"bridges/articulation points: {recovery.bridge_count}/{len(recovery.articulation_points)}")
    print(f"P3 public candidates: {recovery.candidate_count}")
    print(f"candidate memberships: {recovery.candidate_membership_histogram}")
    print(f"candidate overlap degrees: {recovery.candidate_overlap_degree_histogram}")
    print(f"candidate/triangle incidence: {recovery.candidate_triangle_incidence}")
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
    print(f"reference cover available: {recovery.reference_available}")
    print(f"accepted non-reference solutions: {recovery.nonreference_accepted_solutions}")

    ok = (
        normalization.reverse_moves == params.stacking_steps
        and normalization.reached_tetrahedron_boundary
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
