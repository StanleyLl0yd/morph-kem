#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib

from morph_kem.hyperbolic import (
    a5_violation_count,
    generate_a5_instance,
    recover_a5_belief_propagation,
    recover_a5_breakout,
    recover_a5_hamming_repair,
    recover_a5_min_conflicts,
    recover_a5_tree_coordinates,
    solve_a5_csp,
    validate_a5_frames,
)

BASE_SEED = bytes.fromhex("26457513110645905905016157536392")


def sweep_seed(index: int) -> bytes:
    if index == 0:
        return BASE_SEED
    return hashlib.sha256(
        b"MORPH-KEM H2 sweep seed v1\x00"
        + BASE_SEED
        + index.to_bytes(4, "big")
    ).digest()[:16]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a small deterministic MORPH H2 generated-instance attack sweep."
    )
    parser.add_argument("--count", type=int, default=4)
    parser.add_argument("--tree-sweeps", type=int, default=40)
    parser.add_argument("--csp-nodes", type=int, default=250)
    args = parser.parse_args()

    if args.count <= 0 or args.count > 64:
        parser.error("count must be in [1, 64]")
    if args.tree_sweeps <= 0:
        parser.error("tree-sweeps must be positive")
    if args.csp_nodes <= 0:
        parser.error("csp-nodes must be positive")

    print(
        "index,reference,bp,local,breakout,tree,hamming,csp,"
        "best_violations,csp_nodes,singleton_removed"
    )

    for index in range(args.count):
        public, reference = generate_a5_instance(sweep_seed(index))
        reference_ok = validate_a5_frames(public, reference.frames).accepted

        belief = recover_a5_belief_propagation(
            public,
            iterations=30,
            damping=0.35,
        )
        local = recover_a5_min_conflicts(
            public,
            restarts=4,
            max_sweeps=40,
            attack_seed=b"H2-sweep-local-" + index.to_bytes(2, "big"),
            initial_frames=belief.frames,
        )
        breakout = recover_a5_breakout(
            public,
            local.frames,
            max_sweeps=200,
            attack_seed=b"H2-sweep-breakout-" + index.to_bytes(2, "big"),
        )
        tree = recover_a5_tree_coordinates(
            public,
            breakout.frames,
            max_sweeps=args.tree_sweeps,
            attack_seed=b"H2-sweep-tree-" + index.to_bytes(2, "big"),
        )

        preferred = (
            tree.frames
            if tree.best_violations <= breakout.best_violations
            else breakout.frames
        )
        hamming = recover_a5_hamming_repair(
            public,
            preferred,
            max_changes=3,
            max_nodes_per_radius=1_000,
        )
        if hamming.accepted and hamming.frames is not None:
            preferred = hamming.frames

        csp = solve_a5_csp(
            public,
            solution_cap=1,
            max_nodes=args.csp_nodes,
            preferred_frames=preferred,
            singleton_passes=1,
            singleton_probe_cap=50,
        )

        observed = [
            belief.violations,
            local.best_violations,
            breakout.best_violations,
            tree.best_violations,
            a5_violation_count(public, preferred),
        ]
        if csp.first_solution is not None:
            observed.append(a5_violation_count(public, csp.first_solution))

        print(
            f"{index},{reference_ok},{belief.violations},"
            f"{local.best_violations},{breakout.best_violations},"
            f"{tree.best_violations},{hamming.accepted},{csp.accepted},"
            f"{min(observed)},{csp.nodes},{csp.singleton_removed}"
        )

        if not reference_ok:
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
