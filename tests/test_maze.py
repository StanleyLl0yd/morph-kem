import unittest

from morph_kem.maze import (
    MAZE_PARAMETER_SETS,
    MazeParameters,
    bounded_core_search,
    generate_maze,
    greedy_reduce,
    planted_reduce,
    planted_reduction_metrics,
    random_greedy_survey,
    recover_three_regular_core,
    verify_core,
)

MASTER_SEED = bytes.fromhex("31415926535897932384626433832795")


class MazeExperimentTests(unittest.TestCase):
    def test_generation_is_byte_deterministic(self) -> None:
        params = MAZE_PARAMETER_SETS["maze-6"]
        public1, trapdoor1 = generate_maze(params, MASTER_SEED)
        public2, trapdoor2 = generate_maze(params, MASTER_SEED)
        self.assertEqual(public1.encode(), public2.encode())
        self.assertEqual(trapdoor1.encode(), trapdoor2.encode())

    def test_planted_certificate_reduces_exactly_to_hidden_core(self) -> None:
        params = MAZE_PARAMETER_SETS["maze-6"]
        public, trapdoor = generate_maze(params, MASTER_SEED)
        core = planted_reduce(public, trapdoor)
        self.assertEqual(core, trapdoor.core)
        self.assertTrue(verify_core(public, core))
        self.assertEqual(len(trapdoor.certificate), params.expansions)

    def test_target_starts_with_multiple_free_choices(self) -> None:
        params = MAZE_PARAMETER_SETS["maze-6"]
        public, trapdoor = generate_maze(params, MASTER_SEED)
        metrics = planted_reduction_metrics(public, trapdoor)
        self.assertGreaterEqual(
            metrics.initial_free_pairs,
            params.min_initial_free_pairs,
        )
        self.assertGreater(metrics.mean_free_pairs, 1.0)

    def test_blind_greedy_is_reproducible(self) -> None:
        public, _ = generate_maze(MAZE_PARAMETER_SETS["maze-6"], MASTER_SEED)
        first = greedy_reduce(public, strategy="lex")
        second = greedy_reduce(public, strategy="lex")
        self.assertEqual(first.residual.encode(), second.residual.encode())
        self.assertEqual(first.collapses, second.collapses)

    def test_random_survey_is_reproducible(self) -> None:
        public, _ = generate_maze(MAZE_PARAMETER_SETS["maze-6"], MASTER_SEED)
        a = random_greedy_survey(public, trials=16, attack_seed=b"survey-test")
        b = random_greedy_survey(public, trials=16, attack_seed=b"survey-test")
        self.assertEqual(a, b)
        self.assertGreaterEqual(a.unique_residuals, 2)

    def test_bounded_search_finds_small_hidden_core(self) -> None:
        params = MazeParameters("test-maze-4", vertices=10, expansions=4)
        public, _ = generate_maze(params, MASTER_SEED)
        result = bounded_core_search(public, max_nodes=10_000)
        self.assertTrue(result.found)
        self.assertEqual(len(result.certificate), params.expansions)

    def test_degree_core_recovery_breaks_maze6(self) -> None:
        public, trapdoor = generate_maze(
            MAZE_PARAMETER_SETS["maze-6"],
            MASTER_SEED,
        )
        result = recover_three_regular_core(public, max_nodes=500_000)
        self.assertTrue(result.found)
        self.assertEqual(result.core, trapdoor.core)
        self.assertGreater(result.forced_edges, 0)

    def test_trapdoor_binding_rejects_other_public_instance(self) -> None:
        params = MAZE_PARAMETER_SETS["maze-4"]
        public1, _ = generate_maze(params, MASTER_SEED)
        _, trapdoor2 = generate_maze(params, b"another deterministic master seed")
        with self.assertRaises(ValueError):
            planted_reduce(public1, trapdoor2)


if __name__ == "__main__":
    unittest.main()
