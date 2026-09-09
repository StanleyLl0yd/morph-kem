#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.higher_atlas import higher_atlas_scaling_sweep


def main() -> int:
    parser = argparse.ArgumentParser(description="Sweep MORPH H2-E2 higher-order atlas parameters.")
    parser.add_argument("--max-nodes", type=int, default=2_000_000)
    parser.add_argument(
        "--master-seed",
        default="17320508075688772935274463415059",
        help="hex-encoded deterministic H2-E2 generation seed",
    )
    args = parser.parse_args()

    rows = higher_atlas_scaling_sweep(
        bytes.fromhex(args.master_seed),
        max_nodes=args.max_nodes,
    )

    print("name,variables,charts,budget,pairwise,found,min_seams,nodes,backtracks,seam_signatures_seen")
    for row in rows:
        print(
            f"{row.name},{row.variables},{row.charts},{row.budget},"
            f"{row.pairwise_compatible},{row.found},{row.minimum_seams},"
            f"{row.nodes},{row.backtracks},{row.seam_signatures_seen_in_normal}"
        )
    return 0 if all(row.found and row.pairwise_compatible for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
