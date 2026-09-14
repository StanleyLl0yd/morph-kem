from __future__ import annotations

import argparse
import hashlib

from morph_kem.bpt_pachner import BPT_WEAK_PARAMETER_SETS, generate_bpt_weak_instance, recover_bpt_weak


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 32:
        raise SystemExit("seed count outside toy bounds")
    print("set,seed,depth,bound,recovered,accepted,matches_planted,source_paths,target_paths,multiplicity,vertex_scans,legal_seen,retries")
    for name in sorted(BPT_WEAK_PARAMETER_SETS):
        params = BPT_WEAK_PARAMETER_SETS[name]
        for index in range(args.seeds):
            seed = hashlib.sha256(f"MORPH-KEM BPT-W0 sweep {name} seed {index} v1".encode()).digest()
            public, reference = generate_bpt_weak_instance(params, seed)
            result = recover_bpt_weak(public, reference=reference)
            print(
                f"{name},{index},{params.stack_depth},{public.move_bound},{result.recovered_length},"
                f"{int(result.accepted)},{int(bool(result.matches_planted_after_public_success))},"
                f"{result.source_simplification_paths},{result.target_simplification_paths},"
                f"{result.accepted_path_multiplicity_lower_bound},"
                f"{result.source_vertex_scans + result.target_vertex_scans},"
                f"{result.source_legal_moves_seen + result.target_legal_moves_seen},"
                f"{reference.target_generation_retries}"
            )


if __name__ == "__main__":
    main()
