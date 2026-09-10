from __future__ import annotations

import argparse
from math import comb

from morph_kem.gluing import gluing_incidence
from morph_kem.gluing_overlap import (
    G9_PARAMETER_SETS,
    generate_overlap_gluing_instance,
    recover_overlap_gluing,
    validate_overlap_gluing_witness,
)


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(G9_PARAMETER_SETS), default="g9-30")
    args = parser.parse_args()

    params = G9_PARAMETER_SETS[args.params]
    public, reference = generate_overlap_gluing_instance(params, MASTER_SEED)
    incidence = gluing_incidence(public)
    recovery = recover_overlap_gluing(public, reference=reference)
    reference_validation = validate_overlap_gluing_witness(public, reference.groups)
    expected = params.tetrahedron_count * comb(params.piece_count, params.d2_count) // params.piece_count

    print(f"parameters: {params.name}")
    print(f"public tetrahedra / witness pieces: {params.tetrahedron_count}/{params.piece_count}")
    print(f"required D2/D3 pieces: {params.d2_count}/{params.d3_count}")
    print(
        "public V/E/F/T: "
        f"{incidence.vertices}/{incidence.edges}/{incidence.faces}/{incidence.tetrahedra}"
    )
    print(f"Euler characteristic: {incidence.euler_characteristic}")
    print(
        "boundary faces/max face incidence: "
        f"{incidence.boundary_faces}/{incidence.max_face_incidence}"
    )
    print(f"dual graph vertices/edges: {len(public.tetrahedra)}/{recovery.dual_edges}")
    print(f"dual degree histogram: {recovery.dual_degree_histogram}")
    print(f"bridges/articulation points: {recovery.bridge_count}/{len(recovery.articulation_points)}")
    print(f"D2/D3 public candidates: {recovery.d2_candidates}/{recovery.d3_candidates}")
    print(f"candidate memberships per tetrahedron: {recovery.membership_histogram}")
    print(f"candidate overlap-degree histogram: {recovery.overlap_degree_histogram}")
    print(f"candidate/tetrahedron incidence size: {recovery.candidate_incidence_size}")
    print(f"face occurrence checks: {recovery.face_occurrences}")
    print(
        "exact-cover solutions/cap: "
        f"{recovery.exact_cover_solutions}/{recovery.exact_cover_solution_cap}"
    )
    print(f"exact-cover cap hit: {recovery.exact_cover_cap_hit}")
    print(
        "exact-cover nodes/backtracks: "
        f"{recovery.exact_cover_nodes}/{recovery.exact_cover_backtracks}"
    )
    print(
        "cycle-DP states/transition checks/tilings: "
        f"{recovery.cycle_dp_states}/{recovery.cycle_dp_transition_checks}/{recovery.cycle_dp_tilings}"
    )
    print(f"analytic cyclic tilings: {expected}")
    print(f"accepted public solutions: {recovery.accepted_solutions}")
    print(f"accepted non-reference solutions: {recovery.nonreference_accepted_solutions}")
    print(f"reference witness accepted: {reference_validation.valid}")

    success = (
        reference_validation.valid
        and recovery.bridge_count == 0
        and not recovery.articulation_points
        and recovery.d2_candidates == params.tetrahedron_count
        and recovery.d3_candidates == params.tetrahedron_count
        and recovery.membership_histogram == ((5, params.tetrahedron_count),)
        and recovery.exact_cover_solutions == expected
        and recovery.cycle_dp_tilings == expected
        and recovery.accepted_solutions == expected
        and recovery.nonreference_accepted_solutions == expected - 1
        and not recovery.exact_cover_cap_hit
    )
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
