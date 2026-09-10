from __future__ import annotations

from itertools import islice, product
import json
import unittest

from morph_kem.gluing import GluingExperimentError
from morph_kem.gluing_coupled import G4_PARAMETER_SETS, generate_coupled_phase_instance
from morph_kem.gluing_exact_one import G5_PARAMETER_SETS, generate_exact_one_instance
from morph_kem.gluing_phase_csp import (
    CompiledPhaseCSP,
    RelationConstraint,
    compile_g4,
    compile_g5,
    compile_g6,
    compile_g7,
    compiled_accepts,
    lift_assignment,
    original_accepts,
    semantic_equivalence_audit,
    serialize_compiled_csp,
    solve_compiled_csp,
)
from morph_kem.gluing_residual import G6_PARAMETER_SETS, generate_residual_exact_one_instance
from morph_kem.gluing_sat import G7_PARAMETER_SETS, generate_sat_phase_instance


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


class PhaseCSPCollapseTests(unittest.TestCase):
    def _small_instances(self):
        g4_public, g4_reference = generate_coupled_phase_instance(
            G4_PARAMETER_SETS["g4-4"], MASTER_SEED
        )
        g5_public, g5_reference = generate_exact_one_instance(
            G5_PARAMETER_SETS["g5-12"], MASTER_SEED
        )
        g6_public, g6_reference = generate_residual_exact_one_instance(
            G6_PARAMETER_SETS["g6-12"], MASTER_SEED
        )
        g7_public, g7_reference = generate_sat_phase_instance(
            G7_PARAMETER_SETS["g7-12"], MASTER_SEED
        )
        return (
            ("G4", g4_public, g4_reference, compile_g4(g4_public), 2),
            ("G5", g5_public, g5_reference, compile_g5(g5_public), 3),
            ("G6", g6_public, g6_reference, compile_g6(g6_public), 3),
            ("G7", g7_public, g7_reference, compile_g7(g7_public), 7),
        )

    def test_compiled_representation_contains_only_finite_domain_relations(self) -> None:
        for family, _, _, compiled, allowed_size in self._small_instances():
            with self.subTest(family=family):
                self.assertTrue(all(size == 2 for size in compiled.csp.domain_sizes))
                self.assertTrue(compiled.csp.constraints)
                self.assertTrue(
                    all(len(relation.allowed) == allowed_size for relation in compiled.csp.constraints)
                )
                serialized = serialize_compiled_csp(compiled.csp)
                decoded = json.loads(serialized)
                self.assertEqual(decoded["family"], family)
                self.assertEqual(len(decoded["domain_sizes"]), len(compiled.csp.domain_sizes))
                lowered = serialized.lower()
                for forbidden in ("tetra", "face", "vertex", "simplic", "group"):
                    self.assertNotIn(forbidden, lowered)
                self.assertGreater(compiled.lift.topological_tetrahedra, 0)
                self.assertEqual(compiled.lift.extraction_backtracks, 0)

    def test_generic_solver_solutions_lift_to_original_verifiers(self) -> None:
        for family, public, reference, compiled, _ in self._small_instances():
            with self.subTest(family=family):
                recovery = solve_compiled_csp(compiled.csp, solution_cap=16)
                self.assertGreaterEqual(recovery.solution_count, 1)
                for assignment in recovery.assignments:
                    self.assertTrue(compiled_accepts(compiled.csp, assignment))
                    groups = lift_assignment(compiled.lift, assignment)
                    self.assertTrue(original_accepts(family, public, groups))
                self.assertIn(reference.phases, tuple(product(*(range(size) for size in compiled.csp.domain_sizes))))
                self.assertTrue(compiled_accepts(compiled.csp, reference.phases))

    def test_g4_exhaustive_semantic_equivalence(self) -> None:
        public, _ = generate_coupled_phase_instance(G4_PARAMETER_SETS["g4-4"], MASTER_SEED)
        compiled = compile_g4(public)
        audit = semantic_equivalence_audit("G4", public, compiled)
        self.assertEqual(audit.assignments_checked, 16)
        self.assertEqual(audit.compiled_accepts, 2)
        self.assertEqual(audit.original_accepts, 2)
        self.assertEqual(audit.mismatches, 0)

    def test_sampled_semantic_equivalence_for_ternary_families(self) -> None:
        for family, public, reference, compiled, _ in self._small_instances()[1:]:
            assignments = list(islice(product(*(range(size) for size in compiled.csp.domain_sizes)), 32))
            assignments.append(reference.phases)
            for assignment in assignments:
                with self.subTest(family=family, assignment=assignment):
                    phase_assignment = tuple(assignment)
                    groups = lift_assignment(compiled.lift, phase_assignment)
                    self.assertEqual(
                        compiled_accepts(compiled.csp, phase_assignment),
                        original_accepts(family, public, groups),
                    )

    def test_malformed_compiled_inputs_are_rejected(self) -> None:
        malformed = CompiledPhaseCSP(
            family="bad",
            domain_sizes=(2, 2),
            constraints=(RelationConstraint(scope=(0, 1), allowed=((0, 2),)),),
        )
        with self.assertRaises(GluingExperimentError):
            solve_compiled_csp(malformed)

        public, _ = generate_coupled_phase_instance(G4_PARAMETER_SETS["g4-4"], MASTER_SEED)
        compiled = compile_g4(public)
        self.assertFalse(compiled_accepts(compiled.csp, (0,)))
        with self.assertRaises(GluingExperimentError):
            lift_assignment(compiled.lift, (0,))
        with self.assertRaises(GluingExperimentError):
            solve_compiled_csp(compiled.csp, solution_cap=0)


if __name__ == "__main__":
    unittest.main()
