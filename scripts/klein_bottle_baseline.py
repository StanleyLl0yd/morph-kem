#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.klein_bottle import (
    KLEIN_BOTTLE_PARAMETER_SETS,
    analyze_klein_orientability,
    generate_klein_orientation_instance,
    normalize_klein_transitions,
    recover_klein_gauge,
    reference_gauge_matches,
    validate_klein_reference,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the MORPH K0 Klein-bottle orientation-gauge calibration."
    )
    parser.add_argument(
        "--params",
        choices=sorted(KLEIN_BOTTLE_PARAMETER_SETS),
        default="klein-bottle-5x4",
    )
    parser.add_argument(
        "--master-seed",
        default="30124490aabbccddeeff1029384756ab",
        help="hex-encoded deterministic K0 generation seed",
    )
    args = parser.parse_args()

    parameters = KLEIN_BOTTLE_PARAMETER_SETS[args.params]
    public, reference = generate_klein_orientation_instance(
        parameters,
        bytes.fromhex(args.master_seed),
    )
    scaffold = public.scaffold
    orientation = analyze_klein_orientability(scaffold)
    public_normal = normalize_klein_transitions(
        scaffold,
        public.transitions,
    )
    canonical = tuple(
        edge.canonical_transition
        for edge in scaffold.dual_edges
    )
    canonical_normal = normalize_klein_transitions(
        scaffold,
        canonical,
    )
    recovery = recover_klein_gauge(public)

    print(f"parameters: {parameters.name}")
    print(
        "cells V/E/F: "
        f"{len(scaffold.complex.vertices)}/"
        f"{len(scaffold.edges)}/"
        f"{len(scaffold.faces)}"
    )
    print(f"Euler characteristic: {scaffold.euler_characteristic}")
    print(f"free collapse pairs: {len(scaffold.complex.free_collapse_pairs())}")
    print(
        "dual V/E/cycle-rank: "
        f"{len(scaffold.faces)}/"
        f"{len(scaffold.dual_edges)}/"
        f"{scaffold.dual_cycle_rank}"
    )
    print(f"orientable: {orientation.orientable}")
    print(
        "nonzero fundamental orientation syndromes: "
        f"{orientation.nonzero_syndromes}/"
        f"{orientation.cycle_rank}"
    )
    print(f"reference valid: {validate_klein_reference(public, reference)}")
    print(
        "public normalization equals canonical normalization: "
        f"{public_normal.normalized_transitions == canonical_normal.normalized_transitions}"
    )
    print(
        "tree transitions normalized to zero: "
        f"{sum(public_normal.normalized_transitions[i] == 0 for i in public_normal.tree_edge_indices)}/"
        f"{len(public_normal.tree_edge_indices)}"
    )
    print(f"hidden gauge recovery consistent: {recovery.consistent}")
    print(
        "hidden face gauges recovered up to global bit: "
        f"{reference_gauge_matches(recovery, reference)}"
    )
    print(f"public edge checks: {recovery.edge_checks}")
    print("residual global orientation-gauge choices: 2")

    return 0 if (
        not orientation.orientable
        and recovery.consistent
        and reference_gauge_matches(recovery, reference)
        and public_normal.normalized_transitions
        == canonical_normal.normalized_transitions
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
