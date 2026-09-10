#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.gluing_sat import (
    G7_PARAMETER_SETS,
    generate_sat_phase_instance,
    recover_sat_by_dpll,
    validate_sat_witness,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run MORPH G7 planted signed 3-SAT negative control.")
    parser.add_argument("--params", choices=sorted(G7_PARAMETER_SETS), default="g7-24")
    parser.add_argument(
        "--master-seed",
        default="76120450aabbccddeeff001122334455",
        help="hex deterministic generation seed",
    )
    parser.add_argument("--solution-cap", type=int, default=16)
    args = parser.parse_args()

    params = G7_PARAMETER_SETS[args.params]
    public, reference = generate_sat_phase_instance(params, bytes.fromhex(args.master_seed))
    recovery = recover_sat_by_dpll(
        public, solution_cap=args.solution_cap, reference=reference
    )
    reference_validation = validate_sat_witness(public, reference.groups)

    print(f"parameters: {params.name}")
    print(f"gadgets: {recovery.gadget_count}")
    print(f"total public tetrahedra: {recovery.total_tetrahedra}")
    print(f"clauses: {recovery.clause_count}")
    print(f"variable degree histogram: {recovery.variable_degree_histogram}")
    print(f"factor components/cycle rank: {recovery.factor_components}/{recovery.factor_cycle_rank}")
    print(f"local nontrivial affine implications: {recovery.local_affine_implications}")
    print(f"per-gadget perfect matchings: {recovery.gadget_matching_solutions}")
    print(f"total local matching nodes/backtracks: {recovery.gadget_matching_nodes}/{recovery.gadget_matching_backtracks}")
    print(f"DPLL solutions/cap: {recovery.solution_count}/{recovery.solution_cap}")
    print(f"DPLL cap hit: {recovery.solution_cap_hit}")
    print(f"DPLL nodes/decisions: {recovery.dpll_nodes}/{recovery.dpll_decisions}")
    print(f"DPLL propagations/conflicts/backtracks: {recovery.dpll_propagations}/{recovery.dpll_conflicts}/{recovery.dpll_backtracks}")
    print(f"exact verifier clause checks: {recovery.exact_verifier_clause_checks}")
    print(f"accepted DPLL solutions: {recovery.accepted_solutions}")
    print(f"accepted non-reference solutions: {recovery.nonreference_accepted_solutions}")
    print(f"first DPLL solution equals hidden reference: {recovery.first_solution_matches_reference}")
    print(f"reference witness accepted: {reference_validation.valid}")

    return 0 if (
        recovery.local_affine_implications == 0
        and recovery.accepted_solutions >= 1
        and recovery.nonreference_accepted_solutions >= 1
        and reference_validation.valid
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
