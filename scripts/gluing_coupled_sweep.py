#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib

from morph_kem.gluing_coupled import (
    G4_PARAMETER_SETS,
    generate_coupled_phase_instance,
    recover_coupled_phases,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Sweep MORPH G4 coupled-phase parity negative control.")
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
        "set,seed,gadgets,total_tetrahedra,coupling_edges,cycle_rank,matching_nodes,matching_backtracks,"
        "xor_eqs,xor_vars,rank,nullity,row_xors,tree_assignments,constraint_checks,phase_solutions,accepted,nonreference"
    )

    for name in sorted(G4_PARAMETER_SETS):
        params = G4_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            seed = hashlib.sha256(
                b"MORPH-KEM G4 sweep v1\x00"
                + master_seed
                + name.encode("ascii")
                + seed_index.to_bytes(4, "big")
            ).digest()
            public, reference = generate_coupled_phase_instance(params, seed)
            recovery = recover_coupled_phases(public, reference=reference)
            ok = (
                recovery.gf2_rank == params.gadget_count - 1
                and recovery.gf2_nullity == 1
                and recovery.phase_solutions == 2
                and recovery.accepted_solutions == 2
                and recovery.nonreference_accepted_solutions == 1
            )
            all_ok = all_ok and ok
            print(
                f"{name},{seed_index},{recovery.gadget_count},{recovery.total_tetrahedra},"
                f"{recovery.coupling_edges},{recovery.coupling_cycle_rank},"
                f"{recovery.gadget_matching_nodes},{recovery.gadget_matching_backtracks},"
                f"{recovery.xor_equations},{recovery.xor_variables},{recovery.gf2_rank},"
                f"{recovery.gf2_nullity},{recovery.gf2_row_xors},"
                f"{recovery.propagation_tree_assignments},{recovery.propagation_constraint_checks},"
                f"{recovery.phase_solutions},{recovery.accepted_solutions},"
                f"{recovery.nonreference_accepted_solutions}"
            )

    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
