#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib

from morph_kem.gluing_cohomology_cycle import (
    G16_PARAMETER_SETS,
    generate_cohomology_cycle_instance,
    recover_cohomology_cycle,
)


MASTER_SEED = bytes.fromhex("76160450aabbccddeeff001122334455")


def _seed(name: str, index: int) -> bytes:
    return hashlib.sha256(
        b"MORPH-KEM G16 sweep v1\x00"
        + MASTER_SEED
        + name.encode("ascii")
        + index.to_bytes(4, "big")
    ).digest()


def _fmt_histogram(histogram: tuple[tuple[int, int], ...]) -> str:
    return "/".join(f"{value}:{count}" for value, count in histogram)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sweep MORPH-KEM G16 public fundamental-cycle recovery."
    )
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 64:
        parser.error("--seeds must be in [1,64]")

    print(
        "set,seed,V,E,F,degree_hist,improving_flips,cycle_rank,cycle_nullity,cycle_xors,"
        "cocycle_rank,cocycle_dim,coboundary_rank,h1_dim,cocycle_xors,alpha_weight,"
        "tree_edges,non_tree_edges,cycles_tested,path_scans,cycle_len,accepted,matches_reference,"
        "affine_rank,affine_nullity,affine_xors,affine_support,affine_cycles_tested,"
        "affine_cycle_len,affine_accepted"
    )
    failures = 0
    for name in sorted(G16_PARAMETER_SETS):
        params = G16_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            public, reference = generate_cohomology_cycle_instance(
                params, _seed(name, seed_index)
            )
            recovery = recover_cohomology_cycle(
                public, reference=reference, successful_flips=params.successful_flips
            )
            print(
                f"{name},{seed_index},{recovery.vertices},{recovery.edges},{recovery.triangles},"
                f"{_fmt_histogram(recovery.primal_vertex_degree_histogram)},"
                f"{recovery.normalization_improving_flips},{recovery.cycle_rank},"
                f"{recovery.cycle_nullity},{recovery.cycle_row_xors},{recovery.cocycle_rank},"
                f"{recovery.cocycle_dimension},{recovery.coboundary_rank},{recovery.h1_dimension},"
                f"{recovery.cocycle_row_xors},{recovery.alpha_weight},{recovery.tree_edges},"
                f"{recovery.non_tree_edges},{recovery.fundamental_cycles_tested},"
                f"{recovery.fundamental_path_edge_scans},{recovery.selected_cycle_length},"
                f"{int(recovery.selected_cycle_accepted)},"
                f"{'' if recovery.selected_cycle_matches_reference is None else int(recovery.selected_cycle_matches_reference)},"
                f"{recovery.affine_rank},{recovery.affine_nullity},{recovery.affine_row_xors},"
                f"{recovery.affine_support_edges},{recovery.affine_cycles_tested},"
                f"{recovery.affine_selected_cycle_length},{int(recovery.affine_cycle_accepted)}"
            )
            ok = (
                recovery.euler_characteristic == 0
                and recovery.h1_dimension == 2
                and recovery.selected_cycle_accepted
                and recovery.affine_cycle_accepted
            )
            failures += int(not ok)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
