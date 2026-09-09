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
)


MASTER_SEED = bytes.fromhex("27182818284590452353602874713526")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the MORPH-KEM M3 constructive-attack sweep.")
    parser.add_argument("--collapse-trials", type=int, default=32)
    parser.add_argument("--greedy-trials", type=int, default=8)
    args = parser.parse_args()

    failed = False
    for name in sorted(MORSE_PARAMETER_SETS, key=lambda key: MORSE_PARAMETER_SETS[key].expansions):
        started = time.perf_counter()
        public, _ = generate_morse_instance(MORSE_PARAMETER_SETS[name], MASTER_SEED)
        lex = collapse_to_graph_witness(public, strategy="lex")
        reverse = collapse_to_graph_witness(public, strategy="reverse")
        random = collapse_witness_survey(
            public,
            trials=args.collapse_trials,
            attack_seed=b"M3-sweep-collapse-" + name.encode("ascii"),
        )
        greedy = greedy_matching_survey(
            public,
            trials=args.greedy_trials,
            attack_seed=b"M3-sweep-greedy-" + name.encode("ascii"),
        )
        elapsed = time.perf_counter() - started
        print(
            f"{name}: target={public.critical_target} simplices={len(public.target.simplices)} "
            f"lex={lex.accepted} reverse={reverse.accepted} "
            f"random={random.accepted}/{random.trials} residuals={random.unique_residuals} "
            f"greedy={greedy.target_hits}/{greedy.trials} "
            f"best_critical={greedy.best_total_critical} elapsed={elapsed:.6f}s"
        )
        if not lex.accepted or not reverse.accepted or random.accepted == 0:
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
