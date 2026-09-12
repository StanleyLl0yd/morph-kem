from __future__ import annotations

import argparse

from morph_kem.nat_s3 import NAT2_PARAMETER_SETS, generate_nat2_instance
from morph_kem.nat_s3_support import recover_from_sign_support


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 32:
        raise SystemExit("seed count outside toy bounds")

    print("set,seed,weight,sign_correction,reached,connected,consistent,accepted,support_match,state_match")
    for name in sorted(NAT2_PARAMETER_SETS):
        params = NAT2_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            seed = (f"MORPH-KEM NAT2 sweep {name} seed {seed_index:02d} v1").encode().ljust(48, b".")
            for weight in params.noise_weights:
                public, reference = generate_nat2_instance(params, seed, weight)
                result = recover_from_sign_support(public, reference=reference)
                print(
                    f"{name},{seed_index},{weight},{result.sign_correction_weight},{result.reached_vertices},"
                    f"{int(result.clean_subgraph_connected)},{int(result.propagation_consistent)},"
                    f"{int(result.exact_state_accepted)},"
                    f"{int(bool(result.support_matches_planted_after_public_success))},"
                    f"{int(bool(result.state_matches_hidden_after_public_success))}"
                )


if __name__ == "__main__":
    main()
