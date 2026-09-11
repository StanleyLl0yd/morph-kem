from __future__ import annotations

import hashlib
import unittest
from itertools import combinations

from morph_kem.gluing import GluingExperimentError
from morph_kem.gluing_cohomology_cycle import (
    G16_PARAMETER_SETS,
    CohomologyCycleParameters,
    generate_cohomology_cycle_instance,
    recover_cohomology_cycle,
    validate_cohomology_cycle_witness,
)


class CohomologyCycleTests(unittest.TestCase):
    def test_exact_topological_dimensions_and_public_break(self) -> None:
        expected = {
            "g16-6x6": (36, 108, 72, 73, 71, 37, 35, 72),
            "g16-6x9": (54, 162, 108, 109, 107, 55, 53, 108),
            "g16-8x9": (72, 216, 144, 145, 143, 73, 71, 144),
        }
        seed = bytes.fromhex("43" * 32)
        for name, params in G16_PARAMETER_SETS.items():
            with self.subTest(params=name):
                public, reference = generate_cohomology_cycle_instance(params, seed)
                recovery = recover_cohomology_cycle(
                    public,
                    reference=reference,
                    successful_flips=params.successful_flips,
                )
                (
                    vertices,
                    edges,
                    triangles,
                    cycle_nullity,
                    cocycle_rank,
                    cocycle_dimension,
                    coboundary_rank,
                    affine_nullity,
                ) = expected[name]
                self.assertEqual((recovery.vertices, recovery.edges, recovery.triangles), (vertices, edges, triangles))
                self.assertEqual(recovery.euler_characteristic, 0)
                self.assertEqual((recovery.min_triangles_per_edge, recovery.max_triangles_per_edge), (2, 2))
                self.assertEqual(recovery.successful_flips, params.successful_flips)
                self.assertEqual(recovery.cycle_rank, vertices - 1)
                self.assertEqual(recovery.cycle_nullity, cycle_nullity)
                self.assertEqual(recovery.cocycle_rank, cocycle_rank)
                self.assertEqual(recovery.cocycle_dimension, cocycle_dimension)
                self.assertEqual(recovery.coboundary_rank, coboundary_rank)
                self.assertEqual(recovery.h1_dimension, 2)
                self.assertEqual(recovery.tree_edges, vertices - 1)
                self.assertEqual(recovery.non_tree_edges, cycle_nullity)
                self.assertGreaterEqual(recovery.fundamental_cycles_tested, 1)
                self.assertLessEqual(recovery.fundamental_cycles_tested, cycle_nullity)
                self.assertGreaterEqual(recovery.selected_cycle_length, 3)
                self.assertTrue(recovery.selected_cycle_accepted)
                self.assertEqual(recovery.affine_rank, vertices)
                self.assertEqual(recovery.affine_nullity, affine_nullity)
                self.assertGreaterEqual(recovery.affine_support_edges, 3)
                self.assertTrue(recovery.affine_cycle_accepted)
                self.assertTrue(validate_cohomology_cycle_witness(public, reference.cycle).valid)

    def test_attack_does_not_need_reference(self) -> None:
        params = G16_PARAMETER_SETS["g16-6x6"]
        public, _ = generate_cohomology_cycle_instance(params, bytes.fromhex("52" * 32))
        recovery = recover_cohomology_cycle(
            public, reference=None, successful_flips=params.successful_flips
        )
        self.assertTrue(recovery.selected_cycle_accepted)
        self.assertIsNone(recovery.selected_cycle_matches_reference)
        self.assertTrue(recovery.affine_cycle_accepted)

    def test_triangle_boundary_is_rejected_by_odd_pairing_verifier(self) -> None:
        params = G16_PARAMETER_SETS["g16-6x6"]
        public, _ = generate_cohomology_cycle_instance(params, bytes.fromhex("61" * 32))
        triangle = next(simplex for simplex in sorted(public.target.simplices) if len(simplex) == 3)
        witness = tuple(sorted(tuple(sorted(edge)) for edge in combinations(triangle, 2)))
        validation = validate_cohomology_cycle_witness(public, witness)
        self.assertFalse(validation.valid)
        self.assertEqual(validation.pairing, 0)

    def test_all_sizes_multi_seed_public_break(self) -> None:
        for name, params in G16_PARAMETER_SETS.items():
            for seed_index in range(4):
                seed = hashlib.sha256(
                    b"MORPH-KEM G16 unit sweep\x00"
                    + name.encode("ascii")
                    + seed_index.to_bytes(4, "big")
                ).digest()
                with self.subTest(params=name, seed=seed_index):
                    public, reference = generate_cohomology_cycle_instance(params, seed)
                    recovery = recover_cohomology_cycle(
                        public,
                        reference=reference,
                        successful_flips=params.successful_flips,
                    )
                    self.assertEqual(recovery.h1_dimension, 2)
                    self.assertTrue(recovery.selected_cycle_accepted)
                    self.assertTrue(recovery.affine_cycle_accepted)

    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(GluingExperimentError):
            CohomologyCycleParameters("bad", 3, 6, 1).validate()
        with self.assertRaises(GluingExperimentError):
            CohomologyCycleParameters("bad", 6, 6, 1000).validate()
        with self.assertRaises(GluingExperimentError):
            generate_cohomology_cycle_instance(G16_PARAMETER_SETS["g16-6x6"], b"short")


if __name__ == "__main__":
    unittest.main()
