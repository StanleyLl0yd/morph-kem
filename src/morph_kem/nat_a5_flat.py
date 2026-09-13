from __future__ import annotations

from dataclasses import dataclass
import hashlib
from math import comb

from .complex import SimplicialComplex
from .nat_a5 import (
    NAT3Error,
    NAT3Parameters,
    Permutation5,
    _A5,
    _IDENTITY,
    _THREE_CYCLES,
    _carrier,
    _clean_edge_labels,
    _digest,
    _face_holonomies,
    _normalized_hidden_labels,
    compose,
    inverse,
    is_three_cycle,
)
from .nat_coboundary import _edges


class NAT4Error(NAT3Error):
    """Raised when a NAT4 locally-flat toy instance is malformed."""


@dataclass(frozen=True, slots=True)
class NAT4Parameters:
    name: str
    triangle_count: int
    successful_flips: int
    deformation_weights: tuple[int, ...]

    def validate(self) -> None:
        if self.triangle_count not in (24, 30, 36):
            raise NAT4Error("NAT4 triangle count outside declared toy sets")
        if self.successful_flips < self.triangle_count or self.successful_flips > 5000:
            raise NAT4Error("NAT4 successful-flip target outside toy bounds")
        if not self.deformation_weights or tuple(sorted(set(self.deformation_weights))) != self.deformation_weights:
            raise NAT4Error("NAT4 deformation weights must be sorted and distinct")
        if any(weight < 1 or weight > 4 for weight in self.deformation_weights):
            raise NAT4Error("NAT4 deformation weight outside declared toy bounds")


NAT4_PARAMETER_SETS = {
    "nat4-F24": NAT4Parameters("nat4-F24", 24, 240, (1, 2, 3)),
    "nat4-F30": NAT4Parameters("nat4-F30", 30, 300, (1, 2, 3)),
    "nat4-F36": NAT4Parameters("nat4-F36", 36, 360, (1, 2, 3, 4)),
}


@dataclass(frozen=True, slots=True)
class NAT4Public:
    name: str
    target: SimplicialComplex
    observed_edge_labels: tuple[Permutation5, ...]
    public_deformation_weight: int


@dataclass(frozen=True, slots=True)
class NAT4Reference:
    hidden_clean_labels_normalized: tuple[Permutation5, ...]
    planted_deformation_labels: tuple[Permutation5, ...]
    planted_deformation_support: tuple[int, ...]
    effective_public_state: tuple[Permutation5, ...]
    rejected_flip_proposals: int


@dataclass(frozen=True, slots=True)
class NAT4Recovery:
    vertices: int
    edges: int
    triangles: int
    deformation_weight: int
    nonidentity_face_holonomies: int
    integration_edge_checks: int
    integration_consistent: bool
    equivalent_witness_lower_bound: int
    canonical_support: tuple[int, ...]
    canonical_witness_accepted: bool
    canonical_support_matches_planted_after_public_success: bool | None
    canonical_clean_state_matches_planted_after_public_success: bool | None
    effective_state_matches_reference_after_public_success: bool | None


def _nat3_carrier_params(params: NAT4Parameters) -> NAT3Parameters:
    return NAT3Parameters(
        params.name + "-carrier",
        params.triangle_count,
        params.successful_flips,
        (1,),
    )


def _deformation_support(
    vertex_count: int,
    weight: int,
    seed: bytes,
    name: str,
) -> tuple[int, ...]:
    if weight >= vertex_count:
        raise NAT4Error("NAT4 deformation weight leaves no normalized root")
    candidates = list(range(1, vertex_count))
    candidates.sort(
        key=lambda vertex: (
            _digest(b"MORPH-KEM NAT4 deformation support v1", seed, name, vertex),
            vertex,
        )
    )
    return tuple(sorted(candidates[:weight]))


def _planted_deformation(
    vertex_count: int,
    weight: int,
    seed: bytes,
    name: str,
) -> tuple[tuple[Permutation5, ...], tuple[int, ...]]:
    support = _deformation_support(vertex_count, weight, seed, name)
    labels: list[Permutation5] = [_IDENTITY] * vertex_count
    for vertex in support:
        digest = _digest(
            b"MORPH-KEM NAT4 deformation value v1",
            seed,
            name,
            vertex,
        )
        labels[vertex] = _THREE_CYCLES[int.from_bytes(digest[:8], "big") % len(_THREE_CYCLES)]
    return tuple(labels), support


def generate_nat4_instance(
    params: NAT4Parameters,
    master_seed: bytes,
    deformation_weight: int,
) -> tuple[NAT4Public, NAT4Reference]:
    params.validate()
    if len(master_seed) < 16:
        raise NAT4Error("NAT4 master seed must contain at least 128 bits")
    if deformation_weight not in params.deformation_weights:
        raise NAT4Error("NAT4 deformation weight is not in the public parameter sweep")

    target, rejected = _carrier(_nat3_carrier_params(params), master_seed)
    suffix = params.name + f"-w{deformation_weight}"
    hidden = _normalized_hidden_labels(target, master_seed, suffix)
    deformation, support = _planted_deformation(
        len(target.vertices), deformation_weight, master_seed, suffix
    )
    effective = tuple(
        compose(hidden[vertex], deformation[vertex])
        for vertex in range(len(hidden))
    )
    if effective[0] != _IDENTITY:
        raise NAT4Error("NAT4 effective state lost root normalization")
    observed = _clean_edge_labels(target, effective)

    public = NAT4Public(params.name, target, observed, deformation_weight)
    reference = NAT4Reference(hidden, deformation, support, effective, rejected)
    return public, reference


