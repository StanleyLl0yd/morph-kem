from __future__ import annotations

import hashlib

from morph_kem.gluing_cohomology_cycle import _edges, _triangles
from morph_kem.nat_a5 import _IDENTITY, compose, inverse
from morph_kem.nat_a5_torus_flat import NAT6_PARAMETER_SETS, generate_nat6_instance
from morph_kem.nat_residual_representation import (
    extract_residual_representation,
    triangle_relator_holonomies,
)
from morph_kem.nat_tree_gauge import GroupOps


OPS = GroupOps(_IDENTITY, compose, inverse)


def digest(label: str) -> bytes:
    return hashlib.sha256(label.encode("ascii")).digest()


def main() -> None:
    params = NAT6_PARAMETER_SETS["nat6-8x9"]
    public, _ = generate_nat6_instance(
        params, digest("MORPH-KEM NAT8 fixed baseline v1")
    )
    edges = _edges(public.target)
    triangles = _triangles(public.target)
    result = extract_residual_representation(
        len(public.target.vertices), edges, public.observed_edge_labels, OPS
    )
    relators = triangle_relator_holonomies(
        edges, public.observed_edge_labels, triangles, OPS
    )

    print(f"parameters: {params.name}")
    print(f"vertices / edges / triangles: {len(public.target.vertices)}/{len(edges)}/{len(triangles)}")
    print(f"tree / generator edges: {len(result.tree_edge_indices)}/{len(result.generator_edge_indices)}")
    print(f"free rank E-V+1: {result.free_rank}")
    print(f"public generator images: {len(result.generator_images)}")
    print(f"nonidentity generator images: {result.generator_residuals_nonidentity}")
    print(f"tree identity residuals: {result.tree_identity_residuals}")
    print(f"public triangular relators: {len(relators)}")
    print(f"nonidentity triangular relators: {sum(value != _IDENTITY for value in relators)}")
    print(f"residual vector reconstructed: {result.residual_vector_reconstructed}")
    print(f"exact connection reconstructed: {result.connection_reconstructed}")


if __name__ == "__main__":
    main()
