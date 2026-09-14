from __future__ import annotations

import argparse
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


def seed_for(name: str, index: int) -> bytes:
    return hashlib.sha256(
        f"MORPH-KEM NAT8 sweep {name} seed {index} v1".encode("ascii")
    ).digest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 32:
        raise SystemExit("--seeds must be in 1..32")

    print(
        "set,seed,V,E,F,free_rank,public_generator_images,nonidentity_generator_images,"
        "tree_identity,nonidentity_face_relators,residual_reconstructed,connection_reconstructed"
    )
    for params in NAT6_PARAMETER_SETS.values():
        for index in range(args.seeds):
            public, _ = generate_nat6_instance(params, seed_for(params.name, index))
            edges = _edges(public.target)
            triangles = _triangles(public.target)
            result = extract_residual_representation(
                len(public.target.vertices), edges, public.observed_edge_labels, OPS
            )
            relators = triangle_relator_holonomies(
                edges, public.observed_edge_labels, triangles, OPS
            )
            print(
                f"{params.name},{index},{len(public.target.vertices)},{len(edges)},{len(triangles)},"
                f"{result.free_rank},{len(result.generator_images)},"
                f"{result.generator_residuals_nonidentity},{result.tree_identity_residuals},"
                f"{sum(value != _IDENTITY for value in relators)},"
                f"{int(result.residual_vector_reconstructed)},{int(result.connection_reconstructed)}"
            )


if __name__ == "__main__":
    main()
