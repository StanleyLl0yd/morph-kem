from __future__ import annotations

import unittest

from morph_kem.nat_s3 import NAT2_PARAMETER_SETS, generate_nat2_instance
from morph_kem.nat_s3_support import recover_from_sign_support


class NAT2SupportTests(unittest.TestCase):
    def test_single_error_support_propagates_exact_state(self) -> None:
        params = NAT2_PARAMETER_SETS["nat2-F24"]
        public, reference = generate_nat2_instance(
            params, b"NAT2 support unit seed single v1....", 1
        )
        result = recover_from_sign_support(public, reference=reference)
        self.assertTrue(result.clean_subgraph_connected)
        self.assertTrue(result.propagation_consistent)
        self.assertTrue(result.exact_state_accepted)
        self.assertTrue(result.support_matches_planted_after_public_success)
        self.assertTrue(result.state_matches_hidden_after_public_success)

    def test_support_attack_needs_no_reference(self) -> None:
        params = NAT2_PARAMETER_SETS["nat2-F30"]
        public, _ = generate_nat2_instance(
            params, b"NAT2 support public only seed v1.....", 2
        )
        result = recover_from_sign_support(public)
        self.assertTrue(result.clean_subgraph_connected)
        self.assertTrue(result.propagation_consistent)
        self.assertTrue(result.exact_state_accepted)
        self.assertIsNone(result.support_matches_planted_after_public_success)
        self.assertIsNone(result.state_matches_hidden_after_public_success)

    def test_measured_style_break_is_stable(self) -> None:
        params = NAT2_PARAMETER_SETS["nat2-F36"]
        accepted = 0
        for index in range(8):
            seed = (f"NAT2 support deterministic {index:02d} v1").encode().ljust(48, b".")
            public, reference = generate_nat2_instance(params, seed, 4)
            result = recover_from_sign_support(public, reference=reference)
            accepted += int(result.exact_state_accepted)
        self.assertGreaterEqual(accepted, 6)


if __name__ == "__main__":
    unittest.main()
