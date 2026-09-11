#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib

from morph_kem.gluing_disjoint_cohomology_pair import (
    G19_PARAMETER_SETS,
    generate_disjoint_cohomology_pair_instance,
    recover_disjoint_cohomology_pair,
)


MASTER_SEED = bytes.fromhex("a74655aa11223344556677889900aabb")


def _seed(name: str, index: int) -> bytes:
    return hashlib.sha256(
        b"MORPH-KEM G19 sweep v1\x00"
        + MASTER_SEED
        + name.encode("ascii")
        + index.to_bytes(4, "big")
    ).digest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Sweep MORPH-KEM G19 A-046 recovery.")
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 64:
        parser.error("--seeds must be in [1,64]")

    print(
        "set,seed,V,E,F,retries,reference_tree_attempts,L1,L2,ref1,ref2,alpha_weight,h1,"
        "first_candidates,first_attempted,second_calls,second_roots,second_reachable,"
        "second_pops,second_scans,second_candidates,deleted_vertices,deleted_edges,"
        "selected1,selected2,pairing1,pairing2,shared,accepted,matches_reference,"
        "independent_cycles,independent_tests,independent_found,independent_accepted"
    )
    failures = 0
    for name in sorted(G19_PARAMETER_SETS):
        params = G19_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            public, reference = generate_disjoint_cohomology_pair_instance(
                params, _seed(name, seed_index)
            )
            recovery = recover_disjoint_cohomology_pair(
                public,
                reference=reference,
                successful_flips=params.successful_flips,
            )
            print(
                f"{name},{seed_index},{recovery.vertices},{recovery.edges},{recovery.triangles},"
                f"{recovery.generation_retries},{reference.reference_tree_attempts},"
                f"{recovery.max_short_length},{recovery.max_long_length},"
                f"{recovery.reference_short_length},{recovery.reference_long_length},"
                f"{recovery.alpha_weight},{recovery.h1_dimension},"
                f"{recovery.first_stage_candidates},{recovery.first_candidates_attempted},"
                f"{recovery.second_stage_calls},{recovery.second_stage_roots},"
                f"{recovery.second_stage_reachable_roots},{recovery.second_stage_queue_pops},"
                f"{recovery.second_stage_edge_scans},{recovery.second_stage_candidates},"
                f"{recovery.selected_deleted_vertices},{recovery.selected_deleted_edges},"
                f"{recovery.selected_short_length},{recovery.selected_long_length},"
                f"{recovery.selected_first_pairing},{recovery.selected_second_pairing},"
                f"{recovery.selected_shared_vertices},{int(recovery.selected_accepted)},"
                f"{'' if recovery.selected_matches_reference is None else int(recovery.selected_matches_reference)},"
                f"{recovery.independent_odd_fundamental_cycles},{recovery.independent_pair_tests},"
                f"{int(recovery.independent_pair_found)},{int(recovery.independent_pair_accepted)}"
            )
            ok = (
                recovery.euler_characteristic == 0
                and recovery.h1_dimension == 2
                and recovery.selected_accepted
                and recovery.selected_shared_vertices == 0
                and recovery.selected_first_pairing == 1
                and recovery.selected_second_pairing == 1
                and recovery.selected_short_length <= recovery.max_short_length
                and recovery.selected_long_length <= recovery.max_long_length
            )
            failures += int(not ok)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
