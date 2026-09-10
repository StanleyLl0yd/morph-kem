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
class ToroidalMatchingParameters:
    name: str
    rows: int
    cols: int

    def validate(self) -> None:
        if self.rows < 4 or self.rows > 16 or self.cols < 4 or self.cols > 16:
            raise GluingExperimentError("G10 torus dimensions outside toy bounds")
        if self.rows % 2 or self.cols % 2:
            raise GluingExperimentError("G10 calibration uses even torus dimensions")


G10_PARAMETER_SETS = {
    "g10-4x4": ToroidalMatchingParameters("g10-4x4", 4, 4),
    "g10-6x6": ToroidalMatchingParameters("g10-6x6", 6, 6),
    "g10-8x8": ToroidalMatchingParameters("g10-8x8", 8, 8),
}


@dataclass(frozen=True, slots=True)
class ToroidalMatchingPublicInstance:
    name: str
    target: SimplicialComplex


@dataclass(frozen=True, slots=True)
class ToroidalMatchingReference:
    groups: tuple[TriangleGroup, ...]


@dataclass(frozen=True, slots=True)
class ToroidalMatchingIncidence:
    vertices: int
    edges: int
    triangles: int
    euler_characteristic: int
    min_triangles_per_edge: int
    max_triangles_per_edge: int


@dataclass(frozen=True, slots=True)
class ToroidalMatchingValidation:
    valid: bool
    reason: str
    piece_count: int


@dataclass(frozen=True, slots=True)
class ToroidalMatchingRecovery:
    accepted_groups: tuple[tuple[TriangleGroup, ...], ...]
    dual_edges: int
    dual_degree_histogram: tuple[tuple[int, int], ...]
    bridge_count: int
    articulation_points: tuple[int, ...]
    bipartition_sizes: tuple[int, int]
    candidate_edges: int
    base_augmentations: int
    base_dfs_calls: int
    base_edge_scans: int
    alternative_attempts: int
    alternative_matching_edge_scans: int
    matching_solutions: int
    matching_solution_cap: int
    matching_cap_hit: bool
    accepted_solutions: int
    nonreference_accepted_solutions: int


@dataclass(frozen=True, slots=True)
class _MatchingResult:
    groups: tuple[TriangleGroup, ...]
    perfect: bool
    augmentations: int
    dfs_calls: int
    edge_scans: int


def _triangles(public: ToroidalMatchingPublicInstance) -> tuple[Triangle, ...]:
    return tuple(sorted(simplex for simplex in public.target.simplices if len(simplex) == 3))


def _normalize_groups(groups: tuple[TriangleGroup, ...]) -> tuple[TriangleGroup, ...]:
    return tuple(sorted(tuple(sorted(group)) for group in groups))


def _edge_owners(public: ToroidalMatchingPublicInstance) -> dict[tuple[int, int], tuple[int, ...]]:
    owners: dict[tuple[int, int], list[int]] = defaultdict(list)
    for triangle_index, triangle in enumerate(_triangles(public)):
        for edge in combinations(triangle, 2):
            owners[tuple(sorted(edge))].append(triangle_index)
    return {edge: tuple(sorted(indices)) for edge, indices in owners.items()}


def toroidal_matching_incidence(public: ToroidalMatchingPublicInstance) -> ToroidalMatchingIncidence:
    owners = _edge_owners(public)
    counts = [len(indices) for indices in owners.values()]
    vertices = sum(len(simplex) == 1 for simplex in public.target.simplices)
    edges = sum(len(simplex) == 2 for simplex in public.target.simplices)
    triangles = sum(len(simplex) == 3 for simplex in public.target.simplices)
    return ToroidalMatchingIncidence(
        vertices=vertices,
        edges=edges,
        triangles=triangles,
        euler_characteristic=vertices - edges + triangles,
        min_triangles_per_edge=min(counts),
        max_triangles_per_edge=max(counts),
    )


