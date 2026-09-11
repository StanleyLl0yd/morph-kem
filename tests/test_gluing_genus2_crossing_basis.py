from __future__ import annotations

import unittest

from morph_kem.gluing import GluingExperimentError
from morph_kem.gluing_genus2_crossing_basis import (
    G21_PARAMETER_SETS,
    GenusTwoCrossingBasisParameters,
    GenusTwoCrossingBasisWitness,
    generate_genus2_crossing_basis_instance,
    recover_genus2_crossing_basis,
    validate_genus2_crossing_basis_witness,
)
from morph_kem.gluing_symplectic_cycle_pair import (
    _dual_data,
    _pair_from_leftover,
    _tree_cotree_data,
)
from morph_kem.gluing_cohomology_cycle import _edges


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")
IDENTITY4 = (
    (1, 0, 0, 0),
    (0, 1, 0, 0),
    (0, 0, 1, 0),
    (0, 0, 0, 1),
)


class GenusTwoCrossingBasisTests(unittest.TestCase):
    def test_structural_metrics_and_public_treecotree_break(self) -> None:
        for name, params in G21_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public = generate_genus2_crossing_basis_instance(params, MASTER_SEED)
                recovery = recover_genus2_crossing_basis(
                    public, successful_flips=params.successful_flips
                )
                cells = params.rows * params.cols
                self.assertEqual(recovery.vertices, 2 * cells - 3)
                self.assertEqual(recovery.edges, 6 * cells - 3)
                self.assertEqual(recovery.triangles, 4 * cells - 2)
                self.assertEqual(recovery.euler_characteristic, -2)
                self.assertEqual(recovery.min_triangles_per_edge, 2)
                self.assertEqual(recovery.max_triangles_per_edge, 2)
                self.assertEqual(recovery.h1_dimension, 4)
                self.assertEqual(recovery.primal_tree_edges, recovery.vertices - 1)
                self.assertEqual(recovery.dual_cotree_edges, recovery.triangles - 1)
                self.assertEqual(recovery.forbidden_dual_edges, recovery.vertices - 1)
                self.assertEqual(recovery.leftover_edges, 4)
                self.assertEqual(recovery.exact_crossing_matrix, IDENTITY4)
                self.assertEqual(recovery.off_diagonal_nonzero, 0)
                self.assertTrue(recovery.exact_verifier_accepted)
                self.assertEqual(recovery.full_crossing_matrix_rank, 4)
                self.assertEqual(recovery.full_crossing_matrix_rows, recovery.full_primal_cycles)
                self.assertEqual(recovery.full_crossing_matrix_cols, recovery.full_dual_cycles)

    def test_attack_uses_only_public_carrier(self) -> None:
        public = generate_genus2_crossing_basis_instance(
            G21_PARAMETER_SETS["g21-6x6"], MASTER_SEED
        )
        recovery = recover_genus2_crossing_basis(public)
        self.assertTrue(recovery.exact_verifier_accepted)
        self.assertEqual(recovery.exact_crossing_matrix, IDENTITY4)
        self.assertEqual(recovery.off_diagonal_nonzero, 0)

    def test_swapping_dual_roles_breaks_exact_identity_verifier(self) -> None:
        public = generate_genus2_crossing_basis_instance(
            G21_PARAMETER_SETS["g21-4x4"], MASTER_SEED
        )
        primal_edges = _edges(public.target)
        dual = _dual_data(public.target, primal_edges)
        primal_tree, dual_tree, leftovers = _tree_cotree_data(
            len(public.target.vertices), primal_edges, len(dual.triangles), dual.dual_edges
        )
        pairs = tuple(
            _pair_from_leftover(
                leftover, primal_edges, dual.dual_edges, primal_tree, dual_tree
            )[0]
            for leftover in leftovers
        )
        good = GenusTwoCrossingBasisWitness(
            tuple(pair.primal_cycle for pair in pairs),
            tuple(pair.dual_cycle for pair in pairs),
        )
        self.assertTrue(validate_genus2_crossing_basis_witness(public, good).valid)
        dual_cycles = list(good.dual_cycles)
        dual_cycles[0], dual_cycles[1] = dual_cycles[1], dual_cycles[0]
        bad = GenusTwoCrossingBasisWitness(good.primal_cycles, tuple(dual_cycles))
        validation = validate_genus2_crossing_basis_witness(public, bad)
        self.assertFalse(validation.valid)
        self.assertNotEqual(validation.crossing_matrix, IDENTITY4)

    def test_break_is_stable_under_public_relabeling(self) -> None:
        for name, params in G21_PARAMETER_SETS.items():
            for seed_index in range(4):
                with self.subTest(name=name, seed=seed_index):
                    seed = bytes([seed_index + 1]) * 32
                    public = generate_genus2_crossing_basis_instance(params, seed)
                    recovery = recover_genus2_crossing_basis(public)
                    self.assertEqual(recovery.leftover_edges, 4)
                    self.assertEqual(recovery.exact_crossing_matrix, IDENTITY4)
                    self.assertEqual(recovery.off_diagonal_nonzero, 0)
                    self.assertTrue(recovery.exact_verifier_accepted)
                    self.assertEqual(recovery.full_crossing_matrix_rank, 4)

    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(GluingExperimentError):
            GenusTwoCrossingBasisParameters("small", 3, 6, 10).validate()
        with self.assertRaises(GluingExperimentError):
            GenusTwoCrossingBasisParameters("flips", 4, 4, 0).validate()
        with self.assertRaises(GluingExperimentError):
            generate_genus2_crossing_basis_instance(
                G21_PARAMETER_SETS["g21-4x4"], b"short"
            )


if __name__ == "__main__":
    unittest.main()
