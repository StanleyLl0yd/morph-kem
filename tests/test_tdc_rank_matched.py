from __future__ import annotations

import hashlib
import unittest

from morph_kem.tdc_rank_matched import (
    TDC2FError,
    TDC2FParameters,
    TDC2F_PARAMETER_SETS,
    generate_tdc2f_instance,
    recover_tdc2f,
)


def seed_for(label: str) -> bytes:
    return hashlib.sha256(label.encode("ascii")).digest()


class TDC2FRankMatchedTests(unittest.TestCase):
    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(TDC2FError):
            TDC2FParameters("bad", "tdc2b-n8", row_scramble_rounds=0).validate()
        with self.assertRaises(TDC2FError):
            TDC2FParameters("bad", "tdc2b-n8", column_mixing_rounds=5).validate()
        with self.assertRaises(TDC2FError):
            generate_tdc2f_instance(TDC2F_PARAMETER_SETS["tdc2f-n8"], b"short")

    def test_generation_is_deterministic(self) -> None:
        params = TDC2F_PARAMETER_SETS["tdc2f-n8"]
        seed = seed_for("tdc2f-deterministic")
        self.assertEqual(
            generate_tdc2f_instance(params, seed),
            generate_tdc2f_instance(params, seed),
        )

    def test_public_rank_dimension_are_matched_by_construction(self) -> None:
        for params in TDC2F_PARAMETER_SETS.values():
            public = generate_tdc2f_instance(params, seed_for(params.name))
            recovery = recover_tdc2f(public)
            self.assertTrue(recovery.rank_profile_equal)
            self.assertTrue(recovery.dimension_profile_equal)
            self.assertEqual(recovery.topology.rank, public.target_rank)
            self.assertEqual(recovery.matched_random.rank, public.target_rank)
            self.assertEqual(recovery.topology.rows, public.target_rank)
            self.assertEqual(recovery.matched_random.rows, public.target_rank)

    def test_public_columns_are_nonzero_and_unique(self) -> None:
        params = TDC2F_PARAMETER_SETS["tdc2f-n9"]
        instance = generate_tdc2f_instance(params, seed_for("tdc2f-public-columns"))
        for item in (instance.topology, instance.matched_random):
            self.assertFalse(any(column == 0 for column in item.code.columns))
            self.assertEqual(len(item.code.columns), len(set(item.code.columns)))
            self.assertEqual(
                len(item.column_mixing_reference.operations),
                params.column_mixing_rounds * len(item.code.columns),
            )
            self.assertEqual(
                item.row_scramble_operations,
                params.row_scramble_rounds * item.code.row_count,
            )

    def test_declared_small_sweep_runs(self) -> None:
        for params in TDC2F_PARAMETER_SETS.values():
            for index in range(2):
                instance = generate_tdc2f_instance(
                    params, seed_for(f"tdc2f-sweep-{params.name}-{index}")
                )
                recovery = recover_tdc2f(instance)
                self.assertTrue(recovery.rank_profile_equal)
                self.assertTrue(recovery.dimension_profile_equal)


if __name__ == "__main__":
    unittest.main()
