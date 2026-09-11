from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib
from itertools import combinations

from .complex import SimplicialComplex
from .gluing import GluingExperimentError
from .gluing_surface_hypercover import (
    ToroidalHypercoverPublicInstance,
    toroidal_hypercover_incidence,
)


Triangle = tuple[int, int, int]


@dataclass(frozen=True, slots=True)
class StackedSphereParameters:
    name: str
    triangle_count: int

    def validate(self) -> None:
        if self.triangle_count < 12 or self.triangle_count > 192:
            raise GluingExperimentError("G14 triangle count outside toy bounds")
        if self.triangle_count % 3:
            raise GluingExperimentError("G14 triangle count must be divisible by three")
        if (self.triangle_count - 4) % 2:
            raise GluingExperimentError("G14 triangle count is not reachable by stacking")

    @property
    def stacking_steps(self) -> int:
        return (self.triangle_count - 4) // 2


G14_PARAMETER_SETS = {
    "g14-36": StackedSphereParameters("g14-36", 36),
    "g14-54": StackedSphereParameters("g14-54", 54),
    "g14-72": StackedSphereParameters("g14-72", 72),
}


@dataclass(frozen=True, slots=True)
class ReverseStackingRecovery:
    moves: int
    removed_vertices: tuple[int, ...]
    candidate_counts: tuple[int, ...]
    candidate_count_histogram: tuple[tuple[int, int], ...]
    max_candidates: int
    terminal_vertices: int
    terminal_edges: int
    terminal_triangles: int
    terminal_euler_characteristic: int
    reached_tetrahedron_boundary: bool


def _facets(public: ToroidalHypercoverPublicInstance) -> tuple[Triangle, ...]:
    return tuple(sorted(simplex for simplex in public.target.facets if len(simplex) == 3))


def _seeded_index(seed: bytes, domain: bytes, counter: int, modulus: int) -> int:
    if modulus <= 0:
        raise GluingExperimentError("G14 seeded selection has empty domain")
    digest = hashlib.sha256(
        domain + b"\x00" + seed + counter.to_bytes(8, "big")
    ).digest()
    return int.from_bytes(digest[:8], "big") % modulus


def _public_relabel(facets: set[Triangle], seed: bytes) -> set[Triangle]:
    vertices = sorted({vertex for facet in facets for vertex in facet})
    ordered = sorted(
        vertices,
        key=lambda vertex: (
            hashlib.sha256(
                b"MORPH-KEM G14 public relabel v1\x00"
                + seed
                + vertex.to_bytes(4, "big")
            ).digest(),
            vertex,
        ),
    )
    mapping = {vertex: index for index, vertex in enumerate(ordered)}
    return {
        tuple(sorted(mapping[vertex] for vertex in facet))
        for facet in facets
    }


def generate_stacked_sphere_instance(
    params: StackedSphereParameters,
    master_seed: bytes,
) -> ToroidalHypercoverPublicInstance:
    params.validate()
    if len(master_seed) < 16:
        raise GluingExperimentError("G14 master seed must contain at least 128 bits")

    facets: set[Triangle] = {
        (0, 1, 2),
        (0, 1, 3),
        (0, 2, 3),
        (1, 2, 3),
    }
    for step in range(params.stacking_steps):
        ordered_facets = sorted(facets)
        selected = ordered_facets[
            _seeded_index(
                master_seed,
                b"MORPH-KEM G14 stacking face v1",
                step,
                len(ordered_facets),
            )
        ]
        facets.remove(selected)
        new_vertex = 4 + step
        left, middle, right = selected
        facets.add(tuple(sorted((left, middle, new_vertex))))
        facets.add(tuple(sorted((left, right, new_vertex))))
        facets.add(tuple(sorted((middle, right, new_vertex))))

    facets = _public_relabel(facets, master_seed)
    public = ToroidalHypercoverPublicInstance(
        name=params.name,
        target=SimplicialComplex.from_facets(sorted(facets)),
    )
    incidence = toroidal_hypercover_incidence(public)
    expected_vertices = params.triangle_count // 2 + 2
    expected_edges = 3 * expected_vertices - 6
    if (
        incidence.vertices != expected_vertices
        or incidence.edges != expected_edges
        or incidence.triangles != params.triangle_count
        or incidence.euler_characteristic != 2
        or incidence.min_triangles_per_edge != 2
        or incidence.max_triangles_per_edge != 2
    ):
        raise GluingExperimentError("G14 generated carrier failed sphere invariants")
    return public


def _vertex_neighbors(facets: set[Triangle]) -> dict[int, set[int]]:
    neighbors: dict[int, set[int]] = {}
    for facet in facets:
        for left, right in combinations(facet, 2):
            neighbors.setdefault(left, set()).add(right)
            neighbors.setdefault(right, set()).add(left)
    return neighbors


def _reverse_candidates(facets: set[Triangle]) -> tuple[tuple[int, Triangle], ...]:
    neighbors = _vertex_neighbors(facets)
    candidates: list[tuple[int, Triangle]] = []
    for vertex, adjacent in neighbors.items():
        if len(adjacent) != 3:
            continue
        link = tuple(sorted(adjacent))
        if link in facets:
            continue
        incident = {facet for facet in facets if vertex in facet}
        expected = {
            tuple(sorted((vertex, left, right)))
            for left, right in combinations(link, 2)
        }
        if incident == expected:
            candidates.append((vertex, link))
    return tuple(sorted(candidates))


def _complex_counts(facets: set[Triangle]) -> tuple[int, int, int, int]:
    vertices = {vertex for facet in facets for vertex in facet}
    edges = {
        tuple(sorted(edge))
        for facet in facets
        for edge in combinations(facet, 2)
    }
    triangle_count = len(facets)
    return len(vertices), len(edges), triangle_count, len(vertices) - len(edges) + triangle_count


def recover_reverse_stacking(
    public: ToroidalHypercoverPublicInstance,
) -> ReverseStackingRecovery:
    facets = set(_facets(public))
    removed: list[int] = []
    candidate_counts: list[int] = []

    while True:
        candidates = _reverse_candidates(facets)
        if not candidates:
            break
        candidate_counts.append(len(candidates))
        vertex, link = candidates[0]
        facets = {facet for facet in facets if vertex not in facet}
        if link in facets:
            raise GluingExperimentError("G14 reverse stacking would duplicate restored face")
        facets.add(link)
        removed.append(vertex)

    vertices, edges, triangles, euler = _complex_counts(facets)
    reached_tetrahedron = (
        vertices == 4
        and edges == 6
        and triangles == 4
        and euler == 2
        and len({vertex for facet in facets for vertex in facet}) == 4
    )
    histogram = tuple(sorted(Counter(candidate_counts).items()))
    return ReverseStackingRecovery(
        moves=len(removed),
        removed_vertices=tuple(removed),
        candidate_counts=tuple(candidate_counts),
        candidate_count_histogram=histogram,
        max_candidates=max(candidate_counts, default=0),
        terminal_vertices=vertices,
        terminal_edges=edges,
        terminal_triangles=triangles,
        terminal_euler_characteristic=euler,
        reached_tetrahedron_boundary=reached_tetrahedron,
    )
