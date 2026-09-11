from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib

from .complex import SimplicialComplex
from .gluing import GluingExperimentError
from .gluing_cohomology_cycle import _edges, _pairing, _rref, _tree_path_edges
from .gluing_genus2_crossing_basis import (
    GenusTwoCrossingBasisParameters,
    generate_genus2_crossing_basis_instance,
)
from .gluing_genus2_multicurve import _cohomology_basis
from .gluing_length_bounded_pair import _seeded_spanning_tree
from .gluing_surface_hypercover import (
    ToroidalHypercoverPublicInstance,
    toroidal_hypercover_incidence,
)
from .gluing_symplectic_cycle_pair import Cycle, _is_one_simple_cycle


@dataclass(frozen=True, slots=True)
class SameSideParameters:
    name: str
    rows: int
    cols: int
    successful_flips: int
    max_cycle_length: int
    public_tree_samples: int = 16
    candidates_per_signature: int = 10

    def validate(self) -> None:
        if self.rows < 4 or self.rows > 12 or self.cols < 4 or self.cols > 12:
            raise GluingExperimentError("G22 torus dimensions outside toy bounds")
        if self.successful_flips < 1:
            raise GluingExperimentError("G22 successful-flip target must be positive")
        if self.max_cycle_length < 3 or self.max_cycle_length > 128:
            raise GluingExperimentError("G22 public cycle-length bound outside toy bounds")
        if self.public_tree_samples < 1 or self.public_tree_samples > 64:
            raise GluingExperimentError("G22 tree sample count outside toy bounds")
        if self.candidates_per_signature < 1 or self.candidates_per_signature > 64:
            raise GluingExperimentError("G22 candidate cap outside toy bounds")


G22_PARAMETER_SETS = {
    "g22-4x4": SameSideParameters("g22-4x4", 4, 4, 124, 16),
    "g22-6x6": SameSideParameters("g22-6x6", 6, 6, 284, 24),
    "g22-6x9": SameSideParameters("g22-6x9", 6, 9, 428, 30),
}


@dataclass(frozen=True, slots=True)
class SameSidePublicInstance:
    name: str
    target: SimplicialComplex
    max_cycle_length: int
    public_tree_samples: int
    candidates_per_signature: int


@dataclass(frozen=True, slots=True)
class SameSideWitness:
    cycles: tuple[Cycle, Cycle, Cycle, Cycle]


@dataclass(frozen=True, slots=True)
class SameSideValidation:
    valid: bool
    reason: str
    lengths: tuple[int, ...]
    signatures: tuple[int, ...]
    signature_rank: int
    vertex_intersection_matrix: tuple[tuple[int, ...], ...]


@dataclass(frozen=True, slots=True)
class SameSideRecovery:
    vertices: int
    edges: int
    triangles: int
    euler_characteristic: int
    h1_dimension: int
    tree_samples: int
    raw_fundamental_cycles: int
    distinct_cycles: int
    bounded_nonzero_cycles: int
    candidate_signature_histogram: tuple[tuple[int, int], ...]
    retained_candidates: int
    exact_one_pairs: int
    pair_pair_tests: int
    selected_lengths: tuple[int, ...]
    selected_signatures: tuple[int, ...]
    selected_rank: int
    selected_intersection_matrix: tuple[tuple[int, ...], ...]
    selected_accepted: bool


def _cycle_vertices(cycle: Cycle) -> frozenset[int]:
    vertices: set[int] = set()
    for left, right in cycle:
        vertices.add(left)
        vertices.add(right)
    return frozenset(vertices)


def _signature_with_width(
    cocycles: tuple[int, ...],
    edge_count: int,
    indices: tuple[int, ...],
) -> int:
    value = 0
    for bit, cocycle in enumerate(cocycles):
        cochain = tuple((cocycle >> index) & 1 for index in range(edge_count))
        value |= _pairing(cochain, indices) << bit
    return value


def _rank(signatures: tuple[int, ...]) -> int:
    return _rref(list(signatures), 4).rank


def _intersection_matrix(cycles: tuple[Cycle, ...]) -> tuple[tuple[int, ...], ...]:
    vertices = tuple(_cycle_vertices(cycle) for cycle in cycles)
    return tuple(
        tuple(len(left & right) for right in vertices)
        for left in vertices
    )


