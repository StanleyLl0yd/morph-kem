from __future__ import annotations

from morph_kem.gluing_coupled import G4_PARAMETER_SETS, generate_coupled_phase_instance
from morph_kem.gluing_exact_one import G5_PARAMETER_SETS, generate_exact_one_instance
from morph_kem.gluing_phase_csp import (
    compile_g4,
    compile_g5,
    compile_g6,
    compile_g7,
    semantic_equivalence_audit,
)
from morph_kem.gluing_residual import G6_PARAMETER_SETS, generate_residual_exact_one_instance
from morph_kem.gluing_sat import G7_PARAMETER_SETS, generate_sat_phase_instance


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


def main() -> int:
    g4_public, _ = generate_coupled_phase_instance(G4_PARAMETER_SETS["g4-4"], MASTER_SEED)
    g5_public, _ = generate_exact_one_instance(G5_PARAMETER_SETS["g5-12"], MASTER_SEED)
    g6_public, _ = generate_residual_exact_one_instance(G6_PARAMETER_SETS["g6-12"], MASTER_SEED)
    g7_public, _ = generate_sat_phase_instance(G7_PARAMETER_SETS["g7-12"], MASTER_SEED)
    cases = (
        ("G4", g4_public, compile_g4(g4_public)),
        ("G5", g5_public, compile_g5(g5_public)),
        ("G6", g6_public, compile_g6(g6_public)),
        ("G7", g7_public, compile_g7(g7_public)),
    )

    success = True
    for family, public, compiled in cases:
        audit = semantic_equivalence_audit(family, public, compiled)
        print(
            f"{family}: checked={audit.assignments_checked} "
            f"compiled_accepts={audit.compiled_accepts} "
            f"original_accepts={audit.original_accepts} mismatches={audit.mismatches}"
        )
        success &= audit.mismatches == 0 and audit.compiled_accepts == audit.original_accepts
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