def _triangle_dual(
    public: ToroidalMatchingPublicInstance,
) -> tuple[list[list[int]], tuple[DualEdge, ...]]:
    triangles = _triangles(public)
    owners = _edge_owners(public)
    if len(owners) != sum(len(simplex) == 2 for simplex in public.target.simplices):
        raise GluingExperimentError("G10 edge incidence does not cover the public 1-skeleton")
    if any(len(indices) != 2 for indices in owners.values()):
        raise GluingExperimentError("G10 public surface is not closed at an edge")

    adjacency = [set() for _ in triangles]
    edges: set[DualEdge] = set()
    for indices in owners.values():
        left, right = indices
        edge = tuple(sorted((left, right)))
        edges.add(edge)
        adjacency[left].add(right)
        adjacency[right].add(left)
    return [sorted(neighbors) for neighbors in adjacency], tuple(sorted(edges))


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
                    raise GluingExperimentError("G10 public triangle dual graph is not bipartite")
    if components != 1:
        raise GluingExperimentError("G10 public triangle dual graph is disconnected")
    left = tuple(index for index, color in enumerate(colors) if color == 0)
    right = tuple(index for index, color in enumerate(colors) if color == 1)
    return left, right


def _allowed_pair(public: ToroidalMatchingPublicInstance, group: TriangleGroup) -> bool:
    if len(group) != 2 or len(set(group)) != 2:
        return False
    triangles = _triangles(public)
    if any(index < 0 or index >= len(triangles) for index in group):
        return False
    left = set(triangles[group[0]])
    right = set(triangles[group[1]])
    return len(left & right) == 2 and len(left | right) == 4


def validate_toroidal_matching_witness(
    public: ToroidalMatchingPublicInstance,
    groups: tuple[TriangleGroup, ...],
) -> ToroidalMatchingValidation:
    triangles = _triangles(public)
    normalized = _normalize_groups(groups)
    if len(normalized) != len(triangles) // 2:
        return ToroidalMatchingValidation(False, "wrong G10 piece count", len(normalized))
    flattened = [triangle for group in normalized for triangle in group]
    if sorted(flattened) != list(range(len(triangles))):
        return ToroidalMatchingValidation(False, "G10 groups do not partition public triangles", len(normalized))
    if not all(_allowed_pair(public, group) for group in normalized):
        return ToroidalMatchingValidation(False, "invalid G10 adjacent-triangle piece", len(normalized))
    return ToroidalMatchingValidation(True, "accepted", len(normalized))


def _perfect_matching(
    adjacency: list[list[int]],
    left: tuple[int, ...],
    right: tuple[int, ...],
    forced_edge: DualEdge | None = None,
) -> _MatchingResult:
    left_set = set(left)
    right_set = set(right)
    match_right: dict[int, int] = {}
    forced_left: int | None = None
    forced_right: int | None = None
    augmentations = 0
    dfs_calls = 0
    edge_scans = 0

    if forced_edge is not None:
        a, b = forced_edge
        if a in left_set and b in right_set:
            forced_left, forced_right = a, b
        elif b in left_set and a in right_set:
            forced_left, forced_right = b, a
        else:
            return _MatchingResult((), False, 0, 0, 0)
        if forced_right not in adjacency[forced_left]:
            return _MatchingResult((), False, 0, 0, 0)
        match_right[forced_right] = forced_left
        augmentations = 1

    def augment(left_vertex: int, seen_right: set[int]) -> bool:
        nonlocal dfs_calls, edge_scans
        dfs_calls += 1
        for right_vertex in adjacency[left_vertex]:
            edge_scans += 1
            if right_vertex not in right_set or right_vertex in seen_right:
                continue
            if forced_right is not None and right_vertex == forced_right:
                continue
            seen_right.add(right_vertex)
            owner = match_right.get(right_vertex)
            if owner is None or augment(owner, seen_right):
                match_right[right_vertex] = left_vertex
                return True
        return False

    for left_vertex in left:
        if left_vertex == forced_left:
            continue
        if not augment(left_vertex, set()):
            return _MatchingResult((), False, augmentations, dfs_calls, edge_scans)
        augmentations += 1

    if len(match_right) != len(left) or len(left) != len(right):
        return _MatchingResult((), False, augmentations, dfs_calls, edge_scans)
    groups = _normalize_groups(
        tuple((left_vertex, right_vertex) for right_vertex, left_vertex in match_right.items())
    )
    return _MatchingResult(groups, True, augmentations, dfs_calls, edge_scans)


def _matching_family(
    adjacency: list[list[int]],
    dual_edges: tuple[DualEdge, ...],
    left: tuple[int, ...],
    right: tuple[int, ...],
    solution_cap: int,
) -> tuple[tuple[tuple[TriangleGroup, ...], ...], _MatchingResult, int, int]:
    base = _perfect_matching(adjacency, left, right)
    if not base.perfect:
        return (), base, 0, 0
    solutions: set[tuple[TriangleGroup, ...]] = {base.groups}
    base_edges = {tuple(group) for group in base.groups}
    attempts = 0
    alternative_scans = 0
    for edge in dual_edges:
        if tuple(edge) in base_edges:
            continue
        attempts += 1
        result = _perfect_matching(adjacency, left, right, forced_edge=edge)
        alternative_scans += result.edge_scans
        if result.perfect:
            solutions.add(result.groups)
        if len(solutions) >= solution_cap:
            break
    return tuple(sorted(solutions)), base, attempts, alternative_scans


