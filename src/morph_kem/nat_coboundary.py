from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import hashlib
from itertools import combinations

from .complex import SimplicialComplex
from .surface import SurfaceParameters, generate_surface_instance


class NATError(ValueError):
    """Raised when a NAT toy-control input is invalid."""


@dataclass(frozen=True, slots=True)
class NATParameters:
    name: str
    rows: int
    cols: int
    repeated_samples: int
    repeated_noise_weight: int

    def validate(self) -> None:
        if self.rows < 3 or self.rows > 16 or self.cols < 3 or self.cols > 16:
            raise NATError("NAT0 torus dimensions outside toy bounds")
        if self.repeated_samples < 3 or self.repeated_samples > 15:
            raise NATError("NAT0 repeated sample count outside toy bounds")
        if self.repeated_samples % 2 == 0:
            raise NATError("NAT0 repeated sample count must be odd")
        if self.repeated_noise_weight < 1:
            raise NATError("NAT0 repeated noise weight must be positive")


NAT0_PARAMETER_SETS = {
    "nat0-4x4": NATParameters("nat0-4x4", 4, 4, 7, 2),
    "nat0-6x6": NATParameters("nat0-6x6", 6, 6, 7, 3),
    "nat0-8x8": NATParameters("nat0-8x8", 8, 8, 7, 4),
}


@dataclass(frozen=True, slots=True)
class NATSinglePublic:
    name: str
    target: SimplicialComplex
    observed_edge_mask: int


@dataclass(frozen=True, slots=True)
class NATSingleReference:
    hidden_vertex_mask: int
    noise_edge_index: int


@dataclass(frozen=True, slots=True)
class NATSingleRecovery:
    violated_triangles: tuple[int, ...]
    recovered_noise_edge: int
    recovered_clean_edge_mask: int
    recovered_vertex_mask_normalized: int
    accepted: bool
    matches_reference_after_public_success: bool | None


@dataclass(frozen=True, slots=True)
class NATRepeatedPublic:
    name: str
    target: SimplicialComplex
    observed_edge_masks: tuple[int, ...]
    public_noise_weight: int


@dataclass(frozen=True, slots=True)
class NATRepeatedReference:
    hidden_vertex_mask: int


@dataclass(frozen=True, slots=True)
class NATRepeatedRecovery:
    recovered_clean_edge_mask: int
    recovered_vertex_mask_normalized: int
    sample_distances: tuple[int, ...]
    majority_edge_votes: int
    accepted: bool
    matches_reference_after_public_success: bool | None


def _digest(domain: bytes, seed: bytes, name: str, counter: int = 0) -> bytes:
    return hashlib.sha256(
        domain + b"\x00" + seed + name.encode("ascii") + counter.to_bytes(8, "big")
    ).digest()


def _seeded_order(size: int, domain: bytes, seed: bytes, name: str) -> tuple[int, ...]:
    return tuple(
        sorted(
            range(size),
            key=lambda index: (_digest(domain, seed, name, index), index),
        )
    )


def _edges(target: SimplicialComplex) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(simplex for simplex in target.simplices if len(simplex) == 2))


def _triangles(target: SimplicialComplex) -> tuple[tuple[int, int, int], ...]:
    return tuple(sorted(simplex for simplex in target.simplices if len(simplex) == 3))


def _clean_edge_mask(target: SimplicialComplex, vertex_mask: int) -> int:
    result = 0
    for edge_index, (left, right) in enumerate(_edges(target)):
        left_bit = (vertex_mask >> left) & 1
        right_bit = (vertex_mask >> right) & 1
        if left_bit ^ right_bit:
            result |= 1 << edge_index
    return result


def _normalize_vertex_mask(target: SimplicialComplex, vertex_mask: int) -> int:
    vertices = target.vertices
    if not vertices:
        raise NATError("NAT0 public complex has no vertices")
    root = min(vertices)
    if ((vertex_mask >> root) & 1) == 0:
        return vertex_mask
    all_vertices = sum(1 << vertex for vertex in vertices)
    return vertex_mask ^ all_vertices


