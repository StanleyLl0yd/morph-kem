from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
import hashlib
import json
from statistics import mean

from .complex import Simplex, SimplicialComplex

MorsePair = tuple[Simplex, Simplex]


class MorseExperimentError(ValueError):
    """Raised when an M3 Morse-witness experiment input is invalid."""


@dataclass(frozen=True, slots=True)
class MorseParameters:
    name: str
    vertices: int
    extra_edges: int
    expansions: int

    def validate(self) -> None:
        if self.vertices < 8 or self.vertices > 128:
            raise MorseExperimentError("M3 vertex count must be in [8, 128]")
        max_extra = self.vertices * (self.vertices - 1) // 2 - self.vertices
        if self.extra_edges <= 0 or self.extra_edges > max_extra:
            raise MorseExperimentError("M3 extra-edge count is outside the valid range")
        if self.expansions <= 0 or self.expansions > 128:
            raise MorseExperimentError("M3 expansions must be in [1, 128]")


MORSE_PARAMETER_SETS = {
    "morse-6": MorseParameters("morse-6", vertices=12, extra_edges=4, expansions=6),
    "morse-8": MorseParameters("morse-8", vertices=14, extra_edges=5, expansions=8),
    "morse-10": MorseParameters("morse-10", vertices=16, extra_edges=6, expansions=10),
    "morse-12": MorseParameters("morse-12", vertices=18, extra_edges=7, expansions=12),
    "morse-16": MorseParameters("morse-16", vertices=22, extra_edges=9, expansions=16),
}


@dataclass(frozen=True, slots=True)
class MorsePublicInstance:
    parameters: MorseParameters
    target: SimplicialComplex
    critical_target: tuple[int, ...]
    version: int = 1

    def __post_init__(self) -> None:
        self.parameters.validate()
        if self.version != 1:
            raise MorseExperimentError("unsupported M3 public-instance version")
        if self.target.dimension != 2:
            raise MorseExperimentError("M3 target must be two-dimensional")
        if self.target.vertices != tuple(range(self.parameters.vertices)):
            raise MorseExperimentError("M3 target must use the canonical public vertex universe")
        if len(self.critical_target) != self.target.dimension + 1:
            raise MorseExperimentError("critical target length does not match target dimension")
        if any(value < 0 for value in self.critical_target):
            raise MorseExperimentError("critical counts must be non-negative")

    def encode(self) -> bytes:
        payload = {
            "critical_target": list(self.critical_target),
            "parameters": {
                "expansions": self.parameters.expansions,
                "extra_edges": self.parameters.extra_edges,
                "name": self.parameters.name,
                "vertices": self.parameters.vertices,
            },
            "target": self.target.encode().hex(),
            "version": self.version,
        }
        return json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")

    @property
    def fingerprint(self) -> bytes:
        return hashlib.sha256(
            b"MORPH-KEM M3 public fingerprint v1\x00" + self.encode()
        ).digest()


@dataclass(frozen=True, slots=True)
class MorseTrapdoor:
    core: SimplicialComplex
    planted_matching: tuple[MorsePair, ...]
    public_fingerprint: bytes
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise MorseExperimentError("unsupported M3 trapdoor version")
        if self.core.dimension != 1:
            raise MorseExperimentError("M3 hidden core must be one-dimensional")
        if len(self.public_fingerprint) != 32:
            raise MorseExperimentError("M3 trapdoor binding must be 32 bytes")

    def encode(self) -> bytes:
        payload = {
            "core": self.core.encode().hex(),
            "planted_matching": [
                [list(lower), list(upper)] for lower, upper in self.planted_matching
            ],
            "public_fingerprint": self.public_fingerprint.hex(),
            "version": self.version,
        }
        return json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")


@dataclass(frozen=True, slots=True)
class MorseValidation:
    valid: bool
    acyclic: bool
    critical_vector: tuple[int, ...]
    reason: str


@dataclass(frozen=True, slots=True)
class CollapseWitnessResult:
    reached_graph: bool
    accepted: bool
    matching: tuple[MorsePair, ...]
    residual: SimplicialComplex
    triangle_collapses: int
    initial_triangle_choices: int
    max_triangle_choices: int


