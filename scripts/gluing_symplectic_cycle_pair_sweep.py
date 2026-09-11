#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib

from morph_kem.gluing_symplectic_cycle_pair import (
    G17_PARAMETER_SETS,
    generate_symplectic_cycle_pair_instance,
    recover_symplectic_cycle_pair,
)


MASTER_SEED = bytes.fromhex("a74455aa11223344556677889900aabb")


def _seed(name: str, index: int) -> bytes:
    return hashlib.sha256(
        b"MORPH-KEM G17 sweep v1\x00"
        + MASTER_SEED
        + name.encode("ascii")
        + index.to_bytes(4, "big")
    ).digest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Sweep MORPH-KEM G17 A-044 recovery.")
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 64:
        parser.error("--seeds must be in [1,64]")

    print(
        "set,seed,V,E,F,improving_flips,primal_tree,dual_tree,leftovers,"
        "primary_p_scans,primary_d_scans,primary_p_len,primary_d_len,crossings,accepted,"
        "matches_reference,primal_basis,dual_basis,matrix_weight,matrix_rank,matrix_xors,"
        "basis_pairs,basis_p_len,basis_d_len,basis_crossings,basis_accepted"
    )
    failures = 0
    for name in sorted(G17_PARAMETER_SETS):
        params = G17_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            public, reference = generate_symplectic_cycle_pair_instance(
                params, _seed(name, seed_index)
            )
            recovery = recover_symplectic_cycle_pair(
                public, reference=reference, successful_flips=params.successful_flips
            )
            print(
                f"{name},{seed_index},{recovery.vertices},{recovery.edges},{recovery.triangles},"
                f"{recovery.normalization_improving_flips},{recovery.primal_tree_edges},"
                f"{recovery.dual_cotree_edges},{recovery.leftover_edges},"
                f"{recovery.treecotree_primal_path_scans},{recovery.treecotree_dual_path_scans},"
                f"{recovery.treecotree_primal_cycle_length},{recovery.treecotree_dual_cycle_length},"
                f"{recovery.treecotree_crossing_count},{int(recovery.treecotree_accepted)},"
                f"{'' if recovery.treecotree_matches_reference is None else int(recovery.treecotree_matches_reference)},"
                f"{recovery.full_primal_cycles},{recovery.full_dual_cycles},"
                f"{recovery.crossing_matrix_weight},{recovery.crossing_matrix_rank},"
                f"{recovery.crossing_matrix_row_xors},{recovery.full_basis_pairs_tested},"
                f"{recovery.full_basis_primal_cycle_length},{recovery.full_basis_dual_cycle_length},"
                f"{recovery.full_basis_crossing_count},{int(recovery.full_basis_accepted)}"
            )
            ok = (
                recovery.euler_characteristic == 0
                and recovery.leftover_edges == 2
                and recovery.treecotree_crossing_count == 1
                and recovery.treecotree_accepted
                and recovery.crossing_matrix_rank == 2
                and recovery.full_basis_accepted
            )
            failures += int(not ok)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
