import struct
import unittest

from morph_kem import ComplexEncodingError, SimplicialComplex


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
        with self.assertRaises(ComplexEncodingError):
            SimplicialComplex.decode(encoded + b"\x00")

    def test_decode_rejects_noncanonical_vertex_order(self) -> None:
        data = b"MKSC\x01" + struct.pack(">I", 1) + bytes([2]) + struct.pack(">II", 2, 1)
        with self.assertRaises(ComplexEncodingError):
            SimplicialComplex.decode(data)

    def test_decode_rejects_non_closed_complex(self) -> None:
        data = b"MKSC\x01" + struct.pack(">I", 1) + bytes([3]) + struct.pack(">III", 0, 1, 2)
        with self.assertRaises(ComplexEncodingError):
            SimplicialComplex.decode(data)

    def test_elementary_collapse(self) -> None:
        base = SimplicialComplex.from_facets([(0, 1), (0, 2)])
        expanded = base.add_facets([(0, 1, 2)])
        reduced = expanded.collapse((1, 2), (0, 1, 2))
        self.assertEqual(reduced, base)

    def test_collapse_rejects_nonfree_face(self) -> None:
        complex_ = SimplicialComplex.from_facets([(0, 1, 2), (1, 2, 3)])
        with self.assertRaises(ValueError):
            complex_.collapse((1, 2), (0, 1, 2))


if __name__ == "__main__":
    unittest.main()
