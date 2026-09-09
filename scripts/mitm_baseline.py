#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time

from morph_kem.path import (
    PATH_PARAMETER_SETS,
    generate_path_instance,
    mitm_path_recover,
    path_forward,
    support_metrics,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the MORPH-KEM M1 meet-in-the-middle baseline.")
    parser.add_argument("--params", choices=sorted(PATH_PARAMETER_SETS), default="path-16")
    parser.add_argument("--seed", type=lambda value: int(value, 0), default=0xB6D3)
    parser.add_argument(
        "--master-seed",
        default="102132435465768798a9bacbdcedfe0f",
        help="hex-encoded deterministic instance-generation seed",
    )
    args = parser.parse_args()

    params = PATH_PARAMETER_SETS[args.params]
    if args.seed < 0 or args.seed >= (1 << params.layers):
        parser.error("seed is outside the selected path range")

    instance = generate_path_instance(params, bytes.fromhex(args.master_seed))
    target = path_forward(instance, args.seed)
    metrics = support_metrics(instance)

    started = time.perf_counter()
    result = mitm_path_recover(instance, target)
    elapsed = time.perf_counter() - started

    print(f"parameters: {params.name}")
    print(f"layers: {params.layers}")
    print(f"vertices: {params.vertices}")
    print(f"branch support min/mean: {metrics.branch_min}/{metrics.branch_mean:.2f}")
    print(f"relative support min/mean: {metrics.relative_min}/{metrics.relative_mean:.2f}")
    print(f"target seed: {args.seed}")
    print(f"preimages: {result.preimages}")
    print(f"forward states: {result.forward_states}")
    print(f"reverse states: {result.reverse_states}")
    print(f"candidate matches: {result.candidate_matches}")
    print(f"elapsed seconds: {elapsed:.6f}")
    return 0 if args.seed in result.preimages else 1


if __name__ == "__main__":
    raise SystemExit(main())
