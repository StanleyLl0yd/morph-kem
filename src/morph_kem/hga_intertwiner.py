from __future__ import annotations

from dataclasses import dataclass
import hashlib
from itertools import product


class HGA3Error(ValueError):
    """Raised when an HGA3 toy action is malformed."""


Matrix = tuple[tuple[int, ...], ...]
MatrixTuple = tuple[Matrix, ...]


@dataclass(frozen=True, slots=True)
class HGA3Parameters:
    name: str
    prime: int
    dimension: int
    tuple_length: int

    def validate(self) -> None:
        if self.prime not in (5, 7, 11, 13):
            raise HGA3Error("HGA3 prime outside toy set")
        if self.dimension < 2 or self.dimension > 8:
            raise HGA3Error("HGA3 dimension outside toy bounds")
        if self.tuple_length < 2 or self.tuple_length > 5:
            raise HGA3Error("HGA3 tuple length outside toy bounds")


HGA3_PARAMETER_SETS = {
    "hga3-p5-n3": HGA3Parameters("hga3-p5-n3", 5, 3, 3),
    "hga3-p7-n4": HGA3Parameters("hga3-p7-n4", 7, 4, 3),
    "hga3-p11-n5": HGA3Parameters("hga3-p11-n5", 11, 5, 3),
}


@dataclass(frozen=True, slots=True)
class HGA3Public:
    name: str
    prime: int
    source: MatrixTuple
    target: MatrixTuple


@dataclass(frozen=True, slots=True)
class HGA3Reference:
    planted_conjugator: Matrix


@dataclass(frozen=True, slots=True)
class HGA3Recovery:
    prime: int
    dimension: int
    tuple_length: int
    variables: int
    equations: int
    system_rank: int
    system_nullity: int
    row_eliminations: int
    nullspace_basis_size: int
    combination_candidates_tested: int
    recovered_rank: int
    recovered_determinant: int
    exact_endpoint_verified: bool
    scalar_equivalent_to_planted_after_public_success: bool | None
    exactly_matches_planted_after_public_success: bool | None
    source_trace_fingerprint: tuple[int, ...]
    target_trace_fingerprint: tuple[int, ...]


def _digest(domain: bytes, seed: bytes, name: str, counter: int) -> bytes:
    return hashlib.sha256(
        domain + b"\x00" + seed + name.encode("ascii") + counter.to_bytes(8, "big")
    ).digest()


def _identity(n: int) -> Matrix:
    return tuple(tuple(1 if row == col else 0 for col in range(n)) for row in range(n))


def _matmul(left: Matrix, right: Matrix, prime: int) -> Matrix:
    n = len(left)
    if len(right) != n or any(len(row) != n for row in left + right):
        raise HGA3Error("HGA3 matrix dimensions disagree")
    return tuple(
        tuple(
            sum(left[row][mid] * right[mid][col] for mid in range(n)) % prime
            for col in range(n)
        )
        for row in range(n)
    )


def _matrix_rank_and_det(matrix: Matrix, prime: int) -> tuple[int, int]:
    n = len(matrix)
    rows = [list(value % prime for value in row) for row in matrix]
    rank = 0
    determinant = 1
    sign = 1
    for col in range(n):
        pivot = next((row for row in range(rank, n) if rows[row][col] % prime), None)
        if pivot is None:
            determinant = 0
            continue
        if pivot != rank:
            rows[pivot], rows[rank] = rows[rank], rows[pivot]
            sign = -sign
        pivot_value = rows[rank][col] % prime
        determinant = determinant * pivot_value % prime
        inverse = pow(pivot_value, prime - 2, prime)
        rows[rank] = [(value * inverse) % prime for value in rows[rank]]
        for row in range(rank + 1, n):
            factor = rows[row][col] % prime
            if factor:
                rows[row] = [
                    (rows[row][j] - factor * rows[rank][j]) % prime
                    for j in range(n)
                ]
        rank += 1
        if rank == n:
            break
    if rank < n:
        determinant = 0
    else:
        determinant = determinant * sign % prime
    return rank, determinant


def _inverse(matrix: Matrix, prime: int) -> Matrix:
    n = len(matrix)
    augmented = [
        [value % prime for value in matrix[row]]
        + [1 if row == col else 0 for col in range(n)]
        for row in range(n)
    ]
    pivot_row = 0
    for col in range(n):
        pivot = next((row for row in range(pivot_row, n) if augmented[row][col]), None)
        if pivot is None:
            raise HGA3Error("HGA3 matrix is singular")
        augmented[pivot], augmented[pivot_row] = augmented[pivot_row], augmented[pivot]
        inverse = pow(augmented[pivot_row][col], prime - 2, prime)
        augmented[pivot_row] = [(value * inverse) % prime for value in augmented[pivot_row]]
        for row in range(n):
            if row == pivot_row:
                continue
            factor = augmented[row][col]
            if factor:
                augmented[row] = [
                    (augmented[row][j] - factor * augmented[pivot_row][j]) % prime
                    for j in range(2 * n)
                ]
        pivot_row += 1
    return tuple(tuple(row[n:]) for row in augmented)


