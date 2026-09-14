from __future__ import annotations

import hashlib
import unittest

from morph_kem.tdc_prange_isd import (
    TDC3BError,
    TDC3BParameters,
    TDC3B_PARAMETER_SETS,
    generate_tdc3b_instance,
    information_set,
    prange_decode,
    recover_tdc3b_weight,
)
from morph_kem.tdc_decoder_work import planted_error_mask, syndrome


def digest(label: str) -> bytes:
    return hashlib.sha256(label.encode("ascii")).digest()


class TDC3BPrangeISDTests(unittest.TestCase):
    def test_parameter_bounds(self) -> None:
        with self.assertRaises(TDC3BError):
            TDC3BParameters("bad", "tdc3-n8", (4, 8, 16)).validate()
        with self.assertRaises(TDC3BError):
            TDC3BParameters("bad", "missing").validate()

    def test_information_set_is_deterministic_and_sized_to_rank(self) -> None:
        params = TDC3B_PARAMETER_SETS["tdc3b-n8"]
        instance = generate_tdc3b_instance(params, digest("TDC3b information set unit v1"))
        planted = planted_error_mask(instance, 3)
        target = syndrome(instance.pair.topology, planted)
        first = information_set(instance.pair.topology, target, 0)
        second = information_set(instance.pair.topology, target, 0)
        self.assertEqual(first, second)
        self.assertEqual(len(first), instance.pair.topology.row_count)
        self.assertEqual(len(set(first)), len(first))

    def test_public_recovery_verifies_when_accepted(self) -> None:
        params = TDC3B_PARAMETER_SETS["tdc3b-n9"]
        instance = generate_tdc3b_instance(params, digest("TDC3b public recovery unit v1"))
        planted = planted_error_mask(instance, 2)
        target = syndrome(instance.pair.topology, planted)
        recovery = prange_decode(instance.pair.topology, target, 2)
        if recovery.accepted:
            self.assertEqual(
                syndrome(instance.pair.topology, recovery.recovered_error_mask), target
            )
            self.assertLessEqual(recovery.recovered_weight, 2)
            self.assertIsNotNone(recovery.first_success_trial)
        self.assertEqual(tuple(b for b, _ in recovery.success_by_budget), (8, 32, 128))
        self.assertGreater(recovery.trials_attempted, 0)

    def test_pair_recovery_uses_same_planted_support_only_as_target(self) -> None:
        params = TDC3B_PARAMETER_SETS["tdc3b-n10"]
        instance = generate_tdc3b_instance(params, digest("TDC3b pair recovery unit v1"))
        result = recover_tdc3b_weight(instance, 1)
        self.assertTrue(result.topology.accepted)
        self.assertTrue(result.matched_random.accepted)
        self.assertLessEqual(result.topology.recovered_weight, 1)
        self.assertLessEqual(result.matched_random.recovered_weight, 1)

    def test_small_sweep_runs_all_declared_weights(self) -> None:
        params = TDC3B_PARAMETER_SETS["tdc3b-n8"]
        instance = generate_tdc3b_instance(params, digest("TDC3b small sweep unit v1"))
        for weight in instance.params.error_weights:
            result = recover_tdc3b_weight(instance, weight)
            self.assertEqual(result.planted_weight, weight)
            self.assertLessEqual(result.topology.trials_attempted, 128)
            self.assertLessEqual(result.matched_random.trials_attempted, 128)


if __name__ == "__main__":
    unittest.main()
