from __future__ import annotations

import unittest

from morph_kem.gluing import GluingExperimentError
from morph_kem.gluing_sat import (
    G7_PARAMETER_SETS,
    SatClause,
    SatPublicInstance,
    generate_sat_phase_instance,
    groups_for_sat_phases,
    local_or_affine_implication_count,
    parse_minisat_model,
    recover_sat_by_dpll,
    sat_dimacs,
    validate_sat_witness,
)


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


class SatPhaseTests(unittest.TestCase):
    def test_exact_dpll_metrics(self) -> None:
        expected = {
            "g7-12": (12, 48, 85, 84, 10, False, 37, 18, 82, 9, 10, 480, 9),
            "g7-18": (18, 72, 127, 126, 16, True, 36, 20, 14, 0, 0, 1152, 15),
            "g7-24": (24, 96, 169, 168, 16, True, 40, 22, 34, 2, 2, 1536, 16),
        }
        for name, metrics in expected.items():
            with self.subTest(name=name):
                (
                    gadgets,
                    clauses,
                    cycle_rank,
                    matching_nodes,
                    solutions,
                    cap_hit,
                    nodes,
                    decisions,
                    propagations,
                    conflicts,
                    backtracks,
                    verifier_checks,
                    nonreference,
                ) = metrics
                public, reference = generate_sat_phase_instance(
                    G7_PARAMETER_SETS[name], MASTER_SEED
                )
                recovery = recover_sat_by_dpll(public, reference=reference)

                self.assertEqual(recovery.gadget_count, gadgets)
                self.assertEqual(recovery.total_tetrahedra, 6 * gadgets)
                self.assertEqual(recovery.clause_count, clauses)
                self.assertEqual(recovery.variable_degree_histogram, ((12, gadgets),))
                self.assertEqual(recovery.factor_components, 1)
                self.assertEqual(recovery.factor_cycle_rank, cycle_rank)
                self.assertEqual(recovery.local_affine_implications, 0)
                self.assertEqual(recovery.gadget_matching_solutions, (2,) * gadgets)
                self.assertEqual(recovery.gadget_matching_nodes, matching_nodes)
                self.assertEqual(recovery.gadget_matching_backtracks, 0)
                self.assertEqual(recovery.solution_cap, 16)
                self.assertEqual(recovery.solution_count, solutions)
                self.assertEqual(recovery.solution_cap_hit, cap_hit)
                self.assertEqual(recovery.dpll_nodes, nodes)
                self.assertEqual(recovery.dpll_decisions, decisions)
                self.assertEqual(recovery.dpll_propagations, propagations)
                self.assertEqual(recovery.dpll_conflicts, conflicts)
                self.assertEqual(recovery.dpll_backtracks, backtracks)
                self.assertEqual(recovery.exact_verifier_clause_checks, verifier_checks)
                self.assertEqual(recovery.accepted_solutions, solutions)
                self.assertEqual(recovery.nonreference_accepted_solutions, nonreference)
                self.assertFalse(recovery.first_solution_matches_reference)
                self.assertTrue(validate_sat_witness(public, recovery.first_groups).valid)

    def test_or_relation_has_no_nontrivial_affine_implication(self) -> None:
        self.assertEqual(local_or_affine_implication_count(), 0)

    def test_attack_does_not_need_reference(self) -> None:
        public, _ = generate_sat_phase_instance(G7_PARAMETER_SETS["g7-24"], MASTER_SEED)
        recovery = recover_sat_by_dpll(public)
        self.assertGreaterEqual(recovery.accepted_solutions, 1)
        self.assertEqual(recovery.nonreference_accepted_solutions, 0)
        self.assertFalse(recovery.first_solution_matches_reference)
        self.assertTrue(validate_sat_witness(public, recovery.first_groups).valid)

    def test_multi_seed_public_break_and_nonreference_witness(self) -> None:
        for name, params in G7_PARAMETER_SETS.items():
            for seed_index in range(8):
                with self.subTest(name=name, seed=seed_index):
                    seed = bytes([seed_index + 61]) * 32
                    public, reference = generate_sat_phase_instance(params, seed)
                    recovery = recover_sat_by_dpll(public, reference=reference)
                    self.assertEqual(recovery.local_affine_implications, 0)
                    self.assertGreaterEqual(recovery.accepted_solutions, 1)
                    self.assertGreaterEqual(recovery.nonreference_accepted_solutions, 1)
                    self.assertLess(recovery.dpll_nodes, 256)
                    self.assertEqual(recovery.gadget_matching_backtracks, 0)

    def test_dimacs_and_model_round_trip(self) -> None:
        public, reference = generate_sat_phase_instance(
            G7_PARAMETER_SETS["g7-12"], MASTER_SEED
        )
        dimacs = sat_dimacs(public)
        self.assertTrue(dimacs.startswith("p cnf 12 48\n"))
        literals = " ".join(
            str(index + 1 if phase else -(index + 1))
            for index, phase in enumerate(reference.phases)
        )
        parsed = parse_minisat_model(f"SAT\n{literals} 0\n", 12)
        self.assertEqual(parsed, reference.phases)
        groups = groups_for_sat_phases(public, parsed)
        self.assertTrue(validate_sat_witness(public, groups).valid)

    def test_malformed_public_clause_is_rejected(self) -> None:
        public, _ = generate_sat_phase_instance(G7_PARAMETER_SETS["g7-12"], MASTER_SEED)
        malformed = SatPublicInstance(
            name=public.name,
            gadgets=public.gadgets,
            clauses=public.clauses + (SatClause((0, 1, 99), (0, 0, 0)),),
        )
        with self.assertRaises(GluingExperimentError):
            recover_sat_by_dpll(malformed)

    def test_bounds(self) -> None:
        public, _ = generate_sat_phase_instance(G7_PARAMETER_SETS["g7-12"], MASTER_SEED)
        with self.assertRaises(GluingExperimentError):
            generate_sat_phase_instance(G7_PARAMETER_SETS["g7-12"], b"short")
        with self.assertRaises(GluingExperimentError):
            recover_sat_by_dpll(public, solution_cap=0)
        with self.assertRaises(GluingExperimentError):
            parse_minisat_model("UNSAT\n", 12)


if __name__ == "__main__":
    unittest.main()
