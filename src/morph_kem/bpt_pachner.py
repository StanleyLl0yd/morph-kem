from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import hashlib
from itertools import combinations, permutations

from .complex import SimplicialComplex


class BPTError(ValueError):
    """Raised when a BPT toy triangulation or move is malformed."""


@dataclass(frozen=True, slots=True)
class BPTWeakParameters:
    name: str
    stack_depth: int

    def validate(self) -> None:
        if self.stack_depth < 1 or self.stack_depth > 3:
            raise BPTError("BPT-W0 stack depth outside weak-control bounds")


BPT_WEAK_PARAMETER_SETS = {
    "bptw0-d1": BPTWeakParameters("bptw0-d1", 1),
    "bptw0-d2": BPTWeakParameters("bptw0-d2", 2),
    "bptw0-d3": BPTWeakParameters("bptw0-d3", 3),
}


@dataclass(frozen=True, slots=True)
class BPTMove:
    kind: str
    tetrahedron: tuple[int, int, int, int]
    vertex: int

    def __post_init__(self) -> None:
        if self.kind not in ("1-4", "4-1"):
            raise BPTError("unsupported BPT-W0 move kind")
        if len(self.tetrahedron) != 4 or tuple(sorted(self.tetrahedron)) != self.tetrahedron:
            raise BPTError("move tetrahedron must contain four sorted vertices")
        if len(set(self.tetrahedron)) != 4:
            raise BPTError("move tetrahedron repeats a vertex")
        if self.vertex < 0:
            raise BPTError("move vertex must be non-negative")


@dataclass(frozen=True, slots=True)
class BPTWeakPublic:
    name: str
    source: SimplicialComplex
    target: SimplicialComplex
    move_bound: int


@dataclass(frozen=True, slots=True)
class BPTWeakReference:
    planted_path: tuple[BPTMove, ...]
    target_generation_retries: int


@dataclass(frozen=True, slots=True)
class BPTSimplification:
    root: SimplicialComplex
    moves: tuple[BPTMove, ...]
    vertex_scans: int
    legal_moves_seen: int


@dataclass(frozen=True, slots=True)
class BPTWeakRecovery:
    accepted: bool
    recovered_path: tuple[BPTMove, ...]
    recovered_length: int
    source_simplification_steps: int
    target_simplification_steps: int
    source_vertex_scans: int
    target_vertex_scans: int
    source_legal_moves_seen: int
    target_legal_moves_seen: int
    common_root_exact: bool
    common_root_isomorphic: bool
    source_simplification_paths: int
    target_simplification_paths: int
    accepted_path_multiplicity_lower_bound: int
    matches_planted_after_public_success: bool | None


def boundary_of_4_simplex() -> SimplicialComplex:
    """Return the standard five-tetrahedron triangulation of S^3."""
    return SimplicialComplex.from_facets(combinations(range(5), 4))


def _tetrahedra(complex_: SimplicialComplex) -> tuple[tuple[int, int, int, int], ...]:
    if complex_.dimension != 3:
        raise BPTError("BPT-W0 requires a three-dimensional simplicial complex")
    facets = complex_.facets
    if any(len(facet) != 4 for facet in facets):
        raise BPTError("BPT-W0 requires a pure tetrahedral complex")
    return tuple(facets)  # type: ignore[return-value]


def _rebuild(facets: set[tuple[int, int, int, int]]) -> SimplicialComplex:
    return SimplicialComplex.from_facets(sorted(facets))


def apply_one_four(
    complex_: SimplicialComplex,
    tetrahedron: tuple[int, int, int, int],
    new_vertex: int,
) -> SimplicialComplex:
    tetrahedron = tuple(sorted(tetrahedron))  # type: ignore[assignment]
    facets = set(_tetrahedra(complex_))
    if tetrahedron not in facets:
        raise BPTError("1-4 move tetrahedron is not a facet")
    if new_vertex in set(complex_.vertices):
        raise BPTError("1-4 move requires a fresh vertex")

    facets.remove(tetrahedron)
    for face in combinations(tetrahedron, 3):
        facets.add(tuple(sorted((*face, new_vertex))))
    return _rebuild(facets)


def four_one_move_for_vertex(
    complex_: SimplicialComplex,
    vertex: int,
) -> BPTMove | None:
    facets = _tetrahedra(complex_)
    incident = tuple(facet for facet in facets if vertex in facet)
    if len(incident) != 4:
        return None

    neighbours = tuple(sorted({v for facet in incident for v in facet if v != vertex}))
    if len(neighbours) != 4:
        return None

    expected = {
        tuple(sorted((vertex, *face)))
        for face in combinations(neighbours, 3)
    }
    if set(incident) != expected:
        return None

    replacement = tuple(neighbours)
    if replacement in set(facets):
        return None
    return BPTMove("4-1", replacement, vertex)


