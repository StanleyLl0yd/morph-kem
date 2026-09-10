#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time

from morph_kem.pachner import bfs_pachner_recover, bidirectional_pachner_recover, verify_pachner_witness
from morph_kem.pachner_distance import T1_PARAMETER_SETS, astar_tetrahedron_recover, generate_distance_instance


def main() -> int:
    parser = argparse.ArgumentParser(description="Run MORPH T1 exact-distance Pachner calibration.")
    parser.add_argument("--params", choices=sorted(T1_PARAMETER_SETS), default="t1-3")
    parser.add_argument(
        "--master-seed",
        default="76120450aabbccddeeff001122334455",
        help="hex deterministic generation seed",
    )
    parser.add_argument("--attack-states", type=int, default=100000)
    args = parser.parse_args()

    params = T1_PARAMETER_SETS[args.params]
    started = time.perf_counter()
    public, reference = generate_distance_instance(params, bytes.fromhex(args.master_seed))
    generation_elapsed = time.perf_counter() - started

    bfs_started = time.perf_counter()
    bfs = bfs_pachner_recover(public, max_states=args.attack_states)
    bfs_elapsed = time.perf_counter() - bfs_started

    bidir_started = time.perf_counter()
    bidir = bidirectional_pachner_recover(public, max_states=args.attack_states)
    bidir_elapsed = time.perf_counter() - bidir_started

    astar_started = time.perf_counter()
    astar = astar_tetrahedron_recover(public, max_states=args.attack_states)
    astar_elapsed = time.perf_counter() - astar_started

    p = reference.profile
    print(f"parameters: {params.name}")
    print(f"exact distance/public bound: {reference.exact_distance}/{public.bound}")
    print(f"shell sizes: {p.shell_sizes}")
    print(f"ball size/expanded: {p.ball_size}/{p.expanded_states}")
    print(f"raw moves/unique neighbors: {p.raw_moves}/{p.unique_neighbors}")
    print(f"local neighbor collisions/revisit hits: {p.local_neighbor_collisions}/{p.revisit_hits}")
    print(f"max shell frontier: {p.max_frontier}")
    print(f"tetrahedron histograms: {p.tetrahedron_histograms}")
    print(f"mean tetrahedron slack by shell: {tuple(round(x, 4) for x in p.mean_tetrahedron_slack)}")
    print(f"target tetrahedron delta/slack: {reference.target_tetrahedron_delta}/{reference.target_tetrahedron_slack}")
    print(f"max-slack/min-path candidate counts: {reference.max_slack_candidates}/{reference.min_path_candidates}")
    print(f"target shortest paths capped/count-cap-hit: {reference.shortest_paths_capped}/{reference.shortest_path_count_capped}")
    print(f"target shortest predecessors: {reference.shortest_predecessors}")
    print(f"reference witness valid: {verify_pachner_witness(public, reference.shortest_path)}")
    print(f"generation shell elapsed seconds: {generation_elapsed:.6f}")
    print(f"BFS found/distance: {bfs.found}/{bfs.distance}")
    print(f"BFS visited/expanded/frontier: {bfs.visited_states}/{bfs.expanded_states}/{bfs.max_frontier}")
    print(f"BFS elapsed seconds: {bfs_elapsed:.6f}")
    print(f"bidir found/distance: {bidir.found}/{bidir.distance}")
    print(f"bidir forward/reverse/expanded: {bidir.forward_visited}/{bidir.reverse_visited}/{bidir.expanded_states}")
    print(f"bidir elapsed seconds: {bidir_elapsed:.6f}")
    print(f"A* found/distance: {astar.found}/{astar.distance}")
    print(f"A* visited/expanded/frontier: {astar.visited_states}/{astar.expanded_states}/{astar.max_frontier}")
    print(f"A* elapsed seconds: {astar_elapsed:.6f}")

    return 0 if (
        bfs.found
        and bidir.found
        and astar.found
        and bfs.distance == reference.exact_distance
        and bidir.distance == reference.exact_distance
        and astar.distance == reference.exact_distance
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
