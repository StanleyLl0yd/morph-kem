#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.nat_coboundary import (
    NAT0_PARAMETER_SETS,
    generate_nat0_repeated_instance,
    generate_nat0_single_instance,
    recover_nat0_repeated,
    recover_nat0_single,
)


MASTER_SEED = bytes.fromhex("0011aabb2233ccdd4455eeff66778899")


def _counts(target) -> tuple[int, int, int]:
    return (
        sum(len(simplex) == 1 for simplex in target.simplices),
        sum(len(simplex) == 2 for simplex in target.simplices),
        sum(len(simplex) == 3 for simplex in target.simplices),
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run MORPH-KEM NAT0 noisy coboundary negative controls."
    )
    parser.add_argument("--params", choices=sorted(NAT0_PARAMETER_SETS), default="nat0-8x8")
    args = parser.parse_args()
    params = NAT0_PARAMETER_SETS[args.params]

    single_public, single_reference = generate_nat0_single_instance(params, MASTER_SEED)
    single = recover_nat0_single(single_public, reference=single_reference)
    repeated_public, repeated_reference = generate_nat0_repeated_instance(params, MASTER_SEED)
    repeated = recover_nat0_repeated(repeated_public, reference=repeated_reference)
    vertices, edges, triangles = _counts(single_public.target)

    print(f"parameters: {params.name}")
    print(f"public V/E/F: {vertices}/{edges}/{triangles}")
    print(f"single violated triangles: {single.violated_triangles}")
    print(f"single recovered noise edge: {single.recovered_noise_edge}")
    print(f"single accepted: {single.accepted}")
    print(
        "single matches reference after public success: "
        f"{single.matches_reference_after_public_success}"
    )
    print(f"repeated samples: {len(repeated_public.observed_edge_masks)}")
    print(f"public repeated noise weight: {repeated_public.public_noise_weight}")
    print(f"repeated sample distances: {repeated.sample_distances}")
    print(f"majority edge votes: {repeated.majority_edge_votes}")
    print(f"repeated accepted: {repeated.accepted}")
    print(
        "repeated matches reference after public success: "
        f"{repeated.matches_reference_after_public_success}"
    )

    return 0 if (
        single.accepted
        and single.matches_reference_after_public_success
        and repeated.accepted
        and repeated.matches_reference_after_public_success
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
