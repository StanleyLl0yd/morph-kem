#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.nonorientable_map import analyze_cell_orientability
from morph_kem.twisted_a5 import (
    audit_semidirect_product,
    audit_twisted_flattening,
    generate_twisted_a5_instance,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the MORPH K2.0 orientation-twisted A5/S5 flattening calibration."
    )
    parser.add_argument(
        "--master-seed",
        default="36026490a1b2c3d4e5f60718293a4b5c",
        help="hex-encoded deterministic K2.0 generation seed",
    )
    args = parser.parse_args()

    algebra = audit_semidirect_product()
    public, reference = generate_twisted_a5_instance(
        bytes.fromhex(args.master_seed)
    )
    flattening = audit_twisted_flattening(public, reference)
    orientation = analyze_cell_orientability(public.base_map)

    print(f"semidirect elements: {algebra.twisted_elements}")
    print(f"S5 image elements: {algebra.s5_image_elements}")
    print(f"semidirect bijective: {algebra.bijective}")
    print(f"semidirect homomorphic: {algebra.homomorphic}")
    print(f"multiplication checks: {algebra.multiplication_checks}")
    print(f"orientation/parity checks: {algebra.parity_checks}")
    print(
        "orientation component equals S5 parity: "
        f"{algebra.orientation_equals_s5_parity}"
    )
    print(
        "base V/E/F: "
        f"{len(public.base_map.vertices)}/"
        f"{len(public.base_map.edges)}/"
        f"{len(public.base_map.faces)}"
    )
    print(f"base orientable: {orientation.orientable}")
    print(
        "base nonzero orientation syndromes: "
        f"{orientation.nonzero_syndromes}/{orientation.cycle_rank}"
    )
    print(f"twisted public edges: {flattening.edges}")
    print(
        "endpoint assignments checked: "
        f"{flattening.endpoint_assignments_checked}"
    )
    print(f"relation mismatches: {flattening.relation_mismatches}")
    print(
        "public edge parity matches orientation: "
        f"{flattening.public_edge_parity_matches}/{flattening.edges}"
    )
    print(
        "planted twisted accepted: "
        f"{flattening.planted_twisted_accepted}"
    )
    print(
        "planted flattened accepted: "
        f"{flattening.planted_flattened_accepted}"
    )

    return 0 if (
        algebra.bijective
        and algebra.homomorphic
        and algebra.orientation_equals_s5_parity
        and flattening.exact_relation_match
        and flattening.public_edge_parity_matches == flattening.edges
        and flattening.planted_twisted_accepted
        and flattening.planted_flattened_accepted
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
