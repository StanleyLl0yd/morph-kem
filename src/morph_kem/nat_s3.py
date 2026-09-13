from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import hashlib
from itertools import permutations

from .complex import SimplicialComplex
from .gluing_mixed_sphere import (
    MixedSphereParameters,
    _grow_icosahedron,
    _mix_facets,
    _public_relabel,
)
from .nat_coboundary import _edges, _recover_vertex_mask_from_clean, _violated_triangles
from .nat_tjoin import _minimum_t_join


class NAT2Error(ValueError):
    """Raised when a NAT2 toy experiment is malformed."""


Permutation = tuple[int, int, int]
StateSolution = tuple[tuple[Permutation, ...], tuple[int, ...]]
_IDENTITY: Permutation = (0, 1, 2)
_S3: tuple[Permutation, ...] = tuple(permutations(range(3)))  # type: ignore[assignment]
_TRANSPOSITIONS: tuple[Permutation, ...] = ((1, 0, 2), (2, 1, 0), (0, 2, 1))


@dataclass(frozen=True, slots=True)
class NAT2Parameters:
    name: str
    triangle_count: int
    successful_flips: int
    noise_weights: tuple[int, ...]

    def validate(self) -> None:
        if self.triangle_count not in (24, 30, 36):
            raise NAT2Error("NAT2 triangle count outside declared toy sets")
        if self.successful_flips < self.triangle_count or self.successful_flips > 5000:
            raise NAT2Error("NAT2 successful-flip target outside toy bounds")
        if not self.noise_weights or tuple(sorted(set(self.noise_weights))) != self.noise_weights:
            raise NAT2Error("NAT2 noise weights must be sorted and distinct")
        if any(weight < 1 or weight > 4 for weight in self.noise_weights):
            raise NAT2Error("NAT2 noise weight outside toy bounds")


NAT2_PARAMETER_SETS = {
    "nat2-F24": NAT2Parameters("nat2-F24", 24, 240, (1, 2, 3)),
    "nat2-F30": NAT2Parameters("nat2-F30", 30, 300, (1, 2, 3)),
    "nat2-F36": NAT2Parameters("nat2-F36", 36, 360, (1, 2, 3, 4)),
}


@dataclass(frozen=True, slots=True)
class NAT2Public:
    name: str
    target: SimplicialComplex
    observed_edge_labels: tuple[Permutation, ...]
    public_noise_weight: int


@dataclass(frozen=True, slots=True)
class NAT2Reference:
    hidden_vertex_labels_normalized: tuple[Permutation, ...]
    planted_noise_edges: tuple[int, ...]
    planted_noise_labels: tuple[Permutation, ...]
    rejected_flip_proposals: int


@dataclass(frozen=True, slots=True)
class NAT2Recovery:
    vertices: int
    edges: int
    triangles: int
    noise_weight: int
    sign_syndrome_weight: int
    sign_tjoin_weight: int
    sign_tjoin_dp_states: int
    sign_tjoin_pair_tests: int
    sign_clean_parity_accepted: bool
    sign_matches_planted_noise_after_public_success: bool | None
    sign_matches_hidden_vertex_parity_after_public_success: bool | None
    csp_nodes: int
    csp_backtracks: int
    accepted_states: int
    accepted_state_cap: int
    accepted_state_cap_hit: bool
    first_state_accepted: bool
    first_state_noise_edges: tuple[int, ...]
    first_state_matches_hidden_after_public_success: bool | None


def compose(left: Permutation, right: Permutation) -> Permutation:
    return tuple(left[right[index]] for index in range(3))  # type: ignore[return-value]


def inverse(value: Permutation) -> Permutation:
    result = [0, 0, 0]
    for index, image in enumerate(value):
        result[image] = index
    return tuple(result)  # type: ignore[return-value]


def parity(value: Permutation) -> int:
    return sum(
        value[left] > value[right]
        for left in range(3)
        for right in range(left + 1, 3)
    ) & 1


def is_transposition(value: Permutation) -> bool:
    return value in _TRANSPOSITIONS


def _digest(domain: bytes, seed: bytes, name: str, counter: int = 0) -> bytes:
    return hashlib.sha256(
        domain + b"\x00" + seed + name.encode("ascii") + counter.to_bytes(8, "big")
    ).digest()


def _carrier(params: NAT2Parameters, seed: bytes) -> tuple[SimplicialComplex, int]:
    mixed = MixedSphereParameters(
        params.name + "-carrier", params.triangle_count, params.successful_flips
    )
    mixed.validate()
    facets = _grow_icosahedron(
        mixed, _digest(b"MORPH-KEM NAT2 growth v1", seed, params.name)
    )
    mixed_facets, rejected = _mix_facets(
        mixed, facets, _digest(b"MORPH-KEM NAT2 flips v1", seed, params.name)
    )
    target = _public_relabel(
        mixed_facets, _digest(b"MORPH-KEM NAT2 relabel v1", seed, params.name)
    )
    return target, rejected


