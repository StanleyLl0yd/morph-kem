from __future__ import annotations

import hashlib
import unittest

from morph_kem.gluing import (
    G0_PARAMETER_SETS,
    GluingExperimentError,
    GluingParameters,
    generate_gluing_instance,
    gluing_incidence,
    recover_gluing_by_dual_bridges,
    reference_partition_matches,
    validate_gluing_witness,
)


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


class GluingNegativeControlTests(unittest.TestCase):
    def test_exact_structural_metrics(self) -> None:
        expected = {
            "g0-3": (9, 24, 28, 12, 8, 20, 2, 40, 48),
            "g0-5": (13, 38, 46, 20, 12, 34, 4, 68, 80),
            "g0-8": (19, 59, 73, 32, 18, 55, 7, 110, 128),
        }

        for name, params in G0_PARAMETER_SETS.items():
            with self.subTest(name=name):
                public, reference = generate_gluing_instance(params, MASTER_SEED)
                incidence = gluing_incidence(public)
                recovery = recover_gluing_by_dual_bridges(public)
                observed = (
                    incidence.vertices,
                    incidence.edges,
                    incidence.faces,
                    incidence.tetrahedra,
                    incidence.boundary_faces,
                    incidence.dual_edges,
                    len(recovery.bridges),
                    recovery.dfs_edge_scans,
                    recovery.face_occurrences,
                )
                self.assertEqual(observed, expected[name])
                self.assertEqual(incidence.euler_characteristic, 1)
                self.assertEqual(incidence.max_face_incidence, 2)
                self.assertTrue(recovery.validation.valid)
                self.assertTrue(reference_partition_matches(reference, recovery.groups))

    def test_reference_and_public_attack_both_validate(self) -> None:
        for params in G0_PARAMETER_SETS.values():
            with self.subTest(name=params.name):
                public, reference = generate_gluing_instance(params, MASTER_SEED)
                self.assertTrue(validate_gluing_witness(public, reference.groups).valid)
                recovery = recover_gluing_by_dual_bridges(public)
                self.assertTrue(recovery.validation.valid)
                self.assertEqual(len(recovery.groups), params.piece_count)
                self.assertEqual(len(recovery.bridges), params.piece_count - 1)
                self.assertEqual(recovery.validation.component_sizes, (4,) * params.piece_count)

    def test_seeded_public_relabel_does_not_break_recovery(self) -> None:
        encodings = set()
        params = G0_PARAMETER_SETS["g0-8"]
        for index in range(8):
            seed = hashlib.sha256(MASTER_SEED + index.to_bytes(4, "big")).digest()
            public, reference = generate_gluing_instance(params, seed)
            recovery = recover_gluing_by_dual_bridges(public)
            self.assertTrue(recovery.validation.valid)
            self.assertTrue(reference_partition_matches(reference, recovery.groups))
            encodings.add(public.tetrahedra)
        self.assertEqual(len(encodings), 8)

    def test_invalid_partition_is_rejected(self) -> None:
        public, reference = generate_gluing_instance(G0_PARAMETER_SETS["g0-3"], MASTER_SEED)
        missing_one = (reference.groups[0][:-1],) + reference.groups[1:]
        self.assertFalse(validate_gluing_witness(public, missing_one).valid)

    def test_invalid_parameters_and_short_seed_are_rejected(self) -> None:
        with self.assertRaises(GluingExperimentError):
            GluingParameters("disconnected", 4, ((0, 1), (1, 2), (2, 0))).validate()
        with self.assertRaises(GluingExperimentError):
            generate_gluing_instance(G0_PARAMETER_SETS["g0-3"], b"short")


if __name__ == "__main__":
    unittest.main()