def _recover_vertex_mask_from_clean(target: SimplicialComplex, clean_mask: int) -> int:
    edges = _edges(target)
    adjacency: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for edge_index, (left, right) in enumerate(edges):
        value = (clean_mask >> edge_index) & 1
        adjacency[left].append((right, value))
        adjacency[right].append((left, value))
    for neighbors in adjacency.values():
        neighbors.sort()

    root = min(target.vertices)
    values: dict[int, int] = {root: 0}
    queue = [root]
    while queue:
        current = queue.pop(0)
        for neighbor, edge_value in adjacency[current]:
            expected = values[current] ^ edge_value
            if neighbor not in values:
                values[neighbor] = expected
                queue.append(neighbor)
            elif values[neighbor] != expected:
                raise NATError("NAT0 recovered clean edge data is not a public coboundary")
    if len(values) != len(target.vertices):
        raise NATError("NAT0 public primal graph is disconnected")
    return sum(bit << vertex for vertex, bit in values.items())


def _triangle_boundary_edge_indices(target: SimplicialComplex) -> tuple[tuple[int, int, int], ...]:
    edges = _edges(target)
    index = {edge: edge_index for edge_index, edge in enumerate(edges)}
    boundaries: list[tuple[int, int, int]] = []
    for triangle in _triangles(target):
        boundary = tuple(
            sorted(
                index[tuple(sorted(edge))]
                for edge in combinations(triangle, 2)
            )
        )
        boundaries.append(boundary)
    return tuple(boundaries)


def _violated_triangles(target: SimplicialComplex, observed_mask: int) -> tuple[int, ...]:
    violated = []
    for triangle_index, boundary in enumerate(_triangle_boundary_edge_indices(target)):
        parity = sum((observed_mask >> edge_index) & 1 for edge_index in boundary) & 1
        if parity:
            violated.append(triangle_index)
    return tuple(violated)


def _edge_triangle_owners(target: SimplicialComplex) -> tuple[tuple[int, ...], ...]:
    edge_count = len(_edges(target))
    owners: list[list[int]] = [[] for _ in range(edge_count)]
    for triangle_index, boundary in enumerate(_triangle_boundary_edge_indices(target)):
        for edge_index in boundary:
            owners[edge_index].append(triangle_index)
    result = tuple(tuple(sorted(value)) for value in owners)
    if any(len(value) != 2 for value in result):
        raise NATError("NAT0 public surface is not closed at an edge")
    return result


def _hidden_vertex_mask(target: SimplicialComplex, seed: bytes, name: str) -> int:
    mask = 0
    for vertex in target.vertices:
        bit = _digest(
            b"MORPH-KEM NAT0 hidden vertex bit v1", seed, name, vertex
        )[0] & 1
        mask |= bit << vertex
    return mask


def _surface(params: NATParameters, seed: bytes) -> SimplicialComplex:
    surface_seed = hashlib.sha256(
        b"MORPH-KEM NAT0 surface v1\x00" + seed + params.name.encode("ascii")
    ).digest()
    public, _ = generate_surface_instance(
        SurfaceParameters(params.name + "-surface", params.rows, params.cols),
        surface_seed,
    )
    return public.target


def generate_nat0_single_instance(
    params: NATParameters,
    master_seed: bytes,
) -> tuple[NATSinglePublic, NATSingleReference]:
    params.validate()
    if len(master_seed) < 16:
        raise NATError("NAT0 master seed must contain at least 128 bits")
    target = _surface(params, master_seed)
    hidden = _hidden_vertex_mask(target, master_seed, params.name)
    clean = _clean_edge_mask(target, hidden)
    edges = _edges(target)
    noise_edge = int.from_bytes(
        _digest(b"MORPH-KEM NAT0 single noise edge v1", master_seed, params.name)[:8],
        "big",
    ) % len(edges)
    observed = clean ^ (1 << noise_edge)
    return (
        NATSinglePublic(params.name, target, observed),
        NATSingleReference(hidden_vertex_mask=hidden, noise_edge_index=noise_edge),
    )


