from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from itertools import permutations
from statistics import mean

Edge = tuple[int, int]
Perm = tuple[int, int, int]


class HolonomyExperimentError(ValueError):
    """Raised when an H1 signed-holonomy experiment input is invalid."""


@dataclass(frozen=True, slots=True)
class HolonomyParameters:
    name: str
    vertices: int
    extra_edges: int

    def validate(self) -> None:
        if self.vertices < 6 or self.vertices > 64:
            raise HolonomyExperimentError("H1 vertex count must be in [6, 64]")
        max_extra = self.vertices * (self.vertices - 1) // 2 - self.vertices
        if self.extra_edges <= 0 or self.extra_edges > max_extra:
            raise HolonomyExperimentError("H1 extra-edge count is outside the valid range")


HOLONOMY_PARAMETER_SETS = {
    "h1-8": HolonomyParameters("h1-8", vertices=8, extra_edges=4),
    "h1-10": HolonomyParameters("h1-10", vertices=10, extra_edges=5),
    "h1-12": HolonomyParameters("h1-12", vertices=12, extra_edges=6),
    "h1-16": HolonomyParameters("h1-16", vertices=16, extra_edges=8),
    "h1-20": HolonomyParameters("h1-20", vertices=20, extra_edges=10),
}


@dataclass(frozen=True, slots=True)
class HolonomyGraph:
    vertices: int
    edges: tuple[Edge, ...]

    def __post_init__(self) -> None:
        if self.vertices <= 0:
            raise HolonomyExperimentError("graph must have vertices")
        previous: Edge | None = None
        seen: set[Edge] = set()
        for edge in self.edges:
            if len(edge) != 2:
                raise HolonomyExperimentError("edge must have two endpoints")
            left, right = edge
            if left < 0 or right < 0 or left >= self.vertices or right >= self.vertices:
                raise HolonomyExperimentError("edge endpoint outside graph")
            if left >= right:
                raise HolonomyExperimentError("edges must be canonical and loop-free")
            if edge in seen:
                raise HolonomyExperimentError("duplicate edge")
            if previous is not None and edge <= previous:
                raise HolonomyExperimentError("edges must be sorted canonically")
            previous = edge
            seen.add(edge)
        if not self.edges:
            raise HolonomyExperimentError("graph must contain edges")
        if len(self.spanning_tree_edges()) != self.vertices - 1:
            raise HolonomyExperimentError("graph must be connected")

    @property
    def cycle_rank(self) -> int:
        return len(self.edges) - self.vertices + 1

    def neighbors(self) -> tuple[tuple[int, ...], ...]:
        adjacency: list[list[int]] = [[] for _ in range(self.vertices)]
        for left, right in self.edges:
            adjacency[left].append(right)
            adjacency[right].append(left)
        return tuple(tuple(sorted(values)) for values in adjacency)

    def degree_histogram(self) -> tuple[tuple[int, int], ...]:
        counts: dict[int, int] = {}
        for neighbors in self.neighbors():
            degree = len(neighbors)
            counts[degree] = counts.get(degree, 0) + 1
        return tuple(sorted(counts.items()))

    def spanning_tree_edges(self) -> tuple[Edge, ...]:
        adjacency: list[list[int]] = [[] for _ in range(self.vertices)]
        for left, right in self.edges:
            adjacency[left].append(right)
            adjacency[right].append(left)
        for values in adjacency:
            values.sort()

        seen = {0}
        queue = [0]
        tree: list[Edge] = []
        while queue:
            parent = queue.pop(0)
            for child in adjacency[parent]:
                if child in seen:
                    continue
                seen.add(child)
                queue.append(child)
                tree.append(_edge(parent, child))
        return tuple(sorted(tree))

    def chord_edges(self) -> tuple[Edge, ...]:
        tree = set(self.spanning_tree_edges())
        return tuple(edge for edge in self.edges if edge not in tree)

    def encode(self) -> bytes:
        payload = {
            "edges": [list(edge) for edge in self.edges],
            "vertices": self.vertices,
        }
        return json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")


