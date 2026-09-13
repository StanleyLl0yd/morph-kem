from __future__ import annotations

from dataclasses import dataclass
import hashlib

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


class NAT5Error(NAT3Error):
    """Raised when a NAT5 coupled-cycle toy instance is malformed."""


@dataclass(frozen=True, slots=True)
class NAT5Parameters:
    name: str
    triangle_count: int
    successful_flips: int
    cycle_length: int

    def validate(self) -> None:
        if self.triangle_count not in (24, 30, 36):
            raise NAT5Error("NAT5 triangle count outside declared toy sets")
        if self.successful_flips < self.triangle_count or self.successful_flips > 5000:
            raise NAT5Error("NAT5 successful-flip target outside toy bounds")
        if self.cycle_length not in (4, 6):
            raise NAT5Error("NAT5 cycle length outside declared toy values")


NAT5_PARAMETER_SETS = {
    "nat5-F24": NAT5Parameters("nat5-F24", 24, 240, 4),
    "nat5-F30": NAT5Parameters("nat5-F30", 30, 300, 6),
    "nat5-F36": NAT5Parameters("nat5-F36", 36, 360, 6),
}


@dataclass(frozen=True, slots=True)
class NAT5Public:
    name: str
    target: SimplicialComplex
    observed_edge_labels: tuple[Permutation5, ...]
    public_cycle_length: int


@dataclass(frozen=True, slots=True)
class NAT5Reference:
    hidden_clean_labels_normalized: tuple[Permutation5, ...]
    planted_cycle: tuple[int, ...]
    planted_noise_value: Permutation5
    rejected_flip_proposals: int


@dataclass(frozen=True, slots=True)
class NAT5Recovery:
    vertices: int
    edges: int
    triangles: int
    cycle_length: int
    enumerated_cycles: int
    nonidentity_face_holonomies: int
    curvature_hitting_cycles: int
    cycle_value_pairs_tested: int
    consistent_pairs: int
    accepted_witnesses: int
    accepted_cap_hit: bool
    first_accepted: bool
    first_cycle_matches_planted_after_public_success: bool | None
    first_noise_matches_planted_after_public_success: bool | None
    first_state_matches_planted_after_public_success: bool | None


def _nat3_carrier_params(params: NAT5Parameters) -> NAT3Parameters:
    return NAT3Parameters(
        params.name + "-carrier",
        params.triangle_count,
        params.successful_flips,
        (1,),
    )


def _adjacency(target: SimplicialComplex) -> dict[int, tuple[int, ...]]:
    values: dict[int, set[int]] = {vertex: set() for vertex in target.vertices}
    for left, right in _edges(target):
        values[left].add(right)
        values[right].add(left)
    return {vertex: tuple(sorted(neighbors)) for vertex, neighbors in values.items()}


def _canonical_cycle(cycle: tuple[int, ...]) -> tuple[int, ...]:
    values = list(cycle)
    rotations: list[tuple[int, ...]] = []
    for sequence in (values, list(reversed(values))):
        for offset in range(len(sequence)):
            rotations.append(tuple(sequence[offset:] + sequence[:offset]))
    return min(rotations)


def _simple_cycles(
    target: SimplicialComplex,
    length: int,
    *,
    cap: int = 200_000,
) -> tuple[tuple[int, ...], ...]:
    adjacency = _adjacency(target)
    found: set[tuple[int, ...]] = set()

    for start in sorted(target.vertices):
        path = [start]
        visited = {start}

        def dfs(current: int) -> None:
            if len(path) == length:
                if start in adjacency[current]:
                    found.add(_canonical_cycle(tuple(path)))
                    if len(found) > cap:
                        raise NAT5Error("NAT5 simple-cycle enumeration cap exceeded")
                return
            for neighbor in adjacency[current]:
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                path.append(neighbor)
                dfs(neighbor)
                path.pop()
                visited.remove(neighbor)

        dfs(start)
    if not found:
        raise NAT5Error("NAT5 carrier has no simple cycle of declared length")
    return tuple(sorted(found))


def _select_cycle(
    cycles: tuple[tuple[int, ...], ...],
    params: NAT5Parameters,
    seed: bytes,
) -> tuple[int, ...]:
    return min(
        cycles,
        key=lambda cycle: (
            hashlib.sha256(
                b"MORPH-KEM NAT5 planted cycle v1\x00"
                + seed
                + params.name.encode("ascii")
                + b"\x00"
                + b"".join(vertex.to_bytes(4, "big") for vertex in cycle)
            ).digest(),
            cycle,
        ),
    )


