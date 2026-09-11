from __future__ import annotations

import hashlib
import unittest

from morph_kem.gluing import GluingExperimentError
from morph_kem.gluing_symplectic_cycle_pair import (
    G17_PARAMETER_SETS,
    SymplecticCyclePairParameters,
    SymplecticCyclePairWitness,
    generate_symplectic_cycle_pair_instance,
    recover_symplectic_cycle_pair,
    validate_symplectic_cycle_pair_witness,
)


class SymplecticCyclePairTests(unittest.TestCase):
    def test_tree_cotree_break_and_full_basis_rank(self) -> None:
        expected = {
            "g17-6x6": (36, 108, 72, 73, 37),
            "g17-6x9": (54, 162, 108, 109, 55),
            "g17-8x9": (72, 216, 144, 145, 73),
        }
        seed = bytes.fromhex("44" * 32)
        for name, params in G17_PARAMETER_SETS.items():
            with self.subTest(params=name):
                public, reference = generate_symplectic_cycle_pair_instance(params, seed)
                recovery = recover_symplectic_cycle_pair(
                    public, reference=reference, successful_flips=params.successful_flips
                )
                vertices, edges, triangles, primal_cycles, dual_cycles = expected[name]
                self.assertEqual(
                    (recovery.vertices, recovery.edges, recovery.triangles),
                    (vertices, edges, triangles),
                )
                self.assertEqual(recovery.euler_characteristic, 0)
                self.assertEqual(
                    (recovery.min_triangles_per_edge, recovery.max_triangles_per_edge),
                    (2, 2),
                )
                self.assertEqual(recovery.primal_tree_edges, vertices - 1)
                self.assertEqual(recovery.dual_cotree_edges, triangles - 1)
                self.assertEqual(recovery.leftover_edges, 2)
                self.assertEqual(recovery.treecotree_crossing_count, 1)
                self.assertEqual(recovery.treecotree_crossing_parity, 1)
                self.assertTrue(recovery.treecotree_accepted)
                self.assertFalse(recovery.treecotree_matches_reference)
                self.assertEqual(recovery.full_primal_cycles, primal_cycles)
                self.assertEqual(recovery.full_dual_cycles, dual_cycles)
                self.assertEqual(
                    (recovery.crossing_matrix_rows, recovery.crossing_matrix_cols),
                    (primal_cycles, dual_cycles),
                )
                self.assertEqual(recovery.crossing_matrix_rank, 2)
                self.assertGreater(recovery.crossing_matrix_weight, 0)
                self.assertTrue(recovery.full_basis_accepted)

    def test_attack_needs_no_reference(self) -> None:
        params = G17_PARAMETER_SETS["g17-6x6"]
        public, _ = generate_symplectic_cycle_pair_instance(
            params, bytes.fromhex("62" * 32)
        )
        recovery = recover_symplectic_cycle_pair(
            public, reference=None, successful_flips=params.successful_flips
        )
        self.assertTrue(recovery.treecotree_accepted)
        self.assertIsNone(recovery.treecotree_matches_reference)
        self.assertTrue(recovery.full_basis_accepted)

    def test_even_or_malformed_pair_is_rejected(self) -> None:
        params = G17_PARAMETER_SETS["g17-6x6"]
        public, reference = generate_symplectic_cycle_pair_instance(
            params, bytes.fromhex("73" * 32)
        )
        malformed = SymplecticCyclePairWitness(
            reference.witness.primal_cycle,
            tuple(sorted(reference.witness.dual_cycle + (reference.witness.dual_cycle[0],))),
        )
        validation = validate_symplectic_cycle_pair_witness(public, malformed)
        self.assertFalse(validation.valid)

    def test_multi_seed_public_break(self) -> None:
        for name, params in G17_PARAMETER_SETS.items():
            for seed_index in range(4):
                seed = hashlib.sha256(
                    b"MORPH-KEM G17 unit sweep\x00"
                    + name.encode("ascii")
                    + seed_index.to_bytes(4, "big")
                ).digest()
                with self.subTest(params=name, seed=seed_index):
                    public, reference = generate_symplectic_cycle_pair_instance(params, seed)
                    recovery = recover_symplectic_cycle_pair(
                        public,
                        reference=reference,
                        successful_flips=params.successful_flips,
                    )
                    self.assertEqual(recovery.leftover_edges, 2)
                    self.assertEqual(recovery.treecotree_crossing_count, 1)
                    self.assertTrue(recovery.treecotree_accepted)
                    self.assertEqual(recovery.crossing_matrix_rank, 2)
                    self.assertTrue(recovery.full_basis_accepted)

    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(GluingExperimentError):
            SymplecticCyclePairParameters("bad", 3, 6, 1).validate()
        with self.assertRaises(GluingExperimentError):
            SymplecticCyclePairParameters("bad", 6, 6, 1000).validate()
        with self.assertRaises(GluingExperimentError):
            generate_symplectic_cycle_pair_instance(
                G17_PARAMETER_SETS["g17-6x6"], b"short"
            )


if __name__ == "__main__":
    unittest.main()
