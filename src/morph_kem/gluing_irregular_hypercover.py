from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
from itertools import combinations
from math import comb

from .complex import SimplicialComplex
from .gluing import GluingExperimentError, _DeterministicRng
from .gluing_matching import _bridges_and_articulations
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
from .surface import SurfaceParameters, generate_surface_instance


@dataclass(frozen=True, slots=True)
class IrregularHypercoverParameters:
    name: str
    rows: int
    cols: int
    successful_flips: int
    max_generation_attempts: int = 16

    def validate(self) -> None:
        if self.rows < 4 or self.rows > 12 or self.cols < 4 or self.cols > 12:
            raise GluingExperimentError("G12 torus dimensions outside toy bounds")
        triangle_count = 2 * self.rows * self.cols
        if triangle_count % 3:
            raise GluingExperimentError("G12 triangle count must be divisible by three")
        if self.successful_flips < 1 or self.successful_flips > triangle_count:
            raise GluingExperimentError("G12 successful-flip target outside toy bounds")
        if self.max_generation_attempts < 1 or self.max_generation_attempts > 64:
            raise GluingExperimentError("G12 generation-attempt cap outside toy bounds")


G12_PARAMETER_SETS = {
    "g12-6x6": IrregularHypercoverParameters("g12-6x6", 6, 6, 36),
    "g12-6x9": IrregularHypercoverParameters("g12-6x9", 6, 9, 54),
    "g12-8x9": IrregularHypercoverParameters("g12-8x9", 8, 9, 72),
}


IrregularHypercoverPublicInstance = ToroidalHypercoverPublicInstance


@dataclass(frozen=True, slots=True)
class IrregularHypercoverReference:
    groups: tuple[TriangleGroup, ...]
    successful_flips: int
    generation_retries: int


@dataclass(frozen=True, slots=True)
class IrregularHypercoverRecovery:
    accepted_groups: tuple[tuple[TriangleGroup, ...], ...]
    successful_flips: int
    generation_retries: int
    primal_vertex_degree_histogram: tuple[tuple[int, int], ...]
    dual_edges: int
    dual_degree_histogram: tuple[tuple[int, int], ...]
    dual_bipartite: bool
    bridge_count: int
    articulation_points: tuple[int, ...]
    dual_triangle_cycles: int
    dual_four_cycles: int
    local_signature_classes: int
    local_signature_class_size_histogram: tuple[tuple[int, int], ...]
    normalization_improving_flips: int
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


@dataclass(frozen=True, slots=True)
class _Flip:
    edge: tuple[int, int]
    opposite: tuple[int, int]
    old_triangles: tuple[Triangle, Triangle]
    new_triangles: tuple[Triangle, Triangle]


def _facets(target: SimplicialComplex) -> tuple[Triangle, ...]:
    return tuple(sorted(simplex for simplex in target.simplices if len(simplex) == 3))


def _facet_edges(facets: tuple[Triangle, ...]) -> set[tuple[int, int]]:
    return {
        tuple(sorted(edge))
        for triangle in facets
        for edge in combinations(triangle, 2)
    }


def _legal_flips(facets: tuple[Triangle, ...]) -> tuple[_Flip, ...]:
    owners: dict[tuple[int, int], list[Triangle]] = defaultdict(list)
    for triangle in facets:
        for edge in combinations(triangle, 2):
            owners[tuple(sorted(edge))].append(triangle)
    edge_set = set(owners)
    facet_set = set(facets)
    result: list[_Flip] = []
    for edge, adjacent in sorted(owners.items()):
        if len(adjacent) != 2:
            continue
        left, right = sorted(adjacent)
        edge_set_local = set(edge)
        left_opposite = tuple(vertex for vertex in left if vertex not in edge_set_local)
        right_opposite = tuple(vertex for vertex in right if vertex not in edge_set_local)
        if len(left_opposite) != 1 or len(right_opposite) != 1:
            continue
        c = left_opposite[0]
        d = right_opposite[0]
        if c == d:
            continue
        opposite = tuple(sorted((c, d)))
        if opposite in edge_set:
            continue
        a, b = edge
        first = tuple(sorted((a, c, d)))
        second = tuple(sorted((b, c, d)))
        if len(set(first)) != 3 or len(set(second)) != 3 or first == second:
            continue
        remaining = facet_set - {left, right}
        if first in remaining or second in remaining:
            continue
        result.append(
            _Flip(
                edge=edge,
                opposite=opposite,
                old_triangles=(left, right),
                new_triangles=tuple(sorted((first, second))),
            )
        )
    return tuple(result)


