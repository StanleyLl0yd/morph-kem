from __future__ import annotations

from math import comb
import unittest

from morph_kem.gluing import GluingExperimentError, gluing_incidence
from morph_kem.gluing_overlap import (
    G9_PARAMETER_SETS,
    OverlapGluingParameters,
    generate_overlap_gluing_instance,
    overlap_reference_partition_matches,
    recover_overlap_gluing,
    validate_overlap_gluing_witness,
)


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


class OverlapGluingTests(unittest.TestCase):
    def test_exact_structural_metrics_and_candidate_overlap(self) -> None:
        for name, params in G9_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public, reference = generate_overlap_gluing_instance(params, MASTER_SEED)
                incidence = gluing_incidence(public)
                recovery = recover_overlap_gluing(public, reference=reference)
                t = params.tetrahedron_count

                self.assertEqual(
                    (incidence.vertices, incidence.edges, incidence.faces, incidence.tetrahedra),
                    (t + 2, 3 * t + 1, 3 * t, t),
                )
                self.assertEqual(incidence.euler_characteristic, 1)
                self.assertEqual(incidence.boundary_faces, 2 * t)
                self.assertEqual(incidence.max_face_incidence, 2)
                self.assertEqual(recovery.dual_edges, t)
                self.assertEqual(recovery.dual_degree_histogram, ((2, t),))
                self.assertEqual(recovery.bridge_count, 0)
                self.assertEqual(recovery.articulation_points, ())
                self.assertEqual(recovery.d2_candidates, t)
                self.assertEqual(recovery.d3_candidates, t)
                self.assertEqual(recovery.membership_histogram, ((5, t),))
                self.assertEqual(recovery.overlap_degree_histogram, ((6, t), (8, t)))
                self.assertEqual(recovery.candidate_incidence_size, 5 * t)
                self.assertEqual(recovery.face_occurrences, 4 * t)
                self.assertTrue(validate_overlap_gluing_witness(public, reference.groups).valid)

    def test_a036_enumerates_all_cycle_tilings(self) -> None:
        for name, params in G9_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public, reference = generate_overlap_gluing_instance(params, MASTER_SEED)
                recovery = recover_overlap_gluing(public, reference=reference)
                expected = (
                    params.tetrahedron_count * comb(params.piece_count, params.d2_count)
                    // params.piece_count
                )

                self.assertEqual(recovery.exact_cover_solutions, expected)
                self.assertFalse(recovery.exact_cover_cap_hit)
                self.assertEqual(recovery.cycle_dp_tilings, expected)
                self.assertEqual(recovery.accepted_solutions, expected)
                self.assertEqual(recovery.nonreference_accepted_solutions, expected - 1)
                self.assertGreater(recovery.exact_cover_nodes, recovery.accepted_solutions)
                self.assertGreater(recovery.cycle_dp_states, 0)
                self.assertGreater(recovery.cycle_dp_transition_checks, 0)
                self.assertTrue(
                    any(
                        overlap_reference_partition_matches(reference, groups)
                        for groups in recovery.accepted_groups
                    )
                )

    def test_attack_does_not_need_reference(self) -> None:
        public, _ = generate_overlap_gluing_instance(G9_PARAMETER_SETS["g9-30"], MASTER_SEED)
        recovery = recover_overlap_gluing(public)
        self.assertEqual(recovery.exact_cover_solutions, 450)
        self.assertEqual(recovery.accepted_solutions, 450)
        self.assertEqual(recovery.nonreference_accepted_solutions, 0)

    def test_break_is_stable_under_public_relabeling(self) -> None:
        for name, params in G9_PARAMETER_SETS.items():
            expected = params.tetrahedron_count * comb(params.piece_count, params.d2_count) // params.piece_count
            for seed_index in range(4):
                with self.subTest(name=name, seed=seed_index):
                    seed = bytes([seed_index + 1]) * 32
                    public, reference = generate_overlap_gluing_instance(params, seed)
                    recovery = recover_overlap_gluing(public, reference=reference)
                    self.assertEqual(recovery.d2_candidates, params.tetrahedron_count)
                    self.assertEqual(recovery.d3_candidates, params.tetrahedron_count)
                    self.assertEqual(recovery.exact_cover_solutions, expected)
                    self.assertEqual(recovery.cycle_dp_tilings, expected)
                    self.assertEqual(recovery.accepted_solutions, expected)
                    self.assertEqual(recovery.nonreference_accepted_solutions, expected - 1)

    def test_invalid_partition_is_rejected(self) -> None:
        public, reference = generate_overlap_gluing_instance(G9_PARAMETER_SETS["g9-18"], MASTER_SEED)
        changed = list(reference.groups)
        changed[0] = changed[0][:-1]
        self.assertFalse(validate_overlap_gluing_witness(public, tuple(changed)).valid)

    def test_parameter_seed_and_cap_bounds(self) -> None:
        with self.assertRaises(GluingExperimentError):
            OverlapGluingParameters("odd", 17, 7).validate()
        with self.assertRaises(GluingExperimentError):
            OverlapGluingParameters("one-type", 18, 9).validate()
        with self.assertRaises(GluingExperimentError):
            generate_overlap_gluing_instance(G9_PARAMETER_SETS["g9-18"], b"short")
        public, _ = generate_overlap_gluing_instance(G9_PARAMETER_SETS["g9-18"], MASTER_SEED)
        with self.assertRaises(GluingExperimentError):
            recover_overlap_gluing(public, solution_cap=0)


if __name__ == "__main__":
    unittest.main()
