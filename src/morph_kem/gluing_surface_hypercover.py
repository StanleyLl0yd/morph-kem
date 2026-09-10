from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
from itertools import combinations

from .complex import SimplicialComplex
from .gluing import GluingExperimentError
from .gluing_matching import _bridges_and_articulations
from .surface import SurfaceParameters, generate_surface_instance


Triangle = tuple[int, int, int]
TriangleGroup = tuple[int, ...]
DualEdge = tuple[int, int]


@dataclass(frozen=True, slots=True)
class ToroidalHypercoverParameters:
    name: str
    rows: int
    cols: int

    def validate(self) -> None:
        if self.rows < 3 or self.rows > 12 or self.cols < 3 or self.cols > 12:
            raise GluingExperimentError("G11 torus dimensions outside toy bounds")
        triangle_count = 2 * self.rows * self.cols
        if triangle_count % 3:
            raise GluingExperimentError("G11 triangle count must be divisible by three")


G11_PARAMETER_SETS = {
    "g11-3x6": ToroidalHypercoverParameters("g11-3x6", 3, 6),
    "g11-6x6": ToroidalHypercoverParameters("g11-6x6", 6, 6),
    "g11-6x9": ToroidalHypercoverParameters("g11-6x9", 6, 9),
}


@dataclass(frozen=True, slots=True)
class ToroidalHypercoverPublicInstance:
    name: str
    target: SimplicialComplex


@dataclass(frozen=True, slots=True)
class ToroidalHypercoverReference:
    groups: tuple[TriangleGroup, ...]


@dataclass(frozen=True, slots=True)
class ToroidalHypercoverIncidence:
    vertices: int
    edges: int
    triangles: int
    euler_characteristic: int
    min_triangles_per_edge: int
    max_triangles_per_edge: int


@dataclass(frozen=True, slots=True)
class ToroidalHypercoverValidation:
    valid: bool
    reason: str
    piece_count: int


@dataclass(frozen=True, slots=True)
class ToroidalHypercoverRecovery:
    accepted_groups: tuple[tuple[TriangleGroup, ...], ...]
    dual_edges: int
    dual_degree_histogram: tuple[tuple[int, int], ...]
    bridge_count: int
    articulation_points: tuple[int, ...]
    bipartition_sizes: tuple[int, int]
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
class HypercoverSatEncoding:
    candidates: tuple[TriangleGroup, ...]
    clauses: tuple[tuple[int, ...], ...]

    @property
    def variable_count(self) -> int:
        return len(self.candidates)

    def to_dimacs(self) -> str:
        lines = [f"p cnf {self.variable_count} {len(self.clauses)}"]
        lines.extend(" ".join(map(str, clause)) + " 0" for clause in self.clauses)
        return "\n".join(lines) + "\n"


@dataclass(frozen=True, slots=True)
class HypercoverSatModel:
    groups: tuple[TriangleGroup, ...]
    validation: ToroidalHypercoverValidation


@dataclass(frozen=True, slots=True)
class _CoverSearch:
    solutions: tuple[tuple[TriangleGroup, ...], ...]
    nodes: int
    decisions: int
    backtracks: int


def _triangles(public: ToroidalHypercoverPublicInstance) -> tuple[Triangle, ...]:
    return tuple(sorted(simplex for simplex in public.target.simplices if len(simplex) == 3))


def _normalize_groups(groups: tuple[TriangleGroup, ...]) -> tuple[TriangleGroup, ...]:
    return tuple(sorted(tuple(sorted(group)) for group in groups))


def _edge_owners(
    public: ToroidalHypercoverPublicInstance,
) -> dict[tuple[int, int], tuple[int, ...]]:
    owners: dict[tuple[int, int], list[int]] = defaultdict(list)
    for triangle_index, triangle in enumerate(_triangles(public)):
        for edge in combinations(triangle, 2):
            owners[tuple(sorted(edge))].append(triangle_index)
    return {edge: tuple(sorted(indices)) for edge, indices in owners.items()}


def toroidal_hypercover_incidence(
    public: ToroidalHypercoverPublicInstance,
) -> ToroidalHypercoverIncidence:
    owners = _edge_owners(public)
    counts = [len(indices) for indices in owners.values()]
    vertices = sum(len(simplex) == 1 for simplex in public.target.simplices)
    edges = sum(len(simplex) == 2 for simplex in public.target.simplices)
    triangles = sum(len(simplex) == 3 for simplex in public.target.simplices)
    return ToroidalHypercoverIncidence(
        vertices=vertices,
        edges=edges,
        triangles=triangles,
        euler_characteristic=vertices - edges + triangles,
        min_triangles_per_edge=min(counts),
        max_triangles_per_edge=max(counts),
    )


