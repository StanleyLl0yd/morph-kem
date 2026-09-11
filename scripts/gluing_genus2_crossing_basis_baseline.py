#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.gluing_genus2_crossing_basis import (
    G21_PARAMETER_SETS,
    generate_genus2_crossing_basis_instance,
    recover_genus2_crossing_basis,
)


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


def _fmt_matrix(matrix: tuple[tuple[int, ...], ...]) -> str:
    return "/".join(",".join(str(value) for value in row) for row in matrix)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the MORPH-KEM G21 genus-two full crossing-matrix negative control."
    )
    parser.add_argument("--params", choices=sorted(G21_PARAMETER_SETS), default="g21-6x9")
    args = parser.parse_args()

    params = G21_PARAMETER_SETS[args.params]
    public = generate_genus2_crossing_basis_instance(params, MASTER_SEED)
    recovery = recover_genus2_crossing_basis(
        public, successful_flips=params.successful_flips
    )

    print(f"parameters: {params.name}")
    print(f"torus rows/cols per handle: {params.rows}/{params.cols}")
    print(f"successful flips: {recovery.successful_flips}")
    print(f"public V/E/F: {recovery.vertices}/{recovery.edges}/{recovery.triangles}")
    print(f"Euler characteristic: {recovery.euler_characteristic}")
    print(
        "edge triangle incidence min/max: "
        f"{recovery.min_triangles_per_edge}/{recovery.max_triangles_per_edge}"
    )
    print(f"H1 dimension: {recovery.h1_dimension}")
    print(f"primal degree histogram: {recovery.primal_vertex_degree_histogram}")
    print(f"dual degree histogram: {recovery.dual_vertex_degree_histogram}")
    print(f"normalization-improving legal flips: {recovery.normalization_improving_flips}")
    print(f"primal tree edges: {recovery.primal_tree_edges}")
    print(f"forbidden dual edges: {recovery.forbidden_dual_edges}")
    print(f"dual cotree edges: {recovery.dual_cotree_edges}")
    print(f"tree-cotree leftovers: {recovery.leftover_edges}")
    print(f"primal/dual path scans: {recovery.primal_path_scans}/{recovery.dual_path_scans}")
    print(f"primal cycle lengths: {recovery.primal_cycle_lengths}")
    print(f"dual cycle lengths: {recovery.dual_cycle_lengths}")
    print(f"exact crossing matrix: {_fmt_matrix(recovery.exact_crossing_matrix)}")
    print(f"off-diagonal nonzero entries: {recovery.off_diagonal_nonzero}")
    print(f"exact verifier accepted: {recovery.exact_verifier_accepted}")
    print(f"full primal/dual basis cycles: {recovery.full_primal_cycles}/{recovery.full_dual_cycles}")
    print(
        "full primal/dual path scans: "
        f"{recovery.full_primal_path_scans}/{recovery.full_dual_path_scans}"
    )
    print(
        "full crossing matrix rows/cols/weight/rank/xors: "
        f"{recovery.full_crossing_matrix_rows}/{recovery.full_crossing_matrix_cols}/"
        f"{recovery.full_crossing_matrix_weight}/{recovery.full_crossing_matrix_rank}/"
        f"{recovery.full_crossing_matrix_row_xors}"
    )

    return 0 if (
        recovery.euler_characteristic == -2
        and recovery.h1_dimension == 4
        and recovery.leftover_edges == 4
        and recovery.off_diagonal_nonzero == 0
        and recovery.exact_verifier_accepted
        and recovery.full_crossing_matrix_rank == 4
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
