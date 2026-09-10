from __future__ import annotations

import argparse
import hashlib
from math import comb

from morph_kem.gluing import gluing_incidence
from morph_kem.gluing_overlap import (
    G9_PARAMETER_SETS,
    generate_overlap_gluing_instance,
    recover_overlap_gluing,
)


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


def derived_seed(name: str, index: int) -> bytes:
    return hashlib.sha256(
        b"MORPH-KEM G9 sweep v1\x00"
        + MASTER_SEED
        + name.encode("ascii")
        + index.to_bytes(4, "big")
    ).digest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 64:
        raise SystemExit("--seeds must be in 1..64")

    print(
        "set,seed,T,pieces,D2,D3,V,E,F,boundary,dual_edges,bridges,articulations,"
        "d2_candidates,d3_candidates,membership_hist,overlap_hist,candidate_incidence,"
        "cover_solutions,cover_nodes,cover_backtracks,dp_states,dp_transitions,dp_tilings,"
        "accepted,nonreference"
    )
    success = True
    for name in sorted(G9_PARAMETER_SETS):
        params = G9_PARAMETER_SETS[name]
        expected = params.tetrahedron_count * comb(params.piece_count, params.d2_count) // params.piece_count
        for seed_index in range(args.seeds):
            public, reference = generate_overlap_gluing_instance(
                params, derived_seed(name, seed_index)
            )
            incidence = gluing_incidence(public)
            recovery = recover_overlap_gluing(public, reference=reference)
            membership = "/".join(f"{degree}:{count}" for degree, count in recovery.membership_histogram)
            overlap = "/".join(f"{degree}:{count}" for degree, count in recovery.overlap_degree_histogram)
            print(
                f"{name},{seed_index},{params.tetrahedron_count},{params.piece_count},"
                f"{params.d2_count},{params.d3_count},{incidence.vertices},{incidence.edges},"
                f"{incidence.faces},{incidence.boundary_faces},{recovery.dual_edges},"
                f"{recovery.bridge_count},{len(recovery.articulation_points)},"
                f"{recovery.d2_candidates},{recovery.d3_candidates},{membership},{overlap},"
                f"{recovery.candidate_incidence_size},{recovery.exact_cover_solutions},"
                f"{recovery.exact_cover_nodes},{recovery.exact_cover_backtracks},"
                f"{recovery.cycle_dp_states},{recovery.cycle_dp_transition_checks},"
                f"{recovery.cycle_dp_tilings},{recovery.accepted_solutions},"
                f"{recovery.nonreference_accepted_solutions}"
            )
            success &= (
                recovery.bridge_count == 0
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
