#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time

from morph_kem.surface import (
    SURFACE_PARAMETER_SETS,
    generate_surface_instance,
    tree_cotree_survey,
    tree_cotree_witness,
)


MASTER_SEED = bytes.fromhex("16180339887498948482045868343656")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the MORPH-KEM M4 tree-cotree scaling sweep.")
    parser.add_argument("--trials", type=int, default=32)
    args = parser.parse_args()

    failed = False
    for name, params in SURFACE_PARAMETER_SETS.items():
        started = time.perf_counter()
        public, _ = generate_surface_instance(params, MASTER_SEED)
        deterministic = tree_cotree_witness(public, attack_seed=b"M4-sweep-" + name.encode("ascii"))
        survey = tree_cotree_survey(
            public,
            trials=args.trials,
            attack_seed=b"M4-sweep-survey-" + name.encode("ascii"),
        )
        elapsed = time.perf_counter() - started
        print(
            f"{name}: simplices={len(public.target.simplices)} free={len(public.target.free_collapse_pairs())} "
            f"accepted={deterministic.validation.valid} random={survey.target_hits}/{survey.trials} "
            f"unique={survey.unique_matchings} critical={deterministic.validation.critical_vector} "
            f"elapsed={elapsed:.6f}s"
        )
        failed |= not deterministic.validation.valid or survey.target_hits != survey.trials

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
