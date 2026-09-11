#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.gluing_cohomology_cycle import (
    G16_PARAMETER_SETS,
    generate_cohomology_cycle_instance,
    recover_cohomology_cycle,
)


MASTER_SEED = bytes.fromhex("76160450aabbccddeeff001122334455")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the MORPH-KEM G16 nonlocal cohomology-cycle negative control."
    )
    parser.add_argument("--params", choices=sorted(G16_PARAMETER_SETS), default="g16-8x9")
    args = parser.parse_args()

    params = G16_PARAMETER_SETS[args.params]
    public, reference = generate_cohomology_cycle_instance(params, MASTER_SEED)
    recovery = recover_cohomology_cycle(
        public, reference=reference, successful_flips=params.successful_flips
    )

    print(f"parameters: {params.name}")
    print(f"successful carrier flips: {recovery.successful_flips}")
    print(f"public V/E/F: {recovery.vertices}/{recovery.edges}/{recovery.triangles}")
    print(f"Euler characteristic: {recovery.euler_characteristic}")
    print(
        "edge triangle incidence min/max: "
        f"{recovery.min_triangles_per_edge}/{recovery.max_triangles_per_edge}"
    )
    print(f"primal degree histogram: {recovery.primal_vertex_degree_histogram}")
    print(f"normalization-improving legal flips: {recovery.normalization_improving_flips}")
    print(f"cycle equations/variables: {recovery.cycle_equations}/{recovery.cycle_variables}")
    print(f"cycle rank/nullity: {recovery.cycle_rank}/{recovery.cycle_nullity}")
    print(f"cycle-space row XORs: {recovery.cycle_row_xors}")
    print(f"cocycle equations/rank: {recovery.cocycle_equations}/{recovery.cocycle_rank}")
    print(f"cocycle dimension: {recovery.cocycle_dimension}")
    print(f"coboundary rank / H1 dimension: {recovery.coboundary_rank}/{recovery.h1_dimension}")
    print(f"cocycle row XORs: {recovery.cocycle_row_xors}")
    print(f"public alpha weight: {recovery.alpha_weight}")
    print(f"tree/non-tree edges: {recovery.tree_edges}/{recovery.non_tree_edges}")
    print(f"fundamental cycles tested: {recovery.fundamental_cycles_tested}")
    print(f"fundamental path-edge scans: {recovery.fundamental_path_edge_scans}")
    print(f"selected odd cycle length: {recovery.selected_cycle_length}")
    print(f"selected cycle accepted: {recovery.selected_cycle_accepted}")
    print(f"selected cycle matches reference: {recovery.selected_cycle_matches_reference}")
    print(f"affine rank/nullity: {recovery.affine_rank}/{recovery.affine_nullity}")
    print(f"affine row XORs: {recovery.affine_row_xors}")
    print(f"affine support edges: {recovery.affine_support_edges}")
    print(f"affine support cycles tested: {recovery.affine_cycles_tested}")
    print(f"affine selected cycle length: {recovery.affine_selected_cycle_length}")
    print(f"affine selected cycle accepted: {recovery.affine_cycle_accepted}")

    return 0 if recovery.selected_cycle_accepted and recovery.affine_cycle_accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
