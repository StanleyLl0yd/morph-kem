from __future__ import annotations

import argparse
import hashlib

from morph_kem.nat_a5_flat import NAT4_PARAMETER_SETS, generate_nat4_instance, recover_nat4


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(NAT4_PARAMETER_SETS), default="nat4-F36")
    args = parser.parse_args()
    params = NAT4_PARAMETER_SETS[args.params]
    seed = hashlib.sha256(
        f"MORPH-KEM NAT4 fixed baseline {params.name} v1".encode("ascii")
    ).digest()

    print(f"parameters: {params.name}")
    for weight in params.deformation_weights:
        public, reference = generate_nat4_instance(params, seed, weight)
        recovery = recover_nat4(public, reference=reference)
        print(
            f"weight={weight} V/E/F={recovery.vertices}/{recovery.edges}/{recovery.triangles} "
            f"nonidentity_face_holonomies={recovery.nonidentity_face_holonomies} "
            f"integration_checks={recovery.integration_edge_checks} "
            f"integration_consistent={recovery.integration_consistent} "
            f"equivalent_witness_lower_bound={recovery.equivalent_witness_lower_bound} "
            f"canonical_support={recovery.canonical_support} "
            f"accepted={recovery.canonical_witness_accepted} "
            f"support_match={recovery.canonical_support_matches_planted_after_public_success} "
            f"clean_state_match={recovery.canonical_clean_state_matches_planted_after_public_success} "
            f"effective_state_match={recovery.effective_state_matches_reference_after_public_success} "
            f"rejected_flips={reference.rejected_flip_proposals}"
        )


if __name__ == "__main__":
    main()
