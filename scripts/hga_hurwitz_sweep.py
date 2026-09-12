from __future__ import annotations

import argparse

from morph_kem.hga_hurwitz import HGA4_PARAMETER_SETS, generate_hga4_instance, recover_hga4


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 32:
        raise SystemExit("seed count outside toy bounds")

    print("set,seed,planted_len,target_total_len,forward_states,backward_states,forward_transitions,backward_transitions,meet_states,recovered_len,accepted,quotient_match,planted_match,materially_shorter")
    for name in sorted(HGA4_PARAMETER_SETS):
        params = HGA4_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            seed = (f"MORPH-KEM HGA4 sweep {name} seed {seed_index:02d} v1").encode().ljust(48, b".")
            public, reference = generate_hga4_instance(params, seed)
            result = recover_hga4(public, reference=reference)
            print(
                f"{name},{seed_index},{result.planted_word_length},{sum(result.target_component_lengths)},"
                f"{result.forward_states},{result.backward_states},{result.forward_transitions},{result.backward_transitions},"
                f"{result.meet_states},{result.recovered_connector_length},{int(result.endpoint_verified)},"
                f"{int(bool(result.quotient_matches_planted))},{int(bool(result.matches_planted_word_after_public_success))},"
                f"{int(result.materially_shorter_than_planted)}"
            )


if __name__ == "__main__":
    main()
