from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
import hashlib
import json
from statistics import mean

from .complex import Simplex, SimplicialComplex
from .morse import MorsePair, MorseValidation, validate_morse_matching


class NonManifoldExperimentError(ValueError):
    """Raised when an M5 irregular non-manifold experiment input is invalid."""


@dataclass(frozen=True, slots=True)
class NonManifoldParameters:
    name: str
    vertices: int
    sampled_triangles: int
    reference_trials: int = 48

    def validate(self) -> None:
        if self.vertices < 7 or self.vertices > 24:
            raise NonManifoldExperimentError("M5 vertices must be in [7, 24]")
        maximum = self.vertices * (self.vertices - 1) * (self.vertices - 2) // 6
        if self.sampled_triangles <= 0 or self.sampled_triangles >= maximum:
            raise NonManifoldExperimentError("M5 sampled triangle count is invalid")
        if self.reference_trials <= 0 or self.reference_trials > 512:
            raise NonManifoldExperimentError("M5 reference trials must be in [1, 512]")


NONMANIFOLD_PARAMETER_SETS = {
    "m5-8": NonManifoldParameters("m5-8", 8, 30),
    "m5-9": NonManifoldParameters("m5-9", 9, 40),
    "m5-10": NonManifoldParameters("m5-10", 10, 52),
}


