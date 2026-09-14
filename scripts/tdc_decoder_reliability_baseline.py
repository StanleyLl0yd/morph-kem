from __future__ import annotations

import argparse
import hashlib

from morph_kem.tdc_decoder_reliability import reliability_guided_decode_leq6
from morph_kem.tdc_decoder_work import (
    TDC3_PARAMETER_SETS,
    generate_tdc3_instance,
    planted_error_mask,
    syndrome,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(TDC3_PARAMETER_SETS), default="tdc3-n10")
    parser.add_argument("--pool-size", type=int, default=24)
    args = parser.parse_args()
    params = TDC3_PARAMETER_SETS[args.params]
    seed = hashlib.sha256(
        f"MORPH-KEM TDC3 reliability fixed {params.name} v1".encode("ascii")
    ).digest()
    instance = generate_tdc3_instance(params, seed)

    print(f"parameters: {params.name}")
    print(f"pool size: {args.pool_size}")
    for weight in params.error_weights:
        planted = planted_error_mask(instance, weight)
        for label, code in (
            ("topology", instance.pair.topology),
            ("random", instance.pair.matched_random),
        ):
            target = syndrome(code, planted)
            recovery = reliability_guided_decode_leq6(
                code, target, pool_size=args.pool_size
            )
            in_pool = sum(
                1
                for index in recovery.selected_indices
                if (planted >> index) & 1
            )
            print(
                f"weight={weight} {label}: accepted={recovery.accepted} "
                f"recovered_weight={recovery.recovered_weight} planted_in_pool={in_pool}/{weight} "
                f"indexed={recovery.subset_masks_indexed} pairs={recovery.candidate_pairs_tested} "
                f"collisions={recovery.syndrome_bucket_collisions}"
            )


if __name__ == "__main__":
    main()
