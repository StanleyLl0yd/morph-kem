#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time

from morph_kem.surface import (
    SURFACE_PARAMETER_SETS,
    generate_surface_instance,
    surface_greedy_matching_survey,
    surface_incidence,
    tree_cotree_survey,
    tree_cotree_witness,
    verify_surface_trapdoor,
)


MASTER_SEED = bytes.fromhex("16180339887498948482045868343656")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the MORPH-KEM M4 torus/tree-cotree baseline.")
    parser.add_argument("--params", choices=sorted(SURFACE_PARAMETER_SETS), default="torus-4x4")
    parser.add_argument("--tree-trials", type=int, default=16)
    parser.add_argument("--greedy-trials", type=int, default=4)
    args = parser.parse_args()

    public, trapdoor = generate_surface_instance(
        SURFACE_PARAMETER_SETS[args.params],
        MASTER_SEED,
    )
    incidence = surface_incidence(public)
    planted = verify_surface_trapdoor(public, trapdoor)

    started = time.perf_counter()
    attack = tree_cotree_witness(public, attack_seed=b"M4-baseline-attack")
    survey = tree_cotree_survey(
        public,
        trials=args.tree_trials,
        attack_seed=b"M4-baseline-tree-survey",
    )
    greedy = surface_greedy_matching_survey(
        public,
        trials=args.greedy_trials,
        attack_seed=b"M4-baseline-greedy",
    )
    elapsed = time.perf_counter() - started

    print(f"parameters: {args.params}")
    print(f"cells V/E/F: {incidence.vertices}/{incidence.edges}/{incidence.triangles}")
    print(f"edge triangle incidence min/max: {incidence.min_triangles_per_edge}/{incidence.max_triangles_per_edge}")
    print(f"free collapse pairs: {len(public.target.free_collapse_pairs())}")
    print(f"critical target: {public.critical_target}")
    print(f"planted accepted: {planted.valid}")
    print(f"tree-cotree accepted: {attack.validation.valid}")
    print(f"primal/dual tree edges: {attack.primal_tree_edges}/{attack.dual_tree_edges}")
    print(f"critical edges: {attack.critical_edges}")
    print(f"tree-cotree survey: target_hits={survey.target_hits}/{survey.trials} unique_matchings={survey.unique_matchings}")
    print(f"generic greedy: target_hits={greedy.target_hits}/{greedy.trials} best_total_critical={greedy.best_total_critical}")
    print(f"elapsed seconds: {elapsed:.6f}")
    return 0 if planted.valid and attack.validation.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
