from __future__ import annotations

import argparse

from morph_kem.gluing_surface_matching import (
    G10_PARAMETER_SETS,
    generate_toroidal_matching_instance,
    recover_toroidal_matching,
    toroidal_matching_incidence,
    validate_toroidal_matching_witness,
)


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(G10_PARAMETER_SETS), default="g10-8x8")
    parser.add_argument("--solution-cap", type=int, default=64)
    args = parser.parse_args()

    params = G10_PARAMETER_SETS[args.params]
    public, reference = generate_toroidal_matching_instance(params, MASTER_SEED)
    incidence = toroidal_matching_incidence(public)
    recovery = recover_toroidal_matching(
        public, reference=reference, solution_cap=args.solution_cap
    )
    reference_validation = validate_toroidal_matching_witness(public, reference.groups)

    print(f"parameters: {params.name}")
    print(f"torus rows/cols: {params.rows}/{params.cols}")
    print(
        "public V/E/F: "
        f"{incidence.vertices}/{incidence.edges}/{incidence.triangles}"
    )
    print(f"Euler characteristic: {incidence.euler_characteristic}")
    print(
        "edge triangle incidence min/max: "
        f"{incidence.min_triangles_per_edge}/{incidence.max_triangles_per_edge}"
    )
    print(f"dual vertices/edges: {incidence.triangles}/{recovery.dual_edges}")
    print(f"dual degree histogram: {recovery.dual_degree_histogram}")
    print(f"bridges/articulation points: {recovery.bridge_count}/{len(recovery.articulation_points)}")
    print(f"public bipartition sizes: {recovery.bipartition_sizes}")
    print(f"allowed candidate dual edges: {recovery.candidate_edges}")
    print(
        "base matching augmentations/DFS calls/edge scans: "
        f"{recovery.base_augmentations}/{recovery.base_dfs_calls}/{recovery.base_edge_scans}"
    )
    print(f"alternative forced-edge attempts: {recovery.alternative_attempts}")
    print(f"alternative matching edge scans: {recovery.alternative_matching_edge_scans}")
    print(
        "matching solutions/cap: "
        f"{recovery.matching_solutions}/{recovery.matching_solution_cap}"
    )
    print(f"matching cap hit: {recovery.matching_cap_hit}")
    print(f"accepted public solutions: {recovery.accepted_solutions}")
    print(f"accepted non-reference solutions: {recovery.nonreference_accepted_solutions}")
    print(f"reference witness accepted: {reference_validation.valid}")

    success = (
        reference_validation.valid
        and incidence.euler_characteristic == 0
        and incidence.min_triangles_per_edge == 2
        and incidence.max_triangles_per_edge == 2
        and recovery.bridge_count == 0
        and not recovery.articulation_points
        and recovery.accepted_solutions >= 2
        and recovery.nonreference_accepted_solutions >= 1
    )
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
