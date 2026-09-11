from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass
from functools import lru_cache
import hashlib
from itertools import combinations, permutations

from .gluing import _DeterministicRng
from .tdc_cycle_code import _gf2_rank


class TDC1Error(ValueError):
    """Raised when a TDC1 toy experiment is malformed."""


Edge = tuple[int, int]


@dataclass(frozen=True, slots=True)
class TDC1Parameters:
    name: str
    lift_factor: int
    error_weights: tuple[int, ...]
    max_generation_attempts: int = 128

    def validate(self) -> None:
        if self.lift_factor < 4 or self.lift_factor > 64:
            raise TDC1Error("TDC1 lift factor outside toy bounds")
        if not self.error_weights or any(weight < 1 or weight > 8 for weight in self.error_weights):
            raise TDC1Error("TDC1 error weights outside toy bounds")
        if tuple(sorted(set(self.error_weights))) != self.error_weights:
            raise TDC1Error("TDC1 error weights must be sorted and distinct")
        if self.max_generation_attempts < 1 or self.max_generation_attempts > 512:
            raise TDC1Error("TDC1 generation-attempt cap outside toy bounds")

    @property
    def vertex_count(self) -> int:
        return 4 * self.lift_factor


TDC1_PARAMETER_SETS = {
    "tdc1-L8": TDC1Parameters("tdc1-L8", 8, (1, 2, 3, 4)),
    "tdc1-L12": TDC1Parameters("tdc1-L12", 12, (1, 2, 3, 4)),
    "tdc1-L18": TDC1Parameters("tdc1-L18", 18, (1, 2, 3, 4, 5)),
}


@dataclass(frozen=True, slots=True)
class CubicGraphCode:
    name: str
    vertex_count: int
    edges: tuple[Edge, ...]


@dataclass(frozen=True, slots=True)
class TDC1Instance:
    lifted: CubicGraphCode
    matched_random: CubicGraphCode
    lift_generation_retries: int
    random_generation_retries: int


@dataclass(frozen=True, slots=True)
class GraphicCodeMetrics:
    vertices: int
    edges: int
    parity_rank: int
    code_dimension: int
    rate: float
    degree_histogram: tuple[tuple[int, int], ...]
    girth: int
    triangle_count: int
    four_cycle_count: int


@dataclass(frozen=True, slots=True)
class QuotientRecovery:
    found: bool
    search_nodes: int
    backtracks: int
    color_class_sizes: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class GraphicDecodeRecovery:
    error_weight: int
    syndrome_weight: int
    bfs_runs: int
    bfs_queue_pops: int
    bfs_edge_scans: int
    matching_dp_states: int
    matching_pair_tests: int
    matching_distance: int
    recovered_error_weight: int
    accepted: bool
    matches_planted_error_after_public_success: bool


def _digest(domain: bytes, seed: bytes, name: str, counter: int = 0) -> bytes:
    return hashlib.sha256(
        domain + b"\x00" + seed + name.encode("ascii") + counter.to_bytes(8, "big")
    ).digest()


