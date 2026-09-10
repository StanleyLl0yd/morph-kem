#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.gluing import gluing_incidence
from morph_kem.gluing_matching import (
    G3_PARAMETER_SETS,
    generate_matching_gluing_instance,
    recover_matching_gluing,
    validate_matching_gluing_witness,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run MORPH G3 equivalent-matching HGES control.")
    parser.add_argument("--params", choices=sorted(G3_PARAMETER_SETS), default="g3-8")
    parser.add_argument(
        "--master-seed",
        default="76120450aabbccddeeff001122334455",
        help="hex deterministic public-relabel seed",
    )
    args = parser.parse_args()

    params = G3_PARAMETER_SETS[args.params]
    public, reference = generate_matching_gluing_instance(params, bytes.fromhex(args.master_seed))
    incidence = gluing_incidence(public)
    recovery = recover_matching_gluing(public, reference=reference)
    reference_validation = validate_matching_gluing_witness(public, reference.groups)

    print(f"parameters: {params.name}")
    print(f"pieces: {params.piece_count}")
    print(
        "public V/E/F/T: "
        f"{incidence.vertices}/{incidence.edges}/{incidence.faces}/{incidence.tetrahedra}"
    )
    print(f"Euler characteristic: {incidence.euler_characteristic}")
    print(f"boundary faces/max face incidence: {incidence.boundary_faces}/{incidence.max_face_incidence}")
    print(f"dual graph vertices/edges: {incidence.tetrahedra}/{recovery.dual_edges}")
    print(f"dual degree histogram: {recovery.dual_degree_histogram}")
    print(f"bridges/articulation points: {recovery.bridge_count}/{len(recovery.articulation_points)}")
    print(f"allowed candidate dual edges: {recovery.allowed_candidate_edges}")
    print(f"vertex-star candidate pairs: {recovery.vertex_star_candidate_pairs}")
    print(f"vertex tetrahedron-degree histogram: {recovery.vertex_tetrahedron_degree_histogram}")
    print(f"face occurrence checks: {recovery.face_occurrences}")
    print(f"perfect matchings/cap: {recovery.matching_solutions}/{recovery.matching_solution_cap}")
    print(f"matching cap hit: {recovery.matching_cap_hit}")
    print(f"matching nodes/backtracks: {recovery.matching_nodes}/{recovery.matching_backtracks}")
    print(f"accepted decompositions: {recovery.accepted_solutions}")
    print(f"accepted non-planted decompositions: {recovery.nonreference_accepted_solutions}")
    print(f"reference witness accepted: {reference_validation.valid}")

    return 0 if (
        reference_validation.valid
        and recovery.bridge_count == 0
        and not recovery.articulation_points
        and recovery.allowed_candidate_edges == 2 * params.piece_count
        and recovery.matching_solutions == 2
        and recovery.accepted_solutions == 2
        and recovery.nonreference_accepted_solutions == 1
        and recovery.matching_backtracks == 0
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
