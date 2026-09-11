from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from functools import lru_cache
import hashlib

from .complex import SimplicialComplex
from .gluing import GluingExperimentError
from .gluing_mixed_sphere import (
    MixedSphereParameters,
    _grow_icosahedron,
    _mix_facets,
    _public_relabel,
)
from .nat_coboundary import (
    _clean_edge_mask,
    _edge_triangle_owners,
    _edges,
    _hidden_vertex_mask,
    _normalize_vertex_mask,
    _recover_vertex_mask_from_clean,
    _violated_triangles,
)


class NAT1Error(ValueError):
    """Raised when a NAT1 toy experiment is malformed."""


@dataclass(frozen=True, slots=True)
class NAT1Parameters:
    name: str
    triangle_count: int
    successful_flips: int
    noise_weights: tuple[int, ...]

    def validate(self) -> None:
        if self.triangle_count < 24 or self.triangle_count > 192:
            raise NAT1Error("NAT1 triangle count outside toy bounds")
        if self.triangle_count % 2:
            raise NAT1Error("NAT1 triangle count must be even")
        if (self.triangle_count - 20) % 2:
            raise NAT1Error("NAT1 triangle count is not reachable from icosahedron")
        if self.successful_flips < self.triangle_count:
            raise NAT1Error("NAT1 flip target is too small")
        if not self.noise_weights or any(weight < 1 or weight > 8 for weight in self.noise_weights):
            raise NAT1Error("NAT1 noise weights outside toy bounds")
        if tuple(sorted(set(self.noise_weights))) != self.noise_weights:
            raise NAT1Error("NAT1 noise weights must be sorted and distinct")


NAT1_PARAMETER_SETS = {
    "nat1-36": NAT1Parameters("nat1-36", 36, 360, (1, 2, 3, 4)),
    "nat1-54": NAT1Parameters("nat1-54", 54, 540, (1, 2, 3, 4, 5)),
    "nat1-72": NAT1Parameters("nat1-72", 72, 720, (1, 2, 3, 4, 5, 6)),
}


@dataclass(frozen=True, slots=True)
class NAT1Public:
    name: str
    target: SimplicialComplex
    observed_edge_mask: int
    public_noise_weight: int


@dataclass(frozen=True, slots=True)
class NAT1Reference:
    hidden_vertex_mask: int
    planted_noise_mask: int
    rejected_flip_proposals: int


@dataclass(frozen=True, slots=True)
class NAT1Recovery:
    vertices: int
    edges: int
    triangles: int
    noise_weight: int
    syndrome_weight: int
    syndrome_triangles: tuple[int, ...]
    pair_metric_bfs_runs: int
    pair_metric_queue_pops: int
    pair_metric_edge_scans: int
    matching_dp_states: int
    matching_pair_tests: int
    matching_distance: int
    recovered_noise_weight: int
    recovered_noise_mask: int
    recovered_clean_edge_mask: int
    recovered_vertex_mask_normalized: int
    accepted: bool
    matches_planted_noise_after_public_success: bool | None
    matches_hidden_vertex_after_public_success: bool | None


def _digest(domain: bytes, seed: bytes, name: str, counter: int = 0) -> bytes:
    return hashlib.sha256(
        domain + b"\x00" + seed + name.encode("ascii") + counter.to_bytes(8, "big")
    ).digest()


def _carrier(params: NAT1Parameters, seed: bytes) -> tuple[SimplicialComplex, int]:
    mixed_params = MixedSphereParameters(
        params.name + "-carrier", params.triangle_count, params.successful_flips
    )
    base = _grow_icosahedron(mixed_params, _digest(b"MORPH-KEM NAT1 growth v1", seed, params.name))
    facets, rejected = _mix_facets(
        mixed_params,
        base,
        _digest(b"MORPH-KEM NAT1 flips v1", seed, params.name),
    )
    target = _public_relabel(
        facets, _digest(b"MORPH-KEM NAT1 relabel v1", seed, params.name)
    )
    return target, rejected


