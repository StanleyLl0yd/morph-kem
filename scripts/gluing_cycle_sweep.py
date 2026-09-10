#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib

from morph_kem.gluing_cycle import (
    G1_PARAMETER_SETS,
    cycle_structure,
    generate_cycle_gluing_instance,
    recover_cycle_by_dual_k4,
    recover_cycle_by_vertex_stars,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Sweep MORPH G1 HGES cycle attacks.")
    parser.add_argument(
        "--master-seed",
        default="76120450aabbccddeeff001122334455",
        help="hex deterministic generation seed",
    )
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()

    if args.seeds <= 0 or args.seeds > 64:
        parser.error("--seeds must be in 1..64")

    master_seed = bytes.fromhex(args.master_seed)
    all_ok = True
    print(
        "set,seed,pieces,V,E,F,T,boundary,dual_edges,bridges,articulations,"
        "star_candidates,star_nodes,star_backtracks,star_accepted,star_match,"
        "k4_subset_checks,k4_candidates,k4_nodes,k4_backtracks,k4_accepted,k4_match"
    )

    for name in sorted(G1_PARAMETER_SETS):
        params = G1_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            seed = hashlib.sha256(
                b"MORPH-KEM G1 sweep v1\x00"
                + master_seed
                + name.encode("ascii")
                + seed_index.to_bytes(4, "big")
            ).digest()
            public, reference = generate_cycle_gluing_instance(params, seed)
            structure = cycle_structure(public)
            star = recover_cycle_by_vertex_stars(public, reference)
            k4 = recover_cycle_by_dual_k4(public, reference)

            row_ok = (
                not structure.bridges
                and not structure.articulation_vertices
                and star.exact_cover.validation.valid
                and star.matches_reference
                and k4.exact_cover.validation.valid
                and k4.matches_reference
            )
            all_ok = all_ok and row_ok
            print(
                f"{name},{seed_index},{params.piece_count},{structure.vertices},{structure.edges},"
                f"{structure.faces},{structure.tetrahedra},{structure.boundary_faces},"
                f"{structure.dual_edges},{len(structure.bridges)},{len(structure.articulation_vertices)},"
                f"{len(star.valid_candidates)},{star.exact_cover.nodes},{star.exact_cover.backtracks},"
                f"{int(star.exact_cover.validation.valid)},{int(star.matches_reference)},"
                f"{k4.subset_checks},{len(k4.valid_candidates)},{k4.exact_cover.nodes},"
                f"{k4.exact_cover.backtracks},{int(k4.exact_cover.validation.valid)},{int(k4.matches_reference)}"
            )

    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
