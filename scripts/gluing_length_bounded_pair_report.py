#!/usr/bin/env python3
from __future__ import annotations

from morph_kem.gluing_length_bounded_pair import (
    G18_PARAMETER_SETS,
    generate_length_bounded_pair_instance,
    recover_length_bounded_pair,
)


FIXED_SEED = bytes.fromhex(
    "a7450102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e"
)


def main() -> int:
    for name in sorted(G18_PARAMETER_SETS):
        params = G18_PARAMETER_SETS[name]
        public, reference = generate_length_bounded_pair_instance(params, FIXED_SEED)
        recovery = recover_length_bounded_pair(
            public, reference=reference, successful_flips=params.successful_flips
        )
        print(
            f"{name}: bounds={recovery.max_primal_length}/{recovery.max_dual_length} "
            f"selected={recovery.selected_primal_length}/{recovery.selected_dual_length} "
            f"cross={recovery.selected_crossing_count} accepted={recovery.selected_accepted} "
            f"roots={recovery.cover_roots_attempted} cover_scans={recovery.cover_edge_scans} "
            f"connector_calls={recovery.dual_connector_calls} "
            f"connector_scans={recovery.dual_connector_edge_scans} "
            f"treecotree_within={recovery.canonical_treecotree_within_bounds}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
