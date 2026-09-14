from __future__ import annotations

import argparse
import hashlib
from collections import defaultdict

from morph_kem.tdc_decoder_reliability import reliability_guided_decode_leq6
from morph_kem.tdc_decoder_work import (
    TDC3_PARAMETER_SETS,
    generate_tdc3_instance,
    planted_error_mask,
    syndrome,
)


def seed_for(name: str, index: int) -> bytes:
    return hashlib.sha256(
        f"MORPH-KEM TDC3 reliability sweep {name} seed {index} v1".encode("ascii")
    ).digest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(TDC3_PARAMETER_SETS), default=None)
    parser.add_argument("--seeds", type=int, default=8)
    parser.add_argument("--pool-size", type=int, default=24)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 32:
        raise SystemExit("--seeds must be in 1..32")

    params_list = (
        (TDC3_PARAMETER_SETS[args.params],)
        if args.params is not None
        else tuple(TDC3_PARAMETER_SETS.values())
    )
    print(
        "set,seed,weight,top_accept,top_recovered_weight,top_planted_in_pool,top_pairs,top_collisions,"
        "rnd_accept,rnd_recovered_weight,rnd_planted_in_pool,rnd_pairs,rnd_collisions"
    )
    summary: dict[tuple[str, int], list[int]] = defaultdict(lambda: [0, 0, 0, 0, 0])
    totals: dict[str, list[int]] = defaultdict(lambda: [0, 0, 0])
    for params in params_list:
        for index in range(args.seeds):
            instance = generate_tdc3_instance(params, seed_for(params.name, index))
            for weight in params.error_weights:
                planted = planted_error_mask(instance, weight)
                top_target = syndrome(instance.pair.topology, planted)
                rnd_target = syndrome(instance.pair.matched_random, planted)
                top = reliability_guided_decode_leq6(
                    instance.pair.topology, top_target, pool_size=args.pool_size
                )
                rnd = reliability_guided_decode_leq6(
                    instance.pair.matched_random, rnd_target, pool_size=args.pool_size
                )
                top_in_pool = sum(
                    1 for column in top.selected_indices if (planted >> column) & 1
                )
                rnd_in_pool = sum(
                    1 for column in rnd.selected_indices if (planted >> column) & 1
                )
                print(
                    f"{params.name},{index},{weight},"
                    f"{int(top.accepted)},{top.recovered_weight},{top_in_pool},{top.candidate_pairs_tested},{top.syndrome_bucket_collisions},"
                    f"{int(rnd.accepted)},{rnd.recovered_weight},{rnd_in_pool},{rnd.candidate_pairs_tested},{rnd.syndrome_bucket_collisions}"
                )
                row = summary[(params.name, weight)]
                row[0] += int(top.accepted)
                row[1] += int(rnd.accepted)
                row[2] += top_in_pool
                row[3] += rnd_in_pool
                row[4] += 1
                total = totals[params.name]
                total[0] += int(top.accepted)
                total[1] += int(rnd.accepted)
                total[2] += 1

    print("summary,set,weight,top_accept,rnd_accept,delta,top_planted_in_pool,rnd_planted_in_pool,cases")
    for (name, weight), row in sorted(summary.items()):
        print(
            f"summary,{name},{weight},{row[0]},{row[1]},{row[0]-row[1]},"
            f"{row[2]},{row[3]},{row[4]}"
        )
    print("total,set,top_accept,rnd_accept,delta,cases")
    for name, row in sorted(totals.items()):
        print(f"total,{name},{row[0]},{row[1]},{row[0]-row[1]},{row[2]}")


if __name__ == "__main__":
    main()
