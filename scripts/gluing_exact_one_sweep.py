#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib

from morph_kem.gluing_exact_one import (
    G5_PARAMETER_SETS,
    generate_exact_one_instance,
    recover_exact_one_via_parity,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Sweep MORPH G5 exact-one parity-projection negative control.")
    parser.add_argument(
        "--master-seed",
        default="76120450aabbccddeeff001122334455",
        help="hex deterministic generation seed",
    )
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds <= 0 or args.seeds > 64:
        parser.error("--seeds must be in 1..64")

    master_seed = bytes.fromhex(args.master_seed)
    all_ok = True
    print(
        "set,seed,gadgets,total_tetrahedra,clauses,degree_hist,factor_components,factor_cycle_rank,"
        "matching_nodes,matching_backtracks,projected_eqs,projected_vars,rank,nullity,row_xors,"
        "affine_solutions,nonlinear_checks,accepted,matches_reference"
    )

    for name in sorted(G5_PARAMETER_SETS):
        params = G5_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            seed = hashlib.sha256(
                b"MORPH-KEM G5 sweep v1\x00"
                + master_seed
                + name.encode("ascii")
                + seed_index.to_bytes(4, "big")
            ).digest()
            public, reference = generate_exact_one_instance(params, seed)
            recovery = recover_exact_one_via_parity(public, reference=reference)
            ok = (
                recovery.gf2_rank == params.gadget_count
                and recovery.gf2_nullity == 0
                and recovery.affine_solution_count == 1
                and recovery.accepted
                and recovery.matches_reference
            )
            all_ok = all_ok and ok
            degree_hist = "/".join(f"{degree}:{count}" for degree, count in recovery.variable_degree_histogram)
            print(
                f"{name},{seed_index},{recovery.gadget_count},{recovery.total_tetrahedra},"
                f"{recovery.clause_count},{degree_hist},{recovery.factor_components},"
                f"{recovery.factor_cycle_rank},{recovery.gadget_matching_nodes},"
                f"{recovery.gadget_matching_backtracks},{recovery.projected_equations},"
                f"{recovery.projected_variables},{recovery.gf2_rank},{recovery.gf2_nullity},"
                f"{recovery.gf2_row_xors},{recovery.affine_solution_count},"
                f"{recovery.nonlinear_clause_checks},{int(recovery.accepted)},"
                f"{int(recovery.matches_reference)}"
            )

    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