def _sample_matrix(params: HGA3Parameters, seed: bytes, domain: bytes, counter: int) -> Matrix:
    n = params.dimension
    needed = n * n
    values: list[int] = []
    block = 0
    while len(values) < needed:
        digest = _digest(domain, seed, params.name, counter * 256 + block)
        values.extend(byte % params.prime for byte in digest)
        block += 1
    return tuple(
        tuple(values[row * n + col] for col in range(n))
        for row in range(n)
    )


def _sample_invertible(params: HGA3Parameters, seed: bytes) -> Matrix:
    for attempt in range(1024):
        candidate = _sample_matrix(params, seed, b"MORPH-KEM HGA3 conjugator v1", attempt)
        rank, determinant = _matrix_rank_and_det(candidate, params.prime)
        if rank == params.dimension and determinant:
            return candidate
    raise HGA3Error("HGA3 failed to sample invertible conjugator")


def generate_hga3_instance(
    params: HGA3Parameters,
    master_seed: bytes,
) -> tuple[HGA3Public, HGA3Reference]:
    params.validate()
    if len(master_seed) < 16:
        raise HGA3Error("HGA3 master seed must contain at least 128 bits")
    source = tuple(
        _sample_matrix(params, master_seed, b"MORPH-KEM HGA3 source tuple v1", index)
        for index in range(params.tuple_length)
    )
    conjugator = _sample_invertible(params, master_seed)
    inverse = _inverse(conjugator, params.prime)
    target = tuple(
        _matmul(_matmul(conjugator, matrix, params.prime), inverse, params.prime)
        for matrix in source
    )
    return (
        HGA3Public(params.name, params.prime, source, target),
        HGA3Reference(conjugator),
    )


def _rref_mod(rows: list[list[int]], prime: int, width: int) -> tuple[list[list[int]], tuple[int, ...], int]:
    data = [[value % prime for value in row] for row in rows]
    pivots: list[int] = []
    pivot_row = 0
    eliminations = 0
    for col in range(width):
        pivot = next((row for row in range(pivot_row, len(data)) if data[row][col]), None)
        if pivot is None:
            continue
        data[pivot], data[pivot_row] = data[pivot_row], data[pivot]
        inverse = pow(data[pivot_row][col], prime - 2, prime)
        if data[pivot_row][col] != 1:
            data[pivot_row] = [(value * inverse) % prime for value in data[pivot_row]]
        for row in range(len(data)):
            if row == pivot_row:
                continue
            factor = data[row][col]
            if factor:
                data[row] = [
                    (data[row][j] - factor * data[pivot_row][j]) % prime
                    for j in range(width)
                ]
                eliminations += 1
        pivots.append(col)
        pivot_row += 1
        if pivot_row == len(data):
            break
    return data, tuple(pivots), eliminations


def _nullspace_basis(rows: list[list[int]], prime: int, width: int) -> tuple[tuple[int, ...], tuple[int, ...], int]:
    reduced, pivots, eliminations = _rref_mod(rows, prime, width)
    pivot_to_row = {pivot: index for index, pivot in enumerate(pivots)}
    free = tuple(col for col in range(width) if col not in pivot_to_row)
    basis: list[tuple[int, ...]] = []
    for free_col in free:
        vector = [0] * width
        vector[free_col] = 1
        for pivot in reversed(pivots):
            row = reduced[pivot_to_row[pivot]]
            value = sum(row[col] * vector[col] for col in free) % prime
            vector[pivot] = (-value) % prime
        basis.append(tuple(vector))
    return tuple(basis), pivots, eliminations


def _intertwiner_rows(public: HGA3Public) -> list[list[int]]:
    n = len(public.source[0])
    width = n * n
    rows: list[list[int]] = []
    for source, target in zip(public.source, public.target):
        for row in range(n):
            for col in range(n):
                equation = [0] * width
                # (X A)[row,col]
                for mid in range(n):
                    equation[row * n + mid] = (
                        equation[row * n + mid] + source[mid][col]
                    ) % public.prime
                # -(B X)[row,col]
                for mid in range(n):
                    equation[mid * n + col] = (
                        equation[mid * n + col] - target[row][mid]
                    ) % public.prime
                rows.append(equation)
    return rows


