#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib

from morph_kem.hga_heisenberg import (
    HGA1_PARAMETER_SETS,
    generate_hga1_instance,
    recover_hga1,
)


MASTER_SEED = bytes.fromhex("99887766554433221100ffeeddccbbaa")


def _seed(name: str, index: int) -> bytes:
    return hashlib.sha256(
        b"MORPH-KEM HGA1 sweep v1\x00"
        + MASTER_SEED
        + name.encode("ascii")
        + index.to_bytes(4, "big")
    ).digest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sweep MORPH-KEM HGA1 public Nielsen-action recovery."
    )
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 64:
        parser.error("--seeds must be in [1,64]")

    print(
        "set,seed,p,planted_length,quotient_orbit,quotient_shortest,"
        "forward_states,backward_states,transitions,meet_states,"
        "recovered_length,accepted,matches_planted"
    )
    failures = 0
    for name in sorted(HGA1_PARAMETER_SETS):
        params = HGA1_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            public, reference = generate_hga1_instance(params, _seed(name, seed_index))
            recovery = recover_hga1(public, reference=reference)
            print(
                f"{name},{seed_index},{params.prime},{len(reference.secret_word)},"
                f"{recovery.quotient_orbit_size},{recovery.quotient_shortest_length},"
                f"{recovery.forward_states},{recovery.backward_states},"
                f"{recovery.mitm_transitions},{recovery.meet_states},"
                f"{recovery.recovered_length},{int(recovery.accepted)},"
                f"{int(bool(recovery.matches_reference_after_public_success))}"
            )
            failures += int(
                not recovery.accepted
                or recovery.recovered_length > params.secret_word_length
            )

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
