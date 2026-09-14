from __future__ import annotations

import argparse
import hashlib

from morph_kem.nat_lossy_a5_surface import (
    NAT9_PARAMETER_SETS,
    generate_nat9_instance,
    recover_nat9,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(NAT9_PARAMETER_SETS), default="nat9-X4")
    args = parser.parse_args()
    params = NAT9_PARAMETER_SETS[args.params]
    seed = hashlib.sha256(
        f"MORPH-KEM NAT9 fixed baseline {params.name} v1".encode("ascii")
    ).digest()
    public, reference = generate_nat9_instance(params, seed)
    recovery = recover_nat9(public, reference=reference)

    print(f"parameters: {params.name}")
    print(f"generation attempts: {reference.generation_attempts}")
    print(f"generator cycle types: {public.generator_classes}")
    print(f"product cycle types: {public.product_classes}")
    print(f"candidate class sizes: {recovery.generator_candidate_sizes}")
    print(f"left pairs considered/retained: {recovery.left_pairs_considered}/{recovery.left_pairs_retained}")
    print(f"right pairs considered/retained: {recovery.right_pairs_considered}/{recovery.right_pairs_retained}")
    print(f"relator join candidates: {recovery.relator_join_candidates}")
    print(f"verifier candidates tested: {recovery.verifier_candidates_tested}")
    print(f"accepted representations: {recovery.accepted_representations}")
    print(f"public recovery accepted: {recovery.accepted}")
    print(f"first recovered equals planted after success: {recovery.recovered_matches_planted_after_public_success}")


if __name__ == "__main__":
    main()
