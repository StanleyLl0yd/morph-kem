import unittest

from morph_kem.escher import (
    ESCHER_PARAMETER_SETS,
    fundamental_cycle_syndrome,
    generate_escher_instance,
    propagate_escher_potentials,
    solve_escher_repair,
    validate_escher_witness,
)

MASTER_SEED = bytes.fromhex("14142135623730950488016887242097")


class EscherAtlasTests(unittest.TestCase):
    def test_generation_is_byte_deterministic(self) -> None:
        params = ESCHER_PARAMETER_SETS["escher-12"]
        public1, reference1 = generate_escher_instance(params, MASTER_SEED)
        public2, reference2 = generate_escher_instance(params, MASTER_SEED)
        self.assertEqual(public1.encode(), public2.encode())
        self.assertEqual(reference1, reference2)

    def test_planted_seams_are_only_reference_and_form_valid_witness(self) -> None:
        public, reference = generate_escher_instance(
            ESCHER_PARAMETER_SETS["escher-12"],
            MASTER_SEED,
        )
        result = validate_escher_witness(
            public,
            reference.planted_seams,
            reference.heights,
        )
        self.assertTrue(result.accepted)
        self.assertEqual(len(reference.planted_seams), public.parameters.seam_budget)

    def test_public_atlas_is_globally_frustrated_without_seams(self) -> None:
        public, _ = generate_escher_instance(
            ESCHER_PARAMETER_SETS["escher-12"],
            MASTER_SEED,
        )
        propagation = propagate_escher_potentials(public, ())
        self.assertFalse(propagation.balanced)
        self.assertGreater(len(propagation.conflict_cycle), 0)

        syndrome = fundamental_cycle_syndrome(public)
        self.assertEqual(len(syndrome.values), public.graph.cycle_rank)
        self.assertGreater(syndrome.nonzero, 0)

    def test_every_single_edge_constraint_is_locally_satisfiable(self) -> None:
        public, _ = generate_escher_instance(
            ESCHER_PARAMETER_SETS["escher-10"],
            MASTER_SEED,
        )
        modulus = public.parameters.modulus
        for label in public.increments:
            left_height = 0
            right_height = label
            self.assertEqual((right_height - left_height) % modulus, label)

    def test_global_gauge_shift_preserves_a_witness(self) -> None:
        public, reference = generate_escher_instance(
            ESCHER_PARAMETER_SETS["escher-10"],
            MASTER_SEED,
        )
        shifted = tuple(
            (height + 3) % public.parameters.modulus
            for height in reference.heights
        )
        self.assertTrue(
            validate_escher_witness(
                public,
                reference.planted_seams,
                shifted,
            ).accepted
        )

    def test_exact_attack_finds_an_equivalent_repair(self) -> None:
        public, _ = generate_escher_instance(
            ESCHER_PARAMETER_SETS["escher-12"],
            MASTER_SEED,
        )
        repair = solve_escher_repair(public, max_nodes=100_000)
        self.assertTrue(repair.found)
        self.assertIsNotNone(repair.minimum_seams)
        self.assertLessEqual(repair.minimum_seams, public.parameters.seam_budget)
        self.assertTrue(
            validate_escher_witness(
                public,
                repair.seams,
                repair.heights,
            ).accepted
        )

    def test_toy_ladder_is_solved_within_baseline_bound(self) -> None:
        for name in ("escher-8", "escher-10", "escher-12"):
            public, _ = generate_escher_instance(
                ESCHER_PARAMETER_SETS[name],
                MASTER_SEED,
            )
            repair = solve_escher_repair(public, max_nodes=100_000)
            self.assertTrue(repair.found, name)
            self.assertFalse(repair.exhausted, name)


if __name__ == "__main__":
    unittest.main()
