from __future__ import annotations

import unittest

from morph_kem.gluing import GluingExperimentError
from morph_kem.gluing_surface_hypercover import (
    G11_PARAMETER_SETS,
    ToroidalHypercoverParameters,
    encode_toroidal_hypercover_sat,
    enumerate_p3_candidates,
    generate_toroidal_hypercover_instance,
    recover_toroidal_hypercover,
    toroidal_hypercover_incidence,
    validate_toroidal_hypercover_witness,
)


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


class ToroidalHypercoverTests(unittest.TestCase):
    def test_exact_structural_candidate_metrics(self) -> None:
        for name, params in G11_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public, reference = generate_toroidal_hypercover_instance(params, MASTER_SEED)
                incidence = toroidal_hypercover_incidence(public)
                recovery = recover_toroidal_hypercover(
                    public, reference=reference, solution_cap=16
                )
                triangle_count = 2 * params.rows * params.cols
                self.assertEqual(incidence.vertices, params.rows * params.cols)
                self.assertEqual(incidence.edges, 3 * params.rows * params.cols)
                self.assertEqual(incidence.triangles, triangle_count)
                self.assertEqual(incidence.euler_characteristic, 0)
                self.assertEqual(incidence.min_triangles_per_edge, 2)
                self.assertEqual(incidence.max_triangles_per_edge, 2)
                self.assertEqual(recovery.dual_edges, 3 * triangle_count // 2)
                self.assertEqual(recovery.dual_degree_histogram, ((3, triangle_count),))
                self.assertEqual(recovery.bridge_count, 0)
                self.assertEqual(recovery.articulation_points, ())
                self.assertEqual(recovery.bipartition_sizes, (triangle_count // 2, triangle_count // 2))
                self.assertEqual(recovery.candidate_count, 3 * triangle_count)
                self.assertEqual(recovery.candidate_membership_histogram, ((9, triangle_count),))
                self.assertEqual(
                    recovery.candidate_overlap_degree_histogram,
                    ((18, 3 * triangle_count),),
                )
                self.assertEqual(recovery.candidate_triangle_incidence, 9 * triangle_count)
                self.assertEqual(len(enumerate_p3_candidates(public)), 3 * triangle_count)
                self.assertTrue(validate_toroidal_hypercover_witness(public, reference.groups).valid)

    def test_a038_finds_equivalent_public_covers(self) -> None:
        for name, params in G11_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public, reference = generate_toroidal_hypercover_instance(params, MASTER_SEED)
                recovery = recover_toroidal_hypercover(
                    public, reference=reference, solution_cap=16
                )
                self.assertEqual(recovery.exact_cover_solutions, 16)
                self.assertTrue(recovery.exact_cover_cap_hit)
                self.assertEqual(recovery.accepted_solutions, 16)
                self.assertGreaterEqual(recovery.nonreference_accepted_solutions, 15)
                self.assertGreater(recovery.exact_cover_nodes, 0)
                self.assertGreater(recovery.exact_cover_decisions, 0)
                self.assertTrue(
                    all(
                        validate_toroidal_hypercover_witness(public, groups).valid
                        for groups in recovery.accepted_groups
                    )
                )

    def test_attack_does_not_need_reference(self) -> None:
        public, _ = generate_toroidal_hypercover_instance(
            G11_PARAMETER_SETS["g11-6x6"], MASTER_SEED
        )
        recovery = recover_toroidal_hypercover(public, solution_cap=8)
        self.assertEqual(recovery.accepted_solutions, 8)
        self.assertTrue(recovery.exact_cover_cap_hit)
        self.assertEqual(recovery.nonreference_accepted_solutions, 0)

    def test_sat_encoding_matches_regular_candidate_incidence(self) -> None:
        for name, params in G11_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public, _ = generate_toroidal_hypercover_instance(params, MASTER_SEED)
                encoding = encode_toroidal_hypercover_sat(public)
                triangle_count = 2 * params.rows * params.cols
                self.assertEqual(encoding.variable_count, 3 * triangle_count)
                self.assertEqual(len(encoding.clauses), 37 * triangle_count)
                header = encoding.to_dimacs().splitlines()[0]
                self.assertEqual(
                    header,
                    f"p cnf {3 * triangle_count} {37 * triangle_count}",
                )

    def test_invalid_partition_is_rejected(self) -> None:
        public, reference = generate_toroidal_hypercover_instance(
            G11_PARAMETER_SETS["g11-3x6"], MASTER_SEED
        )
        changed = list(reference.groups)
        changed[-1] = changed[0]
        self.assertFalse(validate_toroidal_hypercover_witness(public, tuple(changed)).valid)

    def test_break_is_stable_under_public_relabeling(self) -> None:
        for name, params in G11_PARAMETER_SETS.items():
            for seed_index in range(4):
                with self.subTest(name=name, seed=seed_index):
                    seed = bytes([seed_index + 1]) * 32
                    public, reference = generate_toroidal_hypercover_instance(params, seed)
                    recovery = recover_toroidal_hypercover(
                        public, reference=reference, solution_cap=8
                    )
                    self.assertEqual(recovery.accepted_solutions, 8)
                    self.assertTrue(recovery.exact_cover_cap_hit)
                    self.assertGreaterEqual(recovery.nonreference_accepted_solutions, 7)
                    self.assertEqual(recovery.bridge_count, 0)
                    self.assertEqual(recovery.articulation_points, ())

    def test_parameter_seed_and_cap_bounds(self) -> None:
        with self.assertRaises(GluingExperimentError):
            ToroidalHypercoverParameters("too-small", 2, 6).validate()
        with self.assertRaises(GluingExperimentError):
            ToroidalHypercoverParameters("not-divisible", 4, 4).validate()
        with self.assertRaises(GluingExperimentError):
            generate_toroidal_hypercover_instance(
                G11_PARAMETER_SETS["g11-3x6"], b"short"
            )
        public, _ = generate_toroidal_hypercover_instance(
            G11_PARAMETER_SETS["g11-3x6"], MASTER_SEED
        )
        for cap in (0, 1025):
            with self.assertRaises(GluingExperimentError):
                recover_toroidal_hypercover(public, solution_cap=cap)


if __name__ == "__main__":
    unittest.main()