def _noise_value(params: NAT5Parameters, seed: bytes) -> Permutation5:
    digest = _digest(b"MORPH-KEM NAT5 cycle value v1", seed, params.name)
    return _THREE_CYCLES[int.from_bytes(digest[:8], "big") % len(_THREE_CYCLES)]


def _cycle_edge_positions(cycle: tuple[int, ...]) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        (cycle[index], cycle[(index + 1) % len(cycle)], index)
        for index in range(len(cycle))
    )


def _apply_cycle_noise(
    target: SimplicialComplex,
    clean_public_labels: tuple[Permutation5, ...],
    cycle: tuple[int, ...],
    noise_value: Permutation5,
) -> tuple[Permutation5, ...]:
    edges = _edges(target)
    edge_index = {edge: index for index, edge in enumerate(edges)}
    observed = list(clean_public_labels)
    noise_inverse = inverse(noise_value)

    for left, right, position in _cycle_edge_positions(cycle):
        public_edge = (min(left, right), max(left, right))
        index = edge_index.get(public_edge)
        if index is None:
            raise NAT5Error("NAT5 cycle uses a non-edge")
        public_clean = clean_public_labels[index]
        traversal_clean = public_clean if left < right else inverse(public_clean)
        traversal_noise = noise_value if position % 2 == 0 else noise_inverse
        traversal_observed = compose(traversal_clean, traversal_noise)
        observed[index] = traversal_observed if left < right else inverse(traversal_observed)
    return tuple(observed)


def _remove_cycle_noise(
    target: SimplicialComplex,
    observed_public_labels: tuple[Permutation5, ...],
    cycle: tuple[int, ...],
    noise_value: Permutation5,
) -> tuple[Permutation5, ...]:
    edges = _edges(target)
    edge_index = {edge: index for index, edge in enumerate(edges)}
    clean = list(observed_public_labels)
    noise_inverse = inverse(noise_value)

    for left, right, position in _cycle_edge_positions(cycle):
        public_edge = (min(left, right), max(left, right))
        index = edge_index.get(public_edge)
        if index is None:
            raise NAT5Error("NAT5 candidate cycle uses a non-edge")
        public_observed = observed_public_labels[index]
        traversal_observed = public_observed if left < right else inverse(public_observed)
        traversal_noise = noise_value if position % 2 == 0 else noise_inverse
        traversal_clean = compose(traversal_observed, inverse(traversal_noise))
        clean[index] = traversal_clean if left < right else inverse(traversal_clean)
    return tuple(clean)


def _integrate_clean_labels(
    target: SimplicialComplex,
    labels: tuple[Permutation5, ...],
) -> tuple[tuple[Permutation5, ...], bool]:
    edges = _edges(target)
    adjacency: dict[int, list[tuple[int, int, bool]]] = {
        vertex: [] for vertex in target.vertices
    }
    for index, (left, right) in enumerate(edges):
        adjacency[left].append((right, index, True))
        adjacency[right].append((left, index, False))
    for values in adjacency.values():
        values.sort()

    state: list[Permutation5 | None] = [None] * len(target.vertices)
    state[0] = _IDENTITY
    queue = [0]
    consistent = True
    while queue and consistent:
        current = queue.pop(0)
        current_value = state[current]
        if current_value is None:
            raise NAT5Error("NAT5 integration lost assigned state")
        for neighbor, edge_index, forward in adjacency[current]:
            edge_value = labels[edge_index]
            candidate = (
                compose(current_value, edge_value)
                if forward
                else compose(current_value, inverse(edge_value))
            )
            if state[neighbor] is None:
                state[neighbor] = candidate
                queue.append(neighbor)
            elif state[neighbor] != candidate:
                consistent = False
                break
    if any(value is None for value in state):
        consistent = False
    concrete = tuple(_IDENTITY if value is None else value for value in state)
    return concrete, consistent


def generate_nat5_instance(
    params: NAT5Parameters,
    master_seed: bytes,
) -> tuple[NAT5Public, NAT5Reference]:
    params.validate()
    if len(master_seed) < 16:
        raise NAT5Error("NAT5 master seed must contain at least 128 bits")

    target, rejected = _carrier(_nat3_carrier_params(params), master_seed)
    cycles = _simple_cycles(target, params.cycle_length)
    cycle = _select_cycle(cycles, params, master_seed)
    noise_value = _noise_value(params, master_seed)
    hidden = _normalized_hidden_labels(target, master_seed, params.name)
    clean = _clean_edge_labels(target, hidden)
    observed = _apply_cycle_noise(target, clean, cycle, noise_value)
    public = NAT5Public(params.name, target, observed, params.cycle_length)
    reference = NAT5Reference(hidden, cycle, noise_value, rejected)
    return public, reference


