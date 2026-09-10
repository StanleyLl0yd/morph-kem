#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.pachner import bidirectional_pachner_recover
from morph_kem.pachner_distance import T1_PARAMETER_SETS, astar_tetrahedron_recover, generate_distance_instance


def main() -> int:
    parser = argparse.ArgumentParser(description="Sweep MORPH T1 exact-distance Pachner toy sets.")
    parser.add_argument(
        "--master-seed",
        default="76120450aabbccddeeff001122334455",
        help="hex deterministic generation seed",
    )
    parser.add_argument("--attack-states", type=int, default=100000)
    args = parser.parse_args()
    seed = bytes.fromhex(args.master_seed)

    print("set,D,shell_sizes,ball,target_delta,target_slack,shortest_paths,predecessors,bidir_forward,bidir_reverse,bidir_expanded,astar_visited,astar_expanded")
    ok = True
    for name in sorted(T1_PARAMETER_SETS):
        public, reference = generate_distance_instance(T1_PARAMETER_SETS[name], seed)
        bidir = bidirectional_pachner_recover(public, max_states=args.attack_states)
        astar = astar_tetrahedron_recover(public, max_states=args.attack_states)
        ok &= bool(
            bidir.found
            and astar.found
            and bidir.distance == reference.exact_distance
            and astar.distance == reference.exact_distance
        )
        print(
            f"{name},{reference.exact_distance},{'/'.join(map(str, reference.profile.shell_sizes))},"
            f"{reference.profile.ball_size},{reference.target_tetrahedron_delta},{reference.target_tetrahedron_slack},"
            f"{reference.shortest_paths_capped},{reference.shortest_predecessors},"
            f"{bidir.forward_visited},{bidir.reverse_visited},{bidir.expanded_states},"
            f"{astar.visited_states},{astar.expanded_states}"
        )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
