from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib

from .complex import SimplicialComplex
from .gluing import GluingExperimentError, _DeterministicRng
from .gluing_irregular_hypercover import (
    _apply_flip,
    _dual_is_bipartite,
    _dual_short_cycles,
    _facet_edges,
    _legal_flips,
    _local_signature_metrics,
    _normalization_improving_flip_count,
    _primal_vertex_degree_histogram,
)
from .gluing_matching import _bridges_and_articulations
from .gluing_stacked_sphere import _reverse_candidates, recover_reverse_stacking
from .gluing_surface_hypercover import (
    HypercoverSatEncoding,
    HypercoverSatModel,
    ToroidalHypercoverPublicInstance,
    Triangle,
    TriangleGroup,
    _candidate_metrics,
    _exact_cover,
    _normalize_groups,
    _triangle_dual,
    _triangles,
    decode_toroidal_hypercover_sat_model,
    encode_toroidal_hypercover_sat,
    enumerate_p3_candidates,
    toroidal_hypercover_incidence,
    validate_toroidal_hypercover_witness,
)


@dataclass(frozen=True, slots=True)
class MixedSphereParameters:
    name: str
    triangle_count: int
    successful_flips: int
    max_generation_attempts: int = 16
    max_proposal_factor: int = 20

    def validate(self) -> None:
        if self.triangle_count < 24 or self.triangle_count > 192:
            raise GluingExperimentError("G15 triangle count outside toy bounds")
        if self.triangle_count % 3:
            raise GluingExperimentError("G15 triangle count must be divisible by three")
        if (self.triangle_count - 20) % 2:
            raise GluingExperimentError("G15 triangle count is not reachable from icosahedron")
        if self.successful_flips < self.triangle_count or self.successful_flips > 10000:
            raise GluingExperimentError("G15 successful-flip target outside toy bounds")
        if self.max_generation_attempts < 1 or self.max_generation_attempts > 64:
            raise GluingExperimentError("G15 generation-attempt cap outside toy bounds")
        if self.max_proposal_factor < 2 or self.max_proposal_factor > 100:
            raise GluingExperimentError("G15 flip-proposal factor outside toy bounds")

    @property
    def growth_steps(self) -> int:
        return (self.triangle_count - 20) // 2


G15_PARAMETER_SETS = {
    "g15-36": MixedSphereParameters("g15-36", 36, 720),
    "g15-54": MixedSphereParameters("g15-54", 54, 1080),
    "g15-72": MixedSphereParameters("g15-72", 72, 1440),
}


MixedSpherePublicInstance = ToroidalHypercoverPublicInstance


@dataclass(frozen=True, slots=True)
class MixedSphereReference:
    groups: tuple[TriangleGroup, ...]
    growth_steps: int
    successful_flips: int
    rejected_flip_proposals: int
    generation_retries: int


@dataclass(frozen=True, slots=True)
class MixedSphereRecovery:
    accepted_groups: tuple[tuple[TriangleGroup, ...], ...]
    growth_steps: int
    successful_flips: int
    rejected_flip_proposals: int
    generation_retries: int
    primal_vertex_degree_histogram: tuple[tuple[int, int], ...]
    initial_degree_three_vertices: int
    initial_reverse_candidates: int
    reverse_moves: int
    reverse_terminal_vertices: int
    reverse_terminal_edges: int
    reverse_terminal_triangles: int
    reverse_reached_tetrahedron: bool
    normalization_improving_flips: int
    dual_edges: int
    dual_degree_histogram: tuple[tuple[int, int], ...]
    dual_bipartite: bool
    bridge_count: int
    articulation_points: tuple[int, ...]
    dual_triangle_cycles: int
    dual_four_cycles: int
    local_signature_classes: int
    local_signature_class_size_histogram: tuple[tuple[int, int], ...]
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


def _icosahedron_facets() -> tuple[Triangle, ...]:
    facets: set[Triangle] = set()
    for index in range(5):
        upper = 1 + index
        upper_next = 1 + ((index + 1) % 5)
        lower = 6 + index
        lower_next = 6 + ((index + 1) % 5)
        facets.add(tuple(sorted((0, upper, upper_next))))
        facets.add(tuple(sorted((upper, upper_next, lower))))
        facets.add(tuple(sorted((upper_next, lower_next, lower))))
        facets.add(tuple(sorted((11, lower_next, lower))))
    result = tuple(sorted(facets))
    if len(result) != 20:
        raise GluingExperimentError("G15 icosahedron seed does not have 20 facets")
    return result


