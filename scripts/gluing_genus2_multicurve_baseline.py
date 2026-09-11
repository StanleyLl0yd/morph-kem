#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.gluing_genus2_multicurve import (
    G20_PARAMETER_SETS,
    generate_genus2_multicurve_instance,
    recover_genus2_multicurve,
    validate_genus2_multicurve_witness,
)


MASTER_SEED = bytes.fromhex("47" * 32)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run MORPH-KEM G20 genus-two multicurve negative control."
    )
    parser.add_argument("--params", choices=sorted(G20_PARAMETER_SETS), default="g20-6x9")
    args = parser.parse_args()

    params = G20_PARAMETER_SETS[args.params]
    public, reference = generate_genus2_multicurve_instance(params, MASTER_SEED)
    recovery = recover_genus2_multicurve(
        public,
        reference=reference,
        successful_flips=params.successful_flips,
    )
    reference_validation = validate_genus2_multicurve_witness(public, reference.witness)

    print(f"parameters: {params.name}")
    print(f"torus rows/cols per handle: {params.rows}/{params.cols}")
    print(f"successful flips / generation retries: {recovery.successful_flips}/{recovery.generation_retries}")
    print(f"public V/E/F: {recovery.vertices}/{recovery.edges}/{recovery.triangles}")
    print(f"Euler characteristic: {recovery.euler_characteristic}")
    print(f"edge triangle incidence min/max: {recovery.min_triangles_per_edge}/{recovery.max_triangles_per_edge}")
    print(f"primal degree histogram: {recovery.primal_vertex_degree_histogram}")
    print(f"normalization-improving legal flips: {recovery.normalization_improving_flips}")
    print(f"H1 dimension: {recovery.h1_dimension}")
    print(f"alpha/beta weights: {recovery.alpha_weight}/{recovery.beta_weight}")
    print(f"public alpha/beta bounds: {recovery.max_alpha_length}/{recovery.max_beta_length}")
    print(f"reference alpha/beta lengths: {recovery.reference_alpha_length}/{recovery.reference_beta_length}")
    print(f"articulation points: {len(recovery.articulation_points)}")
    print(f"two-vertex separators: {recovery.two_vertex_separator_count}")
    print(f"separating primal triangles: {recovery.separating_triangle_count}")
    print(f"first separating triangle: {recovery.first_separating_triangle}")
    print(f"first separating component sizes: {recovery.first_separating_component_sizes}")
    print(f"four-sheet states: {recovery.four_sheet_states}")
    print(f"alpha roots/pops/scans: {recovery.alpha_roots}/{recovery.alpha_queue_pops}/{recovery.alpha_edge_scans}")
    print(f"alpha candidates: {recovery.alpha_candidates}")
    print(f"alpha length histogram: {recovery.alpha_length_histogram}")
    print(f"alpha candidates attempted: {recovery.alpha_candidates_attempted}")
    print(f"beta stage calls: {recovery.beta_stage_calls}")
    print(f"beta roots/reachable/pops/scans: {recovery.beta_roots}/{recovery.beta_reachable_roots}/{recovery.beta_queue_pops}/{recovery.beta_edge_scans}")
    print(f"beta candidates: {recovery.beta_candidates}")
    print(f"selected deleted vertices/edges: {recovery.selected_deleted_vertices}/{recovery.selected_deleted_edges}")
    print(f"selected alpha/beta lengths: {recovery.selected_alpha_length}/{recovery.selected_beta_length}")
    print(f"selected alpha signature: {recovery.selected_alpha_signature}")
    print(f"selected beta signature: {recovery.selected_beta_signature}")
    print(f"selected shared vertices: {recovery.selected_shared_vertices}")
    print(f"selected accepted: {recovery.selected_accepted}")
    print(f"selected matches reference: {recovery.selected_matches_reference}")
    print(f"independent alpha/beta cycles: {recovery.independent_alpha_cycles}/{recovery.independent_beta_cycles}")
    print(f"independent pair tests: {recovery.independent_pair_tests}")
    print(f"independent pair found/accepted: {recovery.independent_pair_found}/{recovery.independent_pair_accepted}")
    print(f"reference witness accepted: {reference_validation.valid}")

    return 0 if recovery.selected_accepted and reference_validation.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
