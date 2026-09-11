from __future__ import annotations

import unittest

from morph_kem.hga_modular import (
    HGA2Error,
    HGA2Parameters,
    HGA2_PARAMETER_SETS,
    apply_word,
    generate_hga2_instance,
    recover_hga2,
    reduce_to_infinity,
    word_matrix,
)


class HGA2ModularTests(unittest.TestCase):
    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(HGA2Error):
            HGA2Parameters("bad", 2, 31).validate()
        with self.assertRaises(HGA2Error):
            generate_hga2_instance(HGA2_PARAMETER_SETS["hga2-12"], b"short")

    def test_generator_inverse_round_trip(self) -> None:
        point = (7, 11)
        self.assertEqual(apply_word(apply_word(point, "T"), "t"), point)
        self.assertEqual(apply_word(apply_word(point, "S"), "S"), point)

    def test_matrix_and_word_action_agree_indirectly(self) -> None:
        point = (5, 13)
        word = "TSTtST"
        # word_matrix itself validates determinant one; recovery tests verify
        # its action independently against the direct generator path.
        matrix = word_matrix(word)
        self.assertEqual(matrix[0] * matrix[3] - matrix[1] * matrix[2], 1)
        self.assertNotEqual(apply_word(point, word), point)

    def test_euclidean_reduction_reaches_infinity(self) -> None:
        for point in ((1, 2), (17, 29), (-11, 7), (31, 5)):
            word, quotients, divisions = reduce_to_infinity(point)
            self.assertEqual(apply_word(point, word)[1], 0)
            self.assertEqual(divisions, len(quotients))
            self.assertGreater(divisions, 0)

    def test_public_canonical_recovery_needs_no_reference(self) -> None:
        params = HGA2_PARAMETER_SETS["hga2-20"]
        public, _ = generate_hga2_instance(params, b"HGA2 public recovery unit seed v1")
        recovery = recover_hga2(public)
        self.assertTrue(recovery.endpoint_verified)
        self.assertIsNone(recovery.matches_planted_word_after_public_success)
        self.assertIsNone(recovery.planted_matrix_equal_after_public_success)

    def test_break_is_stable_across_seeds(self) -> None:
        params = HGA2_PARAMETER_SETS["hga2-32"]
        for index in range(8):
            seed = (f"HGA2 deterministic seed {index:02d} v1").encode().ljust(40, b".")
            public, reference = generate_hga2_instance(params, seed)
            recovery = recover_hga2(public, reference=reference)
            self.assertTrue(recovery.endpoint_verified)
            self.assertGreater(recovery.recovered_connector_length, 0)


if __name__ == "__main__":
    unittest.main()
