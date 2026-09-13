from __future__ import annotations

import argparse
import hashlib

from morph_kem.tdc_irregular_expansion import (
    TDC2D_PARAMETER_SETS,
    generate_tdc2d_instance,
    recover_tdc2d,
)


def describe(label: str, metrics) -> None:
    print(f"{label} rows/columns: {metrics.rows}/{metrics.columns}")
    print(f"{label} row multiplicities: {metrics.row_multiplicity_histogram}")
    print(f"{label} row weights: {metrics.row_weight_histogram}")
    print(f"{label} column weights: {metrics.column_weight_histogram}")
    print(f"{label} color rounds: {metrics.color_rounds}")
    print(f"{label} color class sizes: {metrics.color_class_size_histogram}")
    print(f"{label} singleton/max color classes: {metrics.singleton_color_classes}/{metrics.maximum_color_class_size}")
    print(
        f"{label} exact row fibers by color: "
        f"{metrics.exact_row_fibers_recovered_by_color}/{metrics.total_row_fibers}"
    )
    print(
        f"{label} exact column fibers by color: "
        f"{metrics.exact_column_fibers_recovered_by_color}/{metrics.total_column_fibers}"
    )
    print(f"{label} minimum weight <=6: {metrics.minimum_weight_leq6}")
    print(f"{label} minimum-weight multiplicity: {metrics.minimum_weight_multiplicity}")
    print(
        f"{label} pair/triple collision buckets: "
        f"{metrics.pair_syndrome_collision_buckets}/{metrics.triple_syndrome_collision_buckets}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(TDC2D_PARAMETER_SETS), default="tdc2d-n10")
    args = parser.parse_args()
    params = TDC2D_PARAMETER_SETS[args.params]
    seed = hashlib.sha256(
        f"MORPH-KEM TDC2d fixed baseline {params.name} v1".encode("ascii")
    ).digest()
    recovery = recover_tdc2d(generate_tdc2d_instance(params, seed))
    print(f"parameters: {params.name}")
    describe("topology", recovery.topology)
    describe("random", recovery.matched_random)


if __name__ == "__main__":
    main()
