import unittest

from morph_kem.pachner import (
    PACHNER_PARAMETER_SETS,
    PachnerState,
    apply_move,
    bfs_pachner_recover,
    bidirectional_pachner_recover,
    boundary_of_4_simplex,
    canonical_state,
    generate_pachner_instance,
    legal_moves,
    pachner_path_metrics,
    verify_pachner_witness,
)

MASTER_SEED = bytes.fromhex("48026490aabbccddeeff1029384756aa")


class PachnerStateTests(unittest.TestCase):
    def test_boundary_of_4_simplex_invariants(self) -> None:
        state = boundary_of_4_simplex()
        self.assertEqual((len(state.vertices), len(state.edges), len(state.triangles), state.tetrahedra), (5, 10, 10, 5))
        self.assertEqual(state.euler_characteristic, 0)

    def test_canonical_state_removes_vertex_labels(self) -> None:
        state = boundary_of_4_simplex()
        mapping = {0: 8, 1: 3, 2: 11, 3: 5, 4: 1}
        relabeled = PachnerState(tuple(sorted(tuple(sorted(mapping[v] for v in tet)) for tet in state.facets)))
        self.assertEqual(canonical_state(state).facets, canonical_state(relabeled).facets)

    def test_23_has_32_inverse_in_quotient_graph(self) -> None:
        public, _ = generate_pachner_instance(PACHNER_PARAMETER_SETS["t0-4"], MASTER_SEED)
        move = next(move for move in legal_moves(public.start) if move.kind == "23")
        target = apply_move(public.start, move)
        inverse_targets = {
            apply_move(target, candidate).facets
            for candidate in legal_moves(target)
            if candidate.kind == "32"
        }
        self.assertIn(public.start.facets, inverse_targets)


class PachnerExperimentTests(unittest.TestCase):
    def test_generation_is_deterministic_and_planted_path_valid(self) -> None:
        params = PACHNER_PARAMETER_SETS["t0-8"]
        public1, reference1 = generate_pachner_instance(params, MASTER_SEED)
        public2, reference2 = generate_pachner_instance(params, MASTER_SEED)
        self.assertEqual(public1.encode(), public2.encode())
        self.assertEqual(reference1, reference2)
        self.assertTrue(verify_pachner_witness(public1, reference1.planted_moves))
        self.assertEqual(len(public1.start.vertices), 9)

    def test_bfs_recovers_t0_4(self) -> None:
        public, reference = generate_pachner_instance(PACHNER_PARAMETER_SETS["t0-4"], MASTER_SEED)
        result = bfs_pachner_recover(public, max_states=10_000)
        self.assertTrue(result.found)
        self.assertEqual(result.distance, 4)
        self.assertTrue(verify_pachner_witness(public, result.moves))
        self.assertLess(result.visited_states, 1_000)
        self.assertEqual(len(reference.planted_moves), 4)

    def test_bidirectional_attack_recovers_all_toy_sets(self) -> None:
        for name, params in PACHNER_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public, _ = generate_pachner_instance(params, MASTER_SEED)
                result = bidirectional_pachner_recover(public, max_states=20_000)
                self.assertTrue(result.found)
                self.assertTrue(verify_pachner_witness(public, result.moves))
                self.assertLessEqual(result.distance, public.bound)

    def test_t0_8_has_shorter_equivalent_path(self) -> None:
        public, reference = generate_pachner_instance(PACHNER_PARAMETER_SETS["t0-8"], MASTER_SEED)
        result = bidirectional_pachner_recover(public, max_states=20_000)
        self.assertTrue(result.found)
        self.assertEqual(len(reference.planted_moves), 8)
        self.assertEqual(result.distance, 4)

    def test_metrics_show_state_dependent_branching(self) -> None:
        public, reference = generate_pachner_instance(PACHNER_PARAMETER_SETS["t0-6"], MASTER_SEED)
        metrics = pachner_path_metrics(public, reference)
        self.assertGreaterEqual(metrics.initial_branching, 2)
        self.assertGreater(metrics.max_branching, metrics.min_branching)
        self.assertGreater(metrics.commuting_pairs_tested, 0)


if __name__ == "__main__":
    unittest.main()
