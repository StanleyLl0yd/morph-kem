from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
import hashlib
import hmac
import json
import math
from statistics import mean

from .complex import Simplex, SimplicialComplex

CollapsePair = tuple[Simplex, Simplex]


class MazeExperimentError(ValueError):
    """Raised when an M2 collapse-maze input or generated instance is invalid."""


@dataclass(frozen=True, slots=True)
class MazeParameters:
    name: str
    vertices: int
    expansions: int
    min_initial_free_pairs: int = 4

    def validate(self) -> None:
        if self.vertices < 8 or self.vertices > 128 or self.vertices % 2:
            raise MazeExperimentError("M2 vertex count must be even and in [8, 128]")
        if self.expansions <= 0 or self.expansions > 64:
            raise MazeExperimentError("M2 expansions must be in [1, 64]")
        if self.min_initial_free_pairs < 2:
            raise MazeExperimentError("M2 must require at least two initial free choices")


MAZE_PARAMETER_SETS = {
    "maze-4": MazeParameters("maze-4", vertices=10, expansions=4),
    "maze-6": MazeParameters("maze-6", vertices=12, expansions=6),
    "maze-8": MazeParameters("maze-8", vertices=12, expansions=8),
    "maze-10": MazeParameters("maze-10", vertices=16, expansions=10),
    "maze-12": MazeParameters("maze-12", vertices=16, expansions=12),
    "maze-16": MazeParameters("maze-16", vertices=20, expansions=16),
}


