#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time

from morph_kem.morse import (
    MORSE_PARAMETER_SETS,
    collapse_to_graph_witness,
    collapse_witness_survey,
    generate_morse_instance,
    greedy_matching_survey,
    verify_planted_witness,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the MORPH-KEM M3 equivalent-witness baseline.")
    parser.add_argument("--params", choices=sorted(MORSE_PARAMETER_SETS), default="morse-6")
    parser.add_argument("--collapse-trials", type=int, default=32)
    parser.add_argument("--greedy-trials", type=int, default=8)
    parser.add_argument(
        "--master-seed",
        default="27182818284590452353602874713526",
        help="hex-encoded deterministic M3 instance-generation seed",
    )
    args = parser.parse_args()

    public, trapdoor = generate_morse_instance(
        MORSE_PARAMETER_SETS[args.params],
        bytes.fromhex(args.master_seed),
    )
    planted = verify_planted_witness(public, trapdoor)

    started = time.perf_counter()
    lex = collapse_to_graph_witness(public, strategy="lex")
    reverse = collapse_to_graph_witness(public, strategy="reverse")
    survey = collapse_witness_survey(
        public,
        trials=args.collapse_trials,
        attack_seed=b"M3-baseline-collapse",
    )
    greedy = greedy_matching_survey(
        public,
        trials=args.greedy_trials,
        attack_seed=b"M3-baseline-greedy",
    )
    elapsed = time.perf_counter() - started

    print(f"parameters: {args.params}")
    print(f"target simplices: {len(public.target.simplices)}")
    print(f"critical target: {public.critical_target}")
    print(f"planted witness pairs: {len(trapdoor.planted_matching)}")
    print(f"planted accepted: {planted.valid}")
    print(f"lex collapse: reached_graph={lex.reached_graph} accepted={lex.accepted} triangle_collapses={lex.triangle_collapses}")
    print(f"reverse collapse: reached_graph={reverse.reached_graph} accepted={reverse.accepted} triangle_collapses={reverse.triangle_collapses}")
    print(f"initial/max triangle choices: {lex.initial_triangle_choices}/{lex.max_triangle_choices}")
    print(f"random collapse survey: trials={survey.trials} reached_graph={survey.reached_graph} accepted={survey.accepted} unique_residuals={survey.unique_residuals}")
    print(f"random mean triangle collapses: {survey.mean_triangle_collapses:.2f}")
    print(f"generic greedy matching: trials={greedy.trials} target_hits={greedy.target_hits} unique_vectors={greedy.unique_critical_vectors} best_total_critical={greedy.best_total_critical}")
    print(f"elapsed seconds: {elapsed:.6f}")
    return 0 if planted.valid and lex.accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
