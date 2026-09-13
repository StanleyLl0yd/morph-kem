from __future__ import annotations

import hashlib
import unittest

from morph_kem.hga_hurwitz import apply_braid_word, generate_hga4_instance
from morph_kem.hga_hurwitz_self_avoiding import (
    HGA4BDeadEnd,
    HGA4BError,
    HGA4BParameters,
    HGA4B_PARAMETER_SETS,
    _source_parameters,
    generate_hga4b_instance,
    recover_hga4b,
)


def seed_for(label: str) -> bytes:
    return hashlib.sha256(label.encode("ascii")).digest()


class HGA4BSelfAvoidingTests(unittest.TestCase):
    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(HGA4BError):
            HGA4BParameters("too-short", 3).validate()
        with self.assertRaises(HGA4BError):
            HGA4BParameters("too-long", 21).validate()
        with self.assertRaises(HGA4BError):
            generate_hga4b_instance(HGA4B_PARAMETER_SETS["hga4b-L8"], b"short")

    def test_generated_path_is_exact_and_self_avoiding(self) -> None:
        params = HGA4B_PARAMETER_SETS["hga4b-L16"]
        public, reference = generate_hga4b_instance(params, seed_for("hga4b-path"))
        self.assertEqual(len(reference.planted_word), params.planted_word_length)
        self.assertEqual(len(reference.path_states), params.planted_word_length + 1)
        self.assertEqual(reference.distinct_path_states, len(reference.path_states))
        self.assertEqual(reference.dead_end_count, 0)
        self.assertEqual(apply_braid_word(public.source, reference.planted_word), public.target)
        self.assertEqual(reference.path_states[0], public.source)
        self.assertEqual(reference.path_states[-1], public.target)

    def test_generator_is_deterministic_and_has_no_hidden_retry(self) -> None:
        params = HGA4B_PARAMETER_SETS["hga4b-L12"]
        seed = seed_for("hga4b-deterministic")
        first = generate_hga4b_instance(params, seed)
        second = generate_hga4b_instance(params, seed)
        self.assertEqual(first, second)
        self.assertEqual(first[1].dead_end_count, 0)

    def test_official_sweep_dead_end_is_explicit(self) -> None:
        params = HGA4B_PARAMETER_SETS["hga4b-L12"]
        seed = seed_for("MORPH-KEM HGA4b sweep hga4b-L12 seed 7 v1")
        with self.assertRaises(HGA4BDeadEnd) as context:
            generate_hga4b_instance(params, seed)
        self.assertEqual(context.exception.step, 5)
        self.assertEqual(len(context.exception.partial_word), 5)
        self.assertEqual(len(context.exception.path_states), 6)
        self.assertEqual(len(set(context.exception.path_states)), 6)

    def test_paired_control_preserves_source_state(self) -> None:
        params = HGA4B_PARAMETER_SETS["hga4b-L12"]
        seed = seed_for("hga4b-paired-source")
        public, _ = generate_hga4b_instance(params, seed)
        old_public, _ = generate_hga4_instance(_source_parameters(params), seed)
        self.assertEqual(public.source, old_public.source)
        self.assertEqual(public.public_word_bound, old_public.public_word_bound)

    def test_public_mitm_needs_no_reference(self) -> None:
        params = HGA4B_PARAMETER_SETS["hga4b-L8"]
        public, _ = generate_hga4b_instance(params, seed_for("hga4b-public-attack"))
        recovery = recover_hga4b(public)
        self.assertTrue(recovery.endpoint_verified)
        self.assertLessEqual(recovery.recovered_connector_length, params.planted_word_length)
        self.assertIsNone(recovery.matches_planted_word_after_public_success)
        self.assertIsNone(recovery.quotient_matches_planted)

    def test_generation_stays_self_avoiding_across_successful_declared_samples(self) -> None:
        for params in HGA4B_PARAMETER_SETS.values():
            for index in range(8):
                _, reference = generate_hga4b_instance(
                    params, seed_for(f"{params.name}-seed-{index}")
                )
                self.assertEqual(reference.distinct_path_states, params.planted_word_length + 1)
                self.assertEqual(reference.dead_end_count, 0)


if __name__ == "__main__":
    unittest.main()
