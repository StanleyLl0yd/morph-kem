#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time

from morph_kem.escher import (
    ESCHER_PARAMETER_SETS,
    fundamental_cycle_syndrome,
    generate_escher_instance,
    solve_escher_repair,
    validate_escher_witness,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the MORPH H2-E Escher-atlas baseline.")
    parser.add_argument("--params", choices=sorted(ESCHER_PARAMETER_SETS), default="escher-12")
    parser.add_argument("--max-nodes", type=int, default=1_000_000)
    parser.add_argument(
        "--master-seed",
        default="14142135623730950488016887242097",
        help="hex-encoded deterministic H2-E generation seed",
    )
    args = parser.parse_args()

    public, reference = generate_escher_instance(
        ESCHER_PARAMETER_SETS[args.params],
        bytes.fromhex(args.master_seed),
    )
    syndrome = fundamental_cycle_syndrome(public)

    started = time.perf_counter()
    repair = solve_escher_repair(public, max_nodes=args.max_nodes)
    elapsed = time.perf_counter() - started

    planted_valid = validate_escher_witness(
        public,
        reference.planted_seams,
        reference.heights,
    ).accepted
    attack_valid = (
        repair.found
        and validate_escher_witness(public, repair.seams, repair.heights).accepted
    )

    print(f"parameters: {args.params}")
    print(f"vertices/edges/cycle-rank: {public.graph.vertices}/{len(public.graph.edges)}/{public.graph.cycle_rank}")
    print(f"degree histogram: {public.graph.degree_histogram()}")
    print(f"modulus: {public.parameters.modulus}")
    print(f"planted seam budget: {public.parameters.seam_budget}")
    print(f"planted witness valid: {planted_valid}")
    print(f"fundamental cycle syndromes nonzero: {syndrome.nonzero}/{len(syndrome.values)}")
    print(f"attack found repair: {repair.found}")
    print(f"attack witness valid: {attack_valid}")
    print(f"minimum seams found: {repair.minimum_seams}")
    print(f"attack nodes/backtracks/max-branch: {repair.nodes}/{repair.backtracks}/{repair.max_branch}")
    print(f"attack edge checks: {repair.edge_checks}")
    print(f"attack exhausted search: {repair.exhausted}")
    print(f"elapsed seconds: {elapsed:.6f}")
    return 0 if planted_valid and attack_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
