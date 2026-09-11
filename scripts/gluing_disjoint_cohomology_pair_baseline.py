#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.gluing_disjoint_cohomology_pair import (
    G19_PARAMETER_SETS,
    generate_disjoint_cohomology_pair_instance,
    recover_disjoint_cohomology_pair,
)


FIXED_SEED = bytes.fromhex(
    "a7460102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e"
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run MORPH-KEM G19 A-046 baseline.")
    parser.add_argument("--params", choices=sorted(G19_PARAMETER_SETS), default="g19-8x9")
    args = parser.parse_args()
    params = G19_PARAMETER_SETS[args.params]
    public, reference = generate_disjoint_cohomology_pair_instance(params, FIXED_SEED)
    recovery = recover_disjoint_cohomology_pair(
        public,
        reference=reference,
        successful_flips=params.successful_flips,
    )

    print(f"parameters: {args.params}")
    print(f"successful carrier flips / generation retries: {recovery.successful_flips}/{recovery.generation_retries}")
    print(f"public V/E/F: {recovery.vertices}/{recovery.edges}/{recovery.triangles}")
    print(f"Euler characteristic: {recovery.euler_characteristic}")
    print(
        "edge triangle incidence min/max: "
        f"{recovery.min_triangles_per_edge}/{recovery.max_triangles_per_edge}"
    )
    print(f"primal degree histogram: {recovery.primal_vertex_degree_histogram}")
    print(f"normalization-improving legal flips: {recovery.normalization_improving_flips}")
    print(f"public alpha weight / H1 dimension: {recovery.alpha_weight}/{recovery.h1_dimension}")
    print(f"public short/long bounds: {recovery.max_short_length}/{recovery.max_long_length}")
    print(
        "reference short/long lengths: "
        f"{recovery.reference_short_length}/{recovery.reference_long_length}"
    )
    print(f"reference seeded-tree attempts: {reference.reference_tree_attempts}")
    print(
        "first-stage roots/queue pops/edge scans: "
        f"{recovery.first_stage_roots}/{recovery.first_stage_queue_pops}/{recovery.first_stage_edge_scans}"
    )
    print(f"first-stage candidates: {recovery.first_stage_candidates}")
    print(f"first-stage length histogram: {recovery.first_stage_length_histogram}")
    print(f"first candidates attempted: {recovery.first_candidates_attempted}")
    print(f"second-stage calls: {recovery.second_stage_calls}")
    print(
        "second-stage roots/reachable roots: "
        f"{recovery.second_stage_roots}/{recovery.second_stage_reachable_roots}"
    )
    print(
        "second-stage queue pops/edge scans: "
        f"{recovery.second_stage_queue_pops}/{recovery.second_stage_edge_scans}"
    )
    print(
        "second-stage decomposition cycles/path scans: "
        f"{recovery.second_stage_decomposition_cycles}/{recovery.second_stage_decomposition_scans}"
    )
    print(f"second-stage candidates: {recovery.second_stage_candidates}")
    print(
        "selected deleted vertices/edges: "
        f"{recovery.selected_deleted_vertices}/{recovery.selected_deleted_edges}"
    )
    print(
        "selected short/long lengths: "
        f"{recovery.selected_short_length}/{recovery.selected_long_length}"
    )
    print(
        "selected pairings/shared vertices: "
        f"{recovery.selected_first_pairing}/{recovery.selected_second_pairing}/"
        f"{recovery.selected_shared_vertices}"
    )
    print(f"selected accepted: {recovery.selected_accepted}")
    print(f"selected matches reference: {recovery.selected_matches_reference}")
    print(
        "independent odd fundamental cycles/pair tests: "
        f"{recovery.independent_odd_fundamental_cycles}/{recovery.independent_pair_tests}"
    )
    print(
        "independent pair found/accepted: "
        f"{recovery.independent_pair_found}/{recovery.independent_pair_accepted}"
    )

    ok = (
        recovery.euler_characteristic == 0
        and recovery.h1_dimension == 2
        and recovery.selected_accepted
        and recovery.selected_shared_vertices == 0
        and recovery.selected_first_pairing == 1
        and recovery.selected_second_pairing == 1
        and recovery.selected_short_length <= recovery.max_short_length
        and recovery.selected_long_length <= recovery.max_long_length
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
