from __future__ import annotations

import hashlib
import unittest

from morph_kem.nat_a5_flat import (
    NAT4Error,
    NAT4Parameters,
    NAT4_PARAMETER_SETS,
    generate_nat4_instance,
    recover_nat4,
    validate_nat4_witness,
)


def seed_for(label: str) -> bytes:
    return hashlib.sha256(label.encode("ascii")).digest()


class NAT4FlatGaugeTests(unittest.TestCase):
    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(NAT4Error):
            NAT4Parameters("bad", 27, 270, (1, 2)).validate()
        with self.assertRaises(NAT4Error):
            NAT4Parameters("bad", 24, 240, (1, 5)).validate()
        with self.assertRaises(NAT4Error):
            generate_nat4_instance(NAT4_PARAMETER_SETS["nat4-F24"], b"short", 1)

    def test_planted_witness_is_accepted(self) -> None:
        params = NAT4_PARAMETER_SETS["nat4-F24"]
        public, reference = generate_nat4_instance(params, seed_for("nat4-planted"), 2)
        self.assertTrue(
            validate_nat4_witness(
                public,
                reference.hidden_clean_labels_normalized,
                reference.planted_deformation_labels,
            )
        )

    def test_public_canonical_equivalent_witness_is_accepted(self) -> None:
        params = NAT4_PARAMETER_SETS["nat4-F24"]
        public, _ = generate_nat4_instance(params, seed_for("nat4-public"), 3)
        recovery = recover_nat4(public)
        self.assertEqual(recovery.nonidentity_face_holonomies, 0)
        self.assertTrue(recovery.integration_consistent)
        self.assertTrue(recovery.canonical_witness_accepted)
        self.assertIsNone(recovery.canonical_support_matches_planted_after_public_success)

    def test_equivalent_witness_count_is_large(self) -> None:
        params = NAT4_PARAMETER_SETS["nat4-F36"]
        public, _ = generate_nat4_instance(params, seed_for("nat4-count"), 4)
        recovery = recover_nat4(public)
        self.assertGreater(recovery.equivalent_witness_lower_bound, 1_000_000)

    def test_gauge_break_is_stable_across_sets_and_seeds(self) -> None:
        for params in NAT4_PARAMETER_SETS.values():
            for index in range(4):
                for weight in params.deformation_weights:
                    public, reference = generate_nat4_instance(
                        params, seed_for(f"{params.name}-{index}"), weight
                    )
                    recovery = recover_nat4(public, reference=reference)
                    self.assertEqual(recovery.nonidentity_face_holonomies, 0)
                    self.assertTrue(recovery.integration_consistent)
                    self.assertTrue(recovery.canonical_witness_accepted)
                    self.assertTrue(recovery.effective_state_matches_reference_after_public_success)


if __name__ == "__main__":
    unittest.main()
