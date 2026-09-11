from __future__ import annotations

import unittest

from morph_kem.hga_intertwiner import (
    HGA3Error,
    HGA3Parameters,
    HGA3_PARAMETER_SETS,
    generate_hga3_instance,
    recover_hga3,
)


class HGA3IntertwinerTests(unittest.TestCase):
    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(HGA3Error):
            HGA3Parameters("bad", 3, 3, 3).validate()
        with self.assertRaises(HGA3Error):
            generate_hga3_instance(HGA3_PARAMETER_SETS["hga3-p5-n3"], b"short")

    def test_public_intertwiner_recovers_endpoint(self) -> None:
        params = HGA3_PARAMETER_SETS["hga3-p7-n4"]
        public, reference = generate_hga3_instance(params, b"HGA3 endpoint unit seed v1")
        recovery = recover_hga3(public, reference=reference)
        self.assertTrue(recovery.exact_endpoint_verified)
        self.assertGreater(recovery.system_rank, 0)
        self.assertGreater(recovery.system_nullity, 0)
        self.assertEqual(recovery.system_rank + recovery.system_nullity, params.dimension**2)
        self.assertEqual(recovery.recovered_rank, params.dimension)
        self.assertNotEqual(recovery.recovered_determinant, 0)
        self.assertEqual(recovery.source_trace_fingerprint, recovery.target_trace_fingerprint)

    def test_attack_needs_no_reference(self) -> None:
        params = HGA3_PARAMETER_SETS["hga3-p5-n3"]
        public, _ = generate_hga3_instance(params, b"HGA3 public only unit seed v1")
        recovery = recover_hga3(public)
        self.assertTrue(recovery.exact_endpoint_verified)
        self.assertIsNone(recovery.scalar_equivalent_to_planted_after_public_success)
        self.assertIsNone(recovery.exactly_matches_planted_after_public_success)

    def test_break_is_stable_across_seeds(self) -> None:
        params = HGA3_PARAMETER_SETS["hga3-p11-n5"]
        for index in range(8):
            seed = (f"HGA3 deterministic seed {index:02d} v1").encode().ljust(40, b".")
            public, reference = generate_hga3_instance(params, seed)
            recovery = recover_hga3(public, reference=reference)
            self.assertTrue(recovery.exact_endpoint_verified)
            self.assertLessEqual(recovery.combination_candidates_tested, 100_000)


if __name__ == "__main__":
    unittest.main()
