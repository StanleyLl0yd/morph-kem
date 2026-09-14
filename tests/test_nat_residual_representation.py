from __future__ import annotations

import hashlib
import unittest

from morph_kem.gluing_cohomology_cycle import _edges, _triangles
from morph_kem.nat_a5 import _IDENTITY, compose, inverse
from morph_kem.nat_a5_torus_flat import NAT6_PARAMETER_SETS, generate_nat6_instance
from morph_kem.nat_residual_representation import (
    ResidualRepresentation,
    extract_residual_representation,
    triangle_relator_holonomies,
)
from morph_kem.nat_tree_gauge import GroupOps


A5_OPS = GroupOps(_IDENTITY, compose, inverse)
Z5_OPS = GroupOps(0, lambda left, right: (left + right) % 5, lambda value: (-value) % 5)


def digest(label: str) -> bytes:
    return hashlib.sha256(label.encode("ascii")).digest()


class NAT8ResidualRepresentationTests(unittest.TestCase):
    def test_nonflat_public_connection_still_exposes_free_generators(self) -> None:
        edges = ((0, 1), (0, 2), (1, 2))
        labels = (1, 2, 4)
        result = extract_residual_representation(3, edges, labels, Z5_OPS)
        self.assertIsInstance(result, ResidualRepresentation)
        self.assertEqual(result.free_rank, 1)
        self.assertEqual(len(result.generator_images), 1)
        self.assertTrue(result.residual_vector_reconstructed)
        self.assertTrue(result.connection_reconstructed)

        face = triangle_relator_holonomies(edges, labels, ((0, 1, 2),), Z5_OPS)
        self.assertEqual(face, (3,))
        self.assertNotEqual(face[0], Z5_OPS.identity)

    def test_nat6_flat_torus_representation_is_public(self) -> None:
        params = NAT6_PARAMETER_SETS["nat6-8x9"]
        public, _ = generate_nat6_instance(
            params, digest("MORPH-KEM NAT8 fixed unit regression v1")
        )
        edges = _edges(public.target)
        triangles = _triangles(public.target)
        result = extract_residual_representation(
            len(public.target.vertices), edges, public.observed_edge_labels, A5_OPS
        )
        self.assertEqual(result.free_rank, len(edges) - len(public.target.vertices) + 1)
        self.assertEqual(result.free_rank, 145)
        self.assertEqual(result.tree_identity_residuals, len(public.target.vertices) - 1)
        self.assertTrue(result.connection_reconstructed)
        self.assertTrue(result.residual_vector_reconstructed)
        self.assertTrue(
            all(
                value == _IDENTITY
                for value in triangle_relator_holonomies(
                    edges, public.observed_edge_labels, triangles, A5_OPS
                )
            )
        )

    def test_nat6_declared_family_is_stable(self) -> None:
        for params in NAT6_PARAMETER_SETS.values():
            for index in range(4):
                public, _ = generate_nat6_instance(
                    params,
                    digest(f"MORPH-KEM NAT8 unit {params.name} seed {index} v1"),
                )
                edges = _edges(public.target)
                result = extract_residual_representation(
                    len(public.target.vertices),
                    edges,
                    public.observed_edge_labels,
                    A5_OPS,
                )
                self.assertEqual(
                    result.free_rank,
                    len(edges) - len(public.target.vertices) + 1,
                )
                self.assertEqual(len(result.generator_images), result.free_rank)
                self.assertTrue(result.connection_reconstructed)


if __name__ == "__main__":
    unittest.main()
