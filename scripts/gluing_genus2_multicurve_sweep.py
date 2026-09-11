#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib

from morph_kem.gluing_genus2_multicurve import (
    G20_PARAMETER_SETS,
    generate_genus2_multicurve_instance,
    recover_genus2_multicurve,
)


MASTER_SEED = bytes.fromhex("47" * 32)


def _seed(name: str, index: int) -> bytes:
    return hashlib.sha256(
        b"MORPH-KEM G20 sweep v1\x00"
        + MASTER_SEED
        + name.encode("ascii")
        + index.to_bytes(4, "big")
    ).digest()


def _hist(values: tuple[tuple[int, int], ...]) -> str:
    return "/".join(f"{value}:{count}" for value, count in values)


def main() -> int:
    parser = argparse.ArgumentParser(description="Sweep MORPH-KEM G20 A-047 recovery.")
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 32:
        parser.error("--seeds must be in [1,32]")

    print(
        "set,seed,V,E,F,retries,H1,alpha_weight,beta_weight,alpha_bound,beta_bound,"
        "articulations,two_sep,separating_triangles,alpha_candidates,alpha_attempted,"
        "beta_calls,beta_scans,selected_alpha,selected_beta,shared,accepted,nonreference,"
        "independent_found,independent_accepted"
    )
    failures = 0
    for name in sorted(G20_PARAMETER_SETS):
        params = G20_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            public, reference = generate_genus2_multicurve_instance(
                params, _seed(name, seed_index)
            )
            recovery = recover_genus2_multicurve(
                public,
                reference=reference,
                successful_flips=params.successful_flips,
            )
            nonreference = int(recovery.selected_matches_reference is False)
            print(
                f"{name},{seed_index},{recovery.vertices},{recovery.edges},{recovery.triangles},"
                f"{recovery.generation_retries},{recovery.h1_dimension},"
                f"{recovery.alpha_weight},{recovery.beta_weight},"
                f"{recovery.max_alpha_length},{recovery.max_beta_length},"
                f"{len(recovery.articulation_points)},{recovery.two_vertex_separator_count},"
                f"{recovery.separating_triangle_count},{recovery.alpha_candidates},"
                f"{recovery.alpha_candidates_attempted},{recovery.beta_stage_calls},"
                f"{recovery.beta_edge_scans},{recovery.selected_alpha_length},"
                f"{recovery.selected_beta_length},{recovery.selected_shared_vertices},"
                f"{int(recovery.selected_accepted)},{nonreference},"
                f"{int(recovery.independent_pair_found)},{int(recovery.independent_pair_accepted)}"
            )
            ok = (
                recovery.euler_characteristic == -2
                and recovery.min_triangles_per_edge == 2
                and recovery.max_triangles_per_edge == 2
                and recovery.h1_dimension == 4
                and recovery.selected_alpha_signature == (1, 0)
                and recovery.selected_beta_signature == (0, 1)
                and recovery.selected_shared_vertices == 0
                and recovery.selected_alpha_length <= recovery.max_alpha_length
                and recovery.selected_beta_length <= recovery.max_beta_length
                and recovery.selected_accepted
                and recovery.selected_matches_reference is False
            )
            failures += int(not ok)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
