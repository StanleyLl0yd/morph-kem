#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time

from morph_kem.higher_atlas import (
    HIGHER_ATLAS_PARAMETER_SETS,
    chart_role_signature_audit,
    generate_higher_atlas,
    pairwise_compatibility_audit,
    solve_higher_atlas_repair,
    validate_higher_atlas_witness,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the MORPH H2-E2 higher-order Escher baseline.")
    parser.add_argument("--params", choices=sorted(HIGHER_ATLAS_PARAMETER_SETS), default="atlas-12")
    parser.add_argument("--max-nodes", type=int, default=2_000_000)
    parser.add_argument(
        "--master-seed",
        default="17320508075688772935274463415059",
        help="hex-encoded deterministic H2-E2 generation seed",
    )
    args = parser.parse_args()

    public, reference = generate_higher_atlas(
        HIGHER_ATLAS_PARAMETER_SETS[args.params],
        bytes.fromhex(args.master_seed),
    )
    pairwise = pairwise_compatibility_audit(public)
    role = chart_role_signature_audit(public, reference)

    started = time.perf_counter()
    repair = solve_higher_atlas_repair(public, max_nodes=args.max_nodes)
    elapsed = time.perf_counter() - started

    reference_valid = validate_higher_atlas_witness(
        public,
        reference.planted_seams,
        reference.assignment,
    ).accepted
    attack_valid = (
        repair.found
        and validate_higher_atlas_witness(
            public,
            repair.seams,
            repair.assignment,
        ).accepted
    )

    print(f"parameters: {args.params}")
    print(f"variables/charts/budget: {public.parameters.variables}/{public.parameters.charts}/{public.parameters.seam_budget}")
    print(f"pairwise chart compatibility: {pairwise.compatible_pairs}/{pairwise.chart_pairs}")
    print(f"reference valid: {reference_valid}")
    print(f"attack found: {repair.found}")
    print(f"attack valid: {attack_valid}")
    print(f"minimum seams: {repair.minimum_seams}")
    print(f"nodes/backtracks/best-updates: {repair.nodes}/{repair.backtracks}/{repair.best_updates}")
    print(f"proven minimum: {repair.proven_minimum}")
    print(f"node cap exhausted: {repair.exhausted_node_cap}")
    print(f"planted seam signatures seen among normal charts: {role.seam_signatures_seen_in_normal}/{role.planted_seams}")
    print(f"unique simple seam signatures: {role.unique_seam_signatures}")
    print(f"elapsed seconds: {elapsed:.6f}")
    return 0 if reference_valid and attack_valid and pairwise.all_compatible else 1


if __name__ == "__main__":
    raise SystemExit(main())
