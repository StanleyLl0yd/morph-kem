#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib

from morph_kem.gluing_sat import (
    G7_PARAMETER_SETS,
    generate_sat_phase_instance,
    recover_sat_by_dpll,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Sweep MORPH G7 planted signed 3-SAT negative control.")
    parser.add_argument(
        "--master-seed",
        default="76120450aabbccddeeff001122334455",
        help="hex deterministic generation seed",
    )
    parser.add_argument("--seeds", type=int, default=8)
    parser.add_argument("--solution-cap", type=int, default=16)
    args = parser.parse_args()

    if args.seeds <= 0 or args.seeds > 64:
        parser.error("--seeds must be in 1..64")

    master_seed = bytes.fromhex(args.master_seed)
    all_ok = True
    print(
        "set,seed,gadgets,total_tetrahedra,clauses,degree_hist,factor_components,"
        "factor_cycle_rank,affine_implications,matching_nodes,matching_backtracks,"
        "solutions,solution_cap,cap_hit,dpll_nodes,dpll_decisions,dpll_propagations,"
        "dpll_conflicts,dpll_backtracks,verifier_checks,accepted,nonreference,first_matches_reference"
    )

    for name in sorted(G7_PARAMETER_SETS):
        params = G7_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            seed = hashlib.sha256(
                b"MORPH-KEM G7 sweep v1\x00"
                + master_seed
                + name.encode("ascii")
                + seed_index.to_bytes(4, "big")
            ).digest()
            public, reference = generate_sat_phase_instance(params, seed)
            recovery = recover_sat_by_dpll(
                public, solution_cap=args.solution_cap, reference=reference
            )
            all_ok = all_ok and (
                recovery.local_affine_implications == 0
                and recovery.accepted_solutions >= 1
                and recovery.nonreference_accepted_solutions >= 1
            )
            degree_hist = "/".join(
                f"{degree}:{count}" for degree, count in recovery.variable_degree_histogram
            )
            print(
                f"{name},{seed_index},{recovery.gadget_count},{recovery.total_tetrahedra},"
                f"{recovery.clause_count},{degree_hist},{recovery.factor_components},"
                f"{recovery.factor_cycle_rank},{recovery.local_affine_implications},"
                f"{recovery.gadget_matching_nodes},{recovery.gadget_matching_backtracks},"
                f"{recovery.solution_count},{recovery.solution_cap},{int(recovery.solution_cap_hit)},"
                f"{recovery.dpll_nodes},{recovery.dpll_decisions},{recovery.dpll_propagations},"
                f"{recovery.dpll_conflicts},{recovery.dpll_backtracks},"
                f"{recovery.exact_verifier_clause_checks},{recovery.accepted_solutions},"
                f"{recovery.nonreference_accepted_solutions},{int(recovery.first_solution_matches_reference)}"
            )

    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
