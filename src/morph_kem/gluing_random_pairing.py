from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
from itertools import combinations

from .gluing import GluingExperimentError, _DeterministicRng, _UnionFind


Triangle = tuple[int, int, int]
DualEdge = tuple[int, int]


@dataclass(frozen=True, slots=True)
class RandomPairingParameters:
    name: str
    triangle_count: int

    def validate(self) -> None:
        if self.triangle_count < 12 or self.triangle_count > 192:
            raise GluingExperimentError("G13 triangle count outside toy bounds")
        if self.triangle_count % 2:
            raise GluingExperimentError("G13 triangle count must be even")
        if self.triangle_count % 3:
            raise GluingExperimentError("G13 triangle count must be divisible by three")


G13_PARAMETER_SETS = {
    "g13-36": RandomPairingParameters("g13-36", 36),
    "g13-54": RandomPairingParameters("g13-54", 54),
    "g13-72": RandomPairingParameters("g13-72", 72),
}


@dataclass(frozen=True, slots=True)
class PairingSurface:
    triangles: tuple[Triangle, ...]
    dual_edges: tuple[DualEdge, ...]
    vertices: int
    edges: int
    euler_characteristic: int
    genus: int


@dataclass(frozen=True, slots=True)
class PairingAttempt:
    reason: str
    surface: PairingSurface | None


@dataclass(frozen=True, slots=True)
class PairingAudit:
    parameter_name: str
    triangle_count: int
    attempts: int
    reason_counts: tuple[tuple[str, int], ...]
    successes: int
    success_rate: float
    zero_success_rule_of_three_upper: float
    genus_histogram: tuple[tuple[int, int], ...]


_REASONS = (
    "dual_loop",
    "dual_parallel",
    "dual_disconnected",
    "degenerate_triangle",
    "duplicate_triangle",
    "bad_edge_incidence",
    "bad_vertex_link",
    "bad_genus",
    "success",
)


def _attempt_seed(params: RandomPairingParameters, master_seed: bytes, index: int) -> bytes:
    return hashlib.sha256(
        b"MORPH-KEM G13 random-pairing attempt v1\x00"
        + master_seed
        + params.name.encode("ascii")
        + index.to_bytes(8, "big")
    ).digest()


def _connected(vertex_count: int, edges: set[DualEdge]) -> bool:
    adjacency = [set() for _ in range(vertex_count)]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    seen = {0}
    stack = [0]
    while stack:
        current = stack.pop()
        for neighbor in adjacency[current]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return len(seen) == vertex_count


def _vertex_links_are_cycles(triangles: tuple[Triangle, ...]) -> bool:
    incident: dict[int, list[Triangle]] = defaultdict(list)
    for triangle in triangles:
        for vertex in triangle:
            incident[vertex].append(triangle)

    for vertex, star in incident.items():
        link: dict[int, set[int]] = defaultdict(set)
        for triangle in star:
            others = [value for value in triangle if value != vertex]
            if len(others) != 2:
                return False
            left, right = others
            link[left].add(right)
            link[right].add(left)
        if not link or any(len(neighbors) != 2 for neighbors in link.values()):
            return False
        root = min(link)
        seen = {root}
        stack = [root]
        while stack:
            current = stack.pop()
            for neighbor in link[current]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        if len(seen) != len(link):
            return False
    return True


