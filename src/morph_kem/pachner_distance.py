from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib
import heapq
from statistics import mean

from .pachner import (
    PachnerExperimentError,
    PachnerMove,
    PachnerParameters,
    PachnerPublicInstance,
    PachnerState,
    _rich_burn_in,
    legal_moves,
    unique_neighbors,
    verify_pachner_witness,
)

Facets = tuple[tuple[int, int, int, int], ...]


@dataclass(frozen=True, slots=True)
class DistanceParameters:
    name: str
    burn_in_14: int
    distance: int
    max_ball_states: int
    path_count_cap: int = 1_000_000

    def validate(self) -> None:
        if not 1 <= self.burn_in_14 <= 6:
            raise PachnerExperimentError("T1 burn-in outside toy bounds")
        if not 1 <= self.distance <= 12:
            raise PachnerExperimentError("T1 distance outside toy bounds")
        if self.max_ball_states < 100 or self.max_ball_states > 2_000_000:
            raise PachnerExperimentError("T1 ball-state cap outside toy bounds")
        if self.path_count_cap < 1 or self.path_count_cap > 1_000_000_000:
            raise PachnerExperimentError("T1 path-count cap outside bounds")


T1_PARAMETER_SETS = {
    "t1-2": DistanceParameters("t1-2", burn_in_14=4, distance=2, max_ball_states=20_000),
    "t1-3": DistanceParameters("t1-3", burn_in_14=4, distance=3, max_ball_states=80_000),
}


@dataclass(frozen=True, slots=True)
class DistanceShellProfile:
    depth: int
    shell_sizes: tuple[int, ...]
    ball_size: int
    expanded_states: int
    raw_moves: int
    unique_neighbors: int
    local_neighbor_collisions: int
    revisit_hits: int
    max_frontier: int
    tetrahedron_histograms: tuple[tuple[tuple[int, int], ...], ...]
    mean_tetrahedron_slack: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class DistanceReference:
    exact_distance: int
    shortest_path: tuple[PachnerMove, ...]
    shortest_paths_capped: int
    shortest_path_count_capped: bool
    shortest_predecessors: int
    target_tetrahedron_delta: int
    target_tetrahedron_slack: int
    max_shell_tetrahedron_slack: int
    max_slack_candidates: int
    min_path_candidates: int
    profile: DistanceShellProfile


@dataclass(frozen=True, slots=True)
class AStarResult:
    found: bool
    moves: tuple[PachnerMove, ...]
    distance: int | None
    visited_states: int
    expanded_states: int
    max_frontier: int


@dataclass(slots=True)
class _ShellData:
    profile: DistanceShellProfile
    states: dict[Facets, PachnerState]
    distance: dict[Facets, int]
    parent: dict[Facets, tuple[Facets, PachnerMove] | None]
    shortest_paths: dict[Facets, int]
    shortest_predecessors: dict[Facets, int]
    path_count_capped: set[Facets]
    levels: tuple[tuple[Facets, ...], ...]


class _DeterministicRng:
    def __init__(self, seed: bytes):
        self._seed = seed
        self._counter = 0

    def randbelow(self, upper: int) -> int:
        if upper <= 0:
            raise ValueError("upper must be positive")
        limit = (1 << 256) - ((1 << 256) % upper)
        while True:
            block = hashlib.sha256(
                b"MORPH-KEM T1 rng v1\x00"
                + self._seed
                + self._counter.to_bytes(8, "big")
            ).digest()
            self._counter += 1
            value = int.from_bytes(block, "big")
            if value < limit:
                return value % upper


