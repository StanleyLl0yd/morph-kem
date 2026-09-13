from __future__ import annotations

import argparse
import hashlib

from morph_kem.nat_a5_torus_direct import recover_nat6_direct
from morph_kem.nat_a5_torus_flat import NAT6_PARAMETER_SETS, generate_nat6_instance


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--params", choices=sorted(NAT6_PARAMETER_SETS), default="nat6-8x9"
    )
    args = parser.parse_args()
    params = NAT6_PARAMETER_SETS[args.params]
    seed = hashlib.sha256(
        f"MORPH-KEM NAT6 direct fixed baseline {params.name} v1".encode("ascii")
    ).digest()
    public, reference = generate_nat6_instance(params, seed)
    recovery = recover_nat6_direct(public, reference=reference)

    print(f"parameters: {params.name}")
    print(f"fundamental cycles scanned: {recovery.fundamental_cycles_scanned}")
    print(f"fundamental path-edge scans: {recovery.fundamental_path_edge_scans}")
    print(f"pairing vectors: {recovery.first_pairing_vector}/{recovery.second_pairing_vector}")
    print(f"propagation assignments: {recovery.propagation_assignments}")
    print(f"accepted: {recovery.accepted}")
    print(f"pair matches planted: {recovery.pair_matches_planted_after_public_success}")
    print(f"gauge matches planted: {recovery.gauge_matches_planted_after_public_success}")


if __name__ == "__main__":
    main()