@dataclass(frozen=True, slots=True)
class CollapseSurvey:
    trials: int
    reached_graph: int
    accepted: int
    unique_residuals: int
    mean_triangle_collapses: float


@dataclass(frozen=True, slots=True)
class GreedyMatchingResult:
    matching: tuple[MorsePair, ...]
    validation: MorseValidation


@dataclass(frozen=True, slots=True)
class GreedyMatchingSurvey:
    trials: int
    target_hits: int
    unique_critical_vectors: int
    best_total_critical: int


class _DeterministicRng:
    def __init__(self, seed: bytes):
        self._seed = seed
        self._counter = 0

    def _block(self) -> bytes:
        block = hashlib.sha256(
            b"MORPH-KEM M3 deterministic rng v1\x00"
            + self._seed
            + self._counter.to_bytes(8, "big")
        ).digest()
        self._counter += 1
        return block

    def randbelow(self, upper: int) -> int:
        if upper <= 0:
            raise ValueError("upper bound must be positive")
        limit = (1 << 256) - ((1 << 256) % upper)
        while True:
            candidate = int.from_bytes(self._block(), "big")
            if candidate < limit:
                return candidate % upper


def _shuffle(items: list, seed: bytes) -> None:
    rng = _DeterministicRng(seed)
    for index in range(len(items) - 1, 0, -1):
        swap = rng.randbelow(index + 1)
        items[index], items[swap] = items[swap], items[index]


def _edge(left: int, right: int) -> Simplex:
    return (left, right) if left < right else (right, left)


def _variable_degree_core(
    vertices: int,
    extra_edges: int,
    seed: bytes,
) -> SimplicialComplex:
    cycle = {_edge(vertex, (vertex + 1) % vertices) for vertex in range(vertices)}
    all_chords = [
        _edge(left, right)
        for left in range(vertices)
        for right in range(left + 1, vertices)
        if _edge(left, right) not in cycle
    ]

    for attempt in range(1024):
        candidates = list(all_chords)
        _shuffle(
            candidates,
            hashlib.sha256(
                b"MORPH-KEM M3 core chords v1\x00"
                + seed
                + attempt.to_bytes(4, "big")
            ).digest(),
        )
        edges = cycle | set(candidates[:extra_edges])
        degrees = [0] * vertices
        for left, right in edges:
            degrees[left] += 1
            degrees[right] += 1
        if min(degrees) < 2:
            continue
        if len(set(degrees)) < 2:
            continue
        return SimplicialComplex.from_facets(sorted(edges))
    raise MorseExperimentError("could not generate a variable-degree connected M3 core")


def _expansion_candidates(
    complex_: SimplicialComplex,
    vertices: int,
) -> tuple[tuple[Simplex, Simplex, int], ...]:
    simplex_set = set(complex_.simplices)
    edges = {simplex for simplex in simplex_set if len(simplex) == 2}
    triangles = {simplex for simplex in simplex_set if len(simplex) == 3}
    facet_edges = {facet for facet in complex_.facets if len(facet) == 2}

    candidates: list[tuple[Simplex, Simplex, int]] = []
    for tau in combinations(range(vertices), 3):
        if tau in triangles:
            continue
        triangle_edges = tuple(combinations(tau, 2))
        missing = tuple(edge for edge in triangle_edges if edge not in edges)
        if len(missing) != 1:
            continue
        present = tuple(edge for edge in triangle_edges if edge in edges)
        overlap_score = sum(edge in facet_edges for edge in present)
        if overlap_score == 0:
            continue
        candidates.append((missing[0], tau, overlap_score))
    return tuple(candidates)


def _permutation(size: int, seed: bytes) -> tuple[int, ...]:
    values = list(range(size))
    _shuffle(values, seed)
    return tuple(values)


def _relabel_simplex(simplex: Simplex, mapping: tuple[int, ...]) -> Simplex:
    return tuple(sorted(mapping[vertex] for vertex in simplex))


