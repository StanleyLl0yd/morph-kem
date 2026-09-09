#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time

from morph_kem.hyperbolic import (
    audit_a5,
    generate_a5_instance,
    generate_klein_quartic,
    solve_a5_csp,
    validate_a5_frames,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the MORPH H2 Klein-quartic/A5 baseline.")
    parser.add_argument("--solution-cap", type=int, default=8)
    parser.add_argument("--max-nodes", type=int, default=2_000_000)
    parser.add_argument(
        "--master-seed",
        default="26457513110645905905016157536392",
        help="hex-encoded deterministic H2 generation seed",
    )
    args = parser.parse_args()

    klein = generate_klein_quartic()
    audit = audit_a5()
    public, reference = generate_a5_instance(bytes.fromhex(args.master_seed))

    started = time.perf_counter()
    result = solve_a5_csp(public, solution_cap=args.solution_cap, max_nodes=args.max_nodes)
    elapsed = time.perf_counter() - started

    print(f"Klein V/E/F: {len(klein.vertices)}/{len(klein.edges)}/{len(klein.faces)}")
    print(f"Klein degree set: {sorted(set(klein.vertex_degrees))}")
    print(f"Klein edge-face degree set: {sorted(set(klein.edge_face_degrees))}")
    print(f"Klein Euler/genus: {klein.euler_characteristic}/{klein.genus}")
    print(f"Klein free collapse pairs: {len(klein.complex.free_collapse_pairs())}")
    print(f"rotation group order: {klein.group_order}")
    print(f"triangle generator orders: {klein.r_order}/{klein.s_order}/{klein.t_order}")
    print(f"A5 order/class-size/class-order: {audit.order}/{audit.conjugacy_class_size}/{audit.conjugacy_class_order}")
    print(f"A5 commutator/generated-by-class size: {audit.commutator_subgroup_size}/{audit.generated_by_class_size}")
    print(f"reference accepted: {validate_a5_frames(public, reference.frames).accepted}")
    print(f"CSP accepted: {result.accepted}")
    print(f"CSP solutions found: {result.solutions_found}")
    print(f"CSP nodes/backtracks: {result.nodes}/{result.backtracks}")
    print(f"CSP arc revisions: {result.arc_revisions}")
    print(f"CSP hit solution cap: {result.hit_solution_cap}")
    print(f"CSP node cap reached without witness: {not result.accepted and result.nodes >= args.max_nodes}")
    print(f"CSP elapsed seconds: {elapsed:.6f}")
    return 0 if validate_a5_frames(public, reference.frames).accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
