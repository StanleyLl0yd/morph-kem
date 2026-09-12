from __future__ import annotations

import argparse

from morph_kem.tdc_boundary2 import TDC2_PARAMETER_SETS, boundary_code_metrics, generate_tdc2_instance


def show(label: str, metrics: object) -> None:
    print(f"{label} rows/columns/rank/dimension/rate: {metrics.rows}/{metrics.columns}/{metrics.rank}/{metrics.dimension}/{metrics.rate:.9f}")
    print(f"{label} row weights: {metrics.row_weight_histogram}")
    print(f"{label} column weights: {metrics.column_weight_histogram}")
    print(f"{label} minimum weight <=3: {metrics.minimum_weight_leq3}")
    print(f"{label} weight-4 codewords: {metrics.weight4_codewords}")
    print(f"{label} pair-syndrome collision buckets: {metrics.pair_syndrome_buckets_with_collisions}")
    print(f"{label} maximum pair-syndrome bucket: {metrics.maximum_pair_syndrome_bucket}")
    print(f"{label} non-graphic column-weight obstruction: {metrics.graphic_column_weight_obstruction}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(TDC2_PARAMETER_SETS), default="tdc2-n8")
    args = parser.parse_args()
    params = TDC2_PARAMETER_SETS[args.params]
    instance = generate_tdc2_instance(params, b"MORPH-KEM TDC2 fixed baseline seed v1")
    topology = boundary_code_metrics(instance.topology_code)
    random_control = boundary_code_metrics(instance.matched_random)
    print(f"parameters: {params.name}")
    print(f"random generation retries: {instance.random_generation_retries}")
    print(f"expected tetrahedron boundaries: {instance.expected_tetrahedron_boundaries}")
    show("topology", topology)
    show("random", random_control)


if __name__ == "__main__":
    main()
