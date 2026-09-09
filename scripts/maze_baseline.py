#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time

from morph_kem.maze import (
    MAZE_PARAMETER_SETS,
    bounded_core_search,
    generate_maze,
    greedy_reduce,
    planted_reduction_metrics,
    random_greedy_survey,
    recover_three_regular_core,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the MORPH-KEM M2 collapse-maze baseline.")
    parser.add_argument("--params", choices=sorted(MAZE_PARAMETER_SETS), default="maze-6")
    parser.add_argument("--trials", type=int, default=32)
    parser.add_argument("--search-nodes", type=int, default=10_000)
    parser.add_argument(
        "--master-seed",
        default="31415926535897932384626433832795",
        help="hex-encoded deterministic instance-generation seed",
    )
    args = parser.parse_args()

    public, trapdoor = generate_maze(
        MAZE_PARAMETER_SETS[args.params],
        bytes.fromhex(args.master_seed),
    )
    planted = planted_reduction_metrics(public, trapdoor)
    lex = greedy_reduce(public, strategy="lex")
    reverse = greedy_reduce(public, strategy="reverse")
    survey = random_greedy_survey(
        public,
        trials=args.trials,
        attack_seed=b"M2-baseline-survey",
    )

    started = time.perf_counter()
    search = bounded_core_search(public, max_nodes=args.search_nodes)
    search_elapsed = time.perf_counter() - started

    started = time.perf_counter()
    core_recovery = recover_three_regular_core(public, max_nodes=max(args.search_nodes, 100_000))
    core_recovery_elapsed = time.perf_counter() - started

    print(f"parameters: {args.params}")
    print(f"target simplices: {len(public.target.simplices)}")
    print(f"hidden core simplices: {len(trapdoor.core.simplices)}")
    print(f"planted steps: {planted.steps}")
    print(f"initial free pairs: {planted.initial_free_pairs}")
    print(f"planted free pairs min/mean/max: {planted.min_free_pairs}/{planted.mean_free_pairs:.2f}/{planted.max_free_pairs}")
    print(f"mean planted choice rank: {planted.mean_planted_rank:.2f}")
    print(f"lex greedy: collapses={lex.collapses} core_hit={lex.verified_core} residual_simplices={len(lex.residual.simplices)}")
    print(f"reverse greedy: collapses={reverse.collapses} core_hit={reverse.verified_core} residual_simplices={len(reverse.residual.simplices)}")
    print(f"random survey: trials={survey.trials} core_hits={survey.core_hits} unique_residuals={survey.unique_residuals}")
    print(f"random residual simplex range: {survey.min_residual_simplices}..{survey.max_residual_simplices}")
    print(f"random mean collapses: {survey.mean_collapses:.2f}")
    print(f"bounded search: found={search.found} nodes={search.nodes} visited={search.visited_states} max_frontier={search.max_frontier}")
    print(f"bounded search elapsed seconds: {search_elapsed:.6f}")
    print(f"degree-core recovery: found={core_recovery.found} nodes={core_recovery.nodes} candidates={core_recovery.degree_candidates} forced_edges={core_recovery.forced_edges} optional_edges={core_recovery.optional_edges}")
    print(f"degree-core recovery elapsed seconds: {core_recovery_elapsed:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
