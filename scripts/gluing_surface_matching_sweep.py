from __future__ import annotations

import argparse
import hashlib

from morph_kem.gluing_surface_matching import (
    G10_PARAMETER_SETS,
    generate_toroidal_matching_instance,
    recover_toroidal_matching,
    toroidal_matching_incidence,
)


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


def derived_seed(name: str, index: int) -> bytes:
    return hashlib.sha256(
        b"MORPH-KEM G10 sweep v1\x00"
        + MASTER_SEED
        + name.encode("ascii")
        + index.to_bytes(4, "big")
    ).digest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    parser.add_argument("--solution-cap", type=int, default=64)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 64:
        raise SystemExit("--seeds must be in 1..64")

    print(
        "set,seed,V,E,F,euler,dual_edges,bridges,articulations,bipart_left,bipart_right,"
        "candidate_edges,base_augmentations,base_dfs_calls,base_edge_scans,alt_attempts,"
        "alt_edge_scans,solutions,cap_hit,accepted,nonreference"
    )
    success = True
    for name in sorted(G10_PARAMETER_SETS):
        params = G10_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            public, reference = generate_toroidal_matching_instance(
                params, derived_seed(name, seed_index)
            )
            incidence = toroidal_matching_incidence(public)
            recovery = recover_toroidal_matching(
                public, reference=reference, solution_cap=args.solution_cap
            )
            print(
                f"{name},{seed_index},{incidence.vertices},{incidence.edges},{incidence.triangles},"
                f"{incidence.euler_characteristic},{recovery.dual_edges},{recovery.bridge_count},"
                f"{len(recovery.articulation_points)},{recovery.bipartition_sizes[0]},"
                f"{recovery.bipartition_sizes[1]},{recovery.candidate_edges},"
                f"{recovery.base_augmentations},{recovery.base_dfs_calls},{recovery.base_edge_scans},"
                f"{recovery.alternative_attempts},{recovery.alternative_matching_edge_scans},"
                f"{recovery.matching_solutions},{int(recovery.matching_cap_hit)},"
                f"{recovery.accepted_solutions},{recovery.nonreference_accepted_solutions}"
            )
            cells = params.rows * params.cols
            success &= (
                incidence.vertices == cells
                and incidence.edges == 3 * cells
                and incidence.triangles == 2 * cells
                and incidence.euler_characteristic == 0
                and incidence.min_triangles_per_edge == 2
                and incidence.max_triangles_per_edge == 2
                and recovery.dual_edges == 3 * cells
                and recovery.dual_degree_histogram == ((3, 2 * cells),)
                and recovery.bridge_count == 0
                and not recovery.articulation_points
                and recovery.bipartition_sizes == (cells, cells)
                and recovery.candidate_edges == 3 * cells
                and recovery.accepted_solutions >= 2
                and recovery.nonreference_accepted_solutions >= 1
            )
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
