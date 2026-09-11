from __future__ import annotations

import argparse

from morph_kem.tdc_boundary2 import TDC2_PARAMETER_SETS, boundary_code_metrics, generate_tdc2_instance


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 32:
        raise SystemExit("seed count outside toy bounds")
    print("set,seed,rows,cols,top_rank,top_dim,top_low_le3,top_w4,random_rank,random_dim,random_low_le3,random_w4,random_retries")
    for name in sorted(TDC2_PARAMETER_SETS):
        params = TDC2_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            seed = (f"MORPH-KEM TDC2 sweep {name} seed {seed_index:02d} v1").encode().ljust(48, b".")
            instance = generate_tdc2_instance(params, seed)
            topology = boundary_code_metrics(instance.topology_code)
            random_control = boundary_code_metrics(instance.matched_random)
            print(
                f"{name},{seed_index},{topology.rows},{topology.columns},{topology.rank},{topology.dimension},"
                f"{topology.minimum_weight_leq3 or 0},{topology.weight4_codewords},"
                f"{random_control.rank},{random_control.dimension},{random_control.minimum_weight_leq3 or 0},"
                f"{random_control.weight4_codewords},{instance.random_generation_retries}"
            )


if __name__ == "__main__":
    main()
