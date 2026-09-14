from __future__ import annotations

import argparse
import hashlib

from morph_kem.hga_hurwitz_heldout_quotient import (
    HGA4E_PARAMETER_SETS,
    generate_hga4e_instance,
    recover_hga4e,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--params", choices=sorted(HGA4E_PARAMETER_SETS), default="hga4e-D8"
    )
    args = parser.parse_args()
    params = HGA4E_PARAMETER_SETS[args.params]
    seed = hashlib.sha256(
        f"MORPH-KEM HGA4e fixed baseline {params.name} v1".encode("ascii")
    ).digest()
    public, reference = generate_hga4e_instance(params, seed)
    recovery = recover_hga4e(public, reference=reference)

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
    print(f"ordinary connector/accepted: {recovery.ordinary_connector_length}/{recovery.ordinary_endpoint_verified}")
    for item in recovery.training_metrics:
        print(f"training quotient: {item.quotient_name}")
        print(
            f"  proxy retained states/fraction: {item.selected_retained_proxy_states}/"
            f"{item.selected_retained_proxy_fraction:.9f}"
        )
        print(
            f"  shell targets below selected retention: "
            f"{item.shell_targets_below_selected_retention}"
        )
        print(
            f"  actual states/transitions/accepted: {item.actual_exact_states_retained}/"
            f"{item.actual_exact_transitions}/{item.actual_endpoint_verified}"
        )
    for attack in recovery.heldout:
        print(f"held-out quotient: {attack.quotient_label}")
        print(f"  components: {attack.quotient_components}")
        print(f"  reverse states: {attack.reverse_states}")
        print(f"  reverse transitions: {attack.reverse_transitions}")
        print(f"  quotient distances: {attack.quotient_distances}")
        print(f"  exact states/transitions: {attack.exact_states_kept}/{attack.exact_transitions_tested}")
        print(f"  candidate prunes/duplicates: {attack.exact_candidate_prunes}/{attack.exact_duplicate_skips}")
        print(
            f"  fractions ball/MITM: {attack.exact_state_fraction_of_generator_ball:.9f}/"
            f"{attack.exact_state_fraction_of_ordinary_mitm_states:.9f}"
        )
        print(
            f"  product states/max bucket: {attack.distinct_product_quotient_states_seen}/"
            f"{attack.max_exact_states_per_product_state}"
        )
        print(f"  connector/accepted: {attack.recovered_connector_length}/{attack.endpoint_verified}")


if __name__ == "__main__":
    main()
