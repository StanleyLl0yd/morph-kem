#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib

from morph_kem.gluing_random_pairing import (
    G13_PARAMETER_SETS,
    audit_random_pairing_generator,
)


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


def _seed(name: str, index: int) -> bytes:
    return hashlib.sha256(
        b"MORPH-KEM G13 generator sweep v1\x00"
        + MASTER_SEED
        + name.encode("ascii")
        + index.to_bytes(4, "big")
    ).digest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sweep MORPH-KEM G13 configuration-pairing generator conditioning."
    )
    parser.add_argument("--seeds", type=int, default=8)
    parser.add_argument("--attempts", type=int, default=1024)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 64:
        parser.error("--seeds must be in [1,64]")

    print(
        "set,seed,attempts,loop,parallel,disconnected,degenerate,duplicate,"
        "edge_incidence,vertex_link,bad_genus,success,rule3_upper"
    )
    for name in sorted(G13_PARAMETER_SETS):
        params = G13_PARAMETER_SETS[name]
        for seed_index in range(args.seeds):
            audit = audit_random_pairing_generator(
                params, _seed(name, seed_index), attempts=args.attempts
            )
            counts = dict(audit.reason_counts)
            print(
                f"{name},{seed_index},{audit.attempts},{counts['dual_loop']},"
                f"{counts['dual_parallel']},{counts['dual_disconnected']},"
                f"{counts['degenerate_triangle']},{counts['duplicate_triangle']},"
                f"{counts['bad_edge_incidence']},{counts['bad_vertex_link']},"
                f"{counts['bad_genus']},{counts['success']},"
                f"{audit.zero_success_rule_of_three_upper:.9f}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