def apply_four_one(
    complex_: SimplicialComplex,
    vertex: int,
    expected_tetrahedron: tuple[int, int, int, int] | None = None,
) -> SimplicialComplex:
    move = four_one_move_for_vertex(complex_, vertex)
    if move is None:
        raise BPTError("4-1 move is not legal at this vertex")
    if expected_tetrahedron is not None and tuple(sorted(expected_tetrahedron)) != move.tetrahedron:
        raise BPTError("4-1 move replacement tetrahedron does not match public move")

    facets = set(_tetrahedra(complex_))
    incident = {facet for facet in facets if vertex in facet}
    facets.difference_update(incident)
    facets.add(move.tetrahedron)
    return _rebuild(facets)


def apply_move(complex_: SimplicialComplex, move: BPTMove) -> SimplicialComplex:
    if move.kind == "1-4":
        return apply_one_four(complex_, move.tetrahedron, move.vertex)
    return apply_four_one(complex_, move.vertex, move.tetrahedron)


def inverse_move(move: BPTMove) -> BPTMove:
    if move.kind == "1-4":
        return BPTMove("4-1", move.tetrahedron, move.vertex)
    return BPTMove("1-4", move.tetrahedron, move.vertex)


def apply_path(complex_: SimplicialComplex, path: tuple[BPTMove, ...]) -> SimplicialComplex:
    current = complex_
    for move in path:
        current = apply_move(current, move)
    return current


def legal_four_one_moves(complex_: SimplicialComplex) -> tuple[BPTMove, ...]:
    result = []
    for vertex in complex_.vertices:
        move = four_one_move_for_vertex(complex_, vertex)
        if move is not None:
            result.append(move)
    result.sort(key=lambda move: (move.vertex, move.tetrahedron))
    return tuple(result)


def greedy_simplify(complex_: SimplicialComplex) -> BPTSimplification:
    current = complex_
    moves: list[BPTMove] = []
    scans = 0
    legal_seen = 0
    while True:
        scans += len(current.vertices)
        legal = legal_four_one_moves(current)
        legal_seen += len(legal)
        if not legal:
            break
        chosen = legal[0]
        current = apply_move(current, chosen)
        moves.append(chosen)
    return BPTSimplification(current, tuple(moves), scans, legal_seen)


@lru_cache(maxsize=2048)
def canonical_tetrahedral_signature(complex_: SimplicialComplex) -> tuple[tuple[int, int, int, int], ...]:
    """Exact toy isomorphism signature by exhaustive relabeling."""
    vertices = tuple(sorted(complex_.vertices))
    if len(vertices) > 8:
        raise BPTError("exact BPT-W0 canonicalization is limited to eight vertices")
    facets = _tetrahedra(complex_)
    best: tuple[tuple[int, int, int, int], ...] | None = None
    for labels in permutations(range(len(vertices))):
        mapping = dict(zip(vertices, labels))
        candidate = tuple(
            sorted(tuple(sorted(mapping[v] for v in facet)) for facet in facets)
        )
        if best is None or candidate < best:
            best = candidate
    if best is None:
        raise BPTError("empty tetrahedral signature")
    return best


def recover_tetrahedral_isomorphism(
    left: SimplicialComplex,
    right: SimplicialComplex,
) -> tuple[tuple[int, int], ...] | None:
    """Recover a deterministic exact vertex isomorphism from left to right.

    The exhaustive search is intentionally limited to the tiny BPT-W0 range.
    """
    left_vertices = tuple(sorted(left.vertices))
    right_vertices = tuple(sorted(right.vertices))
    if len(left_vertices) != len(right_vertices):
        return None
    left_facets = _tetrahedra(left)
    right_facets = set(_tetrahedra(right))
    if len(left_facets) != len(right_facets):
        return None
    if len(left_vertices) > 8:
        raise BPTError("exact BPT-W0 isomorphism recovery is limited to eight vertices")

    for images in permutations(right_vertices):
        mapping = dict(zip(left_vertices, images))
        mapped = {
            tuple(sorted(mapping[v] for v in facet))
            for facet in left_facets
        }
        if mapped == right_facets:
            return tuple(sorted(mapping.items()))
    return None


def isomorphic(left: SimplicialComplex, right: SimplicialComplex) -> bool:
    if len(left.vertices) != len(right.vertices):
        return False
    if len(_tetrahedra(left)) != len(_tetrahedra(right)):
        return False
    return canonical_tetrahedral_signature(left) == canonical_tetrahedral_signature(right)


def verify_path(public: BPTWeakPublic, path: tuple[BPTMove, ...]) -> bool:
    if len(path) > public.move_bound:
        return False
    try:
        final = apply_path(public.source, path)
    except (BPTError, ValueError):
        return False
    return isomorphic(final, public.target)


def _digest_index(seed: bytes, domain: bytes, step: int, modulus: int) -> int:
    if modulus <= 0:
        raise BPTError("empty public move choice")
    digest = hashlib.sha256(domain + b"\x00" + seed + step.to_bytes(4, "big")).digest()
    return int.from_bytes(digest[:8], "big") % modulus


