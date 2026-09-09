#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time

from morph_kem.maze import MAZE_PARAMETER_SETS, generate_maze, recover_three_regular_core


DEFAULT_SETS = ("maze-4", "maze-6", "maze-8", "maze-10", "maze-12")


def main() -> int:
    parser = argparse.ArgumentParser(description="Sweep the M2 structural core-recovery attack.")
    parser.add_argument("--max-nodes", type=int, default=2_000_000)
    parser.add_argument(
        "--master-seed",
        default="31415926535897932384626433832795",
        help="hex-encoded deterministic instance-generation seed",
    )
    args = parser.parse_args()

    master_seed = bytes.fromhex(args.master_seed)
    for name in DEFAULT_SETS:
        public, _ = generate_maze(MAZE_PARAMETER_SETS[name], master_seed)
        started = time.perf_counter()
        result = recover_three_regular_core(public, max_nodes=args.max_nodes)
        elapsed = time.perf_counter() - started
        print(
            f"{name}: found={result.found} nodes={result.nodes} "
            f"candidates={result.degree_candidates} forced={result.forced_edges} "
            f"optional={result.optional_edges} exhausted={result.exhausted} "
            f"elapsed={elapsed:.6f}s"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
