import unittest

from morph_kem.crossed_q8 import (
    Q8_MINUS_ONE,
    audit_crossed_module,
    boundary,
    face_boundary_preimages,
    generate_q8_fake_flat_instance,
    public_face_lift_attack,
    q8_automorphisms,
    q8_inv,
    q8_mul,
    validate_fake_flatness,
)

MASTER_SEED = bytes.fromhex("40226490aabbccddeeff001122334455")


class Q8CrossedModuleTests(unittest.TestCase):
    def test_q8_group_and_automorphism_counts(self) -> None:
        for element in range(8):
            inverse = q8_inv(element)
            self.assertEqual(q8_mul(element, inverse), 0)
            self.assertEqual(q8_mul(inverse, element), 0)
        self.assertEqual(q8_mul(2, 4), 6)  # i*j=k
        self.assertEqual(q8_mul(4, 2), 7)  # j*i=-k
        self.assertEqual(q8_mul(2, 2), Q8_MINUS_ONE)
        self.assertEqual(len(q8_automorphisms()), 24)

    def test_crossed_module_exact_structure_and_identities(self) -> None:
        audit = audit_crossed_module()
        self.assertEqual(audit.q8_order, 8)
        self.assertEqual(audit.automorphism_order, 24)
        self.assertEqual(audit.kernel_size, 2)
        self.assertEqual(audit.image_size, 4)
        self.assertEqual(audit.cokernel_cosets, 6)
        self.assertEqual(audit.first_identity_checks, 24 * 8)
        self.assertEqual(audit.second_identity_checks, 8 * 8)
        self.assertTrue(audit.identities_hold)
        self.assertEqual(boundary(0), boundary(1))

    def test_generation_is_deterministic_and_reference_valid(self) -> None:
        public1, reference1 = generate_q8_fake_flat_instance(MASTER_SEED)
        public2, reference2 = generate_q8_fake_flat_instance(MASTER_SEED)
        self.assertEqual(public1.encode(), public2.encode())
        self.assertEqual(reference1, reference2)
        self.assertTrue(validate_fake_flatness(public1, reference1.face_values))

    def test_every_face_has_exactly_kernel_size_public_lifts(self) -> None:
        public, _ = generate_q8_fake_flat_instance(MASTER_SEED)
        for face_index in range(len(public.base_map.faces)):
            self.assertEqual(len(face_boundary_preimages(public, face_index)), 2)

    def test_public_face_lift_attack_recovers_equivalent_witness(self) -> None:
        public, reference = generate_q8_fake_flat_instance(MASTER_SEED)
        result = public_face_lift_attack(public)
        self.assertTrue(result.accepted)
        self.assertTrue(validate_fake_flatness(public, result.face_values))
        self.assertEqual(result.fiber_sizes, (2, 2, 2, 2))
        self.assertEqual(result.total_equivalent_witnesses, 16)
        self.assertEqual(result.boundary_image_faces, 4)
        self.assertGreater(result.nonidentity_curvatures, 0)
        self.assertEqual(result.edge_compositions, 24)
        self.assertEqual(result.q8_preimage_checks, 32)
        # The public attack need not recover the planted representative.
        self.assertNotEqual(result.face_values, ())
        self.assertTrue(validate_fake_flatness(public, reference.face_values))


if __name__ == "__main__":
    unittest.main()
