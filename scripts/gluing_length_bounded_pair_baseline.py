#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.gluing_length_bounded_pair import (
    G18_PARAMETER_SETS,
    generate_length_bounded_pair_instance,
    recover_length_bounded_pair,
)


FIXED_SEED = bytes.fromhex(
    "a7450102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e"
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run MORPH-KEM G18 A-045 baseline.")
    parser.add_argument("--params", choices=sorted(G18_PARAMETER_SETS), default="g18-8x9")
    args = parser.parse_args()
    params = G18_PARAMETER_SETS[args.params]
    public, reference = generate_length_bounded_pair_instance(params, FIXED_SEED)
    recovery = recover_length_bounded_pair(
        public, reference=reference, successful_flips=params.successful_flips
    )

    print(f"parameters: {args.params}")
    print(f"successful carrier flips: {recovery.successful_flips}")
    print(f"public V/E/F: {recovery.vertices}/{recovery.edges}/{recovery.triangles}")
    print(f"Euler characteristic: {recovery.euler_characteristic}")
    print(
        "edge triangle incidence min/max: "
        f"{recovery.min_triangles_per_edge}/{recovery.max_triangles_per_edge}"
    )
    print(f"primal degree histogram: {recovery.primal_vertex_degree_histogram}")
    print(f"dual degree histogram: {recovery.dual_vertex_degree_histogram}")
    print(f"normalization-improving legal flips: {recovery.normalization_improving_flips}")
    print(f"public primal/dual length bounds: {recovery.max_primal_length}/{recovery.max_dual_length}")
    print(
        "reference primal/dual lengths: "
        f"{recovery.reference_primal_length}/{recovery.reference_dual_length}"
    )
    print(f"public alpha weight / H1 dimension: {recovery.alpha_weight}/{recovery.h1_dimension}")
    print(
        "parity-cover vertices/directed arcs: "
        f"{recovery.parity_cover_vertices}/{recovery.parity_cover_directed_arcs}"
    )
    print(f"parity-cover roots attempted: {recovery.cover_roots_attempted}")
    print(f"parity-cover queue pops / edge scans: {recovery.cover_queue_pops}/{recovery.cover_edge_scans}")
    print(f"minimum odd walk/support edges: {recovery.cover_walk_length_min}/{recovery.cover_support_edges_min}")
    print(
        "support decomposition cycles/path scans: "
        f"{recovery.decomposition_cycles_tested}/{recovery.decomposition_path_scans}"
    )
    print(
        "distinct primal candidates / within bound: "
        f"{recovery.distinct_primal_candidates}/{recovery.primal_candidates_within_bound}"
    )
    print(f"dual connector calls: {recovery.dual_connector_calls}")
    print(
        "dual connector queue pops / edge scans: "
        f"{recovery.dual_connector_queue_pops}/{recovery.dual_connector_edge_scans}"
    )
    print(
        "selected primal/dual lengths: "
        f"{recovery.selected_primal_length}/{recovery.selected_dual_length}"
    )
    print(f"selected exact crossing count: {recovery.selected_crossing_count}")
    print(f"selected accepted: {recovery.selected_accepted}")
    print(f"selected matches reference: {recovery.selected_matches_reference}")
    print(f"canonical tree-cotree leftovers: {recovery.canonical_treecotree_leftovers}")
    print(
        "canonical tree-cotree primal/dual lengths: "
        f"{recovery.canonical_treecotree_primal_length}/{recovery.canonical_treecotree_dual_length}"
    )
    print(
        "canonical tree-cotree crossing/within-bounds/accepted: "
        f"{recovery.canonical_treecotree_crossing_count}/"
        f"{recovery.canonical_treecotree_within_bounds}/"
        f"{recovery.canonical_treecotree_accepted}"
    )

    ok = (
        recovery.euler_characteristic == 0
        and recovery.h1_dimension == 2
        and recovery.selected_crossing_count == 1
        and recovery.selected_accepted
        and recovery.selected_primal_length <= recovery.max_primal_length
        and recovery.selected_dual_length <= recovery.max_dual_length
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
