from __future__ import annotations

import hashlib
import unittest

from morph_kem.hga_markoff_action import (
    HGA1Error,
    HGA1Parameters,
    HGA1_PARAMETER_SETS,
    apply_generator,
    apply_word,
    bidirectional_bfs,
    enumerate_markoff_points,
    generate_hga1_instance,
    is_markoff_point,
    is_reduced_word,
    recover_hga1,
    reduced_word_multiplicity,
    shortest_bfs,
    verify_action,
)


def digest(label: str) -> bytes:
    return hashlib.sha256(label.encode("ascii")).digest()


class HGA1MarkoffActionTests(unittest.TestCase):
    def test_parameter_grid_is_fixed(self) -> None:
        self.assertEqual(len(HGA1_PARAMETER_SETS), 9)
        with self.assertRaises(HGA1Error):
            HGA1Parameters("bad", 31, 8).validate()
        with self.assertRaises(HGA1Error):
            HGA1Parameters("bad", 29, 12).validate()

    def test_generators_preserve_markoff_surface_and_are_involutions(self) -> None:
        points = enumerate_markoff_points(29)
        self.assertGreater(len(points), 0)
        for point in points[:64]:
            self.assertTrue(is_markoff_point(point, 29))
            for generator in (0, 1, 2):
                moved = apply_generator(point, generator, 29)
                self.assertTrue(is_markoff_point(moved, 29))
                self.assertEqual(apply_generator(moved, generator, 29), point)

    def test_generation_is_deterministic_nontrivial_and_publicly_verifiable(self) -> None:
        params = HGA1_PARAMETER_SETS["hga1-p29-L8"]
        seed = digest("HGA1 deterministic generation unit v1")
        first = generate_hga1_instance(params, seed)
        second = generate_hga1_instance(params, seed)
        self.assertEqual(first, second)
        self.assertNotEqual(first.source, first.target)
        self.assertEqual(len(first.planted_word), params.word_bound)
        self.assertTrue(is_reduced_word(first.planted_word))
        self.assertEqual(
            apply_word(first.source, first.planted_word, params.prime), first.target
        )
        self.assertTrue(
            verify_action(
                params.prime,
                first.source,
                first.target,
                params.word_bound,
                first.planted_word,
            )
        )

    def test_public_bfs_attacks_recover_without_reference_word(self) -> None:
        params = HGA1_PARAMETER_SETS["hga1-p43-L16"]
        instance = generate_hga1_instance(
            params, digest("HGA1 public BFS recovery unit v1")
        )
        bfs = shortest_bfs(
            params.prime, instance.source, instance.target, params.word_bound
        )
        bidirectional = bidirectional_bfs(
            params.prime, instance.source, instance.target, params.word_bound
        )
        self.assertTrue(bfs.accepted)
        self.assertTrue(bidirectional.accepted)
        self.assertEqual(bfs.recovered_length, bidirectional.recovered_length)
        self.assertLessEqual(bfs.recovered_length, params.word_bound)
        self.assertTrue(
            verify_action(
                params.prime,
                instance.source,
                instance.target,
                params.word_bound,
                bfs.recovered_word,
            )
        )
        self.assertTrue(
            verify_action(
                params.prime,
                instance.source,
                instance.target,
                params.word_bound,
                bidirectional.recovered_word,
            )
        )

    def test_reduced_word_multiplicity_contains_planted_witness(self) -> None:
        params = HGA1_PARAMETER_SETS["hga1-p29-L8"]
        instance = generate_hga1_instance(
            params, digest("HGA1 multiplicity unit v1")
        )
        multiplicity = reduced_word_multiplicity(
            params.prime, instance.source, instance.target, params.word_bound
        )
        self.assertGreaterEqual(multiplicity.transporter_reduced_words_leq_bound, 1)
        self.assertGreaterEqual(
            multiplicity.stabilizer_nonempty_reduced_words_leq_bound, 0
        )

    def test_full_recovery_keeps_planted_equality_post_success_only(self) -> None:
        params = HGA1_PARAMETER_SETS["hga1-p29-L8"]
        instance = generate_hga1_instance(
            params, digest("HGA1 full recovery unit v1")
        )
        result = recover_hga1(instance)
        self.assertTrue(result.bfs.accepted)
        self.assertTrue(result.bidirectional.accepted)
        self.assertGreaterEqual(result.orbit_size, 2)
        self.assertEqual(result.orbit_edge_scans, 3 * result.orbit_size)
        self.assertGreaterEqual(
            result.multiplicity.transporter_reduced_words_leq_bound, 1
        )


if __name__ == "__main__":
    unittest.main()
