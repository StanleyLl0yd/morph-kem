import unittest

from morph_kem.twisted_a5 import (
    S5_ELEMENTS,
    audit_semidirect_product,
    audit_twisted_flattening,
    flattened_public_edge_labels,
    generate_twisted_a5_instance,
    validate_flattened_s5_frames,
    validate_twisted_frames,
)

MASTER_SEED = bytes.fromhex("36026490a1b2c3d4e5f60718293a4b5c")


class TwistedA5SemidirectTests(unittest.TestCase):
    def test_a5_c2_semidirect_is_exactly_s5(self) -> None:
        audit = audit_semidirect_product()
        self.assertEqual(audit.twisted_elements, 120)
        self.assertEqual(audit.s5_image_elements, 120)
        self.assertEqual(len(S5_ELEMENTS), 120)
        self.assertEqual(audit.multiplication_checks, 120 * 120)
        self.assertEqual(audit.parity_checks, 120)
        self.assertTrue(audit.bijective)
        self.assertTrue(audit.homomorphic)
        self.assertTrue(audit.orientation_equals_s5_parity)

    def test_generation_is_deterministic_and_reference_is_accepted(self) -> None:
        public1, reference1 = generate_twisted_a5_instance(MASTER_SEED)
        public2, reference2 = generate_twisted_a5_instance(MASTER_SEED)
        self.assertEqual(public1.encode(), public2.encode())
        self.assertEqual(reference1, reference2)
        self.assertTrue(
            validate_twisted_frames(public1, reference1.face_frames)
        )
        self.assertTrue(
            validate_flattened_s5_frames(public1, reference1.face_frames)
        )

    def test_orientation_bit_is_public_s5_parity(self) -> None:
        public, _ = generate_twisted_a5_instance(MASTER_SEED)
        flattened = flattened_public_edge_labels(public)

        def parity(permutation):
            return sum(
                permutation[left] > permutation[right]
                for left in range(len(permutation))
                for right in range(left + 1, len(permutation))
            ) & 1

        self.assertEqual(
            tuple(parity(S5_ELEMENTS[index]) for index in flattened),
            public.orientation_bits,
        )

    def test_exact_pairwise_relation_flattens_to_s5(self) -> None:
        public, reference = generate_twisted_a5_instance(MASTER_SEED)
        audit = audit_twisted_flattening(public, reference)
        self.assertEqual(audit.edges, 12)
        self.assertEqual(
            audit.endpoint_assignments_checked,
            12 * 60 * 60,
        )
        self.assertEqual(audit.relation_mismatches, 0)
        self.assertTrue(audit.exact_relation_match)
        self.assertEqual(audit.public_edge_parity_matches, 12)
        self.assertTrue(audit.planted_twisted_accepted)
        self.assertTrue(audit.planted_flattened_accepted)


if __name__ == "__main__":
    unittest.main()
