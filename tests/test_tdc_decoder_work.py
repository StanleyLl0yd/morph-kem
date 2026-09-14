from __future__ import annotations

import hashlib
import unittest

from morph_kem.tdc_decoder_work import (
    TDC3Error,
    TDC3Parameters,
    TDC3_PARAMETER_SETS,
    bitflip_decode,
    exact_syndrome_decode_leq6,
    generate_tdc3_instance,
    planted_error_mask,
    recover_tdc3_weight,
    syndrome,
)


def digest(label: str) -> bytes:
    return hashlib.sha256(label.encode("ascii")).digest()


class TDC3DecoderWorkTests(unittest.TestCase):
    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(TDC3Error):
            TDC3Parameters("bad", "missing", (1,)).validate()
        with self.assertRaises(TDC3Error):
            generate_tdc3_instance(TDC3_PARAMETER_SETS["tdc3-n8"], b"short")

    def test_common_error_support_is_deterministic(self) -> None:
        params = TDC3_PARAMETER_SETS["tdc3-n9"]
        seed = digest("TDC3 common support unit v1")
        first = generate_tdc3_instance(params, seed)
        second = generate_tdc3_instance(params, seed)
        for weight in params.error_weights:
            self.assertEqual(
                planted_error_mask(first, weight), planted_error_mask(second, weight)
            )

    def test_exact_decoder_accepts_declared_weights(self) -> None:
        params = TDC3_PARAMETER_SETS["tdc3-n8"]
        instance = generate_tdc3_instance(params, digest("TDC3 exact decoder unit v1"))
        for weight in params.error_weights:
            planted = planted_error_mask(instance, weight)
            for code in (instance.pair.topology, instance.pair.matched_random):
                target = syndrome(code, planted)
                recovery = exact_syndrome_decode_leq6(code, target)
                self.assertTrue(recovery.accepted)
                self.assertLessEqual(recovery.recovered_weight, weight)
                self.assertGreater(recovery.subset_masks_indexed, 0)

    def test_bitflip_public_result_is_self_verifying_when_accepted(self) -> None:
        params = TDC3_PARAMETER_SETS["tdc3-n10"]
        instance = generate_tdc3_instance(params, digest("TDC3 bitflip unit v1"))
        planted = planted_error_mask(instance, 2)
        target = syndrome(instance.pair.topology, planted)
        recovery = bitflip_decode(
            instance.pair.topology, target, params.bitflip_max_iterations
        )
        if recovery.accepted:
            self.assertEqual(
                syndrome(instance.pair.topology, recovery.recovered_error_mask), target
            )
        self.assertGreater(recovery.score_evaluations, 0)

    def test_pair_recovery_needs_no_reference_secret(self) -> None:
        params = TDC3_PARAMETER_SETS["tdc3-n8"]
        instance = generate_tdc3_instance(params, digest("TDC3 pair unit v1"))
        result = recover_tdc3_weight(instance, 4)
        self.assertTrue(result.topology_exact.accepted)
        self.assertTrue(result.random_exact.accepted)
        self.assertLessEqual(result.topology_exact.recovered_weight, 4)
        self.assertLessEqual(result.random_exact.recovered_weight, 4)


if __name__ == "__main__":
    unittest.main()
