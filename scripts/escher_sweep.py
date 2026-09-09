#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.escher import escher_scaling_sweep


def main() -> int:
    parser = argparse.ArgumentParser(description="Sweep MORPH H2-E Escher toy parameters.")
    parser.add_argument("--max-nodes", type=int, default=1_000_000)
    parser.add_argument(
        "--master-seed",
        default="14142135623730950488016887242097",
        help="hex-encoded deterministic H2-E generation seed",
    )
    args = parser.parse_args()

    rows = escher_scaling_sweep(
        bytes.fromhex(args.master_seed),
        max_nodes=args.max_nodes,
    )

    print("name,V,E,cycle_rank,budget,nonzero_syndromes,found,min_seams,nodes,backtracks")
    for row in rows:
        print(
            f"{row.name},{row.vertices},{row.edges},{row.cycle_rank},"
            f"{row.seam_budget},{row.nonzero_syndromes},{row.found},"
            f"{row.minimum_seams},{row.nodes},{row.backtracks}"
        )

    return 0 if all(row.found for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
