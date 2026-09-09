import unittest

from morph_kem import SimplicialComplex


class SimplicialComplexTests(unittest.TestCase):
    def test_from_facets_builds_downward_closure(self) -> None:
        complex_ = SimplicialComplex.from_facets([(0, 1, 2)])
        self.assertEqual(complex_.dimension, 2)
        self.assertEqual(len(complex_.simplices), 7)
        self.assertTrue(complex_.contains((0, 1)))
        self.assertTrue(complex_.contains((0, 1, 2)))

    def test_canonical_round_trip(self) -> None:
        complex_ = SimplicialComplex.from_facets([(9, 2, 5), (100, 101)])
        encoded = complex_.encode()
        self.assertEqual(SimplicialComplex.decode(encoded), complex_)
        self.assertEqual(SimplicialComplex.decode(encoded).encode(), encoded)

    def test_decode_rejects_trailing_data(self) -> None:
        encoded = SimplicialComplex.from_facets([(0, 1)]).encode()
        with self.assertRaises(ValueError):
            SimplicialComplex.decode(encoded + b"\x00")

    def test_elementary_expand_is_inverse_of_collapse(self) -> None:
        base = SimplicialComplex.from_facets([(0, 1), (0, 2)])
        expanded = base.elementary_expand((1, 2), (0, 1, 2))
        self.assertIn(((1, 2), (0, 1, 2)), expanded.free_collapse_pairs())
        self.assertEqual(expanded.collapse((1, 2), (0, 1, 2)), base)

    def test_elementary_expand_rejects_missing_required_face(self) -> None:
        base = SimplicialComplex.from_facets([(0, 1)])
        with self.assertRaises(ValueError):
            base.elementary_expand((1, 2), (0, 1, 2))

    def test_free_pairs_include_all_triangle_edges_when_triangle_is_isolated_facet(self) -> None:
        complex_ = SimplicialComplex.from_facets([(0, 1, 2)])
        pairs = complex_.free_collapse_pairs()
        self.assertEqual(
            set(pairs),
            {
                ((0, 1), (0, 1, 2)),
                ((0, 2), (0, 1, 2)),
                ((1, 2), (0, 1, 2)),
            },
        )

    def test_collapse_rejects_nonfree_face(self) -> None:
        complex_ = SimplicialComplex.from_facets([(0, 1, 2), (1, 2, 3)])
        with self.assertRaises(ValueError):
            complex_.collapse((1, 2), (0, 1, 2))


if __name__ == "__main__":
    unittest.main()