def _stacked_sphere(depth: int, seed: bytes, domain: bytes) -> tuple[SimplicialComplex, tuple[BPTMove, ...]]:
    current = boundary_of_4_simplex()
    history: list[BPTMove] = []
    for step in range(depth):
        facets = _tetrahedra(current)
        chosen = facets[_digest_index(seed, domain, step, len(facets))]
        new_vertex = 5 + step
        move = BPTMove("1-4", chosen, new_vertex)
        current = apply_move(current, move)
        history.append(move)
    return current, tuple(history)


def generate_bpt_weak_instance(
    params: BPTWeakParameters,
    master_seed: bytes,
) -> tuple[BPTWeakPublic, BPTWeakReference]:
    params.validate()
    if len(master_seed) < 16:
        raise BPTError("BPT-W0 master seed must contain at least 128 bits")

    source, source_history = _stacked_sphere(
        params.stack_depth, master_seed, b"MORPH-KEM BPT-W0 source v1"
    )

    retries = 0
    while True:
        target_domain = b"MORPH-KEM BPT-W0 target v1" + retries.to_bytes(2, "big")
        target, target_history = _stacked_sphere(params.stack_depth, master_seed, target_domain)
        if target != source:
            break
        retries += 1
        if retries > 64:
            raise BPTError("failed to generate distinct weak-control endpoints")

    planted = tuple(inverse_move(move) for move in reversed(source_history)) + target_history
    public = BPTWeakPublic(params.name, source, target, 2 * params.stack_depth)
    if not verify_path(public, planted):
        raise BPTError("generated planted BPT-W0 path failed public verification")
    return public, BPTWeakReference(planted, retries)


@lru_cache(maxsize=4096)
def _count_simplification_paths(complex_: SimplicialComplex) -> int:
    base = boundary_of_4_simplex()
    if isomorphic(complex_, base):
        return 1
    legal = legal_four_one_moves(complex_)
    if not legal:
        return 0
    total = 0
    for move in legal:
        total += _count_simplification_paths(apply_move(complex_, move))
        if total >= 1_000_000:
            return 1_000_000
    return total


def _relabel_move(move: BPTMove, mapping: dict[int, int]) -> BPTMove:
    try:
        tetrahedron = tuple(sorted(mapping[v] for v in move.tetrahedron))
        vertex = mapping[move.vertex]
    except KeyError as exc:
        raise BPTError("incomplete BPT-W0 transport isomorphism") from exc
    return BPTMove(move.kind, tetrahedron, vertex)  # type: ignore[arg-type]


def _extend_root_isomorphism(
    public_target: SimplicialComplex,
    target_root: SimplicialComplex,
    source_root: SimplicialComplex,
) -> dict[int, int] | None:
    recovered = recover_tetrahedral_isomorphism(target_root, source_root)
    if recovered is None:
        return None
    mapping = dict(recovered)
    used = set(source_root.vertices)
    fresh = 0
    removed_target_vertices = sorted(set(public_target.vertices) - set(target_root.vertices))
    for vertex in removed_target_vertices:
        while fresh in used:
            fresh += 1
        mapping[vertex] = fresh
        used.add(fresh)
        fresh += 1
    return mapping


def recover_bpt_weak(
    public: BPTWeakPublic,
    *,
    reference: BPTWeakReference | None = None,
) -> BPTWeakRecovery:
    source = greedy_simplify(public.source)
    target = greedy_simplify(public.target)

    common_exact = source.root == target.root
    common_iso = isomorphic(source.root, target.root)
    source_paths = _count_simplification_paths(public.source)
    target_paths = _count_simplification_paths(public.target)

    transport = _extend_root_isomorphism(public.target, target.root, source.root)
    if transport is None:
        return BPTWeakRecovery(
            False,
            (),
            0,
            len(source.moves),
            len(target.moves),
            source.vertex_scans,
            target.vertex_scans,
            source.legal_moves_seen,
            target.legal_moves_seen,
            common_exact,
            common_iso,
            source_paths,
            target_paths,
            0,
            None,
        )

    transported_target_reverse = tuple(
        _relabel_move(inverse_move(move), transport)
        for move in reversed(target.moves)
    )
    recovered = source.moves + transported_target_reverse
    accepted = verify_path(public, recovered)
    multiplicity = min(1_000_000, source_paths * target_paths)
    matches = None
    if accepted and reference is not None:
        matches = recovered == reference.planted_path

    return BPTWeakRecovery(
        accepted,
        recovered,
        len(recovered),
        len(source.moves),
        len(target.moves),
        source.vertex_scans,
        target.vertex_scans,
        source.legal_moves_seen,
        target.legal_moves_seen,
        common_exact,
        common_iso,
        source_paths,
        target_paths,
        multiplicity,
        matches,
    )
