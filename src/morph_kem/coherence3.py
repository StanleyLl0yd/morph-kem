from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
import hashlib
import json

from .complex import SimplicialComplex
from .crossed_q8 import Q8_MINUS_ONE, boundary, q8_mul

Simplex = tuple[int, ...]


class KernelCoherenceError(ValueError):
    """Raised when a K2.3 3-dimensional kernel-coherence input is invalid."""


@dataclass(frozen=True, slots=True)
class Boundary4Simplex:
    complex: SimplicialComplex
    vertices: tuple[int, ...]
    edges: tuple[Simplex, ...]
    faces: tuple[Simplex, ...]
    tetrahedra: tuple[Simplex, ...]
    face_tetra_degrees: tuple[int, ...]
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise KernelCoherenceError("unsupported K2.3 scaffold version")
        if (len(self.vertices), len(self.edges), len(self.faces), len(self.tetrahedra)) != (5, 10, 10, 5):
            raise KernelCoherenceError("boundary-4-simplex cell counts must be 5/10/10/5")
        if self.complex.dimension != 3:
            raise KernelCoherenceError("K2.3 scaffold must be three-dimensional")
        if any(degree != 2 for degree in self.face_tetra_degrees):
            raise KernelCoherenceError("every triangular face must lie in exactly two tetrahedra")
        if self.euler_characteristic != 0:
            raise KernelCoherenceError("boundary-4-simplex Euler characteristic must be zero")

    @property
    def euler_characteristic(self) -> int:
        return len(self.vertices) - len(self.edges) + len(self.faces) - len(self.tetrahedra)

    def encode(self) -> bytes:
        payload = {
            "edges": [list(value) for value in self.edges],
            "faces": [list(value) for value in self.faces],
            "tetrahedra": [list(value) for value in self.tetrahedra],
            "version": self.version,
            "vertices": list(self.vertices),
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


@lru_cache(maxsize=1)
def generate_boundary4_simplex() -> Boundary4Simplex:
    tetrahedra = tuple(combinations(range(5), 4))
    complex_ = SimplicialComplex.from_facets(tetrahedra)
    vertices = tuple(simplex[0] for simplex in complex_.simplices if len(simplex) == 1)
    edges = tuple(simplex for simplex in complex_.simplices if len(simplex) == 2)
    faces = tuple(simplex for simplex in complex_.simplices if len(simplex) == 3)
    facets = tuple(simplex for simplex in complex_.simplices if len(simplex) == 4)
    degrees = tuple(
        sum(set(face).issubset(tetrahedron) for tetrahedron in facets)
        for face in faces
    )
    return Boundary4Simplex(
        complex=complex_,
        vertices=vertices,
        edges=edges,
        faces=faces,
        tetrahedra=facets,
        face_tetra_degrees=degrees,
    )


@dataclass(frozen=True, slots=True)
class KernelCoherencePublic:
    scaffold: Boundary4Simplex
    face_boundaries: tuple[int, ...]
    tetra_syndromes: tuple[int, ...]
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise KernelCoherenceError("unsupported K2.3 public version")
        if len(self.face_boundaries) != len(self.scaffold.faces):
            raise KernelCoherenceError("face-boundary count mismatch")
        if len(self.tetra_syndromes) != len(self.scaffold.tetrahedra):
            raise KernelCoherenceError("tetrahedron syndrome count mismatch")
        image = {boundary(element) for element in range(8)}
        if any(value not in image for value in self.face_boundaries):
            raise KernelCoherenceError("public face boundary is outside im(partial)")
        if any(value not in (0, 1) for value in self.tetra_syndromes):
            raise KernelCoherenceError("tetrahedron syndromes must be bits")

    def encode(self) -> bytes:
        payload = {
            "face_boundaries": list(self.face_boundaries),
            "scaffold": json.loads(self.scaffold.encode().decode("ascii")),
            "tetra_syndromes": list(self.tetra_syndromes),
            "version": self.version,
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


@dataclass(frozen=True, slots=True)
class KernelCoherenceReference:
    face_values: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class GF2SolveResult:
    consistent: bool
    solution: tuple[int, ...]
    rank: int
    nullity: int
    pivot_columns: tuple[int, ...]
    row_xors: int


@dataclass(frozen=True, slots=True)
class KernelCoherenceAttack:
    accepted: bool
    face_values: tuple[int, ...]
    kernel_bits: tuple[int, ...]
    equations: int
    variables: int
    rank: int
    nullity: int
    dependent_equations: int
    equivalent_witnesses: int
    row_xors: int


def face_boundary_fiber(boundary_value: int) -> tuple[int, ...]:
    return tuple(element for element in range(8) if boundary(element) == boundary_value)


def canonical_face_lift(boundary_value: int) -> int:
    fiber = face_boundary_fiber(boundary_value)
    if not fiber:
        raise KernelCoherenceError("face boundary has no Q8 lift")
    return min(fiber)


def kernel_bit_for_face(boundary_value: int, face_value: int) -> int | None:
    if face_value < 0 or face_value >= 8:
        return None
    canonical = canonical_face_lift(boundary_value)
    alternate = q8_mul(Q8_MINUS_ONE, canonical)
    if face_value == canonical:
        return 0
    if face_value == alternate and boundary(face_value) == boundary_value:
        return 1
    return None


def coherence_rows(scaffold: Boundary4Simplex) -> tuple[int, ...]:
    face_index = {face: index for index, face in enumerate(scaffold.faces)}
    rows: list[int] = []
    for tetrahedron in scaffold.tetrahedra:
        mask = 0
        for face in combinations(tetrahedron, 3):
            mask |= 1 << face_index[tuple(face)]
        rows.append(mask)
    return tuple(rows)


def apply_coherence_rows(rows: tuple[int, ...], bits: tuple[int, ...]) -> tuple[int, ...]:
    packed = sum((bit & 1) << index for index, bit in enumerate(bits))
    return tuple((row & packed).bit_count() & 1 for row in rows)


def solve_affine_gf2(
    rows: tuple[int, ...],
    rhs: tuple[int, ...],
    variables: int,
) -> GF2SolveResult:
    if len(rows) != len(rhs):
        raise KernelCoherenceError("GF(2) row/right-hand-side count mismatch")
    if variables <= 0 or variables > 4096:
        raise KernelCoherenceError("GF(2) variable count outside supported range")
    if any(value not in (0, 1) for value in rhs):
        raise KernelCoherenceError("GF(2) right-hand side must contain bits")
    limit = (1 << variables) - 1
    if any(row < 0 or row & ~limit for row in rows):
        raise KernelCoherenceError("GF(2) row contains an out-of-range variable")

    work = [[row, bit] for row, bit in zip(rows, rhs)]
    pivot_columns: list[int] = []
    pivot_row = 0
    row_xors = 0

    for column in range(variables):
        selected = next(
            (index for index in range(pivot_row, len(work)) if (work[index][0] >> column) & 1),
            None,
        )
        if selected is None:
            continue
        work[pivot_row], work[selected] = work[selected], work[pivot_row]
        for index in range(len(work)):
            if index == pivot_row:
                continue
            if (work[index][0] >> column) & 1:
                work[index][0] ^= work[pivot_row][0]
                work[index][1] ^= work[pivot_row][1]
                row_xors += 1
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break

    consistent = all(mask != 0 or bit == 0 for mask, bit in work)
    rank = len(pivot_columns)
    nullity = variables - rank
    if not consistent:
        return GF2SolveResult(False, (), rank, nullity, tuple(pivot_columns), row_xors)

    # Free variables are fixed to zero for one deterministic public representative.
    solution = [0] * variables
    for index, column in enumerate(pivot_columns):
        solution[column] = work[index][1]

    candidate = tuple(solution)
    if apply_coherence_rows(rows, candidate) != rhs:
        raise KernelCoherenceError("internal GF(2) elimination produced an invalid solution")
    return GF2SolveResult(True, candidate, rank, nullity, tuple(pivot_columns), row_xors)


def validate_kernel_coherence(
    public: KernelCoherencePublic,
    face_values: tuple[int, ...],
) -> bool:
    if len(face_values) != len(public.scaffold.faces):
        return False
    bits: list[int] = []
    for boundary_value, face_value in zip(public.face_boundaries, face_values):
        bit = kernel_bit_for_face(boundary_value, face_value)
        if bit is None:
            return False
        bits.append(bit)
    rows = coherence_rows(public.scaffold)
    return apply_coherence_rows(rows, tuple(bits)) == public.tetra_syndromes


def _deterministic_byte(master_seed: bytes, label: bytes, index: int) -> int:
    return hashlib.sha256(
        b"MORPH-KEM K2.3 kernel coherence v1\x00"
        + label
        + b"\x00"
        + master_seed
        + index.to_bytes(4, "big")
    ).digest()[0]


def generate_kernel_coherence_instance(
    master_seed: bytes,
) -> tuple[KernelCoherencePublic, KernelCoherenceReference]:
    if not isinstance(master_seed, bytes) or not master_seed:
        raise KernelCoherenceError("master_seed must be non-empty bytes")

    scaffold = generate_boundary4_simplex()
    image = tuple(sorted({boundary(element) for element in range(8)}))
    face_boundaries = tuple(
        image[_deterministic_byte(master_seed, b"boundary", index) % len(image)]
        for index in range(len(scaffold.faces))
    )
    bits = tuple(
        _deterministic_byte(master_seed, b"kernel-bit", index) & 1
        for index in range(len(scaffold.faces))
    )
    if not any(bits):
        bits = (1,) + bits[1:]

    rows = coherence_rows(scaffold)
    syndromes = apply_coherence_rows(rows, bits)
    public = KernelCoherencePublic(scaffold, face_boundaries, syndromes)

    face_values = tuple(
        canonical_face_lift(boundary_value)
        if bit == 0
        else q8_mul(Q8_MINUS_ONE, canonical_face_lift(boundary_value))
        for boundary_value, bit in zip(face_boundaries, bits)
    )
    reference = KernelCoherenceReference(face_values)
    if not validate_kernel_coherence(public, reference.face_values):
        raise KernelCoherenceError("internal K2.3 reference validation failed")
    return public, reference


def public_gf2_coherence_attack(public: KernelCoherencePublic) -> KernelCoherenceAttack:
    rows = coherence_rows(public.scaffold)
    solved = solve_affine_gf2(rows, public.tetra_syndromes, len(public.scaffold.faces))
    if not solved.consistent:
        return KernelCoherenceAttack(
            accepted=False,
            face_values=(),
            kernel_bits=(),
            equations=len(rows),
            variables=len(public.scaffold.faces),
            rank=solved.rank,
            nullity=solved.nullity,
            dependent_equations=len(rows) - solved.rank,
            equivalent_witnesses=0,
            row_xors=solved.row_xors,
        )

    face_values = tuple(
        canonical_face_lift(boundary_value)
        if bit == 0
        else q8_mul(Q8_MINUS_ONE, canonical_face_lift(boundary_value))
        for boundary_value, bit in zip(public.face_boundaries, solved.solution)
    )
    accepted = validate_kernel_coherence(public, face_values)
    return KernelCoherenceAttack(
        accepted=accepted,
        face_values=face_values,
        kernel_bits=solved.solution,
        equations=len(rows),
        variables=len(public.scaffold.faces),
        rank=solved.rank,
        nullity=solved.nullity,
        dependent_equations=len(rows) - solved.rank,
        equivalent_witnesses=(1 << solved.nullity) if accepted else 0,
        row_xors=solved.row_xors,
    )