def recover_toroidal_matching(
    public: ToroidalMatchingPublicInstance,
    *,
    reference: ToroidalMatchingReference | None = None,
    solution_cap: int = 64,
) -> ToroidalMatchingRecovery:
    if solution_cap < 1 or solution_cap > 1024:
        raise GluingExperimentError("G10 matching solution cap outside toy bounds")
    adjacency, dual_edges = _triangle_dual(public)
    left, right = _bipartition(adjacency)
    bridges, articulations = _bridges_and_articulations(adjacency)
    degree_histogram = tuple(sorted(Counter(len(neighbors) for neighbors in adjacency).items()))
    solutions, base, attempts, alternative_scans = _matching_family(
        adjacency, dual_edges, left, right, solution_cap
    )
    accepted = tuple(
        groups for groups in solutions if validate_toroidal_matching_witness(public, groups).valid
    )
    reference_groups = _normalize_groups(reference.groups) if reference is not None else None
    nonreference = sum(reference_groups is not None and groups != reference_groups for groups in accepted)
    return ToroidalMatchingRecovery(
        accepted_groups=accepted,
        dual_edges=len(dual_edges),
        dual_degree_histogram=degree_histogram,
        bridge_count=len(bridges),
        articulation_points=tuple(sorted(articulations)),
        bipartition_sizes=(len(left), len(right)),
        candidate_edges=len(dual_edges),
        base_augmentations=base.augmentations,
        base_dfs_calls=base.dfs_calls,
        base_edge_scans=base.edge_scans,
        alternative_attempts=attempts,
        alternative_matching_edge_scans=alternative_scans,
        matching_solutions=len(solutions),
        matching_solution_cap=solution_cap,
        matching_cap_hit=len(solutions) >= solution_cap,
        accepted_solutions=len(accepted),
        nonreference_accepted_solutions=nonreference,
    )


def toroidal_reference_partition_matches(
    reference: ToroidalMatchingReference,
    groups: tuple[TriangleGroup, ...],
) -> bool:
    return _normalize_groups(reference.groups) == _normalize_groups(groups)


def generate_toroidal_matching_instance(
    params: ToroidalMatchingParameters,
    master_seed: bytes,
) -> tuple[ToroidalMatchingPublicInstance, ToroidalMatchingReference]:
    params.validate()
    if len(master_seed) < 16:
        raise GluingExperimentError("G10 master seed must contain at least 128 bits")

    surface_seed = hashlib.sha256(
        b"MORPH-KEM G10 torus v1\x00" + master_seed + params.name.encode("ascii")
    ).digest()
    surface_public, _ = generate_surface_instance(
        SurfaceParameters(params.name + "-surface", params.rows, params.cols),
        surface_seed,
    )
    public = ToroidalMatchingPublicInstance(name=params.name, target=surface_public.target)

    adjacency, dual_edges = _triangle_dual(public)
    left, right = _bipartition(adjacency)
    solutions, _, _, _ = _matching_family(adjacency, dual_edges, left, right, 64)
    if len(solutions) < 2:
        raise GluingExperimentError("G10 generated torus does not expose alternative perfect matchings")
    selector = int.from_bytes(
        hashlib.sha256(
            b"MORPH-KEM G10 reference matching v1\x00"
            + master_seed
            + params.name.encode("ascii")
        ).digest(),
        "big",
    )
    reference = ToroidalMatchingReference(groups=solutions[selector % len(solutions)])

    incidence = toroidal_matching_incidence(public)
    if incidence.euler_characteristic != 0:
        raise GluingExperimentError("G10 generated surface is not toroidal by Euler characteristic")
    if incidence.min_triangles_per_edge != 2 or incidence.max_triangles_per_edge != 2:
        raise GluingExperimentError("G10 generated surface is not closed")
    if any(len(neighbors) != 3 for neighbors in adjacency):
        raise GluingExperimentError("G10 triangle dual graph is not 3-regular")
    if not validate_toroidal_matching_witness(public, reference.groups).valid:
        raise GluingExperimentError("G10 generated reference matching does not validate")

    return public, reference
