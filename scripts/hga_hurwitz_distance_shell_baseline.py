from __future__ import annotations

import argparse
import hashlib

from morph_kem.hga_hurwitz_distance_shell import (
    HGA4C_PARAMETER_SETS,
    generate_hga4c_instance,
    recover_hga4c,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(HGA4C_PARAMETER_SETS), default="hga4c-D8")
    args = parser.parse_args()
    params = HGA4C_PARAMETER_SETS[args.params]
    seed = hashlib.sha256(
        f"MORPH-KEM HGA4c fixed baseline {params.name} v1".encode("ascii")
    ).digest()
    public, reference = generate_hga4c_instance(params, seed)
    recovery = recover_hga4c(public, reference=reference)

    print(f"parameters: {params.name}")
    print(f"exact distance: {recovery.exact_distance}")
    print(f"generator ball / shell states: {recovery.generator_ball_states}/{recovery.generator_shell_states}")
    print(f"generator transitions: {recovery.generator_transitions}")
    print(f"selected target total reduced length: {recovery.selected_target_total_length}")
    print(f"shortest path multiplicity: {recovery.shortest_path_multiplicity}")
    print(f"attacker forward/backward states: {recovery.attacker_forward_states}/{recovery.attacker_backward_states}")
    print(f"attacker forward/backward transitions: {recovery.attacker_forward_transitions}/{recovery.attacker_backward_transitions}")
    print(f"meet states: {recovery.meet_states}")
    print(f"recovered connector length: {recovery.recovered_connector_length}")
    print(f"endpoint verified: {recovery.endpoint_verified}")
    print(f"matches generator certificate: {recovery.matches_generator_certificate_after_public_success}")
    print(f"attacker state fraction of generator ball: {recovery.attacker_state_fraction_of_generator_ball:.9f}")


if __name__ == "__main__":
    main()
