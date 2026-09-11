from __future__ import annotations

import unittest

from morph_kem.gluing import GluingExperimentError
from morph_kem.gluing_mixed_sphere import (
    G15_PARAMETER_SETS,
    MixedSphereParameters,
    encode_mixed_sphere_sat,
    generate_mixed_sphere_instance,
    recover_mixed_sphere,
    validate_mixed_sphere_witness,
)
from morph_kem.gluing_surface_hypercover import toroidal_hypercover_incidence


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


class MixedSphereTests(unittest.TestCase):
    def test_a042_defeats_complete_reverse_stacking_but_exact_cover_succeeds(self) -> None:
        for name, params in G15_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public, reference = generate_mixed_sphere_instance(params, MASTER_SEED)
                incidence = toroidal_hypercover_incidence(public)
                recovery = recover_mixed_sphere(public, reference=reference, solution_cap=32)
                self.assertEqual(incidence.triangles, params.triangle_count)
                self.assertEqual(incidence.euler_characteristic, 2)
                self.assertEqual(incidence.min_triangles_per_edge, 2)
                self.assertEqual(incidence.max_triangles_per_edge, 2)
                self.assertEqual(recovery.growth_steps, params.growth_steps)
                self.assertEqual(recovery.successful_flips, params.successful_flips)
                self.assertGreater(recovery.rejected_flip_proposals, 0)
                self.assertFalse(recovery.reverse_reached_tetrahedron)
                self.assertGreater(recovery.reverse_terminal_triangles, 4)
                self.assertGreaterEqual(recovery.accepted_solutions, 1)
                self.assertGreaterEqual(recovery.nonreference_accepted_solutions, 1)
                self.assertTrue(
                    all(
                        validate_mixed_sphere_witness(public, groups).valid
                        for groups in recovery.accepted_groups
                    )
                )

    def test_attack_does_not_need_reference(self) -> None:
        public, _ = generate_mixed_sphere_instance(G15_PARAMETER_SETS["g15-36"], MASTER_SEED)
        recovery = recover_mixed_sphere(public, solution_cap=8)
        self.assertGreaterEqual(recovery.accepted_solutions, 1)
        self.assertTrue(
            all(
                validate_mixed_sphere_witness(public, groups).valid
                for groups in recovery.accepted_groups
            )
        )

    def test_break_is_stable_under_deterministic_seeds(self) -> None:
        for name, params in G15_PARAMETER_SETS.items():
            for seed_index in range(3):
                with self.subTest(name=name, seed=seed_index):
                    seed = bytes([seed_index + 1]) * 32
                    public, reference = generate_mixed_sphere_instance(params, seed)
                    recovery = recover_mixed_sphere(public, reference=reference, solution_cap=8)
                    self.assertFalse(recovery.reverse_reached_tetrahedron)
                    self.assertGreaterEqual(recovery.accepted_solutions, 1)
                    self.assertGreaterEqual(recovery.nonreference_accepted_solutions, 1)

    def test_sat_encoding_covers_every_public_triangle(self) -> None:
        public, _ = generate_mixed_sphere_instance(G15_PARAMETER_SETS["g15-36"], MASTER_SEED)
        encoding = encode_mixed_sphere_sat(public)
        triangle_count = sum(len(simplex) == 3 for simplex in public.target.simplices)
        covered = {triangle for candidate in encoding.candidates for triangle in candidate}
        self.assertEqual(covered, set(range(triangle_count)))
        self.assertGreater(encoding.variable_count, triangle_count)

    def test_parameter_seed_and_cap_bounds(self) -> None:
        with self.assertRaises(GluingExperimentError):
            MixedSphereParameters("too-small", 18, 360).validate()
        with self.assertRaises(GluingExperimentError):
            MixedSphereParameters("bad-count", 39, 780).validate()
        with self.assertRaises(GluingExperimentError):
            generate_mixed_sphere_instance(G15_PARAMETER_SETS["g15-36"], b"short")
        public, _ = generate_mixed_sphere_instance(G15_PARAMETER_SETS["g15-36"], MASTER_SEED)
        with self.assertRaises(GluingExperimentError):
            recover_mixed_sphere(public, solution_cap=0)


if __name__ == "__main__":
    unittest.main()