@dataclass(frozen=True, slots=True)
class Z2PublicInstance:
    parameters: HolonomyParameters
    graph: HolonomyGraph
    labels: tuple[int, ...]
    chord_target: tuple[int, ...]
    version: int = 1

    def __post_init__(self) -> None:
        self.parameters.validate()
        if self.version != 1:
            raise HolonomyExperimentError("unsupported H1-Z2 version")
        if len(self.labels) != len(self.graph.edges):
            raise HolonomyExperimentError("Z2 label count does not match edges")
        if any(label not in (0, 1) for label in self.labels):
            raise HolonomyExperimentError("Z2 labels must be bits")
        if len(self.chord_target) != self.graph.cycle_rank:
            raise HolonomyExperimentError("Z2 target length does not match cycle rank")
        if any(value not in (0, 1) for value in self.chord_target):
            raise HolonomyExperimentError("Z2 target values must be bits")

    def encode(self) -> bytes:
        payload = {
            "chord_target": list(self.chord_target),
            "graph": json.loads(self.graph.encode().decode("ascii")),
            "labels": list(self.labels),
            "parameters": {
                "extra_edges": self.parameters.extra_edges,
                "name": self.parameters.name,
                "vertices": self.parameters.vertices,
            },
            "version": self.version,
        }
        return json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")


@dataclass(frozen=True, slots=True)
class Z2Reference:
    frames: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class Z2Recovery:
    accepted: bool
    frames: tuple[int, ...]
    tree_edges: int
    chord_edges: int
    edge_checks: int


@dataclass(frozen=True, slots=True)
class S3PublicInstance:
    parameters: HolonomyParameters
    graph: HolonomyGraph
    labels: tuple[int, ...]
    version: int = 1

    def __post_init__(self) -> None:
        self.parameters.validate()
        if self.version != 1:
            raise HolonomyExperimentError("unsupported H1-S3 version")
        if len(self.labels) != len(self.graph.edges):
            raise HolonomyExperimentError("S3 label count does not match edges")
        if any(label < 0 or label >= len(S3_ELEMENTS) for label in self.labels):
            raise HolonomyExperimentError("invalid S3 element index")

    def encode(self) -> bytes:
        payload = {
            "allowed_normalized": list(S3_TRANSPOSITIONS),
            "graph": json.loads(self.graph.encode().decode("ascii")),
            "labels": list(self.labels),
            "parameters": {
                "extra_edges": self.parameters.extra_edges,
                "name": self.parameters.name,
                "vertices": self.parameters.vertices,
            },
            "version": self.version,
        }
        return json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")


@dataclass(frozen=True, slots=True)
class S3Reference:
    frames: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class S3Validation:
    accepted: bool
    failed_edge: Edge | None


@dataclass(frozen=True, slots=True)
class AbelianizationLeak:
    consistent: bool
    parities: tuple[int, ...]
    recovered_vertices: int
    edge_checks: int


@dataclass(frozen=True, slots=True)
class S3CspResult:
    accepted: bool
    first_solution: tuple[int, ...] | None
    solutions_found: int
    nodes: int
    backtracks: int
    parity_pruned_domain_mean: float
    hit_solution_cap: bool


