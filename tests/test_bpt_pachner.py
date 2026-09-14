from __future__ import annotations

import unittest

from morph_kem.bpt_pachner import (
    BPTError,
    BPTWeakParameters,
    BPT_WEAK_PARAMETER_SETS,
    apply_move,
    boundary_of_4_simplex,
    canonical_tetrahedral_signature,
    generate_bpt_weak_instance,
    inverse_move,
    isomorphic,
    recover_bpt_weak,
    verify_path,
)


class BPTPachnerWeakTests(unittest.TestCase):
    def test_boundary_of_4_simplex_is_standard_s3_control(self) -> None:
        sphere = boundary_of_4_simplex()
        self.assertEqual(sphere.dimension, 3)
        self.assertEqual(len(sphere.vertices), 5)
        self.assertEqual(len(sphere.facets), 5)

    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(BPTError):
            BPTWeakParameters("bad", 4).validate()
        with self.assertRaises(BPTError):
            generate_bpt_weak_instance(BPT_WEAK_PARAMETER_SETS["bptw0-d1"], b"short")

    def test_one_four_inverse_round_trip(self) -> None:
        params = BPT_WEAK_PARAMETER_SETS["bptw0-d1"]
        public, reference = generate_bpt_weak_instance(params, b"BPT-W0 inverse unit seed v1")
        # The first half of the planted path collapses source to the common root.
        first = reference.planted_path[0]
        root = apply_move(public.source, first)
        self.assertEqual(root, boundary_of_4_simplex())
        self.assertEqual(apply_move(root, inverse_move(first)), public.source)

    def test_public_verifier_accepts_generated_reference(self) -> None:
        params = BPT_WEAK_PARAMETER_SETS["bptw0-d3"]
        public, reference = generate_bpt_weak_instance(params, b"BPT-W0 verifier unit seed v1")
        self.assertEqual(len(reference.planted_path), public.move_bound)
        self.assertTrue(verify_path(public, reference.planted_path))

    def test_exact_toy_isomorphism_signature_survives_relabeling(self) -> None:
        sphere = boundary_of_4_simplex()
        relabelled = sphere.relabel({0: 9, 1: 7, 2: 5, 3: 3, 4: 1})
        self.assertNotEqual(sphere, relabelled)
        self.assertTrue(isomorphic(sphere, relabelled))
        self.assertEqual(
            canonical_tetrahedral_signature(sphere),
            canonical_tetrahedral_signature(relabelled),
        )

    def test_greedy_public_attack_recovers_accepted_path_without_reference(self) -> None:
        params = BPT_WEAK_PARAMETER_SETS["bptw0-d3"]
        public, _ = generate_bpt_weak_instance(params, b"BPT-W0 public recovery unit seed v1")
        recovery = recover_bpt_weak(public)
        self.assertTrue(recovery.accepted)
        self.assertEqual(recovery.recovered_length, public.move_bound)
        self.assertTrue(recovery.common_root_exact)
        self.assertIsNone(recovery.matches_planted_after_public_success)
        self.assertGreaterEqual(recovery.accepted_path_multiplicity_lower_bound, 1)

    def test_break_is_stable_across_seeds(self) -> None:
        params = BPT_WEAK_PARAMETER_SETS["bptw0-d3"]
        for index in range(8):
            seed = (f"BPT-W0 deterministic seed {index:02d} v1").encode().ljust(40, b".")
            public, reference = generate_bpt_weak_instance(params, seed)
            recovery = recover_bpt_weak(public, reference=reference)
            self.assertTrue(recovery.accepted)
            self.assertLessEqual(recovery.recovered_length, public.move_bound)
            self.assertEqual(recovery.source_simplification_steps, params.stack_depth)
            self.assertEqual(recovery.target_simplification_steps, params.stack_depth)


if __name__ == "__main__":
    unittest.main()
