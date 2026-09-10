from __future__ import annotations

import hashlib
import math
import unittest

from morph_kem.gluing import GluingExperimentError, gluing_incidence, recover_gluing_by_dual_bridges
from morph_kem.gluing_cycle import (
    G1_PARAMETER_SETS,
    CycleGluingParameters,
    cycle_reference_partition_matches,
    generate_cycle_gluing_instance,
    recover_cycle_gluing_by_k4_exact_cover,
    validate_cycle_gluing_witness,
)


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


class CycleGluingTests(unittest.TestCase):
    def test_exact_structural_metrics(self) -> None:
        for name in ("g1-4", "g1-8", "g1-12"):
            with self.subTest(name=name):
                params = G1_PARAMETER_SETS[name]
                public, reference = generate_cycle_gluing_instance(params, MASTER_SEED)
                incidence = gluing_incidence(public)
                n = params.piece_count

                self.assertEqual(incidence.vertices, 2 * n + 2)
                self.assertEqual(incidence.edges, 7 * n + 1)
                self.assertEqual(incidence.faces, 9 * n)
                self.assertEqual(incidence.tetrahedra, 4 * n)
                self.assertEqual(incidence.boundary_faces, 2 * n)
                self.assertEqual(incidence.max_face_incidence, 2)
                self.assertEqual(incidence.euler_characteristic, 1)
                self.assertEqual(incidence.dual_edges, 7 * n)
                self.assertTrue(validate_cycle_gluing_witness(public, reference.groups).valid)

    def test_a024_disappears_and_a028_recovers_exact_partition(self) -> None:
        for name in ("g1-4", "g1-8", "g1-12"):
            with self.subTest(name=name):
                params = G1_PARAMETER_SETS[name]
                public, reference = generate_cycle_gluing_instance(params, MASTER_SEED)
                n = params.piece_count

                bridge_recovery = recover_gluing_by_dual_bridges(public)
                self.assertEqual(bridge_recovery.bridges, ())
                self.assertFalse(validate_cycle_gluing_witness(public, bridge_recovery.groups).valid)

                recovery = recover_cycle_gluing_by_k4_exact_cover(public)
                self.assertEqual(recovery.bridge_count, 0)
                self.assertEqual(recovery.articulation_points, ())
                self.assertEqual(recovery.two_vertex_separator_pairs, 2 * n * (n - 1))
                self.assertEqual(recovery.dual_edges, 7 * n)
                self.assertEqual(recovery.face_occurrences, 16 * n)
                self.assertEqual(recovery.four_subsets_tested, math.comb(4 * n, 4))
                self.assertEqual(recovery.dual_k4_candidates, n)
                self.assertEqual(recovery.allowed_piece_candidates, n)
                self.assertEqual(recovery.exact_cover_solutions, 1)
                self.assertFalse(recovery.exact_cover_cap_hit)
                self.assertEqual(recovery.exact_cover_nodes, n + 1)
                self.assertEqual(recovery.exact_cover_backtracks, 0)
                self.assertTrue(recovery.validation.valid)
                self.assertTrue(cycle_reference_partition_matches(reference, recovery.groups))

    def test_recovery_is_stable_under_public_relabeling(self) -> None:
        params = G1_PARAMETER_SETS["g1-12"]
        for seed_index in range(8):
            with self.subTest(seed_index=seed_index):
                seed = hashlib.sha256(
                    b"MORPH-KEM G1 relabel regression/" + seed_index.to_bytes(4, "big")
                ).digest()
                public, reference = generate_cycle_gluing_instance(params, seed)
                recovery = recover_cycle_gluing_by_k4_exact_cover(public)

                self.assertTrue(recovery.validation.valid)
                self.assertEqual(recovery.bridge_count, 0)
                self.assertEqual(recovery.articulation_points, ())
                self.assertEqual(recovery.dual_k4_candidates, params.piece_count)
                self.assertEqual(recovery.allowed_piece_candidates, params.piece_count)
                self.assertEqual(recovery.exact_cover_solutions, 1)
                self.assertTrue(cycle_reference_partition_matches(reference, recovery.groups))

    def test_invalid_partition_is_rejected(self) -> None:
        public, reference = generate_cycle_gluing_instance(
            G1_PARAMETER_SETS["g1-4"],
            MASTER_SEED,
        )
        groups = list(reference.groups)
        first = list(groups[0])
        second = list(groups[1])
        first[0], second[0] = second[0], first[0]
        groups[0] = tuple(first)
        groups[1] = tuple(second)

        validation = validate_cycle_gluing_witness(public, tuple(groups))
        self.assertFalse(validation.valid)

    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(GluingExperimentError):
            CycleGluingParameters("too-small", 3).validate()
        with self.assertRaises(GluingExperimentError):
            CycleGluingParameters("too-large", 17).validate()
        with self.assertRaises(GluingExperimentError):
            generate_cycle_gluing_instance(G1_PARAMETER_SETS["g1-4"], b"short")

    def test_solution_cap_bounds(self) -> None:
        public, _ = generate_cycle_gluing_instance(G1_PARAMETER_SETS["g1-4"], MASTER_SEED)
        with self.assertRaises(GluingExperimentError):
            recover_cycle_gluing_by_k4_exact_cover(public, solution_cap=0)
        with self.assertRaises(GluingExperimentError):
            recover_cycle_gluing_by_k4_exact_cover(public, solution_cap=1025)


if __name__ == "__main__":
    unittest.main()