def _normalized_hidden_labels(
    target: SimplicialComplex, seed: bytes, name: str
) -> tuple[Permutation, ...]:
    vertices = tuple(sorted(target.vertices))
    if vertices != tuple(range(len(vertices))):
        raise NAT2Error("NAT2 public relabeling did not produce contiguous vertices")
    labels = tuple(
        _S3[
            int.from_bytes(
                _digest(b"MORPH-KEM NAT2 hidden S3 v1", seed, name, vertex)[:8],
                "big",
            )
            % len(_S3)
        ]
        for vertex in vertices
    )
    gauge = inverse(labels[0])
    return tuple(compose(gauge, label) for label in labels)


def _clean_edge_labels(
    target: SimplicialComplex, labels: tuple[Permutation, ...]
) -> tuple[Permutation, ...]:
    return tuple(
        compose(inverse(labels[left]), labels[right]) for left, right in _edges(target)
    )


def _noise_edges(edge_count: int, weight: int, seed: bytes, name: str) -> tuple[int, ...]:
    ordered = sorted(
        range(edge_count),
        key=lambda index: (
            _digest(b"MORPH-KEM NAT2 noise edge v1", seed, name, index),
            index,
        ),
    )
    return tuple(sorted(ordered[:weight]))


def generate_nat2_instance(
    params: NAT2Parameters, master_seed: bytes, noise_weight: int
) -> tuple[NAT2Public, NAT2Reference]:
    params.validate()
    if len(master_seed) < 16:
        raise NAT2Error("NAT2 master seed must contain at least 128 bits")
    if noise_weight not in params.noise_weights:
        raise NAT2Error("NAT2 noise weight is not in the public parameter sweep")

    target, rejected = _carrier(params, master_seed)
    suffix = params.name + f"-w{noise_weight}"
    hidden = _normalized_hidden_labels(target, master_seed, suffix)
    observed = list(_clean_edge_labels(target, hidden))
    noise_edges = _noise_edges(len(observed), noise_weight, master_seed, suffix)
    noise_labels: list[Permutation] = []
    for edge_index in noise_edges:
        digest = _digest(
            b"MORPH-KEM NAT2 transposition v1", master_seed, suffix, edge_index
        )
        transposition = _TRANSPOSITIONS[int.from_bytes(digest[:8], "big") % 3]
        observed[edge_index] = compose(observed[edge_index], transposition)
        noise_labels.append(transposition)
    return (
        NAT2Public(params.name, target, tuple(observed), noise_weight),
        NAT2Reference(hidden, noise_edges, tuple(noise_labels), rejected),
    )


def _observed_sign_mask(public: NAT2Public) -> int:
    return sum(
        parity(value) << edge_index
        for edge_index, value in enumerate(public.observed_edge_labels)
    )


def _labels_parity_mask(labels: tuple[Permutation, ...]) -> int:
    return sum(parity(label) << vertex for vertex, label in enumerate(labels))


def validate_nat2_state(
    public: NAT2Public, labels: tuple[Permutation, ...]
) -> tuple[bool, tuple[int, ...]]:
    if len(labels) != len(public.target.vertices) or labels[0] != _IDENTITY:
        return False, ()
    noisy: list[int] = []
    for edge_index, (left, right) in enumerate(_edges(public.target)):
        clean = compose(inverse(labels[left]), labels[right])
        residual = compose(inverse(clean), public.observed_edge_labels[edge_index])
        if residual == _IDENTITY:
            continue
        if not is_transposition(residual):
            return False, ()
        noisy.append(edge_index)
    return len(noisy) == public.public_noise_weight, tuple(noisy)


def _spanning_tree(target: SimplicialComplex) -> tuple[tuple[int, int, int], ...]:
    edges = _edges(target)
    adjacency: dict[int, list[tuple[int, int]]] = {
        vertex: [] for vertex in target.vertices
    }
    for edge_index, (left, right) in enumerate(edges):
        adjacency[left].append((right, edge_index))
        adjacency[right].append((left, edge_index))
    for row in adjacency.values():
        row.sort()
    root = min(target.vertices)
    seen = {root}
    queue = deque([root])
    tree: list[tuple[int, int, int]] = []
    while queue:
        parent = queue.popleft()
        for child, edge_index in adjacency[parent]:
            if child in seen:
                continue
            seen.add(child)
            tree.append((parent, child, edge_index))
            queue.append(child)
    if len(seen) != len(target.vertices):
        raise NAT2Error("NAT2 public primal graph is disconnected")
    return tuple(tree)


def _derive_child_label(
    parent: int,
    child: int,
    edge: tuple[int, int],
    parent_label: Permutation,
    observed: Permutation,
    noise: Permutation | None,
) -> Permutation:
    # observed = clean * tau and every allowed tau is an involution.
    clean = observed if noise is None else compose(observed, noise)
    left, right = edge
    if parent == left and child == right:
        return compose(parent_label, clean)
    if parent == right and child == left:
        return compose(parent_label, inverse(clean))
    raise NAT2Error("NAT2 spanning-tree orientation mismatch")


