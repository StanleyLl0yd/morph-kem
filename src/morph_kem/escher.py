from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from statistics import mean

from .holonomy import HolonomyGraph, HolonomyParameters, generate_holonomy_graph

Edge = tuple[int, int]


class EscherExperimentError(ValueError):
    """Raised when an H2-E Escher-atlas experiment input is invalid."""


@dataclass(frozen=True, slots=True)
class EscherParameters:
    name: str
    vertices: int
    extra_edges: int
    seam_budget: int
    modulus: int = 7

    def validate(self) -> None:
        if self.vertices < 6 or self.vertices > 96:
            raise EscherExperimentError("H2-E vertex count must be in [6, 96]")
        max_extra = self.vertices * (self.vertices - 1) // 2 - self.vertices
        if self.extra_edges <= 0 or self.extra_edges > max_extra:
            raise EscherExperimentError("H2-E extra-edge count is outside the valid range")
        if self.seam_budget <= 0 or self.seam_budget >= self.vertices:
            raise EscherExperimentError("H2-E seam budget must be in [1, vertices)")
        if self.modulus < 3 or self.modulus > 251:
            raise EscherExperimentError("H2-E modulus must be in [3, 251]")


ESCHER_PARAMETER_SETS = {
    "escher-8": EscherParameters("escher-8", vertices=8, extra_edges=4, seam_budget=1),
    "escher-10": EscherParameters("escher-10", vertices=10, extra_edges=5, seam_budget=2),
    "escher-12": EscherParameters("escher-12", vertices=12, extra_edges=6, seam_budget=2),
    "escher-16": EscherParameters("escher-16", vertices=16, extra_edges=8, seam_budget=3),
    "escher-20": EscherParameters("escher-20", vertices=20, extra_edges=10, seam_budget=4),
}