def _incidence_pairs(complex_: SimplicialComplex) -> tuple[MorsePair, ...]:
    result: list[MorsePair] = []
    for upper in complex_.simplices:
        if len(upper) < 2:
            continue
        for lower in combinations(upper, len(upper) - 1):
            result.append((lower, upper))
    result.sort(key=lambda pair: (-len(pair[1]), pair[1], pair[0]))
    return tuple(result)


def _critical_vector(
    complex_: SimplicialComplex,
    matching: tuple[MorsePair, ...],
) -> tuple[int, ...]:
    used = {simplex for pair in matching for simplex in pair}
    counts = [0] * (complex_.dimension + 1)
    for simplex in complex_.simplices:
        if simplex not in used:
            counts[len(simplex) - 1] += 1
    return tuple(counts)


def validate_morse_matching(
    complex_: SimplicialComplex,
    matching: tuple[MorsePair, ...],
    target: tuple[int, ...] | None = None,
) -> MorseValidation:
    simplex_set = set(complex_.simplices)
    normalized: list[MorsePair] = []
    used: set[Simplex] = set()

    for pair in matching:
        if len(pair) != 2:
            return MorseValidation(False, False, (), "matching entry must contain two simplices")
        lower = tuple(pair[0])
        upper = tuple(pair[1])
        if lower not in simplex_set or upper not in simplex_set:
            return MorseValidation(False, False, (), "matching references a simplex outside the complex")
        if len(upper) != len(lower) + 1 or not set(lower).issubset(upper):
            return MorseValidation(False, False, (), "matching pair is not a codimension-one incidence")
        if lower in used or upper in used:
            return MorseValidation(False, False, (), "a simplex is reused by multiple matching pairs")
        used.add(lower)
        used.add(upper)
        normalized.append((lower, upper))

    matching_set = set(normalized)
    adjacency: dict[Simplex, list[Simplex]] = {
        simplex: [] for simplex in complex_.simplices
    }
    indegree: dict[Simplex, int] = {
        simplex: 0 for simplex in complex_.simplices
    }

    for lower, upper in _incidence_pairs(complex_):
        if (lower, upper) in matching_set:
            source, destination = lower, upper
        else:
            source, destination = upper, lower
        adjacency[source].append(destination)
        indegree[destination] += 1

    ready = sorted(simplex for simplex, degree in indegree.items() if degree == 0)
    visited = 0
    while ready:
        current = ready.pop()
        visited += 1
        for destination in adjacency[current]:
            indegree[destination] -= 1
            if indegree[destination] == 0:
                ready.append(destination)

    acyclic = visited == len(complex_.simplices)
    critical = _critical_vector(complex_, tuple(normalized))
    if not acyclic:
        return MorseValidation(False, False, critical, "oriented Hasse diagram contains a directed cycle")
    if target is not None:
        if len(target) != complex_.dimension + 1:
            return MorseValidation(False, True, critical, "target critical vector has wrong dimension")
        if critical != target:
            return MorseValidation(False, True, critical, "critical vector does not match public target")
    return MorseValidation(True, True, critical, "accepted")


def _spanning_tree_matching(graph: SimplicialComplex) -> tuple[MorsePair, ...]:
    if graph.dimension > 1:
        raise MorseExperimentError("spanning-tree matching requires a graph")

    vertices = list(graph.vertices)
    if not vertices:
        raise MorseExperimentError("graph has no vertices")
    adjacency: dict[int, list[tuple[int, Simplex]]] = {vertex: [] for vertex in vertices}
    for edge in (simplex for simplex in graph.simplices if len(simplex) == 2):
        left, right = edge
        adjacency[left].append((right, edge))
        adjacency[right].append((left, edge))
    for neighbors in adjacency.values():
        neighbors.sort()

    root = min(vertices)
    queue = [root]
    seen = {root}
    matching: list[MorsePair] = []
    while queue:
        parent = queue.pop(0)
        for child, edge in adjacency[parent]:
            if child in seen:
                continue
            seen.add(child)
            queue.append(child)
            matching.append(((child,), edge))

    if len(seen) != len(vertices):
        raise MorseExperimentError("graph is disconnected")
    return tuple(matching)


