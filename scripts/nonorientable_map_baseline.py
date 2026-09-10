#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.nonorientable_map import (
    analyze_cell_orientability,
    build_orientation_double_cover,
    generate_k1_orientation_instance,
    k1_reference_gauge_matches,
    normalize_cell_transitions,
    recover_k1_gauge,
    regular_type_is_hyperbolic,
    validate_k1_reference,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the MORPH K1 non-orientable hyperbolic control."
    )
    parser.add_argument(
        "--master-seed",
        default="34016490ffeeddccbbaa1234567890ab",
        help="hex-encoded deterministic K1 generation seed",
    )
    args = parser.parse_args()

    public, reference = generate_k1_orientation_instance(
        bytes.fromhex(args.master_seed)
    )
    base = public.base_map
    orientation = analyze_cell_orientability(base)
    recovery = recover_k1_gauge(public)
    public_normal = normalize_cell_transitions(base, public.transitions)
    canonical = tuple(
        edge.canonical_transition
        for edge in base.dual_edges
    )
    canonical_normal = normalize_cell_transitions(base, canonical)
    lifted = build_orientation_double_cover(base, public.transitions)
    cover_orientation = analyze_cell_orientability(lifted.cover)

    print(f"map: {base.name}")
    print(
        "base V/E/F: "
        f"{len(base.vertices)}/{len(base.edges)}/{len(base.faces)}"
    )
    print(f"base vertex degrees: {sorted(set(base.vertex_degrees))}")
    print(f"base face sizes: {sorted(set(base.face_sizes))}")
    print(f"base edge-face degrees: {sorted(set(base.edge_face_degrees))}")
    print(f"base Euler characteristic: {base.euler_characteristic}")
    print(f"base dual cycle rank: {base.dual_cycle_rank}")
    print(f"regular type hyperbolic: {regular_type_is_hyperbolic(6, 4)}")
    print(f"base orientable: {orientation.orientable}")
    print(
        "nonzero fundamental orientation syndromes: "
        f"{orientation.nonzero_syndromes}/{orientation.cycle_rank}"
    )
    print(f"reference valid: {validate_k1_reference(public, reference)}")
    print(
        "public normalization equals canonical normalization: "
        f"{public_normal.normalized_transitions == canonical_normal.normalized_transitions}"
    )
    print(
        "hidden face gauges recovered up to global bit: "
        f"{k1_reference_gauge_matches(recovery, reference)}"
    )
    print(f"public gauge edge checks: {recovery.edge_checks}")

    cover = lifted.cover
    print(
        "orientation cover V/E/F: "
        f"{len(cover.vertices)}/{len(cover.edges)}/{len(cover.faces)}"
    )
    print(f"orientation cover Euler characteristic: {cover.euler_characteristic}")
    print(f"orientation cover orientable: {cover_orientation.orientable}")
    print(
        "orientation cover genus: "
        f"{(2 - cover.euler_characteristic) // 2 if cover_orientation.orientable else -1}"
    )
    print(
        "cover reconstructed from public transitions: "
        f"{lifted.reconstructed_from_public_transitions}"
    )

    return 0 if (
        not orientation.orientable
        and recovery.consistent
        and k1_reference_gauge_matches(recovery, reference)
        and cover_orientation.orientable
        and len(cover.vertices) == 12
        and len(cover.edges) == 24
        and len(cover.faces) == 8
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
