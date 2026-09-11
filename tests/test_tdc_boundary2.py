from __future__ import annotations

import unittest
from math import comb

from morph_kem.tdc_boundary2 import (
    TDC2Error,
    TDC2Parameters,
    TDC2_PARAMETER_SETS,
    boundary_code_metrics,
    generate_tdc2_instance,
)


class TDC2BoundaryTests(unittest.TestCase):
    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(TDC2Error):
            TDC2Parameters("bad", 5).validate()
        with self.assertRaises(TDC2Error):
            generate_tdc2_instance(TDC2_PARAMETER_SETS["tdc2-n6"], b"short")

    def test_topology_code_is_non_graphic_and_has_tetrahedron_words(self) -> None:
        params = TDC2_PARAMETER_SETS["tdc2-n7"]
        instance = generate_tdc2_instance(params, b"TDC2 topology unit seed v1")
        metrics = boundary_code_metrics(instance.topology_code)
        self.assertTrue(metrics.graphic_column_weight_obstruction)
        self.assertEqual(metrics.column_weight_histogram, ((3, comb(7, 3)),))
        self.assertEqual(metrics.row_weight_histogram, ((5, comb(7, 2)),))
        self.assertIsNone(metrics.minimum_weight_leq3)
        self.assertEqual(metrics.weight4_codewords, comb(7, 4))
        self.assertEqual(instance.expected_tetrahedron_boundaries, comb(7, 4))

    def test_rank_and_dimension_match_full_simplex_boundary(self) -> None:
        for params in TDC2_PARAMETER_SETS.values():
            instance = generate_tdc2_instance(params, b"TDC2 rank unit seed v1" + params.name.encode())
            metrics = boundary_code_metrics(instance.topology_code)
            expected_rank = comb(params.vertex_count, 2) - params.vertex_count + 1
            expected_dimension = comb(params.vertex_count, 3) - expected_rank
            self.assertEqual(metrics.rank, expected_rank)
            self.assertEqual(metrics.dimension, expected_dimension)

    def test_matched_random_has_identical_degree_profile(self) -> None:
        params = TDC2_PARAMETER_SETS["tdc2-n8"]
        instance = generate_tdc2_instance(params, b"TDC2 random control unit seed v1")
        topology = boundary_code_metrics(instance.topology_code)
        random_control = boundary_code_metrics(instance.matched_random)
        self.assertEqual(topology.rows, random_control.rows)
        self.assertEqual(topology.columns, random_control.columns)
        self.assertEqual(topology.row_weight_histogram, random_control.row_weight_histogram)
        self.assertEqual(topology.column_weight_histogram, random_control.column_weight_histogram)

    def test_break_is_stable_across_public_relabeling_seeds(self) -> None:
        params = TDC2_PARAMETER_SETS["tdc2-n8"]
        for index in range(8):
            seed = (f"TDC2 deterministic seed {index:02d} v1").encode().ljust(40, b".")
            instance = generate_tdc2_instance(params, seed)
            metrics = boundary_code_metrics(instance.topology_code)
            self.assertIsNone(metrics.minimum_weight_leq3)
            self.assertEqual(metrics.weight4_codewords, comb(8, 4))
            self.assertTrue(metrics.graphic_column_weight_obstruction)


if __name__ == "__main__":
    unittest.main()
