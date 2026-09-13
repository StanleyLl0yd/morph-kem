from __future__ import annotations

import argparse

from morph_kem.tdc_sparse_faces import (
    TDC2_SPARSE_PARAMETER_SETS,
    generate_tdc2_sparse_instance,
    sparse_face_metrics,
    topology_sparse_face_metrics,
)


def show(label: str, metrics: object) -> None:
    print(f"{label} rows/columns/rank/dimension/rate: {metrics.rows}/{metrics.columns}/{metrics.rank}/{metrics.dimension}/{metrics.rate:.9f}")
    print(f"{label} row weights: {metrics.row_weight_histogram}")
    print(f"{label} column weights: {metrics.column_weight_histogram}")
    print(f"{label} tetrahedron boundaries: {metrics.tetrahedron_boundary_count}")
    print(f"{label} minimum weight <=6: {metrics.minimum_weight_leq6}")
    print(f"{label} minimum-weight multiplicity: {metrics.minimum_weight_multiplicity}")
    print(f"{label} pair collision buckets: {metrics.pair_syndrome_collision_buckets}")
    print(f"{label} triple collision buckets: {metrics.triple_syndrome_collision_buckets}")
    print(f"{label} non-graphic obstruction: {metrics.graphic_column_weight_obstruction}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(TDC2_SPARSE_PARAMETER_SETS), default="tdc2b-n10")
    args = parser.parse_args()
    params = TDC2_SPARSE_PARAMETER_SETS[args.params]
    seed = b"MORPH-KEM TDC2b fixed baseline seed v1"
    instance = generate_tdc2_sparse_instance(params, seed)
    topology = topology_sparse_face_metrics(params, seed, instance.topology_code)
    random_control = sparse_face_metrics(instance.matched_random)
    print(f"parameters: {params.name}")
    print(f"selected faces: {instance.selected_face_count}")
    print(f"skipped tetrahedron completions: {instance.skipped_tetrahedron_completions}")
    print(f"matched-random retries: {instance.random_generation_retries}")
    show("topology", topology)
    show("random", random_control)


if __name__ == "__main__":
    main()
