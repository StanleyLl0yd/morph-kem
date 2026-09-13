from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass
import hashlib
from itertools import combinations

from .complex import SimplicialComplex
from .gluing import GluingExperimentError
from .gluing_cohomology_cycle import (
    CohomologyCycleParameters,
    _edges,
    _nullspace_basis,
    _rref,
    _triangles,
    generate_cohomology_cycle_instance,
)
from .nat_a5 import (
    NAT3Error,
    Permutation5,
    _A5,
    _IDENTITY,
    _normalized_hidden_labels,
    compose,
    inverse,
)


class NAT6Error(NAT3Error):
    """Raised when a NAT6 flat-torus toy instance is malformed."""


@dataclass(frozen=True, slots=True)
class NAT6Parameters:
    name: str
    rows: int
    cols: int
    successful_flips: int

    def validate(self) -> None:
        if (self.rows, self.cols) not in ((6, 6), (6, 9), (8, 9)):
            raise NAT6Error("NAT6 torus dimensions outside declared toy sets")
        triangle_count = 2 * self.rows * self.cols
        if self.successful_flips < 1 or self.successful_flips > triangle_count:
            raise NAT6Error("NAT6 successful-flip target outside toy bounds")


NAT6_PARAMETER_SETS = {
    "nat6-6x6": NAT6Parameters("nat6-6x6", 6, 6, 36),
    "nat6-6x9": NAT6Parameters("nat6-6x9", 6, 9, 54),
    "nat6-8x9": NAT6Parameters("nat6-8x9", 8, 9, 72),
}


@dataclass(frozen=True, slots=True)
class NAT6Public:
    name: str
    target: SimplicialComplex
    observed_edge_labels: tuple[Permutation5, ...]
    alpha: tuple[int, ...]
    beta: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class NAT6Reference:
    hidden_vertex_labels_normalized: tuple[Permutation5, ...]
    holonomy_pair: tuple[Permutation5, Permutation5]


@dataclass(frozen=True, slots=True)
class NAT6Recovery:
    vertices: int
    edges: int
    triangles: int
    euler_characteristic: int
    min_triangles_per_edge: int
    max_triangles_per_edge: int
    h1_dimension: int
    alpha_weight: int
    beta_weight: int
    nonidentity_face_holonomies: int
    tree_edges: int
    non_tree_edges: int
    normalized_nonidentity_residuals: int
    normalized_distinct_nonidentity_residuals: int
    commuting_pair_candidates: int
    pair_candidates_tested: int
    propagation_assignments: int
    accepted_decompositions: int
    first_accepted: bool
    first_pair_matches_planted_after_public_success: bool | None
    first_gauge_matches_planted_after_public_success: bool | None


_INVOLUTIONS: tuple[Permutation5, ...] = tuple(
    value
    for value in _A5
    if value != _IDENTITY and compose(value, value) == _IDENTITY
)
_COMMUTING_PAIRS: tuple[tuple[Permutation5, Permutation5], ...] = tuple(
    (left, right)
    for left in _INVOLUTIONS
    for right in _INVOLUTIONS
    if left != right and compose(left, right) == compose(right, left)
)


def _carrier_params(params: NAT6Parameters) -> CohomologyCycleParameters:
    return CohomologyCycleParameters(
        params.name + "-carrier",
        params.rows,
        params.cols,
        params.successful_flips,
    )


def _cohomology_basis_pair(
    target: SimplicialComplex,
) -> tuple[tuple[int, ...], tuple[int, ...], int]:
    edges = _edges(target)
    edge_index = {edge: index for index, edge in enumerate(edges)}

    triangle_rows: list[int] = []
    for triangle in _triangles(target):
        mask = 0
        for edge in combinations(triangle, 2):
            mask ^= 1 << edge_index[tuple(sorted(edge))]
        triangle_rows.append(mask)
    cocycle_rref = _rref(triangle_rows, len(edges))
    cocycle_basis = _nullspace_basis(cocycle_rref, len(edges))

    coboundary_rows: list[int] = []
    for vertex in target.vertices:
        mask = 0
        for index, edge in enumerate(edges):
            if vertex in edge:
                mask ^= 1 << index
        coboundary_rows.append(mask)
    base_rank = _rref(coboundary_rows, len(edges)).rank
    h1_dimension = len(cocycle_basis) - base_rank
    if h1_dimension != 2:
        raise NAT6Error("NAT6 carrier does not expose H1 dimension two")

    selected: list[int] = []
    current_rows = list(coboundary_rows)
    current_rank = base_rank
    for vector in sorted(cocycle_basis):
        trial = _rref(current_rows + [vector], len(edges))
        if trial.rank == current_rank:
            continue
        selected.append(vector)
        current_rows.append(vector)
        current_rank = trial.rank
        if len(selected) == 2:
            break
    if len(selected) != 2:
        raise NAT6Error("NAT6 failed to select two independent public cocycles")

    alpha = tuple((selected[0] >> index) & 1 for index in range(len(edges)))
    beta = tuple((selected[1] >> index) & 1 for index in range(len(edges)))
    if not any(alpha) or not any(beta) or alpha == beta:
        raise NAT6Error("NAT6 selected a degenerate public cohomology pair")
    return alpha, beta, h1_dimension


