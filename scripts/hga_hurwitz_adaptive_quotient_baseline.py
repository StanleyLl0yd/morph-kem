from __future__ import annotations

import argparse
import hashlib

from morph_kem.hga_hurwitz_adaptive_quotient import (
    HGA4F_PARAMETER_SETS,
    generate_hga4f_instance,
    recover_hga4f,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(HGA4F_PARAMETER_SETS), default="hga4f-D8")
    args = parser.parse_args()
    params = HGA4F_PARAMETER_SETS[args.params]
    seed = hashlib.sha256(
        f"MORPH-KEM HGA4f fixed baseline {params.name} v1".encode("ascii")
    ).digest()
    public, reference = generate_hga4f_instance(params, seed)
    recovery = recover_hga4f(public, reference=reference)

    print(f"parameters: {params.name}")
    print(f"exact distance: {recovery.exact_distance}")
    print(
        f"generator ball/shell/transitions: {recovery.generator_ball_states}/"
        f"{recovery.generator_shell_states}/{recovery.generator_transitions}"
    )
    print(
        f"ordinary MITM states/transitions: {recovery.ordinary_mitm_states}/"
        f"{recovery.ordinary_mitm_transitions}"
    )
    print(f"representation library size: {recovery.library_size}")
    for metric in sorted(recovery.singles, key=lambda item: (item.exact_states_kept, item.label)):
        print(
            f"single {metric.label}: states={metric.exact_states_kept} "
            f"transitions={metric.exact_transitions_tested} "
            f"ball_fraction={metric.exact_state_fraction_of_generator_ball:.9f} "
            f"mitm_fraction={metric.exact_state_fraction_of_ordinary_mitm_states:.9f} "
            f"accepted={metric.endpoint_verified}"
        )
    print(f"selected top singles: {recovery.selected_single_labels}")
    for metric in sorted(recovery.products, key=lambda item: (item.exact_states_kept, item.label)):
        print(
            f"product {metric.label}: states={metric.exact_states_kept} "
            f"transitions={metric.exact_transitions_tested} "
            f"ball_fraction={metric.exact_state_fraction_of_generator_ball:.9f} "
            f"mitm_fraction={metric.exact_state_fraction_of_ordinary_mitm_states:.9f} "
            f"accepted={metric.endpoint_verified}"
        )
    print(f"best single: {recovery.best_single_label}/{recovery.best_single_states}")
    print(f"best product: {recovery.best_product_label}/{recovery.best_product_states}")
    print(f"best product fraction of ball: {recovery.best_product_fraction_of_generator_ball:.9f}")
    print(f"best product fraction of MITM states: {recovery.best_product_fraction_of_ordinary_mitm_states:.9f}")


if __name__ == "__main__":
    main()
