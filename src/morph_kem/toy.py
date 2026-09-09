from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Iterable

from .complex import Simplex, SimplicialComplex

_TOY_VERSION = 1


class ToyRelationError(ValueError):
    """Raised when a toy relation input is invalid or inconsistent."""


class NoPreimageError(ToyRelationError):
    pass


class AmbiguousPreimageError(ToyRelationError):
    pass


@dataclass(frozen=True, slots=True)
class ToyParameters:
    name: str
    seed_bits: int


TOY_PARAMETER_SETS = {
    "toy-8": ToyParameters("toy-8", 8),
    "toy-12": ToyParameters("toy-12", 12),
    "toy-16": ToyParameters("toy-16", 16),
    "toy-24": ToyParameters("toy-24", 24),
    "toy-32": ToyParameters("toy-32", 32),
}


@dataclass(frozen=True, slots=True)
class ToyPublicKey:
    seed_bits: int
    base: SimplicialComplex
    choices: tuple[tuple[Simplex, Simplex], ...]
    version: int = _TOY_VERSION

    def __post_init__(self) -> None:
        if self.version != _TOY_VERSION:
            raise ToyRelationError("unsupported toy public-key version")
        if self.seed_bits <= 0 or self.seed_bits > 32:
            raise ToyRelationError("toy seed size must be in [1, 32]")
        if len(self.choices) != self.seed_bits:
            raise ToyRelationError("choice count does not match seed size")
        for pair in self.choices:
            if len(pair) != 2:
                raise ToyRelationError("each coordinate must have two choices")
            for simplex in pair:
                if len(simplex) != 3:
                    raise ToyRelationError("toy choices must be triangles")

    def encode(self) -> bytes:
        payload = {
            "base": self.base.encode().hex(),
            "choices": [[list(pair[0]), list(pair[1])] for pair in self.choices],
            "seed_bits": self.seed_bits,
            "version": self.version,
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")

    @property
    def fingerprint(self) -> bytes:
        return hashlib.sha256(b"MORPH-KEM toy pk fingerprint v1\x00" + self.encode()).digest()


@dataclass(frozen=True, slots=True)
class ToySecretKey:
    seed_bits: int
    permutation: tuple[int, ...]
    public_key_fingerprint: bytes
    version: int = _TOY_VERSION

    def __post_init__(self) -> None:
        if self.version != _TOY_VERSION:
            raise ToyRelationError("unsupported toy secret-key version")
        expected_vertices = self.seed_bits * 5
        if len(self.permutation) != expected_vertices:
            raise ToyRelationError("permutation length does not match parameters")
        if set(self.permutation) != set(range(expected_vertices)):
            raise ToyRelationError("secret permutation is not a bijection")
        if len(self.public_key_fingerprint) != 32:
            raise ToyRelationError("public-key fingerprint must be 32 bytes")

    def encode(self) -> bytes:
        payload = {
            "permutation": list(self.permutation),
            "public_key_fingerprint": self.public_key_fingerprint.hex(),
            "seed_bits": self.seed_bits,
            "version": self.version,
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


class _DeterministicRng:
    def __init__(self, seed: bytes):
        self._seed = seed
        self._counter = 0

    def _block(self) -> bytes:
        block = hashlib.sha256(
            b"MORPH-KEM toy deterministic rng v1\x00"
            + self._seed
            + self._counter.to_bytes(8, "big")
        ).digest()
        self._counter += 1
        return block

    def randbelow(self, upper: int) -> int:
        if upper <= 0:
            raise ValueError("upper bound must be positive")
        limit = (1 << 256) - ((1 << 256) % upper)
        while True:
            candidate = int.from_bytes(self._block(), "big")
            if candidate < limit:
                return candidate % upper


def _deterministic_permutation(size: int, seed: bytes) -> tuple[int, ...]:
    values = list(range(size))
    rng = _DeterministicRng(seed)
    for i in range(size - 1, 0, -1):
        j = rng.randbelow(i + 1)
        values[i], values[j] = values[j], values[i]
    return tuple(values)


def _hidden_coordinate(index: int) -> tuple[int, tuple[tuple[int, int], tuple[int, int]], tuple[Simplex, Simplex]]:
    anchor = index * 5
    u0, v0, u1, v1 = anchor + 1, anchor + 2, anchor + 3, anchor + 4
    free_edges = ((u0, v0), (u1, v1))
    triangles = ((anchor, u0, v0), (anchor, u1, v1))
    return anchor, free_edges, triangles


def _hidden_base(seed_bits: int) -> SimplicialComplex:
    facets: list[tuple[int, int]] = []
    for index in range(seed_bits):
        anchor, _, triangles = _hidden_coordinate(index)
        for triangle in triangles:
            _, u, v = triangle
            facets.append((anchor, u))
            facets.append((anchor, v))
    return SimplicialComplex.from_facets(facets)


def _relabel_simplex(simplex: Iterable[int], mapping: tuple[int, ...]) -> Simplex:
    return tuple(sorted(mapping[v] for v in simplex))


def keygen(parameters: ToyParameters, master_seed: bytes) -> tuple[ToyPublicKey, ToySecretKey]:
    if not isinstance(master_seed, bytes) or len(master_seed) == 0:
        raise ToyRelationError("master_seed must be non-empty bytes")
    if parameters.seed_bits <= 0 or parameters.seed_bits > 32:
        raise ToyRelationError("toy seed size must be in [1, 32]")

    vertex_count = parameters.seed_bits * 5
    seed_material = hashlib.sha256(
        b"MORPH-KEM toy keygen v1\x00"
        + parameters.name.encode("ascii")
        + b"\x00"
        + parameters.seed_bits.to_bytes(2, "big")
        + master_seed
    ).digest()
    permutation = _deterministic_permutation(vertex_count, seed_material)

    hidden_base = _hidden_base(parameters.seed_bits)
    public_base = hidden_base.relabel(permutation)

    choices: list[tuple[Simplex, Simplex]] = []
    for index in range(parameters.seed_bits):
        _, _, triangles = _hidden_coordinate(index)
        choices.append(
            (
                _relabel_simplex(triangles[0], permutation),
                _relabel_simplex(triangles[1], permutation),
            )
        )

    public_key = ToyPublicKey(parameters.seed_bits, public_base, tuple(choices))
    secret_key = ToySecretKey(parameters.seed_bits, permutation, public_key.fingerprint)
    return public_key, secret_key


def forward(public_key: ToyPublicKey, seed: int) -> SimplicialComplex:
    if not isinstance(seed, int) or isinstance(seed, bool):
        raise ToyRelationError("seed must be an integer")
    if seed < 0 or seed >= (1 << public_key.seed_bits):
        raise ToyRelationError("seed is outside the parameter range")

    selected: list[Simplex] = []
    for index, pair in enumerate(public_key.choices):
        bit = (seed >> index) & 1
        selected.append(pair[bit])
    return public_key.base.add_facets(selected)


def accept(public_key: ToyPublicKey, seed: int, ciphertext: SimplicialComplex) -> bool:
    try:
        return forward(public_key, seed) == ciphertext
    except ToyRelationError:
        return False


def invert_with_trapdoor(
    public_key: ToyPublicKey,
    secret_key: ToySecretKey,
    ciphertext: SimplicialComplex,
) -> int:
    if public_key.seed_bits != secret_key.seed_bits:
        raise ToyRelationError("public/secret parameter mismatch")
    if public_key.fingerprint != secret_key.public_key_fingerprint:
        raise ToyRelationError("secret key is bound to a different public key")

    inverse = {public: hidden for hidden, public in enumerate(secret_key.permutation)}
    try:
        hidden_ciphertext = ciphertext.relabel(inverse)
    except KeyError as exc:
        raise NoPreimageError("ciphertext contains a vertex outside this key") from exc

    recovered = 0
    selected_pairs: list[tuple[Simplex, Simplex]] = []
    for index in range(public_key.seed_bits):
        _, free_edges, triangles = _hidden_coordinate(index)
        present = [hidden_ciphertext.contains(triangle) for triangle in triangles]
        if present == [True, False]:
            bit = 0
        elif present == [False, True]:
            bit = 1
            recovered |= 1 << index
        else:
            raise NoPreimageError("coordinate does not contain exactly one selected triangle")
        selected_pairs.append((free_edges[bit], triangles[bit]))

    reduced = hidden_ciphertext
    for free_face, coface in selected_pairs:
        try:
            reduced = reduced.collapse(free_face, coface)
        except ValueError as exc:
            raise NoPreimageError("trapdoor reduction certificate is invalid for ciphertext") from exc

    if reduced != _hidden_base(public_key.seed_bits):
        raise NoPreimageError("ciphertext does not reduce to the canonical hidden base")
    if not accept(public_key, recovered, ciphertext):
        raise NoPreimageError("recovered seed fails exact re-encapsulation")
    return recovered


def direct_public_recover(public_key: ToyPublicKey, ciphertext: SimplicialComplex) -> int:
    recovered = 0
    for index, pair in enumerate(public_key.choices):
        present = [ciphertext.contains(pair[0]), ciphertext.contains(pair[1])]
        if present == [True, False]:
            bit = 0
        elif present == [False, True]:
            bit = 1
            recovered |= 1 << index
        else:
            raise NoPreimageError("ciphertext is not a valid M0 coordinate encoding")
    if not accept(public_key, recovered, ciphertext):
        raise NoPreimageError("publicly recovered seed fails exact acceptance")
    return recovered


def exhaustive_recover(public_key: ToyPublicKey, ciphertext: SimplicialComplex) -> int:
    match: int | None = None
    for candidate in range(1 << public_key.seed_bits):
        if accept(public_key, candidate, ciphertext):
            if match is not None:
                raise AmbiguousPreimageError("ciphertext has multiple accepted seeds")
            match = candidate
    if match is None:
        raise NoPreimageError("ciphertext has no accepted seed")
    return match
