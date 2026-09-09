import unittest

from morph_kem.hyperbolic import (
    A5_ELEMENTS,
    A5_THREE_CYCLES,
    audit_a5,
    generate_a5_instance,
    generate_klein_quartic,
    gl32_group,
    klein_triangle_generators,
    solve_a5_csp,
    validate_a5_frames,
)

MASTER_SEED = bytes.fromhex("26457513110645905905016157536392")


class KleinQuarticTests(unittest.TestCase):
    def test_gl32_has_168_elements_and_triangle_orders(self) -> None:
        self.assertEqual(len(gl32_group()), 168)
        r, s, t = klein_triangle_generators()

        def order(value):
            current = tuple(range(len(value)))
            for exponent in range(1, 100):
                current = tuple(value[current[index]] for index in range(len(value)))
                if current == tuple(range(len(value))):
                    return exponent
            self.fail("order bound exceeded")

        self.assertEqual((order(r), order(s), order(t)), (2, 3, 7))

    def test_klein_quartic_exact_invariants(self) -> None:
        klein = generate_klein_quartic()
        self.assertEqual(len(klein.vertices), 24)
        self.assertEqual(len(klein.edges), 84)
        self.assertEqual(len(klein.faces), 56)
        self.assertEqual(set(klein.vertex_degrees), {7})
        self.assertEqual(set(klein.edge_face_degrees), {2})
        self.assertEqual(klein.euler_characteristic, -4)
        self.assertEqual(klein.genus, 3)
        self.assertEqual(klein.complex.dimension, 2)
        self.assertEqual(len(klein.complex.free_collapse_pairs()), 0)

    def test_klein_encoding_is_deterministic(self) -> None:
        self.assertEqual(generate_klein_quartic().encode(), generate_klein_quartic().encode())


class A5Tests(unittest.TestCase):
    def test_a5_audit_has_no_abelianization_shortcut(self) -> None:
        audit = audit_a5()
        self.assertEqual(len(A5_ELEMENTS), 60)
        self.assertEqual(len(A5_THREE_CYCLES), 20)
        self.assertEqual(audit.order, 60)
        self.assertEqual(audit.conjugacy_class_size, 20)
        self.assertEqual(audit.conjugacy_class_order, 3)
        self.assertEqual(audit.commutator_subgroup_size, 60)
        self.assertEqual(audit.generated_by_class_size, 60)

    def test_reference_frames_are_accepted(self) -> None:
        public, reference = generate_a5_instance(MASTER_SEED)
        self.assertTrue(validate_a5_frames(public, reference.frames).accepted)

    def test_generation_is_byte_deterministic(self) -> None:
        public1, reference1 = generate_a5_instance(MASTER_SEED)
        public2, reference2 = generate_a5_instance(MASTER_SEED)
        self.assertEqual(public1.encode(), public2.encode())
        self.assertEqual(reference1, reference2)

    def test_exact_csp_finds_equivalent_witness(self) -> None:
        public, _ = generate_a5_instance(MASTER_SEED)
        result = solve_a5_csp(public, solution_cap=4, max_nodes=500_000)
        self.assertTrue(result.accepted)
        self.assertIsNotNone(result.first_solution)
        self.assertTrue(validate_a5_frames(public, result.first_solution).accepted)


if __name__ == "__main__":
    unittest.main()
