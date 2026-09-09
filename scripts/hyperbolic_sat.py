#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

from morph_kem.hyperbolic import generate_a5_instance, validate_a5_frames
from morph_kem.hyperbolic_sat import (
    decode_a5_sat_model,
    encode_a5_sat,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Solve the MORPH H2 Klein-quartic/A5 relation with an external SAT solver."
    )
    parser.add_argument("--solver", default="minisat")
    parser.add_argument(
        "--master-seed",
        default="26457513110645905905016157536392",
        help="hex-encoded deterministic H2 generation seed",
    )
    args = parser.parse_args()

    solver = shutil.which(args.solver)
    if solver is None:
        parser.error(f"SAT solver not found: {args.solver}")

    public, reference = generate_a5_instance(bytes.fromhex(args.master_seed))
    if not validate_a5_frames(public, reference.frames).accepted:
        raise RuntimeError("reference witness unexpectedly rejected")

    encoding = encode_a5_sat(public)
    dimacs = encoding.to_dimacs()

    print(f"solver: {solver}")
    print(f"SAT variables: {encoding.variable_count}")
    print(f"SAT clauses: {len(encoding.clauses)}")
    print(f"DIMACS bytes: {len(dimacs.encode('ascii'))}")

    with tempfile.TemporaryDirectory(prefix="morph-h2-sat-") as directory:
        cnf_path = Path(directory) / "h2.cnf"
        model_path = Path(directory) / "h2.model"
        cnf_path.write_text(dimacs, encoding="ascii")

        started = time.perf_counter()
        completed = subprocess.run(
            [solver, str(cnf_path), str(model_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        elapsed = time.perf_counter() - started

        print(f"solver return code: {completed.returncode}")
        print(f"solver elapsed seconds: {elapsed:.6f}")

        interesting = (
            "restarts",
            "conflicts",
            "decisions",
            "propagations",
            "CPU time",
        )
        for line in completed.stdout.splitlines():
            if any(label in line for label in interesting):
                print(f"solver {line.strip()}")

        # MiniSat convention: 10 = SAT, 20 = UNSAT.
        if completed.returncode == 20:
            print("solver result: UNSAT")
            print("ERROR: generated instance has a known valid witness")
            return 2
        if completed.returncode != 10:
            print("solver result: UNKNOWN/ERROR")
            if completed.stderr:
                print(completed.stderr.strip())
            return 3
        if not model_path.exists():
            print("solver result: SAT without model file")
            return 4

        tokens = model_path.read_text(encoding="ascii").split()
        if not tokens or tokens[0] != "SAT":
            print("solver result: malformed model")
            return 5
        literals = tuple(
            int(token)
            for token in tokens[1:]
            if token not in {"0"}
        )
        model = decode_a5_sat_model(public, encoding, literals)
        print("solver result: SAT")
        print(f"decoded accepted witness: {model.accepted}")
        return 0 if model.accepted else 6


if __name__ == "__main__":
    raise SystemExit(main())
