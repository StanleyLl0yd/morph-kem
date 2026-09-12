from __future__ import annotations

import argparse

from morph_kem.nat_s3 import NAT2_PARAMETER_SETS, generate_nat2_instance, recover_nat2


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 32:
        raise SystemExit("seed count outside toy bounds")

    print("set,seed,weight,V,E,F,sign_syndrome,sign_tjoin,sign_dp,sign_pair_tests,sign_noise_match,sign_hidden_match,csp_nodes,csp_backtracks,accepted_states,cap_hit,first_accepted,first_hidden_match")
    for name in sorted(NAT2_PARAMETER_SETS):
        params = NAT2_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            seed = (f"MORPH-KEM NAT2 sweep {name} seed {seed_index:02d} v1").encode().ljust(48, b".")
            for weight in params.noise_weights:
                public, reference = generate_nat2_instance(params, seed, weight)
                result = recover_nat2(public, reference=reference)
                print(
                    f"{name},{seed_index},{weight},{result.vertices},{result.edges},{result.triangles},"
                    f"{result.sign_syndrome_weight},{result.sign_tjoin_weight},{result.sign_tjoin_dp_states},"
                    f"{result.sign_tjoin_pair_tests},{int(bool(result.sign_matches_planted_noise_after_public_success))},"
                    f"{int(bool(result.sign_matches_hidden_vertex_parity_after_public_success))},{result.csp_nodes},"
                    f"{result.csp_backtracks},{result.accepted_states},{int(result.accepted_state_cap_hit)},"
                    f"{int(result.first_state_accepted)},{int(bool(result.first_state_matches_hidden_after_public_success))}"
                )


if __name__ == "__main__":
    main()
