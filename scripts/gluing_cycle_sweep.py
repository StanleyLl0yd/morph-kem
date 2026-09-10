#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib

from morph_kem.gluing import gluing_incidence, recover_gluing_by_dual_bridges
from morph_kem.gluing_cycle import (
    G1_PARAMETER_SETS,
    cycle_reference_partition_matches,
    generate_cycle_gluing_instance,
    recover_cycle_gluing_by_k4_exact_cover,
    validate_cycle_gluing_witness,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sweep MORPH G1 bridge-free HGES clique-decomposition negative control."
    )
    parser.add_argument(
        "--master-seed",
        default="76120450aabbccddeeff001122334455",
        help="hex deterministic generation seed",
    )
    parser.add_argument("--seeds", type=int, default=8)
    parser.add_argument("--solution-cap", type=int, default=64)
    args = parser.parse_args()

    if args.seeds <= 0 or args.seeds > 64:
        parser.error("--seeds must be in 1..64")

    master_seed = bytes.fromhex(args.master_seed)
    all_ok = True
    print(
        "set,seed,pieces,V,E,F,T,boundary,max_face_incidence,euler,dual_edges,"
        "bridges,articulations,two_vertex_separators,face_occurrences,four_subsets,"
        "dual_k4,allowed_pieces,exact_cover_solutions,cover_nodes,cover_backtracks,"
        "accepted,matches_reference"
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
            incidence = gluing_incidence(public)
            bridge_recovery = recover_gluing_by_dual_bridges(public)
            bridge_cycle_validation = validate_cycle_gluing_witness(public, bridge_recovery.groups)
            recovery = recover_cycle_gluing_by_k4_exact_cover(
                public,
                solution_cap=args.solution_cap,
            )
            matches = cycle_reference_partition_matches(reference, recovery.groups)

            ok = (
                len(bridge_recovery.bridges) == 0
                and not bridge_cycle_validation.valid
                and recovery.bridge_count == 0
                and not recovery.articulation_points
                and recovery.validation.valid
                and matches
                and recovery.exact_cover_solutions >= 1
            )
            all_ok = all_ok and ok

            print(
                f"{name},{seed_index},{params.piece_count},{incidence.vertices},{incidence.edges},"
                f"{incidence.faces},{incidence.tetrahedra},{incidence.boundary_faces},"
                f"{incidence.max_face_incidence},{incidence.euler_characteristic},{recovery.dual_edges},"
                f"{len(bridge_recovery.bridges)},{len(recovery.articulation_points)},"
                f"{recovery.two_vertex_separator_pairs},{recovery.face_occurrences},"
                f"{recovery.four_subsets_tested},{recovery.dual_k4_candidates},"
                f"{recovery.allowed_piece_candidates},{recovery.exact_cover_solutions},"
                f"{recovery.exact_cover_nodes},{recovery.exact_cover_backtracks},"
                f"{int(recovery.validation.valid)},{int(matches)}"
            )

    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
