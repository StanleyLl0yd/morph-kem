from __future__ import annotations

import argparse
import hashlib

from morph_kem.hga_hurwitz_finite_quotient import (
    HGA4D_PARAMETER_SETS,
    generate_hga4d_instance,
    recover_hga4d,
)


def seed_for(name: str, index: int) -> bytes:
    return hashlib.sha256(
        f"MORPH-KEM HGA4d sweep {name} seed {index} v1".encode("ascii")
    ).digest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 16:
        raise SystemExit("--seeds must be between 1 and 16")

    print(
        "set,seed,D,quotient,generator_ball,generator_shell,ordinary_mitm_states,"
        "ordinary_mitm_transitions,quotient_reverse_states,quotient_reverse_transitions,"
        "quotient_distance,distance_gap,exact_states,exact_transitions,prunes,duplicates,"
        "quotient_states_seen,max_exact_per_quotient,state_fraction,recovered,accepted"
    )
    for params in HGA4D_PARAMETER_SETS.values():
        for index in range(args.seeds):
            public, reference = generate_hga4d_instance(
                params, seed_for(params.name, index)
            )
            recovery = recover_hga4d(public, reference=reference)
            for result in recovery.quotients:
                print(
                    f"{params.name},{index},{params.exact_distance},{result.quotient_name},"
                    f"{recovery.generator_ball_states},{recovery.generator_shell_states},"
                    f"{recovery.ordinary_mitm_states},{recovery.ordinary_mitm_transitions},"
                    f"{result.quotient_reverse_states},{result.quotient_reverse_transitions},"
                    f"{result.quotient_shortest_distance},{result.quotient_distance_gap},"
                    f"{result.exact_states_kept},{result.exact_transitions_tested},"
                    f"{result.exact_candidate_prunes},{result.exact_duplicate_skips},"
                    f"{result.distinct_quotient_states_seen},{result.max_exact_states_per_quotient},"
                    f"{result.exact_state_fraction_of_generator_ball:.9f},"
                    f"{result.recovered_connector_length},{int(result.endpoint_verified)}"
                )


if __name__ == "__main__":
    main()
