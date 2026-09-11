from __future__ import annotations

import unittest

from morph_kem.gluing import GluingExperimentError
from morph_kem.gluing_stacked_sphere import (
    G14_PARAMETER_SETS,
    StackedSphereParameters,
    generate_stacked_sphere_instance,
    recover_reverse_stacking,
)
from morph_kem.gluing_surface_hypercover import toroidal_hypercover_incidence


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


class StackedSphereTests(unittest.TestCase):
    def test_exact_sphere_and_reverse_metrics(self) -> None:
        for name, params in G14_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public = generate_stacked_sphere_instance(params, MASTER_SEED)
                incidence = toroidal_hypercover_incidence(public)
                recovery = recover_reverse_stacking(public)
                expected_vertices = params.triangle_count // 2 + 2
                self.assertEqual(incidence.vertices, expected_vertices)
                self.assertEqual(incidence.edges, 3 * expected_vertices - 6)
                self.assertEqual(incidence.triangles, params.triangle_count)
                self.assertEqual(incidence.euler_characteristic, 2)
                self.assertEqual(incidence.min_triangles_per_edge, 2)
                self.assertEqual(incidence.max_triangles_per_edge, 2)
                self.assertEqual(recovery.moves, params.stacking_steps)
                self.assertEqual(len(recovery.removed_vertices), params.stacking_steps)
                self.assertEqual(len(set(recovery.removed_vertices)), params.stacking_steps)
                self.assertTrue(recovery.reached_tetrahedron_boundary)
                self.assertEqual(
                    (
                        recovery.terminal_vertices,
                        recovery.terminal_edges,
                        recovery.terminal_triangles,
                        recovery.terminal_euler_characteristic,
                    ),
                    (4, 6, 4, 2),
                )
                self.assertGreaterEqual(recovery.max_candidates, 1)

    def test_break_is_stable_across_deterministic_seeds(self) -> None:
        for name, params in G14_PARAMETER_SETS.items():
            for seed_index in range(8):
                with self.subTest(name=name, seed=seed_index):
                    seed = bytes([seed_index + 1]) * 32
                    public = generate_stacked_sphere_instance(params, seed)
                    recovery = recover_reverse_stacking(public)
                    self.assertEqual(recovery.moves, params.stacking_steps)
                    self.assertTrue(recovery.reached_tetrahedron_boundary)

    def test_generation_is_deterministic(self) -> None:
        params = G14_PARAMETER_SETS["g14-54"]
        left = generate_stacked_sphere_instance(params, MASTER_SEED)
        right = generate_stacked_sphere_instance(params, MASTER_SEED)
        self.assertEqual(left.target, right.target)
        self.assertEqual(recover_reverse_stacking(left), recover_reverse_stacking(right))

    def test_parameter_and_seed_bounds(self) -> None:
        with self.assertRaises(GluingExperimentError):
            StackedSphereParameters("too-small", 6).validate()
        with self.assertRaises(GluingExperimentError):
            StackedSphereParameters("not-divisible-three", 38).validate()
        with self.assertRaises(GluingExperimentError):
            generate_stacked_sphere_instance(G14_PARAMETER_SETS["g14-36"], b"short")


if __name__ == "__main__":
    unittest.main()
