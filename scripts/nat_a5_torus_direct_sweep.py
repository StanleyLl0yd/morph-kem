from __future__ import annotations

import argparse
import hashlib

from morph_kem.nat_a5_torus_direct import recover_nat6_direct
from morph_kem.nat_a5_torus_flat import NAT6_PARAMETER_SETS, generate_nat6_instance


def seed_for(name: str, index: int) -> bytes:
    return hashlib.sha256(
        f"MORPH-KEM NAT6 direct sweep {name} seed {index} v1".encode("ascii")
    ).digest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 64:
        raise SystemExit("--seeds must be in 1..64")

    print(
        "set,seed,V,E,F,cycles_scanned,path_edge_scans,first_pairing,second_pairing,"
        "assignments,accepted,pair_match,gauge_match"
    )
    for params in NAT6_PARAMETER_SETS.values():
        for index in range(args.seeds):
            public, reference = generate_nat6_instance(params, seed_for(params.name, index))
            recovery = recover_nat6_direct(public, reference=reference)
            print(
                f"{params.name},{index},{len(public.target.vertices)},"
                f"{len(public.observed_edge_labels)},"
                f"{sum(1 for simplex in public.target.simplices if len(simplex) == 3)},"
                f"{recovery.fundamental_cycles_scanned},"
                f"{recovery.fundamental_path_edge_scans},"
                f"{recovery.first_pairing_vector[0]}{recovery.first_pairing_vector[1]},"
                f"{recovery.second_pairing_vector[0]}{recovery.second_pairing_vector[1]},"
                f"{recovery.propagation_assignments},"
                f"{int(recovery.accepted)},"
                f"{int(bool(recovery.pair_matches_planted_after_public_success))},"
                f"{int(bool(recovery.gauge_matches_planted_after_public_success))}"
            )


if __name__ == "__main__":
    main()
