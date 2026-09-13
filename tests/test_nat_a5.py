from __future__ import annotations

import hashlib
import unittest

from morph_kem.nat_a5 import (
    NAT3Error,
    NAT3Parameters,
    NAT3_PARAMETER_SETS,
    _A5,
    _THREE_CYCLES,
    _IDENTITY,
    compose,
    generate_nat3_instance,
    inverse,
    parity,
    recover_nat3,
    validate_nat3_state,
)


def seed_for(label: str) -> bytes:
    return hashlib.sha256(label.encode("ascii")).digest()


class NAT3A5Tests(unittest.TestCase):
    def test_a5_group_tables_and_noise_class(self) -> None:
        self.assertEqual(len(_A5), 60)
        self.assertEqual(len(_THREE_CYCLES), 20)
        for value in _A5:
            self.assertEqual(parity(value), 0)
            self.assertEqual(compose(value, inverse(value)), _IDENTITY)
            self.assertEqual(compose(inverse(value), value), _IDENTITY)

    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(NAT3Error):
            NAT3Parameters("bad", 27, 270, (1, 2, 3)).validate()
        with self.assertRaises(NAT3Error):
            NAT3Parameters("bad", 24, 240, (1, 4)).validate()
        with self.assertRaises(NAT3Error):
            generate_nat3_instance(NAT3_PARAMETER_SETS["nat3-F24"], b"short", 1)

    def test_planted_state_passes_exact_public_verifier(self) -> None:
        params = NAT3_PARAMETER_SETS["nat3-F24"]
        public, reference = generate_nat3_instance(params, seed_for("nat3-planted"), 2)
        accepted, inferred = validate_nat3_state(
            public, reference.hidden_vertex_labels_normalized
        )
        self.assertTrue(accepted)
        self.assertEqual(inferred, reference.planted_noise_edges)

    def test_single_noise_curvature_localizes_support(self) -> None:
        params = NAT3_PARAMETER_SETS["nat3-F24"]
        public, reference = generate_nat3_instance(params, seed_for("nat3-single"), 1)
        recovery = recover_nat3(public, reference=reference)
        self.assertTrue(recovery.first_state_accepted)
        self.assertTrue(recovery.planted_support_is_curvature_hitting)
        self.assertEqual(recovery.curvature_hitting_supports, 1)
        self.assertEqual(recovery.first_state_noise_edges, reference.planted_noise_edges)
        self.assertTrue(recovery.first_state_matches_planted_after_public_success)

    def test_public_attack_needs_no_reference(self) -> None:
        params = NAT3_PARAMETER_SETS["nat3-F24"]
        public, _ = generate_nat3_instance(params, seed_for("nat3-public"), 2)
        recovery = recover_nat3(public)
        self.assertTrue(recovery.first_state_accepted)
        self.assertIsNone(recovery.first_support_matches_planted_after_public_success)
        self.assertIsNone(recovery.first_state_matches_planted_after_public_success)

    def test_single_noise_localization_is_stable_across_sets(self) -> None:
        for params in NAT3_PARAMETER_SETS.values():
            for index in range(4):
                public, reference = generate_nat3_instance(
                    params, seed_for(f"{params.name}-single-{index}"), 1
                )
                recovery = recover_nat3(public, reference=reference)
                self.assertEqual(recovery.curvature_hitting_supports, 1)
                self.assertTrue(recovery.first_state_accepted)


if __name__ == "__main__":
    unittest.main()
