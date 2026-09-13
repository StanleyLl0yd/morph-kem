from __future__ import annotations

import argparse
import hashlib

from morph_kem.tdc_sparse_mixing import (
    TDC2E_PARAMETER_SETS,
    generate_tdc2e_instance,
    recover_tdc2e,
)


def describe(label: str, result) -> None:
    print(f"{label} rows/columns: {result.rows}/{result.columns}")
    print(f"{label} rank/dimension/rate: {result.rank}/{result.dimension}/{result.rate:.6f}")
    print(f"{label} mixing operations/rejected candidates: {result.successful_mixing_operations}/{result.rejected_mixing_candidates}")
    print(f"{label} base column weights: {result.base_column_weight_histogram}")
    print(f"{label} public row weights: {result.public_row_weight_histogram}")
    print(f"{label} public column weights: {result.public_column_weight_histogram}")
    print(f"{label} minimum weight <=6: {result.minimum_weight_leq6}")
    print(f"{label} minimum-weight multiplicity: {result.minimum_weight_multiplicity}")
    print(f"{label} pair/triple syndrome collision buckets: {result.pair_syndrome_collision_buckets}/{result.triple_syndrome_collision_buckets}")
    print(f"{label} Tanner 4-cycles: {result.tanner_four_cycles}")
    print(f"{label} singleton weight-3 columns: {result.singleton_weight3_columns}")
    print(f"{label} pair weight-3 occurrences/distinct atoms: {result.pair_weight3_occurrences}/{result.distinct_pair_weight3_atoms}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--params", choices=sorted(TDC2E_PARAMETER_SETS), default="tdc2e-n10"
    )
    args = parser.parse_args()
    params = TDC2E_PARAMETER_SETS[args.params]
    seed = hashlib.sha256(
        f"MORPH-KEM TDC2e fixed baseline {params.name} v1".encode("ascii")
    ).digest()
    instance = generate_tdc2e_instance(params, seed)
    recovery = recover_tdc2e(instance)
    print(f"parameters: {params.name}")
    print(f"mixing rounds: {params.mixing_rounds}")
    describe("topology", recovery.topology)
    describe("random", recovery.matched_random)


if __name__ == "__main__":
    main()
