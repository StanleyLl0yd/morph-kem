from __future__ import annotations

import argparse

from morph_kem.hga_intertwiner import HGA3_PARAMETER_SETS, generate_hga3_instance, recover_hga3


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(HGA3_PARAMETER_SETS), default="hga3-p11-n5")
    args = parser.parse_args()
    params = HGA3_PARAMETER_SETS[args.params]
    public, reference = generate_hga3_instance(params, b"MORPH-KEM HGA3 fixed baseline seed v1")
    result = recover_hga3(public, reference=reference)
    print(f"parameters: {params.name}")
    print(f"prime / dimension / tuple length: {result.prime}/{result.dimension}/{result.tuple_length}")
    print(f"linear variables / equations: {result.variables}/{result.equations}")
    print(f"system rank / nullity: {result.system_rank}/{result.system_nullity}")
    print(f"row eliminations: {result.row_eliminations}")
    print(f"invertible combinations tested: {result.combination_candidates_tested}")
    print(f"recovered rank / determinant: {result.recovered_rank}/{result.recovered_determinant}")
    print(f"endpoint verified: {result.exact_endpoint_verified}")
    print(f"scalar-equivalent to planted after public success: {result.scalar_equivalent_to_planted_after_public_success}")
    print(f"exactly matches planted after public success: {result.exactly_matches_planted_after_public_success}")
    print(f"source trace fingerprint: {result.source_trace_fingerprint}")
    print(f"target trace fingerprint: {result.target_trace_fingerprint}")


if __name__ == "__main__":
    main()
