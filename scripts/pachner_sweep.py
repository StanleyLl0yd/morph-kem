#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.pachner import (
    PACHNER_PARAMETER_SETS,
    bfs_pachner_recover,
    bidirectional_pachner_recover,
    generate_pachner_instance,
    pachner_path_metrics,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Sweep MORPH T0 bounded Pachner toy sets.")
    parser.add_argument("--max-states", type=int, default=20_000)
    parser.add_argument("--master-seed", default="48026490aabbccddeeff1029384756aa")
    args = parser.parse_args(); seed = bytes.fromhex(args.master_seed)

    print("set,planted,bfs_distance,bfs_visited,bfs_expanded,bidir_distance,bidir_forward,bidir_reverse,bidir_expanded,branch_mean,commuting_fraction")
    ok = True
    for name, params in PACHNER_PARAMETER_SETS.items():
        public, reference = generate_pachner_instance(params, seed)
        metrics = pachner_path_metrics(public, reference)
        bfs = bfs_pachner_recover(public, args.max_states)
        bidir = bidirectional_pachner_recover(public, args.max_states)
        fraction = metrics.commuting_pairs / metrics.commuting_pairs_tested if metrics.commuting_pairs_tested else 0.0
        print(f"{name},{len(reference.planted_moves)},{bfs.distance},{bfs.visited_states},{bfs.expanded_states},{bidir.distance},{bidir.forward_visited},{bidir.reverse_visited},{bidir.expanded_states},{metrics.mean_unique_branching:.3f},{fraction:.6f}")
        ok = ok and bfs.found and bidir.found
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