def recover_nat0_single(
    public: NATSinglePublic,
    *,
    reference: NATSingleReference | None = None,
) -> NATSingleRecovery:
    violated = _violated_triangles(public.target, public.observed_edge_mask)
    if len(violated) != 2:
        raise NATError("NAT0 one-edge control did not produce exactly two violated triangles")
    target_pair = tuple(sorted(violated))
    matches = [
        edge_index
        for edge_index, owners in enumerate(_edge_triangle_owners(public.target))
        if owners == target_pair
    ]
    if len(matches) != 1:
        raise NATError("NAT0 violated-triangle pair does not identify one public edge")
    recovered_noise = matches[0]
    clean = public.observed_edge_mask ^ (1 << recovered_noise)
    vertex_mask = _recover_vertex_mask_from_clean(public.target, clean)
    accepted = (
        _clean_edge_mask(public.target, vertex_mask) == clean
        and (public.observed_edge_mask ^ clean).bit_count() == 1
    )
    reference_match = None
    if reference is not None:
        reference_match = (
            recovered_noise == reference.noise_edge_index
            and vertex_mask
            == _normalize_vertex_mask(public.target, reference.hidden_vertex_mask)
        )
    return NATSingleRecovery(
        violated_triangles=violated,
        recovered_noise_edge=recovered_noise,
        recovered_clean_edge_mask=clean,
        recovered_vertex_mask_normalized=vertex_mask,
        accepted=accepted,
        matches_reference_after_public_success=reference_match,
    )


def generate_nat0_repeated_instance(
    params: NATParameters,
    master_seed: bytes,
) -> tuple[NATRepeatedPublic, NATRepeatedReference]:
    params.validate()
    if len(master_seed) < 16:
        raise NATError("NAT0 master seed must contain at least 128 bits")
    target = _surface(params, master_seed)
    hidden = _hidden_vertex_mask(target, master_seed, params.name)
    clean = _clean_edge_mask(target, hidden)
    edge_count = len(_edges(target))
    required = params.repeated_samples * params.repeated_noise_weight
    if required > edge_count:
        raise NATError("NAT0 repeated control needs more distinct noisy edges than public edges")
    order = _seeded_order(
        edge_count,
        b"MORPH-KEM NAT0 repeated noise order v1",
        master_seed,
        params.name,
    )
    observed: list[int] = []
    for sample_index in range(params.repeated_samples):
        start = sample_index * params.repeated_noise_weight
        noisy_edges = order[start : start + params.repeated_noise_weight]
        noise_mask = sum(1 << edge_index for edge_index in noisy_edges)
        observed.append(clean ^ noise_mask)
    return (
        NATRepeatedPublic(
            name=params.name,
            target=target,
            observed_edge_masks=tuple(observed),
            public_noise_weight=params.repeated_noise_weight,
        ),
        NATRepeatedReference(hidden_vertex_mask=hidden),
    )


def recover_nat0_repeated(
    public: NATRepeatedPublic,
    *,
    reference: NATRepeatedReference | None = None,
) -> NATRepeatedRecovery:
    sample_count = len(public.observed_edge_masks)
    if sample_count < 3 or sample_count % 2 == 0:
        raise NATError("NAT0 majority control requires an odd sample count >= 3")
    edge_count = len(_edges(public.target))
    recovered = 0
    majority_votes = 0
    for edge_index in range(edge_count):
        ones = sum((sample >> edge_index) & 1 for sample in public.observed_edge_masks)
        majority_votes += sample_count
        if ones > sample_count // 2:
            recovered |= 1 << edge_index
    vertex_mask = _recover_vertex_mask_from_clean(public.target, recovered)
    distances = tuple(
        (sample ^ recovered).bit_count() for sample in public.observed_edge_masks
    )
    accepted = (
        _clean_edge_mask(public.target, vertex_mask) == recovered
        and all(distance == public.public_noise_weight for distance in distances)
    )
    reference_match = None
    if reference is not None:
        reference_match = (
            vertex_mask
            == _normalize_vertex_mask(public.target, reference.hidden_vertex_mask)
        )
    return NATRepeatedRecovery(
        recovered_clean_edge_mask=recovered,
        recovered_vertex_mask_normalized=vertex_mask,
        sample_distances=distances,
        majority_edge_votes=majority_votes,
        accepted=accepted,
        matches_reference_after_public_success=reference_match,
    )
