from __future__ import annotations

import unittest

from morph_kem.tdc_sparse_faces import (
    TDC2SparseError,
    TDC2SparseParameters,
    TDC2_SPARSE_PARAMETER_SETS,
    generate_tdc2_sparse_instance,
    sparse_face_metrics,
    topology_sparse_face_metrics,
)


class TDC2SparseFaceTests(unittest.TestCase):
    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(TDC2SparseError):
            TDC2SparseParameters("bad", 7).validate()
        with self.assertRaises(TDC2SparseError):
            generate_tdc2_sparse_instance(
                TDC2_SPARSE_PARAMETER_SETS["tdc2b-n8"], b"short"
            )

    def test_topology_generator_removes_all_tetrahedron_boundaries(self) -> None:
        params = TDC2_SPARSE_PARAMETER_SETS["tdc2b-n8"]
        seed = b"TDC2b tetra-free unit seed v1........"
        instance = generate_tdc2_sparse_instance(params, seed)
        metrics = topology_sparse_face_metrics(params, seed, instance.topology_code)
        self.assertEqual(metrics.tetrahedron_boundary_count, 0)
        self.assertEqual(metrics.column_weight_histogram, ((3, metrics.columns),))
        self.assertTrue(metrics.graphic_column_weight_obstruction)
        self.assertIsNone(
            metrics.minimum_weight_leq6
            if metrics.minimum_weight_leq6 is not None and metrics.minimum_weight_leq6 <= 4
            else None
        )
        self.assertGreater(instance.skipped_tetrahedron_completions, 0)

    def test_matched_random_preserves_exact_degree_profiles(self) -> None:
        params = TDC2_SPARSE_PARAMETER_SETS["tdc2b-n9"]
        seed = b"TDC2b matched random unit seed v1....."
        instance = generate_tdc2_sparse_instance(params, seed)
        topology = topology_sparse_face_metrics(params, seed, instance.topology_code)
        random_control = sparse_face_metrics(instance.matched_random)
        self.assertEqual(topology.rows, random_control.rows)
        self.assertEqual(topology.columns, random_control.columns)
        self.assertEqual(topology.row_weight_histogram, random_control.row_weight_histogram)
        self.assertEqual(topology.column_weight_histogram, random_control.column_weight_histogram)

    def test_tetra_free_property_is_stable_across_seeds(self) -> None:
        params = TDC2_SPARSE_PARAMETER_SETS["tdc2b-n10"]
        for index in range(4):
            seed = (f"TDC2b deterministic seed {index:02d} v1").encode().ljust(48, b".")
            instance = generate_tdc2_sparse_instance(params, seed)
            metrics = topology_sparse_face_metrics(params, seed, instance.topology_code)
            self.assertEqual(metrics.tetrahedron_boundary_count, 0)
            self.assertTrue(metrics.graphic_column_weight_obstruction)
            if metrics.minimum_weight_leq6 is not None:
                self.assertGreaterEqual(metrics.minimum_weight_leq6, 5)


if __name__ == "__main__":
    unittest.main()
