from __future__ import annotations

import argparse
import hashlib

from morph_kem.hga_hurwitz import generate_hga4_instance, recover_hga4
from morph_kem.hga_hurwitz_self_avoiding import (
    HGA4BDeadEnd,
    HGA4B_PARAMETER_SETS,
    _source_parameters,
    generate_hga4b_instance,
    recover_hga4b,
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
        "set,seed,L,generation_ok,dead_end_step,achieved,path_states,target_total_len,"
        "sa_forward,sa_backward,sa_meets,sa_recovered,sa_shorter,sa_accepted,sa_planted_match,"
        "old_forward,old_backward,old_meets,old_recovered,old_shorter,old_accepted,old_planted_match"
    )
    for params in HGA4B_PARAMETER_SETS.values():
        for index in range(args.seeds):
            seed = seed_for(params.name, index)

            old_public, old_reference = generate_hga4_instance(_source_parameters(params), seed)
            old = recover_hga4(old_public, reference=old_reference)

            try:
                public, reference = generate_hga4b_instance(params, seed)
            except HGA4BDeadEnd as failure:
                print(
                    f"{params.name},{index},{params.planted_word_length},0,{failure.step},"
                    f"{len(failure.partial_word)},{len(failure.path_states)},-1,"
                    f"-1,-1,-1,-1,0,0,0,"
                    f"{old.forward_states},{old.backward_states},{old.meet_states},"
                    f"{old.recovered_connector_length},{int(old.materially_shorter_than_planted)},"
                    f"{int(old.endpoint_verified)},{int(bool(old.matches_planted_word_after_public_success))}"
                )
                continue

            if public.source != old_public.source:
                raise RuntimeError("paired HGA4/HGA4b source mismatch")
            sa = recover_hga4b(public, reference=reference)
            print(
                f"{params.name},{index},{params.planted_word_length},1,-1,"
                f"{len(reference.planted_word)},{reference.distinct_path_states},"
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
