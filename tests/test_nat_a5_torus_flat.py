from __future__ import annotations

import hashlib
import unittest

from morph_kem.nat_a5_torus_flat import (
    NAT6Error,
    NAT6Parameters,
    NAT6_PARAMETER_SETS,
    _COMMUTING_PAIRS,
    generate_nat6_instance,
    recover_nat6,
    validate_nat6_witness,
)


def seed_for(label: str) -> bytes:
    return hashlib.sha256(label.encode("ascii")).digest()


class NAT6FlatTorusTests(unittest.TestCase):
    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(NAT6Error):
            NAT6Parameters("bad", 5, 5, 25).validate()
        with self.assertRaises(NAT6Error):
            generate_nat6_instance(NAT6_PARAMETER_SETS["nat6-6x6"], b"short")

    def test_a5_commuting_pair_family_is_small_and_nonempty(self) -> None:
        self.assertEqual(len(_COMMUTING_PAIRS), 30)

    def test_planted_witness_is_accepted(self) -> None:
        params = NAT6_PARAMETER_SETS["nat6-6x6"]
        public, reference = generate_nat6_instance(params, seed_for("nat6-planted"))
        self.assertTrue(
            validate_nat6_witness(
                public,
                reference.hidden_vertex_labels_normalized,
                reference.holonomy_pair,
            )
        )
        recovery = recover_nat6(public, reference=reference)
        self.assertEqual(recovery.nonidentity_face_holonomies, 0)
        self.assertEqual(recovery.h1_dimension, 2)
        self.assertTrue(recovery.first_accepted)

    def test_public_recovery_needs_no_reference(self) -> None:
        params = NAT6_PARAMETER_SETS["nat6-6x6"]
        public, _ = generate_nat6_instance(params, seed_for("nat6-public"))
        recovery = recover_nat6(public)
        self.assertTrue(recovery.first_accepted)
        self.assertGreaterEqual(recovery.accepted_decompositions, 1)
        self.assertEqual(recovery.pair_candidates_tested, len(_COMMUTING_PAIRS))
        self.assertIsNone(recovery.first_pair_matches_planted_after_public_success)

    def test_declared_sweep_is_flat_and_publicly_recoverable(self) -> None:
        for params in NAT6_PARAMETER_SETS.values():
            for index in range(3):
                public, reference = generate_nat6_instance(
                    params, seed_for(f"{params.name}-{index}")
                )
                recovery = recover_nat6(public, reference=reference)
                self.assertEqual(recovery.euler_characteristic, 0)
                self.assertEqual(recovery.min_triangles_per_edge, 2)
                self.assertEqual(recovery.max_triangles_per_edge, 2)
                self.assertEqual(recovery.nonidentity_face_holonomies, 0)
                self.assertTrue(recovery.first_accepted)
                self.assertGreaterEqual(recovery.accepted_decompositions, 1)
                self.assertLessEqual(recovery.normalized_distinct_nonidentity_residuals, 3)


if __name__ == "__main__":
    unittest.main()
