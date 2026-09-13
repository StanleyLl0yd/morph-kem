from __future__ import annotations

import argparse
import hashlib

from morph_kem.hga_hurwitz_self_avoiding import (
    HGA4B_PARAMETER_SETS,
    generate_hga4b_instance,
    recover_hga4b_paired,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(HGA4B_PARAMETER_SETS), default="hga4b-L20")
    args = parser.parse_args()
    params = HGA4B_PARAMETER_SETS[args.params]
    seed = hashlib.sha256(
        f"MORPH-KEM HGA4b fixed baseline {params.name} v1".encode("ascii")
    ).digest()

    _, reference = generate_hga4b_instance(params, seed)
    paired = recover_hga4b_paired(params, seed)
    recovery = paired.self_avoiding
    old = paired.locally_reduced

    print(f"parameters: {params.name}")
    print(f"requested / achieved self-avoiding length: {params.planted_word_length}/{len(reference.planted_word)}")
    print(f"distinct generated path states: {reference.distinct_path_states}")
    print(f"generator dead ends: {reference.dead_end_count}")
    print(f"source component lengths: {recovery.source_component_lengths}")
    print(f"target component lengths: {recovery.target_component_lengths}")
    print(f"invariant product length / verified: {recovery.invariant_product_length}/{recovery.invariant_product_verified}")
    print(f"recovered strand permutation: {recovery.recovered_strand_permutation}")
    print(f"quotient matches planted: {recovery.quotient_matches_planted}")
    print(f"forward/backward depth: {recovery.forward_depth}/{recovery.backward_depth}")
    print(f"forward/backward states: {recovery.forward_states}/{recovery.backward_states}")
    print(f"forward/backward transitions: {recovery.forward_transitions}/{recovery.backward_transitions}")
    print(f"meet states: {recovery.meet_states}")
    print(f"self-avoiding recovered connector length: {recovery.recovered_connector_length}")
    print(f"self-avoiding materially shorter: {recovery.materially_shorter_than_planted}")
    print(f"self-avoiding endpoint verified: {recovery.endpoint_verified}")
    print(f"self-avoiding matches planted word: {recovery.matches_planted_word_after_public_success}")
    print(f"paired old recovered connector length: {old.recovered_connector_length}")
    print(f"paired old materially shorter: {old.materially_shorter_than_planted}")
    print(f"paired old forward/backward states: {old.forward_states}/{old.backward_states}")


if __name__ == "__main__":
    main()
