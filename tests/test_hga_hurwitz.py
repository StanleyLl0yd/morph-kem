from __future__ import annotations

import unittest

from morph_kem.hga_hurwitz import (
    HGA4Error,
    HGA4Parameters,
    HGA4_PARAMETER_SETS,
    abelianization,
    apply_braid_word,
    apply_hurwitz_generator,
    generate_hga4_instance,
    inverse_braid_word,
    inverse_free_word,
    recover_hga4,
    reduce_free_word,
    state_product,
)


class HGA4HurwitzTests(unittest.TestCase):
    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(HGA4Error):
            HGA4Parameters("bad", 2).validate()
        with self.assertRaises(HGA4Error):
            generate_hga4_instance(HGA4_PARAMETER_SETS["hga4-L8"], b"short")

    def test_free_reduction_and_inverse(self) -> None:
        self.assertEqual(reduce_free_word("aAbB"), "")
        self.assertEqual(reduce_free_word("abBA"), "")
        word = reduce_free_word("abAbaB")
        self.assertEqual(reduce_free_word(word + inverse_free_word(word)), "")

    def test_hurwitz_generators_are_exact_inverses_and_preserve_product(self) -> None:
        state = ("abA", "ba", "aBB")
        for generator, inverse in (("p", "P"), ("P", "p"), ("q", "Q"), ("Q", "q")):
            moved = apply_hurwitz_generator(state, generator)
            self.assertEqual(apply_hurwitz_generator(moved, inverse), state)
            self.assertEqual(state_product(moved), state_product(state))

    def test_abelianization_only_permutes_strands(self) -> None:
        state = ("a", "b", "ab")
        moved = apply_braid_word(state, "pqPq")
        source_vectors = sorted(abelianization(word) for word in state)
        target_vectors = sorted(abelianization(word) for word in moved)
        self.assertEqual(source_vectors, target_vectors)

    def test_public_mitm_needs_no_reference(self) -> None:
        params = HGA4_PARAMETER_SETS["hga4-L12"]
        public, _ = generate_hga4_instance(params, b"HGA4 public MITM unit seed v1")
        recovery = recover_hga4(public)
        self.assertTrue(recovery.endpoint_verified)
        self.assertTrue(recovery.invariant_product_verified)
        self.assertLessEqual(recovery.recovered_connector_length, params.planted_word_length)
        self.assertIsNone(recovery.matches_planted_word_after_public_success)
        self.assertIsNone(recovery.quotient_matches_planted)

    def test_bounded_break_is_stable_across_seeds(self) -> None:
        params = HGA4_PARAMETER_SETS["hga4-L16"]
        for index in range(4):
            seed = (f"HGA4 deterministic seed {index:02d} v1").encode().ljust(40, b".")
            public, reference = generate_hga4_instance(params, seed)
            recovery = recover_hga4(public, reference=reference)
            self.assertTrue(recovery.endpoint_verified)
            self.assertTrue(recovery.quotient_matches_planted)
            self.assertLessEqual(recovery.recovered_connector_length, 16)
            self.assertGreater(recovery.forward_states, 0)
            self.assertGreater(recovery.backward_states, 0)
            self.assertGreater(recovery.meet_states, 0)
            inverse = inverse_braid_word(reference.planted_word)
            self.assertEqual(apply_braid_word(public.target, inverse), public.source)


if __name__ == "__main__":
    unittest.main()
