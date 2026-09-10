#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time

from morph_kem.pachner import (
    PACHNER_PARAMETER_SETS,
    bfs_pachner_recover,
    bidirectional_pachner_recover,
    generate_pachner_instance,
    pachner_path_metrics,
    verify_pachner_witness,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the MORPH T0 bounded Pachner search baseline.")
    parser.add_argument("--params", choices=sorted(PACHNER_PARAMETER_SETS), default="t0-8")
    parser.add_argument("--max-states", type=int, default=20_000)
    parser.add_argument("--master-seed", default="48026490aabbccddeeff1029384756aa")
    args = parser.parse_args()

    public, reference = generate_pachner_instance(PACHNER_PARAMETER_SETS[args.params], bytes.fromhex(args.master_seed))
    metrics = pachner_path_metrics(public, reference)

    started = time.perf_counter(); bfs = bfs_pachner_recover(public, args.max_states); bfs_elapsed = time.perf_counter() - started
    started = time.perf_counter(); bidir = bidirectional_pachner_recover(public, args.max_states); bidir_elapsed = time.perf_counter() - started

    print(f"parameters: {args.params}")
    print(f"start vertices/tetrahedra: {len(public.start.vertices)}/{public.start.tetrahedra}")
    print(f"target vertices/tetrahedra: {len(public.target.vertices)}/{public.target.tetrahedra}")
    print(f"Euler start/target: {public.start.euler_characteristic}/{public.target.euler_characteristic}")
    print(f"planted length/public bound: {len(reference.planted_moves)}/{public.bound}")
    print(f"planted move counts 2-3/3-2: {metrics.move_23}/{metrics.move_32}")
    print(f"branching initial/min/mean/max: {metrics.initial_branching}/{metrics.min_branching}/{metrics.mean_branching:.2f}/{metrics.max_branching}")
    print(f"mean unique branching: {metrics.mean_unique_branching:.2f}")
    print(f"neighbor collisions: {metrics.neighbor_collisions}")
    print(f"commuting move pairs: {metrics.commuting_pairs}/{metrics.commuting_pairs_tested}")
    print(f"planted witness valid: {verify_pachner_witness(public, reference.planted_moves)}")
    print(f"BFS found/distance: {bfs.found}/{bfs.distance}")
    print(f"BFS visited/expanded/max-frontier: {bfs.visited_states}/{bfs.expanded_states}/{bfs.max_frontier}")
    print(f"BFS elapsed seconds: {bfs_elapsed:.6f}")
    print(f"bidir found/distance: {bidir.found}/{bidir.distance}")
    print(f"bidir forward/reverse visited: {bidir.forward_visited}/{bidir.reverse_visited}")
    print(f"bidir expanded/max-frontiers: {bidir.expanded_states}/{bidir.max_forward_frontier}/{bidir.max_reverse_frontier}")
    print(f"bidir witness valid: {verify_pachner_witness(public, bidir.moves) if bidir.found else False}")
    print(f"bidir elapsed seconds: {bidir_elapsed:.6f}")
    return 0 if bidir.found and verify_pachner_witness(public, bidir.moves) else 1


if __name__ == "__main__":
    raise SystemExit(main())
