from __future__ import annotations

import hashlib
import unittest

from morph_kem.tdc_random_overlay import (
    TDC2GError,
    TDC2GParameters,
    TDC2G_PARAMETER_SETS,
    generate_tdc2g_instance,
    recover_tdc2g,
)


def digest(label: str) -> bytes:
    return hashlib.sha256(label.encode("ascii")).digest()


class TDC2GRandomOverlayTests(unittest.TestCase):
    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(TDC2GError):
            TDC2GParameters("bad", "missing").validate()
        with self.assertRaises(TDC2GError):
            generate_tdc2g_instance(TDC2G_PARAMETER_SETS["tdc2g-n8"], b"short")

    def test_overlay_increases_both_ranks_equally(self) -> None:
        params = TDC2G_PARAMETER_SETS["tdc2g-n10"]
        instance = generate_tdc2g_instance(params, digest("TDC2g rank unit seed v1"))
        recovery = recover_tdc2g(instance)
        self.assertEqual(recovery.extra_rows, params.extra_rows)
        self.assertEqual(recovery.final_rank, recovery.base_rank + params.extra_rows)
        self.assertTrue(recovery.rank_profile_equal)
        self.assertTrue(recovery.dimension_profile_equal)
        self.assertEqual(recovery.topology.rank, recovery.final_rank)
        self.assertEqual(recovery.matched_random.rank, recovery.final_rank)

    def test_overlay_is_deterministic(self) -> None:
        params = TDC2G_PARAMETER_SETS["tdc2g-n9"]
        seed = digest("TDC2g deterministic overlay unit v1")
        first = generate_tdc2g_instance(params, seed)
        second = generate_tdc2g_instance(params, seed)
        self.assertEqual(first.overlay_rows, second.overlay_rows)
        self.assertEqual(first.topology.columns, second.topology.columns)
        self.assertEqual(first.matched_random.columns, second.matched_random.columns)

    def test_small_declared_sweep_preserves_profiles(self) -> None:
        for params in TDC2G_PARAMETER_SETS.values():
            for index in range(2):
                instance = generate_tdc2g_instance(
                    params,
                    digest(f"TDC2g unit {params.name} seed {index} v1"),
                )
                recovery = recover_tdc2g(instance)
                self.assertTrue(recovery.rank_profile_equal)
                self.assertTrue(recovery.dimension_profile_equal)
                self.assertGreaterEqual(recovery.overlay_attempts, params.extra_rows)


if __name__ == "__main__":
    unittest.main()
