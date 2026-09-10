from __future__ import annotations

import unittest

from morph_kem.gluing import GluingExperimentError, _normalize_groups
from morph_kem.gluing_coupled import (
    G4_PARAMETER_SETS,
    CoupledPhaseParameters,
    CoupledPhasePublicInstance,
    PhaseConstraint,
    generate_coupled_phase_instance,
    recover_coupled_phases,
    validate_coupled_phase_witness,
)
from morph_kem.gluing_matching import recover_matching_gluing


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


class CoupledPhaseTests(unittest.TestCase):
    def test_exact_parity_metrics(self) -> None:
        expected = {
            "g4-4": (4, 6, 3, 3, 1, 10, 28, 6, 12),
            "g4-8": (8, 12, 5, 7, 1, 38, 56, 14, 24),
            "g4-12": (12, 18, 7, 11, 1, 72, 84, 22, 36),
        }
        for name, metrics in expected.items():
            with self.subTest(name=name):
                gadgets, edges, cycle_rank, rank, nullity, row_xors, matching_nodes, assignments, checks = metrics
                public, reference = generate_coupled_phase_instance(
                    G4_PARAMETER_SETS[name], MASTER_SEED
                )
                recovery = recover_coupled_phases(public, reference=reference)
                validation = validate_coupled_phase_witness(public, reference.groups)

                self.assertTrue(validation.valid)
                self.assertEqual(recovery.gadget_count, gadgets)
                self.assertEqual(recovery.total_tetrahedra, 6 * gadgets)
                self.assertEqual(recovery.coupling_edges, edges)
                self.assertEqual(recovery.coupling_cycle_rank, cycle_rank)
                self.assertEqual(recovery.gadget_matching_solutions, (2,) * gadgets)
                self.assertEqual(recovery.gadget_matching_nodes, matching_nodes)
                self.assertEqual(recovery.gadget_matching_backtracks, 0)
                self.assertEqual(recovery.xor_equations, edges)
                self.assertEqual(recovery.xor_variables, gadgets)
                self.assertEqual(recovery.gf2_rank, rank)
                self.assertEqual(recovery.gf2_nullity, nullity)
                self.assertEqual(recovery.gf2_row_xors, row_xors)
                self.assertEqual(recovery.propagation_tree_assignments, assignments)
                self.assertEqual(recovery.propagation_constraint_checks, checks)
                self.assertEqual(recovery.phase_solutions, 2)
                self.assertEqual(recovery.accepted_solutions, 2)
                self.assertEqual(recovery.nonreference_accepted_solutions, 1)
                self.assertEqual(
                    recovery.recovered_phases[1],
                    tuple(bit ^ 1 for bit in recovery.recovered_phases[0]),
                )

    def test_attack_does_not_need_reference(self) -> None:
        public, _ = generate_coupled_phase_instance(G4_PARAMETER_SETS["g4-8"], MASTER_SEED)
        recovery = recover_coupled_phases(public)
        self.assertEqual(recovery.accepted_solutions, 2)
        self.assertEqual(recovery.nonreference_accepted_solutions, 0)
        self.assertTrue(
            all(
                validate_coupled_phase_witness(public, groups).valid
                for groups in recovery.recovered_groups
            )
        )

    def test_single_local_phase_flip_is_rejected(self) -> None:
        public, reference = generate_coupled_phase_instance(
            G4_PARAMETER_SETS["g4-4"], MASTER_SEED
        )
        changed = list(reference.groups)
        local = recover_matching_gluing(public.gadgets[0])
        reference_local = _normalize_groups(reference.groups[0])
        changed[0] = next(
            groups
            for groups in local.accepted_groups
            if _normalize_groups(groups) != reference_local
        )
        self.assertFalse(validate_coupled_phase_witness(public, tuple(changed)).valid)

    def test_public_relabel_seeds_preserve_break(self) -> None:
        for name, params in G4_PARAMETER_SETS.items():
            for seed_index in range(4):
                with self.subTest(name=name, seed=seed_index):
                    seed = bytes([seed_index + 1]) * 32
                    public, reference = generate_coupled_phase_instance(params, seed)
                    recovery = recover_coupled_phases(public, reference=reference)
                    self.assertEqual(recovery.gf2_rank, params.gadget_count - 1)
                    self.assertEqual(recovery.gf2_nullity, 1)
                    self.assertEqual(recovery.phase_solutions, 2)
                    self.assertEqual(recovery.accepted_solutions, 2)
                    self.assertEqual(recovery.nonreference_accepted_solutions, 1)
                    self.assertEqual(recovery.gadget_matching_backtracks, 0)

    def test_malformed_public_constraint_is_rejected(self) -> None:
        public, reference = generate_coupled_phase_instance(
            G4_PARAMETER_SETS["g4-4"], MASTER_SEED
        )
        malformed = CoupledPhasePublicInstance(
            name=public.name,
            gadgets=public.gadgets,
            constraints=public.constraints + (PhaseConstraint(0, 99, 1),),
        )
        self.assertFalse(
            validate_coupled_phase_witness(malformed, reference.groups).valid
        )
        with self.assertRaises(GluingExperimentError):
            recover_coupled_phases(malformed)

    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(GluingExperimentError):
            CoupledPhaseParameters("too-small", 1, ()).validate()
        with self.assertRaises(GluingExperimentError):
            CoupledPhaseParameters("disconnected", 4, ((0, 1), (2, 3))).validate()
        with self.assertRaises(GluingExperimentError):
            CoupledPhaseParameters("duplicate", 3, ((0, 1), (1, 0), (1, 2))).validate()
        with self.assertRaises(GluingExperimentError):
            generate_coupled_phase_instance(G4_PARAMETER_SETS["g4-4"], b"short")


if __name__ == "__main__":
    unittest.main()
