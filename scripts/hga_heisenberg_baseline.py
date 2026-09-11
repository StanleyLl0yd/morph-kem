#!/usr/bin/env python3
from __future__ import annotations

import argparse

from morph_kem.hga_heisenberg import (
    HGA1_PARAMETER_SETS,
    generate_hga1_instance,
    recover_hga1,
)


MASTER_SEED = bytes.fromhex("99887766554433221100ffeeddccbbaa")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run MORPH-KEM HGA1 Heisenberg Nielsen-action negative control."
    )
    parser.add_argument("--params", choices=sorted(HGA1_PARAMETER_SETS), default="hga1-p11")
    args = parser.parse_args()
    params = HGA1_PARAMETER_SETS[args.params]
    public, reference = generate_hga1_instance(params, MASTER_SEED)
    recovery = recover_hga1(public, reference=reference)

    print(f"parameters: {params.name}")
    print(f"Heisenberg prime / group size: {params.prime}/{params.prime ** 3}")
    print(f"planted word length: {len(reference.secret_word)}")
    print(f"quotient orbit size: {recovery.quotient_orbit_size}")
    print(f"quotient BFS transitions: {recovery.quotient_bfs_transitions}")
    print(f"quotient shortest connector length: {recovery.quotient_shortest_length}")
    print(f"MITM forward states: {recovery.forward_states}")
    print(f"MITM backward states: {recovery.backward_states}")
    print(f"MITM transitions: {recovery.mitm_transitions}")
    print(f"MITM meet states: {recovery.meet_states}")
    print(f"recovered connector length: {recovery.recovered_length}")
    print(f"recovered connector: {''.join(recovery.recovered_word)}")
    print(f"public endpoint verification: {recovery.accepted}")
    print(
        "matches planted word after public success: "
        f"{recovery.matches_reference_after_public_success}"
    )

    return 0 if (
        recovery.accepted
        and recovery.recovered_length <= params.secret_word_length
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
