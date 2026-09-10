from __future__ import annotations

import hashlib
import math
import unittest

from morph_kem.gluing import GluingExperimentError
from morph_kem.gluing_cycle import (
    G1_PARAMETER_SETS,
    CycleGluingParameters,
    cycle_structure,
    generate_cycle_gluing_instance,
    recover_cycle_by_dual_k4,
    recover_cycle_by_vertex_stars,
    validate_cycle_gluing_witness,
)


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


class CycleGluingTests(unittest.TestCase):
    def test_exact_structural_gate_and_metrics(self) -> None:
        expected = {
            "g1-3": (8, 22, 27, 12, 6, 21, 48, 42),
            "g1-5": (12, 36, 45, 20, 10, 35, 80, 70),
            "g1-8": (18, 57, 72, 32, 16, 56, 128, 112),
        }

        for name, params in G1_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public, reference = generate_cycle_gluing_instance(params, MASTER_SEED)
                structure = cycle_structure(public)
                self.assertEqual(
                    (
                        structure.vertices,
                        structure.edges,
                        structure.faces,
                        structure.tetrahedra,
                        structure.boundary_faces,
                        structure.dual_edges,
                        structure.face_occurrences,
                        structure.dfs_edge_scans,
                    ),
                    expected[name],
                )
                self.assertEqual(structure.max_face_incidence, 2)
                self.assertEqual(structure.euler_characteristic, 1)
                self.assertEqual(structure.bridges, ())
                self.assertEqual(structure.articulation_vertices, ())
                self.assertEqual(
                    structure.dual_degree_histogram,
                    ((3, 2 * params.piece_count), (4, 2 * params.piece_count)),
                )
                self.assertEqual(
                    structure.vertex_tetrahedron_degree_histogram,
                    (
                        (4, params.piece_count),
                        (6, params.piece_count),
                        (3 * params.piece_count, 2),
                    ),
                )
                self.assertEqual(sum(reference.swap_bits) % 2, 0)
                self.assertTrue(validate_cycle_gluing_witness(public, reference.groups).valid)

    def test_a028_vertex_star_recovery_is_exact(self) -> None:
        for params in G1_PARAMETER_SETS.values():
            with self.subTest(name=params.name):
                public, reference = generate_cycle_gluing_instance(params, MASTER_SEED)
                recovery = recover_cycle_by_vertex_stars(public, reference)
                self.assertEqual(recovery.candidate_vertices, params.piece_count)
                self.assertEqual(len(recovery.valid_candidates), params.piece_count)
                self.assertTrue(recovery.exact_cover.validation.valid)
                self.assertEqual(recovery.exact_cover.nodes, params.piece_count + 1)
                self.assertEqual(recovery.exact_cover.backtracks, 0)
                self.assertEqual(recovery.exact_cover.solutions, 1)
                self.assertTrue(recovery.exact_cover.exhausted)
                self.assertTrue(recovery.matches_reference)

    def test_a029_dual_k4_recovery_is_exact(self) -> None:
        for params in G1_PARAMETER_SETS.values():
            with self.subTest(name=params.name):
                public, reference = generate_cycle_gluing_instance(params, MASTER_SEED)
                recovery = recover_cycle_by_dual_k4(public, reference)
                self.assertEqual(recovery.subset_checks, math.comb(4 * params.piece_count, 4))
                self.assertEqual(recovery.clique_candidates, params.piece_count)
                self.assertEqual(len(recovery.valid_candidates), params.piece_count)
                self.assertTrue(recovery.exact_cover.validation.valid)
                self.assertEqual(recovery.exact_cover.nodes, params.piece_count + 1)
                self.assertEqual(recovery.exact_cover.backtracks, 0)
                self.assertEqual(recovery.exact_cover.solutions, 1)
                self.assertTrue(recovery.matches_reference)

    def test_multi_seed_sweep_keeps_gate_and_both_breaks(self) -> None:
        for params in G1_PARAMETER_SETS.values():
            for seed_index in range(8):
                seed = hashlib.sha256(
                    b"MORPH-KEM G1 tests\x00"
                    + MASTER_SEED
                    + params.name.encode("ascii")
                    + seed_index.to_bytes(4, "big")
                ).digest()
                with self.subTest(name=params.name, seed=seed_index):
                    public, reference = generate_cycle_gluing_instance(params, seed)
                    structure = cycle_structure(public)
                    self.assertFalse(structure.bridges)
                    self.assertFalse(structure.articulation_vertices)
                    star = recover_cycle_by_vertex_stars(public, reference)
                    k4 = recover_cycle_by_dual_k4(public, reference)
                    self.assertTrue(star.exact_cover.validation.valid)
                    self.assertTrue(star.matches_reference)
                    self.assertTrue(k4.exact_cover.validation.valid)
                    self.assertTrue(k4.matches_reference)

    def test_invalid_witness_and_parameters_are_rejected(self) -> None:
        public, reference = generate_cycle_gluing_instance(G1_PARAMETER_SETS["g1-3"], MASTER_SEED)
        malformed = (reference.groups[0][:-1],) + reference.groups[1:]
        self.assertFalse(validate_cycle_gluing_witness(public, malformed).valid)

        with self.assertRaises(GluingExperimentError):
            CycleGluingParameters("too-small", 2).validate()
        with self.assertRaises(GluingExperimentError):
            generate_cycle_gluing_instance(G1_PARAMETER_SETS["g1-3"], b"short")


if __name__ == "__main__":
    unittest.main()
