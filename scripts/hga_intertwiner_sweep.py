from __future__ import annotations

import argparse

from morph_kem.hga_intertwiner import HGA3_PARAMETER_SETS, generate_hga3_instance, recover_hga3


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 32:
        raise SystemExit("seed count outside toy bounds")
    print("set,seed,p,n,k,variables,equations,rank,nullity,row_eliminations,combination_tests,recovered_det,accepted,scalar_match,exact_match")
    for name in sorted(HGA3_PARAMETER_SETS):
        params = HGA3_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            seed = (f"MORPH-KEM HGA3 sweep {name} seed {seed_index:02d} v1").encode().ljust(48, b".")
            public, reference = generate_hga3_instance(params, seed)
            result = recover_hga3(public, reference=reference)
            print(
                f"{name},{seed_index},{result.prime},{result.dimension},{result.tuple_length},"
                f"{result.variables},{result.equations},{result.system_rank},{result.system_nullity},"
                f"{result.row_eliminations},{result.combination_candidates_tested},{result.recovered_determinant},"
                f"{int(result.exact_endpoint_verified)},"
                f"{int(bool(result.scalar_equivalent_to_planted_after_public_success))},"
                f"{int(bool(result.exactly_matches_planted_after_public_success))}"
            )


if __name__ == "__main__":
    main()
