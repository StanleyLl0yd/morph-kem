#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

from morph_kem.gluing_surface_hypercover import (
    G11_PARAMETER_SETS,
    decode_toroidal_hypercover_sat_model,
    encode_toroidal_hypercover_sat,
    generate_toroidal_hypercover_instance,
    toroidal_hypercover_reference_matches,
)


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Cross-check MORPH-KEM G11 P3 hypercover with MiniSat."
    )
    parser.add_argument("--params", choices=sorted(G11_PARAMETER_SETS), default="g11-6x9")
    parser.add_argument("--solver", default="minisat")
    args = parser.parse_args()

    solver = shutil.which(args.solver)
    if solver is None:
        parser.error(f"SAT solver not found: {args.solver}")

    public, reference = generate_toroidal_hypercover_instance(
        G11_PARAMETER_SETS[args.params], MASTER_SEED
    )
    encoding = encode_toroidal_hypercover_sat(public)
    dimacs = encoding.to_dimacs()

    print(f"parameters: {args.params}")
    print(f"solver: {solver}")
    print(f"SAT variables: {encoding.variable_count}")
    print(f"SAT clauses: {len(encoding.clauses)}")
    print(f"DIMACS bytes: {len(dimacs.encode('ascii'))}")

    with tempfile.TemporaryDirectory(prefix="morph-g11-sat-") as directory:
        cnf_path = Path(directory) / "g11.cnf"
        model_path = Path(directory) / "g11.model"
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
        for line in completed.stdout.splitlines():
            if any(
                label in line
                for label in ("restarts", "conflicts", "decisions", "propagations", "CPU time")
            ):
                print(f"solver {line.strip()}")

        if completed.returncode == 20:
            print("solver result: UNSAT")
            print("ERROR: generated G11 instance has a known valid reference cover")
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
        literals = tuple(int(token) for token in tokens[1:] if token != "0")
        model = decode_toroidal_hypercover_sat_model(public, encoding, literals)
        print("solver result: SAT")
        print(f"selected candidate pieces: {len(model.groups)}")
        print(f"decoded accepted witness: {model.validation.valid}")
        print(
            "decoded witness matches reference after public success: "
            f"{toroidal_hypercover_reference_matches(reference, model.groups)}"
        )
        return 0 if model.validation.valid else 6


if __name__ == "__main__":
    raise SystemExit(main())