def _core_labels(
    alpha: tuple[int, ...],
    beta: tuple[int, ...],
    pair: tuple[Permutation5, Permutation5],
) -> tuple[Permutation5, ...]:
    left, right = pair
    result: list[Permutation5] = []
    for first, second in zip(alpha, beta, strict=True):
        value = _IDENTITY
        if first:
            value = compose(value, left)
        if second:
            value = compose(value, right)
        result.append(value)
    return tuple(result)


def _observed_from_witness(
    target: SimplicialComplex,
    alpha: tuple[int, ...],
    beta: tuple[int, ...],
    labels: tuple[Permutation5, ...],
    pair: tuple[Permutation5, Permutation5],
) -> tuple[Permutation5, ...]:
    core = _core_labels(alpha, beta, pair)
    return tuple(
        compose(compose(inverse(labels[left]), core[index]), labels[right])
        for index, (left, right) in enumerate(_edges(target))
    )


def _pair_is_legal(pair: tuple[Permutation5, Permutation5]) -> bool:
    left, right = pair
    return (
        left in _INVOLUTIONS
        and right in _INVOLUTIONS
        and left != right
        and compose(left, right) == compose(right, left)
    )


def validate_nat6_witness(
    public: NAT6Public,
    labels: tuple[Permutation5, ...],
    pair: tuple[Permutation5, Permutation5],
) -> bool:
    if len(labels) != len(public.target.vertices) or labels[0] != _IDENTITY:
        return False
    if any(value not in _A5 for value in labels) or not _pair_is_legal(pair):
        return False
    return (
        _observed_from_witness(public.target, public.alpha, public.beta, labels, pair)
        == public.observed_edge_labels
    )


def _face_holonomies(public: NAT6Public) -> tuple[Permutation5, ...]:
    edges = _edges(public.target)
    edge_index = {edge: index for index, edge in enumerate(edges)}
    values: list[Permutation5] = []
    for a, b, c in _triangles(public.target):
        ab = public.observed_edge_labels[edge_index[(a, b)]]
        ac = public.observed_edge_labels[edge_index[(a, c)]]
        bc = public.observed_edge_labels[edge_index[(b, c)]]
        values.append(compose(compose(ab, bc), inverse(ac)))
    return tuple(values)


def _tree_adjacency(
    target: SimplicialComplex,
) -> tuple[list[list[tuple[int, int, bool]]], tuple[int, ...]]:
    edges = _edges(target)
    adjacency: list[list[tuple[int, int, bool]]] = [
        [] for _ in target.vertices
    ]
    for index, (left, right) in enumerate(edges):
        adjacency[left].append((right, index, True))
        adjacency[right].append((left, index, False))
    for values in adjacency:
        values.sort()

    parent = [-1] * len(target.vertices)
    parent[0] = 0
    tree_edges: list[int] = []
    queue = deque([0])
    while queue:
        current = queue.popleft()
        for neighbor, edge_index, _ in adjacency[current]:
            if parent[neighbor] != -1:
                continue
            parent[neighbor] = current
            tree_edges.append(edge_index)
            queue.append(neighbor)
    if any(value == -1 for value in parent):
        raise NAT6Error("NAT6 public primal graph is disconnected")
    return adjacency, tuple(sorted(tree_edges))


def _tree_normalized_residuals(
    public: NAT6Public,
) -> tuple[tuple[Permutation5, ...], tuple[int, ...]]:
    adjacency, tree_edges = _tree_adjacency(public.target)
    labels: list[Permutation5 | None] = [None] * len(public.target.vertices)
    labels[0] = _IDENTITY
    queue = deque([0])
    while queue:
        current = queue.popleft()
        current_label = labels[current]
        if current_label is None:
            raise NAT6Error("NAT6 tree normalization lost assigned state")
        for neighbor, edge_index, forward in adjacency[current]:
            if labels[neighbor] is not None:
                continue
            observed = public.observed_edge_labels[edge_index]
            labels[neighbor] = (
                compose(current_label, observed)
                if forward
                else compose(current_label, inverse(observed))
            )
            queue.append(neighbor)
    concrete = tuple(value if value is not None else _IDENTITY for value in labels)
    residuals = tuple(
        compose(
            compose(concrete[left], public.observed_edge_labels[index]),
            inverse(concrete[right]),
        )
        for index, (left, right) in enumerate(_edges(public.target))
    )
    return residuals, tree_edges


