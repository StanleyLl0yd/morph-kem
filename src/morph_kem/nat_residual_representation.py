from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from .nat_tree_gauge import (
    GroupOps,
    NAT7Error,
    normalize_connection,
    reconstruct_connection,
)


T = TypeVar("T")


class NAT8Error(NAT7Error):
    """Raised when residual-representation extraction is malformed."""


@dataclass(frozen=True, slots=True)
class ResidualRepresentation(Generic[T]):
    vertex_count: int
    edge_count: int
    free_rank: int
    tree_edge_indices: tuple[int, ...]
    generator_edge_indices: tuple[int, ...]
    integration_labels: tuple[T, ...]
    generator_images: tuple[T, ...]
    residual_labels: tuple[T, ...]
    tree_identity_residuals: int
    generator_residuals_nonidentity: int
    residual_vector_reconstructed: bool
    connection_reconstructed: bool


def extract_residual_representation(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
    edge_labels: tuple[T, ...],
    ops: GroupOps[T],
) -> ResidualRepresentation[T]:
    """Extract the complete rooted fundamental-cycle representation publicly.

    A deterministic public spanning tree gives one free generator of the graph
    fundamental group for every non-tree edge.  The tree-normalized residual on
    that edge is exactly the holonomy of the corresponding rooted fundamental
    cycle.  Thus the images of a free basis are public once exact edge labels are
    public.

    No flatness assumption is used.  If the graph is the one-skeleton of a flat
    public 2-complex connection, public face relators merely impose equations on
    these already-public generator images.
    """

    normalization = normalize_connection(vertex_count, edges, edge_labels, ops)
    tree_set = set(normalization.tree_edge_indices)
    generator_edges = normalization.non_tree_edge_indices

    expected_rank = len(edges) - vertex_count + 1
    if len(generator_edges) != expected_rank:
        raise NAT8Error("NAT8 free-rank accounting mismatch")

    generator_images = tuple(
        normalization.residual_labels[index] for index in generator_edges
    )

    rebuilt_residuals = tuple(
        ops.identity if index in tree_set else normalization.residual_labels[index]
        for index in range(len(edges))
    )
    residual_ok = rebuilt_residuals == normalization.residual_labels

    rebuilt_connection = reconstruct_connection(
        edges,
        normalization.integration_labels,
        rebuilt_residuals,
        ops,
    )
    connection_ok = rebuilt_connection == edge_labels

    if not residual_ok or not connection_ok:
        raise NAT8Error("NAT8 public generator images failed exact reconstruction")

    return ResidualRepresentation(
        vertex_count=vertex_count,
        edge_count=len(edges),
        free_rank=expected_rank,
        tree_edge_indices=normalization.tree_edge_indices,
        generator_edge_indices=generator_edges,
        integration_labels=normalization.integration_labels,
        generator_images=generator_images,
        residual_labels=normalization.residual_labels,
        tree_identity_residuals=normalization.tree_identity_residuals,
        generator_residuals_nonidentity=sum(
            value != ops.identity for value in generator_images
        ),
        residual_vector_reconstructed=residual_ok,
        connection_reconstructed=connection_ok,
    )


def triangle_relator_holonomies(
    edges: tuple[tuple[int, int], ...],
    edge_labels: tuple[T, ...],
    triangles: tuple[tuple[int, int, int], ...],
    ops: GroupOps[T],
) -> tuple[T, ...]:
    """Evaluate canonical triangular face relators from exact public labels."""

    if len(edge_labels) != len(edges):
        raise NAT8Error("NAT8 edge-label count mismatch")
    edge_index = {edge: index for index, edge in enumerate(edges)}
    values: list[T] = []
    for triangle in triangles:
        a, b, c = tuple(sorted(triangle))
        try:
            ab = edge_labels[edge_index[(a, b)]]
            bc = edge_labels[edge_index[(b, c)]]
            ac = edge_labels[edge_index[(a, c)]]
        except KeyError as exc:
            raise NAT8Error("NAT8 triangle references a missing edge") from exc
        values.append(ops.multiply(ops.multiply(ab, bc), ops.inverse(ac)))
    return tuple(values)
