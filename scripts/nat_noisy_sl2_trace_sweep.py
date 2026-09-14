from __future__ import annotations

import argparse
import hashlib
from collections import defaultdict

from morph_kem.nat_noisy_sl2_trace import (
    NAT10_PARAMETER_SETS,
    generate_nat10_instance,
    recover_nat10,
)


def seed_for(name: str, index: int) -> bytes:
    return hashlib.sha256(
        f"MORPH-KEM NAT10 sweep {name} seed {index} v1".encode("ascii")
    ).digest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 32:
        raise SystemExit("--seeds must be in 1..32")

    print(
        "set,seed,gen_attempts,accepted,planted_match,candidate_sizes,left_considered,left_retained,"
        "right_considered,right_retained,join_candidates,verifier_tests,accepted_representations,orbit_lower_bound"
    )
    summary: dict[str, list[int]] = defaultdict(lambda: [0, 0, 0, 0, 0, 0, 0, 0, 0])
    for params in NAT10_PARAMETER_SETS.values():
        for index in range(args.seeds):
            public, reference = generate_nat10_instance(params, seed_for(params.name, index))
            recovery = recover_nat10(public, reference=reference)
            print(
                f"{params.name},{index},{reference.generation_attempts},{int(recovery.accepted)},"
                f"{int(bool(recovery.recovered_matches_planted_after_public_success))},"
                f"{'/'.join(str(value) for value in recovery.generator_candidate_sizes)},"
                f"{recovery.left_pairs_considered},{recovery.left_pairs_retained},"
                f"{recovery.right_pairs_considered},{recovery.right_pairs_retained},"
                f"{recovery.relator_join_candidates},{recovery.verifier_candidates_tested},"
                f"{recovery.accepted_representations},{recovery.conjugacy_orbit_lower_bound}"
            )
            row = summary[params.name]
            row[0] += int(recovery.accepted)
            row[1] += int(bool(recovery.recovered_matches_planted_after_public_success))
            row[2] += recovery.accepted_representations
            row[3] = recovery.accepted_representations if row[3] == 0 else min(row[3], recovery.accepted_representations)
            row[4] = max(row[4], recovery.accepted_representations)
            row[5] = recovery.conjugacy_orbit_lower_bound if row[5] == 0 else min(row[5], recovery.conjugacy_orbit_lower_bound)
            row[6] = max(row[6], recovery.conjugacy_orbit_lower_bound)
            row[7] = max(row[7], recovery.relator_join_candidates)
            row[8] = max(row[8], recovery.verifier_candidates_tested)

    print(
        "summary,set,accepted,planted_match,accepted_rep_sum,accepted_rep_min,accepted_rep_max,"
        "orbit_lb_min,orbit_lb_max,max_joins,max_verifier_tests,cases"
    )
    for name, row in sorted(summary.items()):
        print(
            f"summary,{name},{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},"
            f"{row[5]},{row[6]},{row[7]},{row[8]},{args.seeds}"
        )


if __name__ == "__main__":
    main()