def _build_shell(
    start: PachnerState,
    depth: int,
    max_states: int,
    path_count_cap: int,
) -> _ShellData:
    if depth < 0 or depth > 12:
        raise PachnerExperimentError("T1 shell depth outside toy bounds")
    if max_states <= 0:
        raise PachnerExperimentError("T1 shell state cap must be positive")
    if path_count_cap <= 0:
        raise PachnerExperimentError("T1 path-count cap must be positive")

    states: dict[Facets, PachnerState] = {start.facets: start}
    distance: dict[Facets, int] = {start.facets: 0}
    parent: dict[Facets, tuple[Facets, PachnerMove] | None] = {start.facets: None}
    shortest_paths: dict[Facets, int] = {start.facets: 1}
    shortest_predecessors: dict[Facets, int] = {start.facets: 0}
    capped: set[Facets] = set()
    levels: list[tuple[Facets, ...]] = [(start.facets,)]

    expanded_states = 0
    raw_moves = 0
    unique_neighbor_count = 0
    local_neighbor_collisions = 0
    revisit_hits = 0
    max_frontier = 1

    for current_depth in range(depth):
        next_level: set[Facets] = set()
        for key in levels[current_depth]:
            current = states[key]
            expanded_states += 1
            raw = len(legal_moves(current))
            neighbors = unique_neighbors(current)
            raw_moves += raw
            unique_neighbor_count += len(neighbors)
            local_neighbor_collisions += raw - len(neighbors)

            for move, neighbor in neighbors:
                nkey = neighbor.facets
                candidate_depth = current_depth + 1
                known_depth = distance.get(nkey)
                if known_depth is None:
                    if len(states) >= max_states:
                        raise PachnerExperimentError(
                            "T1 exact shell exceeded state cap; refusing incomplete distance certificate"
                        )
                    states[nkey] = neighbor
                    distance[nkey] = candidate_depth
                    parent[nkey] = (key, move)
                    count = shortest_paths[key]
                    if count >= path_count_cap or key in capped:
                        count = path_count_cap
                        capped.add(nkey)
                    shortest_paths[nkey] = count
                    shortest_predecessors[nkey] = 1
                    next_level.add(nkey)
                elif known_depth == candidate_depth:
                    revisit_hits += 1
                    shortest_predecessors[nkey] += 1
                    old = shortest_paths[nkey]
                    add = shortest_paths[key]
                    total = old + add
                    if total >= path_count_cap or nkey in capped or key in capped:
                        shortest_paths[nkey] = path_count_cap
                        capped.add(nkey)
                    else:
                        shortest_paths[nkey] = total
                else:
                    revisit_hits += 1

        levels.append(tuple(sorted(next_level)))
        max_frontier = max(max_frontier, len(next_level))

    shell_sizes = tuple(len(level) for level in levels)
    histograms: list[tuple[tuple[int, int], ...]] = []
    mean_slack: list[float] = []
    start_tets = start.tetrahedra
    for d, level in enumerate(levels):
        counts = Counter(states[key].tetrahedra for key in level)
        histograms.append(tuple(sorted(counts.items())))
        slacks = [d - abs(states[key].tetrahedra - start_tets) for key in level]
        mean_slack.append(mean(slacks) if slacks else 0.0)

    profile = DistanceShellProfile(
        depth=depth,
        shell_sizes=shell_sizes,
        ball_size=len(states),
        expanded_states=expanded_states,
        raw_moves=raw_moves,
        unique_neighbors=unique_neighbor_count,
        local_neighbor_collisions=local_neighbor_collisions,
        revisit_hits=revisit_hits,
        max_frontier=max_frontier,
        tetrahedron_histograms=tuple(histograms),
        mean_tetrahedron_slack=tuple(mean_slack),
    )
    return _ShellData(
        profile=profile,
        states=states,
        distance=distance,
        parent=parent,
        shortest_paths=shortest_paths,
        shortest_predecessors=shortest_predecessors,
        path_count_capped=capped,
        levels=tuple(levels),
    )


def profile_distance_shell(
    start: PachnerState,
    depth: int,
    max_states: int = 100_000,
    path_count_cap: int = 1_000_000,
) -> DistanceShellProfile:
    return _build_shell(start, depth, max_states, path_count_cap).profile


def exact_shell_states(
    start: PachnerState,
    depth: int,
    max_states: int = 100_000,
) -> tuple[PachnerState, ...]:
    data = _build_shell(start, depth, max_states, 1_000_000)
    return tuple(data.states[key] for key in data.levels[depth])


def _reconstruct_path(
    target: Facets,
    parent: dict[Facets, tuple[Facets, PachnerMove] | None],
) -> tuple[PachnerMove, ...]:
    moves: list[PachnerMove] = []
    cursor = target
    while parent[cursor] is not None:
        previous, move = parent[cursor]
        moves.append(move)
        cursor = previous
    moves.reverse()
    return tuple(moves)