def _apply_flip(facets: tuple[Triangle, ...], flip: _Flip) -> tuple[Triangle, ...]:
    values = set(facets)
    for triangle in flip.old_triangles:
        values.remove(triangle)
    values.update(flip.new_triangles)
    return tuple(sorted(values))


def _flip_surface(
    target: SimplicialComplex,
    successful_flips: int,
    seed: bytes,
) -> SimplicialComplex:
    facets = _facets(target)
    rng = _DeterministicRng(b"MORPH-KEM G12 edge flips v1", seed)
    for _ in range(successful_flips):
        legal = _legal_flips(facets)
        if not legal:
            raise GluingExperimentError("G12 edge-flip walk reached a state with no legal flip")
        facets = _apply_flip(facets, legal[rng.randbelow(len(legal))])
    return SimplicialComplex.from_facets(facets)


def _final_relabel(target: SimplicialComplex, seed: bytes) -> SimplicialComplex:
    labels = list(range(len(target.vertices)))
    rng = _DeterministicRng(b"MORPH-KEM G12 final public relabel v1", seed)
    rng.shuffle(labels)
    return target.relabel(tuple(labels))


def _primal_vertex_degrees(target: SimplicialComplex) -> dict[int, int]:
    adjacency: dict[int, set[int]] = {vertex: set() for vertex in target.vertices}
    for edge in (simplex for simplex in target.simplices if len(simplex) == 2):
        left, right = edge
        adjacency[left].add(right)
        adjacency[right].add(left)
    return {vertex: len(neighbors) for vertex, neighbors in adjacency.items()}


def _primal_vertex_degree_histogram(target: SimplicialComplex) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(_primal_vertex_degrees(target).values()).items()))


def _dual_is_bipartite(adjacency: list[list[int]]) -> bool:
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


def _dual_short_cycles(adjacency: list[list[int]]) -> tuple[int, int]:
    neighbor_sets = [set(neighbors) for neighbors in adjacency]
    triangle_cycles = sum(
        1
        for left in range(len(adjacency))
        for right in adjacency[left]
        if left < right
        for third in neighbor_sets[left] & neighbor_sets[right]
        if right < third
    )
    four_twice = 0
    for left in range(len(adjacency)):
        for right in range(left + 1, len(adjacency)):
            common = len(neighbor_sets[left] & neighbor_sets[right])
            if common >= 2:
                four_twice += comb(common, 2)
    return triangle_cycles, four_twice // 2


def _local_signature_metrics(
    public: IrregularHypercoverPublicInstance,
    adjacency: list[list[int]],
) -> tuple[int, tuple[tuple[int, int], ...]]:
    triangles = _triangles(public)
    degrees = _primal_vertex_degrees(public.target)
    neighbor_sets = [set(neighbors) for neighbors in adjacency]
    signatures: list[tuple[tuple[int, int, int], int, int, int]] = []
    for index, triangle in enumerate(triangles):
        primal = tuple(sorted(degrees[vertex] for vertex in triangle))
        radius_one = neighbor_sets[index]
        radius_one_internal = sum(
            1
            for left, right in combinations(sorted(radius_one), 2)
            if right in neighbor_sets[left]
        )
        radius_two = {index} | set(radius_one)
        for neighbor in radius_one:
            radius_two.update(neighbor_sets[neighbor])
        radius_two_edges = sum(
            1
            for left in radius_two
            for right in adjacency[left]
            if left < right and right in radius_two
        )
        signatures.append((primal, radius_one_internal, len(radius_two), radius_two_edges))
    classes = Counter(signatures)
    size_histogram = tuple(sorted(Counter(classes.values()).items()))
    return len(classes), size_histogram


def _normalization_improving_flip_count(target: SimplicialComplex) -> int:
    facets = _facets(target)
    degrees = _primal_vertex_degrees(target)
    score = sum((degree - 6) ** 2 for degree in degrees.values())
    improving = 0
    for flip in _legal_flips(facets):
        changed = dict(degrees)
        a, b = flip.edge
        c, d = flip.opposite
        changed[a] -= 1
        changed[b] -= 1
        changed[c] += 1
        changed[d] += 1
        new_score = sum((degree - 6) ** 2 for degree in changed.values())
        improving += int(new_score < score)
    return improving


def validate_irregular_hypercover_witness(
    public: IrregularHypercoverPublicInstance,
    groups: tuple[TriangleGroup, ...],
):
    return validate_toroidal_hypercover_witness(public, groups)


