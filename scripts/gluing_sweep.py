#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib

from morph_kem.gluing import (
    G0_PARAMETER_SETS,
    generate_gluing_instance,
    gluing_incidence,
    recover_gluing_by_dual_bridges,
    reference_partition_matches,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Sweep MORPH G0 HGES canonical-gluing negative control.")
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
        "set,seed,pieces,V,E,F,T,boundary,max_face_incidence,euler,dual_edges,"
        "bridges,component_sizes,face_occurrences,dfs_edge_scans,accepted,matches_reference"
    )

    for name in sorted(G0_PARAMETER_SETS):
        params = G0_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            seed = hashlib.sha256(
                b"MORPH-KEM G0 sweep v1\x00"
                + master_seed
                + name.encode("ascii")
                + seed_index.to_bytes(4, "big")
            ).digest()
            public, reference = generate_gluing_instance(params, seed)
            incidence = gluing_incidence(public)
            recovery = recover_gluing_by_dual_bridges(public)
            matches = reference_partition_matches(reference, recovery.groups)
            all_ok = all_ok and recovery.validation.valid and matches
            component_sizes = "/".join(str(size) for size in recovery.validation.component_sizes)
            print(
                f"{name},{seed_index},{params.piece_count},{incidence.vertices},{incidence.edges},"
                f"{incidence.faces},{incidence.tetrahedra},{incidence.boundary_faces},"
                f"{incidence.max_face_incidence},{incidence.euler_characteristic},{recovery.dual_edges},"
                f"{len(recovery.bridges)},{component_sizes},{recovery.face_occurrences},"
                f"{recovery.dfs_edge_scans},{int(recovery.validation.valid)},{int(matches)}"
            )

    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
