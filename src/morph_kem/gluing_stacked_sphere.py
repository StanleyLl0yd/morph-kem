from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
from itertools import combinations

from .complex import SimplicialComplex
from .gluing import GluingExperimentError
from .gluing_matching import _bridges_and_articulations
from .gluing_surface_hypercover import (
    HypercoverSatEncoding,
    HypercoverSatModel,
    ToroidalHypercoverPublicInstance,
    ToroidalHypercoverReference,
    ToroidalHypercoverValidation,
    _candidate_metrics,
    _exact_cover,
    _triangle_dual,
    _triangles,
    decode_toroidal_hypercover_sat_model,
    encode_toroidal_hypercover_sat,
    enumerate_p3_candidates,
    toroidal_hypercover_incidence,
    validate_toroidal_hypercover_witness,
)


Triangle = tuple[int, int, int]
TriangleGroup = tuple[int, ...]


@dataclass(frozen=True, slots=True)
class StackedSphereParameters:
    name: str
    stacking_steps: int

    def validate(self) -> None:
        if self.stacking_steps < 1 or self.stacking_steps > 64:
            raise GluingExperimentError("G14 stacking steps outside toy bounds")
        if (4 + 2 * self.stacking_steps) % 3:
            raise GluingExperimentError("G14 triangle count must be divisible by three")


G14_PARAMETER_SETS = {
    "g14-36": StackedSphereParameters("g14-36", 16),
    "g14-54": StackedSphereParameters("g14-54", 25),
    "g14-72": StackedSphereParameters("g14-72", 34),
}


@dataclass(frozen=True, slots=True)
class StackedSpherePublicInstance:
    name: str
    target: SimplicialComplex


@dataclass(frozen=True, slots=True)
class StackedSphereReference:
    groups: tuple[TriangleGroup, ...]


@dataclass(frozen=True, slots=True)
class ReverseStackingRecovery:
    initial_vertices: int
    initial_edges: int
    initial_triangles: int
    initial_degree_histogram: tuple[tuple[int, int], ...]
    initial_degree_three_vertices: int
    reverse_moves: int
    candidate_counts: tuple[int, ...]
    max_candidates: int
    terminal_vertices: int
    terminal_edges: int
    terminal_triangles: int
    terminal_euler_characteristic: int
    reached_tetrahedron_boundary: bool


@dataclass(frozen=True, slots=True)
class StackedSphereHypercoverRecovery:
    dual_edges: int
    dual_degree_histogram: tuple[tuple[int, int], ...]
    bridge_count: int
    articulation_points: tuple[int, ...]
    dual_bipartite: bool
    candidate_count: int
    candidate_membership_histogram: tuple[tuple[int, int], ...]
    candidate_overlap_degree_histogram: tuple[tuple[int, int], ...]
    candidate_triangle_incidence: int
    exact_cover_solutions: int
    exact_cover_solution_cap: int
    exact_cover_cap_hit: bool
    exact_cover_nodes: int
    exact_cover_decisions: int
    exact_cover_backtracks: int
    accepted_solutions: int
    nonreference_accepted_solutions: int
    reference_available: bool


@dataclass(frozen=True, slots=True)
class StackedSphereExperiment:
    public: StackedSpherePublicInstance
    reference: StackedSphereReference | None
    normalization: ReverseStackingRecovery
    hypercover: StackedSphereHypercoverRecovery


def _as_hypercover_public(
    public: StackedSpherePublicInstance,
) -> ToroidalHypercoverPublicInstance:
    return ToroidalHypercoverPublicInstance(name=public.name, target=public.target)


def _surface_counts(target: SimplicialComplex) -> tuple[int, int, int, int]:
    vertices = sum(len(simplex) == 1 for simplex in target.simplices)
    edges = sum(len(simplex) == 2 for simplex in target.simplices)
    triangles = sum(len(simplex) == 3 for simplex in target.simplices)
    return vertices, edges, triangles, vertices - edges + triangles


def _vertex_degrees(faces: set[Triangle]) -> dict[int, int]:
    neighbors: dict[int, set[int]] = defaultdict(set)
    for triangle in faces:
        for left, right in combinations(triangle, 2):
            neighbors[left].add(right)
            neighbors[right].add(left)
    return {vertex: len(items) for vertex, items in neighbors.items()}


def _reverse_candidates(faces: set[Triangle]) -> tuple[tuple[int, Triangle], ...]:
    neighbors: dict[int, set[int]] = defaultdict(set)
    incident: dict[int, set[Triangle]] = defaultdict(set)
    for triangle in faces:
        for vertex in triangle:
            incident[vertex].add(triangle)
        for left, right in combinations(triangle, 2):
            neighbors[left].add(right)
            neighbors[right].add(left)

    candidates: list[tuple[int, Triangle]] = []
    for vertex in sorted(neighbors):
        if len(neighbors[vertex]) != 3 or len(incident[vertex]) != 3:
            continue
        link = tuple(sorted(neighbors[vertex]))
        if link in faces:
            continue
        expected = {
            tuple(sorted((vertex, left, right)))
            for left, right in combinations(link, 2)
        }
        if incident[vertex] != expected:
            continue
        candidates.append((vertex, link))
    return tuple(candidates)


