from __future__ import annotations

import argparse
import hashlib

from morph_kem.tdc_cyclic_lift import (
    TDC2C_LIFT_PARAMETER_SETS,
    generate_tdc2c_lift_instance,
    recover_tdc2c_lift,
)


def describe(label: str, recovery) -> None:
    print(f"{label} color rounds: {recovery.stabilized_rounds}")
    print(f"{label} color class sizes: {recovery.color_class_histogram}")
    print(f"{label} row/column quotient classes: {recovery.row_class_count}/{recovery.column_class_count}")
    print(f"{label} exact fiber partition: {recovery.exact_fiber_partition}")
    print(f"{label} quotient valid: {recovery.quotient_valid}")
    print(f"{label} quotient kernel weight <=6: {recovery.quotient_kernel_weight}")
    print(f"{label} lifted kernel weight: {recovery.lifted_kernel_weight}")
    print(f"{label} lifted kernel verified: {recovery.lifted_kernel_verified}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(TDC2C_LIFT_PARAMETER_SETS), default="tdc2c-n10-L4")
    args = parser.parse_args()
    params = TDC2C_LIFT_PARAMETER_SETS[args.params]
    seed = hashlib.sha256(
        f"MORPH-KEM TDC2c fixed baseline {params.name} v1".encode("ascii")
    ).digest()
    instance = generate_tdc2c_lift_instance(params, seed)
    recovery = recover_tdc2c_lift(instance)

    print(f"parameters: {params.name}")
    print(f"lift degree: {params.lift_degree}")
    print(f"topology lifted rows/columns: {instance.topology.row_count}/{len(instance.topology.columns)}")
    print(f"random lifted rows/columns: {instance.matched_random.row_count}/{len(instance.matched_random.columns)}")
    describe("topology", recovery.topology)
    describe("random", recovery.matched_random)


if __name__ == "__main__":
    main()
