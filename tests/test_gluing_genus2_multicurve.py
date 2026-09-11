from __future__ import annotations

import hashlib
import unittest

from morph_kem.gluing import GluingExperimentError
from morph_kem.gluing_genus2_multicurve import (
    G20_PARAMETER_SETS,
    GenusTwoMulticurveParameters,
    GenusTwoMulticurvePublicInstance,
    generate_genus2_multicurve_instance,
    recover_genus2_multicurve,
    validate_genus2_multicurve_witness,
)


FIXED_SEED = bytes.fromhex("47" * 32)


class GenusTwoMulticurveTests(unittest.TestCase):
    def test_constructive_carrier_and_public_recovery(self) -> None:
        expected = {
            "g20-4x4": (29, 93, 62),
            "g20-6x6": (69, 213, 142),
            "g20-6x9": (105, 321, 214),
        }
        for name, params in G20_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public, reference = generate_genus2_multicurve_instance(params, FIXED_SEED)
                recovery = recover_genus2_multicurve(
                    public,
                    reference=reference,
                    successful_flips=params.successful_flips,
                )
                self.assertEqual(
                    (recovery.vertices, recovery.edges, recovery.triangles), expected[name]
                )
                self.assertEqual(recovery.euler_characteristic, -2)
                self.assertEqual(
                    (recovery.min_triangles_per_edge, recovery.max_triangles_per_edge),
                    (2, 2),
                )
                self.assertEqual(recovery.h1_dimension, 4)
                self.assertGreater(recovery.alpha_weight, 0)
                self.assertGreater(recovery.beta_weight, 0)
                self.assertEqual(recovery.four_sheet_states, 4 * recovery.vertices)
                self.assertGreater(recovery.alpha_candidates, 0)
                self.assertGreater(recovery.beta_stage_calls, 0)
                self.assertEqual(recovery.selected_alpha_signature, (1, 0))
                self.assertEqual(recovery.selected_beta_signature, (0, 1))
                self.assertEqual(recovery.selected_shared_vertices, 0)
                self.assertLessEqual(
                    recovery.selected_alpha_length, recovery.max_alpha_length
                )
                self.assertLessEqual(
                    recovery.selected_beta_length, recovery.max_beta_length
                )
                self.assertTrue(recovery.selected_accepted)
                self.assertTrue(
                    validate_genus2_multicurve_witness(public, reference.witness).valid
                )

    def test_attack_does_not_need_reference(self) -> None:
        params = G20_PARAMETER_SETS["g20-4x4"]
        public, _ = generate_genus2_multicurve_instance(params, FIXED_SEED)
        recovery = recover_genus2_multicurve(
            public, reference=None, successful_flips=params.successful_flips
        )
        self.assertTrue(recovery.selected_accepted)
        self.assertIsNone(recovery.selected_matches_reference)
        self.assertEqual(recovery.selected_shared_vertices, 0)

    def test_public_bounds_are_enforced(self) -> None:
        params = G20_PARAMETER_SETS["g20-4x4"]
        public, reference = generate_genus2_multicurve_instance(params, FIXED_SEED)
        tighter = GenusTwoMulticurvePublicInstance(
            public.name,
            public.target,
            public.alpha,
            public.beta,
            max(0, len(reference.witness.alpha_cycle) - 1),
            public.max_beta_length,
        )
        self.assertFalse(
            validate_genus2_multicurve_witness(tighter, reference.witness).valid
        )

    def test_multi_seed_break(self) -> None:
        for name, params in G20_PARAMETER_SETS.items():
            for seed_index in range(2):
                seed = hashlib.sha256(
                    b"MORPH-KEM G20 unit sweep\x00"
                    + name.encode("ascii")
                    + seed_index.to_bytes(4, "big")
                ).digest()
                with self.subTest(name=name, seed=seed_index):
                    public, reference = generate_genus2_multicurve_instance(params, seed)
                    recovery = recover_genus2_multicurve(
                        public,
                        reference=reference,
                        successful_flips=params.successful_flips,
                    )
                    self.assertTrue(recovery.selected_accepted)
                    self.assertEqual(recovery.selected_alpha_signature, (1, 0))
                    self.assertEqual(recovery.selected_beta_signature, (0, 1))
                    self.assertEqual(recovery.selected_shared_vertices, 0)

    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(GluingExperimentError):
            GenusTwoMulticurveParameters("bad", 3, 4, 10).validate()
        with self.assertRaises(GluingExperimentError):
            GenusTwoMulticurveParameters("bad", 4, 4, 10000).validate()
        with self.assertRaises(GluingExperimentError):
            generate_genus2_multicurve_instance(
                G20_PARAMETER_SETS["g20-4x4"], b"short"
            )


if __name__ == "__main__":
    unittest.main()
