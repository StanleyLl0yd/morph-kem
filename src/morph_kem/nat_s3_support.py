from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from .nat_coboundary import _edges, _violated_triangles
from .nat_s3 import (
    NAT2Public,
    NAT2Reference,
    Permutation,
    _IDENTITY,
    _observed_sign_mask,
    compose,
    inverse,
    validate_nat2_state,
)
from .nat_tjoin import _minimum_t_join


@dataclass(frozen=True, slots=True)
class NAT2SupportRecovery:
    sign_correction_weight: int
    reached_vertices: int
    clean_subgraph_connected: bool
    propagation_consistent: bool
    exact_state_accepted: bool
    verifier_noise_edges: tuple[int, ...]
    support_matches_planted_after_public_success: bool | None
    state_matches_hidden_after_public_success: bool | None


def recover_from_sign_support(
    public: NAT2Public,
    *,
    reference: NAT2Reference | None = None,
) -> NAT2SupportRecovery:
    sign_mask = _observed_sign_mask(public)
    defects = _violated_triangles(public.target, sign_mask)
    correction, _, _, _, _, _ = _minimum_t_join(public.target, defects)
    excluded = {
        edge_index
        for edge_index in range(len(_edges(public.target)))
        if (correction >> edge_index) & 1
    }

    edges = _edges(public.target)
    adjacency: dict[int, list[tuple[int, int]]] = {
        vertex: [] for vertex in public.target.vertices
    }
    for edge_index, (left, right) in enumerate(edges):
        if edge_index in excluded:
            continue
        adjacency[left].append((right, edge_index))
        adjacency[right].append((left, edge_index))
    for row in adjacency.values():
        row.sort()

    root = min(public.target.vertices)
    labels: dict[int, Permutation] = {root: _IDENTITY}
    queue = deque([root])
    consistent = True
    while queue and consistent:
        current = queue.popleft()
        for neighbor, edge_index in adjacency[current]:
            left, right = edges[edge_index]
            observed = public.observed_edge_labels[edge_index]
            if current == left and neighbor == right:
                expected = compose(labels[current], observed)
            elif current == right and neighbor == left:
                expected = compose(labels[current], inverse(observed))
            else:
                raise ValueError("NAT2 support propagation edge orientation mismatch")
            if neighbor not in labels:
                labels[neighbor] = expected
                queue.append(neighbor)
            elif labels[neighbor] != expected:
                consistent = False
                break

    connected = len(labels) == len(public.target.vertices)
    accepted = False
    verifier_noise: tuple[int, ...] = ()
    concrete: tuple[Permutation, ...] | None = None
    if connected and consistent:
        concrete = tuple(labels[index] for index in range(len(labels)))
        accepted, verifier_noise = validate_nat2_state(public, concrete)

    support_match = None
    hidden_match = None
    if reference is not None and accepted and concrete is not None:
        support_match = tuple(sorted(excluded)) == reference.planted_noise_edges
        hidden_match = concrete == reference.hidden_vertex_labels_normalized

    return NAT2SupportRecovery(
        sign_correction_weight=correction.bit_count(),
        reached_vertices=len(labels),
        clean_subgraph_connected=connected,
        propagation_consistent=consistent,
        exact_state_accepted=accepted,
        verifier_noise_edges=verifier_noise,
        support_matches_planted_after_public_success=support_match,
        state_matches_hidden_after_public_success=hidden_match,
    )
