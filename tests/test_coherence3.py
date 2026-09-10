import unittest

from morph_kem.coherence3 import (
    coherence_rows,
    face_boundary_fiber,
    generate_boundary4_simplex,
    generate_kernel_coherence_instance,
    kernel_bit_for_face,
    public_gf2_coherence_attack,
    validate_kernel_coherence,
)

MASTER_SEED = bytes.fromhex("2309425a6bc7d8e90123456789abcdef")


class KernelCoherenceTests(unittest.TestCase):
    def test_boundary4_simplex_exact_counts(self) -> None:
        scaffold = generate_boundary4_simplex()
        self.assertEqual(
            (len(scaffold.vertices), len(scaffold.edges), len(scaffold.faces), len(scaffold.tetrahedra)),
            (5, 10, 10, 5),
        )
        self.assertEqual(set(scaffold.face_tetra_degrees), {2})
        self.assertEqual(scaffold.euler_characteristic, 0)
        self.assertEqual(scaffold.complex.dimension, 3)

    def test_generation_is_byte_deterministic(self) -> None:
        public1, reference1 = generate_kernel_coherence_instance(MASTER_SEED)
        public2, reference2 = generate_kernel_coherence_instance(MASTER_SEED)
        self.assertEqual(public1.encode(), public2.encode())
        self.assertEqual(reference1, reference2)

    def test_reference_is_accepted_and_each_face_has_two_lifts(self) -> None:
        public, reference = generate_kernel_coherence_instance(MASTER_SEED)
        self.assertTrue(validate_kernel_coherence(public, reference.face_values))
        self.assertEqual(
            tuple(len(face_boundary_fiber(value)) for value in public.face_boundaries),
            (2,) * 10,
        )
        self.assertTrue(
            all(
                kernel_bit_for_face(boundary_value, face_value) in (0, 1)
                for boundary_value, face_value in zip(public.face_boundaries, reference.face_values)
            )
        )

    def test_boundary_matrix_has_expected_dependency(self) -> None:
        scaffold = generate_boundary4_simplex()
        rows = coherence_rows(scaffold)
        xor_all = 0
        for row in rows:
            xor_all ^= row
        self.assertEqual(xor_all, 0)

    def test_public_gf2_attack_recovers_equivalent_witness(self) -> None:
        public, _ = generate_kernel_coherence_instance(MASTER_SEED)
        attack = public_gf2_coherence_attack(public)
        self.assertTrue(attack.accepted)
        self.assertTrue(validate_kernel_coherence(public, attack.face_values))
        self.assertEqual((attack.equations, attack.variables), (5, 10))
        self.assertEqual((attack.rank, attack.nullity), (4, 6))
        self.assertEqual(attack.dependent_equations, 1)
        self.assertEqual(attack.equivalent_witnesses, 64)


if __name__ == "__main__":
    unittest.main()
