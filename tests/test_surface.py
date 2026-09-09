import unittest

from morph_kem.surface import (
    SURFACE_PARAMETER_SETS,
    generate_surface_instance,
    surface_greedy_matching_survey,
    surface_incidence,
    tree_cotree_survey,
    tree_cotree_witness,
    verify_surface_trapdoor,
)

MASTER_SEED = bytes.fromhex("16180339887498948482045868343656")


class SurfaceExperimentTests(unittest.TestCase):
    def test_generation_is_byte_deterministic(self) -> None:
        params = SURFACE_PARAMETER_SETS["torus-3x3"]
        public1, trapdoor1 = generate_surface_instance(params, MASTER_SEED)
        public2, trapdoor2 = generate_surface_instance(params, MASTER_SEED)
        self.assertEqual(public1.encode(), public2.encode())
        self.assertEqual(trapdoor1.encode(), trapdoor2.encode())

    def test_surface_is_closed_and_has_no_free_collapse_pair(self) -> None:
        public, _ = generate_surface_instance(
            SURFACE_PARAMETER_SETS["torus-3x3"],
            MASTER_SEED,
        )
        incidence = surface_incidence(public)
        self.assertEqual(incidence.min_triangles_per_edge, 2)
        self.assertEqual(incidence.max_triangles_per_edge, 2)
        self.assertEqual(public.target.free_collapse_pairs(), ())

    def test_torus_cell_counts(self) -> None:
        public, _ = generate_surface_instance(
            SURFACE_PARAMETER_SETS["torus-4x4"],
            MASTER_SEED,
        )
        incidence = surface_incidence(public)
        self.assertEqual(incidence.vertices, 16)
        self.assertEqual(incidence.edges, 48)
        self.assertEqual(incidence.triangles, 32)

    def test_planted_witness_is_accepted(self) -> None:
        public, trapdoor = generate_surface_instance(
            SURFACE_PARAMETER_SETS["torus-3x3"],
            MASTER_SEED,
        )
        result = verify_surface_trapdoor(public, trapdoor)
        self.assertTrue(result.valid)
        self.assertEqual(result.critical_vector, (1, 2, 1))

    def test_public_tree_cotree_attack_is_accepted(self) -> None:
        public, _ = generate_surface_instance(
            SURFACE_PARAMETER_SETS["torus-4x4"],
            MASTER_SEED,
        )
        result = tree_cotree_witness(public, attack_seed=b"public-attack")
        self.assertTrue(result.validation.valid)
        self.assertEqual(result.validation.critical_vector, (1, 2, 1))
        self.assertEqual(result.primal_tree_edges, 15)
        self.assertEqual(result.dual_tree_edges, 31)
        self.assertEqual(result.critical_edges, 2)

    def test_random_tree_cotree_survey_is_reproducible(self) -> None:
        public, _ = generate_surface_instance(
            SURFACE_PARAMETER_SETS["torus-4x4"],
            MASTER_SEED,
        )
        first = tree_cotree_survey(public, trials=16, attack_seed=b"survey")
        second = tree_cotree_survey(public, trials=16, attack_seed=b"survey")
        self.assertEqual(first, second)
        self.assertEqual(first.target_hits, 16)
        self.assertGreater(first.unique_matchings, 1)

    def test_generic_greedy_survey_is_reproducible(self) -> None:
        public, _ = generate_surface_instance(
            SURFACE_PARAMETER_SETS["torus-3x3"],
            MASTER_SEED,
        )
        first = surface_greedy_matching_survey(public, trials=4, attack_seed=b"greedy")
        second = surface_greedy_matching_survey(public, trials=4, attack_seed=b"greedy")
        self.assertEqual(first, second)
        self.assertGreaterEqual(first.best_total_critical, 4)


if __name__ == "__main__":
    unittest.main()
