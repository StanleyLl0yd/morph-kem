from __future__ import annotations

from dataclasses import dataclass
import hashlib
from math import gcd


class HGA2Error(ValueError):
    """Raised when an HGA2 toy action is malformed."""


Point = tuple[int, int]
Matrix2 = tuple[int, int, int, int]


@dataclass(frozen=True, slots=True)
class HGA2Parameters:
    name: str
    planted_word_length: int
    source_bound: int

    def validate(self) -> None:
        if self.planted_word_length < 4 or self.planted_word_length > 128:
            raise HGA2Error("HGA2 planted word length outside toy bounds")
        if self.source_bound < 3 or self.source_bound > 10_000:
            raise HGA2Error("HGA2 source bound outside toy bounds")


HGA2_PARAMETER_SETS = {
    "hga2-12": HGA2Parameters("hga2-12", 12, 31),
    "hga2-20": HGA2Parameters("hga2-20", 20, 63),
    "hga2-32": HGA2Parameters("hga2-32", 32, 127),
}


@dataclass(frozen=True, slots=True)
class HGA2Public:
    name: str
    source: Point
    target: Point
    public_word_bound: int


@dataclass(frozen=True, slots=True)
class HGA2Reference:
    planted_word: str


@dataclass(frozen=True, slots=True)
class HGA2Recovery:
    source: Point
    target: Point
    source_bit_length: int
    target_bit_length: int
    source_euclidean_divisions: int
    target_euclidean_divisions: int
    source_cf_quotients: tuple[int, ...]
    target_cf_quotients: tuple[int, ...]
    recovered_connector: str
    recovered_connector_length: int
    recovered_matrix: Matrix2
    recovered_matrix_entry_bit_length: int
    endpoint_verified: bool
    matches_planted_word_after_public_success: bool | None
    planted_matrix_equal_after_public_success: bool | None
    mod5_fingerprint: tuple[int, int, int, int]
    mod7_fingerprint: tuple[int, int, int, int]
    mod11_fingerprint: tuple[int, int, int, int]


def _normalize_point(point: Point) -> Point:
    p, q = point
    if p == 0 and q == 0:
        raise HGA2Error("projective point cannot be zero")
    divisor = gcd(abs(p), abs(q))
    p //= divisor
    q //= divisor
    if q < 0 or (q == 0 and p < 0):
        p, q = -p, -q
    return p, q


def _apply_generator(point: Point, generator: str) -> Point:
    p, q = point
    if generator == "T":
        return _normalize_point((p + q, q))
    if generator == "t":
        return _normalize_point((p - q, q))
    if generator == "S":
        return _normalize_point((-q, p))
    raise HGA2Error(f"unknown HGA2 generator {generator!r}")


def apply_word(point: Point, word: str) -> Point:
    result = _normalize_point(point)
    for generator in word:
        result = _apply_generator(result, generator)
    return result


def _inverse_word(word: str) -> str:
    inverse = {"T": "t", "t": "T", "S": "S"}
    return "".join(inverse[generator] for generator in reversed(word))


def _matrix_multiply(left: Matrix2, right: Matrix2) -> Matrix2:
    a, b, c, d = left
    e, f, g, h = right
    return (
        a * e + b * g,
        a * f + b * h,
        c * e + d * g,
        c * f + d * h,
    )


def word_matrix(word: str) -> Matrix2:
    generators: dict[str, Matrix2] = {
        "T": (1, 1, 0, 1),
        "t": (1, -1, 0, 1),
        "S": (0, -1, 1, 0),
    }
    result: Matrix2 = (1, 0, 0, 1)
    for generator in word:
        try:
            result = _matrix_multiply(generators[generator], result)
        except KeyError as exc:
            raise HGA2Error(f"unknown HGA2 generator {generator!r}") from exc
    return _canonical_psl_matrix(result)


def _canonical_psl_matrix(matrix: Matrix2) -> Matrix2:
    a, b, c, d = matrix
    determinant = a * d - b * c
    if determinant != 1:
        raise HGA2Error("HGA2 matrix determinant is not one")
    for value in matrix:
        if value:
            if value < 0:
                return tuple(-entry for entry in matrix)  # type: ignore[return-value]
            break
    return matrix


def _matrix_action(matrix: Matrix2, point: Point) -> Point:
    a, b, c, d = matrix
    p, q = point
    return _normalize_point((a * p + b * q, c * p + d * q))


def _digest(domain: bytes, seed: bytes, name: str, counter: int = 0) -> bytes:
    return hashlib.sha256(
        domain + b"\x00" + seed + name.encode("ascii") + counter.to_bytes(8, "big")
    ).digest()


