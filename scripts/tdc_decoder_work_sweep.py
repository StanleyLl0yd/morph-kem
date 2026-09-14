from __future__ import annotations

import argparse
import hashlib
from collections import defaultdict

from morph_kem.tdc_decoder_work import (
    TDC3_PARAMETER_SETS,
    generate_tdc3_instance,
    recover_tdc3_weight,
)


def seed_for(name: str, index: int) -> bytes:
    return hashlib.sha256(
        f"MORPH-KEM TDC3 sweep {name} seed {index} v1".encode("ascii")
    ).digest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(TDC3_PARAMETER_SETS), default=None)
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 32:
        raise SystemExit("--seeds must be in 1..32")

    params_list = (
        (TDC3_PARAMETER_SETS[args.params],)
        if args.params is not None
        else tuple(TDC3_PARAMETER_SETS.values())
    )
    print(
        "set,seed,weight,top_bf,top_bf_iter,top_bf_eval,rnd_bf,rnd_bf_iter,rnd_bf_eval,"
        "top_exact_w,top_exact_pairs,top_exact_collisions,top_exact_match,"
        "rnd_exact_w,rnd_exact_pairs,rnd_exact_collisions,rnd_exact_match"
    )
    summary: dict[tuple[str, int], list[int]] = defaultdict(lambda: [0, 0, 0, 0, 0, 0])
    totals: dict[str, list[int]] = defaultdict(lambda: [0, 0, 0, 0, 0])
    for params in params_list:
        for index in range(args.seeds):
            instance = generate_tdc3_instance(params, seed_for(params.name, index))
            for weight in params.error_weights:
                result = recover_tdc3_weight(instance, weight)
                print(
                    f"{params.name},{index},{weight},"
                    f"{int(result.topology_bitflip.accepted)},{result.topology_bitflip.iterations},{result.topology_bitflip.score_evaluations},"
                    f"{int(result.random_bitflip.accepted)},{result.random_bitflip.iterations},{result.random_bitflip.score_evaluations},"
                    f"{result.topology_exact.recovered_weight},{result.topology_exact.candidate_pairs_tested},"
                    f"{result.topology_exact.syndrome_bucket_collisions},{int(result.topology_exact_matches_planted_after_public_success)},"
                    f"{result.random_exact.recovered_weight},{result.random_exact.candidate_pairs_tested},"
                    f"{result.random_exact.syndrome_bucket_collisions},{int(result.random_exact_matches_planted_after_public_success)}"
                )
                row = summary[(params.name, weight)]
                row[0] += int(result.topology_bitflip.accepted)
                row[1] += int(result.random_bitflip.accepted)
                row[2] += int(result.topology_exact.accepted)
                row[3] += int(result.random_exact.accepted)
                row[4] += int(result.topology_exact_matches_planted_after_public_success)
                row[5] += int(result.random_exact_matches_planted_after_public_success)
                total = totals[params.name]
                total[0] += int(result.topology_bitflip.accepted)
                total[1] += int(result.random_bitflip.accepted)
                total[2] += int(result.topology_exact.accepted)
                total[3] += int(result.random_exact.accepted)
                total[4] += 1

    print("summary,set,weight,top_bf,rnd_bf,bf_delta,top_exact,rnd_exact,top_match,rnd_match")
    for (name, weight), row in sorted(summary.items()):
        print(
            f"summary,{name},{weight},{row[0]},{row[1]},{row[0]-row[1]},"
            f"{row[2]},{row[3]},{row[4]},{row[5]}"
        )
    print("total,set,top_bf,rnd_bf,bf_delta,top_exact,rnd_exact,cases")
    for name, row in sorted(totals.items()):
        print(f"total,{name},{row[0]},{row[1]},{row[0]-row[1]},{row[2]},{row[3]},{row[4]}")


if __name__ == "__main__":
    main()
