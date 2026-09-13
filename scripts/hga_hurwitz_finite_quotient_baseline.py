from __future__ import annotations

import argparse
import hashlib

from morph_kem.hga_hurwitz_finite_quotient import (
    HGA4D_PARAMETER_SETS,
    generate_hga4d_instance,
    recover_hga4d,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--params", choices=sorted(HGA4D_PARAMETER_SETS), default="hga4d-D8"
    )
    args = parser.parse_args()
    params = HGA4D_PARAMETER_SETS[args.params]
    seed = hashlib.sha256(
        f"MORPH-KEM HGA4d fixed baseline {params.name} v1".encode("ascii")
    ).digest()
    public, reference = generate_hga4d_instance(params, seed)
    recovery = recover_hga4d(public, reference=reference)

    print(f"parameters: {params.name}")
    print(f"exact distance: {recovery.exact_distance}")
    print(
        f"generator ball / shell states: "
        f"{recovery.generator_ball_states}/{recovery.generator_shell_states}"
    )
    print(f"ordinary MITM states: {recovery.ordinary_mitm_states}")
    print(f"ordinary MITM transitions: {recovery.ordinary_mitm_transitions}")
    print(f"ordinary MITM connector length: {recovery.ordinary_mitm_connector_length}")
    print(f"ordinary MITM endpoint verified: {recovery.ordinary_mitm_endpoint_verified}")
    for result in recovery.quotients:
        print(f"quotient: {result.quotient_name}")
        print(f"  degree: {result.quotient_degree}")
        print(f"  reverse states/transitions: {result.quotient_reverse_states}/{result.quotient_reverse_transitions}")
        print(f"  quotient shortest distance: {result.quotient_shortest_distance}")
        print(f"  quotient distance gap: {result.quotient_distance_gap}")
        print(f"  exact states kept: {result.exact_states_kept}")
        print(f"  exact transitions tested: {result.exact_transitions_tested}")
        print(f"  exact candidate prunes: {result.exact_candidate_prunes}")
        print(f"  exact duplicate skips: {result.exact_duplicate_skips}")
        print(f"  distinct quotient states seen: {result.distinct_quotient_states_seen}")
        print(f"  max exact states per quotient: {result.max_exact_states_per_quotient}")
        print(f"  exact state fraction of generator ball: {result.exact_state_fraction_of_generator_ball:.9f}")
        print(f"  recovered connector length: {result.recovered_connector_length}")
        print(f"  endpoint verified: {result.endpoint_verified}")


if __name__ == "__main__":
    main()