def reverse_stacked_sphere(
    public: StackedSpherePublicInstance,
) -> ReverseStackingRecovery:
    faces = set(_triangles(_as_hypercover_public(public)))
    initial_target = SimplicialComplex.from_facets(faces)
    initial_vertices, initial_edges, initial_triangles, _ = _surface_counts(initial_target)
    degree_histogram = tuple(sorted(Counter(_vertex_degrees(faces).values()).items()))
    initial_degree_three = sum(degree == 3 for degree in _vertex_degrees(faces).values())

    candidate_counts: list[int] = []
    moves = 0
    while True:
        candidates = _reverse_candidates(faces)
        candidate_counts.append(len(candidates))
        if not candidates:
            break
        vertex, link = candidates[0]
        faces = {triangle for triangle in faces if vertex not in triangle}
        faces.add(link)
        moves += 1

    terminal = SimplicialComplex.from_facets(faces)
    vertices, edges, triangles, chi = _surface_counts(terminal)
    tetrahedron_boundary = (
        vertices == 4
        and edges == 6
        and triangles == 4
        and chi == 2
        and len(terminal.facets) == 4
        and all(len(facet) == 3 for facet in terminal.facets)
    )
    return ReverseStackingRecovery(
        initial_vertices=initial_vertices,
        initial_edges=initial_edges,
        initial_triangles=initial_triangles,
        initial_degree_histogram=degree_histogram,
        initial_degree_three_vertices=initial_degree_three,
        reverse_moves=moves,
        candidate_counts=tuple(candidate_counts),
        max_candidates=max(candidate_counts, default=0),
        terminal_vertices=vertices,
        terminal_edges=edges,
        terminal_triangles=triangles,
        terminal_euler_characteristic=chi,
        reached_tetrahedron_boundary=tetrahedron_boundary,
    )


def _is_bipartite(adjacency: list[list[int]]) -> bool:
    colors = [-1] * len(adjacency)
    for root in range(len(adjacency)):
        if colors[root] >= 0:
            continue
        colors[root] = 0
        queue = [root]
        while queue:
            current = queue.pop(0)
            for neighbor in adjacency[current]:
                if colors[neighbor] < 0:
                    colors[neighbor] = colors[current] ^ 1
                    queue.append(neighbor)
                elif colors[neighbor] == colors[current]:
                    return False
    return True


def validate_stacked_sphere_witness(
    public: StackedSpherePublicInstance,
    groups: tuple[TriangleGroup, ...],
) -> ToroidalHypercoverValidation:
    return validate_toroidal_hypercover_witness(_as_hypercover_public(public), groups)


def recover_stacked_sphere_hypercover(
    public: StackedSpherePublicInstance,
    *,
    reference: StackedSphereReference | None = None,
    solution_cap: int = 64,
) -> StackedSphereHypercoverRecovery:
    if solution_cap < 1 or solution_cap > 1024:
        raise GluingExperimentError("G14 exact-cover solution cap outside toy bounds")

    base_public = _as_hypercover_public(public)
    triangles = _triangles(base_public)
    adjacency, dual_edges = _triangle_dual(base_public)
    bridges, articulations = _bridges_and_articulations(adjacency)
    candidates = enumerate_p3_candidates(base_public)
    memberships, overlap_degrees, candidate_incidence = _candidate_metrics(
        len(triangles), candidates
    )
    search = _exact_cover(len(triangles), candidates, solution_cap)
    accepted = tuple(
        groups
        for groups in search.solutions
        if validate_toroidal_hypercover_witness(base_public, groups).valid
    )
    reference_groups = (
        tuple(sorted(tuple(sorted(group)) for group in reference.groups))
        if reference is not None
        else None
    )
    nonreference = sum(
        reference_groups is not None and groups != reference_groups for groups in accepted
    )
    degree_histogram = tuple(sorted(Counter(len(items) for items in adjacency).items()))
    return StackedSphereHypercoverRecovery(
        dual_edges=len(dual_edges),
        dual_degree_histogram=degree_histogram,
        bridge_count=len(bridges),
        articulation_points=tuple(sorted(articulations)),
        dual_bipartite=_is_bipartite(adjacency),
        candidate_count=len(candidates),
        candidate_membership_histogram=memberships,
        candidate_overlap_degree_histogram=overlap_degrees,
        candidate_triangle_incidence=candidate_incidence,
        exact_cover_solutions=len(search.solutions),
        exact_cover_solution_cap=solution_cap,
        exact_cover_cap_hit=len(search.solutions) >= solution_cap,
        exact_cover_nodes=search.nodes,
        exact_cover_decisions=search.decisions,
        exact_cover_backtracks=search.backtracks,
        accepted_solutions=len(accepted),
        nonreference_accepted_solutions=nonreference,
        reference_available=reference is not None,
    )


