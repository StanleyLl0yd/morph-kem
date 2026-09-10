#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time

from morph_kem.morse import validate_morse_matching
from morph_kem.nonmanifold import (
    NONMANIFOLD_PARAMETER_SETS,
    bounded_tree_extension_search,
    generate_nonmanifold_instance,
    greedy_witness_survey,
    incidence_metrics,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the MORPH M5 irregular non-manifold baseline.")
    parser.add_argument("--params", choices=sorted(NONMANIFOLD_PARAMETER_SETS), default="m5-8")
    parser.add_argument("--greedy-trials", type=int, default=32)
    parser.add_argument("--tree-trials", type=int, default=4)
    parser.add_argument("--max-nodes", type=int, default=20000)
    parser.add_argument(
        "--master-seed",
        default="50126490aabbccddeeff1234567890ab",
        help="hex-encoded deterministic M5 generation seed",
    )
    args = parser.parse_args()

    parameters = NONMANIFOLD_PARAMETER_SETS[args.params]
    public, reference = generate_nonmanifold_instance(parameters, bytes.fromhex(args.master_seed))
    metrics = incidence_metrics(public.target)
    planted = validate_morse_matching(public.target, reference.matching, public.critical_target)

    greedy_started = time.perf_counter()
    greedy = greedy_witness_survey(public, trials=args.greedy_trials)
    greedy_elapsed = time.perf_counter() - greedy_started

    search_started = time.perf_counter()
    search = bounded_tree_extension_search(
        public,
        tree_trials=args.tree_trials,
        max_nodes=args.max_nodes,
    )
    search_elapsed = time.perf_counter() - search_started

    print(f"parameters: {parameters.name}")
    print(f"V/E/F: {metrics.vertices}/{metrics.edges}/{metrics.triangles}")
    print(f"edge triangle incidence min/max: {metrics.min_triangles_per_edge}/{metrics.max_triangles_per_edge}")
    print(f"incidence histogram: {metrics.incidence_histogram}")
    print(f"free collapse pairs: {metrics.free_collapse_pairs}")
    print(f"critical target: {public.critical_target}")
    print(f"reference accepted: {planted.valid}")
    print(f"greedy target hits: {greedy.target_hits}/{greedy.trials}")
    print(f"greedy unique vectors: {greedy.unique_vectors}")
    print(f"greedy unique target matchings: {greedy.unique_target_matchings}")
    print(f"greedy best/mean total critical: {greedy.best_total_critical}/{greedy.mean_total_critical:.2f}")
    print(f"greedy elapsed seconds: {greedy_elapsed:.6f}")
    print(f"bounded extension found: {search.found}")
    print(f"bounded extension nodes/tree-trials: {search.nodes}/{search.tree_trials}")
    print(f"bounded extension exhausted: {search.exhausted}")
    print(f"bounded extension elapsed seconds: {search_elapsed:.6f}")
    return 0 if planted.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
