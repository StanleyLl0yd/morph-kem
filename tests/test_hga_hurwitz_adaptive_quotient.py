from __future__ import annotations

import hashlib
import unittest

from morph_kem.hga_hurwitz import _BRAID_GENERATORS, apply_hurwitz_generator
from morph_kem.hga_hurwitz_adaptive_quotient import (
    HGA4FError,
    HGA4FParameters,
    HGA4F_PARAMETER_SETS,
    _LIBRARY,
    generate_hga4f_instance,
    quotient_hurwitz,
    quotient_state,
    recover_hga4f,
)


def seed_for(label: str) -> bytes:
    return hashlib.sha256(label.encode("ascii")).digest()


class HGA4FAdaptiveQuotientTests(unittest.TestCase):
    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(HGA4FError):
            HGA4FParameters("bad", 5).validate()
        with self.assertRaises(HGA4FError):
            generate_hga4f_instance(HGA4F_PARAMETER_SETS["hga4f-D4"], b"short")

    def test_library_quotients_commute_with_hurwitz_action(self) -> None:
        public, _ = generate_hga4f_instance(
            HGA4F_PARAMETER_SETS["hga4f-D4"], seed_for("hga4f-commutation")
        )
        for rep in _LIBRARY:
            for generator in _BRAID_GENERATORS:
                exact_next = apply_hurwitz_generator(public.source, generator)
                self.assertEqual(
                    quotient_state(exact_next, rep.label),
                    quotient_hurwitz(quotient_state(public.source, rep.label), generator),
                )

    def test_generation_is_deterministic(self) -> None:
        params = HGA4F_PARAMETER_SETS["hga4f-D6"]
        seed = seed_for("hga4f-deterministic")
        self.assertEqual(
            generate_hga4f_instance(params, seed),
            generate_hga4f_instance(params, seed),
        )

    def test_public_recovery_needs_no_reference(self) -> None:
        params = HGA4F_PARAMETER_SETS["hga4f-D4"]
        public, _ = generate_hga4f_instance(params, seed_for("hga4f-public-only"))
        recovery = recover_hga4f(public)
        self.assertTrue(recovery.ordinary_endpoint_verified)
        self.assertEqual(recovery.library_size, len(_LIBRARY))
        self.assertTrue(all(metric.endpoint_verified for metric in recovery.singles))
        self.assertTrue(all(metric.endpoint_verified for metric in recovery.products))
        self.assertLessEqual(recovery.best_product_states, recovery.best_single_states)

    def test_declared_sweep_recovers_certified_distance(self) -> None:
        for params in HGA4F_PARAMETER_SETS.values():
            for index in range(2):
                public, reference = generate_hga4f_instance(
                    params, seed_for(f"hga4f-sweep-{params.name}-{index}")
                )
                recovery = recover_hga4f(public, reference=reference)
                self.assertEqual(recovery.ordinary_connector_length, params.exact_distance)
                self.assertTrue(recovery.ordinary_endpoint_verified)
                self.assertTrue(all(metric.endpoint_verified for metric in recovery.singles))
                self.assertTrue(all(metric.endpoint_verified for metric in recovery.products))
                self.assertLessEqual(recovery.best_product_states, recovery.best_single_states)
                self.assertEqual(len(recovery.selected_single_labels), 3)


if __name__ == "__main__":
    unittest.main()
