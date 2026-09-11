from __future__ import annotations

import argparse
import hashlib

from morph_kem.gluing_mixed_sphere import (
    G15_PARAMETER_SETS,
    generate_mixed_sphere_instance,
    recover_mixed_sphere,
)


def _seed(name: str, seed_index: int) -> bytes:
    return hashlib.sha256(
        b"MORPH-KEM G15 sweep v1\x00"
        + name.encode("ascii")
        + seed_index.to_bytes(4, "big")
    ).digest()


def _histogram_text(histogram: tuple[tuple[int, int], ...]) -> str:
    return "/".join(f"{value}:{count}" for value, count in histogram)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    parser.add_argument("--solution-cap", type=int, default=32)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 64:
        raise SystemExit("seed count outside toy bounds")

    print(
        "set,seed,growth,flips,rejected,retries,degree_hist,degree3,reverse_candidates,"
        "reverse_moves,reverse_terminal_F,reached_tetrahedron,improving_flips,dual_bipartite,"
        "tri_cycles,four_cycles,signature_classes,candidates,membership_hist,overlap_hist,"
        "incidence,cover_solutions,cap_hit,nodes,decisions,backtracks,accepted,nonreference"
    )
    for name, params in sorted(G15_PARAMETER_SETS.items()):
        for seed_index in range(args.seeds):
            public, reference = generate_mixed_sphere_instance(params, _seed(name, seed_index))
            recovery = recover_mixed_sphere(
                public, reference=reference, solution_cap=args.solution_cap
            )
            print(
                f"{name},{seed_index},{reference.growth_steps},{reference.successful_flips},"
                f"{reference.rejected_flip_proposals},{reference.generation_retries},"
                f"{_histogram_text(recovery.primal_vertex_degree_histogram)},"
                f"{recovery.initial_degree_three_vertices},{recovery.initial_reverse_candidates},"
                f"{recovery.reverse_moves},{recovery.reverse_terminal_triangles},"
                f"{int(recovery.reverse_reached_tetrahedron)},"
                f"{recovery.normalization_improving_flips},{int(recovery.dual_bipartite)},"
                f"{recovery.dual_triangle_cycles},{recovery.dual_four_cycles},"
                f"{recovery.local_signature_classes},{recovery.candidate_count},"
                f"{_histogram_text(recovery.candidate_membership_histogram)},"
                f"{_histogram_text(recovery.candidate_overlap_degree_histogram)},"
                f"{recovery.candidate_triangle_incidence},{recovery.exact_cover_solutions},"
                f"{int(recovery.exact_cover_cap_hit)},{recovery.exact_cover_nodes},"
                f"{recovery.exact_cover_decisions},{recovery.exact_cover_backtracks},"
                f"{recovery.accepted_solutions},{recovery.nonreference_accepted_solutions}"
            )


if __name__ == "__main__":
    main()