@dataclass(frozen=True, slots=True)
class MazePublicInstance:
    parameters: MazeParameters
    target: SimplicialComplex
    core_digest: bytes
    version: int = 1

    def __post_init__(self) -> None:
        self.parameters.validate()
        if self.version != 1:
            raise MazeExperimentError("unsupported M2 public-instance version")
        if len(self.core_digest) != 32:
            raise MazeExperimentError("M2 core digest must be 32 bytes")
        if self.target.dimension != 2:
            raise MazeExperimentError("M2 target must be a 2-dimensional complex")
        if self.target.vertices != tuple(range(self.parameters.vertices)):
            raise MazeExperimentError("M2 target must use the complete canonical vertex universe")

    def encode(self) -> bytes:
        payload = {
            "core_digest": self.core_digest.hex(),
            "parameters": {
                "expansions": self.parameters.expansions,
                "min_initial_free_pairs": self.parameters.min_initial_free_pairs,
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
            b"MORPH-KEM M2 public fingerprint v1\x00" + self.encode()
        ).digest()


@dataclass(frozen=True, slots=True)
class MazeTrapdoor:
    core: SimplicialComplex
    certificate: tuple[CollapsePair, ...]
    public_fingerprint: bytes
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise MazeExperimentError("unsupported M2 trapdoor version")
        if self.core.dimension != 1:
            raise MazeExperimentError("M2 hidden core must be one-dimensional")
        if len(self.public_fingerprint) != 32:
            raise MazeExperimentError("M2 trapdoor public binding must be 32 bytes")

    def encode(self) -> bytes:
        payload = {
            "certificate": [
                [list(sigma), list(tau)] for sigma, tau in self.certificate
            ],
            "core": self.core.encode().hex(),
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
class PlantedReductionMetrics:
    steps: int
    initial_free_pairs: int
    min_free_pairs: int
    max_free_pairs: int
    mean_free_pairs: float
    mean_planted_rank: float


@dataclass(frozen=True, slots=True)
class GreedyResult:
    residual: SimplicialComplex
    collapses: int
    initial_free_pairs: int
    max_free_pairs: int
    verified_core: bool


@dataclass(frozen=True, slots=True)
class GreedySurvey:
    trials: int
    core_hits: int
    unique_residuals: int
    min_residual_simplices: int
    max_residual_simplices: int
    mean_collapses: float


@dataclass(frozen=True, slots=True)
class SearchResult:
    found: bool
    certificate: tuple[CollapsePair, ...]
    nodes: int
    visited_states: int
    max_frontier: int
    min_simplices_seen: int
    exhausted: bool


@dataclass(frozen=True, slots=True)
class CoreRecoveryResult:
    found: bool
    core: SimplicialComplex | None
    nodes: int
    degree_candidates: int
    forced_edges: int
    optional_edges: int
    exhausted: bool


class _DeterministicRng:
    def __init__(self, seed: bytes):
        self._seed = seed
        self._counter = 0

    def _block(self) -> bytes:
        block = hashlib.sha256(
            b"MORPH-KEM M2 deterministic rng v1\x00"
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


def _permutation(size: int, seed: bytes) -> tuple[int, ...]:
    values = list(range(size))
    rng = _DeterministicRng(seed)
    for i in range(size - 1, 0, -1):
        j = rng.randbelow(i + 1)
        values[i], values[j] = values[j], values[i]
    return tuple(values)


def _edge(a: int, b: int) -> Simplex:
    return (a, b) if a < b else (b, a)


def _core_digest(core: SimplicialComplex) -> bytes:
    return hashlib.sha256(
        b"MORPH-KEM M2 hidden core digest v1\x00" + core.encode()
    ).digest()


def _three_regular_core(vertices: int, seed: bytes) -> SimplicialComplex:
    cycle_edges = {
        _edge(i, (i + 1) % vertices)
        for i in range(vertices)
    }

    for attempt in range(4096):
        material = hashlib.sha256(
            b"MORPH-KEM M2 core matching v1\x00"
            + seed
            + attempt.to_bytes(4, "big")
        ).digest()
        order = _permutation(vertices, material)
        matching: list[Simplex] = []
        valid = True
        for left, right in zip(order[::2], order[1::2]):
            candidate = _edge(left, right)
            if candidate in cycle_edges:
                valid = False
                break
            matching.append(candidate)
        if valid:
            return SimplicialComplex.from_facets(
                sorted(cycle_edges | set(matching))
            )
    raise MazeExperimentError("could not generate a valid 3-regular hidden core")


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
        trap_edges = sum(edge in facet_edges for edge in present)
        if trap_edges == 0:
            continue
        candidates.append((missing[0], tau, trap_edges))
    return tuple(candidates)


def _relabel_simplex(simplex: Simplex, mapping: tuple[int, ...]) -> Simplex:
    return tuple(sorted(mapping[vertex] for vertex in simplex))


def _expected_core_simplex_count(parameters: MazeParameters) -> int:
    return parameters.vertices + (3 * parameters.vertices // 2)


def generate_maze(
    parameters: MazeParameters,
    master_seed: bytes,
) -> tuple[MazePublicInstance, MazeTrapdoor]:
    parameters.validate()
    if not isinstance(master_seed, bytes) or not master_seed:
        raise MazeExperimentError("master_seed must be non-empty bytes")

    for generation_attempt in range(256):
        attempt_seed = hashlib.sha256(
            b"MORPH-KEM M2 generation attempt v1\x00"
            + parameters.name.encode("ascii")
            + b"\x00"
            + master_seed
            + generation_attempt.to_bytes(4, "big")
        ).digest()
        core = _three_regular_core(parameters.vertices, attempt_seed)
        state = core
        expansion_steps: list[CollapsePair] = []
        rng = _DeterministicRng(
            hashlib.sha256(
                b"MORPH-KEM M2 expansion chooser v1\x00" + attempt_seed
            ).digest()
        )

        for _ in range(parameters.expansions):
            candidates = _expansion_candidates(state, parameters.vertices)
            if not candidates:
                break
            best_trap_count = max(candidate[2] for candidate in candidates)
            pool = [
                candidate
                for candidate in candidates
                if candidate[2] == best_trap_count
            ]
            sigma, tau, _ = pool[rng.randbelow(len(pool))]
            state = state.elementary_expand(sigma, tau)
            expansion_steps.append((sigma, tau))

        if len(expansion_steps) != parameters.expansions:
            continue

        relabeling = _permutation(
            parameters.vertices,
            hashlib.sha256(
                b"MORPH-KEM M2 final relabeling v1\x00" + attempt_seed
            ).digest(),
        )
        relabeled_core = core.relabel(relabeling)
        relabeled_target = state.relabel(relabeling)
        certificate = tuple(
            (
                _relabel_simplex(sigma, relabeling),
                _relabel_simplex(tau, relabeling),
            )
            for sigma, tau in reversed(expansion_steps)
        )

        if len(relabeled_target.free_collapse_pairs()) < parameters.min_initial_free_pairs:
            continue

        public = MazePublicInstance(
            parameters=parameters,
            target=relabeled_target,
            core_digest=_core_digest(relabeled_core),
        )
        trapdoor = MazeTrapdoor(
            core=relabeled_core,
            certificate=certificate,
            public_fingerprint=public.fingerprint,
        )

        reduced = planted_reduce(public, trapdoor)
        if reduced != relabeled_core:
            raise MazeExperimentError("internal M2 planted-certificate verification failed")
        return public, trapdoor

    raise MazeExperimentError("could not generate an M2 instance with requested branching")


def verify_core(public: MazePublicInstance, candidate: SimplicialComplex) -> bool:
    return hmac.compare_digest(public.core_digest, _core_digest(candidate))


def planted_reduce(
    public: MazePublicInstance,
    trapdoor: MazeTrapdoor,
) -> SimplicialComplex:
    if public.fingerprint != trapdoor.public_fingerprint:
        raise MazeExperimentError("M2 trapdoor is bound to a different public instance")
    if len(trapdoor.certificate) != public.parameters.expansions:
        raise MazeExperimentError("M2 certificate length does not match parameters")

    state = public.target
    for sigma, tau in trapdoor.certificate:
        state = state.collapse(sigma, tau)

    if state != trapdoor.core or not verify_core(public, state):
        raise MazeExperimentError("M2 planted certificate did not reach the bound hidden core")
    return state


def planted_reduction_metrics(
    public: MazePublicInstance,
    trapdoor: MazeTrapdoor,
) -> PlantedReductionMetrics:
    if public.fingerprint != trapdoor.public_fingerprint:
        raise MazeExperimentError("M2 trapdoor is bound to a different public instance")

    state = public.target
    counts: list[int] = []
    ranks: list[int] = []
    for pair in trapdoor.certificate:
        available = state.free_collapse_pairs()
        counts.append(len(available))
        try:
            ranks.append(available.index(pair) + 1)
        except ValueError as exc:
            raise MazeExperimentError("planted collapse is not free at its certificate step") from exc
        state = state.collapse(*pair)

    if state != trapdoor.core:
        raise MazeExperimentError("planted metric walk did not reach hidden core")
    return PlantedReductionMetrics(
        steps=len(trapdoor.certificate),
        initial_free_pairs=counts[0],
        min_free_pairs=min(counts),
        max_free_pairs=max(counts),
        mean_free_pairs=mean(counts),
        mean_planted_rank=mean(ranks),
    )


def _choose_greedy_pair(
    state: SimplicialComplex,
    pairs: tuple[CollapsePair, ...],
    strategy: str,
    rng: _DeterministicRng | None,
) -> tuple[CollapsePair, SimplicialComplex | None]:
    if strategy == "lex":
        return pairs[0], None
    if strategy == "reverse":
        return pairs[-1], None
    if strategy == "random":
        assert rng is not None
        return pairs[rng.randbelow(len(pairs))], None
    if strategy == "max-branch":
        scored: list[tuple[int, CollapsePair, SimplicialComplex]] = []
        for pair in pairs:
            candidate = state.collapse(*pair)
            scored.append(
                (len(candidate.free_collapse_pairs()), pair, candidate)
            )
        best_score = max(item[0] for item in scored)
        best = min(
            (item for item in scored if item[0] == best_score),
            key=lambda item: item[1],
        )
        return best[1], best[2]
    raise MazeExperimentError(f"unknown M2 greedy strategy: {strategy}")


def greedy_reduce(
    public: MazePublicInstance,
    strategy: str = "lex",
    attack_seed: bytes = b"M2-greedy",
) -> GreedyResult:
    if strategy == "random" and not attack_seed:
        raise MazeExperimentError("random greedy attack requires a non-empty attack seed")

    rng = _DeterministicRng(
        hashlib.sha256(
            b"MORPH-KEM M2 greedy attack v1\x00" + attack_seed
        ).digest()
    ) if strategy == "random" else None

    state = public.target
    initial_free_pairs = len(state.free_collapse_pairs())
    max_free_pairs = initial_free_pairs
    collapses = 0

    while True:
        pairs = state.free_collapse_pairs()
        if not pairs:
            break
        max_free_pairs = max(max_free_pairs, len(pairs))
        pair, precomputed = _choose_greedy_pair(state, pairs, strategy, rng)
        state = precomputed if precomputed is not None else state.collapse(*pair)
        collapses += 1

    return GreedyResult(
        residual=state,
        collapses=collapses,
        initial_free_pairs=initial_free_pairs,
        max_free_pairs=max_free_pairs,
        verified_core=verify_core(public, state),
    )


def random_greedy_survey(
    public: MazePublicInstance,
    trials: int = 64,
    attack_seed: bytes = b"M2-survey",
) -> GreedySurvey:
    if trials <= 0 or trials > 10_000:
        raise MazeExperimentError("M2 survey trials must be in [1, 10000]")
    if not attack_seed:
        raise MazeExperimentError("M2 survey requires a non-empty attack seed")

    residuals: set[bytes] = set()
    residual_sizes: list[int] = []
    collapse_counts: list[int] = []
    core_hits = 0

    for trial in range(trials):
        trial_seed = hashlib.sha256(
            b"MORPH-KEM M2 survey trial v1\x00"
            + attack_seed
            + trial.to_bytes(8, "big")
        ).digest()
        result = greedy_reduce(public, strategy="random", attack_seed=trial_seed)
        residuals.add(result.residual.encode())
        residual_sizes.append(len(result.residual.simplices))
        collapse_counts.append(result.collapses)
        core_hits += int(result.verified_core)

    return GreedySurvey(
        trials=trials,
        core_hits=core_hits,
        unique_residuals=len(residuals),
        min_residual_simplices=min(residual_sizes),
        max_residual_simplices=max(residual_sizes),
        mean_collapses=mean(collapse_counts),
    )


def bounded_core_search(
    public: MazePublicInstance,
    max_nodes: int = 10_000,
) -> SearchResult:
    if max_nodes <= 0 or max_nodes > 2_000_000:
        raise MazeExperimentError("M2 search max_nodes must be in [1, 2000000]")

    target_key = public.target.encode()
    stack: list[tuple[SimplicialComplex, tuple[CollapsePair, ...]]] = [
        (public.target, ())
    ]
    visited: set[bytes] = {target_key}
    nodes = 0
    max_frontier = 1
    min_simplices_seen = len(public.target.simplices)
    expected_core_size = _expected_core_simplex_count(public.parameters)

    while stack and nodes < max_nodes:
        state, path = stack.pop()
        nodes += 1
        size = len(state.simplices)
        min_simplices_seen = min(min_simplices_seen, size)

        if size == expected_core_size and verify_core(public, state):
            return SearchResult(
                found=True,
                certificate=path,
                nodes=nodes,
                visited_states=len(visited),
                max_frontier=max_frontier,
                min_simplices_seen=min_simplices_seen,
                exhausted=False,
            )
        if size <= expected_core_size:
            continue

        pairs = state.free_collapse_pairs()
        for pair in reversed(pairs):
            candidate = state.collapse(*pair)
            if len(candidate.simplices) < expected_core_size:
                continue
            key = candidate.encode()
            if key in visited:
                continue
            visited.add(key)
            stack.append((candidate, path + (pair,)))
        max_frontier = max(max_frontier, len(stack))

    return SearchResult(
        found=False,
        certificate=(),
        nodes=nodes,
        visited_states=len(visited),
        max_frontier=max_frontier,
        min_simplices_seen=min_simplices_seen,
        exhausted=not stack,
    )


def recover_three_regular_core(
    public: MazePublicInstance,
    max_nodes: int = 1_000_000,
) -> CoreRecoveryResult:
    """Recover the M2 hidden core from its public generator invariant.

    Every non-core edge is introduced together with a filled triangle.
    Therefore any target edge that belongs to no 2-simplex is forced to be a
    core edge. The remaining search enumerates 3-regular spanning subgraphs of
    the public 1-skeleton and uses the public core digest as an exact verifier.
    """
    if max_nodes <= 0 or max_nodes > 20_000_000:
        raise MazeExperimentError(
            "M2 degree-core search max_nodes must be in [1, 20000000]"
        )

    vertices = public.parameters.vertices
    all_edges = tuple(
        simplex for simplex in public.target.simplices if len(simplex) == 2
    )
    triangles = tuple(
        simplex for simplex in public.target.simplices if len(simplex) == 3
    )
    triangle_edges: set[Simplex] = set()
    for triangle in triangles:
        triangle_edges.update(combinations(triangle, 2))

    forced = tuple(sorted(edge for edge in all_edges if edge not in triangle_edges))
    optional = list(sorted(edge for edge in all_edges if edge in triangle_edges))

    degrees = [0] * vertices
    chosen: list[Simplex] = []
    for left, right in forced:
        degrees[left] += 1
        degrees[right] += 1
        chosen.append((left, right))
    if any(degree > 3 for degree in degrees):
        return CoreRecoveryResult(
            found=False,
            core=None,
            nodes=0,
            degree_candidates=0,
            forced_edges=len(forced),
            optional_edges=len(optional),
            exhausted=True,
        )

    target_degrees = [0] * vertices
    for left, right in all_edges:
        target_degrees[left] += 1
        target_degrees[right] += 1
    optional.sort(
        key=lambda edge: (
            target_degrees[edge[0]] + target_degrees[edge[1]],
            edge,
        )
    )

    suffix_incidence = [[0] * vertices for _ in range(len(optional) + 1)]
    for index in range(len(optional) - 1, -1, -1):
        suffix_incidence[index] = suffix_incidence[index + 1].copy()
        left, right = optional[index]
        suffix_incidence[index][left] += 1
        suffix_incidence[index][right] += 1

    required_edges = 3 * vertices // 2
    nodes = 0
    degree_candidates = 0
    found_core: SimplicialComplex | None = None

    def search(index: int) -> None:
        nonlocal nodes, degree_candidates, found_core
        if found_core is not None or nodes >= max_nodes:
            return
        nodes += 1

        if len(chosen) > required_edges:
            return
        if len(chosen) + (len(optional) - index) < required_edges:
            return
        for vertex in range(vertices):
            if degrees[vertex] > 3:
                return
            if degrees[vertex] + suffix_incidence[index][vertex] < 3:
                return

        if index == len(optional):
            if len(chosen) != required_edges or any(
                degree != 3 for degree in degrees
            ):
                return
            degree_candidates += 1
            candidate = SimplicialComplex.from_facets(chosen)
            if verify_core(public, candidate):
                found_core = candidate
            return

        left, right = optional[index]

        if degrees[left] < 3 and degrees[right] < 3:
            chosen.append((left, right))
            degrees[left] += 1
            degrees[right] += 1
            search(index + 1)
            degrees[left] -= 1
            degrees[right] -= 1
            chosen.pop()

        search(index + 1)

    search(0)
    return CoreRecoveryResult(
        found=found_core is not None,
        core=found_core,
        nodes=nodes,
        degree_candidates=degree_candidates,
        forced_edges=len(forced),
        optional_edges=len(optional),
        exhausted=found_core is None and nodes < max_nodes,
    )
