#!/usr/bin/env python3
from __future__ import annotations

import argparse

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
        description="Run MORPH G1 bridge-free HGES clique-decomposition negative control."
    )
    parser.add_argument("--params", choices=sorted(G1_PARAMETER_SETS), default="g1-12")
    parser.add_argument(
        "--master-seed",
        default="76120450aabbccddeeff001122334455",
        help="hex deterministic generation seed",
    )
    parser.add_argument("--solution-cap", type=int, default=64)
    args = parser.parse_args()

    params = G1_PARAMETER_SETS[args.params]
    public, reference = generate_cycle_gluing_instance(params, bytes.fromhex(args.master_seed))
    incidence = gluing_incidence(public)
    bridge_recovery = recover_gluing_by_dual_bridges(public)
    bridge_cycle_validation = validate_cycle_gluing_witness(public, bridge_recovery.groups)
    recovery = recover_cycle_gluing_by_k4_exact_cover(
        public,
        solution_cap=args.solution_cap,
    )
    reference_validation = validate_cycle_gluing_witness(public, reference.groups)
    matches = cycle_reference_partition_matches(reference, recovery.groups)

    print(f"parameters: {params.name}")
    print(f"pieces: {params.piece_count}")
    print(
        "public V/E/F/T: "
        f"{incidence.vertices}/{incidence.edges}/{incidence.faces}/{incidence.tetrahedra}"
    )
    print(f"Euler characteristic: {incidence.euler_characteristic}")
    print(
        "boundary faces/max face incidence: "
        f"{incidence.boundary_faces}/{incidence.max_face_incidence}"
    )
    print(f"dual graph vertices/edges: {incidence.tetrahedra}/{recovery.dual_edges}")
    print(f"A-024 dual bridges: {len(bridge_recovery.bridges)}")
    print(f"A-024 bridge-block witness accepted by G1: {bridge_cycle_validation.valid}")
    print(f"articulation points: {len(recovery.articulation_points)}")
    print(f"two-vertex separator pairs: {recovery.two_vertex_separator_pairs}")
    print(f"face occurrence checks: {recovery.face_occurrences}")
    print(f"4-subsets tested: {recovery.four_subsets_tested}")
    print(f"dual K4 candidates: {recovery.dual_k4_candidates}")
    print(f"allowed-piece candidates: {recovery.allowed_piece_candidates}")
    print(
        "exact-cover solutions/cap: "
        f"{recovery.exact_cover_solutions}/{recovery.exact_cover_solution_cap}"
    )
    print(f"exact-cover cap hit: {recovery.exact_cover_cap_hit}")
    print(f"exact-cover nodes/backtracks: {recovery.exact_cover_nodes}/{recovery.exact_cover_backtracks}")
    print(f"reference witness accepted: {reference_validation.valid}")
    print(f"A-028 public witness accepted: {recovery.validation.valid}")
    print(f"recovered partition equals planted up to group order: {matches}")

    return 0 if (
        reference_validation.valid
        and len(bridge_recovery.bridges) == 0
        and not bridge_cycle_validation.valid
        and recovery.bridge_count == 0
        and not recovery.articulation_points
        and recovery.validation.valid
        and matches
        and recovery.exact_cover_solutions >= 1
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
