#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.gluing_cycle import (
    G1_PARAMETER_SETS,
    cycle_structure,
    generate_cycle_gluing_instance,
    recover_cycle_by_dual_k4,
    recover_cycle_by_vertex_stars,
    validate_cycle_gluing_witness,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run MORPH G1 bridge-free HGES cycle calibration.")
    parser.add_argument("--params", choices=sorted(G1_PARAMETER_SETS), default="g1-8")
    parser.add_argument(
        "--master-seed",
        default="76120450aabbccddeeff001122334455",
        help="hex deterministic generation seed",
    )
    args = parser.parse_args()

    params = G1_PARAMETER_SETS[args.params]
    public, reference = generate_cycle_gluing_instance(params, bytes.fromhex(args.master_seed))
    structure = cycle_structure(public)
    reference_validation = validate_cycle_gluing_witness(public, reference.groups)
    star = recover_cycle_by_vertex_stars(public, reference)
    k4 = recover_cycle_by_dual_k4(public, reference)

    print(f"parameters: {params.name}")
    print(f"pieces: {params.piece_count}")
    print(
        "public V/E/F/T: "
        f"{structure.vertices}/{structure.edges}/{structure.faces}/{structure.tetrahedra}"
    )
    print(f"Euler characteristic: {structure.euler_characteristic}")
    print(f"boundary faces/max face incidence: {structure.boundary_faces}/{structure.max_face_incidence}")
    print(f"dual graph vertices/edges: {structure.tetrahedra}/{structure.dual_edges}")
    print(f"dual bridges/articulation vertices: {len(structure.bridges)}/{len(structure.articulation_vertices)}")
    print(f"dual degree histogram: {structure.dual_degree_histogram}")
    print(f"vertex tetrahedron-degree histogram: {structure.vertex_tetrahedron_degree_histogram}")
    print(f"face occurrences/DFS edge scans: {structure.face_occurrences}/{structure.dfs_edge_scans}")
    print(f"cycle swap bits: {reference.swap_bits}")
    print(f"reference witness accepted: {reference_validation.valid}")
    print()
    print("A-028 vertex-star recovery")
    print(f"candidate vertices/valid piece candidates: {star.candidate_vertices}/{len(star.valid_candidates)}")
    print(
        "exact-cover nodes/backtracks/solutions: "
        f"{star.exact_cover.nodes}/{star.exact_cover.backtracks}/{star.exact_cover.solutions}"
    )
    print(f"accepted/matches reference: {star.exact_cover.validation.valid}/{star.matches_reference}")
    print()
    print("A-029 dual-K4 recovery")
    print(f"4-subset checks/K4 candidates/valid pieces: {k4.subset_checks}/{k4.clique_candidates}/{len(k4.valid_candidates)}")
    print(
        "exact-cover nodes/backtracks/solutions: "
        f"{k4.exact_cover.nodes}/{k4.exact_cover.backtracks}/{k4.exact_cover.solutions}"
    )
    print(f"accepted/matches reference: {k4.exact_cover.validation.valid}/{k4.matches_reference}")

    ok = (
        reference_validation.valid
        and not structure.bridges
        and not structure.articulation_vertices
        and star.exact_cover.validation.valid
        and star.matches_reference
        and k4.exact_cover.validation.valid
        and k4.matches_reference
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
