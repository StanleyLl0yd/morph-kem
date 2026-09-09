from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from statistics import mean

from .complex import SimplicialComplex

Permutation = tuple[int, ...]


class PathExperimentError(ValueError):
    """Raised when an M1 branching-path instance or query is invalid."""


@dataclass(frozen=True, slots=True)
class PathParameters:
    name: str
    layers: int
    vertices: int
    min_support_fraction: float = 0.75


PATH_PARAMETER_SETS = {
    "path-12": PathParameters("path-12", layers=12, vertices=20),
    "path-16": PathParameters("path-16", layers=16, vertices=24),
    "path-20": PathParameters("path-20", layers=20, vertices=28),
    "path-24": PathParameters("path-24", layers=24, vertices=32),
}


@dataclass(frozen=True, slots=True)
class PathInstance:
    parameters: PathParameters
    base: SimplicialComplex
    branches: tuple[tuple[Permutation, Permutation], ...]
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise PathExperimentError("unsupported M1 instance version")
        p = self.parameters
        if p.layers <= 0 or p.layers > 32:
            raise PathExperimentError("M1 layers must be in [1, 32]")
        if p.vertices < 8 or p.vertices > 256:
            raise PathExperimentError("M1 vertex count must be in [8, 256]")
        if not 0.0 < p.min_support_fraction <= 1.0:
            raise PathExperimentError("support fraction must be in (0, 1]")
        if len(self.branches) != p.layers:
            raise PathExperimentError("branch count does not match layer count")
        if self.base.vertices != tuple(range(p.vertices)):
            raise PathExperimentError("M1 base must use the complete canonical vertex universe")
        for pair in self.branches:
            if len(pair) != 2:
                raise PathExperimentError("every M1 layer must have two branches")
            for permutation in pair:
                _validate_permutation(permutation, p.vertices)

    def encode(self) -> bytes:
        payload = {
            "base": self.base.encode().hex(),
            "branches": [[list(pair[0]), list(pair[1])] for pair in self.branches],
            "parameters": {
                "layers": self.parameters.layers,
                "min_support_fraction": self.parameters.min_support_fraction,
                "name": self.parameters.name,
                "vertices": self.parameters.vertices,
            },
            "version": self.version,
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


@dataclass(frozen=True, slots=True)
class SupportMetrics:
    branch_min: int
    branch_mean: float
    relative_min: int
    relative_mean: float


@dataclass(frozen=True, slots=True)
class MitmResult:
    preimages: tuple[int, ...]
    split_layer: int
    forward_states: int
    reverse_states: int
    candidate_matches: int


def _validate_permutation(permutation: Permutation, size: int) -> None:
    if len(permutation) != size or set(permutation) != set(range(size)):
        raise PathExperimentError("invalid permutation")


def _inverse(permutation: Permutation) -> Permutation:
    inverse = [0] * len(permutation)
    for source, target in enumerate(permutation):
        inverse[target] = source
    return tuple(inverse)


def _compose(after: Permutation, before: Permutation) -> Permutation:
    if len(after) != len(before):
        raise PathExperimentError("permutation size mismatch")
    return tuple(after[before[i]] for i in range(len(before)))


def _support(permutation: Permutation) -> int:
    return sum(i != target for i, target in enumerate(permutation))


class _DeterministicRng:
    def __init__(self, seed: bytes):
        self.seed = seed
        self.counter = 0

    def block(self) -> bytes:
        out = hashlib.sha256(
            b"MORPH-KEM M1 path rng v1\x00"
            + self.seed
            + self.counter.to_bytes(8, "big")
        ).digest()
        self.counter += 1
        return out

    def randbelow(self, upper: int) -> int:
        if upper <= 0:
            raise ValueError("upper must be positive")
        limit = (1 << 256) - ((1 << 256) % upper)
        while True:
            x = int.from_bytes(self.block(), "big")
            if x < limit:
                return x % upper


def _permutation(size: int, seed: bytes) -> Permutation:
    values = list(range(size))
    rng = _DeterministicRng(seed)
    for i in range(size - 1, 0, -1):
        j = rng.randbelow(i + 1)
        values[i], values[j] = values[j], values[i]
    return tuple(values)


def _scaffold(vertices: int) -> SimplicialComplex:
    """Create a connected 2D scaffold over every vertex."""
    facets: list[tuple[int, ...]] = []
    for i in range(vertices - 1):
        facets.append((i, i + 1))
    for i in range(vertices - 2):
        facets.append((i, i + 1, i + 2))
    for i in range(2, vertices - 1, 2):
        facets.append((0, i, i + 1))
    return SimplicialComplex.from_facets(facets)


def generate_path_instance(parameters: PathParameters, master_seed: bytes) -> PathInstance:
    if not isinstance(master_seed, bytes) or not master_seed:
        raise PathExperimentError("master_seed must be non-empty bytes")

    minimum_support = math.ceil(parameters.vertices * parameters.min_support_fraction)
    branches: list[tuple[Permutation, Permutation]] = []

    for layer in range(parameters.layers):
        accepted: list[Permutation] = []
        attempt = 0
        while len(accepted) < 2:
            material = hashlib.sha256(
                b"MORPH-KEM M1 branch v1\x00"
                + parameters.name.encode("ascii")
                + b"\x00"
                + master_seed
                + layer.to_bytes(2, "big")
                + len(accepted).to_bytes(1, "big")
                + attempt.to_bytes(4, "big")
            ).digest()
            candidate = _permutation(parameters.vertices, material)
            attempt += 1
            if _support(candidate) < minimum_support:
                continue
            if accepted:
                relative = _compose(candidate, _inverse(accepted[0]))
                if _support(relative) < minimum_support:
                    continue
                if candidate == accepted[0]:
                    continue
            accepted.append(candidate)
        branches.append((accepted[0], accepted[1]))

    return PathInstance(parameters, _scaffold(parameters.vertices), tuple(branches))


def path_forward(instance: PathInstance, seed: int) -> SimplicialComplex:
    if not isinstance(seed, int) or isinstance(seed, bool):
        raise PathExperimentError("seed must be an integer")
    if seed < 0 or seed >= (1 << instance.parameters.layers):
        raise PathExperimentError("seed outside M1 path range")

    state = instance.base
    for layer, pair in enumerate(instance.branches):
        bit = (seed >> layer) & 1
        state = state.relabel(pair[bit])
    return state


def path_accept(instance: PathInstance, seed: int, target: SimplicialComplex) -> bool:
    try:
        return path_forward(instance, seed) == target
    except PathExperimentError:
        return False


def support_metrics(instance: PathInstance) -> SupportMetrics:
    branch_supports: list[int] = []
    relative_supports: list[int] = []
    for left, right in instance.branches:
        branch_supports.extend((_support(left), _support(right)))
        relative_supports.append(_support(_compose(right, _inverse(left))))
    return SupportMetrics(
        branch_min=min(branch_supports),
        branch_mean=mean(branch_supports),
        relative_min=min(relative_supports),
        relative_mean=mean(relative_supports),
    )


def exhaustive_path_recover(instance: PathInstance, target: SimplicialComplex) -> tuple[int, ...]:
    return tuple(
        seed
        for seed in range(1 << instance.parameters.layers)
        if path_accept(instance, seed, target)
    )


def mitm_path_recover(
    instance: PathInstance,
    target: SimplicialComplex,
    split_layer: int | None = None,
) -> MitmResult:
    layers = instance.parameters.layers
    split = layers // 2 if split_layer is None else split_layer
    if split < 0 or split > layers:
        raise PathExperimentError("split layer outside valid range")

    forward_table: dict[bytes, list[int]] = {}
    for prefix in range(1 << split):
        state = instance.base
        for layer in range(split):
            bit = (prefix >> layer) & 1
            state = state.relabel(instance.branches[layer][bit])
        forward_table.setdefault(state.encode(), []).append(prefix)

    suffix_layers = layers - split
    recovered: set[int] = set()
    candidate_matches = 0
    for suffix in range(1 << suffix_layers):
        state = target
        for layer in range(layers - 1, split - 1, -1):
            bit = (suffix >> (layer - split)) & 1
            state = state.relabel(_inverse(instance.branches[layer][bit]))
        prefixes = forward_table.get(state.encode(), ())
        candidate_matches += len(prefixes)
        for prefix in prefixes:
            seed = prefix | (suffix << split)
            if path_accept(instance, seed, target):
                recovered.add(seed)

    return MitmResult(
        preimages=tuple(sorted(recovered)),
        split_layer=split,
        forward_states=1 << split,
        reverse_states=1 << suffix_layers,
        candidate_matches=candidate_matches,
    )