def generate_distance_instance(
    parameters: DistanceParameters,
    master_seed: bytes,
) -> tuple[PachnerPublicInstance, DistanceReference]:
    parameters.validate()
    if not isinstance(master_seed, bytes) or not master_seed:
        raise PachnerExperimentError("T1 master seed must be non-empty bytes")

    start = _rich_burn_in(parameters.burn_in_14)
    data = _build_shell(
        start,
        parameters.distance,
        parameters.max_ball_states,
        parameters.path_count_cap,
    )
    shell = data.levels[parameters.distance]
    if not shell:
        raise PachnerExperimentError("T1 requested exact-distance shell is empty")

    start_tets = start.tetrahedra
    slack_by_key = {
        key: parameters.distance - abs(data.states[key].tetrahedra - start_tets)
        for key in shell
    }
    max_slack = max(slack_by_key.values())
    slack_candidates = [key for key in shell if slack_by_key[key] == max_slack]

    # Hard-region sampling is explicit: first avoid targets whose exact distance
    # is almost certified by tetrahedron count, then avoid unusually high
    # shortest-path multiplicity. This is a calibration distribution, not a
    # security claim.
    min_paths = min(data.shortest_paths[key] for key in slack_candidates)
    finalists = sorted(
        key for key in slack_candidates if data.shortest_paths[key] == min_paths
    )
    rng = _DeterministicRng(
        hashlib.sha256(
            b"MORPH-KEM T1 hard-shell target v1\x00"
            + parameters.name.encode("ascii")
            + b"\x00"
            + master_seed
        ).digest()
    )
    target_key = finalists[rng.randbelow(len(finalists))]
    target = data.states[target_key]
    path = _reconstruct_path(target_key, data.parent)

    public_parameters = PachnerParameters(
        parameters.name,
        parameters.burn_in_14,
        parameters.distance,
    )
    public = PachnerPublicInstance(
        public_parameters,
        start,
        target,
        parameters.distance,
    )
    if len(path) != parameters.distance or not verify_pachner_witness(public, path):
        raise PachnerExperimentError("T1 internal exact-distance witness failed")

    delta = abs(target.tetrahedra - start_tets)
    reference = DistanceReference(
        exact_distance=parameters.distance,
        shortest_path=path,
        shortest_paths_capped=data.shortest_paths[target_key],
        shortest_path_count_capped=target_key in data.path_count_capped,
        shortest_predecessors=data.shortest_predecessors[target_key],
        target_tetrahedron_delta=delta,
        target_tetrahedron_slack=parameters.distance - delta,
        max_shell_tetrahedron_slack=max_slack,
        max_slack_candidates=len(slack_candidates),
        min_path_candidates=len(finalists),
        profile=data.profile,
    )
    return public, reference


def _tetrahedron_heuristic(state: PachnerState, target: PachnerState) -> int:
    # Every challenge move changes the tetrahedron count by exactly one.
    return abs(state.tetrahedra - target.tetrahedra)


def astar_tetrahedron_recover(
    public: PachnerPublicInstance,
    max_states: int = 100_000,
) -> AStarResult:
    if max_states <= 0:
        raise PachnerExperimentError("T1 A* state cap must be positive")

    start = public.start
    target = public.target
    start_key = start.facets
    target_key = target.facets
    if start_key == target_key:
        return AStarResult(True, (), 0, 1, 0, 1)

    best_g: dict[Facets, int] = {start_key: 0}
    parent: dict[Facets, tuple[Facets, PachnerMove] | None] = {start_key: None}
    states: dict[Facets, PachnerState] = {start_key: start}
    counter = 0
    heap: list[tuple[int, int, int, Facets]] = []
    h0 = _tetrahedron_heuristic(start, target)
    heapq.heappush(heap, (h0, h0, counter, start_key))
    expanded = 0
    max_frontier = 1

    while heap:
        _, _, _, key = heapq.heappop(heap)
        current = states[key]
        g = best_g[key]
        if key == target_key:
            moves = _reconstruct_path(key, parent)
            return AStarResult(
                True,
                moves,
                len(moves),
                len(best_g),
                expanded,
                max_frontier,
            )
        if g >= public.bound:
            continue

        expanded += 1
        for move, neighbor in unique_neighbors(current):
            nkey = neighbor.facets
            ng = g + 1
            if ng > public.bound or ng >= best_g.get(nkey, 1 << 30):
                continue
            if nkey not in best_g and len(best_g) >= max_states:
                return AStarResult(False, (), None, len(best_g), expanded, max_frontier)
            best_g[nkey] = ng
            parent[nkey] = (key, move)
            states[nkey] = neighbor
            h = _tetrahedron_heuristic(neighbor, target)
            counter += 1
            heapq.heappush(heap, (ng + h, h, counter, nkey))
        max_frontier = max(max_frontier, len(heap))

    return AStarResult(False, (), None, len(best_g), expanded, max_frontier)
