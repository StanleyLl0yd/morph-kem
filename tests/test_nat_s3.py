from __future__ import annotations

import unittest

from morph_kem.nat_s3 import (
    NAT2Error,
    NAT2Parameters,
    NAT2_PARAMETER_SETS,
    compose,
    generate_nat2_instance,
    inverse,
    is_transposition,
    parity,
    recover_nat2,
    validate_nat2_state,
)


class NAT2S3Tests(unittest.TestCase):
    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(NAT2Error):
            NAT2Parameters("bad", 27, 270, (1, 2)).validate()
        with self.assertRaises(NAT2Error):
            generate_nat2_instance(NAT2_PARAMETER_SETS["nat2-F24"], b"short", 1)
        with self.assertRaises(NAT2Error):
            generate_nat2_instance(NAT2_PARAMETER_SETS["nat2-F24"], b"0" * 32, 4)

    def test_s3_group_operations(self) -> None:
        identity = (0, 1, 2)
        values = (
            identity,
            (1, 0, 2),
            (2, 1, 0),
            (0, 2, 1),
            (1, 2, 0),
            (2, 0, 1),
        )
        for value in values:
            self.assertEqual(compose(value, inverse(value)), identity)
            self.assertEqual(compose(inverse(value), value), identity)
        self.assertTrue(is_transposition((1, 0, 2)))
        self.assertEqual(parity((1, 2, 0)), 0)
        self.assertEqual(parity((1, 0, 2)), 1)

    def test_planted_state_passes_exact_public_verifier(self) -> None:
        params = NAT2_PARAMETER_SETS["nat2-F24"]
        public, reference = generate_nat2_instance(params, b"NAT2 verifier unit seed v1.........", 3)
        accepted, noise_edges = validate_nat2_state(
            public, reference.hidden_vertex_labels_normalized
        )
        self.assertTrue(accepted)
        self.assertEqual(noise_edges, reference.planted_noise_edges)

    def test_single_transposition_sign_quotient_recovers_reference(self) -> None:
        params = NAT2_PARAMETER_SETS["nat2-F24"]
        public, reference = generate_nat2_instance(params, b"NAT2 sign quotient unit seed v1.....", 1)
        result = recover_nat2(public, reference=reference)
        self.assertTrue(result.sign_clean_parity_accepted)
        self.assertTrue(result.sign_matches_planted_noise_after_public_success)
        self.assertTrue(result.sign_matches_hidden_vertex_parity_after_public_success)
        self.assertTrue(result.first_state_accepted)

    def test_public_exact_search_needs_no_reference(self) -> None:
        params = NAT2_PARAMETER_SETS["nat2-F30"]
        public, _ = generate_nat2_instance(params, b"NAT2 public exact search seed v1.....", 3)
        result = recover_nat2(public)
        self.assertTrue(result.first_state_accepted)
        self.assertGreater(result.csp_nodes, 0)
        self.assertGreater(result.accepted_states, 0)
        self.assertIsNone(result.first_state_matches_hidden_after_public_success)

    def test_break_is_stable_across_seeds(self) -> None:
        params = NAT2_PARAMETER_SETS["nat2-F36"]
        for index in range(4):
            seed = (f"NAT2 deterministic seed {index:02d} v1").encode().ljust(48, b".")
            public, reference = generate_nat2_instance(params, seed, 4)
            result = recover_nat2(public, reference=reference)
            self.assertTrue(result.first_state_accepted)
            self.assertGreater(result.accepted_states, 0)
            self.assertLessEqual(result.sign_tjoin_weight, 4)


if __name__ == "__main__":
    unittest.main()