def _enumerate_candidates(
    public: SameSidePublicInstance,
) -> tuple[
    tuple[tuple[tuple[int, ...], int, frozenset[int]], ...],
    int,
    int,
    tuple[tuple[int, int], ...],
]:
    edges, cocycles, h1_dimension = _cohomology_basis(public.target)
    if h1_dimension != 4 or len(cocycles) != 4:
        raise GluingExperimentError("G22 carrier must expose four public cohomology basis vectors")

    fingerprint = hashlib.sha256(
        b"MORPH-KEM G22 public candidate trees v1\x00" + public.target.encode()
    ).digest()
    raw = 0
    unique: dict[tuple[int, ...], tuple[int, frozenset[int]]] = {}
    for tree_index in range(public.public_tree_samples):
        seed = hashlib.sha256(fingerprint + tree_index.to_bytes(4, "big")).digest()
        tree = _seeded_spanning_tree(len(public.target.vertices), edges, seed)
        for edge_index, (left, right) in enumerate(edges):
            if edge_index in tree.tree_edges:
                continue
            raw += 1
            path = _tree_path_edges(left, right, tree)
            indices = tuple(sorted(path + (edge_index,)))
            if len(indices) > public.max_cycle_length:
                continue
            cycle = tuple(sorted(edges[index] for index in indices))
            if not _is_one_simple_cycle(cycle, edges):
                raise GluingExperimentError("G22 fundamental candidate is not one simple cycle")
            signature = _signature_with_width(cocycles, len(edges), indices)
            if signature == 0:
                continue
            unique.setdefault(indices, (signature, _cycle_vertices(cycle)))

    histogram = Counter(signature for signature, _ in unique.values())
    by_signature: dict[int, list[tuple[tuple[int, ...], int, frozenset[int]]]] = defaultdict(list)
    for indices, (signature, vertices) in unique.items():
        by_signature[signature].append((indices, signature, vertices))
    retained: list[tuple[tuple[int, ...], int, frozenset[int]]] = []
    for signature in sorted(by_signature):
        values = sorted(by_signature[signature], key=lambda item: (len(item[0]), item[0]))
        retained.extend(values[: public.candidates_per_signature])
    retained.sort(key=lambda item: (len(item[0]), item[1], item[0]))
    return tuple(retained), raw, len(unique), tuple(sorted(histogram.items()))


def validate_same_side_witness(
    public: SameSidePublicInstance,
    witness: SameSideWitness,
) -> SameSideValidation:
    if len(witness.cycles) != 4 or len(set(witness.cycles)) != 4:
        return SameSideValidation(False, "G22 witness needs four distinct cycles", (), (), 0, ())
    edges, cocycles, h1_dimension = _cohomology_basis(public.target)
    if h1_dimension != 4:
        return SameSideValidation(False, "G22 public H1 dimension is not four", (), (), 0, ())
    edge_lookup = {edge: index for index, edge in enumerate(edges)}
    lengths: list[int] = []
    signatures: list[int] = []
    for cycle in witness.cycles:
        if not _is_one_simple_cycle(cycle, edges):
            return SameSideValidation(False, "G22 witness contains a non-simple cycle", tuple(lengths), tuple(signatures), 0, ())
        if len(cycle) > public.max_cycle_length:
            return SameSideValidation(False, "G22 witness exceeds public length bound", tuple(lengths), tuple(signatures), 0, ())
        indices = tuple(edge_lookup[edge] for edge in cycle)
        lengths.append(len(cycle))
        signatures.append(_signature_with_width(cocycles, len(edges), indices))
    signature_tuple = tuple(signatures)
    rank = _rank(signature_tuple)
    matrix = _intersection_matrix(witness.cycles)
    if rank != 4:
        return SameSideValidation(False, "G22 cycle classes do not span H1", tuple(lengths), signature_tuple, rank, matrix)

    expected = (
        (0, 1, 0, 0),
        (1, 0, 0, 0),
        (0, 0, 0, 1),
        (0, 0, 1, 0),
    )
    off_diagonal = tuple(
        tuple(0 if row == column else matrix[row][column] for column in range(4))
        for row in range(4)
    )
    if off_diagonal != expected:
        return SameSideValidation(False, "G22 same-side geometric intersection pattern differs from target", tuple(lengths), signature_tuple, rank, matrix)
    return SameSideValidation(True, "accepted", tuple(lengths), signature_tuple, rank, matrix)


