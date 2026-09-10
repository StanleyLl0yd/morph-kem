from __future__ import annotations

import unittest

from morph_kem.gluing import GluingExperimentError
from morph_kem.gluing_exact_one import ExactOneClause, ExactOnePublicInstance, validate_exact_one_witness
from morph_kem.gluing_residual import (
    G6_PARAMETER_SETS,
    _residual_clause_triples,
    generate_residual_exact_one_instance,
    recover_residual_exact_one,
)


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


class ResidualExactOneTests(unittest.TestCase):
    def test_residual_affine_metrics_and_recovery(self) -> None:
        expected = {
            "g6-12": (12, 24, 37, 10, 2, 92, 84, 96, 24),
            "g6-18": (18, 36, 55, 16, 2, 188, 126, 144, 36),
            "g6-24": (24, 48, 73, 22, 2, 308, 168, 192, 48),
        }
        for name, metrics in expected.items():
            with self.subTest(name=name):
                gadgets, clauses, cycle_rank, rank, nullity, row_xors, matching_nodes, residual_checks, verifier_checks = metrics
                public, reference = generate_residual_exact_one_instance(
                    G6_PARAMETER_SETS[name], MASTER_SEED
                )
                recovery = recover_residual_exact_one(public, reference=reference)

                self.assertEqual(len(_residual_clause_triples(gadgets)), clauses)
                self.assertEqual(recovery.gadget_count, gadgets)
                self.assertEqual(recovery.total_tetrahedra, 6 * gadgets)
                self.assertEqual(recovery.clause_count, clauses)
                self.assertEqual(recovery.variable_degree_histogram, ((6, gadgets),))
                self.assertEqual(recovery.factor_components, 1)
                self.assertEqual(recovery.factor_cycle_rank, cycle_rank)
                self.assertEqual(recovery.gadget_matching_solutions, (2,) * gadgets)
                self.assertEqual(recovery.gadget_matching_nodes, matching_nodes)
                self.assertEqual(recovery.gadget_matching_backtracks, 0)
                self.assertEqual(recovery.projected_equations, clauses)
                self.assertEqual(recovery.projected_variables, gadgets)
                self.assertEqual(recovery.gf2_rank, rank)
                self.assertEqual(recovery.gf2_nullity, nullity)
                self.assertEqual(recovery.gf2_row_xors, row_xors)
                self.assertEqual(recovery.affine_candidate_count, 4)
                self.assertEqual(recovery.residual_clause_checks, residual_checks)
                self.assertEqual(recovery.accepted_candidate_count, 1)
                self.assertEqual(recovery.exact_verifier_clause_checks, verifier_checks)
                self.assertEqual(recovery.nonreference_accepted_candidates, 0)
                self.assertTrue(recovery.first_accepted_matches_reference)
                self.assertTrue(
                    validate_exact_one_witness(public, recovery.recovered_groups).valid
                )

    def test_attack_does_not_need_reference(self) -> None:
        public, _ = generate_residual_exact_one_instance(
            G6_PARAMETER_SETS["g6-18"], MASTER_SEED
        )
        recovery = recover_residual_exact_one(public)
        self.assertEqual(recovery.gf2_nullity, 2)
        self.assertEqual(recovery.affine_candidate_count, 4)
        self.assertEqual(recovery.accepted_candidate_count, 1)
        self.assertEqual(recovery.nonreference_accepted_candidates, 0)
        self.assertFalse(recovery.first_accepted_matches_reference)
        self.assertTrue(validate_exact_one_witness(public, recovery.recovered_groups).valid)

    def test_seeded_sweep_keeps_constant_residual_and_public_break(self) -> None:
        for name, params in G6_PARAMETER_SETS.items():
            for seed_index in range(8):
                with self.subTest(name=name, seed=seed_index):
                    seed = bytes([seed_index + 41]) * 32
                    public, reference = generate_residual_exact_one_instance(params, seed)
                    recovery = recover_residual_exact_one(public, reference=reference)
                    self.assertEqual(recovery.gf2_rank, params.gadget_count - 2)
                    self.assertEqual(recovery.gf2_nullity, 2)
                    self.assertEqual(recovery.affine_candidate_count, 4)
                    self.assertEqual(recovery.accepted_candidate_count, 1)
                    self.assertEqual(recovery.nonreference_accepted_candidates, 0)
                    self.assertTrue(recovery.first_accepted_matches_reference)
                    self.assertEqual(recovery.gadget_matching_backtracks, 0)

    def test_malformed_public_clause_is_rejected(self) -> None:
        public, _ = generate_residual_exact_one_instance(
            G6_PARAMETER_SETS["g6-12"], MASTER_SEED
        )
        malformed = ExactOnePublicInstance(
            name=public.name,
            gadgets=public.gadgets,
            clauses=public.clauses + (ExactOneClause((0, 1, 99), (0, 0, 0)),),
        )
        with self.assertRaises(GluingExperimentError):
            recover_residual_exact_one(malformed)

    def test_seed_bounds(self) -> None:
        with self.assertRaises(GluingExperimentError):
            generate_residual_exact_one_instance(G6_PARAMETER_SETS["g6-12"], b"short")


if __name__ == "__main__":
    unittest.main()
