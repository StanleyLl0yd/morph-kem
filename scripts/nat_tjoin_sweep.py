from __future__ import annotations

import argparse

from morph_kem.nat_tjoin import NAT1_PARAMETER_SETS, generate_nat1_instance, recover_nat1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 32:
        raise SystemExit("seed count outside toy bounds")

    print("set,seed,weight,V,E,F,syndrome,dp_states,pair_tests,matching_distance,recovered_weight,accepted,matches_noise,matches_hidden")
    for name in sorted(NAT1_PARAMETER_SETS):
        params = NAT1_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            seed = (f"MORPH-KEM NAT1 sweep {name} seed {seed_index:02d} v1").encode().ljust(48, b".")
            for weight in params.noise_weights:
                public, reference = generate_nat1_instance(params, seed, weight)
                result = recover_nat1(public, reference=reference)
                print(
                    f"{name},{seed_index},{weight},{result.vertices},{result.edges},{result.triangles},"
                    f"{result.syndrome_weight},{result.matching_dp_states},{result.matching_pair_tests},"
                    f"{result.matching_distance},{result.recovered_noise_weight},{int(result.accepted)},"
                    f"{int(bool(result.matches_planted_noise_after_public_success))},"
                    f"{int(bool(result.matches_hidden_vertex_after_public_success))}"
                )


if __name__ == "__main__":
    main()
