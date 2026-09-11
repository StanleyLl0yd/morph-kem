from __future__ import annotations

import argparse

from morph_kem.hga_modular import HGA2_PARAMETER_SETS, generate_hga2_instance, recover_hga2


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(HGA2_PARAMETER_SETS), default="hga2-32")
    args = parser.parse_args()
    params = HGA2_PARAMETER_SETS[args.params]
    public, reference = generate_hga2_instance(params, b"MORPH-KEM HGA2 fixed baseline seed v1")
    result = recover_hga2(public, reference=reference)

    print(f"parameters: {params.name}")
    print(f"source: {result.source[0]}/{result.source[1]}")
    print(f"target: {result.target[0]}/{result.target[1]}")
    print(f"source/target bit lengths: {result.source_bit_length}/{result.target_bit_length}")
    print(f"planted word length: {len(reference.planted_word)}")
    print(f"source Euclidean divisions: {result.source_euclidean_divisions}")
    print(f"target Euclidean divisions: {result.target_euclidean_divisions}")
    print(f"source quotients: {result.source_cf_quotients}")
    print(f"target quotients: {result.target_cf_quotients}")
    print(f"recovered connector length: {result.recovered_connector_length}")
    print(f"recovered matrix: {result.recovered_matrix}")
    print(f"matrix entry bit length: {result.recovered_matrix_entry_bit_length}")
    print(f"endpoint verified: {result.endpoint_verified}")
    print(f"matches planted word after public success: {result.matches_planted_word_after_public_success}")
    print(f"same PSL matrix as planted after public success: {result.planted_matrix_equal_after_public_success}")
    print(f"mod 5 fingerprint: {result.mod5_fingerprint}")
    print(f"mod 7 fingerprint: {result.mod7_fingerprint}")
    print(f"mod 11 fingerprint: {result.mod11_fingerprint}")


if __name__ == "__main__":
    main()
