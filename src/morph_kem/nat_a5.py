from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass
import hashlib
from itertools import combinations, permutations
from math import comb

from .complex import SimplicialComplex
from .gluing_mixed_sphere import MixedSphereParameters, _grow_icosahedron, _mix_facets, _public_relabel
from .nat_coboundary import _edges


class NAT3Error(ValueError):
    """Raised when a NAT3 A5 toy experiment is malformed."""


Permutation5 = tuple[int, int, int, int, int]
_IDENTITY: Permutation5 = (0, 1, 2, 3, 4)


def compose(left: Permutation5, right: Permutation5) -> Permutation5:
    return tuple(left[right[index]] for index in range(5))  # type: ignore[return-value]


def inverse(value: Permutation5) -> Permutation5:
    result = [0, 0, 0, 0, 0]
    for index, image in enumerate(value):
        result[image] = index
    return tuple(result)  # type: ignore[return-value]


def parity(value: Permutation5) -> int:
    inversions = 0
    for left in range(5):
        for right in range(left + 1, 5):
            inversions += value[left] > value[right]
    return inversions & 1


def _cycle_type(value: Permutation5) -> tuple[int, ...]:
    seen: set[int] = set()
    lengths: list[int] = []
    for start in range(5):
        if start in seen:
            continue
        current = start
        length = 0
        while current not in seen:
            seen.add(current)
            length += 1
            current = value[current]
        if length > 1:
            lengths.append(length)
    return tuple(sorted(lengths))


_A5: tuple[Permutation5, ...] = tuple(
    value
    for value in permutations(range(5))
    if parity(value) == 0
)  # type: ignore[assignment]
_THREE_CYCLES: tuple[Permutation5, ...] = tuple(
    value for value in _A5 if _cycle_type(value) == (3,)
)


@dataclass(frozen=True, slots=True)
class NAT3Parameters:
    name: str
    triangle_count: int
    successful_flips: int
    noise_weights: tuple[int, ...]

    def validate(self) -> None:
        if self.triangle_count not in (24, 30, 36):
            raise NAT3Error("NAT3 triangle count outside declared toy sets")
        if self.successful_flips < self.triangle_count or self.successful_flips > 5000:
            raise NAT3Error("NAT3 successful-flip target outside toy bounds")
        if not self.noise_weights or tuple(sorted(set(self.noise_weights))) != self.noise_weights:
            raise NAT3Error("NAT3 noise weights must be sorted and distinct")
        if any(weight < 1 or weight > 3 for weight in self.noise_weights):
            raise NAT3Error("NAT3 noise weight outside declared toy bounds")


NAT3_PARAMETER_SETS = {
    "nat3-F24": NAT3Parameters("nat3-F24", 24, 240, (1, 2, 3)),
    "nat3-F30": NAT3Parameters("nat3-F30", 30, 300, (1, 2, 3)),
    "nat3-F36": NAT3Parameters("nat3-F36", 36, 360, (1, 2, 3)),
}


@dataclass(frozen=True, slots=True)
class NAT3Public:
    name: str
    target: SimplicialComplex
    observed_edge_labels: tuple[Permutation5, ...]
    public_noise_weight: int


@dataclass(frozen=True, slots=True)
class NAT3Reference:
    hidden_vertex_labels_normalized: tuple[Permutation5, ...]
    planted_noise_edges: tuple[int, ...]
    planted_noise_labels: tuple[Permutation5, ...]
    rejected_flip_proposals: int


@dataclass(frozen=True, slots=True)
class NAT3Recovery:
    vertices: int
    edges: int
    triangles: int
    noise_weight: int
    curvature_defect_faces: int
    curvature_class_histogram: tuple[tuple[str, int], ...]
    total_support_combinations: int
    curvature_hitting_supports: int
    propagated_supports: int
    connected_consistent_supports: int
    accepted_states: int
    stored_state_cap: int
    stored_state_cap_hit: bool
    first_state_accepted: bool
    first_state_noise_edges: tuple[int, ...]
    first_support_matches_planted_after_public_success: bool | None
    first_state_matches_planted_after_public_success: bool | None
    planted_support_is_curvature_hitting: bool | None


def _digest(domain: bytes, seed: bytes, name: str, counter: int = 0) -> bytes:
    return hashlib.sha256(
        domain + b"\x00" + seed + name.encode("ascii") + counter.to_bytes(8, "big")
    ).digest()


