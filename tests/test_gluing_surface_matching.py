from __future__ import annotations

import unittest

from morph_kem.gluing import GluingExperimentError
from morph_kem.gluing_surface_matching import (
    G10_PARAMETER_SETS,
    ToroidalMatchingParameters,
    generate_toroidal_matching_instance,
    recover_toroidal_matching,
    toroidal_matching_incidence,
    toroidal_reference_partition_matches,
    validate_toroidal_matching_witness,
)


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


class ToroidalMatchingTests(unittest.TestCase):
    def test_exact_surface_and_dual_metrics(self) -> None:
        for name, params in G10_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public, reference = generate_toroidal_matching_instance(params, MASTER_SEED)
                incidence = toroidal_matching_incidence(public)
                recovery = recover_toroidal_matching(public, reference=reference)
                cells = params.rows * params.cols

                self.assertEqual(incidence.vertices, cells)
                self.assertEqual(incidence.edges, 3 * cells)
                self.assertEqual(incidence.triangles, 2 * cells)
                self.assertEqual(incidence.euler_characteristic, 0)
                self.assertEqual(incidence.min_triangles_per_edge, 2)
                self.assertEqual(incidence.max_triangles_per_edge, 2)
                self.assertEqual(recovery.dual_edges, 3 * cells)
                self.assertEqual(recovery.dual_degree_histogram, ((3, 2 * cells),))
                self.assertEqual(recovery.bridge_count, 0)
                self.assertEqual(recovery.articulation_points, ())
                self.assertEqual(recovery.bipartition_sizes, (cells, cells))
                self.assertEqual(recovery.candidate_edges, 3 * cells)
                self.assertEqual(recovery.base_augmentations, cells)
                self.assertTrue(validate_toroidal_matching_witness(public, reference.groups).valid)

    def test_a037_public_matching_is_fatal(self) -> None:
        for name, params in G10_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public, reference = generate_toroidal_matching_instance(params, MASTER_SEED)
                recovery = recover_toroidal_matching(public, reference=reference)
                self.assertGreaterEqual(recovery.matching_solutions, 2)
                self.assertEqual(recovery.accepted_solutions, recovery.matching_solutions)
                self.assertEqual(recovery.nonreference_accepted_solutions, recovery.accepted_solutions - 1)
                self.assertGreater(recovery.base_dfs_calls, 0)
                self.assertGreater(recovery.base_edge_scans, 0)
                self.assertGreater(recovery.alternative_attempts, 0)
                self.assertTrue(
                    any(
                        toroidal_reference_partition_matches(reference, groups)
                        for groups in recovery.accepted_groups
                    )
                )
                self.assertTrue(
                    any(
                        not toroidal_reference_partition_matches(reference, groups)
                        for groups in recovery.accepted_groups
                    )
                )

    def test_attack_does_not_need_reference(self) -> None:
        public, _ = generate_toroidal_matching_instance(G10_PARAMETER_SETS["g10-8x8"], MASTER_SEED)
        recovery = recover_toroidal_matching(public)
        self.assertGreaterEqual(recovery.accepted_solutions, 2)
        self.assertEqual(recovery.nonreference_accepted_solutions, 0)

    def test_break_is_stable_under_public_relabeling(self) -> None:
        for name, params in G10_PARAMETER_SETS.items():
            for seed_index in range(4):
                with self.subTest(name=name, seed=seed_index):
                    seed = bytes([seed_index + 1]) * 32
                    public, reference = generate_toroidal_matching_instance(params, seed)
                    recovery = recover_toroidal_matching(public, reference=reference)
                    self.assertEqual(recovery.bridge_count, 0)
                    self.assertFalse(recovery.articulation_points)
                    self.assertGreaterEqual(recovery.accepted_solutions, 2)
                    self.assertGreaterEqual(recovery.nonreference_accepted_solutions, 1)

    def test_invalid_partition_is_rejected(self) -> None:
        public, reference = generate_toroidal_matching_instance(
            G10_PARAMETER_SETS["g10-4x4"], MASTER_SEED
        )
        changed = list(reference.groups)
        changed[0] = (changed[0][0], changed[1][0])
        self.assertFalse(validate_toroidal_matching_witness(public, tuple(changed)).valid)

    def test_parameter_seed_and_cap_bounds(self) -> None:
        with self.assertRaises(GluingExperimentError):
            ToroidalMatchingParameters("odd", 5, 6).validate()
        with self.assertRaises(GluingExperimentError):
            ToroidalMatchingParameters("small", 2, 4).validate()
        with self.assertRaises(GluingExperimentError):
            generate_toroidal_matching_instance(G10_PARAMETER_SETS["g10-4x4"], b"short")
        public, _ = generate_toroidal_matching_instance(G10_PARAMETER_SETS["g10-4x4"], MASTER_SEED)
        with self.assertRaises(GluingExperimentError):
            recover_toroidal_matching(public, solution_cap=0)


if __name__ == "__main__":
    unittest.main()