def _sample_source(params: HGA2Parameters, seed: bytes) -> Point:
    for counter in range(1024):
        digest = _digest(b"MORPH-KEM HGA2 source v1", seed, params.name, counter)
        p = 1 + int.from_bytes(digest[:8], "big") % params.source_bound
        q = 1 + int.from_bytes(digest[8:16], "big") % params.source_bound
        if gcd(p, q) == 1:
            return _normalize_point((p, q))
    raise HGA2Error("HGA2 failed to sample primitive source")


def _sample_reduced_word(params: HGA2Parameters, seed: bytes) -> str:
    alphabet = ("T", "t", "S")
    inverse = {"T": "t", "t": "T", "S": "S"}
    word: list[str] = []
    counter = 0
    while len(word) < params.planted_word_length:
        digest = _digest(b"MORPH-KEM HGA2 planted word v1", seed, params.name, counter)
        counter += 1
        candidate = alphabet[int.from_bytes(digest[:8], "big") % len(alphabet)]
        if word and inverse[word[-1]] == candidate:
            continue
        word.append(candidate)
    return "".join(word)


def generate_hga2_instance(
    params: HGA2Parameters,
    master_seed: bytes,
) -> tuple[HGA2Public, HGA2Reference]:
    params.validate()
    if len(master_seed) < 16:
        raise HGA2Error("HGA2 master seed must contain at least 128 bits")
    source = _sample_source(params, master_seed)
    planted = _sample_reduced_word(params, master_seed)
    target = apply_word(source, planted)
    public = HGA2Public(params.name, source, target, params.planted_word_length)
    return public, HGA2Reference(planted)


def _repeat_translation(amount: int) -> str:
    if amount > 0:
        return "T" * amount
    if amount < 0:
        return "t" * (-amount)
    return ""


def reduce_to_infinity(point: Point) -> tuple[str, tuple[int, ...], int]:
    p, q = _normalize_point(point)
    word: list[str] = []
    quotients: list[int] = []
    divisions = 0
    while q != 0:
        quotient = p // q
        quotients.append(quotient)
        divisions += 1
        if quotient:
            # Apply T^{-quotient}: (p,q) -> (p-quotient*q,q).
            word.extend(_repeat_translation(-quotient))
            p -= quotient * q
        # Apply S: (p,q) -> (-q,p). The new denominator is the Euclidean remainder.
        word.append("S")
        p, q = -q, p
        p, q = _normalize_point((p, q))
    result = "".join(word)
    if apply_word(point, result)[1] != 0:
        raise HGA2Error("HGA2 Euclidean reduction did not reach infinity")
    return result, tuple(quotients), divisions


def _point_bit_length(point: Point) -> int:
    return max(abs(point[0]).bit_length(), abs(point[1]).bit_length())


def _matrix_bit_length(matrix: Matrix2) -> int:
    return max(abs(value).bit_length() for value in matrix)


def _mod_fingerprint(matrix: Matrix2, prime: int) -> tuple[int, int, int, int]:
    return tuple(value % prime for value in matrix)  # type: ignore[return-value]


def recover_hga2(
    public: HGA2Public,
    *,
    reference: HGA2Reference | None = None,
) -> HGA2Recovery:
    source_reduction, source_quotients, source_divisions = reduce_to_infinity(public.source)
    target_reduction, target_quotients, target_divisions = reduce_to_infinity(public.target)
    connector = source_reduction + _inverse_word(target_reduction)
    recovered_matrix = word_matrix(connector)
    endpoint_verified = (
        apply_word(public.source, connector) == public.target
        and _matrix_action(recovered_matrix, public.source) == public.target
    )
    matches_word = None
    matrix_equal = None
    if reference is not None:
        matches_word = connector == reference.planted_word
        matrix_equal = recovered_matrix == word_matrix(reference.planted_word)
    return HGA2Recovery(
        source=public.source,
        target=public.target,
        source_bit_length=_point_bit_length(public.source),
        target_bit_length=_point_bit_length(public.target),
        source_euclidean_divisions=source_divisions,
        target_euclidean_divisions=target_divisions,
        source_cf_quotients=source_quotients,
        target_cf_quotients=target_quotients,
        recovered_connector=connector,
        recovered_connector_length=len(connector),
        recovered_matrix=recovered_matrix,
        recovered_matrix_entry_bit_length=_matrix_bit_length(recovered_matrix),
        endpoint_verified=endpoint_verified,
        matches_planted_word_after_public_success=matches_word,
        planted_matrix_equal_after_public_success=matrix_equal,
        mod5_fingerprint=_mod_fingerprint(recovered_matrix, 5),
        mod7_fingerprint=_mod_fingerprint(recovered_matrix, 7),
        mod11_fingerprint=_mod_fingerprint(recovered_matrix, 11),
    )
