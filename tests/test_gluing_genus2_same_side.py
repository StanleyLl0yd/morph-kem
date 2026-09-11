from __future__ import annotations

import unittest

from morph_kem.gluing import GluingExperimentError
from morph_kem.gluing_genus2_same_side import (
    G22_PARAMETER_SETS,
    SameSideParameters,
    SameSideWitness,
    generate_same_side_instance,
    recover_same_side_witness,
    validate_same_side_witness,
)


MASTER_SEED = bytes.fromhex("a17e0405060708091011121314151617")


class GenusTwoSameSideTests(unittest.TestCase):
    def test_public_compatibility_attack_finds_accepted_family(self) -> None:
        for name, params in G22_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public = generate_same_side_instance(params, MASTER_SEED)
                recovery = recover_same_side_witness(public)
                self.assertEqual(recovery.euler_characteristic, -2)
                self.assertEqual(recovery.h1_dimension, 4)
                self.assertEqual(recovery.selected_rank, 4)
                self.assertTrue(recovery.selected_accepted)
                self.assertGreater(recovery.retained_candidates, 3)
                self.assertGreater(recovery.exact_one_pairs, 1)
                self.assertGreater(recovery.pair_pair_tests, 0)

    def test_attack_is_stable_under_public_relabeling_seeds(self) -> None:
        params = G22_PARAMETER_SETS["g22-6x6"]
        for seed_index in range(4):
            with self.subTest(seed=seed_index):
                public = generate_same_side_instance(params, bytes([seed_index + 1]) * 32)
                recovery = recover_same_side_witness(public)
                self.assertTrue(recovery.selected_accepted)
                self.assertEqual(recovery.selected_rank, 4)

    def test_invalid_same_side_pattern_is_rejected(self) -> None:
        public = generate_same_side_instance(G22_PARAMETER_SETS["g22-4x4"], MASTER_SEED)
        recovery = recover_same_side_witness(public)
        # Reconstruct an accepted family through a second deterministic recovery path is not
        # exposed directly; instead use candidate corruption via duplicate cycles after
        # obtaining the public attack through the module's verifier contract.
        from morph_kem.gluing_genus2_same_side import _enumerate_candidates
        from morph_kem.gluing_cohomology_cycle import _edges

        candidates, _, _, _ = _enumerate_candidates(public)
        edges = _edges(public.target)
        first = tuple(sorted(edges[index] for index in candidates[0][0]))
        witness = SameSideWitness((first, first, first, first))
        self.assertFalse(validate_same_side_witness(public, witness).valid)
        self.assertTrue(recovery.selected_accepted)

    def test_parameter_bounds(self) -> None:
        with self.assertRaises(GluingExperimentError):
            SameSideParameters("small", 3, 4, 10, 10).validate()
        with self.assertRaises(GluingExperimentError):
            generate_same_side_instance(G22_PARAMETER_SETS["g22-4x4"], b"short")


if __name__ == "__main__":
    unittest.main()