def generate_morse_instance(
    parameters: MorseParameters,
    master_seed: bytes,
) -> tuple[MorsePublicInstance, MorseTrapdoor]:
    parameters.validate()
    if not isinstance(master_seed, bytes) or not master_seed:
        raise MorseExperimentError("master_seed must be non-empty bytes")

    for attempt in range(256):
        attempt_seed = hashlib.sha256(
            b"MORPH-KEM M3 generation attempt v1\x00"
            + parameters.name.encode("ascii")
            + b"\x00"
            + master_seed
            + attempt.to_bytes(4, "big")
        ).digest()
        core = _variable_degree_core(
            parameters.vertices,
            parameters.extra_edges,
            attempt_seed,
        )
        state = core
        expansion_steps: list[MorsePair] = []
        rng = _DeterministicRng(
            hashlib.sha256(
                b"MORPH-KEM M3 expansion chooser v1\x00" + attempt_seed
            ).digest()
        )

        for _ in range(parameters.expansions):
            candidates = _expansion_candidates(state, parameters.vertices)
            if not candidates:
                break
            best_overlap = max(candidate[2] for candidate in candidates)
            pool = [candidate for candidate in candidates if candidate[2] == best_overlap]
            lower, upper, _ = pool[rng.randbelow(len(pool))]
            state = state.elementary_expand(lower, upper)
            expansion_steps.append((lower, upper))

        if len(expansion_steps) != parameters.expansions:
            continue

        relabeling = _permutation(
            parameters.vertices,
            hashlib.sha256(
                b"MORPH-KEM M3 final relabeling v1\x00" + attempt_seed
            ).digest(),
        )
        public_core = core.relabel(relabeling)
        target = state.relabel(relabeling)

        expansion_matching = tuple(
            (
                _relabel_simplex(lower, relabeling),
                _relabel_simplex(upper, relabeling),
            )
            for lower, upper in expansion_steps
        )
        graph_matching = _spanning_tree_matching(public_core)
        planted_matching = expansion_matching + graph_matching

        edge_count = sum(len(simplex) == 2 for simplex in core.simplices)
        beta1 = edge_count - parameters.vertices + 1
        critical_target = (1, beta1, 0)

        public = MorsePublicInstance(
            parameters=parameters,
            target=target,
            critical_target=critical_target,
        )
        trapdoor = MorseTrapdoor(
            core=public_core,
            planted_matching=planted_matching,
            public_fingerprint=public.fingerprint,
        )

        validation = validate_morse_matching(
            public.target,
            trapdoor.planted_matching,
            public.critical_target,
        )
        if validation.valid:
            return public, trapdoor

    raise MorseExperimentError("could not generate a valid M3 planted witness")


def verify_planted_witness(
    public: MorsePublicInstance,
    trapdoor: MorseTrapdoor,
) -> MorseValidation:
    if public.fingerprint != trapdoor.public_fingerprint:
        raise MorseExperimentError("M3 trapdoor is bound to a different public instance")
    return validate_morse_matching(
        public.target,
        trapdoor.planted_matching,
        public.critical_target,
    )


def collapse_to_graph_witness(
    public: MorsePublicInstance,
    strategy: str = "lex",
    attack_seed: bytes = b"M3-collapse",
) -> CollapseWitnessResult:
    if strategy not in {"lex", "reverse", "random"}:
        raise MorseExperimentError(f"unknown M3 collapse strategy: {strategy}")
    if strategy == "random" and not attack_seed:
        raise MorseExperimentError("random M3 collapse attack requires a non-empty seed")

    rng = _DeterministicRng(
        hashlib.sha256(
            b"MORPH-KEM M3 collapse attack v1\x00" + attack_seed
        ).digest()
    ) if strategy == "random" else None

    state = public.target
    chosen: list[MorsePair] = []
    initial = 0
    maximum = 0

    while state.dimension == 2:
        pairs = tuple(
            pair for pair in state.free_collapse_pairs()
            if len(pair[1]) == 3
        )
        if not chosen:
            initial = len(pairs)
        maximum = max(maximum, len(pairs))
        if not pairs:
            break
        if strategy == "lex":
            pair = pairs[0]
        elif strategy == "reverse":
            pair = pairs[-1]
        else:
            assert rng is not None
            pair = pairs[rng.randbelow(len(pairs))]
        chosen.append(pair)
        state = state.collapse(*pair)

    reached_graph = state.dimension <= 1
    if reached_graph:
        try:
            graph_matching = _spanning_tree_matching(state)
        except MorseExperimentError:
            graph_matching = ()
            reached_graph = False
    else:
        graph_matching = ()

    matching = tuple(chosen) + graph_matching
    validation = validate_morse_matching(
        public.target,
        matching,
        public.critical_target,
    ) if reached_graph else MorseValidation(False, False, (), "attack did not reach a graph")

    return CollapseWitnessResult(
        reached_graph=reached_graph,
        accepted=validation.valid,
        matching=matching,
        residual=state,
        triangle_collapses=len(chosen),
        initial_triangle_choices=initial,
        max_triangle_choices=maximum,
    )


