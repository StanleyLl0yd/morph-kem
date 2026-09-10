import unittest

from morph_kem.pachner import (
    PachnerExperimentError,
    bfs_pachner_recover,
    bidirectional_pachner_recover,
    verify_pachner_witness,
)
from morph_kem.pachner_distance import (
    T1_PARAMETER_SETS,
    astar_tetrahedron_recover,
    exact_shell_states,
    generate_distance_instance,
    profile_distance_shell,
)

MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


class PachnerDistanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.public2, cls.reference2 = generate_distance_instance(
            T1_PARAMETER_SETS["t1-2"], MASTER_SEED
        )
        cls.public3, cls.reference3 = generate_distance_instance(
            T1_PARAMETER_SETS["t1-3"], MASTER_SEED
        )

    def test_generation_is_deterministic(self) -> None:
        public, reference = generate_distance_instance(
            T1_PARAMETER_SETS["t1-2"], MASTER_SEED
        )
        self.assertEqual(public.encode(), self.public2.encode())
        self.assertEqual(reference, self.reference2)

    def test_shell_profile_is_complete_and_partitioned(self) -> None:
        profile = self.reference3.profile
        self.assertEqual(profile.depth, 3)
        self.assertEqual(len(profile.shell_sizes), 4)
        self.assertEqual(sum(profile.shell_sizes), profile.ball_size)
        self.assertEqual(profile.shell_sizes[0], 1)
        self.assertEqual(profile.expanded_states, sum(profile.shell_sizes[:-1]))

    def test_reference_path_has_exact_distance_and_verifies(self) -> None:
        reference = self.reference3
        self.assertEqual(len(reference.shortest_path), 3)
        self.assertEqual(reference.exact_distance, 3)
        self.assertTrue(verify_pachner_witness(self.public3, reference.shortest_path))
        bfs = bfs_pachner_recover(self.public3, max_states=80_000)
        self.assertTrue(bfs.found)
        self.assertEqual(bfs.distance, 3)

    def test_target_is_selected_from_max_tetrahedron_slack(self) -> None:
        shell = exact_shell_states(self.public3.start, 3, max_states=80_000)
        start_tets = self.public3.start.tetrahedra
        max_slack = max(3 - abs(state.tetrahedra - start_tets) for state in shell)
        self.assertEqual(self.reference3.target_tetrahedron_slack, max_slack)
        self.assertEqual(self.reference3.max_shell_tetrahedron_slack, max_slack)

    def test_shortest_path_multiplicity_metadata_is_nonzero(self) -> None:
        self.assertGreaterEqual(self.reference3.shortest_paths_capped, 1)
        self.assertGreaterEqual(self.reference3.shortest_predecessors, 1)
        self.assertGreaterEqual(self.reference3.max_slack_candidates, 1)
        self.assertGreaterEqual(self.reference3.min_path_candidates, 1)

    def test_bidirectional_attack_returns_exact_distance(self) -> None:
        result = bidirectional_pachner_recover(self.public3, max_states=80_000)
        self.assertTrue(result.found)
        self.assertEqual(result.distance, 3)
        self.assertTrue(verify_pachner_witness(self.public3, result.moves))

    def test_tetrahedron_astar_returns_exact_distance(self) -> None:
        result = astar_tetrahedron_recover(self.public3, max_states=80_000)
        self.assertTrue(result.found)
        self.assertEqual(result.distance, 3)
        self.assertTrue(verify_pachner_witness(self.public3, result.moves))

    def test_profile_rejects_incomplete_state_cap(self) -> None:
        with self.assertRaises(PachnerExperimentError):
            profile_distance_shell(self.public2.start, 2, max_states=2)


if __name__ == "__main__":
    unittest.main()
