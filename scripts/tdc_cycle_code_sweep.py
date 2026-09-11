#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib

from morph_kem.tdc_cycle_code import (
    TDC0_PARAMETER_SETS,
    cycle_code_metrics,
    generate_tdc0_instance,
    planted_single_edge_syndrome,
    recover_single_edge_error,
)


MASTER_SEED = bytes.fromhex("102132435465768798a9bacbdcedfe0f")


def _seed(name: str, index: int) -> bytes:
    return hashlib.sha256(
        b"MORPH-KEM TDC0 sweep v1\x00"
        + MASTER_SEED
        + name.encode("ascii")
        + index.to_bytes(4, "big")
    ).digest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sweep MORPH-KEM TDC0 incidence cycle-code control."
    )
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 64:
        parser.error("--seeds must be in [1,64]")

    print(
        "set,seed,V,E,F,rank,dimension,rate,min_distance,triangle_codewords,"
        "syndrome_weight,lookup_entries,accepted,matches_reference"
    )
    failures = 0
    for name in sorted(TDC0_PARAMETER_SETS):
        params = TDC0_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            public, reference = generate_tdc0_instance(params, _seed(name, seed_index))
            metrics = cycle_code_metrics(public)
            syndrome = planted_single_edge_syndrome(public, reference)
            recovery = recover_single_edge_error(public, syndrome, reference=reference)
            print(
                f"{name},{seed_index},{metrics.vertices},{metrics.edges},{metrics.triangles},"
                f"{metrics.parity_rank},{metrics.code_dimension},{metrics.rate:.9f},"
                f"{metrics.exact_minimum_distance},{metrics.triangle_codeword_count},"
                f"{recovery.syndrome_weight},{recovery.lookup_entries},"
                f"{int(recovery.accepted)},"
                f"{int(bool(recovery.matches_reference_after_public_success))}"
            )
            failures += int(
                metrics.exact_minimum_distance != 3
                or metrics.triangle_codeword_count != metrics.triangles
                or not recovery.accepted
                or not recovery.matches_reference_after_public_success
            )

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
