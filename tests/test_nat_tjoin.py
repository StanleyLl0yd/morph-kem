from __future__ import annotations

import unittest

from morph_kem.nat_tjoin import (
    NAT1Error,
    NAT1Parameters,
    NAT1_PARAMETER_SETS,
    generate_nat1_instance,
    recover_nat1,
)


class NAT1TJoinTests(unittest.TestCase):
    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(NAT1Error):
            NAT1Parameters("bad", 35, 350, (1, 2)).validate()
        with self.assertRaises(NAT1Error):
            NAT1Parameters("bad", 36, 360, (2, 2)).validate()
        params = NAT1_PARAMETER_SETS["nat1-36"]
        with self.assertRaises(NAT1Error):
            generate_nat1_instance(params, b"short", 1)
        with self.assertRaises(NAT1Error):
            generate_nat1_instance(params, b"0" * 32, 7)

    def test_exact_tjoin_recovers_public_clean_object(self) -> None:
        params = NAT1_PARAMETER_SETS["nat1-36"]
        public, reference = generate_nat1_instance(params, b"NAT1 unit seed exact recovery v1", 4)
        recovery = recover_nat1(public, reference=reference)
        self.assertTrue(recovery.accepted)
        self.assertEqual(recovery.noise_weight, 4)
        self.assertEqual(recovery.matching_distance, recovery.recovered_noise_weight)
        self.assertEqual(recovery.syndrome_weight % 2, 0)
        self.assertGreater(recovery.matching_dp_states, 0)
        self.assertGreaterEqual(recovery.matching_pair_tests, recovery.syndrome_weight // 2)

    def test_decoder_needs_no_reference(self) -> None:
        params = NAT1_PARAMETER_SETS["nat1-54"]
        public, _ = generate_nat1_instance(params, b"NAT1 unit seed public only v1", 5)
        recovery = recover_nat1(public)
        self.assertTrue(recovery.accepted)
        self.assertIsNone(recovery.matches_planted_noise_after_public_success)
        self.assertIsNone(recovery.matches_hidden_vertex_after_public_success)

    def test_recovery_curve_across_weights(self) -> None:
        params = NAT1_PARAMETER_SETS["nat1-36"]
        seed = b"NAT1 unit seed curve v1................"
        for weight in params.noise_weights:
            public, reference = generate_nat1_instance(params, seed, weight)
            recovery = recover_nat1(public, reference=reference)
            self.assertTrue(recovery.accepted)
            self.assertLessEqual(recovery.recovered_noise_weight, weight)
            self.assertEqual(recovery.recovered_noise_weight, recovery.matching_distance)

    def test_break_is_stable_across_seeds(self) -> None:
        params = NAT1_PARAMETER_SETS["nat1-54"]
        for index in range(4):
            seed = (f"NAT1 deterministic seed {index:02d} v1").encode().ljust(32, b".")
            public, reference = generate_nat1_instance(params, seed, 4)
            recovery = recover_nat1(public, reference=reference)
            self.assertTrue(recovery.accepted)
            self.assertLessEqual(recovery.recovered_noise_weight, 4)


if __name__ == "__main__":
    unittest.main()