def attempt_random_pairing_surface(
    params: RandomPairingParameters,
    master_seed: bytes,
    attempt_index: int,
) -> PairingAttempt:
    params.validate()
    if len(master_seed) < 16:
        raise GluingExperimentError("G13 master seed must contain at least 128 bits")
    if attempt_index < 0 or attempt_index >= (1 << 63):
        raise GluingExperimentError("G13 attempt index outside toy bounds")

    triangle_count = params.triangle_count
    stubs = list(range(3 * triangle_count))
    rng = _DeterministicRng(
        b"MORPH-KEM G13 random-pairing shuffle v1",
        _attempt_seed(params, master_seed, attempt_index),
    )
    rng.shuffle(stubs)

    paired_stubs: list[tuple[int, int]] = []
    dual_edges: set[DualEdge] = set()
    for offset in range(0, len(stubs), 2):
        first = stubs[offset]
        second = stubs[offset + 1]
        left = first // 3
        right = second // 3
        if left == right:
            return PairingAttempt("dual_loop", None)
        dual_edge = tuple(sorted((left, right)))
        if dual_edge in dual_edges:
            return PairingAttempt("dual_parallel", None)
        dual_edges.add(dual_edge)
        paired_stubs.append((first, second))

    if not _connected(triangle_count, dual_edges):
        return PairingAttempt("dual_disconnected", None)

    quotient = _UnionFind(3 * triangle_count)
    for first, second in paired_stubs:
        left_triangle, left_side = divmod(first, 3)
        right_triangle, right_side = divmod(second, 3)
        # Side s follows oriented boundary corner s -> s+1. Glue paired
        # boundaries in reverse orientation so all abstract triangles share one
        # consistent orientation if the quotient is a genuine surface.
        quotient.union(
            3 * left_triangle + left_side,
            3 * right_triangle + ((right_side + 1) % 3),
        )
        quotient.union(
            3 * left_triangle + ((left_side + 1) % 3),
            3 * right_triangle + right_side,
        )

    roots = sorted({quotient.find(corner) for corner in range(3 * triangle_count)})
    root_index = {root: index for index, root in enumerate(roots)}
    triangles: list[Triangle] = []
    for triangle_index in range(triangle_count):
        triangle = tuple(
            sorted(
                root_index[quotient.find(3 * triangle_index + corner)]
                for corner in range(3)
            )
        )
        if len(set(triangle)) != 3:
            return PairingAttempt("degenerate_triangle", None)
        triangles.append(triangle)

    triangle_tuple = tuple(sorted(triangles))
    if len(set(triangle_tuple)) != triangle_count:
        return PairingAttempt("duplicate_triangle", None)

    edge_owners: dict[tuple[int, int], list[int]] = defaultdict(list)
    for triangle_index, triangle in enumerate(triangle_tuple):
        for edge in combinations(triangle, 2):
            edge_owners[tuple(sorted(edge))].append(triangle_index)
    if (
        len(edge_owners) != 3 * triangle_count // 2
        or any(len(owners) != 2 for owners in edge_owners.values())
    ):
        return PairingAttempt("bad_edge_incidence", None)

    if not _vertex_links_are_cycles(triangle_tuple):
        return PairingAttempt("bad_vertex_link", None)

    vertex_count = len(roots)
    edge_count = len(edge_owners)
    euler = vertex_count - edge_count + triangle_count
    genus_twice = 2 - euler
    if genus_twice < 0 or genus_twice % 2:
        return PairingAttempt("bad_genus", None)

    return PairingAttempt(
        "success",
        PairingSurface(
            triangles=triangle_tuple,
            dual_edges=tuple(sorted(dual_edges)),
            vertices=vertex_count,
            edges=edge_count,
            euler_characteristic=euler,
            genus=genus_twice // 2,
        ),
    )


def audit_random_pairing_generator(
    params: RandomPairingParameters,
    master_seed: bytes,
    *,
    attempts: int = 1024,
) -> PairingAudit:
    params.validate()
    if attempts < 1 or attempts > 100_000:
        raise GluingExperimentError("G13 audit attempts outside toy bounds")

    reasons = Counter({reason: 0 for reason in _REASONS})
    genera: Counter[int] = Counter()
    for attempt_index in range(attempts):
        result = attempt_random_pairing_surface(params, master_seed, attempt_index)
        reasons[result.reason] += 1
        if result.surface is not None:
            genera[result.surface.genus] += 1

    successes = reasons["success"]
    return PairingAudit(
        parameter_name=params.name,
        triangle_count=params.triangle_count,
        attempts=attempts,
        reason_counts=tuple((reason, reasons[reason]) for reason in _REASONS),
        successes=successes,
        success_rate=successes / attempts,
        zero_success_rule_of_three_upper=(3.0 / attempts if successes == 0 else 0.0),
        genus_histogram=tuple(sorted(genera.items())),
    )
