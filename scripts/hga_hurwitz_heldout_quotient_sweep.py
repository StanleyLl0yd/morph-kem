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
    summary: dict[str, dict[str, float | int]] = {}
    distance_summary: dict[tuple[str, int], dict[str, float | int]] = {}

    def record(label: str, distance: int, ball_fraction: float, mitm_fraction: float, accepted: bool) -> None:
        for key in ((label, None), (label, distance)):
            bucket = summary.setdefault(label, {}) if key[1] is None else distance_summary.setdefault((label, distance), {})
            bucket["runs"] = int(bucket.get("runs", 0)) + 1
            bucket["accepted"] = int(bucket.get("accepted", 0)) + int(accepted)
            bucket["below_20pct_ball"] = int(bucket.get("below_20pct_ball", 0)) + int(ball_fraction < 0.20)
            bucket["below_mitm_states"] = int(bucket.get("below_mitm_states", 0)) + int(mitm_fraction < 1.0)
            bucket["min_ball_fraction"] = min(float(bucket.get("min_ball_fraction", 1.0)), ball_fraction)
            bucket["max_ball_fraction"] = max(float(bucket.get("max_ball_fraction", 0.0)), ball_fraction)
            bucket["sum_ball_fraction"] = float(bucket.get("sum_ball_fraction", 0.0)) + ball_fraction

    for params in HGA4E_PARAMETER_SETS.values():
        for index in range(args.seeds):
            public, reference = generate_hga4e_instance(
                params, seed_for(params.name, index)
            )
            recovery = recover_hga4e(public, reference=reference)
            for metric in recovery.training_metrics:
                ball_fraction = metric.actual_exact_states_retained / recovery.generator_ball_states
                mitm_fraction = metric.actual_exact_states_retained / recovery.ordinary_mitm_states
                print(
                    f"{params.name},{index},{params.exact_distance},training,"
                    f"{metric.quotient_name},{recovery.generator_ball_states},"
                    f"{recovery.generator_shell_states},{recovery.ordinary_mitm_states},"
                    f"{recovery.ordinary_mitm_transitions},{metric.actual_exact_states_retained},"
                    f"{metric.actual_exact_transitions},0,0,"
                    f"{ball_fraction:.9f},{mitm_fraction:.9f},"
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
                record(
                    attack.quotient_label,
                    params.exact_distance,
                    attack.exact_state_fraction_of_generator_ball,
                    attack.exact_state_fraction_of_ordinary_mitm_states,
                    attack.endpoint_verified,
                )

    print("# held-out summary: quotient,runs,accepted,below20pct_ball,below_mitm_states,min_ball_fraction,max_ball_fraction,mean_ball_fraction")
    for label in sorted(summary):
        bucket = summary[label]
        runs = int(bucket["runs"])
        print(
            f"# summary,{label},{runs},{int(bucket['accepted'])},"
            f"{int(bucket['below_20pct_ball'])},{int(bucket['below_mitm_states'])},"
            f"{float(bucket['min_ball_fraction']):.9f},{float(bucket['max_ball_fraction']):.9f},"
            f"{float(bucket['sum_ball_fraction']) / runs:.9f}"
        )
    print("# held-out distance summary: quotient,D,runs,accepted,below20pct_ball,below_mitm_states,min_ball_fraction,max_ball_fraction,mean_ball_fraction")
    for label, distance in sorted(distance_summary):
        bucket = distance_summary[(label, distance)]
        runs = int(bucket["runs"])
        print(
            f"# distance-summary,{label},{distance},{runs},{int(bucket['accepted'])},"
            f"{int(bucket['below_20pct_ball'])},{int(bucket['below_mitm_states'])},"
            f"{float(bucket['min_ball_fraction']):.9f},{float(bucket['max_ball_fraction']):.9f},"
            f"{float(bucket['sum_ball_fraction']) / runs:.9f}"
        )


if __name__ == "__main__":
    main()