@dataclass(frozen=True, slots=True)
class EscherPublicInstance:
    parameters: EscherParameters
    graph: HolonomyGraph
    increments: tuple[int, ...]
    version: int = 1

    def __post_init__(self) -> None:
        self.parameters.validate()
        if self.version != 1:
            raise EscherExperimentError("unsupported H2-E public-instance version")
        if self.graph.vertices != self.parameters.vertices:
            raise EscherExperimentError("H2-E graph size does not match parameters")
        if len(self.increments) != len(self.graph.edges):
            raise EscherExperimentError("H2-E increment count does not match edges")
        if any(value < 0 or value >= self.parameters.modulus for value in self.increments):
            raise EscherExperimentError("H2-E edge increment is outside the modulus")

    def encode(self) -> bytes:
        payload = {
            "graph": json.loads(self.graph.encode().decode("ascii")),
            "increments": list(self.increments),
            "parameters": {
                "extra_edges": self.parameters.extra_edges,
                "modulus": self.parameters.modulus,
                "name": self.parameters.name,
                "seam_budget": self.parameters.seam_budget,
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
class EscherReference:
    heights: tuple[int, ...]
    planted_seams: tuple[Edge, ...]


@dataclass(frozen=True, slots=True)
class EscherValidation:
    accepted: bool
    failed_edge: Edge | None
    reason: str


@dataclass(frozen=True, slots=True)
class FundamentalSyndrome:
    chord_edges: tuple[Edge, ...]
    values: tuple[int, ...]

    @property
    def nonzero(self) -> int:
        return sum(value != 0 for value in self.values)


@dataclass(frozen=True, slots=True)
class PotentialPropagation:
    balanced: bool
    heights: tuple[int, ...]
    conflict_cycle: tuple[Edge, ...]
    edge_checks: int


@dataclass(frozen=True, slots=True)
class EscherRepairResult:
    found: bool
    seams: tuple[Edge, ...]
    heights: tuple[int, ...]
    minimum_seams: int | None
    nodes: int
    backtracks: int
    max_branch: int
    edge_checks: int
    exhausted: bool


@dataclass(frozen=True, slots=True)
class EscherSweepRow:
    name: str
    vertices: int
    edges: int
    cycle_rank: int
    seam_budget: int
    nonzero_syndromes: int
    found: bool
    minimum_seams: int | None
    nodes: int
    backtracks: int


class _DeterministicRng:
    def __init__(self, seed: bytes):
        self._seed = seed
        self._counter = 0

    def _block(self) -> bytes:
        block = hashlib.sha256(
            b"MORPH-KEM H2-E deterministic rng v1\x00"
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


def _edge_label_map(public: EscherPublicInstance) -> dict[Edge, int]:
    return {
        edge: label
        for edge, label in zip(public.graph.edges, public.increments)
    }


def _oriented_increment(edge: Edge, source: int, target: int, label: int, modulus: int) -> int:
    left, right = edge
    if source == left and target == right:
        return label
    if source == right and target == left:
        return (-label) % modulus
    raise EscherExperimentError("edge orientation does not match endpoints")


def generate_escher_instance(
    parameters: EscherParameters,
    master_seed: bytes,
) -> tuple[EscherPublicInstance, EscherReference]:
    parameters.validate()
    if not isinstance(master_seed, bytes) or not master_seed:
        raise EscherExperimentError("master_seed must be non-empty bytes")

    graph_parameters = HolonomyParameters(
        f"{parameters.name}-graph",
        parameters.vertices,
        parameters.extra_edges,
    )

    for attempt in range(512):
        attempt_seed = hashlib.sha256(
            b"MORPH-KEM H2-E generation attempt v1\x00"
            + parameters.name.encode("ascii")
            + b"\x00"
            + master_seed
            + attempt.to_bytes(4, "big")
        ).digest()
        graph = generate_holonomy_graph(graph_parameters, attempt_seed)
        rng = _DeterministicRng(
            hashlib.sha256(
                b"MORPH-KEM H2-E height/defect generator v1\x00" + attempt_seed
            ).digest()
        )

        heights = tuple(rng.randbelow(parameters.modulus) for _ in range(graph.vertices))
        increments = [
            (heights[right] - heights[left]) % parameters.modulus
            for left, right in graph.edges
        ]

        candidate_edges = list(graph.edges)
        _shuffle(
            candidate_edges,
            hashlib.sha256(
                b"MORPH-KEM H2-E seam chooser v1\x00" + attempt_seed
            ).digest(),
        )
        seams = tuple(sorted(candidate_edges[: parameters.seam_budget]))
        edge_index = {edge: index for index, edge in enumerate(graph.edges)}
        for seam in seams:
            index = edge_index[seam]
            offset = 1 + rng.randbelow(parameters.modulus - 1)
            increments[index] = (increments[index] + offset) % parameters.modulus

        public = EscherPublicInstance(parameters, graph, tuple(increments))
        reference = EscherReference(heights, seams)

        if not validate_escher_witness(public, reference.planted_seams, reference.heights).accepted:
            raise EscherExperimentError("internal H2-E planted witness validation failed")

        zero = propagate_escher_potentials(public, ())
        if zero.balanced:
            continue

        return public, reference

    raise EscherExperimentError("could not generate a globally frustrated H2-E instance")


def validate_escher_witness(
    public: EscherPublicInstance,
    seams: tuple[Edge, ...],
    heights: tuple[int, ...],
) -> EscherValidation:
    modulus = public.parameters.modulus
    graph_edges = set(public.graph.edges)

    if len(seams) > public.parameters.seam_budget:
        return EscherValidation(False, None, "seam budget exceeded")
    if tuple(sorted(set(seams))) != seams:
        return EscherValidation(False, None, "seams must be unique and canonically sorted")
    if any(edge not in graph_edges for edge in seams):
        return EscherValidation(False, None, "seam references a non-public edge")
    if len(heights) != public.graph.vertices:
        return EscherValidation(False, None, "height count does not match vertices")
    if any(value < 0 or value >= modulus for value in heights):
        return EscherValidation(False, None, "height is outside the public modulus")

    seam_set = set(seams)
    for edge, label in zip(public.graph.edges, public.increments):
        if edge in seam_set:
            continue
        left, right = edge
        if (heights[right] - heights[left]) % modulus != label:
            return EscherValidation(False, edge, "non-seam edge violates the local height relation")

    return EscherValidation(True, None, "accepted")


def _tree_potentials(public: EscherPublicInstance) -> tuple[int, ...]:
    labels = _edge_label_map(public)
    tree_edges = set(public.graph.spanning_tree_edges())
    adjacency: list[list[int]] = [[] for _ in range(public.graph.vertices)]
    for left, right in tree_edges:
        adjacency[left].append(right)
        adjacency[right].append(left)
    for values in adjacency:
        values.sort()

    heights: list[int | None] = [None] * public.graph.vertices
    heights[0] = 0
    queue = [0]
    modulus = public.parameters.modulus

    while queue:
        source = queue.pop(0)
        assert heights[source] is not None
        for target in adjacency[source]:
            if heights[target] is not None:
                continue
            edge = (source, target) if source < target else (target, source)
            delta = _oriented_increment(edge, source, target, labels[edge], modulus)
            heights[target] = (heights[source] + delta) % modulus
            queue.append(target)

    return tuple(int(value) for value in heights)


def fundamental_cycle_syndrome(public: EscherPublicInstance) -> FundamentalSyndrome:
    heights = _tree_potentials(public)
    labels = _edge_label_map(public)
    modulus = public.parameters.modulus
    chords = public.graph.chord_edges()
    values = tuple(
        (heights[right] - heights[left] - labels[edge]) % modulus
        for edge in chords
        for left, right in (edge,)
    )
    return FundamentalSyndrome(chords, values)


def _path_edges_in_parent_forest(
    left: int,
    right: int,
    parent: list[int | None],
    parent_edge: list[Edge | None],
) -> tuple[Edge, ...]:
    left_ancestors: dict[int, int] = {}
    left_edges: list[Edge] = []
    current = left
    left_ancestors[current] = 0
    while parent[current] is not None:
        edge = parent_edge[current]
        assert edge is not None
        left_edges.append(edge)
        current = parent[current]  # type: ignore[assignment]
        left_ancestors[current] = len(left_edges)

    right_edges: list[Edge] = []
    current = right
    while current not in left_ancestors:
        edge = parent_edge[current]
        if edge is None or parent[current] is None:
            raise EscherExperimentError("conflict endpoints are not in the same parent tree")
        right_edges.append(edge)
        current = parent[current]  # type: ignore[assignment]

    prefix = left_edges[: left_ancestors[current]]
    cycle_path = prefix + list(reversed(right_edges))
    return tuple(cycle_path)


def propagate_escher_potentials(
    public: EscherPublicInstance,
    seams: tuple[Edge, ...],
) -> PotentialPropagation:
    seam_set = set(seams)
    if any(edge not in set(public.graph.edges) for edge in seam_set):
        raise EscherExperimentError("propagation seam references a non-public edge")

    labels = _edge_label_map(public)
    adjacency: list[list[int]] = [[] for _ in range(public.graph.vertices)]
    for edge in public.graph.edges:
        if edge in seam_set:
            continue
        left, right = edge
        adjacency[left].append(right)
        adjacency[right].append(left)
    for values in adjacency:
        values.sort()

    modulus = public.parameters.modulus
    heights: list[int | None] = [None] * public.graph.vertices
    parent: list[int | None] = [None] * public.graph.vertices
    parent_edge: list[Edge | None] = [None] * public.graph.vertices
    edge_checks = 0

    for root in range(public.graph.vertices):
        if heights[root] is not None:
            continue
        heights[root] = 0
        queue = [root]

        while queue:
            source = queue.pop(0)
            assert heights[source] is not None
            for target in adjacency[source]:
                edge = (source, target) if source < target else (target, source)
                delta = _oriented_increment(edge, source, target, labels[edge], modulus)
                expected = (heights[source] + delta) % modulus
                edge_checks += 1

                if heights[target] is None:
                    heights[target] = expected
                    parent[target] = source
                    parent_edge[target] = edge
                    queue.append(target)
                    continue

                if heights[target] != expected:
                    path = _path_edges_in_parent_forest(
                        source,
                        target,
                        parent,
                        parent_edge,
                    )
                    conflict = tuple(sorted(set(path + (edge,))))
                    return PotentialPropagation(
                        False,
                        tuple(0 if value is None else int(value) for value in heights),
                        conflict,
                        edge_checks,
                    )

    return PotentialPropagation(
        True,
        tuple(int(value) for value in heights),
        (),
        edge_checks,
    )


def solve_escher_repair(
    public: EscherPublicInstance,
    max_nodes: int = 1_000_000,
) -> EscherRepairResult:
    if max_nodes <= 0 or max_nodes > 20_000_000:
        raise EscherExperimentError("max_nodes must be in [1, 20000000]")

    total_nodes = 0
    total_backtracks = 0
    total_edge_checks = 0
    global_max_branch = 0
    cap_exhausted = False

    for limit in range(public.parameters.seam_budget + 1):
        visited: set[tuple[Edge, ...]] = set()
        solution: tuple[tuple[Edge, ...], tuple[int, ...]] | None = None

        def search(seams: tuple[Edge, ...]) -> None:
            nonlocal total_nodes, total_backtracks, total_edge_checks
            nonlocal global_max_branch, cap_exhausted, solution

            if solution is not None or cap_exhausted:
                return
            if seams in visited:
                return
            visited.add(seams)

            total_nodes += 1
            if total_nodes > max_nodes:
                cap_exhausted = True
                return

            propagation = propagate_escher_potentials(public, seams)
            total_edge_checks += propagation.edge_checks

            if propagation.balanced:
                validation = validate_escher_witness(public, seams, propagation.heights)
                if validation.accepted:
                    solution = (seams, propagation.heights)
                    return
                total_backtracks += 1
                return

            if len(seams) >= limit:
                total_backtracks += 1
                return

            cycle = tuple(
                edge
                for edge in propagation.conflict_cycle
                if edge not in set(seams)
            )
            global_max_branch = max(global_max_branch, len(cycle))
            if not cycle:
                total_backtracks += 1
                return

            before = total_nodes
            for edge in cycle:
                child = tuple(sorted(seams + (edge,)))
                search(child)
                if solution is not None or cap_exhausted:
                    return
            if total_nodes > before:
                total_backtracks += 1

        search(())

        if solution is not None:
            seams, heights = solution
            return EscherRepairResult(
                True,
                seams,
                heights,
                len(seams),
                total_nodes,
                total_backtracks,
                global_max_branch,
                total_edge_checks,
                False,
            )
        if cap_exhausted:
            return EscherRepairResult(
                False,
                (),
                (),
                None,
                total_nodes,
                total_backtracks,
                global_max_branch,
                total_edge_checks,
                False,
            )

    return EscherRepairResult(
        False,
        (),
        (),
        None,
        total_nodes,
        total_backtracks,
        global_max_branch,
        total_edge_checks,
        True,
    )


def escher_scaling_sweep(
    master_seed: bytes,
    max_nodes: int = 1_000_000,
) -> tuple[EscherSweepRow, ...]:
    rows: list[EscherSweepRow] = []
    for parameters in ESCHER_PARAMETER_SETS.values():
        public, _ = generate_escher_instance(parameters, master_seed)
        syndrome = fundamental_cycle_syndrome(public)
        repair = solve_escher_repair(public, max_nodes=max_nodes)
        rows.append(
            EscherSweepRow(
                parameters.name,
                public.graph.vertices,
                len(public.graph.edges),
                public.graph.cycle_rank,
                parameters.seam_budget,
                syndrome.nonzero,
                repair.found,
                repair.minimum_seams,
                repair.nodes,
                repair.backtracks,
            )
        )
    return tuple(rows)
