from __future__ import annotations

import hashlib
import unittest

from morph_kem.hga_hurwitz import apply_braid_word
from morph_kem.hga_hurwitz_distance_shell import (
    HGA4CError,
    HGA4CParameters,
    HGA4C_PARAMETER_SETS,
    generate_hga4c_instance,
    recover_hga4c,
)


def seed_for(label: str) -> bytes:
    return hashlib.sha256(label.encode("ascii")).digest()


class HGA4CDistanceShellTests(unittest.TestCase):
    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(HGA4CError):
            HGA4CParameters("bad", 5).validate()
        with self.assertRaises(HGA4CError):
            generate_hga4c_instance(HGA4C_PARAMETER_SETS["hga4c-D4"], b"short")

    def test_selected_target_has_exact_certificate_length(self) -> None:
        params = HGA4C_PARAMETER_SETS["hga4c-D8"]
        public, reference = generate_hga4c_instance(params, seed_for("hga4c-shell"))
        self.assertEqual(len(reference.selected_shortest_word), params.exact_distance)
        self.assertEqual(
            apply_braid_word(public.source, reference.selected_shortest_word),
            public.target,
        )
        self.assertGreater(reference.generator_shell_states, 0)
        self.assertGreaterEqual(reference.generator_ball_states, reference.generator_shell_states)

    def test_public_recovery_needs_no_reference(self) -> None:
        params = HGA4C_PARAMETER_SETS["hga4c-D6"]
        public, _ = generate_hga4c_instance(params, seed_for("hga4c-public"))
        recovery = recover_hga4c(public)
        self.assertTrue(recovery.endpoint_verified)
        self.assertEqual(recovery.recovered_connector_length, params.exact_distance)
        self.assertIsNone(recovery.matches_generator_certificate_after_public_success)

    def test_recovery_preserves_exact_distance_across_declared_sets(self) -> None:
        for params in HGA4C_PARAMETER_SETS.values():
            for index in range(4):
                public, reference = generate_hga4c_instance(
                    params, seed_for(f"{params.name}-seed-{index}")
                )
                recovery = recover_hga4c(public, reference=reference)
                self.assertTrue(recovery.endpoint_verified)
                self.assertEqual(recovery.recovered_connector_length, params.exact_distance)
                self.assertGreater(recovery.generator_ball_states, 0)
                self.assertGreater(recovery.generator_shell_states, 0)

    def test_generation_is_deterministic(self) -> None:
        params = HGA4C_PARAMETER_SETS["hga4c-D6"]
        seed = seed_for("hga4c-deterministic")
        self.assertEqual(
            generate_hga4c_instance(params, seed),
            generate_hga4c_instance(params, seed),
        )


if __name__ == "__main__":
    unittest.main()
