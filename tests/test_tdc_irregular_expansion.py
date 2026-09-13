from __future__ import annotations

import hashlib
import unittest

from morph_kem.tdc_irregular_expansion import (
    TDC2DError,
    TDC2DParameters,
    TDC2D_PARAMETER_SETS,
    generate_tdc2d_instance,
    recover_tdc2d,
)


def seed_for(label: str) -> bytes:
    return hashlib.sha256(label.encode("ascii")).digest()


class TDC2DIrregularExpansionTests(unittest.TestCase):
    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(TDC2DError):
            TDC2DParameters("bad", "missing").validate()
        with self.assertRaises(TDC2DError):
            generate_tdc2d_instance(TDC2D_PARAMETER_SETS["tdc2d-n8"], b"short")

    def test_expansion_preserves_column_weight_without_duplicates(self) -> None:
        for params in TDC2D_PARAMETER_SETS.values():
            instance = generate_tdc2d_instance(params, seed_for(params.name + "-shape"))
            for expansion in (instance.topology, instance.matched_random):
                self.assertTrue(all(column.bit_count() == 3 for column in expansion.code.columns))
                self.assertEqual(len(expansion.code.columns), len(set(expansion.code.columns)))
                self.assertTrue(set(expansion.row_multiplicities).issubset({2, 3}))
                self.assertEqual(len(expansion.column_fibers) * 2, len(expansion.code.columns))

    def test_public_attack_metrics_are_available_without_external_mapping(self) -> None:
        params = TDC2D_PARAMETER_SETS["tdc2d-n8"]
        recovery = recover_tdc2d(generate_tdc2d_instance(params, seed_for("tdc2d-public")))
        self.assertGreater(recovery.topology.color_rounds, 0)
        self.assertEqual(recovery.topology.column_weight_histogram, ((3, recovery.topology.columns),))
        self.assertGreater(recovery.topology.total_row_fibers, 0)
        self.assertGreater(recovery.topology.total_column_fibers, 0)

    def test_generation_and_metrics_are_deterministic(self) -> None:
        params = TDC2D_PARAMETER_SETS["tdc2d-n9"]
        seed = seed_for("tdc2d-deterministic")
        first = generate_tdc2d_instance(params, seed)
        second = generate_tdc2d_instance(params, seed)
        self.assertEqual(first, second)
        self.assertEqual(recover_tdc2d(first), recover_tdc2d(second))

    def test_declared_sets_run_on_small_sweep(self) -> None:
        for params in TDC2D_PARAMETER_SETS.values():
            for index in range(2):
                recovery = recover_tdc2d(
                    generate_tdc2d_instance(params, seed_for(f"{params.name}-{index}"))
                )
                self.assertEqual(recovery.topology.column_weight_histogram[0][0], 3)
                self.assertEqual(recovery.matched_random.column_weight_histogram[0][0], 3)


if __name__ == "__main__":
    unittest.main()
