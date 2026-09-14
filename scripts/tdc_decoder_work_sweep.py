from __future__ import annotations

import argparse
import hashlib

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


if __name__ == "__main__":
    main()