def collapse_witness_survey(
    public: MorsePublicInstance,
    trials: int = 64,
    attack_seed: bytes = b"M3-collapse-survey",
) -> CollapseSurvey:
    if trials <= 0 or trials > 10_000:
        raise MorseExperimentError("M3 collapse survey trials must be in [1, 10000]")
    if not attack_seed:
        raise MorseExperimentError("M3 collapse survey requires a non-empty seed")

    reached = 0
    accepted = 0
    residuals: set[bytes] = set()
    counts: list[int] = []

    for trial in range(trials):
        seed = hashlib.sha256(
            b"MORPH-KEM M3 collapse survey trial v1\x00"
            + attack_seed
            + trial.to_bytes(8, "big")
        ).digest()
        result = collapse_to_graph_witness(
            public,
            strategy="random",
            attack_seed=seed,
        )
        reached += int(result.reached_graph)
        accepted += int(result.accepted)
        residuals.add(result.residual.encode())
        counts.append(result.triangle_collapses)

    return CollapseSurvey(
        trials=trials,
        reached_graph=reached,
        accepted=accepted,
        unique_residuals=len(residuals),
        mean_triangle_collapses=mean(counts),
    )


def greedy_acyclic_matching(
    public: MorsePublicInstance,
    attack_seed: bytes = b"M3-greedy-matching",
) -> GreedyMatchingResult:
    if not attack_seed:
        raise MorseExperimentError("M3 greedy matching requires a non-empty seed")

    candidates = list(_incidence_pairs(public.target))
    _shuffle(
        candidates,
        hashlib.sha256(
            b"MORPH-KEM M3 greedy matching order v1\x00" + attack_seed
        ).digest(),
    )

    matching: list[MorsePair] = []
    used: set[Simplex] = set()
    for pair in candidates:
        lower, upper = pair
        if lower in used or upper in used:
            continue
        proposed = tuple(matching + [pair])
        validation = validate_morse_matching(public.target, proposed)
        if not validation.valid:
            continue
        matching.append(pair)
        used.add(lower)
        used.add(upper)

    final = validate_morse_matching(
        public.target,
        tuple(matching),
        public.critical_target,
    )
    return GreedyMatchingResult(tuple(matching), final)


def greedy_matching_survey(
    public: MorsePublicInstance,
    trials: int = 32,
    attack_seed: bytes = b"M3-greedy-survey",
) -> GreedyMatchingSurvey:
    if trials <= 0 or trials > 1000:
        raise MorseExperimentError("M3 greedy matching survey trials must be in [1, 1000]")
    if not attack_seed:
        raise MorseExperimentError("M3 greedy matching survey requires a non-empty seed")

    target_hits = 0
    vectors: set[tuple[int, ...]] = set()
    best = len(public.target.simplices)

    for trial in range(trials):
        seed = hashlib.sha256(
            b"MORPH-KEM M3 greedy survey trial v1\x00"
            + attack_seed
            + trial.to_bytes(8, "big")
        ).digest()
        result = greedy_acyclic_matching(public, seed)
        vector = result.validation.critical_vector
        vectors.add(vector)
        best = min(best, sum(vector))
        target_hits += int(result.validation.valid)

    return GreedyMatchingSurvey(
        trials=trials,
        target_hits=target_hits,
        unique_critical_vectors=len(vectors),
        best_total_critical=best,
    )
