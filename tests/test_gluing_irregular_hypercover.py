from __future__ import annotations

import unittest

from morph_kem.gluing import GluingExperimentError
from morph_kem.gluing_irregular_hypercover import (
    G12_PARAMETER_SETS,
    IrregularHypercoverParameters,
    encode_irregular_hypercover_sat,
    generate_irregular_hypercover_instance,
    recover_irregular_hypercover,
    validate_irregular_hypercover_witness,
)
from morph_kem.gluing_surface_hypercover import toroidal_hypercover_incidence


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


class IrregularHypercoverTests(unittest.TestCase):
    def test_structural_gate_and_irregularity(self) -> None:
        for name, params in G12_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public, reference = generate_irregular_hypercover_instance(params, MASTER_SEED)
                incidence = toroidal_hypercover_incidence(public)
                recovery = recover_irregular_hypercover(
                    public, reference=reference, solution_cap=8
                )
                triangle_count = 2 * params.rows * params.cols
                self.assertEqual(incidence.vertices, params.rows * params.cols)
                self.assertEqual(incidence.edges, 3 * params.rows * params.cols)
                self.assertEqual(incidence.triangles, triangle_count)
                self.assertEqual(incidence.euler_characteristic, 0)
                self.assertEqual(incidence.min_triangles_per_edge, 2)
                self.assertEqual(incidence.max_triangles_per_edge, 2)
                self.assertEqual(recovery.successful_flips, params.successful_flips)
                self.assertGreaterEqual(recovery.generation_retries, 0)
                self.assertEqual(recovery.dual_edges, 3 * triangle_count // 2)
                self.assertEqual(recovery.dual_degree_histogram, ((3, triangle_count),))
                self.assertEqual(recovery.bridge_count, 0)
                self.assertEqual(recovery.articulation_points, ())
                self.assertGreater(len(recovery.primal_vertex_degree_histogram), 1)
                self.assertGreater(recovery.local_signature_classes, 1)
                self.assertGreater(recovery.candidate_count, 0)
                self.assertGreater(recovery.candidate_triangle_incidence, 0)
                self.assertTrue(
                    validate_irregular_hypercover_witness(public, reference.groups).valid
                )

    def test_a039_recovers_public_cover(self) -> None:
        for name, params in G12_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public, reference = generate_irregular_hypercover_instance(params, MASTER_SEED)
                recovery = recover_irregular_hypercover(
                    public, reference=reference, solution_cap=16
                )
                self.assertGreater(recovery.accepted_solutions, 0)
                self.assertGreater(recovery.exact_cover_nodes, 0)
                self.assertTrue(
                    all(
                        validate_irregular_hypercover_witness(public, groups).valid
                        for groups in recovery.accepted_groups
                    )
                )

    def test_attack_does_not_need_reference(self) -> None:
        public, _ = generate_irregular_hypercover_instance(
            G12_PARAMETER_SETS["g12-6x6"], MASTER_SEED
        )
        recovery = recover_irregular_hypercover(public, solution_cap=4)
        self.assertGreater(recovery.accepted_solutions, 0)
        self.assertEqual(recovery.nonreference_accepted_solutions, 0)
        self.assertEqual(recovery.successful_flips, -1)
        self.assertEqual(recovery.generation_retries, -1)

    def test_sat_encoding_covers_every_public_triangle(self) -> None:
        for name, params in G12_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public, _ = generate_irregular_hypercover_instance(params, MASTER_SEED)
                encoding = encode_irregular_hypercover_sat(public)
                self.assertGreater(encoding.variable_count, 0)
                self.assertGreater(len(encoding.clauses), 0)
                self.assertTrue(encoding.to_dimacs().startswith("p cnf "))

    def test_invalid_partition_is_rejected(self) -> None:
        public, reference = generate_irregular_hypercover_instance(
            G12_PARAMETER_SETS["g12-6x6"], MASTER_SEED
        )
        changed = list(reference.groups)
        changed[-1] = changed[0]
        self.assertFalse(validate_irregular_hypercover_witness(public, tuple(changed)).valid)

    def test_break_is_stable_under_public_relabeling(self) -> None:
        for name, params in G12_PARAMETER_SETS.items():
            for seed_index in range(3):
                with self.subTest(name=name, seed=seed_index):
                    seed = bytes([seed_index + 1]) * 32
                    public, reference = generate_irregular_hypercover_instance(params, seed)
                    recovery = recover_irregular_hypercover(
                        public, reference=reference, solution_cap=4
                    )
                    self.assertGreater(recovery.accepted_solutions, 0)
                    self.assertEqual(recovery.bridge_count, 0)
                    self.assertEqual(recovery.articulation_points, ())
                    self.assertGreater(recovery.local_signature_classes, 1)

    def test_parameter_seed_and_cap_bounds(self) -> None:
        with self.assertRaises(GluingExperimentError):
            IrregularHypercoverParameters("too-small", 3, 6, 1).validate()
        with self.assertRaises(GluingExperimentError):
            IrregularHypercoverParameters("not-divisible", 4, 4, 1).validate()
        with self.assertRaises(GluingExperimentError):
            IrregularHypercoverParameters("bad-flips", 6, 6, 0).validate()
        with self.assertRaises(GluingExperimentError):
            generate_irregular_hypercover_instance(
                G12_PARAMETER_SETS["g12-6x6"], b"short"
            )
        public, _ = generate_irregular_hypercover_instance(
            G12_PARAMETER_SETS["g12-6x6"], MASTER_SEED
        )
        for cap in (0, 1025):
            with self.assertRaises(GluingExperimentError):
                recover_irregular_hypercover(public, solution_cap=cap)


if __name__ == "__main__":
    unittest.main()
