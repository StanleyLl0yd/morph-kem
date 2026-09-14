from __future__ import annotations

import argparse
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


def seed_for(name: str, index: int, suffix: str) -> bytes:
    return hashlib.sha256(
        f"MORPH-KEM NAT7 {name} seed {index} {suffix} v1".encode("ascii")
    ).digest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 32:
        raise SystemExit("--seeds must be in 1..32")

    print(
        "set,seed,V,E,tree,non_tree,assignments,tree_identity,nonidentity,distinct,"
        "reconstruct,regauged_reconstruct,same_tree,same_residuals"
    )
    for params in NAT6_PARAMETER_SETS.values():
        for index in range(args.seeds):
            public, _ = generate_nat6_instance(
                params, seed_for(params.name, index, "instance")
            )
            edges = _edges(public.target)
            first = normalize_connection(
                len(public.target.vertices), edges, public.observed_edge_labels, OPS
            )
            gauge = _normalized_hidden_labels(
                public.target,
                seed_for(params.name, index, "comparison-gauge"),
                f"nat7-{params.name}-{index}-comparison",
            )
            gauged = apply_normalized_vertex_gauge(
                edges, public.observed_edge_labels, gauge, OPS
            )
            second = normalize_connection(
                len(public.target.vertices), edges, gauged, OPS
            )
            print(
                f"{params.name},{index},{first.vertex_count},{first.edge_count},"
                f"{len(first.tree_edge_indices)},{len(first.non_tree_edge_indices)},"
                f"{first.tree_assignments},{first.tree_identity_residuals},"
                f"{first.nonidentity_residuals},{first.distinct_nonidentity_residuals},"
                f"{int(first.reconstruction_verified)},{int(second.reconstruction_verified)},"
                f"{int(first.tree_edge_indices == second.tree_edge_indices)},"
                f"{int(first.residual_labels == second.residual_labels)}"
            )


if __name__ == "__main__":
    main()
