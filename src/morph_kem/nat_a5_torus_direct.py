from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from .nat_a5 import Permutation5, _IDENTITY, compose
from .nat_a5_torus_flat import (
    NAT6Error,
    NAT6Public,
    NAT6Reference,
    _propagate_candidate_gauge,
    _tree_normalized_residuals,
    validate_nat6_witness,
)
from .gluing_cohomology_cycle import _edges


@dataclass(frozen=True, slots=True)
class NAT6DirectRecovery:
    fundamental_cycles_scanned: int
    fundamental_path_edge_scans: int
    first_pairing_vector: tuple[int, int]
    second_pairing_vector: tuple[int, int]
    recovered_pair: tuple[Permutation5, Permutation5]
    propagation_assignments: int
    accepted: bool
    pair_matches_planted_after_public_success: bool | None
    gauge_matches_planted_after_public_success: bool | None


def _tree_path(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
    tree_edges: frozenset[int],
    left: int,
    right: int,
) -> tuple[int, ...]:
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for index in tree_edges:
        first, second = edges[index]
        adjacency[first].append((second, index))
        adjacency[second].append((first, index))
    for values in adjacency:
        values.sort()

    parent = {left: (-1, -1)}
    queue = deque([left])
    while queue and right not in parent:
        current = queue.popleft()
        for neighbor, edge_index in adjacency[current]:
            if neighbor in parent:
                continue
            parent[neighbor] = (current, edge_index)
            queue.append(neighbor)
    if right not in parent:
        raise NAT6Error("NAT6 direct tree path crossed components")

    path: list[int] = []
    current = right
    while current != left:
        previous, edge_index = parent[current]
        if previous < 0 or edge_index < 0:
            raise NAT6Error("NAT6 direct tree path reconstruction failed")
        path.append(edge_index)
        current = previous
    return tuple(path)


def _pairing_vector(
    public: NAT6Public,
    cycle_edges: tuple[int, ...],
) -> tuple[int, int]:
    alpha = 0
    beta = 0
    for index in cycle_edges:
        alpha ^= public.alpha[index]
        beta ^= public.beta[index]
    return alpha, beta


def _bit_power(value: Permutation5, bit: int) -> Permutation5:
    return value if bit else _IDENTITY


def _solve_pair(
    first_vector: tuple[int, int],
    first_holonomy: Permutation5,
    second_vector: tuple[int, int],
    second_holonomy: Permutation5,
) -> tuple[Permutation5, Permutation5]:
    a, b = first_vector
    c, d = second_vector
    determinant = (a & d) ^ (b & c)
    if determinant != 1:
        raise NAT6Error("NAT6 direct holonomy pairings are not independent")
    left = compose(
        _bit_power(first_holonomy, d),
        _bit_power(second_holonomy, b),
    )
    right = compose(
        _bit_power(first_holonomy, c),
        _bit_power(second_holonomy, a),
    )
    return left, right


def recover_nat6_direct(
    public: NAT6Public,
    *,
    reference: NAT6Reference | None = None,
) -> NAT6DirectRecovery:
    edges = _edges(public.target)
    residuals, tree_edge_tuple = _tree_normalized_residuals(public)
    tree_edges = frozenset(tree_edge_tuple)
    non_tree_edges = [index for index in range(len(edges)) if index not in tree_edges]

    chosen: list[tuple[tuple[int, int], Permutation5]] = []
    cycles_scanned = 0
    path_scans = 0
    for edge_index in non_tree_edges:
        left, right = edges[edge_index]
        path = _tree_path(
            len(public.target.vertices), edges, tree_edges, left, right
        )
        path_scans += len(path)
        cycle = tuple(path) + (edge_index,)
        pairing = _pairing_vector(public, cycle)
        cycles_scanned += 1
        if pairing == (0, 0):
            continue
        if not chosen:
            chosen.append((pairing, residuals[edge_index]))
            continue
        if pairing != chosen[0][0]:
            chosen.append((pairing, residuals[edge_index]))
            break

    if len(chosen) != 2:
        raise NAT6Error("NAT6 direct attack found no independent fundamental holonomies")

    pair = _solve_pair(chosen[0][0], chosen[0][1], chosen[1][0], chosen[1][1])
    labels, assignments = _propagate_candidate_gauge(public, pair)
    accepted = validate_nat6_witness(public, labels, pair)
    pair_match = None
    gauge_match = None
    if accepted and reference is not None:
        pair_match = pair == reference.holonomy_pair
        gauge_match = labels == reference.hidden_vertex_labels_normalized

    return NAT6DirectRecovery(
        fundamental_cycles_scanned=cycles_scanned,
        fundamental_path_edge_scans=path_scans,
        first_pairing_vector=chosen[0][0],
        second_pairing_vector=chosen[1][0],
        recovered_pair=pair,
        propagation_assignments=assignments,
        accepted=accepted,
        pair_matches_planted_after_public_success=pair_match,
        gauge_matches_planted_after_public_success=gauge_match,
    )
