from __future__ import annotations

import unittest

from morph_kem.tdc_lifted_graphic import (
    TDC1Error,
    TDC1Parameters,
    TDC1_PARAMETER_SETS,
    decode_graphic_error,
    generate_tdc1_instance,
    graphic_code_metrics,
    planted_error_mask,
    recover_k4_quotient,
)


class TDC1LiftedGraphicTests(unittest.TestCase):
    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(TDC1Error):
            TDC1Parameters("bad", 2, (1, 2)).validate()
        with self.assertRaises(TDC1Error):
            TDC1Parameters("bad", 8, (2, 2)).validate()
        with self.assertRaises(TDC1Error):
            generate_tdc1_instance(TDC1_PARAMETER_SETS["tdc1-L8"], b"short")

    def test_lift_and_random_controls_are_matched_cubic_codes(self) -> None:
        params = TDC1_PARAMETER_SETS["tdc1-L8"]
        instance = generate_tdc1_instance(params, b"TDC1 matched graph unit seed v1")
        lifted = graphic_code_metrics(instance.lifted)
        random_control = graphic_code_metrics(instance.matched_random)
        self.assertEqual(lifted.vertices, random_control.vertices)
        self.assertEqual(lifted.edges, random_control.edges)
        self.assertEqual(lifted.degree_histogram, ((3, lifted.vertices),))
        self.assertEqual(random_control.degree_histogram, ((3, random_control.vertices),))
        self.assertEqual(lifted.parity_rank, lifted.vertices - 1)
        self.assertEqual(random_control.parity_rank, random_control.vertices - 1)
        self.assertEqual(lifted.code_dimension, random_control.code_dimension)
        self.assertGreaterEqual(lifted.girth, 3)
        self.assertGreaterEqual(random_control.girth, 3)

    def test_public_k4_quotient_is_recoverable(self) -> None:
        params = TDC1_PARAMETER_SETS["tdc1-L8"]
        instance = generate_tdc1_instance(params, b"TDC1 quotient recovery unit seed v1")
        recovery = recover_k4_quotient(instance.lifted, params.lift_factor)
        self.assertTrue(recovery.found)
        self.assertEqual(recovery.color_class_sizes, (8, 8, 8, 8))
        self.assertGreater(recovery.search_nodes, 0)

    def test_graphic_syndrome_decoder_recovers_equivalent_error(self) -> None:
        params = TDC1_PARAMETER_SETS["tdc1-L12"]
        instance = generate_tdc1_instance(params, b"TDC1 decoder unit seed v1")
        error = planted_error_mask(instance.lifted, 4, b"TDC1 planted error unit v1")
        recovery = decode_graphic_error(instance.lifted, error)
        self.assertTrue(recovery.accepted)
        self.assertLessEqual(recovery.recovered_error_weight, 4)
        self.assertEqual(recovery.matching_distance, recovery.recovered_error_weight)

    def test_break_is_stable_across_seeds(self) -> None:
        params = TDC1_PARAMETER_SETS["tdc1-L8"]
        for index in range(4):
            seed = (f"TDC1 deterministic seed {index:02d} v1").encode().ljust(40, b".")
            instance = generate_tdc1_instance(params, seed)
            quotient = recover_k4_quotient(instance.lifted, params.lift_factor)
            self.assertTrue(quotient.found)
            error = planted_error_mask(instance.lifted, 3, seed + b" error")
            decoded = decode_graphic_error(instance.lifted, error)
            self.assertTrue(decoded.accepted)


if __name__ == "__main__":
    unittest.main()
