from __future__ import annotations

import unittest

from morph_kem.gluing import GluingExperimentError
from morph_kem.gluing_exact_one import (
    G5_PARAMETER_SETS,
    ExactOneClause,
    ExactOnePublicInstance,
    _clause_triples,
    generate_exact_one_instance,
    recover_exact_one_via_parity,
    validate_exact_one_witness,
)


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


class ExactOneTests(unittest.TestCase):
    def test_templates_are_regular_connected_and_full_rank(self) -> None:
        expected_cycle_rank = {12: 37, 18: 55, 24: 73}
        for name, params in G5_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public, reference = generate_exact_one_instance(params, MASTER_SEED)
                recovery = recover_exact_one_via_parity(public, reference=reference)

                self.assertEqual(len(_clause_triples(params.gadget_count)), 2 * params.gadget_count)
                self.assertEqual(recovery.gadget_count, params.gadget_count)
                self.assertEqual(recovery.total_tetrahedra, 6 * params.gadget_count)
                self.assertEqual(recovery.clause_count, 2 * params.gadget_count)
                self.assertEqual(recovery.variable_degree_histogram, ((6, params.gadget_count),))
                self.assertEqual(recovery.factor_components, 1)
                self.assertEqual(recovery.factor_cycle_rank, expected_cycle_rank[params.gadget_count])
                self.assertEqual(recovery.gadget_matching_solutions, (2,) * params.gadget_count)
                self.assertEqual(recovery.gadget_matching_nodes, 7 * params.gadget_count)
                self.assertEqual(recovery.gadget_matching_backtracks, 0)
                self.assertEqual(recovery.projected_equations, 2 * params.gadget_count)
                self.assertEqual(recovery.projected_variables, params.gadget_count)
                self.assertEqual(recovery.gf2_rank, params.gadget_count)
                self.assertEqual(recovery.gf2_nullity, 0)
                self.assertEqual(recovery.affine_solution_count, 1)
                self.assertEqual(recovery.nonlinear_clause_checks, 2 * params.gadget_count)
                self.assertTrue(recovery.accepted)
                self.assertTrue(recovery.matches_reference)

    def test_attack_does_not_need_reference(self) -> None:
        public, _ = generate_exact_one_instance(G5_PARAMETER_SETS["g5-18"], MASTER_SEED)
        recovery = recover_exact_one_via_parity(public)
        self.assertEqual(recovery.gf2_nullity, 0)
        self.assertTrue(recovery.accepted)
        self.assertFalse(recovery.matches_reference)
        self.assertTrue(validate_exact_one_witness(public, recovery.recovered_groups).valid)

    def test_single_phase_flip_is_rejected(self) -> None:
        public, reference = generate_exact_one_instance(G5_PARAMETER_SETS["g5-12"], MASTER_SEED)
        recovery = recover_exact_one_via_parity(public, reference=reference)
        changed = list(recovery.recovered_groups)
        # Every local gadget has exactly two canonical phases.  The public attack
        # already recovered one; replace one local group by the other phase.
        from morph_kem.gluing_matching import recover_matching_gluing

        local = recover_matching_gluing(public.gadgets[0])
        changed[0] = next(groups for groups in local.accepted_groups if groups != changed[0])
        self.assertFalse(validate_exact_one_witness(public, tuple(changed)).valid)

    def test_public_relabel_and_sign_seeds_preserve_linear_break(self) -> None:
        for name, params in G5_PARAMETER_SETS.items():
            for seed_index in range(4):
                with self.subTest(name=name, seed=seed_index):
                    seed = bytes([seed_index + 17]) * 32
                    public, reference = generate_exact_one_instance(params, seed)
                    recovery = recover_exact_one_via_parity(public, reference=reference)
                    self.assertEqual(recovery.gf2_rank, params.gadget_count)
                    self.assertEqual(recovery.gf2_nullity, 0)
                    self.assertTrue(recovery.accepted)
                    self.assertTrue(recovery.matches_reference)
                    self.assertEqual(recovery.gadget_matching_backtracks, 0)

    def test_malformed_public_clause_is_rejected(self) -> None:
        public, reference = generate_exact_one_instance(G5_PARAMETER_SETS["g5-12"], MASTER_SEED)
        malformed = ExactOnePublicInstance(
            name=public.name,
            gadgets=public.gadgets,
            clauses=public.clauses + (ExactOneClause((0, 1, 99), (0, 0, 0)),),
        )
        self.assertFalse(validate_exact_one_witness(malformed, reference.groups).valid)
        with self.assertRaises(GluingExperimentError):
            recover_exact_one_via_parity(malformed)

    def test_seed_bounds(self) -> None:
        with self.assertRaises(GluingExperimentError):
            generate_exact_one_instance(G5_PARAMETER_SETS["g5-12"], b"short")


if __name__ == "__main__":
    unittest.main()