def _vector_to_matrix(vector: tuple[int, ...], n: int) -> Matrix:
    return tuple(tuple(vector[row * n + col] for col in range(n)) for row in range(n))


def _linear_combination(
    basis: tuple[tuple[int, ...], ...], coefficients: tuple[int, ...], prime: int
) -> tuple[int, ...]:
    width = len(basis[0])
    return tuple(
        sum(coefficients[index] * basis[index][col] for index in range(len(basis))) % prime
        for col in range(width)
    )


def _find_invertible(
    basis: tuple[tuple[int, ...], ...], n: int, prime: int
) -> tuple[Matrix, int, int, int]:
    if not basis:
        raise HGA3Error("HGA3 intertwiner space is empty")
    tested = 0
    # Deterministic exhaustive search is bounded by the tiny toy nullities.  Test
    # sparse coefficient vectors first, then lexicographic combinations.
    for weight in range(1, len(basis) + 1):
        for support in __import__("itertools").combinations(range(len(basis)), weight):
            for values in product(range(1, prime), repeat=weight):
                coefficients = [0] * len(basis)
                for index, value in zip(support, values):
                    coefficients[index] = value
                tested += 1
                vector = _linear_combination(basis, tuple(coefficients), prime)
                matrix = _vector_to_matrix(vector, n)
                rank, determinant = _matrix_rank_and_det(matrix, prime)
                if rank == n:
                    return matrix, tested, rank, determinant
                if tested >= 100_000:
                    raise HGA3Error("HGA3 invertible-combination search cap exhausted")
    raise HGA3Error("HGA3 found no invertible public intertwiner")


def _verify(public: HGA3Public, candidate: Matrix) -> bool:
    try:
        inverse = _inverse(candidate, public.prime)
    except HGA3Error:
        return False
    return all(
        _matmul(_matmul(candidate, source, public.prime), inverse, public.prime) == target
        for source, target in zip(public.source, public.target)
    )


def _trace(matrix: Matrix, prime: int) -> int:
    return sum(matrix[index][index] for index in range(len(matrix))) % prime


def _trace_fingerprint(matrices: MatrixTuple, prime: int) -> tuple[int, ...]:
    values = [_trace(matrix, prime) for matrix in matrices]
    if len(matrices) >= 2:
        values.append(_trace(_matmul(matrices[0], matrices[1], prime), prime))
    if len(matrices) >= 3:
        values.append(
            _trace(_matmul(_matmul(matrices[0], matrices[1], prime), matrices[2], prime), prime)
        )
    return tuple(values)


def _scalar_equivalent(left: Matrix, right: Matrix, prime: int) -> bool:
    ratio: int | None = None
    n = len(left)
    for row in range(n):
        for col in range(n):
            a = left[row][col] % prime
            b = right[row][col] % prime
            if b == 0:
                if a != 0:
                    return False
                continue
            candidate = a * pow(b, prime - 2, prime) % prime
            if ratio is None:
                ratio = candidate
            elif candidate != ratio:
                return False
    return ratio not in (None, 0)


def recover_hga3(
    public: HGA3Public,
    *,
    reference: HGA3Reference | None = None,
) -> HGA3Recovery:
    n = len(public.source[0])
    rows = _intertwiner_rows(public)
    basis, pivots, eliminations = _nullspace_basis(rows, public.prime, n * n)
    candidate, tested, rank, determinant = _find_invertible(basis, n, public.prime)
    verified = _verify(public, candidate)
    scalar_match = None
    exact_match = None
    if reference is not None:
        scalar_match = _scalar_equivalent(candidate, reference.planted_conjugator, public.prime)
        exact_match = candidate == reference.planted_conjugator
    source_fingerprint = _trace_fingerprint(public.source, public.prime)
    target_fingerprint = _trace_fingerprint(public.target, public.prime)
    if source_fingerprint != target_fingerprint:
        raise HGA3Error("HGA3 conjugacy trace fingerprints disagree")
    return HGA3Recovery(
        prime=public.prime,
        dimension=n,
        tuple_length=len(public.source),
        variables=n * n,
        equations=len(rows),
        system_rank=len(pivots),
        system_nullity=len(basis),
        row_eliminations=eliminations,
        nullspace_basis_size=len(basis),
        combination_candidates_tested=tested,
        recovered_rank=rank,
        recovered_determinant=determinant,
        exact_endpoint_verified=verified,
        scalar_equivalent_to_planted_after_public_success=scalar_match,
        exactly_matches_planted_after_public_success=exact_match,
        source_trace_fingerprint=source_fingerprint,
        target_trace_fingerprint=target_fingerprint,
    )