def _triangle_dual(
    public: ToroidalHypercoverPublicInstance,
) -> tuple[list[list[int]], tuple[DualEdge, ...]]:
    triangles = _triangles(public)
    owners = _edge_owners(public)
    public_edge_count = sum(len(simplex) == 2 for simplex in public.target.simplices)
    if len(owners) != public_edge_count:
        raise GluingExperimentError("G11 edge incidence does not cover public 1-skeleton")
    if any(len(indices) != 2 for indices in owners.values()):
        raise GluingExperimentError("G11 public surface is not closed at an edge")

    adjacency = [set() for _ in triangles]
    dual_edges: set[DualEdge] = set()
    for indices in owners.values():
        left, right = indices
        edge = tuple(sorted((left, right)))
        dual_edges.add(edge)
        adjacency[left].add(right)
        adjacency[right].add(left)
    return [sorted(neighbors) for neighbors in adjacency], tuple(sorted(dual_edges))


def _bipartition(adjacency: list[list[int]]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    colors = [-1] * len(adjacency)
    components = 0
    for root in range(len(adjacency)):
        if colors[root] >= 0:
            continue
        components += 1
        colors[root] = 0
        queue = [root]
        while queue:
            current = queue.pop(0)
            for neighbor in adjacency[current]:
                if colors[neighbor] < 0:
                    colors[neighbor] = colors[current] ^ 1
                    queue.append(neighbor)
                elif colors[neighbor] == colors[current]:
                    raise GluingExperimentError("G11 public triangle dual graph is not bipartite")
    if components != 1:
        raise GluingExperimentError("G11 public triangle dual graph is disconnected")
    left = tuple(index for index, color in enumerate(colors) if color == 0)
    right = tuple(index for index, color in enumerate(colors) if color == 1)
    return left, right


def _allowed_p3(
    public: ToroidalHypercoverPublicInstance,
    group: TriangleGroup,
) -> bool:
    if len(group) != 3 or len(set(group)) != 3:
        return False
    triangles = _triangles(public)
    if any(index < 0 or index >= len(triangles) for index in group):
        return False

    selected = [triangles[index] for index in group]
    shared_edges = 0
    local_degrees = [0, 0, 0]
    for left_index, right_index in combinations(range(3), 2):
        if len(set(selected[left_index]) & set(selected[right_index])) == 2:
            shared_edges += 1
            local_degrees[left_index] += 1
            local_degrees[right_index] += 1
    if shared_edges != 2 or sorted(local_degrees) != [1, 1, 2]:
        return False

    vertices = set().union(*(set(triangle) for triangle in selected))
    edge_counts: Counter[tuple[int, int]] = Counter()
    for triangle in selected:
        for edge in combinations(triangle, 2):
            edge_counts[tuple(sorted(edge))] += 1
    boundary_edges = sum(count == 1 for count in edge_counts.values())
    return (
        len(vertices) == 5
        and len(edge_counts) == 7
        and boundary_edges == 5
        and len(vertices) - len(edge_counts) + len(selected) == 1
    )


def enumerate_p3_candidates(
    public: ToroidalHypercoverPublicInstance,
) -> tuple[TriangleGroup, ...]:
    adjacency, _ = _triangle_dual(public)
    candidates: set[TriangleGroup] = set()
    for center, neighbors in enumerate(adjacency):
        for left, right in combinations(neighbors, 2):
            candidate = tuple(sorted((left, center, right)))
            if _allowed_p3(public, candidate):
                candidates.add(candidate)
    return tuple(sorted(candidates))


def _candidate_metrics(
    triangle_count: int,
    candidates: tuple[TriangleGroup, ...],
) -> tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...], int]:
    memberships = [0] * triangle_count
    candidate_sets = [frozenset(candidate) for candidate in candidates]
    for candidate in candidates:
        for triangle in candidate:
            memberships[triangle] += 1

    overlap_degrees: list[int] = []
    for index, candidate in enumerate(candidate_sets):
        overlap_degrees.append(
            sum(
                1
                for other_index, other in enumerate(candidate_sets)
                if index != other_index and candidate & other
            )
        )
    return (
        tuple(sorted(Counter(memberships).items())),
        tuple(sorted(Counter(overlap_degrees).items())),
        sum(memberships),
    )


