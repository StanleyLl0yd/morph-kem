from __future__ import annotations

import hashlib

from morph_kem.gluing_cohomology_cycle import _edges
from morph_kem.nat_a5 import _IDENTITY, _normalized_hidden_labels, compose, inverse
from morph_kem.nat_a5_torus_flat import NAT6_PARAMETER_SETS, generate_nat6_instance
from morph_kem.nat_tree_gauge import (
    GroupOps,
    apply_normalized_vertex_gauge,
    normalize_connection,
)


OPS = GroupOps(_IDENTITY, compose, inverse)


def digest(label: str) -> bytes:
    return hashlib.sha256(label.encode("ascii")).digest()


def main() -> None:
    params = NAT6_PARAMETER_SETS["nat6-8x9"]
    public, _ = generate_nat6_instance(params, digest("MORPH-KEM NAT7 fixed baseline v1"))
    edges = _edges(public.target)
    first = normalize_connection(
        len(public.target.vertices), edges, public.observed_edge_labels, OPS
    )
    comparison_gauge = _normalized_hidden_labels(
        public.target,
        digest("MORPH-KEM NAT7 independent comparison gauge v1"),
        "nat7-fixed-comparison",
    )
    gauged = apply_normalized_vertex_gauge(
        edges, public.observed_edge_labels, comparison_gauge, OPS
    )
    second = normalize_connection(len(public.target.vertices), edges, gauged, OPS)

    print(f"parameters: {params.name}")
    print(f"vertices / edges: {first.vertex_count}/{first.edge_count}")
    print(f"tree / non-tree edges: {len(first.tree_edge_indices)}/{len(first.non_tree_edge_indices)}")
    print(f"tree assignments: {first.tree_assignments}")
    print(f"tree identity residuals: {first.tree_identity_residuals}")
    print(f"nonidentity residuals: {first.nonidentity_residuals}")
    print(f"distinct nonidentity residuals: {first.distinct_nonidentity_residuals}")
    print(f"exact reconstruction: {first.reconstruction_verified}")
    print(f"regauged exact reconstruction: {second.reconstruction_verified}")
    print(f"tree choice invariant under normalized gauge: {first.tree_edge_indices == second.tree_edge_indices}")
    print(f"canonical residual invariant under normalized gauge: {first.residual_labels == second.residual_labels}")


if __name__ == "__main__":
    main()
