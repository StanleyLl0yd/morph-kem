from __future__ import annotations

import argparse
import hashlib

from morph_kem.hga_hurwitz_distance_shell import (
    HGA4C_PARAMETER_SETS,
    generate_hga4c_instance,
    recover_hga4c,
)


def seed_for(name: str, index: int) -> bytes:
    return hashlib.sha256(
        f"MORPH-KEM HGA4c sweep {name} seed {index} v1".encode("ascii")
    ).digest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 16:
        raise SystemExit("--seeds must be between 1 and 16")

    print(
        "set,seed,D,ball,shell,generator_transitions,target_total_len,shortest_paths,"
        "forward,backward,forward_transitions,backward_transitions,meets,recovered,accepted,"
        "certificate_match,attacker_ball_fraction"
    )
    for params in HGA4C_PARAMETER_SETS.values():
        for index in range(args.seeds):
            public, reference = generate_hga4c_instance(
                params, seed_for(params.name, index)
            )
            recovery = recover_hga4c(public, reference=reference)
            print(
                f"{params.name},{index},{params.exact_distance},"
                f"{recovery.generator_ball_states},{recovery.generator_shell_states},"
                f"{recovery.generator_transitions},{recovery.selected_target_total_length},"
                f"{recovery.shortest_path_multiplicity},"
                f"{recovery.attacker_forward_states},{recovery.attacker_backward_states},"
                f"{recovery.attacker_forward_transitions},{recovery.attacker_backward_transitions},"
                f"{recovery.meet_states},{recovery.recovered_connector_length},"
                f"{int(recovery.endpoint_verified)},"
                f"{int(bool(recovery.matches_generator_certificate_after_public_success))},"
                f"{recovery.attacker_state_fraction_of_generator_ball:.9f}"
            )


if __name__ == "__main__":
    main()
