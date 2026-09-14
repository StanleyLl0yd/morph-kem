from __future__ import annotations

import hashlib
import unittest

from morph_kem.nat_noisy_sl2_trace import (
    NAT10Error,
    NAT10Parameters,
    NAT10_PARAMETER_SETS,
    identity,
    inverse,
    multiply,
    generate_nat10_instance,
    recover_nat10,
    sl2_group,
    validate_nat10_representation,
)


def digest(label: str) -> bytes:
    return hashlib.sha256(label.encode("ascii")).digest()


class NAT10NoisySL2TraceTests(unittest.TestCase):
    def test_group_sizes_and_inverses(self) -> None:
        self.assertEqual(len(sl2_group(5)), 120)
        self.assertEqual(len(sl2_group(7)), 336)
        for p in (5, 7):
            for value in sl2_group(p)[:: max(1, len(sl2_group(p)) // 17)]:
                self.assertEqual(multiply(value, inverse(value, p), p), identity())

    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(NAT10Error):
            NAT10Parameters("bad", 11, ("A", "B", "C", "D")).validate()
        with self.assertRaises(NAT10Error):
            generate_nat10_instance(NAT10_PARAMETER_SETS["nat10-p5-G4"], b"short")

    def test_generation_is_deterministic_and_planted_verifies(self) -> None:
        params = NAT10_PARAMETER_SETS["nat10-p5-X8"]
        seed = digest("NAT10 deterministic unit v1")
        public1, reference1 = generate_nat10_instance(params, seed)
        public2, reference2 = generate_nat10_instance(params, seed)
        self.assertEqual(public1, public2)
        self.assertEqual(reference1, reference2)
        self.assertTrue(
            validate_nat10_representation(public1, reference1.planted_generators)
        )

    def test_public_recovery_needs_no_reference(self) -> None:
        for name in ("nat10-p5-G4", "nat10-p5-X8"):
            params = NAT10_PARAMETER_SETS[name]
            public, reference = generate_nat10_instance(
                params, digest(f"NAT10 recovery unit {name} v1")
            )
            recovery = recover_nat10(public)
            self.assertTrue(recovery.accepted)
            self.assertGreater(recovery.accepted_representations, 0)
            self.assertGreater(recovery.conjugacy_orbit_lower_bound, 0)
            assert recovery.recovered_generators is not None
            self.assertTrue(
                validate_nat10_representation(public, recovery.recovered_generators)
            )
            with_reference = recover_nat10(public, reference=reference)
            self.assertEqual(recovery.recovered_generators, with_reference.recovered_generators)

    def test_p7_single_recovery(self) -> None:
        params = NAT10_PARAMETER_SETS["nat10-p7-X8"]
        public, _ = generate_nat10_instance(params, digest("NAT10 p7 unit v1"))
        recovery = recover_nat10(public)
        self.assertTrue(recovery.accepted)
        self.assertGreater(recovery.verifier_candidates_tested, 0)


if __name__ == "__main__":
    unittest.main()
