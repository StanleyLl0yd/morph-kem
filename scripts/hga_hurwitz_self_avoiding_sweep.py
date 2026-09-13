from __future__ import annotations

import argparse
import hashlib

from morph_kem.hga_hurwitz_self_avoiding import (
    HGA4B_PARAMETER_SETS,
    generate_hga4b_instance,
    recover_hga4b_paired,
)


def seed_for(name: str, index: int) -> bytes:
    return hashlib.sha256(
        f"MORPH-KEM HGA4b sweep {name} seed {index} v1".encode("ascii")
    ).digest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 16:
        raise SystemExit("--seeds must be between 1 and 16")

    print(
        "set,seed,L,path_states,dead_ends,target_total_len,"
        "sa_forward,sa_backward,sa_meets,sa_recovered,sa_shorter,sa_accepted,sa_planted_match,"
        "old_forward,old_backward,old_meets,old_recovered,old_shorter,old_accepted,old_planted_match"
    )
    for params in HGA4B_PARAMETER_SETS.values():
        for index in range(args.seeds):
            seed = seed_for(params.name, index)
            public, reference = generate_hga4b_instance(params, seed)
            paired = recover_hga4b_paired(params, seed)
            sa = paired.self_avoiding
            old = paired.locally_reduced
            print(
                f"{params.name},{index},{params.planted_word_length},"
                f"{reference.distinct_path_states},{reference.dead_end_count},"
                f"{sum(len(word) for word in public.target)},"
                f"{sa.forward_states},{sa.backward_states},{sa.meet_states},"
                f"{sa.recovered_connector_length},{int(sa.materially_shorter_than_planted)},"
                f"{int(sa.endpoint_verified)},{int(bool(sa.matches_planted_word_after_public_success))},"
                f"{old.forward_states},{old.backward_states},{old.meet_states},"
                f"{old.recovered_connector_length},{int(old.materially_shorter_than_planted)},"
                f"{int(old.endpoint_verified)},{int(bool(old.matches_planted_word_after_public_success))}"
            )


if __name__ == "__main__":
    main()
