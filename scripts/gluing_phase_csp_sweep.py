from __future__ import annotations

import argparse
import hashlib

from morph_kem.gluing_coupled import G4_PARAMETER_SETS, generate_coupled_phase_instance
from morph_kem.gluing_exact_one import G5_PARAMETER_SETS, generate_exact_one_instance
from morph_kem.gluing_phase_csp import (
    compile_g4,
    compile_g5,
    compile_g6,
    compile_g7,
    lift_assignment,
    original_accepts,
    solve_compiled_csp,
)
from morph_kem.gluing_residual import G6_PARAMETER_SETS, generate_residual_exact_one_instance
from morph_kem.gluing_sat import G7_PARAMETER_SETS, generate_sat_phase_instance


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


def derived_seed(index: int) -> bytes:
    return hashlib.sha256(
        b"MORPH-KEM G8 phase-CSP sweep v1\x00"
        + MASTER_SEED
        + index.to_bytes(4, "big")
    ).digest()


def cases(seed: bytes):
    g4_public, g4_reference = generate_coupled_phase_instance(G4_PARAMETER_SETS["g4-12"], seed)
    g5_public, g5_reference = generate_exact_one_instance(G5_PARAMETER_SETS["g5-24"], seed)
    g6_public, g6_reference = generate_residual_exact_one_instance(G6_PARAMETER_SETS["g6-24"], seed)
    g7_public, g7_reference = generate_sat_phase_instance(G7_PARAMETER_SETS["g7-24"], seed)
    return (
        ("G4", g4_public, g4_reference, compile_g4(g4_public)),
        ("G5", g5_public, g5_reference, compile_g5(g5_public)),
        ("G6", g6_public, g6_reference, compile_g6(g6_public)),
        ("G7", g7_public, g7_reference, compile_g7(g7_public)),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=4)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 16:
        parser.error("--seeds must be in 1..16")

    print("family,seed,variables,constraints,extract_nodes,extract_backtracks,solutions,cap_hit,nodes,decisions,prunes,conflicts,backtracks,accepted,nonreference")
    all_ok = True
    for seed_index in range(args.seeds):
        seed = derived_seed(seed_index)
        for family, public, reference, compiled in cases(seed):
            recovery = solve_compiled_csp(compiled.csp, solution_cap=16)
            accepted = 0
            nonreference = 0
            for assignment in recovery.assignments:
                groups = lift_assignment(compiled.lift, assignment)
                if original_accepts(family, public, groups):
                    accepted += 1
                    nonreference += int(assignment != reference.phases)
            print(
                f"{family},{seed_index},{len(compiled.csp.domain_sizes)},{len(compiled.csp.constraints)},"
                f"{compiled.lift.extraction_nodes},{compiled.lift.extraction_backtracks},"
                f"{recovery.solution_count},{int(recovery.solution_cap_hit)},"
                f"{recovery.nodes},{recovery.decisions},{recovery.value_prunes},"
                f"{recovery.conflicts},{recovery.backtracks},{accepted},{nonreference}"
            )
            all_ok &= accepted == recovery.solution_count and accepted > 0
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