def _grow_icosahedron(params: MixedSphereParameters, master_seed: bytes) -> tuple[Triangle, ...]:
    facets = set(_icosahedron_facets())
    rng = _DeterministicRng(b"MORPH-KEM G15 growth v1", master_seed + params.name.encode("ascii"))
    for step in range(params.growth_steps):
        ordered = sorted(facets)
        selected = ordered[rng.randbelow(len(ordered))]
        facets.remove(selected)
        new_vertex = 12 + step
        left, middle, right = selected
        facets.add(tuple(sorted((left, middle, new_vertex))))
        facets.add(tuple(sorted((left, right, new_vertex))))
        facets.add(tuple(sorted((middle, right, new_vertex))))
    return tuple(sorted(facets))


def _mix_facets(
    params: MixedSphereParameters,
    base_facets: tuple[Triangle, ...],
    seed: bytes,
) -> tuple[tuple[Triangle, ...], int]:
    facets = base_facets
    rng = _DeterministicRng(b"MORPH-KEM G15 edge proposals v1", seed)
    rejected = 0
    proposals = 0
    successful = 0
    proposal_cap = params.successful_flips * params.max_proposal_factor
    while successful < params.successful_flips:
        proposals += 1
        if proposals > proposal_cap:
            raise GluingExperimentError("G15 edge-flip proposal cap exhausted")
        edges = tuple(sorted(_facet_edges(facets)))
        proposed_edge = edges[rng.randbelow(len(edges))]
        legal = {flip.edge: flip for flip in _legal_flips(facets)}
        flip = legal.get(proposed_edge)
        if flip is None:
            rejected += 1
            continue
        facets = _apply_flip(facets, flip)
        successful += 1
    return facets, rejected


def _public_relabel(facets: tuple[Triangle, ...], seed: bytes) -> SimplicialComplex:
    target = SimplicialComplex.from_facets(facets)
    labels = list(range(len(target.vertices)))
    rng = _DeterministicRng(b"MORPH-KEM G15 public relabel v1", seed)
    rng.shuffle(labels)
    return target.relabel(tuple(labels))


def _degree_three_count(target: SimplicialComplex) -> int:
    histogram = dict(_primal_vertex_degree_histogram(target))
    return histogram.get(3, 0)


def validate_mixed_sphere_witness(
    public: MixedSpherePublicInstance,
    groups: tuple[TriangleGroup, ...],
):
    return validate_toroidal_hypercover_witness(public, groups)


def recover_mixed_sphere(
    public: MixedSpherePublicInstance,
    *,
    reference: MixedSphereReference | None = None,
    solution_cap: int = 64,
) -> MixedSphereRecovery:
    if solution_cap < 1 or solution_cap > 1024:
        raise GluingExperimentError("G15 exact-cover solution cap outside toy bounds")

    triangles = _triangles(public)
    adjacency, dual_edges = _triangle_dual(public)
    bridges, articulations = _bridges_and_articulations(adjacency)
    candidates = enumerate_p3_candidates(public)
    memberships, overlap_degrees, candidate_incidence = _candidate_metrics(
        len(triangles), candidates
    )
    search = _exact_cover(len(triangles), candidates, solution_cap)
    accepted = tuple(
        groups
        for groups in search.solutions
        if validate_mixed_sphere_witness(public, groups).valid
    )
    reference_groups = _normalize_groups(reference.groups) if reference is not None else None
    nonreference = sum(
        reference_groups is not None and groups != reference_groups for groups in accepted
    )

    reverse_candidates = _reverse_candidates(set(triangles))
    reverse = recover_reverse_stacking(public)
    triangle_cycles, four_cycles = _dual_short_cycles(adjacency)
    signature_classes, signature_sizes = _local_signature_metrics(public, adjacency)

    return MixedSphereRecovery(
        accepted_groups=accepted,
        growth_steps=reference.growth_steps if reference is not None else -1,
        successful_flips=reference.successful_flips if reference is not None else -1,
        rejected_flip_proposals=reference.rejected_flip_proposals if reference is not None else -1,
        generation_retries=reference.generation_retries if reference is not None else -1,
        primal_vertex_degree_histogram=_primal_vertex_degree_histogram(public.target),
        initial_degree_three_vertices=_degree_three_count(public.target),
        initial_reverse_candidates=len(reverse_candidates),
        reverse_moves=reverse.moves,
        reverse_terminal_vertices=reverse.terminal_vertices,
        reverse_terminal_edges=reverse.terminal_edges,
        reverse_terminal_triangles=reverse.terminal_triangles,
        reverse_reached_tetrahedron=reverse.reached_tetrahedron_boundary,
        normalization_improving_flips=_normalization_improving_flip_count(public.target),
        dual_edges=len(dual_edges),
        dual_degree_histogram=tuple(sorted(Counter(len(n) for n in adjacency).items())),
        dual_bipartite=_dual_is_bipartite(adjacency),
        bridge_count=len(bridges),
        articulation_points=tuple(sorted(articulations)),
        dual_triangle_cycles=triangle_cycles,
        dual_four_cycles=four_cycles,
        local_signature_classes=signature_classes,
        local_signature_class_size_histogram=signature_sizes,
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
    )