def _carrier(params: NAT3Parameters, seed: bytes) -> tuple[SimplicialComplex, int]:
    mixed = MixedSphereParameters(
        params.name + "-carrier",
        params.triangle_count,
        params.successful_flips,
    )
    mixed.validate()
    growth_seed = _digest(b"MORPH-KEM NAT3 growth v1", seed, params.name)
    flip_seed = _digest(b"MORPH-KEM NAT3 flips v1", seed, params.name)
    relabel_seed = _digest(b"MORPH-KEM NAT3 relabel v1", seed, params.name)
    facets = _grow_icosahedron(mixed, growth_seed)
    mixed_facets, rejected = _mix_facets(mixed, facets, flip_seed)
    return _public_relabel(mixed_facets, relabel_seed), rejected


def _triangles(target: SimplicialComplex) -> tuple[tuple[int, int, int], ...]:
    return tuple(sorted(simplex for simplex in target.simplices if len(simplex) == 3))


def _normalized_hidden_labels(
    target: SimplicialComplex,
    seed: bytes,
    name: str,
) -> tuple[Permutation5, ...]:
    vertices = tuple(sorted(target.vertices))
    if vertices != tuple(range(len(vertices))):
        raise NAT3Error("NAT3 public carrier vertices are not contiguous")
    labels = tuple(
        _A5[
            int.from_bytes(
                _digest(b"MORPH-KEM NAT3 hidden A5 v1", seed, name, vertex)[:8],
                "big",
            )
            % len(_A5)
        ]
        for vertex in vertices
    )
    left = inverse(labels[0])
    return tuple(compose(left, label) for label in labels)


def _clean_edge_labels(
    target: SimplicialComplex,
    labels: tuple[Permutation5, ...],
) -> tuple[Permutation5, ...]:
    return tuple(
        compose(inverse(labels[left]), labels[right])
        for left, right in _edges(target)
    )


def _seeded_noise_edges(
    edge_count: int,
    weight: int,
    seed: bytes,
    name: str,
) -> tuple[int, ...]:
    order = sorted(
        range(edge_count),
        key=lambda index: (
            _digest(b"MORPH-KEM NAT3 noise edge v1", seed, name, index),
            index,
        ),
    )
    return tuple(sorted(order[:weight]))


def generate_nat3_instance(
    params: NAT3Parameters,
    master_seed: bytes,
    noise_weight: int,
) -> tuple[NAT3Public, NAT3Reference]:
    params.validate()
    if len(master_seed) < 16:
        raise NAT3Error("NAT3 master seed must contain at least 128 bits")
    if noise_weight not in params.noise_weights:
        raise NAT3Error("NAT3 noise weight is not in the public parameter sweep")

    target, rejected = _carrier(params, master_seed)
    suffix = params.name + f"-w{noise_weight}"
    hidden = _normalized_hidden_labels(target, master_seed, suffix)
    observed = list(_clean_edge_labels(target, hidden))
    noise_edges = _seeded_noise_edges(len(observed), noise_weight, master_seed, suffix)
    noise_labels: list[Permutation5] = []
    for edge_index in noise_edges:
        digest = _digest(
            b"MORPH-KEM NAT3 3-cycle noise v1",
            master_seed,
            suffix,
            edge_index,
        )
        noise = _THREE_CYCLES[int.from_bytes(digest[:8], "big") % len(_THREE_CYCLES)]
        observed[edge_index] = compose(observed[edge_index], noise)
        noise_labels.append(noise)

    return (
        NAT3Public(params.name, target, tuple(observed), noise_weight),
        NAT3Reference(hidden, noise_edges, tuple(noise_labels), rejected),
    )


def is_three_cycle(value: Permutation5) -> bool:
    return value in _THREE_CYCLES


def validate_nat3_state(
    public: NAT3Public,
    labels: tuple[Permutation5, ...],
) -> tuple[bool, tuple[int, ...]]:
    if len(labels) != len(public.target.vertices) or labels[0] != _IDENTITY:
        return False, ()
    noisy: list[int] = []
    for edge_index, (left, right) in enumerate(_edges(public.target)):
        clean = compose(inverse(labels[left]), labels[right])
        delta = compose(inverse(clean), public.observed_edge_labels[edge_index])
        if delta == _IDENTITY:
            continue
        if not is_three_cycle(delta):
            return False, ()
        noisy.append(edge_index)
    return len(noisy) == public.public_noise_weight, tuple(noisy)


def _triangle_edge_indices(target: SimplicialComplex) -> tuple[tuple[int, int, int], ...]:
    edges = _edges(target)
    edge_index = {edge: index for index, edge in enumerate(edges)}
    result = []
    for a, b, c in _triangles(target):
        result.append((edge_index[(a, b)], edge_index[(a, c)], edge_index[(b, c)]))
    return tuple(result)