def validate_toroidal_hypercover_witness(
    public: ToroidalHypercoverPublicInstance,
    groups: tuple[TriangleGroup, ...],
) -> ToroidalHypercoverValidation:
    triangles = _triangles(public)
    normalized = _normalize_groups(groups)
    expected_pieces = len(triangles) // 3
    if len(triangles) % 3 or len(normalized) != expected_pieces:
        return ToroidalHypercoverValidation(False, "wrong G11 piece count", len(normalized))
    flattened = [triangle for group in normalized for triangle in group]
    if sorted(flattened) != list(range(len(triangles))):
        return ToroidalHypercoverValidation(
            False, "G11 groups do not partition public triangles", len(normalized)
        )
    if not all(_allowed_p3(public, group) for group in normalized):
        return ToroidalHypercoverValidation(False, "invalid G11 P3-surface piece", len(normalized))
    return ToroidalHypercoverValidation(True, "accepted", len(normalized))


def _exact_cover(
    triangle_count: int,
    candidates: tuple[TriangleGroup, ...],
    solution_cap: int,
    *,
    secret_order: dict[TriangleGroup, bytes] | None = None,
) -> _CoverSearch:
    candidate_sets = [frozenset(candidate) for candidate in candidates]
    by_triangle: list[list[int]] = [[] for _ in range(triangle_count)]
    for candidate_index, candidate in enumerate(candidates):
        for triangle in candidate:
            by_triangle[triangle].append(candidate_index)

    solutions: list[tuple[TriangleGroup, ...]] = []
    nodes = 0
    decisions = 0
    backtracks = 0

    def search(uncovered: frozenset[int], chosen: tuple[int, ...]) -> None:
        nonlocal nodes, decisions, backtracks
        if len(solutions) >= solution_cap:
            return
        nodes += 1
        if not uncovered:
            solutions.append(_normalize_groups(tuple(candidates[index] for index in chosen)))
            return

        options_by_triangle: list[tuple[int, int, list[int]]] = []
        for triangle in uncovered:
            options = [
                candidate_index
                for candidate_index in by_triangle[triangle]
                if candidate_sets[candidate_index] <= uncovered
            ]
            options_by_triangle.append((len(options), triangle, options))
        _, _, options = min(options_by_triangle, key=lambda item: (item[0], item[1]))
        if not options:
            backtracks += 1
            return
        if len(options) > 1:
            decisions += 1

        if secret_order is None:
            options.sort(key=lambda index: candidates[index])
        else:
            options.sort(key=lambda index: (secret_order[candidates[index]], candidates[index]))

        before = len(solutions)
        for candidate_index in options:
            search(uncovered - candidate_sets[candidate_index], chosen + (candidate_index,))
            if len(solutions) >= solution_cap:
                return
        if len(solutions) == before:
            backtracks += 1

    search(frozenset(range(triangle_count)), ())
    return _CoverSearch(tuple(solutions), nodes, decisions, backtracks)


