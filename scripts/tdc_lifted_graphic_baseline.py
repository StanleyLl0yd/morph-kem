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
    parser.add_argument("--params", choices=sorted(TDC1_PARAMETER_SETS), default="tdc1-L18")
    args = parser.parse_args()
    params = TDC1_PARAMETER_SETS[args.params]
    seed = b"MORPH-KEM TDC1 fixed baseline seed v1"
    instance = generate_tdc1_instance(params, seed)
    lifted = graphic_code_metrics(instance.lifted)
    random_control = graphic_code_metrics(instance.matched_random)

    print(f"parameters: {params.name}")
    print(f"lift factor: {params.lift_factor}")
    print(f"lift generation retries: {instance.lift_generation_retries}")
    print(f"matched-random generation retries: {instance.random_generation_retries}")
    print(f"lift V/E/rank/dimension/rate: {lifted.vertices}/{lifted.edges}/{lifted.parity_rank}/{lifted.code_dimension}/{lifted.rate:.9f}")
    print(f"random V/E/rank/dimension/rate: {random_control.vertices}/{random_control.edges}/{random_control.parity_rank}/{random_control.code_dimension}/{random_control.rate:.9f}")
    print(f"lift girth / triangles / four-cycles: {lifted.girth}/{lifted.triangle_count}/{lifted.four_cycle_count}")
    print(f"random girth / triangles / four-cycles: {random_control.girth}/{random_control.triangle_count}/{random_control.four_cycle_count}")

    # Quotient recovery is a secondary structural diagnostic, not the decoding gate.
    # The naive exact coloring probe grows rapidly by L, so run it only on the
    # calibration sizes where it is an intentionally cheap attack.  L18 remains
    # covered by the independent graphic-code decoder below.
    if params.lift_factor <= 12:
        quotient = recover_k4_quotient(instance.lifted, params.lift_factor)
        print(f"public K4 quotient probe attempted: True")
        print(f"public K4 quotient recovered: {quotient.found}")
        print(f"quotient search nodes / backtracks: {quotient.search_nodes}/{quotient.backtracks}")
        print(f"quotient color-class sizes: {quotient.color_class_sizes}")
    else:
        print("public K4 quotient probe attempted: False")
        print("public K4 quotient recovered: n/a")
        print("quotient search nodes / backtracks: 0/0")
        print("quotient color-class sizes: ()")

    for weight in params.error_weights:
        error = planted_error_mask(instance.lifted, weight, seed + weight.to_bytes(2, "big"))
        recovered = decode_graphic_error(instance.lifted, error)
        print(
            "decode weight={weight} syndrome={syndrome} bfs={bfs} pops={pops} scans={scans} "
            "dp_states={states} pair_tests={tests} distance={distance} recovered_weight={recovered_weight} "
            "accepted={accepted} matches_planted={matches}".format(
                weight=weight,
                syndrome=recovered.syndrome_weight,
                bfs=recovered.bfs_runs,
                pops=recovered.bfs_queue_pops,
                scans=recovered.bfs_edge_scans,
                states=recovered.matching_dp_states,
                tests=recovered.matching_pair_tests,
                distance=recovered.matching_distance,
                recovered_weight=recovered.recovered_error_weight,
                accepted=recovered.accepted,
                matches=recovered.matches_planted_error_after_public_success,
            )
        )


if __name__ == "__main__":
    main()
