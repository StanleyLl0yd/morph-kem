from __future__ import annotations

import hashlib
import unittest

from morph_kem.tdc_decoder_reliability import (
    reliability_guided_decode_leq6,
    reliability_order,
)
from morph_kem.tdc_decoder_work import (
    TDC3_PARAMETER_SETS,
    generate_tdc3_instance,
    planted_error_mask,
    syndrome,
)


def digest(label: str) -> bytes:
    return hashlib.sha256(label.encode("ascii")).digest()


class TDC3ReliabilityTests(unittest.TestCase):
    def test_single_error_is_in_top_pool_and_decodes(self) -> None:
        params = TDC3_PARAMETER_SETS["tdc3-n10"]
        instance = generate_tdc3_instance(params, digest("TDC3 reliability unit v1"))
        planted = planted_error_mask(instance, 1)
        planted_index = (planted & -planted).bit_length() - 1
        for code in (instance.pair.topology, instance.pair.matched_random):
            target = syndrome(code, planted)
            order = reliability_order(code, target)
            self.assertIn(planted_index, order[:24])
            recovered = reliability_guided_decode_leq6(code, target, pool_size=24)
            self.assertTrue(recovered.accepted)
            self.assertLessEqual(recovered.recovered_weight, 1)

    def test_public_recovery_is_self_verifying(self) -> None:
        params = TDC3_PARAMETER_SETS["tdc3-n9"]
        instance = generate_tdc3_instance(params, digest("TDC3 reliability verify unit v1"))
        planted = planted_error_mask(instance, 4)
        target = syndrome(instance.pair.topology, planted)
        recovered = reliability_guided_decode_leq6(
            instance.pair.topology, target, pool_size=24
        )
        if recovered.accepted:
            self.assertEqual(
                syndrome(instance.pair.topology, recovered.recovered_error_mask), target
            )
        self.assertEqual(recovered.pool_size, 24)
        self.assertGreater(recovered.subset_masks_indexed, 0)

    def test_declared_small_sweep_is_deterministic(self) -> None:
        params = TDC3_PARAMETER_SETS["tdc3-n8"]
        seed = digest("TDC3 reliability deterministic unit v1")
        first = generate_tdc3_instance(params, seed)
        second = generate_tdc3_instance(params, seed)
        planted_first = planted_error_mask(first, 3)
        planted_second = planted_error_mask(second, 3)
        self.assertEqual(planted_first, planted_second)
        target_first = syndrome(first.pair.topology, planted_first)
        target_second = syndrome(second.pair.topology, planted_second)
        self.assertEqual(
            reliability_guided_decode_leq6(first.pair.topology, target_first),
            reliability_guided_decode_leq6(second.pair.topology, target_second),
        )


if __name__ == "__main__":
    unittest.main()