@dataclass(frozen=True, slots=True)
class NonManifoldPublic:
    parameters: NonManifoldParameters
    target: SimplicialComplex
    critical_target: tuple[int, int, int]
    version: int = 1

    def __post_init__(self) -> None:
        self.parameters.validate()
        if self.version != 1:
            raise NonManifoldExperimentError("unsupported M5 public version")
        if self.target.dimension != 2:
            raise NonManifoldExperimentError("M5 target must be two-dimensional")
        if self.target.vertices != tuple(range(self.parameters.vertices)):
            raise NonManifoldExperimentError("M5 target must use canonical public vertices")
        if len(self.critical_target) != 3 or any(value < 0 for value in self.critical_target):
            raise NonManifoldExperimentError("M5 critical target is invalid")

    def encode(self) -> bytes:
        payload = {
            "critical_target": list(self.critical_target),
            "parameters": {
                "name": self.parameters.name,
                "reference_trials": self.parameters.reference_trials,
                "sampled_triangles": self.parameters.sampled_triangles,
                "vertices": self.parameters.vertices,
            },
            "target": self.target.encode().hex(),
            "version": self.version,
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


@dataclass(frozen=True, slots=True)
class NonManifoldReference:
    matching: tuple[MorsePair, ...]


@dataclass(frozen=True, slots=True)
class IncidenceMetrics:
    vertices: int
    edges: int
    triangles: int
    min_triangles_per_edge: int
    max_triangles_per_edge: int
    incidence_histogram: tuple[tuple[int, int], ...]
    free_collapse_pairs: int


@dataclass(frozen=True, slots=True)
class TreeGreedyResult:
    matching: tuple[MorsePair, ...]
    validation: MorseValidation
    tree_pairs: int
    triangle_pairs: int


@dataclass(frozen=True, slots=True)
class M5GreedySurvey:
    trials: int
    target_hits: int
    unique_vectors: int
    unique_target_matchings: int
    best_total_critical: int
    mean_total_critical: float


@dataclass(frozen=True, slots=True)
class M5SearchResult:
    found: bool
    matching: tuple[MorsePair, ...]
    validation: MorseValidation | None
    nodes: int
    tree_trials: int
    exhausted: bool


class _DeterministicRng:
    def __init__(self, seed: bytes):
        self._seed = seed
        self._counter = 0

    def _block(self) -> bytes:
        result = hashlib.sha256(
            b"MORPH-KEM M5 rng v1\x00"
            + self._seed
            + self._counter.to_bytes(8, "big")
        ).digest()
        self._counter += 1
        return result

    def randbelow(self, upper: int) -> int:
        if upper <= 0:
            raise ValueError("upper must be positive")
        limit = (1 << 256) - ((1 << 256) % upper)
        while True:
            value = int.from_bytes(self._block(), "big")
            if value < limit:
                return value % upper


def _shuffle(values: list, seed: bytes) -> None:
    rng = _DeterministicRng(seed)
    for index in range(len(values) - 1, 0, -1):
        other = rng.randbelow(index + 1)
        values[index], values[other] = values[other], values[index]


def _edge_incidence(triangles: set[Simplex]) -> dict[Simplex, int]:
    counts: dict[Simplex, int] = {}
    for triangle in triangles:
        for edge in combinations(triangle, 2):
            counts[edge] = counts.get(edge, 0) + 1
    return counts


def _peel_two_core(triangles: set[Simplex]) -> set[Simplex]:
    current = set(triangles)
    while current:
        counts = _edge_incidence(current)
        doomed = {
            triangle
            for triangle in current
            if any(counts[edge] < 2 for edge in combinations(triangle, 2))
        }
        if not doomed:
            return current
        current -= doomed
    return current


def _connected_one_skeleton(complex_: SimplicialComplex) -> bool:
    vertices = list(complex_.vertices)
    if not vertices:
        return False
    adjacency = {vertex: set() for vertex in vertices}
    for edge in (simplex for simplex in complex_.simplices if len(simplex) == 2):
        left, right = edge
        adjacency[left].add(right)
        adjacency[right].add(left)
    seen = {vertices[0]}
    queue = [vertices[0]]
    while queue:
        current = queue.pop(0)
        for neighbor in sorted(adjacency[current]):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return len(seen) == len(vertices)


def _permutation(size: int, seed: bytes) -> tuple[int, ...]:
    values = list(range(size))
    _shuffle(values, seed)
    return tuple(values)


def incidence_metrics(complex_: SimplicialComplex) -> IncidenceMetrics:
    triangles = {simplex for simplex in complex_.simplices if len(simplex) == 3}
    counts = _edge_incidence(triangles)
    histogram: dict[int, int] = {}
    for count in counts.values():
        histogram[count] = histogram.get(count, 0) + 1
    return IncidenceMetrics(
        vertices=len(complex_.vertices),
        edges=sum(len(simplex) == 2 for simplex in complex_.simplices),
        triangles=len(triangles),
        min_triangles_per_edge=min(counts.values()) if counts else 0,
        max_triangles_per_edge=max(counts.values()) if counts else 0,
        incidence_histogram=tuple(sorted(histogram.items())),
        free_collapse_pairs=len(complex_.free_collapse_pairs()),
    )


def _incidence_pairs(complex_: SimplicialComplex) -> tuple[MorsePair, ...]:
    pairs: list[MorsePair] = []
    for upper in complex_.simplices:
        if len(upper) < 2:
            continue
        for lower in combinations(upper, len(upper) - 1):
            pairs.append((lower, upper))
    pairs.sort(key=lambda pair: (-len(pair[1]), pair[1], pair[0]))
    return tuple(pairs)


def _spanning_tree_pairs(complex_: SimplicialComplex, seed: bytes) -> tuple[MorsePair, ...]:
    vertices = list(complex_.vertices)
    adjacency: dict[int, list[tuple[int, Simplex]]] = {vertex: [] for vertex in vertices}
    for edge in (simplex for simplex in complex_.simplices if len(simplex) == 2):
        left, right = edge
        adjacency[left].append((right, edge))
        adjacency[right].append((left, edge))
    for vertex in vertices:
        adjacency[vertex].sort()
        _shuffle(
            adjacency[vertex],
            hashlib.sha256(seed + b"adj" + vertex.to_bytes(2, "big")).digest(),
        )
    roots = list(vertices)
    _shuffle(roots, hashlib.sha256(seed + b"root").digest())
    root = roots[0]
    seen = {root}
    queue = [root]
    result: list[MorsePair] = []
    while queue:
        parent = queue.pop(0)
        for child, edge in adjacency[parent]:
            if child in seen:
                continue
            seen.add(child)
            queue.append(child)
            result.append(((child,), edge))
    if len(seen) != len(vertices):
        raise NonManifoldExperimentError("M5 1-skeleton is disconnected")
    return tuple(result)


def tree_greedy_matching(complex_: SimplicialComplex, seed: bytes) -> TreeGreedyResult:
    if not seed:
        raise NonManifoldExperimentError("M5 matching seed must be non-empty")
    matching = list(_spanning_tree_pairs(complex_, seed))
    validation = validate_morse_matching(complex_, tuple(matching))
    if not validation.valid:
        raise NonManifoldExperimentError("M5 spanning-tree matching is unexpectedly cyclic")

    used = {simplex for pair in matching for simplex in pair}
    candidates = [
        pair
        for pair in _incidence_pairs(complex_)
        if len(pair[1]) == 3
    ]
    _shuffle(candidates, hashlib.sha256(seed + b"triangles").digest())
    triangle_pairs = 0
    for lower, upper in candidates:
        if lower in used or upper in used:
            continue
        proposed = tuple(matching + [(lower, upper)])
        check = validate_morse_matching(complex_, proposed)
        if not check.valid:
            continue
        matching.append((lower, upper))
        used.add(lower)
        used.add(upper)
        triangle_pairs += 1

    final = validate_morse_matching(complex_, tuple(matching))
    return TreeGreedyResult(
        matching=tuple(matching),
        validation=final,
        tree_pairs=len(complex_.vertices) - 1,
        triangle_pairs=triangle_pairs,
    )


def _generate_core(parameters: NonManifoldParameters, master_seed: bytes) -> SimplicialComplex:
    all_triangles = list(combinations(range(parameters.vertices), 3))
    for attempt in range(1024):
        candidates = list(all_triangles)
        _shuffle(
            candidates,
            hashlib.sha256(
                b"MORPH-KEM M5 triangle sample v1\x00"
                + parameters.name.encode("ascii")
                + master_seed
                + attempt.to_bytes(4, "big")
            ).digest(),
        )
        sampled = set(candidates[: parameters.sampled_triangles])
        core = _peel_two_core(sampled)
        if len(core) < parameters.vertices:
            continue
        complex_ = SimplicialComplex.from_facets(sorted(core))
        if complex_.vertices != tuple(range(parameters.vertices)):
            continue
        if not _connected_one_skeleton(complex_):
            continue
        metrics = incidence_metrics(complex_)
        if metrics.min_triangles_per_edge < 2:
            continue
        if metrics.max_triangles_per_edge <= 2:
            continue
        if metrics.free_collapse_pairs != 0:
            continue
        relabeling = _permutation(
            parameters.vertices,
            hashlib.sha256(
                b"MORPH-KEM M5 relabel v1\x00"
                + master_seed
                + attempt.to_bytes(4, "big")
            ).digest(),
        )
        return complex_.relabel(relabeling)
    raise NonManifoldExperimentError("could not generate an irregular triangular 2-core")


def generate_nonmanifold_instance(
    parameters: NonManifoldParameters,
    master_seed: bytes,
) -> tuple[NonManifoldPublic, NonManifoldReference]:
    parameters.validate()
    if not isinstance(master_seed, bytes) or not master_seed:
        raise NonManifoldExperimentError("master_seed must be non-empty bytes")
    target = _generate_core(parameters, master_seed)

    best: TreeGreedyResult | None = None
    best_key: tuple | None = None
    for trial in range(parameters.reference_trials):
        seed = hashlib.sha256(
            b"MORPH-KEM M5 reference matching v1\x00"
            + master_seed
            + trial.to_bytes(4, "big")
        ).digest()
        candidate = tree_greedy_matching(target, seed)
        vector = candidate.validation.critical_vector
        key = (sum(vector), vector[2], vector[1], tuple(sorted(candidate.matching)))
        if best is None or key < best_key:
            best = candidate
            best_key = key

    if best is None or not best.validation.valid:
        raise NonManifoldExperimentError("could not construct M5 reference matching")
    vector = best.validation.critical_vector
    if len(vector) != 3 or vector[0] != 1:
        raise NonManifoldExperimentError("M5 reference must leave exactly one critical vertex")

    public = NonManifoldPublic(parameters, target, vector)
    reference = NonManifoldReference(best.matching)
    check = validate_morse_matching(target, reference.matching, public.critical_target)
    if not check.valid:
        raise NonManifoldExperimentError("internal M5 reference verification failed")
    return public, reference


def greedy_witness_survey(
    public: NonManifoldPublic,
    trials: int = 64,
    attack_seed: bytes = b"M5-public-greedy",
) -> M5GreedySurvey:
    if trials <= 0 or trials > 4096:
        raise NonManifoldExperimentError("M5 greedy trials must be in [1, 4096]")
    if not attack_seed:
        raise NonManifoldExperimentError("M5 greedy survey seed must be non-empty")
    hits = 0
    vectors: set[tuple[int, ...]] = set()
    target_matchings: set[tuple[MorsePair, ...]] = set()
    totals: list[int] = []
    for trial in range(trials):
        seed = hashlib.sha256(
            b"MORPH-KEM M5 public greedy trial v1\x00"
            + attack_seed
            + trial.to_bytes(4, "big")
        ).digest()
        result = tree_greedy_matching(public.target, seed)
        vector = result.validation.critical_vector
        vectors.add(vector)
        totals.append(sum(vector))
        if vector == public.critical_target:
            exact = validate_morse_matching(public.target, result.matching, public.critical_target)
            if exact.valid:
                hits += 1
                target_matchings.add(tuple(sorted(result.matching)))
    return M5GreedySurvey(
        trials=trials,
        target_hits=hits,
        unique_vectors=len(vectors),
        unique_target_matchings=len(target_matchings),
        best_total_critical=min(totals),
        mean_total_critical=mean(totals),
    )


def bounded_tree_extension_search(
    public: NonManifoldPublic,
    tree_trials: int = 8,
    max_nodes: int = 50_000,
    attack_seed: bytes = b"M5-exact-extension",
) -> M5SearchResult:
    if tree_trials <= 0 or tree_trials > 256:
        raise NonManifoldExperimentError("M5 tree trials must be in [1, 256]")
    if max_nodes <= 0 or max_nodes > 5_000_000:
        raise NonManifoldExperimentError("M5 max_nodes must be in [1, 5000000]")
    if not attack_seed:
        raise NonManifoldExperimentError("M5 search seed must be non-empty")
    if public.critical_target[0] != 1:
        return M5SearchResult(False, (), None, 0, 0, True)

    triangle_count = sum(len(simplex) == 3 for simplex in public.target.simplices)
    required_triangle_pairs = triangle_count - public.critical_target[2]
    nodes = 0

    for tree_trial in range(tree_trials):
        seed = hashlib.sha256(
            b"MORPH-KEM M5 exact tree v1\x00"
            + attack_seed
            + tree_trial.to_bytes(4, "big")
        ).digest()
        base_matching = list(_spanning_tree_pairs(public.target, seed))
        base_used = {simplex for pair in base_matching for simplex in pair}
        triangles = sorted(simplex for simplex in public.target.simplices if len(simplex) == 3)
        edge_options = {
            triangle: tuple(
                edge
                for edge in combinations(triangle, 2)
                if edge not in base_used
            )
            for triangle in triangles
        }
        order = sorted(triangles, key=lambda triangle: (len(edge_options[triangle]), triangle))
        found: tuple[MorsePair, ...] | None = None

        def search(index: int, matching: list[MorsePair], used_edges: set[Simplex], matched: int) -> None:
            nonlocal nodes, found
            if found is not None or nodes >= max_nodes:
                return
            nodes += 1
            remaining = len(order) - index
            if matched > required_triangle_pairs or matched + remaining < required_triangle_pairs:
                return
            if index == len(order):
                if matched != required_triangle_pairs:
                    return
                candidate = tuple(matching)
                validation = validate_morse_matching(public.target, candidate, public.critical_target)
                if validation.valid:
                    found = candidate
                return

            triangle = order[index]
            if matched < required_triangle_pairs:
                for edge in edge_options[triangle]:
                    if edge in used_edges:
                        continue
                    pair = (edge, triangle)
                    candidate = tuple(matching + [pair])
                    partial = validate_morse_matching(public.target, candidate)
                    if not partial.valid:
                        continue
                    used_edges.add(edge)
                    matching.append(pair)
                    search(index + 1, matching, used_edges, matched + 1)
                    matching.pop()
                    used_edges.remove(edge)
                    if found is not None or nodes >= max_nodes:
                        return
            if matched + (remaining - 1) >= required_triangle_pairs:
                search(index + 1, matching, used_edges, matched)

        search(0, list(base_matching), set(base_used), 0)
        if found is not None:
            validation = validate_morse_matching(public.target, found, public.critical_target)
            return M5SearchResult(True, found, validation, nodes, tree_trial + 1, False)
        if nodes >= max_nodes:
            return M5SearchResult(False, (), None, nodes, tree_trial + 1, False)

    return M5SearchResult(False, (), None, nodes, tree_trials, True)
