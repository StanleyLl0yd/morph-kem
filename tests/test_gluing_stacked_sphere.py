from __future__ import annotations

import unittest

from morph_kem.gluing import GluingExperimentError
from morph_kem.gluing_stacked_sphere import (
    G14_PARAMETER_SETS,
    StackedSphereParameters,
    generate_stacked_sphere_instance,
    recover_stacked_sphere_hypercover,
    reverse_stacked_sphere,
    validate_stacked_sphere_witness,
)


class StackedSphereTests(unittest.TestCase):
    def test_public_reverse_stacking_recovers_tetrahedron(self) -> None:
        seed = bytes.fromhex("41" * 32)
        for params in G14_PARAMETER_SETS.values():
            with self.subTest(params=params.name):
                public, reference = generate_stacked_sphere_instance(params, seed)
                recovery = reverse_stacked_sphere(public)
                self.assertEqual(recovery.initial_triangles, 4 + 2 * params.stacking_steps)
                self.assertEqual(recovery.initial_vertices, 4 + params.stacking_steps)
                self.assertEqual(recovery.initial_edges, 3 * recovery.initial_vertices - 6)
                self.assertEqual(recovery.reverse_moves, params.stacking_steps)
                self.assertTrue(recovery.reached_tetrahedron_boundary)
                self.assertEqual(
                    (recovery.terminal_vertices, recovery.terminal_edges, recovery.terminal_triangles),
                    (4, 6, 4),
                )
                self.assertEqual(recovery.terminal_euler_characteristic, 2)
                self.assertGreaterEqual(recovery.initial_degree_three_vertices, 1)
                self.assertEqual(recovery.candidate_counts[-1], 0)
                if reference is not None:
                    self.assertTrue(validate_stacked_sphere_witness(public, reference.groups).valid)

    def test_all_sizes_multi_seed_reverse_completely(self) -> None:
        for params in G14_PARAMETER_SETS.values():
            for seed_index in range(8):
                seed = (b"G14 deterministic sweep" + seed_index.to_bytes(4, "big")).ljust(32, b"\x00")
                with self.subTest(params=params.name, seed=seed_index):
                    public, _ = generate_stacked_sphere_instance(params, seed)
                    recovery = reverse_stacked_sphere(public)
                    self.assertEqual(recovery.reverse_moves, params.stacking_steps)
                    self.assertTrue(recovery.reached_tetrahedron_boundary)

    def test_hypercover_attack_never_uses_reference_for_acceptance(self) -> None:
        params = G14_PARAMETER_SETS["g14-36"]
        public, reference = generate_stacked_sphere_instance(params, bytes.fromhex("62" * 32))
        without_reference = recover_stacked_sphere_hypercover(
            public, reference=None, solution_cap=16
        )
        with_reference = recover_stacked_sphere_hypercover(
            public, reference=reference, solution_cap=16
        )
        self.assertEqual(without_reference.exact_cover_solutions, with_reference.exact_cover_solutions)
        self.assertEqual(without_reference.accepted_solutions, with_reference.accepted_solutions)
        self.assertFalse(without_reference.reference_available)
        self.assertEqual(without_reference.nonreference_accepted_solutions, 0)
        if reference is not None:
            self.assertTrue(with_reference.reference_available)
            self.assertGreaterEqual(with_reference.accepted_solutions, 1)

    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(GluingExperimentError):
            StackedSphereParameters("bad", 0).validate()
        with self.assertRaises(GluingExperimentError):
            StackedSphereParameters("bad", 2).validate()
        with self.assertRaises(GluingExperimentError):
            generate_stacked_sphere_instance(G14_PARAMETER_SETS["g14-36"], b"short")


if __name__ == "__main__":
    unittest.main()
