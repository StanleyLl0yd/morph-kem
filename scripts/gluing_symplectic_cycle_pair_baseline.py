#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.gluing_symplectic_cycle_pair import (
    G17_PARAMETER_SETS,
    generate_symplectic_cycle_pair_instance,
    recover_symplectic_cycle_pair,
)


FIXED_SEED = bytes.fromhex(
    "a7440102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e"
)


def _fmt(histogram: tuple[tuple[int, int], ...]) -> str:
    return "/".join(f"{value}:{count}" for value, count in histogram)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run MORPH-KEM G17 A-044 baseline.")
    parser.add_argument("--params", choices=sorted(G17_PARAMETER_SETS), default="g17-8x9")
    args = parser.parse_args()
    params = G17_PARAMETER_SETS[args.params]
    public, reference = generate_symplectic_cycle_pair_instance(params, FIXED_SEED)
    recovery = recover_symplectic_cycle_pair(
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
    print(f"primal tree edges: {recovery.primal_tree_edges}")
    print(f"dual cotree edges: {recovery.dual_cotree_edges}")
    print(f"forbidden dual edges: {recovery.forbidden_dual_edges}")
    print(f"tree-cotree leftover edges: {recovery.leftover_edges}")
    print(f"tree-cotree primal path scans: {recovery.treecotree_primal_path_scans}")
    print(f"tree-cotree dual path scans: {recovery.treecotree_dual_path_scans}")
    print(f"tree-cotree primal cycle length: {recovery.treecotree_primal_cycle_length}")
    print(f"tree-cotree dual cycle length: {recovery.treecotree_dual_cycle_length}")
    print(f"tree-cotree crossing count: {recovery.treecotree_crossing_count}")
    print(f"tree-cotree crossing parity: {recovery.treecotree_crossing_parity}")
    print(f"tree-cotree accepted: {recovery.treecotree_accepted}")
    print(f"tree-cotree matches reference: {recovery.treecotree_matches_reference}")
    print(f"full primal cycles: {recovery.full_primal_cycles}")
    print(f"full dual cycles: {recovery.full_dual_cycles}")
    print(
        "full primal cycle length histogram: "
        f"{_fmt(recovery.full_primal_cycle_length_histogram)}"
    )
    print(
        "full dual cycle length histogram: "
        f"{_fmt(recovery.full_dual_cycle_length_histogram)}"
    )
    print(f"full primal path scans: {recovery.full_primal_path_scans}")
    print(f"full dual path scans: {recovery.full_dual_path_scans}")
    print(
        "crossing matrix rows/cols: "
        f"{recovery.crossing_matrix_rows}/{recovery.crossing_matrix_cols}"
    )
    print(f"crossing matrix weight: {recovery.crossing_matrix_weight}")
    print(f"crossing matrix GF2 rank: {recovery.crossing_matrix_rank}")
    print(f"crossing matrix row XORs: {recovery.crossing_matrix_row_xors}")
    print(f"full-basis pairs tested: {recovery.full_basis_pairs_tested}")
    print(f"full-basis primal cycle length: {recovery.full_basis_primal_cycle_length}")
    print(f"full-basis dual cycle length: {recovery.full_basis_dual_cycle_length}")
    print(f"full-basis crossing count: {recovery.full_basis_crossing_count}")
    print(f"full-basis accepted: {recovery.full_basis_accepted}")

    ok = (
        recovery.euler_characteristic == 0
        and recovery.leftover_edges == 2
        and recovery.treecotree_crossing_count == 1
        and recovery.treecotree_accepted
        and recovery.crossing_matrix_rank == 2
        and recovery.full_basis_accepted
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
