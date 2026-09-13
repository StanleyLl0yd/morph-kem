from __future__ import annotations

import hashlib
import unittest

from morph_kem.nat_a5_cycle_noise import (
    NAT5Error,
    NAT5Parameters,
    NAT5_PARAMETER_SETS,
    generate_nat5_instance,
    recover_nat5,
    validate_nat5_witness,
)


def seed_for(label: str) -> bytes:
    return hashlib.sha256(label.encode("ascii")).digest()


class NAT5CycleNoiseTests(unittest.TestCase):
    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(NAT5Error):
            NAT5Parameters("bad", 27, 270, 4).validate()
        with self.assertRaises(NAT5Error):
            NAT5Parameters("bad", 24, 240, 5).validate()
        with self.assertRaises(NAT5Error):
            generate_nat5_instance(NAT5_PARAMETER_SETS["nat5-F24"], b"short")

    def test_planted_cycle_witness_is_accepted(self) -> None:
        params = NAT5_PARAMETER_SETS["nat5-F24"]
        public, reference = generate_nat5_instance(params, seed_for("nat5-planted"))
        self.assertTrue(
            validate_nat5_witness(
                public,
                reference.hidden_clean_labels_normalized,
                reference.planted_cycle,
                reference.planted_noise_value,
            )
        )

    def test_public_attack_needs_no_reference(self) -> None:
        params = NAT5_PARAMETER_SETS["nat5-F24"]
        public, _ = generate_nat5_instance(params, seed_for("nat5-public"))
        recovery = recover_nat5(public)
        self.assertTrue(recovery.first_accepted)
        self.assertGreater(recovery.enumerated_cycles, 0)
        self.assertGreater(recovery.curvature_hitting_cycles, 0)
        self.assertIsNone(recovery.first_cycle_matches_planted_after_public_success)

    def test_attack_is_stable_on_small_declared_sweep(self) -> None:
        for params in NAT5_PARAMETER_SETS.values():
            for index in range(2):
                public, reference = generate_nat5_instance(
                    params, seed_for(f"{params.name}-seed-{index}")
                )
                recovery = recover_nat5(public, reference=reference)
                self.assertTrue(recovery.first_accepted)
                self.assertGreaterEqual(recovery.consistent_pairs, 1)

    def test_generation_is_deterministic(self) -> None:
        params = NAT5_PARAMETER_SETS["nat5-F30"]
        seed = seed_for("nat5-deterministic")
        self.assertEqual(
            generate_nat5_instance(params, seed),
            generate_nat5_instance(params, seed),
        )


if __name__ == "__main__":
    unittest.main()
