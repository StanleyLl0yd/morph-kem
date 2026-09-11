from __future__ import annotations

import argparse
from collections import Counter

from morph_kem.gluing_stacked_sphere import (
    G14_PARAMETER_SETS,
    generate_stacked_sphere_instance,
    recover_reverse_stacking,
)
from morph_kem.gluing_surface_hypercover import toroidal_hypercover_incidence


MASTER_SEED = bytes.fromhex("76120450aabbccddeeff001122334455")


def _vertex_degree_histogram(public) -> tuple[tuple[int, int], ...]:
    vertices = public.target.vertices
    edges = [simplex for simplex in public.target.simplices if len(simplex) == 2]
    degrees = {vertex: 0 for vertex in vertices}
    for left, right in edges:
        degrees[left] += 1
        degrees[right] += 1
    return tuple(sorted(Counter(degrees.values()).items()))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", choices=sorted(G14_PARAMETER_SETS), default="g14-72")
    args = parser.parse_args()

    params = G14_PARAMETER_SETS[args.params]
    public = generate_stacked_sphere_instance(params, MASTER_SEED)
    incidence = toroidal_hypercover_incidence(public)
    recovery = recover_reverse_stacking(public)

    print(f"parameters: {params.name}")
    print(f"stacking steps: {params.stacking_steps}")
    print(f"public V/E/F: {incidence.vertices}/{incidence.edges}/{incidence.triangles}")
    print(f"Euler characteristic: {incidence.euler_characteristic}")
    print(
        "edge triangle incidence min/max: "
        f"{incidence.min_triangles_per_edge}/{incidence.max_triangles_per_edge}"
    )
    print(f"primal vertex-degree histogram: {_vertex_degree_histogram(public)}")
    print(f"reverse-stacking moves: {recovery.moves}")
    print(f"candidate count histogram: {recovery.candidate_count_histogram}")
    print(f"maximum simultaneous reverse candidates: {recovery.max_candidates}")
    print(
        "terminal V/E/F/chi: "
        f"{recovery.terminal_vertices}/{recovery.terminal_edges}/"
        f"{recovery.terminal_triangles}/{recovery.terminal_euler_characteristic}"
    )
    print(f"reached tetrahedron boundary: {recovery.reached_tetrahedron_boundary}")


if __name__ == "__main__":
    main()
