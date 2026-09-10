#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time

from morph_kem.coherence3 import (
    face_boundary_fiber,
    generate_kernel_coherence_instance,
    public_gf2_coherence_attack,
    validate_kernel_coherence,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the MORPH K2.3 3D kernel-coherence baseline.")
    parser.add_argument(
        "--master-seed",
        default="2309425a6bc7d8e90123456789abcdef",
        help="hex-encoded deterministic K2.3 generation seed",
    )
    args = parser.parse_args()

    public, reference = generate_kernel_coherence_instance(bytes.fromhex(args.master_seed))
    scaffold = public.scaffold
    started = time.perf_counter()
    attack = public_gf2_coherence_attack(public)
    elapsed = time.perf_counter() - started

    print(
        "cells V/E/F/T: "
        f"{len(scaffold.vertices)}/{len(scaffold.edges)}/{len(scaffold.faces)}/{len(scaffold.tetrahedra)}"
    )
    print(f"face tetrahedron degree set: {sorted(set(scaffold.face_tetra_degrees))}")
    print(f"Euler characteristic: {scaffold.euler_characteristic}")
    print(f"public Q8 boundary fiber sizes: {tuple(len(face_boundary_fiber(value)) for value in public.face_boundaries)}")
    print(f"reference accepted: {validate_kernel_coherence(public, reference.face_values)}")
    print(f"GF(2) equations/variables: {attack.equations}/{attack.variables}")
    print(f"GF(2) rank/nullity: {attack.rank}/{attack.nullity}")
    print(f"dependent equations: {attack.dependent_equations}")
    print(f"row XOR operations: {attack.row_xors}")
    print(f"equivalent witnesses: {attack.equivalent_witnesses}")
    print(f"public attack accepted: {attack.accepted}")
    print(f"public attack equals planted representative: {attack.face_values == reference.face_values}")
    print(f"elapsed seconds: {elapsed:.6f}")
    return 0 if attack.accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
