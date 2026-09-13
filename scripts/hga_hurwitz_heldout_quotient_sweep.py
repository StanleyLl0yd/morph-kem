from __future__ import annotations

import argparse
import hashlib

from morph_kem.hga_hurwitz_heldout_quotient import (
    HGA4E_PARAMETER_SETS,
    generate_hga4e_instance,
    recover_hga4e,
)


def seed_for(name: str, index: int) -> bytes:
    return hashlib.sha256(
        f"MORPH-KEM HGA4e sweep {name} seed {index} v1".encode("ascii")
    ).digest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 32:
        raise SystemExit("--seeds must be in 1..32")

    print(
        "set,seed,D,kind,quotient,ball,shell,mitm_states,mitm_transitions,states,"
        "transitions,prunes,duplicates,ball_fraction,mitm_fraction,connector,accepted,"
        "training_proxy_fraction,training_below"
    )
    for params in HGA4E_PARAMETER_SETS.values():
        for index in range(args.seeds):
            public, reference = generate_hga4e_instance(
                params, seed_for(params.name, index)
            )
            recovery = recover_hga4e(public, reference=reference)
            for metric in recovery.training_metrics:
                print(
                    f"{params.name},{index},{params.exact_distance},training,"
                    f"{metric.quotient_name},{recovery.generator_ball_states},"
                    f"{recovery.generator_shell_states},{recovery.ordinary_mitm_states},"
                    f"{recovery.ordinary_mitm_transitions},{metric.actual_exact_states_retained},"
                    f"{metric.actual_exact_transitions},0,0,"
                    f"{metric.actual_exact_states_retained/recovery.generator_ball_states:.9f},"
                    f"{metric.actual_exact_states_retained/recovery.ordinary_mitm_states:.9f},"
                    f"{params.exact_distance},{int(metric.actual_endpoint_verified)},"
                    f"{metric.selected_retained_proxy_fraction:.9f},"
                    f"{metric.shell_targets_below_selected_retention}"
                )
            for attack in recovery.heldout:
                print(
                    f"{params.name},{index},{params.exact_distance},heldout,"
                    f"{attack.quotient_label},{recovery.generator_ball_states},"
                    f"{recovery.generator_shell_states},{recovery.ordinary_mitm_states},"
                    f"{recovery.ordinary_mitm_transitions},{attack.exact_states_kept},"
                    f"{attack.exact_transitions_tested},{attack.exact_candidate_prunes},"
                    f"{attack.exact_duplicate_skips},"
                    f"{attack.exact_state_fraction_of_generator_ball:.9f},"
                    f"{attack.exact_state_fraction_of_ordinary_mitm_states:.9f},"
                    f"{attack.recovered_connector_length},{int(attack.endpoint_verified)},,,"
                )


if __name__ == "__main__":
    main()
