#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib

from morph_kem.gluing_genus2_crossing_basis import (
    G21_PARAMETER_SETS,
    generate_genus2_crossing_basis_instance,
    recover_genus2_crossing_basis,
)


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


def _seed(name: str, index: int) -> bytes:
    return hashlib.sha256(
        b"MORPH-KEM G21 sweep v1\x00"
        + MASTER_SEED
        + name.encode("ascii")
        + index.to_bytes(4, "big")
    ).digest()


def _fmt(values: tuple[int, ...]) -> str:
    return "/".join(str(value) for value in values)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sweep MORPH-KEM G21 public full crossing-matrix recovery."
    )
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 64:
        parser.error("--seeds must be in [1,64]")

    print(
        "set,seed,V,E,F,H1,leftovers,primal_scans,dual_scans,primal_lengths,dual_lengths,"
        "offdiag,accepted,full_primal,full_dual,full_weight,full_rank,full_xors"
    )
    failures = 0
    for name in sorted(G21_PARAMETER_SETS):
        params = G21_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            public = generate_genus2_crossing_basis_instance(
                params, _seed(name, seed_index)
            )
            recovery = recover_genus2_crossing_basis(
                public, successful_flips=params.successful_flips
            )
            print(
                f"{name},{seed_index},{recovery.vertices},{recovery.edges},{recovery.triangles},"
                f"{recovery.h1_dimension},{recovery.leftover_edges},"
                f"{recovery.primal_path_scans},{recovery.dual_path_scans},"
                f"{_fmt(recovery.primal_cycle_lengths)},{_fmt(recovery.dual_cycle_lengths)},"
                f"{recovery.off_diagonal_nonzero},{int(recovery.exact_verifier_accepted)},"
                f"{recovery.full_primal_cycles},{recovery.full_dual_cycles},"
                f"{recovery.full_crossing_matrix_weight},{recovery.full_crossing_matrix_rank},"
                f"{recovery.full_crossing_matrix_row_xors}"
            )
            identity = tuple(
                tuple(1 if row == column else 0 for column in range(4))
                for row in range(4)
            )
            ok = (
                recovery.euler_characteristic == -2
                and recovery.min_triangles_per_edge == 2
                and recovery.max_triangles_per_edge == 2
                and recovery.h1_dimension == 4
                and recovery.leftover_edges == 4
                and recovery.exact_crossing_matrix == identity
                and recovery.off_diagonal_nonzero == 0
                and recovery.exact_verifier_accepted
                and recovery.full_crossing_matrix_rank == 4
            )
            failures += int(not ok)

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
