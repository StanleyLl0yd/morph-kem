import unittest

from morph_kem.lifted_atlas import (
    LIFTED_ATLAS_PARAMETER_SETS,
    canonicalize_public_cover,
    check_lift_equivariance,
    compare_to_reference,
    generate_lifted_atlas,
    lift_path,
    residual_root_relabelings,
)

MASTER_SEED = bytes.fromhex("22360679774997896964091736687312")


class LiftedAtlasTests(unittest.TestCase):
    def test_generation_is_byte_deterministic(self) -> None:
        params = LIFTED_ATLAS_PARAMETER_SETS["lift-10x4"]
        public1, reference1 = generate_lifted_atlas(params, MASTER_SEED)
        public2, reference2 = generate_lifted_atlas(params, MASTER_SEED)
        self.assertEqual(public1.encode(), public2.encode())
        self.assertEqual(reference1, reference2)

    def test_public_attack_normalizes_every_tree_edge(self) -> None:
        public, _ = generate_lifted_atlas(
            LIFTED_ATLAS_PARAMETER_SETS["lift-12x5"],
            MASTER_SEED,
        )
        result = canonicalize_public_cover(public)
        self.assertEqual(
            result.tree_identity_edges,
            public.graph.vertices - 1,
        )
        self.assertEqual(
            result.chord_edges,
            public.graph.cycle_rank,
        )

    def test_public_normal_form_is_secret_cover_up_to_one_global_conjugation(self) -> None:
        public, reference = generate_lifted_atlas(
            LIFTED_ATLAS_PARAMETER_SETS["lift-12x5"],
            MASTER_SEED,
        )
        normalization = canonicalize_public_cover(public)
        comparison = compare_to_reference(
            public,
            reference,
            normalization,
        )
        self.assertTrue(comparison.globally_conjugate)

    def test_path_lifting_is_preserved_by_public_gauge_attack(self) -> None:
        public, _ = generate_lifted_atlas(
            LIFTED_ATLAS_PARAMETER_SETS["lift-10x4"],
            MASTER_SEED,
        )
        normalization = canonicalize_public_cover(public)
        path = tuple(range(public.graph.vertices))
        result = check_lift_equivariance(
            public,
            normalization,
            path,
            public_start_sheet=1,
        )
        self.assertTrue(result.holds)

    def test_attack_is_deterministic_and_secret_free(self) -> None:
        public, _ = generate_lifted_atlas(
            LIFTED_ATLAS_PARAMETER_SETS["lift-8x3"],
            MASTER_SEED,
        )
        first = canonicalize_public_cover(public)
        second = canonicalize_public_cover(public)
        self.assertEqual(first, second)
        self.assertGreater(first.permutation_point_ops, 0)

    def test_residual_ambiguity_is_only_global_sheet_relabeling(self) -> None:
        public, _ = generate_lifted_atlas(
            LIFTED_ATLAS_PARAMETER_SETS["lift-8x3"],
            MASTER_SEED,
        )
        self.assertEqual(residual_root_relabelings(public), 6)

    def test_public_path_lift_needs_no_secret(self) -> None:
        public, _ = generate_lifted_atlas(
            LIFTED_ATLAS_PARAMETER_SETS["lift-8x3"],
            MASTER_SEED,
        )
        endpoint = lift_path(
            public.graph,
            public.transitions,
            (0, 1, 2, 3),
            0,
        )
        self.assertIn(endpoint, range(public.parameters.sheets))


if __name__ == "__main__":
    unittest.main()
