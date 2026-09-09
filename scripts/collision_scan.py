#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time

from morph_kem.path import PATH_PARAMETER_SETS, generate_path_instance, path_collision_profile


def main() -> int:
    parser = argparse.ArgumentParser(description="Enumerate output collisions in an M1 path instance.")
    parser.add_argument("--params", choices=sorted(PATH_PARAMETER_SETS), default="path-12")
    parser.add_argument(
        "--master-seed",
        default="102132435465768798a9bacbdcedfe0f",
        help="hex-encoded deterministic instance-generation seed",
    )
    parser.add_argument("--max-states", type=int, default=1 << 16)
    args = parser.parse_args()

    instance = generate_path_instance(PATH_PARAMETER_SETS[args.params], bytes.fromhex(args.master_seed))
    started = time.perf_counter()
    profile = path_collision_profile(instance, max_states=args.max_states)
    elapsed = time.perf_counter() - started

    print(f"parameters: {args.params}")
    print(f"total seeds: {profile.total_seeds}")
    print(f"unique outputs: {profile.unique_outputs}")
    print(f"colliding outputs: {profile.colliding_outputs}")
    print(f"max multiplicity: {profile.max_multiplicity}")
    print(f"elapsed seconds: {elapsed:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
