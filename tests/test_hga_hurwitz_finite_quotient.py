from __future__ import annotations

import hashlib
import unittest

from morph_kem.hga_hurwitz import apply_hurwitz_generator
from morph_kem.hga_hurwitz_finite_quotient import (
    HGA4DError,
    HGA4DParameters,
    HGA4D_PARAMETER_SETS,
    _quotient_hurwitz,
    _quotient_state,
    generate_hga4d_instance,
    recover_hga4d,
)


def seed_for(label: str) -> bytes:
    return hashlib.sha256(label.encode("ascii")).digest()


class HGA4DFiniteQuotientTests(unittest.TestCase):
    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(HGA4DError):
            HGA4DParameters("bad", 5).validate()
        with self.assertRaises(HGA4DError):
            generate_hga4d_instance(HGA4D_PARAMETER_SETS["hga4d-D4"], b"short")

    def test_generation_is_deterministic(self) -> None:
        params = HGA4D_PARAMETER_SETS["hga4d-D4"]
        seed = seed_for("hga4d-deterministic")
        self.assertEqual(
            generate_hga4d_instance(params, seed),
            generate_hga4d_instance(params, seed),
        )

    def test_quotient_maps_commute_with_hurwitz_action(self) -> None:
        params = HGA4D_PARAMETER_SETS["hga4d-D4"]
        public, _ = generate_hga4d_instance(params, seed_for("hga4d-commute"))
        for quotient in ("S3", "A5"):
            for generator in ("p", "P", "q", "Q"):
                exact_next = apply_hurwitz_generator(public.source, generator)
                quotient_next = _quotient_hurwitz(
                    _quotient_state(public.source, quotient), generator
                )
                self.assertEqual(_quotient_state(exact_next, quotient), quotient_next)

    def test_public_recovery_needs_no_reference(self) -> None:
        params = HGA4D_PARAMETER_SETS["hga4d-D4"]
        public, _ = generate_hga4d_instance(params, seed_for("hga4d-public"))
        recovery = recover_hga4d(public)
        self.assertTrue(recovery.ordinary_mitm_endpoint_verified)
        for result in recovery.quotients:
            self.assertTrue(result.endpoint_verified)
            self.assertEqual(result.recovered_connector_length, params.exact_distance)
            self.assertLessEqual(result.quotient_shortest_distance or 0, params.exact_distance)

    def test_declared_sweep_preserves_exact_endpoint(self) -> None:
        for params in HGA4D_PARAMETER_SETS.values():
            for index in range(3):
                public, reference = generate_hga4d_instance(
                    params, seed_for(f"{params.name}-{index}")
                )
                recovery = recover_hga4d(public, reference=reference)
                self.assertEqual(recovery.ordinary_mitm_connector_length, params.exact_distance)
                self.assertTrue(recovery.ordinary_mitm_endpoint_verified)
                for result in recovery.quotients:
                    self.assertTrue(result.endpoint_verified)
                    self.assertEqual(result.recovered_connector_length, params.exact_distance)
                    self.assertLessEqual(
                        result.exact_states_kept,
                        reference.shell.generator_ball_states,
                    )


if __name__ == "__main__":
    unittest.main()
