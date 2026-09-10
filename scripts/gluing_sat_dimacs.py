#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from morph_kem.gluing_sat import G7_PARAMETER_SETS, generate_sat_phase_instance, sat_dimacs


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit a public G7 signed 3-SAT instance as DIMACS CNF.")
    parser.add_argument("--params", choices=sorted(G7_PARAMETER_SETS), default="g7-24")
    parser.add_argument(
        "--master-seed",
        default="76120450aabbccddeeff001122334455",
        help="hex deterministic generation seed",
    )
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    public, _ = generate_sat_phase_instance(
        G7_PARAMETER_SETS[args.params], bytes.fromhex(args.master_seed)
    )
    Path(args.output).write_text(sat_dimacs(public))
    print(f"wrote {len(public.clauses)} public clauses over {len(public.gadgets)} phase variables")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
