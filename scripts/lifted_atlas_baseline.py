#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.lifted_atlas import (
    LIFTED_ATLAS_PARAMETER_SETS,
    canonicalize_public_cover,
    check_lift_equivariance,
    compare_to_reference,
    generate_lifted_atlas,
    residual_root_relabelings,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the MORPH H3-E0 lifted-atlas gauge baseline.")
    parser.add_argument(
        "--params",
        choices=sorted(LIFTED_ATLAS_PARAMETER_SETS),
        default="lift-12x5",
    )
    parser.add_argument(
        "--master-seed",
        default="22360679774997896964091736687312",
        help="hex-encoded deterministic H3-E0 generation seed",
    )
    args = parser.parse_args()

    public, reference = generate_lifted_atlas(
        LIFTED_ATLAS_PARAMETER_SETS[args.params],
        bytes.fromhex(args.master_seed),
    )
    normalization = canonicalize_public_cover(public)
    comparison = compare_to_reference(public, reference, normalization)

    path = tuple(range(public.graph.vertices))
    lift = check_lift_equivariance(
        public,
        normalization,
        path,
        public_start_sheet=0,
    )

    print(f"parameters: {args.params}")
    print(f"base V/E/cycle-rank: {public.graph.vertices}/{len(public.graph.edges)}/{public.graph.cycle_rank}")
    print(f"sheets: {public.parameters.sheets}")
    print(f"tree edges normalized to identity: {normalization.tree_identity_edges}/{public.graph.vertices - 1}")
    print(f"public chord monodromies retained: {normalization.chord_edges}")
    print(f"public attack point-operations estimate: {normalization.permutation_point_ops}")
    print(f"equivalent to secret canonical cover up to one global conjugation: {comparison.globally_conjugate}")
    print(f"path-lift equivariance preserved: {lift.holds}")
    print(f"residual root sheet relabelings: {residual_root_relabelings(public)}")
    print("interpretation: residual relabelings are equivalent-cover gauge, not a useful trapdoor")
    return 0 if comparison.globally_conjugate and lift.holds else 1


if __name__ == "__main__":
    raise SystemExit(main())
