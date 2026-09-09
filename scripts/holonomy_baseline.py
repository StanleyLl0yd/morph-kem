#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time

from morph_kem.holonomy import (
    HOLONOMY_PARAMETER_SETS,
    generate_s3_instance,
    generate_z2_instance,
    recover_s3_abelianization,
    recover_s3_via_abelianization,
    recover_z2_spanning_tree,
    solve_s3_csp,
    validate_s3_frames,
    validate_z2_frames,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the MORPH H1 signed-holonomy baseline.")
    parser.add_argument("--params", choices=sorted(HOLONOMY_PARAMETER_SETS), default="h1-12")
    parser.add_argument("--solution-cap", type=int, default=64)
    parser.add_argument(
        "--master-seed",
        default="16180339887498948482045868343656",
        help="hex-encoded deterministic H1 generation seed",
    )
    args = parser.parse_args()

    params = HOLONOMY_PARAMETER_SETS[args.params]
    master_seed = bytes.fromhex(args.master_seed)

    z2, z2_reference = generate_z2_instance(params, master_seed)
    z2_recovery = recover_z2_spanning_tree(z2)

    s3, s3_reference = generate_s3_instance(params, master_seed)
    leak = recover_s3_abelianization(s3)
    direct = recover_s3_via_abelianization(s3)

    started = time.perf_counter()
    csp = solve_s3_csp(s3, solution_cap=args.solution_cap)
    elapsed = time.perf_counter() - started

    print(f"parameters: {params.name}")
    print(f"vertices/edges/cycle-rank: {s3.graph.vertices}/{len(s3.graph.edges)}/{s3.graph.cycle_rank}")
    print(f"degree histogram: {s3.graph.degree_histogram()}")
    print(f"Z2 reference accepted: {validate_z2_frames(z2, z2_reference.frames)}")
    print(f"Z2 tree recovery accepted: {z2_recovery.accepted}")
    print(f"Z2 edge checks: {z2_recovery.edge_checks}")
    print(f"S3 reference accepted: {validate_s3_frames(s3, s3_reference.frames).accepted}")
    print(f"S3 abelianization consistent: {leak.consistent}")
    print(f"S3 parity vertices recovered: {leak.recovered_vertices}")
    print(f"S3 direct abelianization recovery accepted: {direct.accepted}")
    print(f"S3 direct recovery edge checks: {direct.edge_checks}")
    print(f"S3 CSP accepted: {csp.accepted}")
    print(f"S3 CSP solutions found: {csp.solutions_found}")
    print(f"S3 CSP nodes/backtracks: {csp.nodes}/{csp.backtracks}")
    print(f"S3 post-abelianization mean domain: {csp.parity_pruned_domain_mean:.2f}")
    print(f"S3 hit solution cap: {csp.hit_solution_cap}")
    print(f"S3 CSP elapsed seconds: {elapsed:.6f}")
    return 0 if z2_recovery.accepted and direct.accepted and csp.accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
