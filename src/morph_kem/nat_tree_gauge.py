from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar


T = TypeVar("T")


class NAT7Error(ValueError):
    """Raised when a public tree-gauge normalization input is malformed."""


@dataclass(frozen=True, slots=True)
class GroupOps(Generic[T]):
    identity: T
    multiply: Callable[[T, T], T]
    inverse: Callable[[T], T]


@dataclass(frozen=True, slots=True)
class TreeGaugeNormalization(Generic[T]):
    vertex_count: int
    edge_count: int
    tree_edge_indices: tuple[int, ...]
    non_tree_edge_indices: tuple[int, ...]
    integration_labels: tuple[T, ...]
    residual_labels: tuple[T, ...]
    tree_assignments: int
    tree_identity_residuals: int
    nonidentity_residuals: int
    distinct_nonidentity_residuals: int
    reconstruction_verified: bool


def _validate_edges(vertex_count: int, edges: tuple[tuple[int, int], ...]) -> None:
    if vertex_count < 1:
        raise NAT7Error("NAT7 vertex count must be positive")
    if not edges and vertex_count != 1:
        raise NAT7Error("NAT7 nontrivial carrier has no edges")
    seen: set[tuple[int, int]] = set()
    for left, right in edges:
        if left < 0 or right >= vertex_count or left >= right:
            raise NAT7Error("NAT7 edges must be canonical undirected pairs")
        if (left, right) in seen:
            raise NAT7Error("NAT7 carrier contains duplicate edges")
        seen.add((left, right))


def _tree_adjacency(
    vertex_count: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[tuple[int, int, bool], ...], ...]:
    _validate_edges(vertex_count, edges)
    rows: list[list[tuple[int, int, bool]]] = [[] for _ in range(vertex_count)]
    for edge_index, (left, right) in enumerate(edges):
        rows[left].append((right, edge_index, True))
        rows[right].append((left, edge_index, False))
    for row in rows:
        row.sort()
    return tuple(tuple(row) for row in rows)


def integrate_tree(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
    edge_labels: tuple[T, ...],
    ops: GroupOps[T],
) -> tuple[tuple[T, ...], tuple[int, ...], int]:
    """Integrate a public connection on a deterministic BFS spanning tree.

    Edge labels are oriented according to the canonical `(left,right)` edge order.
    The returned root label is the group identity.  No flatness assumption is used.
    """

    if len(edge_labels) != len(edges):
        raise NAT7Error("NAT7 edge-label count mismatch")
    adjacency = _tree_adjacency(vertex_count, edges)
    labels: list[T | None] = [None] * vertex_count
    labels[0] = ops.identity
    queue = deque([0])
    tree_edges: list[int] = []
    assignments = 0
    while queue:
        current = queue.popleft()
        current_label = labels[current]
        if current_label is None:
            raise NAT7Error("NAT7 tree integration lost an assigned vertex")
        for neighbor, edge_index, forward in adjacency[current]:
            if labels[neighbor] is not None:
                continue
            observed = edge_labels[edge_index]
            labels[neighbor] = (
                ops.multiply(current_label, observed)
                if forward
                else ops.multiply(current_label, ops.inverse(observed))
            )
            tree_edges.append(edge_index)
            assignments += 1
            queue.append(neighbor)
    if any(value is None for value in labels):
        raise NAT7Error("NAT7 public carrier is disconnected")
    concrete = tuple(value for value in labels if value is not None)
    if len(concrete) != vertex_count:
        raise NAT7Error("NAT7 tree integration produced incomplete labels")
    return concrete, tuple(sorted(tree_edges)), assignments


def residual_connection(
    edges: tuple[tuple[int, int], ...],
    edge_labels: tuple[T, ...],
    integration_labels: tuple[T, ...],
    ops: GroupOps[T],
) -> tuple[T, ...]:
    if len(edge_labels) != len(edges):
        raise NAT7Error("NAT7 edge-label count mismatch")
    return tuple(
        ops.multiply(
            ops.multiply(integration_labels[left], edge_labels[index]),
            ops.inverse(integration_labels[right]),
        )
        for index, (left, right) in enumerate(edges)
    )


def reconstruct_connection(
    edges: tuple[tuple[int, int], ...],
    integration_labels: tuple[T, ...],
    residual_labels: tuple[T, ...],
    ops: GroupOps[T],
) -> tuple[T, ...]:
    if len(residual_labels) != len(edges):
        raise NAT7Error("NAT7 residual-label count mismatch")
    return tuple(
        ops.multiply(
            ops.multiply(ops.inverse(integration_labels[left]), residual_labels[index]),
            integration_labels[right],
        )
        for index, (left, right) in enumerate(edges)
    )


def normalize_connection(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
    edge_labels: tuple[T, ...],
    ops: GroupOps[T],
) -> TreeGaugeNormalization[T]:
    integration, tree_edges, assignments = integrate_tree(
        vertex_count, edges, edge_labels, ops
    )
    residuals = residual_connection(edges, edge_labels, integration, ops)
    tree_set = set(tree_edges)
    non_tree = tuple(index for index in range(len(edges)) if index not in tree_set)
    tree_identity = sum(residuals[index] == ops.identity for index in tree_edges)
    nonidentity_values = [value for value in residuals if value != ops.identity]
    reconstructed = reconstruct_connection(edges, integration, residuals, ops)
    return TreeGaugeNormalization(
        vertex_count=vertex_count,
        edge_count=len(edges),
        tree_edge_indices=tree_edges,
        non_tree_edge_indices=non_tree,
        integration_labels=integration,
        residual_labels=residuals,
        tree_assignments=assignments,
        tree_identity_residuals=tree_identity,
        nonidentity_residuals=len(nonidentity_values),
        distinct_nonidentity_residuals=len(set(nonidentity_values)),
        reconstruction_verified=reconstructed == edge_labels,
    )


def apply_normalized_vertex_gauge(
    edges: tuple[tuple[int, int], ...],
    edge_labels: tuple[T, ...],
    gauge: tuple[T, ...],
    ops: GroupOps[T],
) -> tuple[T, ...]:
    """Apply a normalized public vertex gauge to oriented edge labels.

    The root gauge must be identity so deterministic tree normalization is exactly
    invariant rather than merely globally conjugate.
    """

    if not gauge or gauge[0] != ops.identity:
        raise NAT7Error("NAT7 comparison gauge must be normalized at vertex zero")
    if len(edge_labels) != len(edges):
        raise NAT7Error("NAT7 edge-label count mismatch")
    return tuple(
        ops.multiply(
            ops.multiply(ops.inverse(gauge[left]), edge_labels[index]),
            gauge[right],
        )
        for index, (left, right) in enumerate(edges)
    )
