#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib

from morph_kem.gluing_irregular_hypercover import (
    G12_PARAMETER_SETS,
    generate_irregular_hypercover_instance,
    recover_irregular_hypercover,
)
from morph_kem.gluing_surface_hypercover import toroidal_hypercover_incidence


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


def _seed(name: str, index: int) -> bytes:
    return hashlib.sha256(
        b"MORPH-KEM G12 sweep v1\x00"
        + MASTER_SEED
        + name.encode("ascii")
        + index.to_bytes(4, "big")
    ).digest()


def _fmt_histogram(histogram: tuple[tuple[int, int], ...]) -> str:
    return "/".join(f"{value}:{count}" for value, count in histogram)


def main() -> int:
    parser = argparse.ArgumentParser(description="Sweep MORPH-KEM G12 irregular P3 exact-cover recovery.")
    parser.add_argument("--seeds", type=int, default=8)
    parser.add_argument("--solution-cap", type=int, default=32)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 64:
        parser.error("--seeds must be in [1,64]")

    print(
        "set,seed,V,E,F,flips,retries,vertex_degree_hist,dual_bipartite,dual_edges,"
        "bridges,articulations,tri_cycles,four_cycles,signature_classes,signature_size_hist,"
        "improving_flips,candidates,membership_hist,overlap_hist,candidate_incidence,"
        "cover_solutions,cover_cap_hit,cover_nodes,cover_decisions,cover_backtracks,accepted,nonreference"
    )
    failures = 0
    for name in sorted(G12_PARAMETER_SETS):
        params = G12_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            public, reference = generate_irregular_hypercover_instance(params, _seed(name, seed_index))
            incidence = toroidal_hypercover_incidence(public)
            recovery = recover_irregular_hypercover(
                public, reference=reference, solution_cap=args.solution_cap
            )
            print(
                f"{name},{seed_index},{incidence.vertices},{incidence.edges},{incidence.triangles},"
                f"{reference.successful_flips},{reference.generation_retries},"
                f"{_fmt_histogram(recovery.primal_vertex_degree_histogram)},"
                f"{int(recovery.dual_bipartite)},{recovery.dual_edges},{recovery.bridge_count},"
                f"{len(recovery.articulation_points)},{recovery.dual_triangle_cycles},"
                f"{recovery.dual_four_cycles},{recovery.local_signature_classes},"
                f"{_fmt_histogram(recovery.local_signature_class_size_histogram)},"
                f"{recovery.normalization_improving_flips},{recovery.candidate_count},"
                f"{_fmt_histogram(recovery.candidate_membership_histogram)},"
                f"{_fmt_histogram(recovery.candidate_overlap_degree_histogram)},"
                f"{recovery.candidate_triangle_incidence},{recovery.exact_cover_solutions},"
                f"{int(recovery.exact_cover_cap_hit)},{recovery.exact_cover_nodes},"
                f"{recovery.exact_cover_decisions},{recovery.exact_cover_backtracks},"
                f"{recovery.accepted_solutions},{recovery.nonreference_accepted_solutions}"
            )
            triangle_count = incidence.triangles
            ok = (
                incidence.euler_characteristic == 0
                and incidence.min_triangles_per_edge == 2
                and incidence.max_triangles_per_edge == 2
                and recovery.dual_degree_histogram == ((3, triangle_count),)
                and recovery.bridge_count == 0
                and not recovery.articulation_points
                and len(recovery.primal_vertex_degree_histogram) > 1
                and recovery.local_signature_classes > 1
                and recovery.candidate_count > 0
                and recovery.accepted_solutions > 0
            )
            failures += int(not ok)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
