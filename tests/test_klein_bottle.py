import unittest

from morph_kem.klein_bottle import (
    KLEIN_BOTTLE_PARAMETER_SETS,
    analyze_klein_orientability,
    build_klein_bottle,
    generate_klein_orientation_instance,
    normalize_klein_transitions,
    recover_klein_gauge,
    reference_gauge_matches,
    validate_klein_reference,
)

MASTER_SEED = bytes.fromhex("30124490aabbccddeeff1029384756ab")


class KleinBottleControlTests(unittest.TestCase):
    def test_exact_closed_nonorientable_scaffolds(self) -> None:
        for parameters in KLEIN_BOTTLE_PARAMETER_SETS.values():
            scaffold = build_klein_bottle(parameters)
            cells = parameters.width * parameters.height
            self.assertEqual(len(scaffold.complex.vertices), cells)
            self.assertEqual(len(scaffold.edges), 3 * cells)
            self.assertEqual(len(scaffold.faces), 2 * cells)
            self.assertEqual(scaffold.euler_characteristic, 0)
            self.assertEqual(len(scaffold.complex.free_collapse_pairs()), 0)
            self.assertEqual(scaffold.dual_cycle_rank, cells + 1)

            analysis = analyze_klein_orientability(scaffold)
            self.assertFalse(analysis.orientable)
            self.assertGreater(analysis.nonzero_syndromes, 0)
            self.assertEqual(
                len(analysis.fundamental_syndromes),
                scaffold.dual_cycle_rank,
            )

    def test_generation_is_byte_deterministic(self) -> None:
        parameters = KLEIN_BOTTLE_PARAMETER_SETS["klein-bottle-5x4"]
        public1, reference1 = generate_klein_orientation_instance(
            parameters,
            MASTER_SEED,
        )
        public2, reference2 = generate_klein_orientation_instance(
            parameters,
            MASTER_SEED,
        )
        self.assertEqual(public1.encode(), public2.encode())
        self.assertEqual(reference1, reference2)

    def test_reference_is_valid(self) -> None:
        parameters = KLEIN_BOTTLE_PARAMETER_SETS["klein-bottle-5x4"]
        public, reference = generate_klein_orientation_instance(
            parameters,
            MASTER_SEED,
        )
        self.assertTrue(validate_klein_reference(public, reference))

    def test_public_tree_normalization_removes_hidden_gauge(self) -> None:
        parameters = KLEIN_BOTTLE_PARAMETER_SETS["klein-bottle-5x4"]
        public, _ = generate_klein_orientation_instance(
            parameters,
            MASTER_SEED,
        )
        public_normal = normalize_klein_transitions(
            public.scaffold,
            public.transitions,
        )
        canonical = tuple(
            edge.canonical_transition
            for edge in public.scaffold.dual_edges
        )
        canonical_normal = normalize_klein_transitions(
            public.scaffold,
            canonical,
        )
        self.assertEqual(
            public_normal.normalized_transitions,
            canonical_normal.normalized_transitions,
        )
        self.assertEqual(
            public_normal.fundamental_syndromes,
            canonical_normal.fundamental_syndromes,
        )
        self.assertTrue(
            all(
                public_normal.normalized_transitions[index] == 0
                for index in public_normal.tree_edge_indices
            )
        )

    def test_hidden_face_gauge_is_publicly_recovered_up_to_one_bit(self) -> None:
        parameters = KLEIN_BOTTLE_PARAMETER_SETS["klein-bottle-5x4"]
        public, reference = generate_klein_orientation_instance(
            parameters,
            MASTER_SEED,
        )
        recovery = recover_klein_gauge(public)
        self.assertTrue(recovery.consistent)
        self.assertEqual(
            recovery.edge_checks,
            len(public.scaffold.dual_edges),
        )
        self.assertTrue(reference_gauge_matches(recovery, reference))


if __name__ == "__main__":
    unittest.main()
