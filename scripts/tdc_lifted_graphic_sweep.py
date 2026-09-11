from __future__ import annotations

import argparse

from morph_kem.tdc_lifted_graphic import (
    TDC1_PARAMETER_SETS,
    decode_graphic_error,
    generate_tdc1_instance,
    graphic_code_metrics,
    planted_error_mask,
    recover_k4_quotient,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 32:
        raise SystemExit("seed count outside toy bounds")

    print("set,seed,L,lift_girth,random_girth,lift_triangles,random_triangles,lift_four,random_four,quotient_found,quotient_nodes,quotient_backtracks,weight,syndrome,dp_states,pair_tests,recovered_weight,accepted,matches_planted")
    for name in sorted(TDC1_PARAMETER_SETS):
        params = TDC1_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            seed = (f"MORPH-KEM TDC1 sweep {name} seed {seed_index:02d} v1").encode().ljust(48, b".")
            instance = generate_tdc1_instance(params, seed)
            lifted = graphic_code_metrics(instance.lifted)
            random_control = graphic_code_metrics(instance.matched_random)
            quotient = recover_k4_quotient(instance.lifted, params.lift_factor)
            for weight in params.error_weights:
                error = planted_error_mask(instance.lifted, weight, seed + weight.to_bytes(2, "big"))
                recovered = decode_graphic_error(instance.lifted, error)
                print(
                    f"{name},{seed_index},{params.lift_factor},{lifted.girth},{random_control.girth},"
                    f"{lifted.triangle_count},{random_control.triangle_count},{lifted.four_cycle_count},{random_control.four_cycle_count},"
                    f"{int(quotient.found)},{quotient.search_nodes},{quotient.backtracks},{weight},{recovered.syndrome_weight},"
                    f"{recovered.matching_dp_states},{recovered.matching_pair_tests},{recovered.recovered_error_weight},"
                    f"{int(recovered.accepted)},{int(recovered.matches_planted_error_after_public_success)}"
                )


if __name__ == "__main__":
    main()
