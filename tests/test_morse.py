import unittest

from morph_kem import SimplicialComplex
from morph_kem.morse import (
    MORSE_PARAMETER_SETS,
    collapse_to_graph_witness,
    collapse_witness_survey,
    generate_morse_instance,
    greedy_matching_survey,
    validate_morse_matching,
    verify_planted_witness,
)

MASTER_SEED = bytes.fromhex("27182818284590452353602874713526")


class MorseValidationTests(unittest.TestCase):
    def test_rejects_reused_simplex(self) -> None:
        complex_ = SimplicialComplex.from_facets([(0, 1), (0, 2)])
        result = validate_morse_matching(
            complex_,
            (((0,), (0, 1)), ((0,), (0, 2))),
        )
        self.assertFalse(result.valid)
        self.assertIn("reused", result.reason)

    def test_rejects_directed_hasse_cycle(self) -> None:
        cycle = SimplicialComplex.from_facets([(0, 1), (1, 2), (0, 2)])
        matching = (
            ((0,), (0, 1)),
            ((1,), (1, 2)),
            ((2,), (0, 2)),
        )
        result = validate_morse_matching(cycle, matching)
        self.assertFalse(result.valid)
        self.assertFalse(result.acyclic)
        self.assertIn("cycle", result.reason)

    def test_spanning_tree_style_matching_has_expected_critical_vector(self) -> None:
        cycle = SimplicialComplex.from_facets([(0, 1), (1, 2), (2, 3), (0, 3)])
        matching = (
            ((1,), (0, 1)),
            ((2,), (1, 2)),
            ((3,), (2, 3)),
        )
        result = validate_morse_matching(cycle, matching, (1, 1))
        self.assertTrue(result.valid)
        self.assertEqual(result.critical_vector, (1, 1))


class MorseExperimentTests(unittest.TestCase):
    def test_generation_is_byte_deterministic(self) -> None:
        params = MORSE_PARAMETER_SETS["morse-6"]
        public1, trapdoor1 = generate_morse_instance(params, MASTER_SEED)
        public2, trapdoor2 = generate_morse_instance(params, MASTER_SEED)
        self.assertEqual(public1.encode(), public2.encode())
        self.assertEqual(trapdoor1.encode(), trapdoor2.encode())

    def test_planted_witness_is_accepted(self) -> None:
        public, trapdoor = generate_morse_instance(
            MORSE_PARAMETER_SETS["morse-6"],
            MASTER_SEED,
        )
        result = verify_planted_witness(public, trapdoor)
        self.assertTrue(result.valid)
        self.assertEqual(result.critical_vector, public.critical_target)

    def test_public_relation_contains_no_core_digest(self) -> None:
        public, _ = generate_morse_instance(
            MORSE_PARAMETER_SETS["morse-6"],
            MASTER_SEED,
        )
        encoded = public.encode()
        self.assertNotIn(b"core_digest", encoded)
        self.assertIn(b"critical_target", encoded)

    def test_lex_collapse_builds_an_accepted_equivalent_witness(self) -> None:
        public, _ = generate_morse_instance(
            MORSE_PARAMETER_SETS["morse-6"],
            MASTER_SEED,
        )
        result = collapse_to_graph_witness(public, strategy="lex")
        self.assertTrue(result.reached_graph)
        self.assertTrue(result.accepted)
        self.assertEqual(result.triangle_collapses, public.parameters.expansions)

    def test_random_collapse_survey_is_reproducible(self) -> None:
        public, _ = generate_morse_instance(
            MORSE_PARAMETER_SETS["morse-6"],
            MASTER_SEED,
        )
        first = collapse_witness_survey(public, trials=16, attack_seed=b"survey")
        second = collapse_witness_survey(public, trials=16, attack_seed=b"survey")
        self.assertEqual(first, second)
        self.assertGreater(first.accepted, 0)

    def test_greedy_matching_survey_is_reproducible(self) -> None:
        public, _ = generate_morse_instance(
            MORSE_PARAMETER_SETS["morse-6"],
            MASTER_SEED,
        )
        first = greedy_matching_survey(public, trials=4, attack_seed=b"greedy")
        second = greedy_matching_survey(public, trials=4, attack_seed=b"greedy")
        self.assertEqual(first, second)
        self.assertGreaterEqual(first.best_total_critical, sum(public.critical_target))


if __name__ == "__main__":
    unittest.main()