def validate_nat4_witness(
    public: NAT4Public,
    clean_labels: tuple[Permutation5, ...],
    deformation_labels: tuple[Permutation5, ...],
) -> bool:
    vertex_count = len(public.target.vertices)
    if len(clean_labels) != vertex_count or len(deformation_labels) != vertex_count:
        return False
    if clean_labels[0] != _IDENTITY or deformation_labels[0] != _IDENTITY:
        return False
    if any(label not in _A5 for label in clean_labels):
        return False

    support = []
    for vertex, value in enumerate(deformation_labels):
        if value == _IDENTITY:
            continue
        if vertex == 0 or not is_three_cycle(value):
            return False
        support.append(vertex)
    if len(support) != public.public_deformation_weight:
        return False

    effective = tuple(
        compose(clean_labels[vertex], deformation_labels[vertex])
        for vertex in range(vertex_count)
    )
    return _clean_edge_labels(public.target, effective) == public.observed_edge_labels


def _integrate_observed(
    public: NAT4Public,
) -> tuple[tuple[Permutation5, ...], int, bool]:
    edges = _edges(public.target)
    adjacency: dict[int, list[tuple[int, int, bool]]] = {
        vertex: [] for vertex in public.target.vertices
    }
    for edge_index, (left, right) in enumerate(edges):
        adjacency[left].append((right, edge_index, True))
        adjacency[right].append((left, edge_index, False))
    for values in adjacency.values():
        values.sort()

    labels: list[Permutation5 | None] = [None] * len(public.target.vertices)
    labels[0] = _IDENTITY
    queue = [0]
    checks = 0
    consistent = True
    while queue and consistent:
        current = queue.pop(0)
        current_label = labels[current]
        if current_label is None:
            raise NAT4Error("NAT4 integration lost assigned state")
        for neighbor, edge_index, forward in adjacency[current]:
            checks += 1
            edge_label = public.observed_edge_labels[edge_index]
            candidate = (
                compose(current_label, edge_label)
                if forward
                else compose(current_label, inverse(edge_label))
            )
            if labels[neighbor] is None:
                labels[neighbor] = candidate
                queue.append(neighbor)
            elif labels[neighbor] != candidate:
                consistent = False
                break
    if any(label is None for label in labels):
        consistent = False
    concrete = tuple(
        _IDENTITY if label is None else label
        for label in labels
    )
    return concrete, checks, consistent


def recover_nat4(
    public: NAT4Public,
    *,
    reference: NAT4Reference | None = None,
) -> NAT4Recovery:
    holonomies = _face_holonomies(
        type("CurvaturePublic", (), {
            "target": public.target,
            "observed_edge_labels": public.observed_edge_labels,
        })()
    )
    nonidentity = sum(value != _IDENTITY for value in holonomies)

    effective, edge_checks, consistent = _integrate_observed(public)
    if not consistent:
        raise NAT4Error("NAT4 locally-flat observations failed public integration")

    vertices = len(public.target.vertices)
    weight = public.public_deformation_weight
    support = tuple(range(1, 1 + weight))
    deformation = [_IDENTITY] * vertices
    fixed_noise = _THREE_CYCLES[0]
    for vertex in support:
        deformation[vertex] = fixed_noise
    deformation_tuple = tuple(deformation)
    clean = tuple(
        compose(effective[vertex], inverse(deformation_tuple[vertex]))
        for vertex in range(vertices)
    )
    accepted = validate_nat4_witness(public, clean, deformation_tuple)

    support_match = None
    clean_match = None
    effective_match = None
    if reference is not None:
        support_match = support == reference.planted_deformation_support
        clean_match = clean == reference.hidden_clean_labels_normalized
        effective_match = effective == reference.effective_public_state

    equivalent_lower_bound = comb(vertices - 1, weight) * (len(_THREE_CYCLES) ** weight)

    return NAT4Recovery(
        vertices=vertices,
        edges=len(_edges(public.target)),
        triangles=sum(1 for simplex in public.target.simplices if len(simplex) == 3),
        deformation_weight=weight,
        nonidentity_face_holonomies=nonidentity,
        integration_edge_checks=edge_checks,
        integration_consistent=consistent,
        equivalent_witness_lower_bound=equivalent_lower_bound,
        canonical_support=support,
        canonical_witness_accepted=accepted,
        canonical_support_matches_planted_after_public_success=support_match,
        canonical_clean_state_matches_planted_after_public_success=clean_match,
        effective_state_matches_reference_after_public_success=effective_match,
    )