def recover_irregular_hypercover(
    public: IrregularHypercoverPublicInstance,
    *,
    reference: IrregularHypercoverReference | None = None,
    solution_cap: int = 64,
) -> IrregularHypercoverRecovery:
    if solution_cap < 1 or solution_cap > 1024:
        raise GluingExperimentError("G12 exact-cover solution cap outside toy bounds")
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
        if validate_irregular_hypercover_witness(public, groups).valid
    )
    reference_groups = _normalize_groups(reference.groups) if reference is not None else None
    nonreference = sum(
        reference_groups is not None and groups != reference_groups for groups in accepted
    )
    triangle_cycles, four_cycles = _dual_short_cycles(adjacency)
    signature_classes, signature_sizes = _local_signature_metrics(public, adjacency)
    return IrregularHypercoverRecovery(
        accepted_groups=accepted,
        successful_flips=reference.successful_flips if reference is not None else -1,
        generation_retries=reference.generation_retries if reference is not None else -1,
        primal_vertex_degree_histogram=_primal_vertex_degree_histogram(public.target),
        dual_edges=len(dual_edges),
        dual_degree_histogram=tuple(sorted(Counter(len(n) for n in adjacency).items())),
        dual_bipartite=_dual_is_bipartite(adjacency),
        bridge_count=len(bridges),
        articulation_points=tuple(sorted(articulations)),
        dual_triangle_cycles=triangle_cycles,
        dual_four_cycles=four_cycles,
        local_signature_classes=signature_classes,
        local_signature_class_size_histogram=signature_sizes,
        normalization_improving_flips=_normalization_improving_flip_count(public.target),
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


def encode_irregular_hypercover_sat(
    public: IrregularHypercoverPublicInstance,
) -> HypercoverSatEncoding:
    return encode_toroidal_hypercover_sat(public)


def decode_irregular_hypercover_sat_model(
    public: IrregularHypercoverPublicInstance,
    encoding: HypercoverSatEncoding,
    literals: tuple[int, ...],
) -> HypercoverSatModel:
    return decode_toroidal_hypercover_sat_model(public, encoding, literals)


def irregular_hypercover_reference_matches(
    reference: IrregularHypercoverReference,
    groups: tuple[TriangleGroup, ...],
) -> bool:
    return _normalize_groups(reference.groups) == _normalize_groups(groups)


def generate_irregular_hypercover_instance(
    params: IrregularHypercoverParameters,
    master_seed: bytes,
) -> tuple[IrregularHypercoverPublicInstance, IrregularHypercoverReference]:
    params.validate()
    if len(master_seed) < 16:
        raise GluingExperimentError("G12 master seed must contain at least 128 bits")

    base_seed = hashlib.sha256(
        b"MORPH-KEM G12 base torus v1\x00" + master_seed + params.name.encode("ascii")
    ).digest()
    base_public, _ = generate_surface_instance(
        SurfaceParameters(params.name + "-base", params.rows, params.cols), base_seed
    )

    for attempt in range(params.max_generation_attempts):
        flip_seed = hashlib.sha256(
            b"MORPH-KEM G12 flip attempt v1\x00"
            + master_seed
            + params.name.encode("ascii")
            + attempt.to_bytes(4, "big")
        ).digest()
        irregular = _flip_surface(base_public.target, params.successful_flips, flip_seed)
        relabel_seed = hashlib.sha256(
            b"MORPH-KEM G12 final relabel seed v1\x00"
            + master_seed
            + params.name.encode("ascii")
            + attempt.to_bytes(4, "big")
        ).digest()
        irregular = _final_relabel(irregular, relabel_seed)
        public = IrregularHypercoverPublicInstance(name=params.name, target=irregular)
        incidence = toroidal_hypercover_incidence(public)
        adjacency, _ = _triangle_dual(public)
        candidates = enumerate_p3_candidates(public)
        if incidence.euler_characteristic != 0:
            raise GluingExperimentError("G12 edge flips changed Euler characteristic")
        if incidence.min_triangles_per_edge != 2 or incidence.max_triangles_per_edge != 2:
            raise GluingExperimentError("G12 edge flips broke closed-surface incidence")
        if any(len(neighbors) != 3 for neighbors in adjacency):
            raise GluingExperimentError("G12 triangle dual graph is not 3-regular")
        degree_histogram = _primal_vertex_degree_histogram(public.target)
        signature_classes, _ = _local_signature_metrics(public, adjacency)
        if len(degree_histogram) <= 1 or signature_classes <= 1:
            continue

        secret_order = {
            candidate: hashlib.sha256(
                b"MORPH-KEM G12 reference candidate order v1\x00"
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
        reference = IrregularHypercoverReference(
            groups=search.solutions[0],
            successful_flips=params.successful_flips,
            generation_retries=attempt,
        )
        if not validate_irregular_hypercover_witness(public, reference.groups).valid:
            raise GluingExperimentError("G12 generated reference hypercover does not validate")
        return public, reference

    raise GluingExperimentError("G12 generation-attempt cap exhausted before satisfiable irregular cover")
