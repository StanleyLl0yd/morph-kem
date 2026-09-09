from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
import struct
from typing import Iterable, Mapping, Sequence

Simplex = tuple[int, ...]

_MAGIC = b"MKSC\x01"
_MAX_SIMPLEX_COUNT = 1_000_000
_MAX_ARITY = 64
_U32_MAX = (1 << 32) - 1


class ComplexEncodingError(ValueError):
    """Raised when a simplicial-complex encoding is malformed or non-canonical."""


def _normalize_simplex(simplex: Iterable[int]) -> Simplex:
    values = tuple(simplex)
    if not values:
        raise ValueError("a simplex must contain at least one vertex")
    if any(not isinstance(v, int) or isinstance(v, bool) for v in values):
        raise TypeError("vertices must be integers")
    if any(v < 0 or v > _U32_MAX for v in values):
        raise ValueError("vertices must fit in an unsigned 32-bit integer")
    normalized = tuple(sorted(values))
    if len(set(normalized)) != len(normalized):
        raise ValueError("a simplex cannot repeat a vertex")
    if len(normalized) > _MAX_ARITY:
        raise ValueError(f"simplex arity exceeds {_MAX_ARITY}")
    return normalized


def _simplex_sort_key(simplex: Simplex) -> tuple[int, Simplex]:
    return (len(simplex), simplex)


def _faces(simplex: Simplex) -> set[Simplex]:
    result: set[Simplex] = set()
    for arity in range(1, len(simplex) + 1):
        result.update(combinations(simplex, arity))
    return result


