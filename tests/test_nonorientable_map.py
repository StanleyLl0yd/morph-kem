import unittest

from morph_kem.nonorientable_map import (
    analyze_cell_orientability,
    build_orientation_double_cover,
    generate_k1_orientation_instance,
    generate_n4_6_4_3_map,
    k1_reference_gauge_matches,
    normalize_cell_transitions,
    recover_k1_gauge,
    regular_type_is_hyperbolic,
    validate_k1_reference,
)

MASTER_SEED = bytes.fromhex("34016490ffeeddccbbaa1234567890ab")


class K1NonOrientableHyperbolicTests(unittest.TestCase):
    def test_exact_n4_regular_map_invariants(self) -> None:
        cell_map = generate_n4_6_4_3_map()
        self.assertEqual(len(cell_map.vertices), 6)
        self.assertEqual(len(cell_map.edges), 12)
        self.assertEqual(len(cell_map.faces), 4)
        self.assertEqual(set(cell_map.vertex_degrees), {4})
        self.assertEqual(set(cell_map.face_sizes), {6})
        self.assertEqual(set(cell_map.edge_face_degrees), {2})
        self.assertEqual(cell_map.euler_characteristic, -2)
        self.assertEqual(cell_map.dual_cycle_rank, 9)
        self.assertTrue(regular_type_is_hyperbolic(6, 4))

        orientation = analyze_cell_orientability(cell_map)
        self.assertFalse(orientation.orientable)
        self.assertGreater(orientation.nonzero_syndromes, 0)

    def test_underlying_graph_is_k222(self) -> None:
        cell_map = generate_n4_6_4_3_map()
        opposite = {(0, 1), (2, 3), (4, 5)}
        expected = {
            (left, right)
            for left in range(6)
            for right in range(left + 1, 6)
            if (left, right) not in opposite
        }
        self.assertEqual(set(cell_map.edges), expected)

    def test_public_generation_is_deterministic(self) -> None:
        public1, reference1 = generate_k1_orientation_instance(MASTER_SEED)
        public2, reference2 = generate_k1_orientation_instance(MASTER_SEED)
        self.assertEqual(public1.encode(), public2.encode())
        self.assertEqual(reference1, reference2)
        self.assertTrue(validate_k1_reference(public1, reference1))

    def test_hidden_face_gauge_is_recovered_up_to_one_bit(self) -> None:
        public, reference = generate_k1_orientation_instance(MASTER_SEED)
        recovery = recover_k1_gauge(public)
        self.assertTrue(recovery.consistent)
        self.assertEqual(recovery.edge_checks, 12)
        self.assertTrue(k1_reference_gauge_matches(recovery, reference))

        public_normal = normalize_cell_transitions(
            public.base_map,
            public.transitions,
        )
        canonical = tuple(
            edge.canonical_transition
            for edge in public.base_map.dual_edges
        )
        canonical_normal = normalize_cell_transitions(
            public.base_map,
            canonical,
        )
        self.assertEqual(
            public_normal.normalized_transitions,
            canonical_normal.normalized_transitions,
        )

    def test_public_orientation_double_cover_is_orientable_genus3(self) -> None:
        public, _ = generate_k1_orientation_instance(MASTER_SEED)
        lifted = build_orientation_double_cover(
            public.base_map,
            public.transitions,
        )
        cover = lifted.cover
        self.assertTrue(lifted.reconstructed_from_public_transitions)
        self.assertEqual(len(cover.vertices), 12)
        self.assertEqual(len(cover.edges), 24)
        self.assertEqual(len(cover.faces), 8)
        self.assertEqual(cover.euler_characteristic, -4)
        self.assertEqual(set(cover.vertex_degrees), {4})
        self.assertEqual(set(cover.face_sizes), {6})
        self.assertEqual(set(cover.edge_face_degrees), {2})
        self.assertTrue(analyze_cell_orientability(cover).orientable)
        self.assertEqual((2 - cover.euler_characteristic) // 2, 3)

        for original_vertex in public.base_map.vertices:
            self.assertEqual(
                lifted.vertex_projection.count(original_vertex),
                2,
            )
        for original_face in range(len(public.base_map.faces)):
            self.assertEqual(
                lifted.face_projection.count(original_face),
                2,
            )


if __name__ == "__main__":
    unittest.main()
