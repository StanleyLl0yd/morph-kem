from __future__ import annotations

import hashlib
import unittest

from morph_kem.gluing import GluingExperimentError, gluing_incidence
from morph_kem.gluing_cycle import recover_cycle_gluing_by_k4_exact_cover
from morph_kem.gluing_stellar import (
    G2_PARAMETER_SETS,
    StellarGluingParameters,
    generate_stellar_gluing_instance,
    recover_stellar_gluing_by_center_contraction,
    stellar_reference_partition_matches,
    validate_stellar_gluing_witness,
)


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


class StellarGluingTests(unittest.TestCase):
    def test_exact_structural_metrics(self) -> None:
        for name, params in G2_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public, reference = generate_stellar_gluing_instance(params, MASTER_SEED)
                incidence = gluing_incidence(public)
                n = params.piece_count
                self.assertEqual(incidence.vertices, 6 * n + 2)
                self.assertEqual(incidence.edges, 23 * n + 1)
                self.assertEqual(incidence.faces, 33 * n)
                self.assertEqual(incidence.tetrahedra, 16 * n)
                self.assertEqual(incidence.boundary_faces, 2 * n)
                self.assertEqual(incidence.max_face_incidence, 2)
                self.assertEqual(incidence.euler_characteristic, 1)
                self.assertEqual(incidence.dual_edges, 31 * n)
                self.assertTrue(validate_stellar_gluing_witness(public, reference.groups).valid)

    def test_a028_no_longer_returns_piece_level_witness(self) -> None:
        params = G2_PARAMETER_SETS["g2-4"]
        public, _ = generate_stellar_gluing_instance(params, MASTER_SEED)
        old_attack = recover_cycle_gluing_by_k4_exact_cover(public)
        self.assertEqual(old_attack.dual_k4_candidates, 4 * params.piece_count)
        self.assertEqual(old_attack.allowed_piece_candidates, 4 * params.piece_count)
        self.assertFalse(old_attack.validation.valid)
        self.assertEqual(old_attack.groups, ())

    def test_a029_recovers_exact_partition(self) -> None:
        for name, params in G2_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public, reference = generate_stellar_gluing_instance(params, MASTER_SEED)
                recovery = recover_stellar_gluing_by_center_contraction(public)
                n = params.piece_count
                self.assertEqual(recovery.micro_bridge_count, 0)
                self.assertEqual(recovery.micro_articulation_points, ())
                self.assertGreater(recovery.micro_two_vertex_separator_pairs, 0)
                self.assertEqual(recovery.center_star_candidates, 4 * n)
                self.assertEqual(set(recovery.candidate_centers), set(reference.center_vertices))
                self.assertEqual(recovery.center_cover_solutions, 1)
                self.assertFalse(recovery.center_cover_cap_hit)
                self.assertEqual(recovery.center_cover_nodes, 4 * n + 1)
                self.assertEqual(recovery.center_cover_backtracks, 0)
                self.assertEqual(recovery.reconstructed_macro_tetrahedra, 4 * n)
                self.assertEqual(recovery.macro_dual_edges, 7 * n)
                self.assertEqual(recovery.macro_k4_candidates, n)
                self.assertEqual(recovery.macro_allowed_piece_candidates, n)
                self.assertEqual(recovery.macro_cover_solutions, 1)
                self.assertEqual(recovery.macro_cover_nodes, n + 1)
                self.assertEqual(recovery.macro_cover_backtracks, 0)
                self.assertTrue(recovery.validation.valid)
                self.assertTrue(stellar_reference_partition_matches(reference, recovery.groups))

    def test_recovery_is_stable_under_public_relabeling(self) -> None:
        params = G2_PARAMETER_SETS["g2-6"]
        for seed_index in range(8):
            seed = hashlib.sha256(
                b"MORPH-KEM G2 test relabel v1\x00"
                + MASTER_SEED
                + seed_index.to_bytes(4, "big")
            ).digest()
            public, reference = generate_stellar_gluing_instance(params, seed)
            recovery = recover_stellar_gluing_by_center_contraction(public)
            self.assertTrue(recovery.validation.valid)
            self.assertTrue(stellar_reference_partition_matches(reference, recovery.groups))
            self.assertEqual(set(recovery.candidate_centers), set(reference.center_vertices))

    def test_invalid_partition_is_rejected(self) -> None:
        public, reference = generate_stellar_gluing_instance(G2_PARAMETER_SETS["g2-4"], MASTER_SEED)
        groups = list(reference.groups)
        malformed = tuple(groups[0][:-1] + (groups[1][0],))
        groups[0] = malformed
        self.assertFalse(validate_stellar_gluing_witness(public, tuple(groups)).valid)

    def test_parameter_seed_and_cap_bounds(self) -> None:
        with self.assertRaises(GluingExperimentError):
            generate_stellar_gluing_instance(StellarGluingParameters("too-small", 3), MASTER_SEED)
        with self.assertRaises(GluingExperimentError):
            generate_stellar_gluing_instance(StellarGluingParameters("too-large", 9), MASTER_SEED)
        with self.assertRaises(GluingExperimentError):
            generate_stellar_gluing_instance(G2_PARAMETER_SETS["g2-4"], b"short")

        public, _ = generate_stellar_gluing_instance(G2_PARAMETER_SETS["g2-4"], MASTER_SEED)
        with self.assertRaises(GluingExperimentError):
            recover_stellar_gluing_by_center_contraction(public, center_solution_cap=0)
        with self.assertRaises(GluingExperimentError):
            recover_stellar_gluing_by_center_contraction(public, center_solution_cap=1025)
        with self.assertRaises(GluingExperimentError):
            recover_stellar_gluing_by_center_contraction(public, macro_solution_cap=0)


if __name__ == "__main__":
    unittest.main()
