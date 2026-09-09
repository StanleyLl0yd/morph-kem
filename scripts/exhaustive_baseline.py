#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time

from morph_kem import TOY_PARAMETER_SETS, exhaustive_recover, forward, keygen


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the MORPH-KEM M0 exhaustive baseline.")
    parser.add_argument("--params", choices=sorted(TOY_PARAMETER_SETS), default="toy-8")
    parser.add_argument("--seed", type=lambda value: int(value, 0), default=0xA5)
    parser.add_argument(
        "--master-seed",
        default="00112233445566778899aabbccddeeff",
        help="hex-encoded deterministic key-generation seed",
    )
    args = parser.parse_args()

    params = TOY_PARAMETER_SETS[args.params]
    if args.seed < 0 or args.seed >= (1 << params.seed_bits):
        parser.error("seed is outside the selected parameter range")

    pk, _ = keygen(params, bytes.fromhex(args.master_seed))
    ct = forward(pk, args.seed)

    started = time.perf_counter()
    recovered = exhaustive_recover(pk, ct)
    elapsed = time.perf_counter() - started

    print(f"parameters: {params.name}")
    print(f"seed bits: {params.seed_bits}")
    print(f"target seed: {args.seed}")
    print(f"recovered seed: {recovered}")
    print(f"ciphertext bytes: {len(ct.encode())}")
    print(f"elapsed seconds: {elapsed:.6f}")
    return 0 if recovered == args.seed else 1


if __name__ == "__main__":
    raise SystemExit(main())
