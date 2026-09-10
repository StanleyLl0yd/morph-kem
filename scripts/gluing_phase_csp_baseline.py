from __future__ import annotations

from collections import Counter

from morph_kem.gluing_coupled import G4_PARAMETER_SETS, generate_coupled_phase_instance
from morph_kem.gluing_exact_one import G5_PARAMETER_SETS, generate_exact_one_instance
from morph_kem.gluing_phase_csp import (
    compile_g4,
    compile_g5,
    compile_g6,
    compile_g7,
    lift_assignment,
    original_accepts,
    serialize_compiled_csp,
    solve_compiled_csp,
)
from morph_kem.gluing_residual import G6_PARAMETER_SETS, generate_residual_exact_one_instance
from morph_kem.gluing_sat import G7_PARAMETER_SETS, generate_sat_phase_instance


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


def cases():
    g4_public, g4_reference = generate_coupled_phase_instance(
        G4_PARAMETER_SETS["g4-12"], MASTER_SEED
    )
    g5_public, g5_reference = generate_exact_one_instance(
        G5_PARAMETER_SETS["g5-24"], MASTER_SEED
    )
    g6_public, g6_reference = generate_residual_exact_one_instance(
        G6_PARAMETER_SETS["g6-24"], MASTER_SEED
    )
    g7_public, g7_reference = generate_sat_phase_instance(
        G7_PARAMETER_SETS["g7-24"], MASTER_SEED
    )
    return (
        ("G4", g4_public, g4_reference, compile_g4(g4_public)),
        ("G5", g5_public, g5_reference, compile_g5(g5_public)),
        ("G6", g6_public, g6_reference, compile_g6(g6_public)),
        ("G7", g7_public, g7_reference, compile_g7(g7_public)),
    )


def main() -> int:
    success = True
    for family, public, reference, compiled in cases():
        recovery = solve_compiled_csp(compiled.csp, solution_cap=16)
        relation_histogram = tuple(
            sorted(Counter((len(r.scope), len(r.allowed)) for r in compiled.csp.constraints).items())
        )
        accepted = 0
        nonreference = 0
        for assignment in recovery.assignments:
            groups = lift_assignment(compiled.lift, assignment)
            if original_accepts(family, public, groups):
                accepted += 1
                nonreference += int(assignment != reference.phases)

        serialized = serialize_compiled_csp(compiled.csp)
        topology_tokens = any(
            token in serialized.lower()
            for token in ("tetra", "face", "vertex", "simplic", "group")
        )
        print(f"[{family}]")
        print(f"CSP variables: {len(compiled.csp.domain_sizes)}")
        print(f"domain sizes: {compiled.csp.domain_sizes}")
        print(f"constraints: {len(compiled.csp.constraints)}")
        print(f"relation histogram ((arity,allowed),count): {relation_histogram}")
        print(f"topological tetrahedra before compile: {compiled.lift.topological_tetrahedra}")
        print(f"phase extraction nodes/backtracks: {compiled.lift.extraction_nodes}/{compiled.lift.extraction_backtracks}")
        print(f"serialized CSP bytes: {len(serialized.encode('utf-8'))}")
        print(f"serialized topology tokens present: {topology_tokens}")
        print(f"generic solutions/cap: {recovery.solution_count}/{recovery.solution_cap}")
        print(f"generic cap hit: {recovery.solution_cap_hit}")
        print(f"generic nodes/decisions: {recovery.nodes}/{recovery.decisions}")
        print(f"generic prunes/conflicts/backtracks: {recovery.value_prunes}/{recovery.conflicts}/{recovery.backtracks}")
        print(f"lifted exact-verifier accepted: {accepted}")
        print(f"accepted non-reference: {nonreference}")
        print()
        success &= accepted == recovery.solution_count and accepted > 0 and not topology_tokens

    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