def _exact_state_search(
    public: NAT2Public, *, solution_cap: int = 16
) -> tuple[tuple[StateSolution, ...], int, int, bool]:
    vertices = tuple(sorted(public.target.vertices))
    if vertices != tuple(range(len(vertices))):
        raise NAT2Error("NAT2 state search requires contiguous public vertices")
    edges = _edges(public.target)
    tree = _spanning_tree(public.target)
    tree_indices = {edge_index for _, _, edge_index in tree}
    non_tree = tuple(index for index in range(len(edges)) if index not in tree_indices)
    labels: list[Permutation | None] = [None] * len(vertices)
    labels[0] = _IDENTITY
    solutions: list[StateSolution] = []
    nodes = 0
    backtracks = 0
    cap_hit = False

    def finish(tree_noise: tuple[int, ...]) -> None:
        nonlocal backtracks, cap_hit
        if any(label is None for label in labels):
            raise NAT2Error("NAT2 exact search reached incomplete state")
        concrete: tuple[Permutation, ...] = tuple(labels)  # type: ignore[assignment]
        noisy = list(tree_noise)
        for edge_index in non_tree:
            left, right = edges[edge_index]
            clean = compose(inverse(concrete[left]), concrete[right])
            residual = compose(inverse(clean), public.observed_edge_labels[edge_index])
            if residual == _IDENTITY:
                continue
            if not is_transposition(residual):
                backtracks += 1
                return
            noisy.append(edge_index)
            if len(noisy) > public.public_noise_weight:
                backtracks += 1
                return
        if len(noisy) != public.public_noise_weight:
            backtracks += 1
            return
        accepted, verifier_noise = validate_nat2_state(public, concrete)
        if not accepted:
            raise NAT2Error("NAT2 exact search produced verifier-rejected state")
        solutions.append((concrete, verifier_noise))
        cap_hit = len(solutions) >= solution_cap

    def search(tree_index: int, noisy: tuple[int, ...]) -> None:
        nonlocal nodes, backtracks
        if cap_hit:
            return
        nodes += 1
        if tree_index == len(tree):
            finish(noisy)
            return
        parent, child, edge_index = tree[tree_index]
        parent_label = labels[parent]
        if parent_label is None:
            raise NAT2Error("NAT2 spanning tree is not parent-first")
        progressed = False
        for noise in (None,) + _TRANSPOSITIONS:
            extra = int(noise is not None)
            if len(noisy) + extra > public.public_noise_weight:
                continue
            labels[child] = _derive_child_label(
                parent,
                child,
                edges[edge_index],
                parent_label,
                public.observed_edge_labels[edge_index],
                noise,
            )
            progressed = True
            search(
                tree_index + 1,
                noisy if noise is None else noisy + (edge_index,),
            )
            labels[child] = None
            if cap_hit:
                return
        if not progressed:
            backtracks += 1

    search(0, ())
    return tuple(solutions), nodes, backtracks, cap_hit


def recover_nat2(
    public: NAT2Public,
    *,
    reference: NAT2Reference | None = None,
    solution_cap: int = 16,
) -> NAT2Recovery:
    sign_mask = _observed_sign_mask(public)
    defects = _violated_triangles(public.target, sign_mask)
    correction, _, _, dp_states, pair_tests, _ = _minimum_t_join(public.target, defects)
    clean_sign = sign_mask ^ correction
    recovered_parity = _recover_vertex_mask_from_clean(public.target, clean_sign)

    sign_match_noise = None
    sign_match_hidden = None
    if reference is not None:
        planted_noise = sum(1 << edge for edge in reference.planted_noise_edges)
        sign_match_noise = correction == planted_noise
        sign_match_hidden = recovered_parity == _labels_parity_mask(
            reference.hidden_vertex_labels_normalized
        )

    solutions, nodes, backtracks, cap_hit = _exact_state_search(
        public, solution_cap=solution_cap
    )
    first_accepted = bool(solutions)
    first_noise: tuple[int, ...] = ()
    first_matches_hidden = None
    if solutions:
        first_labels, first_noise = solutions[0]
        if reference is not None:
            first_matches_hidden = first_labels == reference.hidden_vertex_labels_normalized
    elif reference is not None:
        first_matches_hidden = False

    triangle_count = sum(1 for simplex in public.target.simplices if len(simplex) == 3)
    return NAT2Recovery(
        vertices=len(public.target.vertices),
        edges=len(_edges(public.target)),
        triangles=triangle_count,
        noise_weight=public.public_noise_weight,
        sign_syndrome_weight=len(defects),
        sign_tjoin_weight=correction.bit_count(),
        sign_tjoin_dp_states=dp_states,
        sign_tjoin_pair_tests=pair_tests,
        sign_clean_parity_accepted=True,
        sign_matches_planted_noise_after_public_success=sign_match_noise,
        sign_matches_hidden_vertex_parity_after_public_success=sign_match_hidden,
        csp_nodes=nodes,
        csp_backtracks=backtracks,
        accepted_states=len(solutions),
        accepted_state_cap=solution_cap,
        accepted_state_cap_hit=cap_hit,
        first_state_accepted=first_accepted,
        first_state_noise_edges=first_noise,
        first_state_matches_hidden_after_public_success=first_matches_hidden,
    )
