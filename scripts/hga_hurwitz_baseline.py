from __future__ import annotations

import argparse

from morph_kem.hga_hurwitz import HGA4_PARAMETER_SETS, generate_hga4_instance, recover_hga4


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(HGA4_PARAMETER_SETS), default="hga4-L16")
    args = parser.parse_args()
    params = HGA4_PARAMETER_SETS[args.params]
    public, reference = generate_hga4_instance(params, b"MORPH-KEM HGA4 fixed baseline seed v1")
    result = recover_hga4(public, reference=reference)

    print(f"parameters: {params.name}")
    print(f"source component lengths: {result.source_component_lengths}")
    print(f"target component lengths: {result.target_component_lengths}")
    print(f"invariant product length / verified: {result.invariant_product_length}/{result.invariant_product_verified}")
    print(f"source abelianization: {result.source_abelianization}")
    print(f"target abelianization: {result.target_abelianization}")
    print(f"recovered strand permutation: {result.recovered_strand_permutation}")
    print(f"quotient matches planted: {result.quotient_matches_planted}")
    print(f"planted word length: {result.planted_word_length}")
    print(f"forward/backward depth: {result.forward_depth}/{result.backward_depth}")
    print(f"forward/backward states: {result.forward_states}/{result.backward_states}")
    print(f"forward/backward transitions: {result.forward_transitions}/{result.backward_transitions}")
    print(f"meet states: {result.meet_states}")
    print(f"recovered connector length: {result.recovered_connector_length}")
    print(f"materially shorter than planted: {result.materially_shorter_than_planted}")
    print(f"endpoint verified: {result.endpoint_verified}")
    print(f"matches planted word after public success: {result.matches_planted_word_after_public_success}")


if __name__ == "__main__":
    main()