@dataclass(frozen=True, slots=True)
class SimplicialComplex:
    """Finite simplicial complex with a canonical simplex ordering."""

    simplices: tuple[Simplex, ...]

    def __post_init__(self) -> None:
        previous_key: tuple[int, Simplex] | None = None
        seen: set[Simplex] = set()
        for simplex in self.simplices:
            normalized = _normalize_simplex(simplex)
            if normalized != simplex:
                raise ValueError("simplices must use canonical vertex ordering")
            if simplex in seen:
                raise ValueError("duplicate simplex")
            key = _simplex_sort_key(simplex)
            if previous_key is not None and key <= previous_key:
                raise ValueError("simplices must use canonical complex ordering")
            previous_key = key
            seen.add(simplex)

        for simplex in seen:
            if not _faces(simplex).issubset(seen):
                raise ValueError("simplex set is not downward closed")

    @classmethod
    def from_simplices(cls, simplices: Iterable[Iterable[int]]) -> "SimplicialComplex":
        normalized: list[Simplex] = []
        seen: set[Simplex] = set()
        for simplex in simplices:
            item = _normalize_simplex(simplex)
            if item in seen:
                raise ValueError("duplicate simplex")
            seen.add(item)
            normalized.append(item)
        normalized.sort(key=_simplex_sort_key)
        return cls(tuple(normalized))

    @classmethod
    def from_facets(cls, facets: Iterable[Iterable[int]]) -> "SimplicialComplex":
        closure: set[Simplex] = set()
        at_least_one = False
        for facet in facets:
            at_least_one = True
            closure.update(_faces(_normalize_simplex(facet)))
        if not at_least_one:
            return cls(())
        return cls(tuple(sorted(closure, key=_simplex_sort_key)))

    @property
    def vertices(self) -> tuple[int, ...]:
        return tuple(simplex[0] for simplex in self.simplices if len(simplex) == 1)

    @property
    def dimension(self) -> int:
        if not self.simplices:
            return -1
        return max(len(simplex) - 1 for simplex in self.simplices)

    @property
    def facets(self) -> tuple[Simplex, ...]:
        simplex_set = set(self.simplices)
        facets: list[Simplex] = []
        for simplex in self.simplices:
            simplex_vertices = set(simplex)
            if not any(
                len(other) > len(simplex) and simplex_vertices.issubset(other)
                for other in simplex_set
            ):
                facets.append(simplex)
        return tuple(facets)

    def contains(self, simplex: Iterable[int]) -> bool:
        return _normalize_simplex(simplex) in set(self.simplices)

    def add_facets(self, facets: Iterable[Iterable[int]]) -> "SimplicialComplex":
        closure = set(self.simplices)
        for facet in facets:
            closure.update(_faces(_normalize_simplex(facet)))
        return SimplicialComplex(tuple(sorted(closure, key=_simplex_sort_key)))

    def relabel(self, mapping: Mapping[int, int] | Sequence[int]) -> "SimplicialComplex":
        lookup = mapping.__getitem__
        relabeled = [tuple(sorted(lookup(v) for v in simplex)) for simplex in self.simplices]
        return SimplicialComplex.from_simplices(relabeled)

    def free_collapse_pairs(self) -> tuple[tuple[Simplex, Simplex], ...]:
        """Return all deterministic elementary-collapse pairs (free face, facet)."""
        facets = self.facets
        result: list[tuple[Simplex, Simplex]] = []
        for tau in facets:
            if len(tau) < 2:
                continue
            for sigma in combinations(tau, len(tau) - 1):
                sigma_vertices = set(sigma)
                containing_maximal = [
                    candidate
                    for candidate in facets
                    if sigma_vertices.issubset(candidate)
                ]
                if containing_maximal == [tau]:
                    result.append((sigma, tau))
        result.sort(key=lambda pair: (len(pair[1]), pair[1], pair[0]))
        return tuple(result)

    def elementary_expand(
        self,
        free_face: Iterable[int],
        coface: Iterable[int],
    ) -> "SimplicialComplex":
        """Apply the inverse of one elementary collapse.

        The supplied free_face and coface must both be absent. Every proper
        non-empty face of coface other than free_face must already be present.
        The method then adds exactly those two simplices.
        """
        sigma = _normalize_simplex(free_face)
        tau = _normalize_simplex(coface)
        simplex_set = set(self.simplices)

        if sigma in simplex_set or tau in simplex_set:
            raise ValueError("expansion pair must be absent")
        if len(tau) != len(sigma) + 1 or not set(sigma).issubset(tau):
            raise ValueError("expansion face must be a codimension-one face of coface")

        required = _faces(tau) - {sigma, tau}
        missing = required - simplex_set
        if missing:
            raise ValueError("all other proper faces of coface must already be present")

        expanded = simplex_set | {sigma, tau}
        return SimplicialComplex(tuple(sorted(expanded, key=_simplex_sort_key)))

    def collapse(self, free_face: Iterable[int], coface: Iterable[int]) -> "SimplicialComplex":
        sigma = _normalize_simplex(free_face)
        tau = _normalize_simplex(coface)
        simplex_set = set(self.simplices)

        if sigma not in simplex_set or tau not in simplex_set:
            raise ValueError("collapse pair is not present")
        if len(tau) != len(sigma) + 1 or not set(sigma).issubset(tau):
            raise ValueError("free face must be a codimension-one face of coface")

        containing_maximal = []
        sigma_vertices = set(sigma)
        for candidate in self.facets:
            if sigma_vertices.issubset(candidate):
                containing_maximal.append(candidate)
        if containing_maximal != [tau]:
            raise ValueError("face is not free with the requested unique maximal coface")

        reduced = simplex_set - {sigma, tau}
        return SimplicialComplex(tuple(sorted(reduced, key=_simplex_sort_key)))

    def encode(self) -> bytes:
        if len(self.simplices) > _MAX_SIMPLEX_COUNT:
            raise ValueError("too many simplices")
        out = bytearray(_MAGIC)
        out.extend(struct.pack(">I", len(self.simplices)))
        for simplex in self.simplices:
            out.append(len(simplex))
            for vertex in simplex:
                out.extend(struct.pack(">I", vertex))
        return bytes(out)

    @classmethod
    def decode(cls, data: bytes) -> "SimplicialComplex":
        if not isinstance(data, bytes):
            raise TypeError("encoded complex must be bytes")
        if len(data) < len(_MAGIC) + 4:
            raise ComplexEncodingError("truncated header")
        if not data.startswith(_MAGIC):
            raise ComplexEncodingError("bad magic/version")

        offset = len(_MAGIC)
        count = struct.unpack_from(">I", data, offset)[0]
        offset += 4
        if count > _MAX_SIMPLEX_COUNT:
            raise ComplexEncodingError("simplex count exceeds limit")

        simplices: list[Simplex] = []
        previous_key: tuple[int, Simplex] | None = None
        for _ in range(count):
            if offset >= len(data):
                raise ComplexEncodingError("truncated simplex arity")
            arity = data[offset]
            offset += 1
            if arity == 0 or arity > _MAX_ARITY:
                raise ComplexEncodingError("invalid simplex arity")
            needed = 4 * arity
            if offset + needed > len(data):
                raise ComplexEncodingError("truncated simplex")
            vertices = tuple(struct.unpack_from(f">{arity}I", data, offset))
            offset += needed
            if any(a >= b for a, b in zip(vertices, vertices[1:])):
                raise ComplexEncodingError("vertices are not strictly increasing")
            key = _simplex_sort_key(vertices)
            if previous_key is not None and key <= previous_key:
                raise ComplexEncodingError("simplices are not in canonical order")
            previous_key = key
            simplices.append(vertices)

        if offset != len(data):
            raise ComplexEncodingError("trailing data")

        try:
            complex_ = cls(tuple(simplices))
        except (TypeError, ValueError) as exc:
            raise ComplexEncodingError(str(exc)) from exc
        if complex_.encode() != data:
            raise ComplexEncodingError("non-canonical encoding")
        return complex_
