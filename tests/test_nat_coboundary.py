from __future__ import annotations

import unittest

from morph_kem.nat_coboundary import (
    NAT0_PARAMETER_SETS,
    NATError,
    NATParameters,
    generate_nat0_repeated_instance,
    generate_nat0_single_instance,
    recover_nat0_repeated,
    recover_nat0_single,
)


MASTER_SEED = bytes.fromhex("0011aabb2233ccdd4455eeff66778899")


class NATCoboundaryTests(unittest.TestCase):
    def test_single_edge_noise_is_removed_by_triangle_syndrome(self) -> None:
        for name, params in NAT0_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public, reference = generate_nat0_single_instance(params, MASTER_SEED)
                recovery = recover_nat0_single(public, reference=reference)
                self.assertEqual(len(recovery.violated_triangles), 2)
                self.assertTrue(recovery.accepted)
                self.assertTrue(recovery.matches_reference_after_public_success)
                self.assertEqual(recovery.recovered_noise_edge, reference.noise_edge_index)

    def test_single_edge_attack_needs_no_reference(self) -> None:
        public, _ = generate_nat0_single_instance(
            NAT0_PARAMETER_SETS["nat0-6x6"], MASTER_SEED
        )
        recovery = recover_nat0_single(public)
        self.assertTrue(recovery.accepted)
        self.assertIsNone(recovery.matches_reference_after_public_success)

    def test_repeated_noise_is_removed_by_public_majority(self) -> None:
        for name, params in NAT0_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public, reference = generate_nat0_repeated_instance(params, MASTER_SEED)
                recovery = recover_nat0_repeated(public, reference=reference)
                self.assertTrue(recovery.accepted)
                self.assertTrue(recovery.matches_reference_after_public_success)
                self.assertEqual(len(recovery.sample_distances), params.repeated_samples)
                self.assertEqual(
                    recovery.sample_distances,
                    (params.repeated_noise_weight,) * params.repeated_samples,
                )
                self.assertEqual(
                    recovery.majority_edge_votes,
                    3 * params.rows * params.cols * params.repeated_samples,
                )

    def test_both_breaks_are_stable_across_seeds(self) -> None:
        params = NAT0_PARAMETER_SETS["nat0-8x8"]
        for seed_index in range(8):
            with self.subTest(seed=seed_index):
                seed = bytes([seed_index + 1]) * 32
                single_public, single_reference = generate_nat0_single_instance(params, seed)
                single = recover_nat0_single(single_public, reference=single_reference)
                repeated_public, repeated_reference = generate_nat0_repeated_instance(params, seed)
                repeated = recover_nat0_repeated(
                    repeated_public, reference=repeated_reference
                )
                self.assertTrue(single.accepted)
                self.assertTrue(single.matches_reference_after_public_success)
                self.assertTrue(repeated.accepted)
                self.assertTrue(repeated.matches_reference_after_public_success)

    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(NATError):
            NATParameters("small", 2, 4, 7, 1).validate()
        with self.assertRaises(NATError):
            NATParameters("even", 4, 4, 6, 1).validate()
        with self.assertRaises(NATError):
            generate_nat0_single_instance(NAT0_PARAMETER_SETS["nat0-4x4"], b"short")
        with self.assertRaises(NATError):
            generate_nat0_repeated_instance(NAT0_PARAMETER_SETS["nat0-4x4"], b"short")


if __name__ == "__main__":
    unittest.main()
