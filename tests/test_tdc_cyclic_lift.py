from __future__ import annotations

import hashlib
import unittest

from morph_kem.tdc_cyclic_lift import (
    TDC2CLiftError,
    TDC2CLiftParameters,
    TDC2C_LIFT_PARAMETER_SETS,
    generate_tdc2c_lift_instance,
    recover_tdc2c_lift,
)


def seed_for(label: str) -> bytes:
    return hashlib.sha256(label.encode("ascii")).digest()


class TDC2CCyclicLiftTests(unittest.TestCase):
    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(TDC2CLiftError):
            TDC2CLiftParameters("bad", "tdc2b-n8", 5).validate()
        with self.assertRaises(TDC2CLiftError):
            TDC2CLiftParameters("bad", "missing", 2).validate()
        with self.assertRaises(TDC2CLiftError):
            generate_tdc2c_lift_instance(
                TDC2C_LIFT_PARAMETER_SETS["tdc2c-n8-L2"], b"short"
            )

    def test_lift_preserves_column_weight_and_scales_sizes(self) -> None:
        for params in TDC2C_LIFT_PARAMETER_SETS.values():
            instance = generate_tdc2c_lift_instance(params, seed_for(params.name + "-sizes"))
            self.assertEqual(
                instance.topology.row_count,
                instance.base_topology_rows * params.lift_degree,
            )
            self.assertEqual(
                len(instance.topology.columns),
                instance.base_topology_columns * params.lift_degree,
            )
            self.assertTrue(all(column.bit_count() == 3 for column in instance.topology.columns))
            self.assertTrue(all(column.bit_count() == 3 for column in instance.matched_random.columns))

    def test_public_recovery_needs_no_reference_mapping(self) -> None:
        params = TDC2C_LIFT_PARAMETER_SETS["tdc2c-n8-L2"]
        instance = generate_tdc2c_lift_instance(params, seed_for("tdc2c-public"))
        recovery = recover_tdc2c_lift(instance)
        if recovery.topology.quotient_valid:
            self.assertTrue(recovery.topology.exact_fiber_partition)
            self.assertIsNotNone(recovery.topology.quotient)
            if recovery.topology.quotient_kernel_weight is not None:
                self.assertTrue(recovery.topology.lifted_kernel_verified)
                self.assertEqual(
                    recovery.topology.lifted_kernel_weight,
                    recovery.topology.quotient_kernel_weight * params.lift_degree,
                )

    def test_color_refinement_is_deterministic(self) -> None:
        params = TDC2C_LIFT_PARAMETER_SETS["tdc2c-n9-L3"]
        seed = seed_for("tdc2c-deterministic")
        first = recover_tdc2c_lift(generate_tdc2c_lift_instance(params, seed))
        second = recover_tdc2c_lift(generate_tdc2c_lift_instance(params, seed))
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
