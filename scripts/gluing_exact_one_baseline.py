#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.gluing_exact_one import (
    G5_PARAMETER_SETS,
    generate_exact_one_instance,
    recover_exact_one_via_parity,
    validate_exact_one_witness,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run MORPH G5 exact-one parity-projection negative control.")
    parser.add_argument("--params", choices=sorted(G5_PARAMETER_SETS), default="g5-24")
    parser.add_argument(
        "--master-seed",
        default="76120450aabbccddeeff001122334455",
        help="hex deterministic generation seed",
    )
    args = parser.parse_args()

    params = G5_PARAMETER_SETS[args.params]
    public, reference = generate_exact_one_instance(params, bytes.fromhex(args.master_seed))
    recovery = recover_exact_one_via_parity(public, reference=reference)
    reference_validation = validate_exact_one_witness(public, reference.groups)

    print(f"parameters: {params.name}")
    print(f"gadgets: {recovery.gadget_count}")
    print(f"total public tetrahedra: {recovery.total_tetrahedra}")
    print(f"clauses: {recovery.clause_count}")
    print(f"variable degree histogram: {recovery.variable_degree_histogram}")
    print(f"factor components/cycle rank: {recovery.factor_components}/{recovery.factor_cycle_rank}")
    print(f"per-gadget perfect matchings: {recovery.gadget_matching_solutions}")
    print(f"total local matching nodes/backtracks: {recovery.gadget_matching_nodes}/{recovery.gadget_matching_backtracks}")
    print(f"projected GF(2) equations/variables: {recovery.projected_equations}/{recovery.projected_variables}")
    print(f"GF(2) rank/nullity: {recovery.gf2_rank}/{recovery.gf2_nullity}")
    print(f"GF(2) row XORs: {recovery.gf2_row_xors}")
    print(f"affine solution count: {recovery.affine_solution_count}")
    print(f"nonlinear clause checks: {recovery.nonlinear_clause_checks}")
    print(f"public parity witness accepted by nonlinear verifier: {recovery.accepted}")
    print(f"public affine solution equals hidden reference: {recovery.matches_reference}")
    print(f"reference witness accepted: {reference_validation.valid}")

    return 0 if (
        reference_validation.valid
        and recovery.gf2_rank == params.gadget_count
        and recovery.gf2_nullity == 0
        and recovery.affine_solution_count == 1
        and recovery.accepted
        and recovery.matches_reference
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