def _adjacency(vertex_count: int, edges: tuple[Edge, ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
    rows: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for edge_index, (left, right) in enumerate(edges):
        if left < 0 or right >= vertex_count or left >= right:
            raise TDC1Error("TDC1 graph edge is malformed")
        rows[left].append((right, edge_index))
        rows[right].append((left, edge_index))
    for row in rows:
        row.sort()
    return tuple(tuple(row) for row in rows)


def _is_connected(vertex_count: int, edges: tuple[Edge, ...]) -> bool:
    adjacency = _adjacency(vertex_count, edges)
    seen = {0}
    queue = deque([0])
    while queue:
        current = queue.popleft()
        for neighbor, _ in adjacency[current]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return len(seen) == vertex_count


def _validate_cubic(graph: CubicGraphCode) -> None:
    if len(set(graph.edges)) != len(graph.edges):
        raise TDC1Error("TDC1 graph contains parallel edges")
    adjacency = _adjacency(graph.vertex_count, graph.edges)
    if any(len(row) != 3 for row in adjacency):
        raise TDC1Error("TDC1 graph is not cubic")
    if not _is_connected(graph.vertex_count, graph.edges):
        raise TDC1Error("TDC1 graph is disconnected")


def _lift_k4(params: TDC1Parameters, seed: bytes) -> tuple[CubicGraphCode, int]:
    base_edges = tuple(combinations(range(4), 2))
    for attempt in range(params.max_generation_attempts):
        edges: set[Edge] = set()
        for base_index, (left_role, right_role) in enumerate(base_edges):
            permutation = list(range(params.lift_factor))
            rng = _DeterministicRng(
                b"MORPH-KEM TDC1 K4 lift permutation v1",
                _digest(b"lift", seed, params.name, attempt * 16 + base_index),
            )
            rng.shuffle(permutation)
            for sheet, mapped_sheet in enumerate(permutation):
                left = left_role * params.lift_factor + sheet
                right = right_role * params.lift_factor + mapped_sheet
                edges.add((min(left, right), max(left, right)))
        ordered = tuple(sorted(edges))
        if len(ordered) != 6 * params.lift_factor:
            raise TDC1Error("TDC1 K4 lift lost edges")
        if not _is_connected(params.vertex_count, ordered):
            continue

        labels = list(range(params.vertex_count))
        relabel_rng = _DeterministicRng(
            b"MORPH-KEM TDC1 public relabel v1",
            _digest(b"relabel", seed, params.name, attempt),
        )
        relabel_rng.shuffle(labels)
        relabelled = tuple(
            sorted(
                (min(labels[left], labels[right]), max(labels[left], labels[right]))
                for left, right in ordered
            )
        )
        graph = CubicGraphCode(params.name + "-lift", params.vertex_count, relabelled)
        _validate_cubic(graph)
        return graph, attempt
    raise TDC1Error("TDC1 connected K4 lift attempt cap exhausted")


def _random_cubic(params: TDC1Parameters, seed: bytes) -> tuple[CubicGraphCode, int]:
    for attempt in range(params.max_generation_attempts):
        stubs = [vertex for vertex in range(params.vertex_count) for _ in range(3)]
        rng = _DeterministicRng(
            b"MORPH-KEM TDC1 matched random cubic v1",
            _digest(b"random-cubic", seed, params.name, attempt),
        )
        rng.shuffle(stubs)
        edges: list[Edge] = []
        valid = True
        seen: set[Edge] = set()
        for index in range(0, len(stubs), 2):
            left, right = stubs[index], stubs[index + 1]
            if left == right:
                valid = False
                break
            edge = (min(left, right), max(left, right))
            if edge in seen:
                valid = False
                break
            seen.add(edge)
            edges.append(edge)
        if not valid:
            continue
        ordered = tuple(sorted(edges))
        if not _is_connected(params.vertex_count, ordered):
            continue
        graph = CubicGraphCode(params.name + "-random", params.vertex_count, ordered)
        _validate_cubic(graph)
        return graph, attempt
    raise TDC1Error("TDC1 matched-random cubic attempt cap exhausted")


def generate_tdc1_instance(params: TDC1Parameters, master_seed: bytes) -> TDC1Instance:
    params.validate()
    if len(master_seed) < 16:
        raise TDC1Error("TDC1 master seed must contain at least 128 bits")
    lifted, lift_retries = _lift_k4(params, master_seed)
    random_graph, random_retries = _random_cubic(params, master_seed)
    return TDC1Instance(lifted, random_graph, lift_retries, random_retries)


def _incidence_rows(graph: CubicGraphCode) -> tuple[int, ...]:
    rows = [0] * graph.vertex_count
    for edge_index, (left, right) in enumerate(graph.edges):
        rows[left] |= 1 << edge_index
        rows[right] |= 1 << edge_index
    return tuple(rows)


def syndrome(graph: CubicGraphCode, error_mask: int) -> int:
    value = 0
    for vertex, row in enumerate(_incidence_rows(graph)):
        if (row & error_mask).bit_count() & 1:
            value |= 1 << vertex
    return value


def _girth(graph: CubicGraphCode) -> int:
    adjacency = _adjacency(graph.vertex_count, graph.edges)
    best = graph.vertex_count + 1
    for blocked_index, (source, target) in enumerate(graph.edges):
        distance = [-1] * graph.vertex_count
        distance[source] = 0
        queue = deque([source])
        while queue:
            current = queue.popleft()
            if distance[current] + 1 >= best:
                continue
            for neighbor, edge_index in adjacency[current]:
                if edge_index == blocked_index:
                    continue
                if distance[neighbor] != -1:
                    continue
                distance[neighbor] = distance[current] + 1
                if neighbor == target:
                    best = min(best, distance[neighbor] + 1)
                    queue.clear()
                    break
                queue.append(neighbor)
    if best > graph.vertex_count:
        raise TDC1Error("TDC1 cubic graph unexpectedly has no cycle")
    return best


def _short_cycle_counts(graph: CubicGraphCode) -> tuple[int, int]:
    neighbors = [set() for _ in range(graph.vertex_count)]
    for left, right in graph.edges:
        neighbors[left].add(right)
        neighbors[right].add(left)
    triangles = sum(len(neighbors[left] & neighbors[right]) for left, right in graph.edges) // 3
    four_twice = 0
    for left in range(graph.vertex_count):
        for right in range(left + 1, graph.vertex_count):
            common = len(neighbors[left] & neighbors[right])
            if common >= 2:
                four_twice += common * (common - 1) // 2
    return triangles, four_twice // 2


def graphic_code_metrics(graph: CubicGraphCode) -> GraphicCodeMetrics:
    _validate_cubic(graph)
    rows = _incidence_rows(graph)
    rank = _gf2_rank(list(rows))
    degrees = Counter(len(row) for row in _adjacency(graph.vertex_count, graph.edges))
    triangles, four_cycles = _short_cycle_counts(graph)
    dimension = len(graph.edges) - rank
    return GraphicCodeMetrics(
        vertices=graph.vertex_count,
        edges=len(graph.edges),
        parity_rank=rank,
        code_dimension=dimension,
        rate=dimension / len(graph.edges),
        degree_histogram=tuple(sorted(degrees.items())),
        girth=_girth(graph),
        triangle_count=triangles,
        four_cycle_count=four_cycles,
    )


def recover_k4_quotient(graph: CubicGraphCode, lift_factor: int) -> QuotientRecovery:
    _validate_cubic(graph)
    adjacency = _adjacency(graph.vertex_count, graph.edges)
    neighbors = tuple(tuple(item[0] for item in row) for row in adjacency)
    nodes = 0
    backtracks = 0

    def attempt(seed_colors: tuple[int, int, int]) -> tuple[bool, tuple[int, ...]]:
        nonlocal nodes, backtracks
        colors = [-1] * graph.vertex_count
        class_sizes = [0, 0, 0, 0]
        colors[0] = 0
        class_sizes[0] = 1
        for neighbor, color in zip(neighbors[0], seed_colors):
            colors[neighbor] = color
            class_sizes[color] += 1

        def possible(vertex: int) -> tuple[int, ...]:
            forbidden = {colors[n] for n in neighbors[vertex] if colors[n] >= 0}
            values = []
            for color in range(4):
                if color in forbidden or class_sizes[color] >= lift_factor:
                    continue
                ok = True
                for neighbor in neighbors[vertex]:
                    if colors[neighbor] != -1:
                        continue
                    seen = [colors[x] for x in neighbors[neighbor] if colors[x] >= 0]
                    if color in seen:
                        ok = False
                        break
                if ok:
                    values.append(color)
            return tuple(values)

        def valid_complete() -> bool:
            if class_sizes != [lift_factor] * 4:
                return False
            for vertex, color in enumerate(colors):
                if {colors[n] for n in neighbors[vertex]} != ({0, 1, 2, 3} - {color}):
                    return False
            return True

        def search() -> bool:
            nonlocal nodes, backtracks
            nodes += 1
            if all(color >= 0 for color in colors):
                return valid_complete()
            best_vertex = -1
            best_values: tuple[int, ...] | None = None
            for vertex, color in enumerate(colors):
                if color >= 0:
                    continue
                values = possible(vertex)
                if not values:
                    backtracks += 1
                    return False
                if best_values is None or (len(values), vertex) < (len(best_values), best_vertex):
                    best_vertex = vertex
                    best_values = values
            if best_values is None:
                return False
            for color in best_values:
                colors[best_vertex] = color
                class_sizes[color] += 1
                if search():
                    return True
                class_sizes[color] -= 1
                colors[best_vertex] = -1
            backtracks += 1
            return False

        found = search()
        return found, tuple(colors) if found else ()

    for seed_colors in permutations((1, 2, 3)):
        found, colors = attempt(seed_colors)
        if found:
            sizes = tuple(colors.count(color) for color in range(4))
            return QuotientRecovery(True, nodes, backtracks, sizes)
    return QuotientRecovery(False, nodes, backtracks, ())


def _shortest_paths(
    graph: CubicGraphCode, source: int
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...], int, int]:
    adjacency = _adjacency(graph.vertex_count, graph.edges)
    distance = [-1] * graph.vertex_count
    parent = [-1] * graph.vertex_count
    parent_edge = [-1] * graph.vertex_count
    distance[source] = 0
    parent[source] = source
    queue = deque([source])
    pops = 0
    scans = 0
    while queue:
        current = queue.popleft()
        pops += 1
        for neighbor, edge_index in adjacency[current]:
            scans += 1
            if distance[neighbor] != -1:
                continue
            distance[neighbor] = distance[current] + 1
            parent[neighbor] = current
            parent_edge[neighbor] = edge_index
            queue.append(neighbor)
    return tuple(distance), tuple(parent), tuple(parent_edge), pops, scans


def _path_edges(source: int, target: int, parent: tuple[int, ...], parent_edge: tuple[int, ...]) -> tuple[int, ...]:
    path: list[int] = []
    current = target
    while current != source:
        edge = parent_edge[current]
        if edge < 0:
            raise TDC1Error("TDC1 shortest-path reconstruction failed")
        path.append(edge)
        current = parent[current]
    path.reverse()
    return tuple(path)


def _minimum_t_join(graph: CubicGraphCode, defects: tuple[int, ...]) -> tuple[int, int, int, int, int, int]:
    if len(defects) % 2:
        raise TDC1Error("TDC1 syndrome has odd weight")
    if len(defects) > 16:
        raise TDC1Error("TDC1 exact decoder defect cap exceeded")
    if not defects:
        return 0, 0, 1, 0, 0, 0

    distance_rows: list[tuple[int, ...]] = []
    parents: list[tuple[int, ...]] = []
    parent_edges: list[tuple[int, ...]] = []
    pops = 0
    scans = 0
    for defect in defects:
        distance, parent, edge_parent, one_pops, one_scans = _shortest_paths(graph, defect)
        distance_rows.append(distance)
        parents.append(parent)
        parent_edges.append(edge_parent)
        pops += one_pops
        scans += one_scans

    pair_distance: dict[tuple[int, int], int] = {}
    pair_path: dict[tuple[int, int], tuple[int, ...]] = {}
    for left in range(len(defects)):
        for right in range(left + 1, len(defects)):
            pair_distance[(left, right)] = distance_rows[left][defects[right]]
            pair_path[(left, right)] = _path_edges(
                defects[left], defects[right], parents[left], parent_edges[left]
            )

    states = 0
    tests = 0

    @lru_cache(maxsize=None)
    def solve(mask: int) -> tuple[int, tuple[tuple[int, int], ...]]:
        nonlocal states, tests
        states += 1
        if mask == 0:
            return 0, ()
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        remainder = mask ^ first_bit
        best: tuple[int, tuple[tuple[int, int], ...]] | None = None
        probe = remainder
        while probe:
            bit = probe & -probe
            second = bit.bit_length() - 1
            tests += 1
            key = (first, second)
            tail_distance, tail_pairs = solve(remainder ^ bit)
            candidate = (pair_distance[key] + tail_distance, (key,) + tail_pairs)
            if best is None or candidate < best:
                best = candidate
            probe ^= bit
        if best is None:
            raise TDC1Error("TDC1 matching DP failed")
        return best

    distance, pairs = solve((1 << len(defects)) - 1)
    correction = 0
    for pair in pairs:
        for edge_index in pair_path[pair]:
            correction ^= 1 << edge_index
    return correction, distance, states, tests, pops, scans


def planted_error_mask(graph: CubicGraphCode, weight: int, seed: bytes) -> int:
    if weight < 1 or weight > len(graph.edges):
        raise TDC1Error("TDC1 planted error weight outside graph bounds")
    ordered = sorted(
        range(len(graph.edges)),
        key=lambda index: (hashlib.sha256(seed + graph.name.encode("ascii") + index.to_bytes(4, "big")).digest(), index),
    )
    return sum(1 << edge_index for edge_index in ordered[:weight])


def decode_graphic_error(
    graph: CubicGraphCode,
    error_mask: int,
) -> GraphicDecodeRecovery:
    observed_syndrome = syndrome(graph, error_mask)
    defects = tuple(vertex for vertex in range(graph.vertex_count) if (observed_syndrome >> vertex) & 1)
    correction, distance, states, tests, pops, scans = _minimum_t_join(graph, defects)
    accepted = syndrome(graph, correction) == observed_syndrome
    return GraphicDecodeRecovery(
        error_weight=error_mask.bit_count(),
        syndrome_weight=len(defects),
        bfs_runs=len(defects),
        bfs_queue_pops=pops,
        bfs_edge_scans=scans,
        matching_dp_states=states,
        matching_pair_tests=tests,
        matching_distance=distance,
        recovered_error_weight=correction.bit_count(),
        accepted=accepted,
        matches_planted_error_after_public_success=correction == error_mask,
    )
