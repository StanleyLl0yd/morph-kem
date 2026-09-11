from __future__ import annotations

import hashlib
import unittest

from morph_kem.gluing import GluingExperimentError
from morph_kem.gluing_disjoint_cohomology_pair import (
    G19_PARAMETER_SETS,
    DisjointCohomologyPairParameters,
    DisjointCohomologyPairPublicInstance,
    generate_disjoint_cohomology_pair_instance,
    recover_disjoint_cohomology_pair,
    validate_disjoint_cohomology_pair_witness,
)


FIXED_SEED = bytes.fromhex(
    "a7460102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e"
)


class DisjointCohomologyPairTests(unittest.TestCase):
    def test_a046_recovers_bounded_disjoint_pair(self) -> None:
        expected = {
            "g19-6x6": (36, 108, 72),
            "g19-6x9": (54, 162, 108),
            "g19-8x9": (72, 216, 144),
        }
        for name, params in G19_PARAMETER_SETS.items():
            with self.subTest(params=name):
                public, reference = generate_disjoint_cohomology_pair_instance(
                    params, FIXED_SEED
                )
                self.assertTrue(
                    validate_disjoint_cohomology_pair_witness(public, reference.witness).valid
                )
                recovery = recover_disjoint_cohomology_pair(
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
                self.assertTrue(recovery.selected_accepted)
                self.assertEqual(recovery.selected_shared_vertices, 0)
                self.assertEqual(recovery.selected_first_pairing, 1)
                self.assertEqual(recovery.selected_second_pairing, 1)
                self.assertLessEqual(
                    recovery.selected_short_length, recovery.max_short_length
                )
                self.assertLessEqual(
                    recovery.selected_long_length, recovery.max_long_length
                )
                self.assertGreater(recovery.first_stage_candidates, 0)
                self.assertGreater(recovery.second_stage_calls, 0)
                self.assertGreater(recovery.second_stage_edge_scans, 0)

    def test_attack_does_not_need_reference(self) -> None:
        params = G19_PARAMETER_SETS["g19-6x6"]
        public, _ = generate_disjoint_cohomology_pair_instance(params, FIXED_SEED)
        recovery = recover_disjoint_cohomology_pair(
            public, reference=None, successful_flips=params.successful_flips
        )
        self.assertTrue(recovery.selected_accepted)
        self.assertIsNone(recovery.selected_matches_reference)
        self.assertEqual(recovery.selected_shared_vertices, 0)

    def test_public_bounds_are_enforced(self) -> None:
        params = G19_PARAMETER_SETS["g19-6x6"]
        public, reference = generate_disjoint_cohomology_pair_instance(params, FIXED_SEED)
        too_tight = DisjointCohomologyPairPublicInstance(
            public.name,
            public.target,
            public.alpha,
            max(0, public.max_short_length - 1),
            max(0, public.max_long_length - 1),
        )
        self.assertFalse(
            validate_disjoint_cohomology_pair_witness(too_tight, reference.witness).valid
        )

    def test_multi_seed_break(self) -> None:
        for name, params in G19_PARAMETER_SETS.items():
            for seed_index in range(3):
                seed = hashlib.sha256(
                    b"MORPH-KEM G19 unit sweep v1\x00"
                    + name.encode("ascii")
                    + seed_index.to_bytes(4, "big")
                ).digest()
                with self.subTest(params=name, seed=seed_index):
                    public, reference = generate_disjoint_cohomology_pair_instance(
                        params, seed
                    )
                    recovery = recover_disjoint_cohomology_pair(
                        public,
                        reference=reference,
                        successful_flips=params.successful_flips,
                    )
                    self.assertTrue(recovery.selected_accepted)
                    self.assertEqual(recovery.selected_shared_vertices, 0)
                    self.assertEqual(
                        (recovery.selected_first_pairing, recovery.selected_second_pairing),
                        (1, 1),
                    )

    def test_parameter_seed_and_retry_bounds(self) -> None:
        with self.assertRaises(GluingExperimentError):
            DisjointCohomologyPairParameters("bad", 3, 6, 1).validate()
        with self.assertRaises(GluingExperimentError):
            DisjointCohomologyPairParameters("bad", 6, 6, 1000).validate()
        with self.assertRaises(GluingExperimentError):
            generate_disjoint_cohomology_pair_instance(
                G19_PARAMETER_SETS["g19-6x6"], b"short"
            )
        with self.assertRaises(GluingExperimentError):
            generate_disjoint_cohomology_pair_instance(
                G19_PARAMETER_SETS["g19-6x6"], FIXED_SEED, max_generation_retries=65
            )


if __name__ == "__main__":
    unittest.main()
