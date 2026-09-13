from __future__ import annotations

import hashlib
import unittest

from morph_kem.nat_a5_torus_direct import recover_nat6_direct
from morph_kem.nat_a5_torus_flat import NAT6_PARAMETER_SETS, generate_nat6_instance


def seed_for(label: str) -> bytes:
    return hashlib.sha256(label.encode("ascii")).digest()


class NAT6DirectHolonomyTests(unittest.TestCase):
    def test_direct_public_recovery_needs_no_reference(self) -> None:
        params = NAT6_PARAMETER_SETS["nat6-6x6"]
        public, _ = generate_nat6_instance(params, seed_for("nat6-direct-public"))
        recovery = recover_nat6_direct(public)
        self.assertTrue(recovery.accepted)
        self.assertIsNone(recovery.pair_matches_planted_after_public_success)
        self.assertIsNone(recovery.gauge_matches_planted_after_public_success)

    def test_direct_recovery_matches_reference_after_success(self) -> None:
        for params in NAT6_PARAMETER_SETS.values():
            for index in range(4):
                public, reference = generate_nat6_instance(
                    params, seed_for(f"nat6-direct-{params.name}-{index}")
                )
                recovery = recover_nat6_direct(public, reference=reference)
                self.assertTrue(recovery.accepted)
                self.assertTrue(recovery.pair_matches_planted_after_public_success)
                self.assertTrue(recovery.gauge_matches_planted_after_public_success)
                self.assertNotEqual(recovery.first_pairing_vector, (0, 0))
                self.assertNotEqual(recovery.second_pairing_vector, (0, 0))
                self.assertNotEqual(
                    recovery.first_pairing_vector,
                    recovery.second_pairing_vector,
                )
                self.assertEqual(
                    recovery.propagation_assignments,
                    len(public.target.vertices) - 1,
                )


if __name__ == "__main__":
    unittest.main()
