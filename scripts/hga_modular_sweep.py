from __future__ import annotations

import argparse

from morph_kem.hga_modular import HGA2_PARAMETER_SETS, generate_hga2_instance, recover_hga2


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 32:
        raise SystemExit("seed count outside toy bounds")

    print("set,seed,planted_length,source_bits,target_bits,source_divisions,target_divisions,recovered_length,matrix_bits,accepted,matches_word,matches_matrix")
    for name in sorted(HGA2_PARAMETER_SETS):
        params = HGA2_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            seed = (f"MORPH-KEM HGA2 sweep {name} seed {seed_index:02d} v1").encode().ljust(48, b".")
            public, reference = generate_hga2_instance(params, seed)
            result = recover_hga2(public, reference=reference)
            print(
                f"{name},{seed_index},{len(reference.planted_word)},{result.source_bit_length},{result.target_bit_length},"
                f"{result.source_euclidean_divisions},{result.target_euclidean_divisions},{result.recovered_connector_length},"
                f"{result.recovered_matrix_entry_bit_length},{int(result.endpoint_verified)},"
                f"{int(bool(result.matches_planted_word_after_public_success))},"
                f"{int(bool(result.planted_matrix_equal_after_public_success))}"
            )


if __name__ == "__main__":
    main()
