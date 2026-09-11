#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib

from morph_kem.gluing_length_bounded_pair import (
    G18_PARAMETER_SETS,
    generate_length_bounded_pair_instance,
    recover_length_bounded_pair,
)


MASTER_SEED = bytes.fromhex("a74555aa11223344556677889900aabb")


def _seed(name: str, index: int) -> bytes:
    return hashlib.sha256(
        b"MORPH-KEM G18 sweep v1\x00"
        + MASTER_SEED
        + name.encode("ascii")
        + index.to_bytes(4, "big")
    ).digest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Sweep MORPH-KEM G18 A-045 recovery.")
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 64:
        parser.error("--seeds must be in [1,64]")

    print(
        "set,seed,V,E,F,Lp,Ld,ref_p,ref_d,alpha_weight,h1,cover_roots,cover_pops,"
        "cover_scans,min_walk,min_support,decomp_cycles,decomp_scans,primal_candidates,"
        "within_bound,connector_calls,connector_pops,connector_scans,selected_p,selected_d,"
        "crossings,accepted,matches_reference,treecotree_p,treecotree_d,treecotree_within,"
        "treecotree_accepted"
    )
    failures = 0
    for name in sorted(G18_PARAMETER_SETS):
        params = G18_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            public, reference = generate_length_bounded_pair_instance(
                params, _seed(name, seed_index)
            )
            recovery = recover_length_bounded_pair(
                public, reference=reference, successful_flips=params.successful_flips
            )
            print(
                f"{name},{seed_index},{recovery.vertices},{recovery.edges},{recovery.triangles},"
                f"{recovery.max_primal_length},{recovery.max_dual_length},"
                f"{recovery.reference_primal_length},{recovery.reference_dual_length},"
                f"{recovery.alpha_weight},{recovery.h1_dimension},{recovery.cover_roots_attempted},"
                f"{recovery.cover_queue_pops},{recovery.cover_edge_scans},{recovery.cover_walk_length_min},"
                f"{recovery.cover_support_edges_min},{recovery.decomposition_cycles_tested},"
                f"{recovery.decomposition_path_scans},{recovery.distinct_primal_candidates},"
                f"{recovery.primal_candidates_within_bound},{recovery.dual_connector_calls},"
                f"{recovery.dual_connector_queue_pops},{recovery.dual_connector_edge_scans},"
                f"{recovery.selected_primal_length},{recovery.selected_dual_length},"
                f"{recovery.selected_crossing_count},{int(recovery.selected_accepted)},"
                f"{'' if recovery.selected_matches_reference is None else int(recovery.selected_matches_reference)},"
                f"{recovery.canonical_treecotree_primal_length},{recovery.canonical_treecotree_dual_length},"
                f"{int(recovery.canonical_treecotree_within_bounds)},"
                f"{int(recovery.canonical_treecotree_accepted)}"
            )
            ok = (
                recovery.euler_characteristic == 0
                and recovery.h1_dimension == 2
                and recovery.selected_crossing_count == 1
                and recovery.selected_accepted
                and recovery.selected_primal_length <= recovery.max_primal_length
                and recovery.selected_dual_length <= recovery.max_dual_length
            )
            failures += int(not ok)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
