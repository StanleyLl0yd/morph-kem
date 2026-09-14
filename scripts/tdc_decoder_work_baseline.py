from __future__ import annotations

import argparse
import hashlib

from morph_kem.tdc_decoder_work import (
    TDC3_PARAMETER_SETS,
    generate_tdc3_instance,
    recover_tdc3_weight,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(TDC3_PARAMETER_SETS), default="tdc3-n10")
    args = parser.parse_args()
    params = TDC3_PARAMETER_SETS[args.params]
    seed = hashlib.sha256(
        f"MORPH-KEM TDC3 fixed baseline {params.name} v1".encode("ascii")
    ).digest()
    instance = generate_tdc3_instance(params, seed)

    print(f"parameters: {params.name}")
    print(f"public rows/columns: {instance.pair.topology.row_count}/{len(instance.pair.topology.columns)}")
    print(f"declared weights: {params.error_weights}")
    for weight in params.error_weights:
        result = recover_tdc3_weight(instance, weight)
        print(
            "weight={w} top_bitflip={tba} top_bf_iter={tbi} top_bf_eval={tbe} "
            "rnd_bitflip={rba} rnd_bf_iter={rbi} rnd_bf_eval={rbe} "
            "top_exact={tea} top_exact_w={tew} top_pairs={tep} top_collisions={tec} top_match={tem} "
            "rnd_exact={rea} rnd_exact_w={rew} rnd_pairs={rep} rnd_collisions={rec} rnd_match={rem}".format(
                w=weight,
                tba=result.topology_bitflip.accepted,
                tbi=result.topology_bitflip.iterations,
                tbe=result.topology_bitflip.score_evaluations,
                rba=result.random_bitflip.accepted,
                rbi=result.random_bitflip.iterations,
                rbe=result.random_bitflip.score_evaluations,
                tea=result.topology_exact.accepted,
                tew=result.topology_exact.recovered_weight,
                tep=result.topology_exact.candidate_pairs_tested,
                tec=result.topology_exact.syndrome_bucket_collisions,
                tem=result.topology_exact_matches_planted_after_public_success,
                rea=result.random_exact.accepted,
                rew=result.random_exact.recovered_weight,
                rep=result.random_exact.candidate_pairs_tested,
                rec=result.random_exact.syndrome_bucket_collisions,
                rem=result.random_exact_matches_planted_after_public_success,
            )
        )


if __name__ == "__main__":
    main()
