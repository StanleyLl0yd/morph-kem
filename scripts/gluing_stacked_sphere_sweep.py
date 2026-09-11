from __future__ import annotations

import argparse
import hashlib

from morph_kem.gluing_stacked_sphere import (
    G14_PARAMETER_SETS,
    generate_stacked_sphere_instance,
    recover_reverse_stacking,
)
from morph_kem.gluing_surface_hypercover import toroidal_hypercover_incidence


def _seed(name: str, seed_index: int) -> bytes:
    return hashlib.sha256(
        b"MORPH-KEM G14 sweep v1\x00"
        + name.encode("ascii")
        + seed_index.to_bytes(4, "big")
    ).digest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=8)
    args = parser.parse_args()
    if args.seeds < 1 or args.seeds > 64:
        raise SystemExit("seed count outside toy bounds")

    print(
        "set,seed,stacking_steps,V,E,F,chi,reverse_moves,max_candidates,"
        "terminal_V,terminal_E,terminal_F,terminal_chi,reached_tetrahedron"
    )
    for name, params in sorted(G14_PARAMETER_SETS.items()):
        for seed_index in range(args.seeds):
            public = generate_stacked_sphere_instance(params, _seed(name, seed_index))
            incidence = toroidal_hypercover_incidence(public)
            recovery = recover_reverse_stacking(public)
            print(
                f"{name},{seed_index},{params.stacking_steps},"
                f"{incidence.vertices},{incidence.edges},{incidence.triangles},"
                f"{incidence.euler_characteristic},{recovery.moves},"
                f"{recovery.max_candidates},{recovery.terminal_vertices},"
                f"{recovery.terminal_edges},{recovery.terminal_triangles},"
                f"{recovery.terminal_euler_characteristic},"
                f"{int(recovery.reached_tetrahedron_boundary)}"
            )


if __name__ == "__main__":
    main()