def _face_holonomies(public: NAT3Public) -> tuple[Permutation5, ...]:
    values: list[Permutation5] = []
    for ab, ac, bc in _triangle_edge_indices(public.target):
        holonomy = compose(
            compose(public.observed_edge_labels[ab], public.observed_edge_labels[bc]),
            inverse(public.observed_edge_labels[ac]),
        )
        values.append(holonomy)
    return tuple(values)


def _curvature_label(value: Permutation5) -> str:
    cycle = _cycle_type(value)
    if cycle == ():
        return "identity"
    return "-".join(str(length) for length in cycle)


def _propagate_clean_subgraph(
    public: NAT3Public,
    support: tuple[int, ...],
) -> tuple[tuple[Permutation5, ...] | None, bool, bool]:
    support_set = set(support)
    edges = _edges(public.target)
    adjacency: dict[int, list[tuple[int, int, bool]]] = {
        vertex: [] for vertex in public.target.vertices
    }
    for edge_index, (left, right) in enumerate(edges):
        if edge_index in support_set:
            continue
        adjacency[left].append((right, edge_index, True))
        adjacency[right].append((left, edge_index, False))
    for values in adjacency.values():
        values.sort()

    labels: list[Permutation5 | None] = [None] * len(public.target.vertices)
    labels[0] = _IDENTITY
    queue = deque([0])
    consistent = True
    while queue and consistent:
        current = queue.popleft()
        current_label = labels[current]
        if current_label is None:
            raise NAT3Error("NAT3 propagation queue lost its assigned label")
        for neighbor, edge_index, forward in adjacency[current]:
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

    connected = all(label is not None for label in labels)
    if not connected or not consistent:
        return None, connected, consistent
    concrete = tuple(labels)
    return concrete, connected, consistent  # type: ignore[return-value]


def recover_nat3(
    public: NAT3Public,
    *,
    reference: NAT3Reference | None = None,
    state_cap: int = 16,
) -> NAT3Recovery:
    if state_cap < 1 or state_cap > 256:
        raise NAT3Error("NAT3 state cap outside toy bounds")

    holonomies = _face_holonomies(public)
    defect_faces = tuple(index for index, value in enumerate(holonomies) if value != _IDENTITY)
    class_hist = Counter(_curvature_label(value) for value in holonomies if value != _IDENTITY)
    boundaries = _triangle_edge_indices(public.target)
    defect_boundaries = tuple(set(boundaries[index]) for index in defect_faces)

    edge_count = len(_edges(public.target))
    total_supports = comb(edge_count, public.public_noise_weight)
    hitting_supports: list[tuple[int, ...]] = []
    for support in combinations(range(edge_count), public.public_noise_weight):
        support_set = set(support)
        if all(support_set.intersection(boundary) for boundary in defect_boundaries):
            hitting_supports.append(support)

    propagated = 0
    connected_consistent = 0
    accepted_total = 0
    stored: list[tuple[tuple[Permutation5, ...], tuple[int, ...]]] = []
    for support in hitting_supports:
        propagated += 1
        labels, connected, consistent = _propagate_clean_subgraph(public, support)
        if not connected or not consistent or labels is None:
            continue
        connected_consistent += 1
        accepted, inferred_support = validate_nat3_state(public, labels)
        if not accepted:
            continue
        accepted_total += 1
        if len(stored) < state_cap:
            stored.append((labels, inferred_support))

    first_accepted = bool(stored)
    first_noise: tuple[int, ...] = ()
    support_match = None
    state_match = None
    planted_hitting = None
    if reference is not None:
        planted = set(reference.planted_noise_edges)
        planted_hitting = all(planted.intersection(boundary) for boundary in defect_boundaries)
    if stored:
        labels, first_noise = stored[0]
        if reference is not None:
            support_match = first_noise == reference.planted_noise_edges
            state_match = labels == reference.hidden_vertex_labels_normalized
    elif reference is not None:
        support_match = False
        state_match = False

    return NAT3Recovery(
        vertices=len(public.target.vertices),
        edges=edge_count,
        triangles=len(_triangles(public.target)),
        noise_weight=public.public_noise_weight,
        curvature_defect_faces=len(defect_faces),
        curvature_class_histogram=tuple(sorted(class_hist.items())),
        total_support_combinations=total_supports,
        curvature_hitting_supports=len(hitting_supports),
        propagated_supports=propagated,
        connected_consistent_supports=connected_consistent,
        accepted_states=accepted_total,
        stored_state_cap=state_cap,
        stored_state_cap_hit=accepted_total > state_cap,
        first_state_accepted=first_accepted,
        first_state_noise_edges=first_noise,
        first_support_matches_planted_after_public_success=support_match,
        first_state_matches_planted_after_public_success=state_match,
        planted_support_is_curvature_hitting=planted_hitting,
    )
