from __future__ import annotations

import argparse
import hashlib
from collections import Counter

from morph_kem.hga_hurwitz_adaptive_quotient import (
    HGA4F_PARAMETER_SETS,
    generate_hga4f_instance,
    recover_hga4f,
)


def seed_for(name: str, index: int) -> bytes:
    return hashlib.sha256(
        f"MORPH-KEM HGA4f sweep {name} seed {index} v1".encode("ascii")
    ).digest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 32:
        raise SystemExit("--seeds must be in 1..32")

    print(
        "set,seed,D,ball,shell,mitm_states,mitm_transitions,best_single,best_single_states,"
        "top3,best_product,best_product_states,best_product_ball_fraction,"
        "best_product_mitm_fraction,accepted"
    )
    total = 0
    accepted = 0
    below_20 = 0
    below_mitm = 0
    fractions: list[float] = []
    selected_counter: Counter[str] = Counter()
    product_counter: Counter[str] = Counter()
    by_distance: dict[int, dict[str, float | int]] = {}

    for params in HGA4F_PARAMETER_SETS.values():
        for index in range(args.seeds):
            public, reference = generate_hga4f_instance(
                params, seed_for(params.name, index)
            )
            recovery = recover_hga4f(public, reference=reference)
            best_product = min(
                recovery.products,
                key=lambda item: (item.exact_states_kept, item.exact_transitions_tested, item.label),
            )
            ok = (
                recovery.ordinary_endpoint_verified
                and all(item.endpoint_verified for item in recovery.singles)
                and all(item.endpoint_verified for item in recovery.products)
            )
            top3 = "+".join(recovery.selected_single_labels)
            print(
                f"{params.name},{index},{params.exact_distance},"
                f"{recovery.generator_ball_states},{recovery.generator_shell_states},"
                f"{recovery.ordinary_mitm_states},{recovery.ordinary_mitm_transitions},"
                f"{recovery.best_single_label},{recovery.best_single_states},"
                f'"{top3}",{recovery.best_product_label},{recovery.best_product_states},'
                f"{recovery.best_product_fraction_of_generator_ball:.9f},"
                f"{recovery.best_product_fraction_of_ordinary_mitm_states:.9f},{int(ok)}"
            )
            total += 1
            accepted += int(ok)
            below_20 += int(recovery.best_product_fraction_of_generator_ball < 0.20)
            below_mitm += int(recovery.best_product_fraction_of_ordinary_mitm_states < 1.0)
            fractions.append(recovery.best_product_fraction_of_generator_ball)
            selected_counter.update(recovery.selected_single_labels)
            product_counter[recovery.best_product_label] += 1

            bucket = by_distance.setdefault(
                params.exact_distance,
                {
                    "runs": 0,
                    "accepted": 0,
                    "below20": 0,
                    "below_mitm": 0,
                    "min": 1.0,
                    "max": 0.0,
                    "sum": 0.0,
                },
            )
            bucket["runs"] = int(bucket["runs"]) + 1
            bucket["accepted"] = int(bucket["accepted"]) + int(ok)
            bucket["below20"] = int(bucket["below20"]) + int(
                recovery.best_product_fraction_of_generator_ball < 0.20
            )
            bucket["below_mitm"] = int(bucket["below_mitm"]) + int(
                recovery.best_product_fraction_of_ordinary_mitm_states < 1.0
            )
            bucket["min"] = min(
                float(bucket["min"]), recovery.best_product_fraction_of_generator_ball
            )
            bucket["max"] = max(
                float(bucket["max"]), recovery.best_product_fraction_of_generator_ball
            )
            bucket["sum"] = float(bucket["sum"]) + recovery.best_product_fraction_of_generator_ball

    print(
        "# summary,runs,accepted,below20pct_ball,below_mitm_states,min_ball_fraction,"
        "max_ball_fraction,mean_ball_fraction"
    )
    print(
        f"# summary,{total},{accepted},{below_20},{below_mitm},"
        f"{min(fractions):.9f},{max(fractions):.9f},{sum(fractions)/len(fractions):.9f}"
    )
    for distance in sorted(by_distance):
        bucket = by_distance[distance]
        runs = int(bucket["runs"])
        print(
            f"# distance-summary,D{distance},{runs},{int(bucket['accepted'])},"
            f"{int(bucket['below20'])},{int(bucket['below_mitm'])},"
            f"{float(bucket['min']):.9f},{float(bucket['max']):.9f},"
            f"{float(bucket['sum'])/runs:.9f}"
        )
    print(f"# selected-single-frequency,{dict(sorted(selected_counter.items()))}")
    print(f"# best-product-frequency,{dict(sorted(product_counter.items()))}")


if __name__ == "__main__":
    main()
