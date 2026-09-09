#!/usr/bin/env python3
from __future__ import annotations

from morph_kem.klein_bottle import (
    KLEIN_BOTTLE_PARAMETER_SETS,
    analyze_klein_orientability,
    generate_klein_orientation_instance,
    recover_klein_gauge,
    reference_gauge_matches,
)


def main() -> int:
    master_seed = bytes.fromhex("30124490aabbccddeeff1029384756ab")
    print(
        "name,V,E,F,dual_cycle_rank,nonzero_syndromes,"
        "gauge_recovered,edge_checks"
    )
    ok = True
    for name in sorted(KLEIN_BOTTLE_PARAMETER_SETS):
        parameters = KLEIN_BOTTLE_PARAMETER_SETS[name]
        public, reference = generate_klein_orientation_instance(
            parameters,
            master_seed,
        )
        scaffold = public.scaffold
        orientation = analyze_klein_orientability(scaffold)
        recovery = recover_klein_gauge(public)
        recovered = reference_gauge_matches(recovery, reference)
        print(
            f"{name},"
            f"{len(scaffold.complex.vertices)},"
            f"{len(scaffold.edges)},"
            f"{len(scaffold.faces)},"
            f"{scaffold.dual_cycle_rank},"
            f"{orientation.nonzero_syndromes},"
            f"{recovered},"
            f"{recovery.edge_checks}"
        )
        ok = ok and (not orientation.orientable) and recovered
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
