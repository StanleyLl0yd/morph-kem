from __future__ import annotations

import unittest

from morph_kem.tdc_cycle_code import (
    TDC0_PARAMETER_SETS,
    TDCError,
    TDCParameters,
    cycle_code_metrics,
    generate_tdc0_instance,
    planted_single_edge_syndrome,
    recover_single_edge_error,
)


MASTER_SEED = bytes.fromhex("102132435465768798a9bacbdcedfe0f")


class TDCCycleCodeTests(unittest.TestCase):
    def test_public_cycle_code_has_exact_low_weight_structure(self) -> None:
        for name, params in TDC0_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public, _ = generate_tdc0_instance(params, MASTER_SEED)
                metrics = cycle_code_metrics(public)
                cells = params.rows * params.cols
                self.assertEqual(metrics.vertices, cells)
                self.assertEqual(metrics.edges, 3 * cells)
                self.assertEqual(metrics.triangles, 2 * cells)
                self.assertEqual(metrics.parity_rank, cells - 1)
                self.assertEqual(metrics.code_dimension, 2 * cells + 1)
                self.assertEqual(metrics.column_weight_histogram, ((2, 3 * cells),))
                self.assertEqual(metrics.triangle_codeword_count, 2 * cells)
                self.assertEqual(
                    metrics.triangle_codeword_weight_histogram,
                    ((3, 2 * cells),),
                )
                self.assertEqual(metrics.exact_minimum_distance, 3)

    def test_single_edge_error_is_publicly_decoded(self) -> None:
        for name, params in TDC0_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public, reference = generate_tdc0_instance(params, MASTER_SEED)
                syndrome = planted_single_edge_syndrome(public, reference)
                recovery = recover_single_edge_error(
                    public, syndrome, reference=reference
                )
                self.assertTrue(recovery.accepted)
                self.assertTrue(recovery.matches_reference_after_public_success)
                self.assertEqual(recovery.syndrome_weight, 2)
                self.assertEqual(recovery.lookup_entries, 3 * params.rows * params.cols)

    def test_decoder_does_not_need_reference(self) -> None:
        public, reference = generate_tdc0_instance(
            TDC0_PARAMETER_SETS["tdc0-6x6"], MASTER_SEED
        )
        recovery = recover_single_edge_error(
            public, planted_single_edge_syndrome(public, reference)
        )
        self.assertTrue(recovery.accepted)
        self.assertIsNone(recovery.matches_reference_after_public_success)

    def test_break_is_stable_across_public_relabeling_seeds(self) -> None:
        params = TDC0_PARAMETER_SETS["tdc0-8x8"]
        for seed_index in range(8):
            with self.subTest(seed=seed_index):
                seed = bytes([seed_index + 1]) * 32
                public, reference = generate_tdc0_instance(params, seed)
                metrics = cycle_code_metrics(public)
                recovery = recover_single_edge_error(
                    public,
                    planted_single_edge_syndrome(public, reference),
                    reference=reference,
                )
                self.assertEqual(metrics.exact_minimum_distance, 3)
                self.assertTrue(recovery.accepted)
                self.assertTrue(recovery.matches_reference_after_public_success)

    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(TDCError):
            TDCParameters("small", 2, 4).validate()
        with self.assertRaises(TDCError):
            generate_tdc0_instance(TDC0_PARAMETER_SETS["tdc0-4x4"], b"short")


if __name__ == "__main__":
    unittest.main()
