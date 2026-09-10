#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.gluing_residual import (
    G6_PARAMETER_SETS,
    generate_residual_exact_one_instance,
    recover_residual_exact_one,
)
from morph_kem.gluing_exact_one import validate_exact_one_witness


def main() -> int:
    parser = argparse.ArgumentParser(description="Run MORPH G6 affine-coset residual negative control.")
    parser.add_argument("--params", choices=sorted(G6_PARAMETER_SETS), default="g6-24")
    parser.add_argument(
        "--master-seed",
        default="76120450aabbccddeeff001122334455",
        help="hex deterministic generation seed",
    )
    args = parser.parse_args()

    params = G6_PARAMETER_SETS[args.params]
    public, reference = generate_residual_exact_one_instance(
        params, bytes.fromhex(args.master_seed)
    )
    recovery = recover_residual_exact_one(public, reference=reference)
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
    print(f"affine candidates: {recovery.affine_candidate_count}")
    print(f"residual nonlinear clause checks: {recovery.residual_clause_checks}")
    print(f"accepted affine candidates: {recovery.accepted_candidate_count}")
    print(f"exact verifier clause checks: {recovery.exact_verifier_clause_checks}")
    print(f"accepted non-reference candidates: {recovery.nonreference_accepted_candidates}")
    print(f"first accepted candidate equals hidden reference: {recovery.first_accepted_matches_reference}")
    print(f"reference witness accepted: {reference_validation.valid}")

    return 0 if (
        recovery.gf2_nullity == 2
        and recovery.affine_candidate_count == 4
        and recovery.accepted_candidate_count >= 1
        and reference_validation.valid
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
