from __future__ import annotations

import argparse
import hashlib

from morph_kem.nat_a5 import NAT3_PARAMETER_SETS, generate_nat3_instance, recover_nat3


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(NAT3_PARAMETER_SETS), default="nat3-F36")
    args = parser.parse_args()
    params = NAT3_PARAMETER_SETS[args.params]
    seed = hashlib.sha256(
        f"MORPH-KEM NAT3 fixed baseline {params.name} v1".encode("ascii")
    ).digest()

    print(f"parameters: {params.name}")
    for weight in params.noise_weights:
        public, reference = generate_nat3_instance(params, seed, weight)
        recovery = recover_nat3(public, reference=reference)
        print(
            f"noise={weight} V/E/F={recovery.vertices}/{recovery.edges}/{recovery.triangles} "
            f"curvature_defects={recovery.curvature_defect_faces} "
            f"curvature_classes={recovery.curvature_class_histogram} "
            f"support_space={recovery.total_support_combinations} "
            f"hitting_supports={recovery.curvature_hitting_supports} "
            f"propagated={recovery.propagated_supports} "
            f"consistent={recovery.connected_consistent_supports} "
            f"accepted_states={recovery.accepted_states} "
            f"first_accepted={recovery.first_state_accepted} "
            f"support_match={recovery.first_support_matches_planted_after_public_success} "
            f"state_match={recovery.first_state_matches_planted_after_public_success} "
            f"planted_hitting={recovery.planted_support_is_curvature_hitting} "
            f"rejected_flips={reference.rejected_flip_proposals}"
        )


if __name__ == "__main__":
    main()
