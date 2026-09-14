from __future__ import annotations

import argparse
import hashlib

from morph_kem.nat_noisy_sl2_trace import (
    NAT10_PARAMETER_SETS,
    generate_nat10_instance,
    recover_nat10,
    sl2_group,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(NAT10_PARAMETER_SETS), default="nat10-p7-X8")
    args = parser.parse_args()
    params = NAT10_PARAMETER_SETS[args.params]
    seed = hashlib.sha256(
        f"MORPH-KEM NAT10 fixed baseline {params.name} v1".encode("ascii")
    ).digest()
    public, reference = generate_nat10_instance(params, seed)
    recovery = recover_nat10(public, reference=reference)

    print(f"parameters: {params.name}")
    print(f"prime / group size: {params.p}/{len(sl2_group(params.p))}")
    print(f"noise radius: {params.noise_radius}")
    print(f"generation attempts: {reference.generation_attempts}")
    print(f"public noisy trace centers: {public.trace_centers}")
    print(f"reference exact traces: {reference.exact_traces}")
    print(f"reference noise values: {reference.noise_values}")
    print(f"generator candidate sizes: {recovery.generator_candidate_sizes}")
    print(f"left pairs considered/retained: {recovery.left_pairs_considered}/{recovery.left_pairs_retained}")
    print(f"right pairs considered/retained: {recovery.right_pairs_considered}/{recovery.right_pairs_retained}")
    print(f"relator join candidates: {recovery.relator_join_candidates}")
    print(f"verifier candidates tested: {recovery.verifier_candidates_tested}")
    print(f"accepted representations: {recovery.accepted_representations}")
    print(f"conjugacy-orbit lower bound: {recovery.conjugacy_orbit_lower_bound}")
    print(f"public recovery accepted: {recovery.accepted}")
    print(f"first recovered equals planted after success: {recovery.recovered_matches_planted_after_public_success}")


if __name__ == "__main__":
    main()
