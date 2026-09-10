from __future__ import annotations

import hashlib
import unittest

from morph_kem.gluing import GluingExperimentError, gluing_incidence
from morph_kem.gluing_matching import (
    G3_PARAMETER_SETS,
    MatchingGluingParameters,
    generate_matching_gluing_instance,
    matching_reference_partition_matches,
    recover_matching_gluing,
    validate_matching_gluing_witness,
)


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


class MatchingGluingTests(unittest.TestCase):
    def test_exact_structural_metrics(self) -> None:
        expected = {
            "g3-3": (8, 19, 18, 6, 12, ((2, 6), (6, 2)), 7),
            "g3-5": (12, 31, 30, 10, 20, ((2, 10), (10, 2)), 11),
            "g3-8": (18, 49, 48, 16, 32, ((2, 16), (16, 2)), 17),
        }
        for name, params in G3_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public, reference = generate_matching_gluing_instance(params, MASTER_SEED)
                incidence = gluing_incidence(public)
                recovery = recover_matching_gluing(public, reference=reference)
                vertices, edges, faces, tetrahedra, boundary, vertex_hist, matching_nodes = expected[name]

                self.assertEqual(
                    (incidence.vertices, incidence.edges, incidence.faces, incidence.tetrahedra),
                    (vertices, edges, faces, tetrahedra),
                )
                self.assertEqual(incidence.euler_characteristic, 1)
                self.assertEqual(incidence.boundary_faces, boundary)
                self.assertEqual(incidence.max_face_incidence, 2)
                self.assertEqual(recovery.dual_edges, 2 * params.piece_count)
                self.assertEqual(recovery.dual_degree_histogram, ((2, 2 * params.piece_count),))
                self.assertEqual(recovery.bridge_count, 0)
                self.assertEqual(recovery.articulation_points, ())
                self.assertEqual(recovery.allowed_candidate_edges, 2 * params.piece_count)
                self.assertEqual(recovery.vertex_star_candidate_pairs, 2 * params.piece_count)
                self.assertEqual(recovery.vertex_tetrahedron_degree_histogram, vertex_hist)
                self.assertEqual(recovery.matching_solutions, 2)
                self.assertEqual(recovery.accepted_solutions, 2)
                self.assertEqual(recovery.nonreference_accepted_solutions, 1)
                self.assertFalse(recovery.matching_cap_hit)
                self.assertEqual(recovery.matching_nodes, matching_nodes)
                self.assertEqual(recovery.matching_backtracks, 0)
                self.assertEqual(recovery.face_occurrences, 8 * params.piece_count)

    def test_both_alternating_matchings_are_valid(self) -> None:
        params = G3_PARAMETER_SETS["g3-8"]
        public, reference = generate_matching_gluing_instance(params, MASTER_SEED)
        recovery = recover_matching_gluing(public, reference=reference)

        self.assertEqual(len(recovery.accepted_groups), 2)
        validations = [
            validate_matching_gluing_witness(public, groups)
            for groups in recovery.accepted_groups
        ]
        self.assertTrue(all(validation.valid for validation in validations))
        self.assertEqual(
            sum(
                matching_reference_partition_matches(reference, groups)
                for groups in recovery.accepted_groups
            ),
            1,
        )

    def test_recovery_is_stable_under_public_relabeling(self) -> None:
        for name, params in G3_PARAMETER_SETS.items():
            for seed_index in range(8):
                with self.subTest(name=name, seed=seed_index):
                    seed = hashlib.sha256(
                        b"MORPH-KEM G3 tests v1\x00"
                        + MASTER_SEED
                        + name.encode("ascii")
                        + seed_index.to_bytes(4, "big")
                    ).digest()
                    public, reference = generate_matching_gluing_instance(params, seed)
                    recovery = recover_matching_gluing(public, reference=reference)
                    self.assertEqual(recovery.bridge_count, 0)
                    self.assertEqual(recovery.articulation_points, ())
                    self.assertEqual(recovery.allowed_candidate_edges, 2 * params.piece_count)
                    self.assertEqual(recovery.accepted_solutions, 2)
                    self.assertEqual(recovery.nonreference_accepted_solutions, 1)
                    self.assertEqual(recovery.matching_backtracks, 0)

    def test_invalid_partition_is_rejected(self) -> None:
        params = G3_PARAMETER_SETS["g3-5"]
        public, reference = generate_matching_gluing_instance(params, MASTER_SEED)
        groups = list(reference.groups)
        left = list(groups[0])
        right = list(groups[1])
        left[0], right[0] = right[0], left[0]
        groups[0] = tuple(left)
        groups[1] = tuple(right)
        validation = validate_matching_gluing_witness(public, tuple(groups))
        self.assertFalse(validation.valid)

    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(GluingExperimentError):
            MatchingGluingParameters("tiny", 2).validate()
        with self.assertRaises(GluingExperimentError):
            MatchingGluingParameters("large", 33).validate()
        with self.assertRaises(GluingExperimentError):
            generate_matching_gluing_instance(G3_PARAMETER_SETS["g3-3"], b"short")

    def test_solution_cap_bounds(self) -> None:
        public, reference = generate_matching_gluing_instance(
            G3_PARAMETER_SETS["g3-3"], MASTER_SEED
        )
        with self.assertRaises(GluingExperimentError):
            recover_matching_gluing(public, reference=reference, solution_cap=0)
        with self.assertRaises(GluingExperimentError):
            recover_matching_gluing(public, reference=reference, solution_cap=1025)

        capped = recover_matching_gluing(public, reference=reference, solution_cap=1)
        self.assertEqual(capped.matching_solutions, 1)
        self.assertEqual(capped.accepted_solutions, 1)
        self.assertTrue(capped.matching_cap_hit)


if __name__ == "__main__":
    unittest.main()