def _propagate_candidate_gauge(
    public: NAT6Public,
    pair: tuple[Permutation5, Permutation5],
) -> tuple[tuple[Permutation5, ...], int]:
    adjacency, _ = _tree_adjacency(public.target)
    core = _core_labels(public.alpha, public.beta, pair)
    labels: list[Permutation5 | None] = [None] * len(public.target.vertices)
    labels[0] = _IDENTITY
    queue = deque([0])
    assignments = 0
    while queue:
        current = queue.popleft()
        current_label = labels[current]
        if current_label is None:
            raise NAT6Error("NAT6 pair propagation lost assigned state")
        for neighbor, edge_index, forward in adjacency[current]:
            if labels[neighbor] is not None:
                continue
            observed = public.observed_edge_labels[edge_index]
            edge_core = core[edge_index]
            labels[neighbor] = (
                compose(compose(inverse(edge_core), current_label), observed)
                if forward
                else compose(compose(edge_core, current_label), inverse(observed))
            )
            assignments += 1
            queue.append(neighbor)
    concrete = tuple(value if value is not None else _IDENTITY for value in labels)
    return concrete, assignments


def generate_nat6_instance(
    params: NAT6Parameters,
    master_seed: bytes,
) -> tuple[NAT6Public, NAT6Reference]:
    params.validate()
    if len(master_seed) < 16:
        raise NAT6Error("NAT6 master seed must contain at least 128 bits")

    carrier_public, _ = generate_cohomology_cycle_instance(
        _carrier_params(params), master_seed
    )
    target = carrier_public.target
    alpha, beta, _ = _cohomology_basis_pair(target)
    if not _COMMUTING_PAIRS:
        raise NAT6Error("NAT6 A5 commuting-pair family is empty")
    digest = hashlib.sha256(
        b"MORPH-KEM NAT6 holonomy pair v1\x00"
        + master_seed
        + params.name.encode("ascii")
    ).digest()
    pair = _COMMUTING_PAIRS[int.from_bytes(digest[:8], "big") % len(_COMMUTING_PAIRS)]
    labels = _normalized_hidden_labels(target, master_seed, params.name + "-gauge")
    observed = _observed_from_witness(target, alpha, beta, labels, pair)
    public = NAT6Public(params.name, target, observed, alpha, beta)
    reference = NAT6Reference(labels, pair)
    if not validate_nat6_witness(public, labels, pair):
        raise NAT6Error("NAT6 generated witness failed its exact verifier")
    if any(value != _IDENTITY for value in _face_holonomies(public)):
        raise NAT6Error("NAT6 generated connection is not face-flat")
    return public, reference


def recover_nat6(
    public: NAT6Public,
    *,
    reference: NAT6Reference | None = None,
) -> NAT6Recovery:
    edges = _edges(public.target)
    triangles = _triangles(public.target)
    if len(public.alpha) != len(edges) or len(public.beta) != len(edges):
        raise NAT6Error("NAT6 public cocycle length mismatch")
    _, _, h1_dimension = _cohomology_basis_pair(public.target)

    face_holonomies = _face_holonomies(public)
    residuals, tree_edges = _tree_normalized_residuals(public)
    nonidentity_residuals = [value for value in residuals if value != _IDENTITY]

    accepted: list[tuple[tuple[Permutation5, Permutation5], tuple[Permutation5, ...]]] = []
    assignments = 0
    tested = 0
    for pair in _COMMUTING_PAIRS:
        tested += 1
        labels, work = _propagate_candidate_gauge(public, pair)
        assignments += work
        if validate_nat6_witness(public, labels, pair):
            accepted.append((pair, labels))

    edge_counts: Counter[tuple[int, int]] = Counter()
    for triangle in triangles:
        for edge in combinations(triangle, 2):
            edge_counts[tuple(sorted(edge))] += 1
    first = accepted[0] if accepted else None
    pair_match = None
    gauge_match = None
    if reference is not None and first is not None:
        pair_match = first[0] == reference.holonomy_pair
        gauge_match = first[1] == reference.hidden_vertex_labels_normalized

    return NAT6Recovery(
        vertices=len(public.target.vertices),
        edges=len(edges),
        triangles=len(triangles),
        euler_characteristic=len(public.target.vertices) - len(edges) + len(triangles),
        min_triangles_per_edge=min(edge_counts.values()) if edge_counts else 0,
        max_triangles_per_edge=max(edge_counts.values()) if edge_counts else 0,
        h1_dimension=h1_dimension,
        alpha_weight=sum(public.alpha),
        beta_weight=sum(public.beta),
        nonidentity_face_holonomies=sum(value != _IDENTITY for value in face_holonomies),
        tree_edges=len(tree_edges),
        non_tree_edges=len(edges) - len(tree_edges),
        normalized_nonidentity_residuals=len(nonidentity_residuals),
        normalized_distinct_nonidentity_residuals=len(set(nonidentity_residuals)),
        commuting_pair_candidates=len(_COMMUTING_PAIRS),
        pair_candidates_tested=tested,
        propagation_assignments=assignments,
        accepted_decompositions=len(accepted),
        first_accepted=first is not None,
        first_pair_matches_planted_after_public_success=pair_match,
        first_gauge_matches_planted_after_public_success=gauge_match,
    )
