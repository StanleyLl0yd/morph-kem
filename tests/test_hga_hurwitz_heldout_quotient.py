from __future__ import annotations

import hashlib
import unittest

from morph_kem.hga_hurwitz import apply_hurwitz_generator
from morph_kem.hga_hurwitz_heldout_quotient import (
    HGA4EError,
    HGA4EParameters,
    HGA4E_PARAMETER_SETS,
    _QUOTIENT_GENERATORS,
    _quotient_hurwitz,
    _quotient_state,
    generate_hga4e_instance,
    recover_hga4e,
)


def seed_for(label: str) -> bytes:
    return hashlib.sha256(label.encode("ascii")).digest()


class HGA4EHeldoutQuotientTests(unittest.TestCase):
    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(HGA4EError):
            HGA4EParameters("bad", 5).validate()
        with self.assertRaises(HGA4EError):
            generate_hga4e_instance(HGA4E_PARAMETER_SETS["hga4e-D4"], b"short")

    def test_generation_is_deterministic(self) -> None:
        params = HGA4E_PARAMETER_SETS["hga4e-D4"]
        seed = seed_for("hga4e-deterministic")
        self.assertEqual(
            generate_hga4e_instance(params, seed),
            generate_hga4e_instance(params, seed),
        )

    def test_all_quotient_maps_commute_with_hurwitz_action(self) -> None:
        public, _ = generate_hga4e_instance(
            HGA4E_PARAMETER_SETS["hga4e-D4"], seed_for("hga4e-commutation")
        )
        for quotient_name in _QUOTIENT_GENERATORS:
            for generator in ("p", "P", "q", "Q"):
                exact = apply_hurwitz_generator(public.source, generator)
                self.assertEqual(
                    _quotient_state(exact, quotient_name),
                    _quotient_hurwitz(
                        _quotient_state(public.source, quotient_name), generator
                    ),
                )

    def test_training_conditioned_instance_recovers_exactly(self) -> None:
        for params in HGA4E_PARAMETER_SETS.values():
            public, reference = generate_hga4e_instance(
                params, seed_for("hga4e-" + params.name)
            )
            recovery = recover_hga4e(public, reference=reference)
            self.assertTrue(recovery.ordinary_endpoint_verified)
            self.assertEqual(recovery.ordinary_connector_length, params.exact_distance)
            self.assertEqual(len(reference.training_metrics), 2)
            self.assertTrue(all(item.actual_endpoint_verified for item in reference.training_metrics))
            self.assertTrue(all(item.endpoint_verified for item in recovery.heldout))
            self.assertTrue(
                all(item.recovered_connector_length == params.exact_distance for item in recovery.heldout)
            )

    def test_public_recovery_needs_no_reference(self) -> None:
        public, _ = generate_hga4e_instance(
            HGA4E_PARAMETER_SETS["hga4e-D4"], seed_for("hga4e-public")
        )
        recovery = recover_hga4e(public)
        self.assertTrue(recovery.ordinary_endpoint_verified)
        self.assertTrue(all(item.endpoint_verified for item in recovery.heldout))
        self.assertEqual(recovery.training_metrics, ())


if __name__ == "__main__":
    unittest.main()