def encode_mixed_sphere_sat(public: MixedSpherePublicInstance) -> HypercoverSatEncoding:
    return encode_toroidal_hypercover_sat(public)


def decode_mixed_sphere_sat_model(
    public: MixedSpherePublicInstance,
    encoding: HypercoverSatEncoding,
    literals: tuple[int, ...],
) -> HypercoverSatModel:
    return decode_toroidal_hypercover_sat_model(public, encoding, literals)


def mixed_sphere_reference_matches(
    reference: MixedSphereReference,
    groups: tuple[TriangleGroup, ...],
) -> bool:
    return _normalize_groups(reference.groups) == _normalize_groups(groups)


def generate_mixed_sphere_instance(
    params: MixedSphereParameters,
    master_seed: bytes,
) -> tuple[MixedSpherePublicInstance, MixedSphereReference]:
    params.validate()
    if len(master_seed) < 16:
        raise GluingExperimentError("G15 master seed must contain at least 128 bits")

    base_facets = _grow_icosahedron(params, master_seed)
    for attempt in range(params.max_generation_attempts):
        mix_seed = hashlib.sha256(
            b"MORPH-KEM G15 mix attempt v1\x00"
            + master_seed
            + params.name.encode("ascii")
            + attempt.to_bytes(4, "big")
        ).digest()
        facets, rejected = _mix_facets(params, base_facets, mix_seed)
        relabel_seed = hashlib.sha256(
            b"MORPH-KEM G15 relabel attempt v1\x00"
            + master_seed
            + params.name.encode("ascii")
            + attempt.to_bytes(4, "big")
        ).digest()
        public = MixedSpherePublicInstance(
            name=params.name,
            target=_public_relabel(facets, relabel_seed),
        )
        incidence = toroidal_hypercover_incidence(public)
        if (
            incidence.triangles != params.triangle_count
            or incidence.euler_characteristic != 2
            or incidence.min_triangles_per_edge != 2
            or incidence.max_triangles_per_edge != 2
        ):
            raise GluingExperimentError("G15 mixed carrier failed closed-sphere invariants")

        candidates = enumerate_p3_candidates(public)
        secret_order = {
            candidate: hashlib.sha256(
                b"MORPH-KEM G15 reference candidate order v1\x00"
                + master_seed
                + params.name.encode("ascii")
                + attempt.to_bytes(4, "big")
                + b"".join(index.to_bytes(4, "big") for index in candidate)
            ).digest()
            for candidate in candidates
        }
        search = _exact_cover(len(_triangles(public)), candidates, 1, secret_order=secret_order)
        if not search.solutions:
            continue
        reference = MixedSphereReference(
            groups=search.solutions[0],
            growth_steps=params.growth_steps,
            successful_flips=params.successful_flips,
            rejected_flip_proposals=rejected,
            generation_retries=attempt,
        )
        if not validate_mixed_sphere_witness(public, reference.groups).valid:
            raise GluingExperimentError("G15 generated reference hypercover does not validate")
        return public, reference

    raise GluingExperimentError("G15 generation-attempt cap exhausted before P3-coverable carrier")