def validate_nat5_witness(
    public: NAT5Public,
    clean_state: tuple[Permutation5, ...],
    cycle: tuple[int, ...],
    noise_value: Permutation5,
) -> bool:
    if len(clean_state) != len(public.target.vertices):
        return False
    if clean_state[0] != _IDENTITY or any(value not in _A5 for value in clean_state):
        return False
    if len(cycle) != public.public_cycle_length or len(set(cycle)) != len(cycle):
        return False
    if any(vertex not in public.target.vertices for vertex in cycle):
        return False
    if not is_three_cycle(noise_value):
        return False
    edge_set = set(_edges(public.target))
    if any(
        (min(left, right), max(left, right)) not in edge_set
        for left, right, _ in _cycle_edge_positions(cycle)
    ):
        return False
    clean = _clean_edge_labels(public.target, clean_state)
    try:
        reconstructed = _apply_cycle_noise(public.target, clean, cycle, noise_value)
    except NAT5Error:
        return False
    return reconstructed == public.observed_edge_labels


def _defect_face_edge_sets(public: NAT5Public) -> tuple[set[tuple[int, int]], ...]:
    holonomy_public = type(
        "CurvaturePublic",
        (),
        {"target": public.target, "observed_edge_labels": public.observed_edge_labels},
    )()
    holonomies = _face_holonomies(holonomy_public)
    faces = tuple(sorted(simplex for simplex in public.target.simplices if len(simplex) == 3))
    defects: list[set[tuple[int, int]]] = []
    for face, holonomy in zip(faces, holonomies):
        if holonomy == _IDENTITY:
            continue
        a, b, c = face
        defects.append({(min(a, b), max(a, b)), (min(b, c), max(b, c)), (min(a, c), max(a, c))})
    return tuple(defects)


def recover_nat5(
    public: NAT5Public,
    *,
    reference: NAT5Reference | None = None,
    accepted_cap: int = 64,
) -> NAT5Recovery:
    cycles = _simple_cycles(public.target, public.public_cycle_length)
    defect_faces = _defect_face_edge_sets(public)

    hitting: list[tuple[int, ...]] = []
    for cycle in cycles:
        support = {
            (min(left, right), max(left, right))
            for left, right, _ in _cycle_edge_positions(cycle)
        }
        if all(support & defect for defect in defect_faces):
            hitting.append(cycle)

    tested = 0
    consistent_pairs = 0
    accepted: list[tuple[tuple[Permutation5, ...], tuple[int, ...], Permutation5]] = []
    cap_hit = False
    for cycle in hitting:
        for noise_value in _THREE_CYCLES:
            tested += 1
            candidate_clean = _remove_cycle_noise(
                public.target, public.observed_edge_labels, cycle, noise_value
            )
            state, consistent = _integrate_clean_labels(public.target, candidate_clean)
            if not consistent:
                continue
            consistent_pairs += 1
            if validate_nat5_witness(public, state, cycle, noise_value):
                accepted.append((state, cycle, noise_value))
                if len(accepted) >= accepted_cap:
                    cap_hit = True
                    break
        if cap_hit:
            break

    first = accepted[0] if accepted else None
    cycle_match = noise_match = state_match = None
    if first is not None and reference is not None:
        state, cycle, noise_value = first
        cycle_match = cycle == reference.planted_cycle
        noise_match = noise_value == reference.planted_noise_value
        state_match = state == reference.hidden_clean_labels_normalized

    return NAT5Recovery(
        vertices=len(public.target.vertices),
        edges=len(_edges(public.target)),
        triangles=sum(1 for simplex in public.target.simplices if len(simplex) == 3),
        cycle_length=public.public_cycle_length,
        enumerated_cycles=len(cycles),
        nonidentity_face_holonomies=len(defect_faces),
        curvature_hitting_cycles=len(hitting),
        cycle_value_pairs_tested=tested,
        consistent_pairs=consistent_pairs,
        accepted_witnesses=len(accepted),
        accepted_cap_hit=cap_hit,
        first_accepted=bool(accepted),
        first_cycle_matches_planted_after_public_success=cycle_match,
        first_noise_matches_planted_after_public_success=noise_match,
        first_state_matches_planted_after_public_success=state_match,
    )
