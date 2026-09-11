#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.tdc_cycle_code import (
    TDC0_PARAMETER_SETS,
    cycle_code_metrics,
    generate_tdc0_instance,
    planted_single_edge_syndrome,
    recover_single_edge_error,
)


MASTER_SEED = bytes.fromhex("102132435465768798a9bacbdcedfe0f")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run MORPH-KEM TDC0 incidence cycle-code negative control."
    )
    parser.add_argument("--params", choices=sorted(TDC0_PARAMETER_SETS), default="tdc0-8x8")
    args = parser.parse_args()

    params = TDC0_PARAMETER_SETS[args.params]
    public, reference = generate_tdc0_instance(params, MASTER_SEED)
    metrics = cycle_code_metrics(public)
    syndrome = planted_single_edge_syndrome(public, reference)
    recovery = recover_single_edge_error(public, syndrome, reference=reference)

    print(f"parameters: {params.name}")
    print(f"public V/E/F: {metrics.vertices}/{metrics.edges}/{metrics.triangles}")
    print(f"parity rank: {metrics.parity_rank}")
    print(f"code dimension: {metrics.code_dimension}")
    print(f"code rate: {metrics.rate:.9f}")
    print(f"row weight histogram: {metrics.row_weight_histogram}")
    print(f"column weight histogram: {metrics.column_weight_histogram}")
    print(f"public triangle codewords: {metrics.triangle_codeword_count}")
    print(
        "triangle codeword weight histogram: "
        f"{metrics.triangle_codeword_weight_histogram}"
    )
    print(f"exact minimum distance: {metrics.exact_minimum_distance}")
    print(f"single-edge syndrome weight: {recovery.syndrome_weight}")
    print(f"single-edge lookup entries: {recovery.lookup_entries}")
    print(f"single-edge public recovery accepted: {recovery.accepted}")
    print(
        "single-edge recovery matches reference after public success: "
        f"{recovery.matches_reference_after_public_success}"
    )

    return 0 if (
        metrics.exact_minimum_distance == 3
        and recovery.accepted
        and recovery.matches_reference_after_public_success
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
