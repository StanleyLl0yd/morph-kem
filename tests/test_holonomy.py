import unittest

from morph_kem.holonomy import (
    HOLONOMY_PARAMETER_SETS,
    S3_TRANSPOSITIONS,
    generate_holonomy_graph,
    generate_s3_instance,
    generate_z2_instance,
    recover_s3_abelianization,
    recover_z2_spanning_tree,
    solve_s3_csp,
    validate_s3_frames,
    validate_z2_frames,
)

MASTER_SEED = bytes.fromhex("16180339887498948482045868343656")


class HolonomyGraphTests(unittest.TestCase):
    def test_graph_generation_is_deterministic_and_cycle_rich(self) -> None:
        params = HOLONOMY_PARAMETER_SETS["h1-12"]
        first = generate_holonomy_graph(params, MASTER_SEED)
        second = generate_holonomy_graph(params, MASTER_SEED)
        self.assertEqual(first.encode(), second.encode())
        self.assertEqual(first.cycle_rank, params.extra_edges + 1)
        self.assertEqual(len(first.spanning_tree_edges()), params.vertices - 1)
        self.assertGreaterEqual(min(len(n) for n in first.neighbors()), 2)


class Z2HolonomyTests(unittest.TestCase):
    def test_reference_and_public_tree_recovery_are_accepted(self) -> None:
        params = HOLONOMY_PARAMETER_SETS["h1-12"]
        public, reference = generate_z2_instance(params, MASTER_SEED)
        self.assertTrue(validate_z2_frames(public, reference.frames))

        recovered = recover_z2_spanning_tree(public)
        self.assertTrue(recovered.accepted)
        self.assertTrue(validate_z2_frames(public, recovered.frames))
        self.assertEqual(recovered.chord_edges, public.graph.cycle_rank)
        self.assertEqual(recovered.edge_checks, len(public.graph.edges))

    def test_z2_public_target_is_exactly_cycle_rank_sized(self) -> None:
        public, _ = generate_z2_instance(
            HOLONOMY_PARAMETER_SETS["h1-10"],
            MASTER_SEED,
        )
        self.assertEqual(len(public.chord_target), public.graph.cycle_rank)


class S3HolonomyTests(unittest.TestCase):
    def test_reference_witness_is_accepted(self) -> None:
        public, reference = generate_s3_instance(
            HOLONOMY_PARAMETER_SETS["h1-12"],
            MASTER_SEED,
        )
        self.assertEqual(len(S3_TRANSPOSITIONS), 3)
        self.assertTrue(validate_s3_frames(public, reference.frames).accepted)

    def test_abelianization_recovers_one_parity_per_vertex(self) -> None:
        public, _ = generate_s3_instance(
            HOLONOMY_PARAMETER_SETS["h1-12"],
            MASTER_SEED,
        )
        leak = recover_s3_abelianization(public)
        self.assertTrue(leak.consistent)
        self.assertEqual(leak.recovered_vertices, public.graph.vertices)
        self.assertGreaterEqual(leak.edge_checks, public.graph.vertices - 1)

    def test_exact_csp_finds_equivalent_witness(self) -> None:
        public, _ = generate_s3_instance(
            HOLONOMY_PARAMETER_SETS["h1-12"],
            MASTER_SEED,
        )
        result = solve_s3_csp(public, solution_cap=32)
        self.assertTrue(result.accepted)
        self.assertIsNotNone(result.first_solution)
        self.assertGreater(result.solutions_found, 0)
        self.assertLessEqual(result.parity_pruned_domain_mean, 3.0)
        self.assertTrue(validate_s3_frames(public, result.first_solution).accepted)

    def test_s3_generation_and_attack_are_deterministic(self) -> None:
        params = HOLONOMY_PARAMETER_SETS["h1-10"]
        public1, reference1 = generate_s3_instance(params, MASTER_SEED)
        public2, reference2 = generate_s3_instance(params, MASTER_SEED)
        self.assertEqual(public1.encode(), public2.encode())
        self.assertEqual(reference1.frames, reference2.frames)
        self.assertEqual(
            solve_s3_csp(public1, solution_cap=16),
            solve_s3_csp(public2, solution_cap=16),
        )


if __name__ == "__main__":
    unittest.main()
