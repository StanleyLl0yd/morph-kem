from __future__ import annotations

import argparse
import hashlib

from morph_kem.tdc_cyclic_lift import (
    TDC2C_LIFT_PARAMETER_SETS,
    generate_tdc2c_lift_instance,
    recover_tdc2c_lift,
)


def seed_for(name: str, index: int) -> bytes:
    return hashlib.sha256(
        f"MORPH-KEM TDC2c sweep {name} seed {index} v1".encode("ascii")
    ).digest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 16:
        raise SystemExit("--seeds must be between 1 and 16")

    print(
        "set,seed,L,kind,lift_rows,lift_cols,color_rounds,fiber_partition,quotient_valid,"
        "quotient_rows,quotient_cols,quotient_kernel,lifted_kernel,lifted_verified,class_sizes"
    )
    for params in TDC2C_LIFT_PARAMETER_SETS.values():
        for index in range(args.seeds):
            instance = generate_tdc2c_lift_instance(params, seed_for(params.name, index))
            recovery = recover_tdc2c_lift(instance)
            for kind, code, result in (
                ("topology", instance.topology, recovery.topology),
                ("random", instance.matched_random, recovery.matched_random),
            ):
                print(
                    f"{params.name},{index},{params.lift_degree},{kind},"
                    f"{code.row_count},{len(code.columns)},"
                    f"{result.stabilized_rounds},{int(result.exact_fiber_partition)},"
                    f"{int(result.quotient_valid)},{result.row_class_count},{result.column_class_count},"
                    f"{result.quotient_kernel_weight},{result.lifted_kernel_weight},"
                    f"{int(result.lifted_kernel_verified)},\"{result.color_class_histogram}\""
                )


if __name__ == "__main__":
    main()
