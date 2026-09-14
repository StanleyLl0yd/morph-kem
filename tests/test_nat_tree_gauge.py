from __future__ import annotations

import hashlib
import unittest

from morph_kem.gluing_cohomology_cycle import _edges
from morph_kem.nat_a5 import (
    _IDENTITY,
    _normalized_hidden_labels,
    compose,
    inverse,
)
from morph_kem.nat_a5_torus_flat import (
    NAT6_PARAMETER_SETS,
    _tree_normalized_residuals,
    generate_nat6_instance,
)
from morph_kem.nat_tree_gauge import (
    GroupOps,
    NAT7Error,
    apply_normalized_vertex_gauge,
    normalize_connection,
)


_A5_OPS = GroupOps(_IDENTITY, compose, inverse)


def seed_for(label: str) -> bytes:
    return hashlib.sha256(label.encode("ascii")).digest()


class NAT7TreeGaugeTests(unittest.TestCase):
    def test_malformed_or_disconnected_carriers_are_rejected(self) -> None:
        with self.assertRaises(NAT7Error):
            normalize_connection(2, (), (), _A5_OPS)
        with self.assertRaises(NAT7Error):
            normalize_connection(3, ((0, 1),), (_IDENTITY,), _A5_OPS)
        with self.assertRaises(NAT7Error):
            normalize_connection(2, ((1, 0),), (_IDENTITY,), _A5_OPS)

    def test_tree_residuals_are_identity_and_connection_reconstructs(self) -> None:
        params = NAT6_PARAMETER_SETS["nat6-6x6"]
        public, _ = generate_nat6_instance(params, seed_for("nat7-tree-reconstruct"))
        edges = _edges(public.target)
        result = normalize_connection(
            len(public.target.vertices), edges, public.observed_edge_labels, _A5_OPS
        )
        self.assertEqual(result.tree_assignments, len(public.target.vertices) - 1)
        self.assertEqual(result.tree_identity_residuals, len(result.tree_edge_indices))
        self.assertEqual(len(result.non_tree_edge_indices), len(edges) - len(result.tree_edge_indices))
        self.assertTrue(result.reconstruction_verified)

    def test_normalized_vertex_gauge_does_not_change_canonical_residuals(self) -> None:
        params = NAT6_PARAMETER_SETS["nat6-6x9"]
        public, _ = generate_nat6_instance(params, seed_for("nat7-gauge-invariance-instance"))
        edges = _edges(public.target)
        gauge = _normalized_hidden_labels(
            public.target, seed_for("nat7-independent-gauge"), "nat7-regauge"
        )
        gauged = apply_normalized_vertex_gauge(
            edges, public.observed_edge_labels, gauge, _A5_OPS
        )
        original = normalize_connection(
            len(public.target.vertices), edges, public.observed_edge_labels, _A5_OPS
        )
        transformed = normalize_connection(
            len(public.target.vertices), edges, gauged, _A5_OPS
        )
        self.assertEqual(original.tree_edge_indices, transformed.tree_edge_indices)
        self.assertEqual(original.residual_labels, transformed.residual_labels)
        self.assertTrue(transformed.reconstruction_verified)

    def test_generic_normalization_matches_nat6_specialized_regression(self) -> None:
        params = NAT6_PARAMETER_SETS["nat6-8x9"]
        public, _ = generate_nat6_instance(params, seed_for("nat7-specialized-regression"))
        edges = _edges(public.target)
        generic = normalize_connection(
            len(public.target.vertices), edges, public.observed_edge_labels, _A5_OPS
        )
        specialized_residuals, specialized_tree = _tree_normalized_residuals(public)
        self.assertEqual(generic.residual_labels, specialized_residuals)
        self.assertEqual(generic.tree_edge_indices, specialized_tree)

    def test_declared_nat6_sweep_is_canonically_gauge_invariant(self) -> None:
        for params in NAT6_PARAMETER_SETS.values():
            for index in range(2):
                public, _ = generate_nat6_instance(
                    params, seed_for(f"nat7-sweep-{params.name}-{index}")
                )
                edges = _edges(public.target)
                gauge = _normalized_hidden_labels(
                    public.target,
                    seed_for(f"nat7-sweep-gauge-{params.name}-{index}"),
                    f"nat7-sweep-gauge-{params.name}-{index}",
                )
                gauged = apply_normalized_vertex_gauge(
                    edges, public.observed_edge_labels, gauge, _A5_OPS
                )
                first = normalize_connection(
                    len(public.target.vertices), edges, public.observed_edge_labels, _A5_OPS
                )
                second = normalize_connection(
                    len(public.target.vertices), edges, gauged, _A5_OPS
                )
                self.assertEqual(first.residual_labels, second.residual_labels)
                self.assertTrue(first.reconstruction_verified)
                self.assertTrue(second.reconstruction_verified)


if __name__ == "__main__":
    unittest.main()
