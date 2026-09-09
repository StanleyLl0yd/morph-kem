#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time

from morph_kem.hyperbolic import (
    audit_a5,
    generate_a5_instance,
    generate_klein_quartic,
    recover_a5_belief_propagation,
    recover_a5_breakout,
    recover_a5_min_conflicts,
    recover_a5_neighborhood_repair,
    recover_a5_pair_repair,
    recover_a5_spectral,
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

    spectral_started = time.perf_counter()
    spectral = recover_a5_spectral(
        public,
        iterations=80,
    )
    spectral_elapsed = time.perf_counter() - spectral_started

    bp_started = time.perf_counter()
    belief = recover_a5_belief_propagation(
        public,
        iterations=60,
        damping=0.35,
    )
    bp_elapsed = time.perf_counter() - bp_started

    initializer = (
        belief.frames
        if belief.violations <= spectral.violations
        else spectral.frames
    )

    local_started = time.perf_counter()
    local = recover_a5_min_conflicts(
        public,
        restarts=8,
        max_sweeps=80,
        attack_seed=b"H2-fixed-baseline",
        initial_frames=initializer,
    )
    local_elapsed = time.perf_counter() - local_started

    breakout_started = time.perf_counter()
    breakout = recover_a5_breakout(
        public,
        local.frames,
        max_sweeps=400,
        attack_seed=b"H2-fixed-breakout",
    )
    breakout_elapsed = time.perf_counter() - breakout_started

    pair_seed = (
        breakout.frames
        if breakout.best_violations <= local.best_violations
        else local.frames
    )

    pair_started = time.perf_counter()
    pair = (
        recover_a5_pair_repair(
            public,
            pair_seed,
            max_iterations=8,
        )
        if pair_seed is not None
        else None
    )
    pair_elapsed = time.perf_counter() - pair_started

    preferred = (
        pair.frames
        if pair is not None and pair.best_violations <= breakout.best_violations
        else breakout.frames
    )

    neighborhood_started = time.perf_counter()
    neighborhood = recover_a5_neighborhood_repair(
        public,
        preferred,
        max_radius=2,
        max_nodes_per_radius=5_000,
    )
    neighborhood_elapsed = time.perf_counter() - neighborhood_started

    if neighborhood.accepted and neighborhood.frames is not None:
        preferred = neighborhood.frames

    started = time.perf_counter()
    result = solve_a5_csp(
        public,
        solution_cap=args.solution_cap,
        max_nodes=args.max_nodes,
        preferred_frames=preferred,
    )
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
    print(f"spectral violations: {spectral.violations}")
    print(f"spectral rounding error: {spectral.rounding_error:.6f}")
    print(f"spectral elapsed seconds: {spectral_elapsed:.6f}")
    print(f"belief-propagation violations: {belief.violations}")
    print(f"belief-propagation mean confidence gap: {belief.mean_confidence_gap:.8f}")
    print(f"belief-propagation elapsed seconds: {bp_elapsed:.6f}")
    print(f"local-search accepted: {local.accepted}")
    print(f"local-search restarts/sweeps/moves: {local.restarts_used}/{local.sweeps_used}/{local.moves}")
    print(f"local-search best violations: {local.best_violations}")
    print(f"local-search elapsed seconds: {local_elapsed:.6f}")
    print(f"breakout accepted: {breakout.accepted}")
    print(f"breakout sweeps/moves/weight-updates: {breakout.sweeps}/{breakout.moves}/{breakout.weight_updates}")
    print(f"breakout best violations/max-edge-weight: {breakout.best_violations}/{breakout.max_edge_weight}")
    print(f"breakout elapsed seconds: {breakout_elapsed:.6f}")
    print(f"pair-repair accepted: {pair.accepted if pair is not None else False}")
    print(f"pair-repair iterations/tests: {pair.iterations if pair is not None else 0}/{pair.pair_assignments_tested if pair is not None else 0}")
    print(f"pair-repair best violations: {pair.best_violations if pair is not None else local.best_violations}")
    print(f"pair-repair elapsed seconds: {pair_elapsed:.6f}")
    print(f"neighborhood-repair accepted: {neighborhood.accepted}")
    print(f"neighborhood-repair radius/mutable: {neighborhood.radius_used}/{neighborhood.mutable_vertices}")
    print(f"neighborhood-repair nodes/backtracks/arcs: {neighborhood.nodes}/{neighborhood.backtracks}/{neighborhood.arc_revisions}")
    print(f"neighborhood-repair elapsed seconds: {neighborhood_elapsed:.6f}")
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