def _noise_mask(edge_count: int, weight: int, seed: bytes, name: str) -> int:
    if weight > edge_count:
        raise NAT1Error("NAT1 noise weight exceeds edge count")
    order = sorted(
        range(edge_count),
        key=lambda index: (_digest(b"MORPH-KEM NAT1 noise order v1", seed, name, index), index),
    )
    return sum(1 << index for index in order[:weight])


def generate_nat1_instance(
    params: NAT1Parameters,
    master_seed: bytes,
    noise_weight: int,
) -> tuple[NAT1Public, NAT1Reference]:
    params.validate()
    if len(master_seed) < 16:
        raise NAT1Error("NAT1 master seed must contain at least 128 bits")
    if noise_weight not in params.noise_weights:
        raise NAT1Error("NAT1 noise weight is not in the public parameter sweep")
    target, rejected = _carrier(params, master_seed)
    hidden = _hidden_vertex_mask(target, master_seed, params.name + f"-w{noise_weight}")
    clean = _clean_edge_mask(target, hidden)
    noise = _noise_mask(len(_edges(target)), noise_weight, master_seed, params.name + f"-w{noise_weight}")
    observed = clean ^ noise
    return (
        NAT1Public(params.name, target, observed, noise_weight),
        NAT1Reference(hidden, noise, rejected),
    )


def _dual_adjacency(target: SimplicialComplex) -> tuple[tuple[tuple[int, int], ...], ...]:
    owners = _edge_triangle_owners(target)
    triangle_count = len(tuple(simplex for simplex in target.simplices if len(simplex) == 3))
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(triangle_count)]
    for edge_index, pair in enumerate(owners):
        if len(pair) != 2:
            raise NAT1Error("NAT1 carrier is not closed")
        left, right = pair
        adjacency[left].append((right, edge_index))
        adjacency[right].append((left, edge_index))
    for row in adjacency:
        row.sort()
    return tuple(tuple(row) for row in adjacency)


def _shortest_paths_from(
    source: int,
    adjacency: tuple[tuple[tuple[int, int], ...], ...],
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...], int, int]:
    parent = [-1] * len(adjacency)
    parent_edge = [-1] * len(adjacency)
    distance = [-1] * len(adjacency)
    parent[source] = source
    distance[source] = 0
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
    if any(value < 0 for value in distance):
        raise NAT1Error("NAT1 dual graph is disconnected")
    return tuple(distance), tuple(parent), tuple(parent_edge), pops, scans


def _path_edges(
    source: int,
    target: int,
    parent: tuple[int, ...],
    parent_edge: tuple[int, ...],
) -> tuple[int, ...]:
    path: list[int] = []
    current = target
    while current != source:
        edge = parent_edge[current]
        if edge < 0:
            raise NAT1Error("NAT1 shortest-path reconstruction failed")
        path.append(edge)
        current = parent[current]
    path.reverse()
    return tuple(path)


