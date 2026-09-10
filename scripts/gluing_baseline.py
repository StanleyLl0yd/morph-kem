#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.gluing import (
    G0_PARAMETER_SETS,
    generate_gluing_instance,
    gluing_incidence,
    recover_gluing_by_dual_bridges,
    reference_partition_matches,
    validate_gluing_witness,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run MORPH G0 HGES canonical-gluing negative control.")
    parser.add_argument("--params", choices=sorted(G0_PARAMETER_SETS), default="g0-8")
    parser.add_argument(
        "--master-seed",
        default="76120450aabbccddeeff001122334455",
        help="hex deterministic generation seed",
    )
    args = parser.parse_args()

    params = G0_PARAMETER_SETS[args.params]
    public, reference = generate_gluing_instance(params, bytes.fromhex(args.master_seed))
    incidence = gluing_incidence(public)
    recovery = recover_gluing_by_dual_bridges(public)
    reference_validation = validate_gluing_witness(public, reference.groups)
    matches = reference_partition_matches(reference, recovery.groups)

    print(f"parameters: {params.name}")
    print(f"pieces: {params.piece_count}")
    print(
        "public V/E/F/T: "
        f"{incidence.vertices}/{incidence.edges}/{incidence.faces}/{incidence.tetrahedra}"
    )
    print(f"Euler characteristic: {incidence.euler_characteristic}")
    print(f"boundary faces/max face incidence: {incidence.boundary_faces}/{incidence.max_face_incidence}")
    print(f"dual graph vertices/edges: {incidence.tetrahedra}/{recovery.dual_edges}")
    print(f"dual bridges: {len(recovery.bridges)}")
    print(f"bridge component sizes: {recovery.validation.component_sizes}")
    print(f"face occurrence checks: {recovery.face_occurrences}")
    print(f"DFS edge scans: {recovery.dfs_edge_scans}")
    print(f"reference witness accepted: {reference_validation.valid}")
    print(f"public bridge witness accepted: {recovery.validation.valid}")
    print(f"recovered partition equals planted up to group order: {matches}")

    return 0 if (
        reference_validation.valid
        and recovery.validation.valid
        and matches
        and len(recovery.bridges) == params.piece_count - 1
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