def recover_same_side_witness(public: SameSidePublicInstance) -> SameSideRecovery:
    incidence = toroidal_hypercover_incidence(
        ToroidalHypercoverPublicInstance(public.name, public.target)
    )
    _, _, h1_dimension = _cohomology_basis(public.target)
    candidates, raw, distinct, signature_hist = _enumerate_candidates(public)
    edges = _edges(public.target)

    exact_pairs: list[tuple[int, int, frozenset[int]]] = []
    for left in range(len(candidates)):
        for right in range(left + 1, len(candidates)):
            if len(candidates[left][2] & candidates[right][2]) != 1:
                continue
            if candidates[left][1] == candidates[right][1]:
                continue
            exact_pairs.append((left, right, candidates[left][2] | candidates[right][2]))
    exact_pairs.sort(
        key=lambda pair: (
            len(candidates[pair[0]][0]) + len(candidates[pair[1]][0]),
            candidates[pair[0]][1], candidates[pair[1]][1],
            candidates[pair[0]][0], candidates[pair[1]][0],
        )
    )

    tests = 0
    selected: SameSideWitness | None = None
    validation: SameSideValidation | None = None
    for first_index, first in enumerate(exact_pairs):
        a, b, first_vertices = first
        for second in exact_pairs[first_index + 1 :]:
            c, d, second_vertices = second
            tests += 1
            if first_vertices & second_vertices:
                continue
            if len({a, b, c, d}) != 4:
                continue
            signatures = (
                candidates[a][1], candidates[b][1], candidates[c][1], candidates[d][1]
            )
            if _rank(signatures) != 4:
                continue
            cycles = tuple(
                tuple(sorted(edges[index] for index in candidates[item][0]))
                for item in (a, b, c, d)
            )
            witness = SameSideWitness(cycles)  # type: ignore[arg-type]
            check = validate_same_side_witness(public, witness)
            if check.valid:
                selected = witness
                validation = check
                break
        if selected is not None:
            break
    if selected is None or validation is None:
        raise GluingExperimentError("G22 public candidate/compatibility attack found no accepted family")

    return SameSideRecovery(
        vertices=incidence.vertices,
        edges=incidence.edges,
        triangles=incidence.triangles,
        euler_characteristic=incidence.euler_characteristic,
        h1_dimension=h1_dimension,
        tree_samples=public.public_tree_samples,
        raw_fundamental_cycles=raw,
        distinct_cycles=distinct,
        bounded_nonzero_cycles=sum(count for _, count in signature_hist),
        candidate_signature_histogram=signature_hist,
        retained_candidates=len(candidates),
        exact_one_pairs=len(exact_pairs),
        pair_pair_tests=tests,
        selected_lengths=validation.lengths,
        selected_signatures=validation.signatures,
        selected_rank=validation.signature_rank,
        selected_intersection_matrix=validation.vertex_intersection_matrix,
        selected_accepted=validation.valid,
    )


def generate_same_side_instance(
    params: SameSideParameters,
    master_seed: bytes,
) -> SameSidePublicInstance:
    params.validate()
    if len(master_seed) < 16:
        raise GluingExperimentError("G22 master seed must contain at least 128 bits")
    carrier = generate_genus2_crossing_basis_instance(
        GenusTwoCrossingBasisParameters(
            params.name + "-carrier",
            params.rows,
            params.cols,
            params.successful_flips,
        ),
        hashlib.sha256(b"MORPH-KEM G22 carrier v1\x00" + master_seed).digest(),
    )
    public = SameSidePublicInstance(
        name=params.name,
        target=carrier.target,
        max_cycle_length=params.max_cycle_length,
        public_tree_samples=params.public_tree_samples,
        candidates_per_signature=params.candidates_per_signature,
    )
    incidence = toroidal_hypercover_incidence(
        ToroidalHypercoverPublicInstance(params.name, public.target)
    )
    if incidence.euler_characteristic != -2:
        raise GluingExperimentError("G22 carrier is not genus two by Euler characteristic")
    recovery = recover_same_side_witness(public)
    if not recovery.selected_accepted:
        raise GluingExperimentError("G22 generated carrier failed public attack calibration")
    return public
