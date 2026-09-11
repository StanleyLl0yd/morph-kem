from __future__ import annotations

import unittest

from morph_kem.hga_actions import (
    HGA0_DIHEDRAL_PARAMETER_SETS,
    HGA0_LINEAR_PARAMETER_SETS,
    DihedralActionParameters,
    HGAError,
    LinearActionParameters,
    apply_dihedral_action,
    apply_linear_action,
    generate_dihedral_action_instance,
    generate_linear_action_instance,
    recover_dihedral_action,
    recover_linear_action,
)


MASTER_SEED = bytes.fromhex("f0e1d2c3b4a5968778695a4b3c2d1e0f")


class HGAActionControlsTests(unittest.TestCase):
    def test_linear_control_is_exactly_publicly_recoverable(self) -> None:
        for name, params in HGA0_LINEAR_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public, reference = generate_linear_action_instance(params, MASTER_SEED)
                recovery = recover_linear_action(public, reference=reference)
                self.assertTrue(recovery.accepted)
                self.assertTrue(recovery.matches_reference_after_public_success)
                self.assertEqual(recovery.representation_rank, params.dimension)
                self.assertEqual(recovery.xor_operations, 1)
                self.assertEqual(len(recovery.recovered_word), params.secret_weight)
                self.assertEqual(
                    apply_linear_action(public.x, recovery.recovered_secret_mask, params.dimension),
                    public.y,
                )

    def test_linear_attack_needs_no_reference(self) -> None:
        public, _ = generate_linear_action_instance(
            HGA0_LINEAR_PARAMETER_SETS["hga0-linear-16"], MASTER_SEED
        )
        recovery = recover_linear_action(public)
        self.assertTrue(recovery.accepted)
        self.assertIsNone(recovery.matches_reference_after_public_success)

    def test_dihedral_control_has_canonical_public_recovery(self) -> None:
        for name, params in HGA0_DIHEDRAL_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public, reference = generate_dihedral_action_instance(params, MASTER_SEED)
                recovery = recover_dihedral_action(public, reference=reference)
                self.assertTrue(recovery.accepted)
                self.assertTrue(recovery.matches_reference_after_public_success)
                self.assertEqual(recovery.candidate_elements_tested, 2 * params.polygon_size)
                self.assertEqual(recovery.stabilizer_size, 1)
                self.assertEqual(len(recovery.matching_elements), 1)
                self.assertEqual(
                    apply_dihedral_action(public.labels, recovery.recovered_element),
                    public.transformed_labels,
                )

    def test_dihedral_break_is_stable_across_seeds(self) -> None:
        params = HGA0_DIHEDRAL_PARAMETER_SETS["hga0-dihedral-25"]
        for seed_index in range(8):
            with self.subTest(seed=seed_index):
                seed = bytes([seed_index + 1]) * 32
                public, reference = generate_dihedral_action_instance(params, seed)
                recovery = recover_dihedral_action(public, reference=reference)
                self.assertTrue(recovery.accepted)
                self.assertTrue(recovery.matches_reference_after_public_success)
                self.assertEqual(recovery.stabilizer_size, 1)

    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(HGAError):
            LinearActionParameters("small", 3, 1).validate()
        with self.assertRaises(HGAError):
            LinearActionParameters("weight", 8, 9).validate()
        with self.assertRaises(HGAError):
            DihedralActionParameters("small", 4).validate()
        with self.assertRaises(HGAError):
            generate_linear_action_instance(
                HGA0_LINEAR_PARAMETER_SETS["hga0-linear-8"], b"short"
            )
        with self.assertRaises(HGAError):
            generate_dihedral_action_instance(
                HGA0_DIHEDRAL_PARAMETER_SETS["hga0-dihedral-9"], b"short"
            )


if __name__ == "__main__":
    unittest.main()
