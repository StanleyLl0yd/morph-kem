#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.gluing_random_pairing import (
    G13_PARAMETER_SETS,
    audit_random_pairing_generator,
)


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit MORPH-KEM G13 raw cubic-dual triangle-pairing generator."
    )
    parser.add_argument("--attempts", type=int, default=4096)
    args = parser.parse_args()

    print(
        "set,triangles,attempts,dual_loop,dual_parallel,dual_disconnected,"
        "degenerate_triangle,duplicate_triangle,bad_edge_incidence,bad_vertex_link,"
        "bad_genus,success,success_rate,zero_success_rule3_upper,genus_histogram"
    )
    for name in sorted(G13_PARAMETER_SETS):
        audit = audit_random_pairing_generator(
            G13_PARAMETER_SETS[name], MASTER_SEED, attempts=args.attempts
        )
        counts = dict(audit.reason_counts)
        genus = "/".join(f"{g}:{count}" for g, count in audit.genus_histogram) or "-"
        print(
            f"{name},{audit.triangle_count},{audit.attempts},"
            f"{counts['dual_loop']},{counts['dual_parallel']},{counts['dual_disconnected']},"
            f"{counts['degenerate_triangle']},{counts['duplicate_triangle']},"
            f"{counts['bad_edge_incidence']},{counts['bad_vertex_link']},{counts['bad_genus']},"
            f"{counts['success']},{audit.success_rate:.9f},"
            f"{audit.zero_success_rule_of_three_upper:.9f},{genus}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
