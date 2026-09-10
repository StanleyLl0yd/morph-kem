import unittest

from morph_kem.morse import validate_morse_matching
from morph_kem.nonmanifold import (
    NONMANIFOLD_PARAMETER_SETS,
    bounded_tree_extension_search,
    generate_nonmanifold_instance,
    greedy_witness_survey,
    incidence_metrics,
)

MASTER_SEED = bytes.fromhex("50126490aabbccddeeff1234567890ab")


class NonManifoldM5Tests(unittest.TestCase):
    def test_generation_is_deterministic_and_irregular(self) -> None:
        parameters = NONMANIFOLD_PARAMETER_SETS["m5-8"]
        public1, reference1 = generate_nonmanifold_instance(parameters, MASTER_SEED)
        public2, reference2 = generate_nonmanifold_instance(parameters, MASTER_SEED)
        self.assertEqual(public1.encode(), public2.encode())
        self.assertEqual(reference1, reference2)
        metrics = incidence_metrics(public1.target)
        self.assertEqual(metrics.vertices, parameters.vertices)
        self.assertGreaterEqual(metrics.min_triangles_per_edge, 2)
        self.assertGreater(metrics.max_triangles_per_edge, 2)
        self.assertEqual(metrics.free_collapse_pairs, 0)

    def test_reference_matching_is_accepted(self) -> None:
        public, reference = generate_nonmanifold_instance(
            NONMANIFOLD_PARAMETER_SETS["m5-8"], MASTER_SEED
        )
        result = validate_morse_matching(public.target, reference.matching, public.critical_target)
        self.assertTrue(result.valid)
        self.assertEqual(result.critical_vector, public.critical_target)
        self.assertEqual(public.critical_target[0], 1)

    def test_public_greedy_survey_is_reproducible(self) -> None:
        public, _ = generate_nonmanifold_instance(
            NONMANIFOLD_PARAMETER_SETS["m5-8"], MASTER_SEED
        )
        first = greedy_witness_survey(public, trials=16, attack_seed=b"survey")
        second = greedy_witness_survey(public, trials=16, attack_seed=b"survey")
        self.assertEqual(first, second)
        self.assertLessEqual(first.best_total_critical, first.mean_total_critical)

    def test_bounded_extension_search_respects_cap(self) -> None:
        public, _ = generate_nonmanifold_instance(
            NONMANIFOLD_PARAMETER_SETS["m5-8"], MASTER_SEED
        )
        result = bounded_tree_extension_search(
            public,
            tree_trials=2,
            max_nodes=5000,
            attack_seed=b"exact",
        )
        self.assertLessEqual(result.nodes, 5000)
        if result.found:
            self.assertIsNotNone(result.validation)
            self.assertTrue(result.validation.valid)


if __name__ == "__main__":
    unittest.main()