def _minimum_t_join(
    target: SimplicialComplex,
    defects: tuple[int, ...],
) -> tuple[int, int, int, int, int, int]:
    if len(defects) % 2:
        raise NAT1Error("NAT1 syndrome has odd defect count")
    if not defects:
        return 0, 0, 0, 1, 0, 0
    if len(defects) > 16:
        raise NAT1Error("NAT1 exact T-join defect cap exceeded")

    adjacency = _dual_adjacency(target)
    distances: list[tuple[int, ...]] = []
    parents: list[tuple[int, ...]] = []
    parent_edges: list[tuple[int, ...]] = []
    total_pops = 0
    total_scans = 0
    for defect in defects:
        distance, parent, edge_parent, pops, scans = _shortest_paths_from(defect, adjacency)
        distances.append(distance)
        parents.append(parent)
        parent_edges.append(edge_parent)
        total_pops += pops
        total_scans += scans

    pair_distance: dict[tuple[int, int], int] = {}
    pair_path: dict[tuple[int, int], tuple[int, ...]] = {}
    for left in range(len(defects)):
        for right in range(left + 1, len(defects)):
            pair_distance[(left, right)] = distances[left][defects[right]]
            pair_path[(left, right)] = _path_edges(
                defects[left], defects[right], parents[left], parent_edges[left]
            )

    state_counter = 0
    pair_tests = 0

    @lru_cache(maxsize=None)
    def solve(mask: int) -> tuple[int, tuple[tuple[int, int], ...]]:
        nonlocal state_counter, pair_tests
        state_counter += 1
        if mask == 0:
            return 0, ()
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        remaining = mask ^ first_bit
        best_cost: int | None = None
        best_pairs: tuple[tuple[int, int], ...] | None = None
        probe = remaining
        while probe:
            bit = probe & -probe
            second = bit.bit_length() - 1
            pair_tests += 1
            key = (first, second) if first < second else (second, first)
            tail_cost, tail_pairs = solve(remaining ^ bit)
            candidate_cost = pair_distance[key] + tail_cost
            candidate_pairs = (key,) + tail_pairs
            if best_cost is None or (candidate_cost, candidate_pairs) < (best_cost, best_pairs):
                best_cost = candidate_cost
                best_pairs = candidate_pairs
            probe ^= bit
        if best_cost is None or best_pairs is None:
            raise NAT1Error("NAT1 matching DP failed")
        return best_cost, best_pairs

    full_mask = (1 << len(defects)) - 1
    distance, pairs = solve(full_mask)
    correction = 0
    for pair in pairs:
        for edge_index in pair_path[pair]:
            correction ^= 1 << edge_index
    return correction, distance, len(defects), state_counter, pair_tests, total_pops + total_scans


def recover_nat1(
    public: NAT1Public,
    *,
    reference: NAT1Reference | None = None,
) -> NAT1Recovery:
    defects = _violated_triangles(public.target, public.observed_edge_mask)
    correction, distance, _, dp_states, pair_tests, traversal_work = _minimum_t_join(
        public.target, defects
    )
    clean = public.observed_edge_mask ^ correction
    vertex_mask = _recover_vertex_mask_from_clean(public.target, clean)
    accepted = (
        _clean_edge_mask(public.target, vertex_mask) == clean
        and _violated_triangles(public.target, correction) == defects
    )
    match_noise = None
    match_hidden = None
    if reference is not None:
        match_noise = correction == reference.planted_noise_mask
        match_hidden = (
            vertex_mask
            == _normalize_vertex_mask(public.target, reference.hidden_vertex_mask)
        )

    # traversal_work is pops + scans from all defect-root BFS runs.  The dual is cubic,
    # so retaining the combined count keeps the toy metric stable and explicit.
    adjacency = _dual_adjacency(public.target)
    bfs_runs = len(defects)
    # One BFS visits every dual vertex and scans every directed dual adjacency arc.
    # These counts are exact for the connected closed-sphere carriers used here.
    queue_pops = bfs_runs * len(adjacency)
    edge_scans = traversal_work - queue_pops

    return NAT1Recovery(
        vertices=len(public.target.vertices),
        edges=len(_edges(public.target)),
        triangles=len(adjacency),
        noise_weight=public.public_noise_weight,
        syndrome_weight=len(defects),
        syndrome_triangles=defects,
        pair_metric_bfs_runs=bfs_runs,
        pair_metric_queue_pops=queue_pops,
        pair_metric_edge_scans=edge_scans,
        matching_dp_states=dp_states,
        matching_pair_tests=pair_tests,
        matching_distance=distance,
        recovered_noise_weight=correction.bit_count(),
        recovered_noise_mask=correction,
        recovered_clean_edge_mask=clean,
        recovered_vertex_mask_normalized=vertex_mask,
        accepted=accepted,
        matches_planted_noise_after_public_success=match_noise,
        matches_hidden_vertex_after_public_success=match_hidden,
    )
