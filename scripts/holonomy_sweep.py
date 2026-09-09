#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.holonomy import (
    HOLONOMY_PARAMETER_SETS,
    generate_s3_instance,
    generate_z2_instance,
    recover_s3_via_abelianization,
    recover_z2_spanning_tree,
    solve_s3_csp,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Sweep MORPH H1 direct and CSP attacks.")
    parser.add_argument("--solution-cap", type=int, default=8)
    parser.add_argument(
        "--master-seed",
        default="16180339887498948482045868343656",
    )
    args = parser.parse_args()
    master_seed = bytes.fromhex(args.master_seed)

    print("set,V,E,cycle_rank,z2,direct_s3,direct_checks,csp,csp_nodes,csp_backtracks,csp_solutions")
    ok = True
    for name, params in HOLONOMY_PARAMETER_SETS.items():
        z2, _ = generate_z2_instance(params, master_seed)
        z2_result = recover_z2_spanning_tree(z2)
        s3, _ = generate_s3_instance(params, master_seed)
        direct = recover_s3_via_abelianization(s3)
        csp = solve_s3_csp(s3, solution_cap=args.solution_cap)
        ok &= z2_result.accepted and direct.accepted and csp.accepted
        print(
            f"{name},{s3.graph.vertices},{len(s3.graph.edges)},{s3.graph.cycle_rank},"
            f"{z2_result.accepted},{direct.accepted},{direct.edge_checks},"
            f"{csp.accepted},{csp.nodes},{csp.backtracks},{csp.solutions_found}"
        )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