class _DeterministicRng:
    def __init__(self, seed: bytes):
        self._seed = seed
        self._counter = 0

    def _block(self) -> bytes:
        block = hashlib.sha256(
            b"MORPH-KEM H1 deterministic rng v1\x00"
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


def _shuffle(values: list, seed: bytes) -> None:
    rng = _DeterministicRng(seed)
    for index in range(len(values) - 1, 0, -1):
        other = rng.randbelow(index + 1)
        values[index], values[other] = values[other], values[index]


def _edge(left: int, right: int) -> Edge:
    return (left, right) if left < right else (right, left)


def generate_holonomy_graph(
    parameters: HolonomyParameters,
    master_seed: bytes,
) -> HolonomyGraph:
    parameters.validate()
    if not isinstance(master_seed, bytes) or not master_seed:
        raise HolonomyExperimentError("master_seed must be non-empty bytes")

    vertices = parameters.vertices
    edges = {
        _edge(vertex, (vertex + 1) % vertices)
        for vertex in range(vertices)
    }
    candidates = [
        (left, right)
        for left in range(vertices)
        for right in range(left + 1, vertices)
        if (left, right) not in edges
    ]
    _shuffle(
        candidates,
        hashlib.sha256(
            b"MORPH-KEM H1 graph chords v1\x00"
            + parameters.name.encode("ascii")
            + b"\x00"
            + master_seed
        ).digest(),
    )
    edges.update(candidates[: parameters.extra_edges])
    return HolonomyGraph(vertices, tuple(sorted(edges)))


def _edge_index(graph: HolonomyGraph) -> dict[Edge, int]:
    return {edge: index for index, edge in enumerate(graph.edges)}


def generate_z2_instance(
    parameters: HolonomyParameters,
    master_seed: bytes,
) -> tuple[Z2PublicInstance, Z2Reference]:
    graph = generate_holonomy_graph(parameters, master_seed)
    rng = _DeterministicRng(
        hashlib.sha256(
            b"MORPH-KEM H1 Z2 generator v1\x00" + master_seed
        ).digest()
    )

    frames = tuple(rng.randbelow(2) for _ in range(graph.vertices))
    tree = set(graph.spanning_tree_edges())
    canonical: dict[Edge, int] = {}
    for edge in graph.edges:
        canonical[edge] = 0 if edge in tree else rng.randbelow(2)

    labels = tuple(
        frames[left] ^ canonical[edge] ^ frames[right]
        for edge in graph.edges
        for left, right in (edge,)
    )
    chord_target = tuple(canonical[edge] for edge in graph.chord_edges())
    public = Z2PublicInstance(parameters, graph, labels, chord_target)
    return public, Z2Reference(frames)


def validate_z2_frames(
    public: Z2PublicInstance,
    frames: tuple[int, ...],
) -> bool:
    if len(frames) != public.graph.vertices or any(value not in (0, 1) for value in frames):
        return False
    tree = set(public.graph.spanning_tree_edges())
    chord_values: list[int] = []
    for edge, label in zip(public.graph.edges, public.labels):
        left, right = edge
        normalized = frames[left] ^ label ^ frames[right]
        if edge in tree:
            if normalized != 0:
                return False
        else:
            chord_values.append(normalized)
    return tuple(chord_values) == public.chord_target


def recover_z2_spanning_tree(public: Z2PublicInstance) -> Z2Recovery:
    graph = public.graph
    labels = {edge: label for edge, label in zip(graph.edges, public.labels)}
    tree_edges = set(graph.spanning_tree_edges())
    adjacency: list[list[int]] = [[] for _ in range(graph.vertices)]
    for edge in tree_edges:
        left, right = edge
        adjacency[left].append(right)
        adjacency[right].append(left)
    for values in adjacency:
        values.sort()

    frames: list[int | None] = [None] * graph.vertices
    frames[0] = 0
    queue = [0]
    edge_checks = 0
    while queue:
        parent = queue.pop(0)
        assert frames[parent] is not None
        for child in adjacency[parent]:
            if frames[child] is not None:
                continue
            label = labels[_edge(parent, child)]
            frames[child] = frames[parent] ^ label
            edge_checks += 1
            queue.append(child)

    recovered = tuple(int(value) for value in frames)
    edge_checks += len(graph.chord_edges())
    return Z2Recovery(
        accepted=validate_z2_frames(public, recovered),
        frames=recovered,
        tree_edges=len(tree_edges),
        chord_edges=len(graph.chord_edges()),
        edge_checks=edge_checks,
    )


S3_ELEMENTS: tuple[Perm, ...] = tuple(permutations((0, 1, 2)))
S3_INDEX = {element: index for index, element in enumerate(S3_ELEMENTS)}
S3_IDENTITY = S3_INDEX[(0, 1, 2)]


def _compose(left: Perm, right: Perm) -> Perm:
    """Return left after right."""
    return tuple(left[right[index]] for index in range(3))


def _inverse(element: Perm) -> Perm:
    result = [0, 0, 0]
    for source, target in enumerate(element):
        result[target] = source
    return tuple(result)  # type: ignore[return-value]


def _s3_mul(left: int, right: int) -> int:
    return S3_INDEX[_compose(S3_ELEMENTS[left], S3_ELEMENTS[right])]


def _s3_inv(element: int) -> int:
    return S3_INDEX[_inverse(S3_ELEMENTS[element])]


def _s3_sign(element: int) -> int:
    perm = S3_ELEMENTS[element]
    inversions = sum(
        perm[left] > perm[right]
        for left in range(3)
        for right in range(left + 1, 3)
    )
    return inversions & 1


S3_TRANSPOSITIONS: tuple[int, ...] = tuple(
    index for index in range(len(S3_ELEMENTS))
    if _s3_sign(index) == 1
)
_S3_TRANSPOSITION_SET = set(S3_TRANSPOSITIONS)


def _normalized_s3(frame_left: int, label: int, frame_right: int) -> int:
    # Public edge is oriented left -> right.
    # Normalized transition = g_right * T * g_left^-1.
    return _s3_mul(
        frame_right,
        _s3_mul(label, _s3_inv(frame_left)),
    )


def generate_s3_instance(
    parameters: HolonomyParameters,
    master_seed: bytes,
) -> tuple[S3PublicInstance, S3Reference]:
    graph = generate_holonomy_graph(parameters, master_seed)
    rng = _DeterministicRng(
        hashlib.sha256(
            b"MORPH-KEM H1 S3 generator v1\x00" + master_seed
        ).digest()
    )
    frames = tuple(rng.randbelow(len(S3_ELEMENTS)) for _ in range(graph.vertices))
    labels: list[int] = []
    for left, right in graph.edges:
        allowed = S3_TRANSPOSITIONS[rng.randbelow(len(S3_TRANSPOSITIONS))]
        # T = g_right^-1 * allowed * g_left
        label = _s3_mul(
            _s3_inv(frames[right]),
            _s3_mul(allowed, frames[left]),
        )
        labels.append(label)

    public = S3PublicInstance(parameters, graph, tuple(labels))
    return public, S3Reference(frames)


def validate_s3_frames(
    public: S3PublicInstance,
    frames: tuple[int, ...],
) -> S3Validation:
    if len(frames) != public.graph.vertices:
        return S3Validation(False, None)
    if any(value < 0 or value >= len(S3_ELEMENTS) for value in frames):
        return S3Validation(False, None)

    for edge, label in zip(public.graph.edges, public.labels):
        left, right = edge
        if _normalized_s3(frames[left], label, frames[right]) not in _S3_TRANSPOSITION_SET:
            return S3Validation(False, edge)
    return S3Validation(True, None)


def recover_s3_abelianization(public: S3PublicInstance) -> AbelianizationLeak:
    # sign(g_right) xor sign(T) xor sign(g_left) = 1
    graph = public.graph
    label_by_edge = {edge: label for edge, label in zip(graph.edges, public.labels)}
    adjacency = graph.neighbors()
    parities: list[int | None] = [None] * graph.vertices
    parities[0] = 0
    queue = [0]
    recovered = 1
    edge_checks = 0

    while queue:
        left = queue.pop(0)
        assert parities[left] is not None
        for right in adjacency[left]:
            edge = _edge(left, right)
            rhs = 1 ^ _s3_sign(label_by_edge[edge])
            expected = parities[left] ^ rhs
            edge_checks += 1
            if parities[right] is None:
                parities[right] = expected
                recovered += 1
                queue.append(right)
            elif parities[right] != expected:
                return AbelianizationLeak(
                    False,
                    tuple(0 if value is None else value for value in parities),
                    recovered,
                    edge_checks,
                )

    return AbelianizationLeak(
        True,
        tuple(int(value) for value in parities),
        recovered,
        edge_checks,
    )


def _compatible_s3(label: int, frame_left: int, frame_right: int) -> bool:
    return _normalized_s3(frame_left, label, frame_right) in _S3_TRANSPOSITION_SET


def solve_s3_csp(
    public: S3PublicInstance,
    solution_cap: int = 64,
) -> S3CspResult:
    if solution_cap <= 0 or solution_cap > 100_000:
        raise HolonomyExperimentError("solution_cap must be in [1, 100000]")

    leak = recover_s3_abelianization(public)
    if not leak.consistent:
        return S3CspResult(False, None, 0, 0, 0, 0.0, False)

    even = {index for index in range(len(S3_ELEMENTS)) if _s3_sign(index) == 0}
    odd = set(range(len(S3_ELEMENTS))) - even
    domains: list[set[int]] = [
        set(even if parity == 0 else odd)
        for parity in leak.parities
    ]
    # The public relation is invariant under common left multiplication.
    # Fix one representative of that gauge orbit.
    domains[0] = {S3_IDENTITY}

    edge_labels = {
        edge: label for edge, label in zip(public.graph.edges, public.labels)
    }
    incident: list[list[Edge]] = [[] for _ in range(public.graph.vertices)]
    for edge in public.graph.edges:
        left, right = edge
        incident[left].append(edge)
        incident[right].append(edge)

    nodes = 0
    backtracks = 0
    solutions: list[tuple[int, ...]] = []
    hit_cap = False
    initial_mean = mean(len(domain) for domain in domains)

    def pair_ok(edge: Edge, left_value: int, right_value: int) -> bool:
        return _compatible_s3(edge_labels[edge], left_value, right_value)

    def prune(current_domains: list[set[int]]) -> bool:
        changed = True
        while changed:
            changed = False
            for edge in public.graph.edges:
                left, right = edge
                left_domain = current_domains[left]
                right_domain = current_domains[right]
                allowed_left = {
                    left_value
                    for left_value in left_domain
                    if any(pair_ok(edge, left_value, right_value) for right_value in right_domain)
                }
                if not allowed_left:
                    return False
                if allowed_left != left_domain:
                    current_domains[left] = allowed_left
                    left_domain = allowed_left
                    changed = True

                allowed_right = {
                    right_value
                    for right_value in right_domain
                    if any(pair_ok(edge, left_value, right_value) for left_value in left_domain)
                }
                if not allowed_right:
                    return False
                if allowed_right != right_domain:
                    current_domains[right] = allowed_right
                    changed = True
        return True

    def search(current_domains: list[set[int]]) -> None:
        nonlocal nodes, backtracks, hit_cap
        if len(solutions) >= solution_cap:
            hit_cap = True
            return

        if not prune(current_domains):
            backtracks += 1
            return

        unresolved = [
            vertex for vertex, domain in enumerate(current_domains)
            if len(domain) > 1
        ]
        if not unresolved:
            candidate = tuple(next(iter(domain)) for domain in current_domains)
            if validate_s3_frames(public, candidate).accepted:
                solutions.append(candidate)
            else:
                backtracks += 1
            return

        vertex = min(
            unresolved,
            key=lambda item: (len(current_domains[item]), -len(incident[item]), item),
        )
        before = len(solutions)
        for value in sorted(current_domains[vertex]):
            if len(solutions) >= solution_cap:
                hit_cap = True
                return
            nodes += 1
            child = [set(domain) for domain in current_domains]
            child[vertex] = {value}
            search(child)

        if len(solutions) == before:
            backtracks += 1

    search([set(domain) for domain in domains])
    first = solutions[0] if solutions else None
    return S3CspResult(
        accepted=first is not None and validate_s3_frames(public, first).accepted,
        first_solution=first,
        solutions_found=len(solutions),
        nodes=nodes,
        backtracks=backtracks,
        parity_pruned_domain_mean=initial_mean,
        hit_solution_cap=hit_cap,
    )
