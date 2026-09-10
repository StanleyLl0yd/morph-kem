#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib

from morph_kem.gluing import gluing_incidence
from morph_kem.gluing_matching import (
    G3_PARAMETER_SETS,
    generate_matching_gluing_instance,
    recover_matching_gluing,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Sweep MORPH G3 equivalent-matching HGES control.")
    parser.add_argument(
        "--master-seed",
        default="76120450aabbccddeeff001122334455",
        help="hex deterministic master seed",
    )
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()

    if args.seeds <= 0 or args.seeds > 64:
        parser.error("--seeds must be in 1..64")

    master_seed = bytes.fromhex(args.master_seed)
    all_ok = True
    print(
        "set,seed,pieces,V,E,F,T,boundary,max_face_incidence,euler,dual_edges,"
        "bridges,articulations,allowed_edges,vertex_star_pairs,vertex_degree_hist,"
        "face_occurrences,matchings,matching_nodes,matching_backtracks,accepted,nonreference"
    )

    for name in sorted(G3_PARAMETER_SETS):
        params = G3_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            seed = hashlib.sha256(
                b"MORPH-KEM G3 sweep v1\x00"
                + master_seed
                + name.encode("ascii")
                + seed_index.to_bytes(4, "big")
            ).digest()
            public, reference = generate_matching_gluing_instance(params, seed)
            incidence = gluing_incidence(public)
            recovery = recover_matching_gluing(public, reference=reference)
            ok = (
                recovery.bridge_count == 0
                and not recovery.articulation_points
                and recovery.allowed_candidate_edges == 2 * params.piece_count
                and recovery.vertex_star_candidate_pairs == 2 * params.piece_count
                and recovery.matching_solutions == 2
                and recovery.accepted_solutions == 2
                and recovery.nonreference_accepted_solutions == 1
                and recovery.matching_backtracks == 0
            )
            all_ok = all_ok and ok
            vertex_hist = "/".join(
                f"{degree}:{count}"
                for degree, count in recovery.vertex_tetrahedron_degree_histogram
            )
            print(
                f"{name},{seed_index},{params.piece_count},{incidence.vertices},{incidence.edges},"
                f"{incidence.faces},{incidence.tetrahedra},{incidence.boundary_faces},"
                f"{incidence.max_face_incidence},{incidence.euler_characteristic},{recovery.dual_edges},"
                f"{recovery.bridge_count},{len(recovery.articulation_points)},"
                f"{recovery.allowed_candidate_edges},{recovery.vertex_star_candidate_pairs},"
                f"{vertex_hist},{recovery.face_occurrences},{recovery.matching_solutions},"
                f"{recovery.matching_nodes},{recovery.matching_backtracks},"
                f"{recovery.accepted_solutions},{recovery.nonreference_accepted_solutions}"
            )

    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
