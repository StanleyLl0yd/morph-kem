from __future__ import annotations

import unittest

from morph_kem.gluing import GluingExperimentError
from morph_kem.gluing_random_pairing import (
    G13_PARAMETER_SETS,
    RandomPairingParameters,
    attempt_random_pairing_surface,
    audit_random_pairing_generator,
)


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


class RandomPairingGeneratorTests(unittest.TestCase):
    def test_audit_accounts_for_every_attempt(self) -> None:
        for name, params in G13_PARAMETER_SETS.items():
            with self.subTest(name=name):
                audit = audit_random_pairing_generator(
                    params, MASTER_SEED, attempts=64
                )
                counts = dict(audit.reason_counts)
                self.assertEqual(sum(counts.values()), 64)
                self.assertEqual(counts["success"], audit.successes)
                self.assertEqual(audit.success_rate, audit.successes / 64)
                self.assertGreaterEqual(counts["dual_loop"] + counts["dual_parallel"], 1)

    def test_attempt_is_deterministic(self) -> None:
        params = G13_PARAMETER_SETS["g13-36"]
        for index in range(16):
            first = attempt_random_pairing_surface(params, MASTER_SEED, index)
            second = attempt_random_pairing_surface(params, MASTER_SEED, index)
            self.assertEqual(first, second)

    def test_success_surface_invariants_if_observed(self) -> None:
        params = G13_PARAMETER_SETS["g13-36"]
        for index in range(256):
            result = attempt_random_pairing_surface(params, MASTER_SEED, index)
            if result.surface is None:
                continue
            surface = result.surface
            self.assertEqual(len(surface.triangles), params.triangle_count)
            self.assertEqual(surface.edges, 3 * params.triangle_count // 2)
            self.assertEqual(
                surface.euler_characteristic,
                surface.vertices - surface.edges + params.triangle_count,
            )
            self.assertEqual(surface.euler_characteristic, 2 - 2 * surface.genus)

    def test_rule_of_three_bound_for_zero_success_audit(self) -> None:
        params = G13_PARAMETER_SETS["g13-36"]
        audit = audit_random_pairing_generator(params, MASTER_SEED, attempts=32)
        if audit.successes == 0:
            self.assertEqual(audit.zero_success_rule_of_three_upper, 3.0 / 32)
        else:
            self.assertEqual(audit.zero_success_rule_of_three_upper, 0.0)

    def test_parameter_seed_attempt_bounds(self) -> None:
        with self.assertRaises(GluingExperimentError):
            RandomPairingParameters("too-small", 6).validate()
        with self.assertRaises(GluingExperimentError):
            RandomPairingParameters("odd", 15).validate()
        with self.assertRaises(GluingExperimentError):
            RandomPairingParameters("not-divisible-by-three", 20).validate()
        with self.assertRaises(GluingExperimentError):
            attempt_random_pairing_surface(
                G13_PARAMETER_SETS["g13-36"], b"short", 0
            )
        with self.assertRaises(GluingExperimentError):
            attempt_random_pairing_surface(
                G13_PARAMETER_SETS["g13-36"], MASTER_SEED, -1
            )
        for attempts in (0, 100_001):
            with self.assertRaises(GluingExperimentError):
                audit_random_pairing_generator(
                    G13_PARAMETER_SETS["g13-36"], MASTER_SEED, attempts=attempts
                )


if __name__ == "__main__":
    unittest.main()
