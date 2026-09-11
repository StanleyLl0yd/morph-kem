from __future__ import annotations

import hashlib
import unittest

from morph_kem.gluing import GluingExperimentError
from morph_kem.gluing_length_bounded_pair import (
    G18_PARAMETER_SETS,
    LengthBoundedPairParameters,
    LengthBoundedPairPublicInstance,
    generate_length_bounded_pair_instance,
    recover_length_bounded_pair,
    validate_length_bounded_pair_witness,
)


FIXED_SEED = bytes.fromhex("a7450102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e")


class LengthBoundedPairTests(unittest.TestCase):
    def test_a045_public_shortest_cycle_connector_break(self) -> None:
        expected = {
            "g18-6x6": (36, 108, 72),
            "g18-6x9": (54, 162, 108),
            "g18-8x9": (72, 216, 144),
        }
        for name, params in G18_PARAMETER_SETS.items():
            with self.subTest(params=name):
                public, reference = generate_length_bounded_pair_instance(params, FIXED_SEED)
                reference_validation = validate_length_bounded_pair_witness(public, reference.witness)
                self.assertTrue(reference_validation.valid)
                recovery = recover_length_bounded_pair(
                    public,
                    reference=reference,
                    successful_flips=params.successful_flips,
                )
                self.assertEqual(
                    (recovery.vertices, recovery.edges, recovery.triangles), expected[name]
                )
                self.assertEqual(recovery.euler_characteristic, 0)
                self.assertEqual(
                    (recovery.min_triangles_per_edge, recovery.max_triangles_per_edge),
                    (2, 2),
                )
                self.assertEqual(recovery.h1_dimension, 2)
                self.assertEqual(recovery.selected_crossing_count, 1)
                self.assertTrue(recovery.selected_accepted)
                self.assertLessEqual(recovery.selected_primal_length, public.max_primal_length)
                self.assertLessEqual(recovery.selected_dual_length, public.max_dual_length)
                self.assertGreater(recovery.cover_roots_attempted, 0)
                self.assertGreater(recovery.cover_edge_scans, 0)
                self.assertGreater(recovery.dual_connector_calls, 0)
                self.assertGreater(recovery.distinct_primal_candidates, 0)
                self.assertGreater(recovery.primal_candidates_within_bound, 0)

    def test_attack_needs_no_reference(self) -> None:
        params = G18_PARAMETER_SETS["g18-6x6"]
        public, _ = generate_length_bounded_pair_instance(params, FIXED_SEED)
        recovery = recover_length_bounded_pair(
            public, reference=None, successful_flips=params.successful_flips
        )
        self.assertTrue(recovery.selected_accepted)
        self.assertIsNone(recovery.selected_matches_reference)
        self.assertEqual(recovery.selected_crossing_count, 1)

    def test_public_bounds_are_enforced(self) -> None:
        params = G18_PARAMETER_SETS["g18-6x6"]
        public, reference = generate_length_bounded_pair_instance(params, FIXED_SEED)
        too_short = LengthBoundedPairPublicInstance(
            name=public.name,
            target=public.target,
            max_primal_length=max(0, len(reference.witness.primal_cycle) - 1),
            max_dual_length=public.max_dual_length,
        )
        self.assertFalse(
            validate_length_bounded_pair_witness(too_short, reference.witness).valid
        )

    def test_multi_seed_public_break(self) -> None:
        for name, params in G18_PARAMETER_SETS.items():
            for seed_index in range(4):
                seed = hashlib.sha256(
                    b"MORPH-KEM G18 unit sweep\x00"
                    + name.encode("ascii")
                    + seed_index.to_bytes(4, "big")
                ).digest()
                with self.subTest(params=name, seed=seed_index):
                    public, reference = generate_length_bounded_pair_instance(params, seed)
                    recovery = recover_length_bounded_pair(
                        public,
                        reference=reference,
                        successful_flips=params.successful_flips,
                    )
                    self.assertTrue(recovery.selected_accepted)
                    self.assertEqual(recovery.selected_crossing_count, 1)
                    self.assertLessEqual(recovery.selected_primal_length, public.max_primal_length)
                    self.assertLessEqual(recovery.selected_dual_length, public.max_dual_length)

    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(GluingExperimentError):
            LengthBoundedPairParameters("bad", 3, 6, 1).validate()
        with self.assertRaises(GluingExperimentError):
            LengthBoundedPairParameters("bad", 6, 6, 1000).validate()
        with self.assertRaises(GluingExperimentError):
            generate_length_bounded_pair_instance(
                G18_PARAMETER_SETS["g18-6x6"], b"short"
            )


if __name__ == "__main__":
    unittest.main()
