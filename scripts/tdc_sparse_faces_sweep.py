from __future__ import annotations

import argparse

from morph_kem.tdc_sparse_faces import (
    TDC2_SPARSE_PARAMETER_SETS,
    generate_tdc2_sparse_instance,
    sparse_face_metrics,
    topology_sparse_face_metrics,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 32:
        raise SystemExit("seed count outside toy bounds")

    print("set,seed,faces,skipped,top_rank,top_dim,top_min_le6,top_min_mult,random_rank,random_dim,random_min_le6,random_min_mult,random_retries")
    for name in sorted(TDC2_SPARSE_PARAMETER_SETS):
        params = TDC2_SPARSE_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            seed = (f"MORPH-KEM TDC2b sweep {name} seed {seed_index:02d} v1").encode().ljust(48, b".")
            instance = generate_tdc2_sparse_instance(params, seed)
            topology = topology_sparse_face_metrics(params, seed, instance.topology_code)
            random_control = sparse_face_metrics(instance.matched_random)
            print(
                f"{name},{seed_index},{instance.selected_face_count},{instance.skipped_tetrahedron_completions},"
                f"{topology.rank},{topology.dimension},{topology.minimum_weight_leq6 or 0},{topology.minimum_weight_multiplicity},"
                f"{random_control.rank},{random_control.dimension},{random_control.minimum_weight_leq6 or 0},"
                f"{random_control.minimum_weight_multiplicity},{instance.random_generation_retries}"
            )


if __name__ == "__main__":
    main()
