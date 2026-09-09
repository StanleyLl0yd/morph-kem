import unittest

from morph_kem.higher_atlas import (
    HIGHER_ATLAS_PARAMETER_SETS,
    chart_role_signature_audit,
    generate_higher_atlas,
    pairwise_compatibility_audit,
    solve_higher_atlas_repair,
    validate_higher_atlas_witness,
)

MASTER_SEED = bytes.fromhex("17320508075688772935274463415059")


class HigherAtlasTests(unittest.TestCase):
    def test_generation_is_deterministic(self) -> None:
        params = HIGHER_ATLAS_PARAMETER_SETS["atlas-10"]
        public1, reference1 = generate_higher_atlas(params, MASTER_SEED)
        public2, reference2 = generate_higher_atlas(params, MASTER_SEED)
        self.assertEqual(public1.encode(), public2.encode())
        self.assertEqual(reference1, reference2)

    def test_planted_reference_is_accepted_after_seams(self) -> None:
        public, reference = generate_higher_atlas(
            HIGHER_ATLAS_PARAMETER_SETS["atlas-10"],
            MASTER_SEED,
        )
        result = validate_higher_atlas_witness(
            public,
            reference.planted_seams,
            reference.assignment,
        )
        self.assertTrue(result.accepted)

    def test_every_chart_pair_is_jointly_compatible(self) -> None:
        public, _ = generate_higher_atlas(
            HIGHER_ATLAS_PARAMETER_SETS["atlas-10"],
            MASTER_SEED,
        )
        audit = pairwise_compatibility_audit(public)
        self.assertTrue(audit.all_compatible)
        self.assertGreater(audit.chart_pairs, 0)

    def test_full_public_atlas_has_no_zero_seam_witness(self) -> None:
        public, _ = generate_higher_atlas(
            HIGHER_ATLAS_PARAMETER_SETS["atlas-10"],
            MASTER_SEED,
        )
        repair = solve_higher_atlas_repair(public, max_nodes=500_000)
        self.assertTrue(repair.found)
        self.assertGreater(repair.minimum_seams, 0)

    def test_exact_attack_finds_valid_equivalent_repair(self) -> None:
        public, _ = generate_higher_atlas(
            HIGHER_ATLAS_PARAMETER_SETS["atlas-12"],
            MASTER_SEED,
        )
        repair = solve_higher_atlas_repair(public, max_nodes=1_000_000)
        self.assertTrue(repair.found)
        self.assertTrue(repair.proven_minimum)
        self.assertLessEqual(repair.minimum_seams, public.parameters.seam_budget)
        self.assertTrue(
            validate_higher_atlas_witness(
                public,
                repair.seams,
                repair.assignment,
            ).accepted
        )

    def test_role_signature_audit_is_deterministic(self) -> None:
        public, reference = generate_higher_atlas(
            HIGHER_ATLAS_PARAMETER_SETS["atlas-10"],
            MASTER_SEED,
        )
        first = chart_role_signature_audit(public, reference)
        second = chart_role_signature_audit(public, reference)
        self.assertEqual(first, second)

    def test_small_ladder_is_solved_within_baseline_bound(self) -> None:
        for name in ("atlas-8", "atlas-10", "atlas-12"):
            public, _ = generate_higher_atlas(
                HIGHER_ATLAS_PARAMETER_SETS[name],
                MASTER_SEED,
            )
            repair = solve_higher_atlas_repair(public, max_nodes=1_000_000)
            self.assertTrue(repair.found, name)
            self.assertTrue(repair.proven_minimum, name)


if __name__ == "__main__":
    unittest.main()