def recover_toroidal_hypercover(
    public: ToroidalHypercoverPublicInstance,
    *,
    reference: ToroidalHypercoverReference | None = None,
    solution_cap: int = 64,
) -> ToroidalHypercoverRecovery:
    if solution_cap < 1 or solution_cap > 1024:
        raise GluingExperimentError("G11 exact-cover solution cap outside toy bounds")

    triangles = _triangles(public)
    adjacency, dual_edges = _triangle_dual(public)
    left, right = _bipartition(adjacency)
    bridges, articulations = _bridges_and_articulations(adjacency)
    degree_histogram = tuple(sorted(Counter(len(neighbors) for neighbors in adjacency).items()))
    candidates = enumerate_p3_candidates(public)
    memberships, overlap_degrees, candidate_incidence = _candidate_metrics(
        len(triangles), candidates
    )
    search = _exact_cover(len(triangles), candidates, solution_cap)
    accepted = tuple(
        groups
        for groups in search.solutions
        if validate_toroidal_hypercover_witness(public, groups).valid
    )
    reference_groups = _normalize_groups(reference.groups) if reference is not None else None
    nonreference = sum(
        reference_groups is not None and groups != reference_groups for groups in accepted
    )
    return ToroidalHypercoverRecovery(
        accepted_groups=accepted,
        dual_edges=len(dual_edges),
        dual_degree_histogram=degree_histogram,
        bridge_count=len(bridges),
        articulation_points=tuple(sorted(articulations)),
        bipartition_sizes=(len(left), len(right)),
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


def encode_toroidal_hypercover_sat(
    public: ToroidalHypercoverPublicInstance,
) -> HypercoverSatEncoding:
    triangles = _triangles(public)
    candidates = enumerate_p3_candidates(public)
    by_triangle: list[list[int]] = [[] for _ in triangles]
    for candidate_index, candidate in enumerate(candidates, start=1):
        for triangle in candidate:
            by_triangle[triangle].append(candidate_index)

    clauses: list[tuple[int, ...]] = []
    for options in by_triangle:
        if not options:
            raise GluingExperimentError("G11 SAT encoding found uncovered triangle")
        clauses.append(tuple(options))
        clauses.extend((-left, -right) for left, right in combinations(options, 2))
    return HypercoverSatEncoding(candidates=candidates, clauses=tuple(clauses))


def decode_toroidal_hypercover_sat_model(
    public: ToroidalHypercoverPublicInstance,
    encoding: HypercoverSatEncoding,
    literals: tuple[int, ...],
) -> HypercoverSatModel:
    positive = {literal for literal in literals if literal > 0}
    groups = _normalize_groups(
        tuple(
            candidate
            for candidate_index, candidate in enumerate(encoding.candidates, start=1)
            if candidate_index in positive
        )
    )
    return HypercoverSatModel(
        groups=groups,
        validation=validate_toroidal_hypercover_witness(public, groups),
    )


def toroidal_hypercover_reference_matches(
    reference: ToroidalHypercoverReference,
    groups: tuple[TriangleGroup, ...],
) -> bool:
    return _normalize_groups(reference.groups) == _normalize_groups(groups)


def generate_toroidal_hypercover_instance(
    params: ToroidalHypercoverParameters,
    master_seed: bytes,
) -> tuple[ToroidalHypercoverPublicInstance, ToroidalHypercoverReference]:
    params.validate()
    if len(master_seed) < 16:
        raise GluingExperimentError("G11 master seed must contain at least 128 bits")

    surface_seed = hashlib.sha256(
        b"MORPH-KEM G11 torus v1\x00" + master_seed + params.name.encode("ascii")
    ).digest()
    surface_public, _ = generate_surface_instance(
        SurfaceParameters(params.name + "-surface", params.rows, params.cols),
        surface_seed,
    )
    public = ToroidalHypercoverPublicInstance(name=params.name, target=surface_public.target)
    triangles = _triangles(public)
    candidates = enumerate_p3_candidates(public)

    secret_order = {
        candidate: hashlib.sha256(
            b"MORPH-KEM G11 reference candidate order v1\x00"
            + master_seed
            + params.name.encode("ascii")
            + b"".join(index.to_bytes(4, "big") for index in candidate)
        ).digest()
        for candidate in candidates
    }
    search = _exact_cover(len(triangles), candidates, 1, secret_order=secret_order)
    if not search.solutions:
        raise GluingExperimentError("G11 generated torus has no P3 exact cover")
    reference = ToroidalHypercoverReference(groups=search.solutions[0])

    incidence = toroidal_hypercover_incidence(public)
    adjacency, _ = _triangle_dual(public)
    memberships, _, _ = _candidate_metrics(len(triangles), candidates)
    if incidence.euler_characteristic != 0:
        raise GluingExperimentError("G11 generated surface is not toroidal by Euler characteristic")
    if incidence.min_triangles_per_edge != 2 or incidence.max_triangles_per_edge != 2:
        raise GluingExperimentError("G11 generated surface is not closed")
    if any(len(neighbors) != 3 for neighbors in adjacency):
        raise GluingExperimentError("G11 triangle dual graph is not 3-regular")
    if len(candidates) != 3 * len(triangles):
        raise GluingExperimentError("G11 P3 candidate count differs from torus control")
    if memberships != ((9, len(triangles)),):
        raise GluingExperimentError("G11 candidate membership profile differs from torus control")
    if not validate_toroidal_hypercover_witness(public, reference.groups).valid:
        raise GluingExperimentError("G11 generated reference hypercover does not validate")

    return public, reference
