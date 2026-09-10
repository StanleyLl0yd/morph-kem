#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.gluing_coupled import (
    G4_PARAMETER_SETS,
    generate_coupled_phase_instance,
    recover_coupled_phases,
    validate_coupled_phase_witness,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run MORPH G4 coupled-phase parity negative control.")
    parser.add_argument("--params", choices=sorted(G4_PARAMETER_SETS), default="g4-12")
    parser.add_argument(
        "--master-seed",
        default="76120450aabbccddeeff001122334455",
        help="hex deterministic generation seed",
    )
    args = parser.parse_args()

    params = G4_PARAMETER_SETS[args.params]
    public, reference = generate_coupled_phase_instance(params, bytes.fromhex(args.master_seed))
    recovery = recover_coupled_phases(public, reference=reference)
    reference_validation = validate_coupled_phase_witness(public, reference.groups)

    print(f"parameters: {params.name}")
    print(f"gadgets: {recovery.gadget_count}")
    print(f"total public tetrahedra: {recovery.total_tetrahedra}")
    print(f"coupling vertices/edges: {recovery.gadget_count}/{recovery.coupling_edges}")
    print(f"coupling cycle rank: {recovery.coupling_cycle_rank}")
    print(f"per-gadget perfect matchings: {recovery.gadget_matching_solutions}")
    print(f"total local matching nodes/backtracks: {recovery.gadget_matching_nodes}/{recovery.gadget_matching_backtracks}")
    print(f"XOR equations/variables: {recovery.xor_equations}/{recovery.xor_variables}")
    print(f"GF(2) rank/nullity: {recovery.gf2_rank}/{recovery.gf2_nullity}")
    print(f"GF(2) row XORs: {recovery.gf2_row_xors}")
    print(f"propagation tree assignments: {recovery.propagation_tree_assignments}")
    print(f"propagation constraint checks: {recovery.propagation_constraint_checks}")
    print(f"recovered phase solutions: {recovery.phase_solutions}")
    print(f"accepted public solutions: {recovery.accepted_solutions}")
    print(f"accepted non-reference solutions: {recovery.nonreference_accepted_solutions}")
    print(f"reference witness accepted: {reference_validation.valid}")

    return 0 if (
        reference_validation.valid
        and recovery.gf2_rank == params.gadget_count - 1
        and recovery.gf2_nullity == 1
        and recovery.phase_solutions == 2
        and recovery.accepted_solutions == 2
        and recovery.nonreference_accepted_solutions == 1
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
