#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.gluing_genus2_same_side import (
    G22_PARAMETER_SETS,
    generate_same_side_instance,
    recover_same_side_witness,
)


MASTER_SEED = bytes.fromhex("a17e0405060708091011121314151617")


def _fmt_matrix(matrix: tuple[tuple[int, ...], ...]) -> str:
    return "/".join(",".join(str(value) for value in row) for row in matrix)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run MORPH-KEM G22 same-side genus-two multicurve control."
    )
    parser.add_argument("--params", choices=sorted(G22_PARAMETER_SETS), default="g22-6x9")
    args = parser.parse_args()
    params = G22_PARAMETER_SETS[args.params]
    public = generate_same_side_instance(params, MASTER_SEED)
    recovery = recover_same_side_witness(public)

    print(f"parameters: {params.name}")
    print(f"public V/E/F: {recovery.vertices}/{recovery.edges}/{recovery.triangles}")
    print(f"Euler characteristic: {recovery.euler_characteristic}")
    print(f"H1 dimension: {recovery.h1_dimension}")
    print(f"public cycle length bound: {public.max_cycle_length}")
    print(f"public spanning-tree samples: {recovery.tree_samples}")
    print(f"raw fundamental cycles: {recovery.raw_fundamental_cycles}")
    print(f"distinct bounded nonzero cycles: {recovery.distinct_cycles}")
    print(f"candidate signature histogram: {recovery.candidate_signature_histogram}")
    print(f"retained candidates: {recovery.retained_candidates}")
    print(f"exact-one candidate pairs: {recovery.exact_one_pairs}")
    print(f"pair-pair compatibility tests: {recovery.pair_pair_tests}")
    print(f"selected lengths: {recovery.selected_lengths}")
    print(f"selected signatures: {recovery.selected_signatures}")
    print(f"selected signature rank: {recovery.selected_rank}")
    print(f"selected vertex intersection matrix: {_fmt_matrix(recovery.selected_intersection_matrix)}")
    print(f"exact verifier accepted: {recovery.selected_accepted}")
    return 0 if recovery.selected_accepted and recovery.selected_rank == 4 else 1


if __name__ == "__main__":
    raise SystemExit(main())
