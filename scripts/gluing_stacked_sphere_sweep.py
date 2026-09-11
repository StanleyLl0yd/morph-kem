#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib

from morph_kem.gluing_stacked_sphere import (
    G14_PARAMETER_SETS,
    run_stacked_sphere_experiment,
)


MASTER_SEED = bytes.fromhex("76140450aabbccddeeff001122334455")


def _seed(name: str, index: int) -> bytes:
    return hashlib.sha256(
        b"MORPH-KEM G14 sweep v1\x00"
        + MASTER_SEED
        + name.encode("ascii")
        + index.to_bytes(4, "big")
    ).digest()


def _fmt_histogram(histogram: tuple[tuple[int, int], ...]) -> str:
    return "/".join(f"{value}:{count}" for value, count in histogram)


def _fmt_counts(counts: tuple[int, ...]) -> str:
    return "/".join(map(str, counts))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sweep MORPH-KEM G14 stacked-sphere reverse normalization."
    )
    parser.add_argument("--seeds", type=int, default=8)
    parser.add_argument("--solution-cap", type=int, default=32)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 64:
        parser.error("--seeds must be in [1,64]")

    print(
        "set,seed,stack_steps,V,E,F,degree_hist,degree3,reverse_moves,reverse_candidates,"
        "max_reverse_candidates,terminal_V,terminal_E,terminal_F,reached_tetrahedron,"
        "dual_edges,dual_bipartite,bridges,articulations,candidates,membership_hist,"
        "overlap_hist,candidate_incidence,reference_available,cover_solutions,cap_hit,"
        "cover_nodes,cover_decisions,cover_backtracks,accepted,nonreference"
    )
    failures = 0
    for name in sorted(G14_PARAMETER_SETS):
        params = G14_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            result = run_stacked_sphere_experiment(
                params, _seed(name, seed_index), solution_cap=args.solution_cap
            )
            norm = result.normalization
            recovery = result.hypercover
            print(
                f"{name},{seed_index},{params.stacking_steps},{norm.initial_vertices},"
                f"{norm.initial_edges},{norm.initial_triangles},"
                f"{_fmt_histogram(norm.initial_degree_histogram)},{norm.initial_degree_three_vertices},"
                f"{norm.reverse_moves},{_fmt_counts(norm.candidate_counts)},{norm.max_candidates},"
                f"{norm.terminal_vertices},{norm.terminal_edges},{norm.terminal_triangles},"
                f"{int(norm.reached_tetrahedron_boundary)},{recovery.dual_edges},"
                f"{int(recovery.dual_bipartite)},{recovery.bridge_count},"
                f"{len(recovery.articulation_points)},{recovery.candidate_count},"
                f"{_fmt_histogram(recovery.candidate_membership_histogram)},"
                f"{_fmt_histogram(recovery.candidate_overlap_degree_histogram)},"
                f"{recovery.candidate_triangle_incidence},{int(recovery.reference_available)},"
                f"{recovery.exact_cover_solutions},{int(recovery.exact_cover_cap_hit)},"
                f"{recovery.exact_cover_nodes},{recovery.exact_cover_decisions},"
                f"{recovery.exact_cover_backtracks},{recovery.accepted_solutions},"
                f"{recovery.nonreference_accepted_solutions}"
            )
            ok = (
                norm.reverse_moves == params.stacking_steps
                and norm.reached_tetrahedron_boundary
                and (norm.terminal_vertices, norm.terminal_edges, norm.terminal_triangles)
                == (4, 6, 4)
            )
            failures += int(not ok)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