def encode_stacked_sphere_sat(
    public: StackedSpherePublicInstance,
) -> HypercoverSatEncoding:
    return encode_toroidal_hypercover_sat(_as_hypercover_public(public))


def decode_stacked_sphere_sat_model(
    public: StackedSpherePublicInstance,
    encoding: HypercoverSatEncoding,
    literals: tuple[int, ...],
) -> HypercoverSatModel:
    return decode_toroidal_hypercover_sat_model(
        _as_hypercover_public(public), encoding, literals
    )


def _stacking_choice(master_seed: bytes, name: str, step: int, count: int) -> int:
    digest = hashlib.sha256(
        b"MORPH-KEM G14 stacking choice v1\x00"
        + master_seed
        + name.encode("ascii")
        + step.to_bytes(4, "big")
    ).digest()
    return int.from_bytes(digest[:8], "big") % count


def _relabel_mapping(master_seed: bytes, name: str, vertices: tuple[int, ...]) -> dict[int, int]:
    ordered = sorted(
        vertices,
        key=lambda vertex: (
            hashlib.sha256(
                b"MORPH-KEM G14 public relabel v1\x00"
                + master_seed
                + name.encode("ascii")
                + vertex.to_bytes(4, "big")
            ).digest(),
            vertex,
        ),
    )
    return {vertex: index for index, vertex in enumerate(ordered)}


def generate_stacked_sphere_instance(
    params: StackedSphereParameters,
    master_seed: bytes,
) -> tuple[StackedSpherePublicInstance, StackedSphereReference | None]:
    params.validate()
    if len(master_seed) < 16:
        raise GluingExperimentError("G14 master seed must contain at least 128 bits")

    faces: set[Triangle] = {
        (0, 1, 2),
        (0, 1, 3),
        (0, 2, 3),
        (1, 2, 3),
    }
    for step in range(params.stacking_steps):
        ordered_faces = sorted(faces)
        selected = ordered_faces[_stacking_choice(master_seed, params.name, step, len(ordered_faces))]
        faces.remove(selected)
        vertex = 4 + step
        left, middle, right = selected
        faces.update(
            {
                tuple(sorted((left, middle, vertex))),
                tuple(sorted((left, right, vertex))),
                tuple(sorted((middle, right, vertex))),
            }
        )

    target = SimplicialComplex.from_facets(faces)
    mapping = _relabel_mapping(master_seed, params.name, target.vertices)
    target = target.relabel(mapping)
    public = StackedSpherePublicInstance(params.name, target)

    incidence = toroidal_hypercover_incidence(_as_hypercover_public(public))
    expected_triangles = 4 + 2 * params.stacking_steps
    expected_vertices = params.stacking_steps + 4
    expected_edges = 3 * expected_vertices - 6
    if (
        incidence.vertices != expected_vertices
        or incidence.edges != expected_edges
        or incidence.triangles != expected_triangles
        or incidence.euler_characteristic != 2
        or incidence.min_triangles_per_edge != 2
        or incidence.max_triangles_per_edge != 2
    ):
        raise GluingExperimentError("G14 constructive carrier failed sphere invariants")

    base_public = _as_hypercover_public(public)
    triangles = _triangles(base_public)
    candidates = enumerate_p3_candidates(base_public)
    secret_order = {
        candidate: hashlib.sha256(
            b"MORPH-KEM G14 reference candidate order v1\x00"
            + master_seed
            + params.name.encode("ascii")
            + b"".join(index.to_bytes(4, "big") for index in candidate)
        ).digest()
        for candidate in candidates
    }
    search = _exact_cover(len(triangles), candidates, 1, secret_order=secret_order)
    reference = (
        StackedSphereReference(groups=search.solutions[0]) if search.solutions else None
    )
    if reference is not None and not validate_stacked_sphere_witness(public, reference.groups).valid:
        raise GluingExperimentError("G14 generated reference hypercover does not validate")
    return public, reference


def run_stacked_sphere_experiment(
    params: StackedSphereParameters,
    master_seed: bytes,
    *,
    solution_cap: int = 64,
) -> StackedSphereExperiment:
    public, reference = generate_stacked_sphere_instance(params, master_seed)
    normalization = reverse_stacked_sphere(public)
    hypercover = recover_stacked_sphere_hypercover(
        public, reference=reference, solution_cap=solution_cap
    )
    return StackedSphereExperiment(public, reference, normalization, hypercover)
