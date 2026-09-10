#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
from collections import Counter

from morph_kem.gluing import GluingPublicInstance, gluing_incidence
from morph_kem.gluing_stellar import (
    G2_PARAMETER_SETS,
    generate_stellar_gluing_instance,
    recover_stellar_gluing_by_center_contraction,
    stellar_reference_partition_matches,
)


def _vertex_star_histogram(public: GluingPublicInstance) -> str:
    stars: Counter[int] = Counter()
    for tetrahedron in public.tetrahedra:
        for vertex in tetrahedron:
            stars[vertex] += 1
    histogram = Counter(stars.values())
    return "/".join(f"{degree}:{histogram[degree]}" for degree in sorted(histogram))


def main() -> int:
    parser = argparse.ArgumentParser(description="Sweep MORPH G2 stellar-contraction negative control.")
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
        "set,seed,pieces,V,E,F,T,boundary,max_face_incidence,euler,micro_dual_edges,"
        "bridges,articulations,two_vertex_separators,face_occurrences,star_histogram,"
        "center_candidates,false_centers,missed_centers,center_cover_solutions,"
        "center_cover_nodes,center_cover_backtracks,macro_tetrahedra,macro_dual_edges,"
        "macro_k4,macro_allowed,macro_cover_solutions,macro_cover_nodes,"
        "macro_cover_backtracks,accepted,matches_reference"
    )

    for name in sorted(G2_PARAMETER_SETS):
        params = G2_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            seed = hashlib.sha256(
                b"MORPH-KEM G2 sweep v1\x00"
                + master_seed
                + name.encode("ascii")
                + seed_index.to_bytes(4, "big")
            ).digest()
            public, reference = generate_stellar_gluing_instance(params, seed)
            incidence = gluing_incidence(public)
            recovery = recover_stellar_gluing_by_center_contraction(public)
            matches = stellar_reference_partition_matches(reference, recovery.groups)
            candidates = set(recovery.candidate_centers)
            reference_centers = set(reference.center_vertices)
            false_centers = len(candidates - reference_centers)
            missed_centers = len(reference_centers - candidates)
            ok = (
                recovery.validation.valid
                and matches
                and recovery.micro_bridge_count == 0
                and not recovery.micro_articulation_points
                and false_centers == 0
                and missed_centers == 0
            )
            all_ok = all_ok and ok
            print(
                f"{name},{seed_index},{params.piece_count},{incidence.vertices},{incidence.edges},"
                f"{incidence.faces},{incidence.tetrahedra},{incidence.boundary_faces},"
                f"{incidence.max_face_incidence},{incidence.euler_characteristic},"
                f"{recovery.micro_dual_edges},{recovery.micro_bridge_count},"
                f"{len(recovery.micro_articulation_points)},{recovery.micro_two_vertex_separator_pairs},"
                f"{recovery.micro_face_occurrences},{_vertex_star_histogram(public)},"
                f"{recovery.center_star_candidates},{false_centers},{missed_centers},"
                f"{recovery.center_cover_solutions},{recovery.center_cover_nodes},"
                f"{recovery.center_cover_backtracks},{recovery.reconstructed_macro_tetrahedra},"
                f"{recovery.macro_dual_edges},{recovery.macro_k4_candidates},"
                f"{recovery.macro_allowed_piece_candidates},{recovery.macro_cover_solutions},"
                f"{recovery.macro_cover_nodes},{recovery.macro_cover_backtracks},"
                f"{int(recovery.validation.valid)},{int(matches)}"
            )

    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
