from __future__ import annotations

from collections import Counter, defaultdict, deque
from dataclasses import dataclass
import hashlib
from itertools import combinations

from .complex import SimplicialComplex
from .gluing import GluingExperimentError
from .gluing_irregular_hypercover import (
    _final_relabel,
    _flip_surface,
    _normalization_improving_flip_count,
    _primal_vertex_degree_histogram,
)
from .gluing_surface_hypercover import (
    ToroidalHypercoverPublicInstance,
    toroidal_hypercover_incidence,
)
from .surface import SurfaceParameters, generate_surface_instance


Edge = tuple[int, int]
Triangle = tuple[int, int, int]
CycleWitness = tuple[Edge, ...]


@dataclass(frozen=True, slots=True)
class CohomologyCycleParameters:
    name: str
    rows: int
    cols: int
    successful_flips: int

    def validate(self) -> None:
        if self.rows < 4 or self.rows > 12 or self.cols < 4 or self.cols > 12:
            raise GluingExperimentError("G16 torus dimensions outside toy bounds")
        triangle_count = 2 * self.rows * self.cols
        if self.successful_flips < 1 or self.successful_flips > triangle_count:
            raise GluingExperimentError("G16 successful-flip target outside toy bounds")


G16_PARAMETER_SETS = {
    "g16-6x6": CohomologyCycleParameters("g16-6x6", 6, 6, 36),
    "g16-6x9": CohomologyCycleParameters("g16-6x9", 6, 9, 54),
    "g16-8x9": CohomologyCycleParameters("g16-8x9", 8, 9, 72),
}


@dataclass(frozen=True, slots=True)
class CohomologyCyclePublicInstance:
    name: str
    target: SimplicialComplex
    alpha: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class CohomologyCycleReference:
    cycle: CycleWitness


@dataclass(frozen=True, slots=True)
class CohomologyCycleValidation:
    valid: bool
    reason: str
    cycle_length: int
    pairing: int


@dataclass(frozen=True, slots=True)
class CohomologyCycleRecovery:
    vertices: int
    edges: int
    triangles: int
    euler_characteristic: int
    min_triangles_per_edge: int
    max_triangles_per_edge: int
    successful_flips: int
    primal_vertex_degree_histogram: tuple[tuple[int, int], ...]
    normalization_improving_flips: int
    cycle_equations: int
    cycle_variables: int
    cycle_rank: int
    cycle_nullity: int
    cycle_row_xors: int
    cocycle_equations: int
    cocycle_rank: int
    cocycle_dimension: int
    coboundary_rank: int
    h1_dimension: int
    cocycle_row_xors: int
    alpha_weight: int
    tree_edges: int
    non_tree_edges: int
    fundamental_cycles_tested: int
    fundamental_path_edge_scans: int
    selected_cycle_length: int
    selected_cycle_accepted: bool
    selected_cycle_matches_reference: bool | None
    affine_rank: int
    affine_nullity: int
    affine_row_xors: int
    affine_support_edges: int
    affine_cycles_tested: int
    affine_selected_cycle_length: int
    affine_cycle_accepted: bool


@dataclass(frozen=True, slots=True)
class _Rref:
    rows: tuple[int, ...]
    pivots: tuple[int, ...]
    rank: int
    row_xors: int


@dataclass(frozen=True, slots=True)
class _Tree:
    parent: tuple[int, ...]
    parent_edge: tuple[int, ...]
    depth: tuple[int, ...]
    tree_edges: frozenset[int]


def _edges(target: SimplicialComplex) -> tuple[Edge, ...]:
    return tuple(sorted(simplex for simplex in target.simplices if len(simplex) == 2))


def _triangles(target: SimplicialComplex) -> tuple[Triangle, ...]:
    return tuple(sorted(simplex for simplex in target.simplices if len(simplex) == 3))


def _edge_index(edges: tuple[Edge, ...]) -> dict[Edge, int]:
    return {edge: index for index, edge in enumerate(edges)}


def _rref(rows: list[int], variable_count: int) -> _Rref:
    work = [row for row in rows if row]
    pivot_row = 0
    pivots: list[int] = []
    row_xors = 0
    for column in range(variable_count):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if (work[row] >> column) & 1),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_mask = work[pivot_row]
        for row in range(len(work)):
            if row == pivot_row or not ((work[row] >> column) & 1):
                continue
            work[row] ^= pivot_mask
            row_xors += 1
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break
    return _Rref(tuple(work[:pivot_row]), tuple(pivots), pivot_row, row_xors)


def _nullspace_basis(rref: _Rref, variable_count: int) -> tuple[int, ...]:
    pivot_set = set(rref.pivots)
    basis: list[int] = []
    for free in range(variable_count):
        if free in pivot_set:
            continue
        vector = 1 << free
        for row, pivot in zip(rref.rows, rref.pivots, strict=True):
            if (row >> free) & 1:
                vector |= 1 << pivot
        basis.append(vector)
    return tuple(basis)


def _reduce_by_rowspace(vector: int, rref: _Rref) -> int:
    value = vector
    for row, pivot in zip(rref.rows, rref.pivots, strict=True):
        if (value >> pivot) & 1:
            value ^= row
    return value


def _cochain_metrics(
    target: SimplicialComplex,
) -> tuple[tuple[Edge, ...], int, int, int, int, int, int, int]:
    edges = _edges(target)
    edge_to_index = _edge_index(edges)
    triangles = _triangles(target)
    triangle_rows: list[int] = []
    for triangle in triangles:
        mask = 0
        for edge in combinations(triangle, 2):
            mask ^= 1 << edge_to_index[tuple(sorted(edge))]
        triangle_rows.append(mask)
    cocycle_rref = _rref(triangle_rows, len(edges))
    cocycle_basis = _nullspace_basis(cocycle_rref, len(edges))

    vertex_rows: list[int] = []
    for vertex in target.vertices:
        mask = 0
        for index, edge in enumerate(edges):
            if vertex in edge:
                mask ^= 1 << index
        vertex_rows.append(mask)
    coboundary_rref = _rref(vertex_rows, len(edges))

    candidates = [
        vector
        for vector in cocycle_basis
        if _reduce_by_rowspace(vector, coboundary_rref) != 0
    ]
    if not candidates:
        raise GluingExperimentError("G16 failed to find a nontrivial public cohomology class")
    alpha_mask = min(candidates)
    h1_dimension = len(cocycle_basis) - coboundary_rref.rank
    return (
        edges,
        alpha_mask,
        cocycle_rref.rank,
        len(cocycle_basis),
        coboundary_rref.rank,
        h1_dimension,
        cocycle_rref.row_xors,
        len(triangles),
    )


def _cycle_equation_metrics(
    target: SimplicialComplex,
    edges: tuple[Edge, ...],
) -> tuple[_Rref, tuple[int, ...]]:
    rows: list[int] = []
    for vertex in target.vertices:
        mask = 0
        for index, edge in enumerate(edges):
            if vertex in edge:
                mask ^= 1 << index
        rows.append(mask)
    rref = _rref(rows, len(edges))
    return rref, _nullspace_basis(rref, len(edges))


def _adjacency(
    vertex_count: int,
    edges: tuple[Edge, ...],
    allowed_edges: frozenset[int] | None = None,
) -> list[list[tuple[int, int]]]:
    result: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for index, (left, right) in enumerate(edges):
        if allowed_edges is not None and index not in allowed_edges:
            continue
        result[left].append((right, index))
        result[right].append((left, index))
    for values in result:
        values.sort()
    return result


def _public_spanning_forest(
    vertex_count: int,
    edges: tuple[Edge, ...],
    allowed_edges: frozenset[int] | None = None,
) -> tuple[_Tree, int]:
    adjacency = _adjacency(vertex_count, edges, allowed_edges)
    parent = [-1] * vertex_count
    parent_edge = [-1] * vertex_count
    depth = [0] * vertex_count
    tree_edges: set[int] = set()
    components = 0
    for root in range(vertex_count):
        if parent[root] != -1:
            continue
        if not adjacency[root] and allowed_edges is not None:
            parent[root] = root
            components += 1
            continue
        components += 1
        parent[root] = root
        queue = deque([root])
        while queue:
            current = queue.popleft()
            for neighbor, edge_index in adjacency[current]:
                if parent[neighbor] != -1:
                    continue
                parent[neighbor] = current
                parent_edge[neighbor] = edge_index
                depth[neighbor] = depth[current] + 1
                tree_edges.add(edge_index)
                queue.append(neighbor)
    return (
        _Tree(tuple(parent), tuple(parent_edge), tuple(depth), frozenset(tree_edges)),
        components,
    )


def _tree_path_edges(left: int, right: int, tree: _Tree) -> tuple[int, ...]:
    first = left
    second = right
    path: list[int] = []
    while tree.depth[first] > tree.depth[second]:
        edge = tree.parent_edge[first]
        if edge < 0:
            raise GluingExperimentError("G16 tree path crossed components")
        path.append(edge)
        first = tree.parent[first]
    while tree.depth[second] > tree.depth[first]:
        edge = tree.parent_edge[second]
        if edge < 0:
            raise GluingExperimentError("G16 tree path crossed components")
        path.append(edge)
        second = tree.parent[second]
    while first != second:
        first_edge = tree.parent_edge[first]
        second_edge = tree.parent_edge[second]
        if first_edge < 0 or second_edge < 0:
            raise GluingExperimentError("G16 tree path crossed components")
        path.extend((first_edge, second_edge))
        first = tree.parent[first]
        second = tree.parent[second]
    return tuple(path)


def _pairing(alpha: tuple[int, ...], edge_indices: tuple[int, ...]) -> int:
    value = 0
    for index in edge_indices:
        value ^= alpha[index]
    return value


def _fundamental_odd_cycle(
    vertex_count: int,
    edges: tuple[Edge, ...],
    alpha: tuple[int, ...],
    *,
    allowed_edges: frozenset[int] | None = None,
) -> tuple[tuple[int, ...], int, int, int, int]:
    tree, components = _public_spanning_forest(vertex_count, edges, allowed_edges)
    active = (
        tuple(range(len(edges)))
        if allowed_edges is None
        else tuple(sorted(allowed_edges))
    )
    non_tree = [index for index in active if index not in tree.tree_edges]
    tested = 0
    path_scans = 0
    for edge_index in non_tree:
        left, right = edges[edge_index]
        path = _tree_path_edges(left, right, tree)
        cycle = tuple(sorted(path + (edge_index,)))
        tested += 1
        path_scans += len(path)
        if _pairing(alpha, cycle) == 1:
            return cycle, tested, path_scans, len(tree.tree_edges), components
    raise GluingExperimentError("G16 public cycle basis contains no odd-pairing cycle")


def _witness_from_indices(edges: tuple[Edge, ...], indices: tuple[int, ...]) -> CycleWitness:
    return tuple(sorted(edges[index] for index in indices))


def validate_cohomology_cycle_witness(
    public: CohomologyCyclePublicInstance,
    witness: CycleWitness,
) -> CohomologyCycleValidation:
    edges = _edges(public.target)
    if len(public.alpha) != len(edges) or any(bit not in (0, 1) for bit in public.alpha):
        return CohomologyCycleValidation(False, "malformed public G16 cocycle", 0, 0)
    if len(witness) < 3 or witness != tuple(sorted(witness)) or len(set(witness)) != len(witness):
        return CohomologyCycleValidation(False, "G16 witness is not a canonical simple edge set", len(witness), 0)
    edge_to_index = _edge_index(edges)
    if any(edge not in edge_to_index or edge[0] >= edge[1] for edge in witness):
        return CohomologyCycleValidation(False, "G16 witness contains a non-public edge", len(witness), 0)

    degrees: Counter[int] = Counter()
    adjacency: dict[int, set[int]] = defaultdict(set)
    for left, right in witness:
        degrees[left] += 1
        degrees[right] += 1
        adjacency[left].add(right)
        adjacency[right].add(left)
    if not degrees or any(degree != 2 for degree in degrees.values()):
        return CohomologyCycleValidation(False, "G16 witness is not degree-two", len(witness), 0)
    start = min(degrees)
    seen = {start}
    stack = [start]
    while stack:
        current = stack.pop()
        for neighbor in adjacency[current]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    if len(seen) != len(degrees):
        return CohomologyCycleValidation(False, "G16 witness is disconnected", len(witness), 0)

    pairing = 0
    for edge in witness:
        pairing ^= public.alpha[edge_to_index[edge]]
    if pairing != 1:
        return CohomologyCycleValidation(False, "G16 cocycle pairing is even", len(witness), pairing)
    return CohomologyCycleValidation(True, "accepted", len(witness), pairing)


def _solve_affine_cycle(
    target: SimplicialComplex,
    edges: tuple[Edge, ...],
    alpha_mask: int,
) -> tuple[int, int, int, int]:
    rows: list[list[int]] = []
    for vertex in target.vertices:
        mask = 0
        for index, edge in enumerate(edges):
            if vertex in edge:
                mask ^= 1 << index
        rows.append([mask, 0])
    rows.append([alpha_mask, 1])

    pivot_row = 0
    pivots: list[int] = []
    row_xors = 0
    for column in range(len(edges)):
        pivot = next(
            (row for row in range(pivot_row, len(rows)) if (rows[row][0] >> column) & 1),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        pivot_mask, pivot_rhs = rows[pivot_row]
        for row in range(len(rows)):
            if row == pivot_row or not ((rows[row][0] >> column) & 1):
                continue
            rows[row][0] ^= pivot_mask
            rows[row][1] ^= pivot_rhs
            row_xors += 1
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    if any(mask == 0 and rhs for mask, rhs in rows):
        raise GluingExperimentError("G16 affine cycle equations are inconsistent")
    solution = 0
    for row_index, pivot in enumerate(pivots):
        if rows[row_index][1]:
            solution |= 1 << pivot
    return solution, pivot_row, len(edges) - pivot_row, row_xors


def recover_cohomology_cycle(
    public: CohomologyCyclePublicInstance,
    *,
    reference: CohomologyCycleReference | None = None,
    successful_flips: int = -1,
) -> CohomologyCycleRecovery:
    edges = _edges(public.target)
    triangles = _triangles(public.target)
    if len(public.alpha) != len(edges):
        raise GluingExperimentError("G16 public cocycle length mismatch")
    alpha_mask = sum(bit << index for index, bit in enumerate(public.alpha))

    base = ToroidalHypercoverPublicInstance(public.name, public.target)
    incidence = toroidal_hypercover_incidence(base)
    cycle_rref, _ = _cycle_equation_metrics(public.target, edges)
    (
        _,
        canonical_alpha_mask,
        cocycle_rank,
        cocycle_dimension,
        coboundary_rank,
        h1_dimension,
        cocycle_row_xors,
        cocycle_equations,
    ) = _cochain_metrics(public.target)
    if alpha_mask != canonical_alpha_mask:
        if any(((alpha_mask & sum(1 << _edge_index(edges)[tuple(sorted(edge))] for edge in combinations(triangle, 2))).bit_count() & 1) for triangle in triangles):
            raise GluingExperimentError("G16 public alpha is not a cocycle")
        cob_rows = []
        for vertex in public.target.vertices:
            mask = 0
            for index, edge in enumerate(edges):
                if vertex in edge:
                    mask ^= 1 << index
            cob_rows.append(mask)
        if _reduce_by_rowspace(alpha_mask, _rref(cob_rows, len(edges))) == 0:
            raise GluingExperimentError("G16 public alpha is a coboundary")

    cycle_indices, tested, path_scans, tree_edges, components = _fundamental_odd_cycle(
        len(public.target.vertices), edges, public.alpha
    )
    if components != 1:
        raise GluingExperimentError("G16 public primal graph is disconnected")
    witness = _witness_from_indices(edges, cycle_indices)
    validation = validate_cohomology_cycle_witness(public, witness)
    if not validation.valid:
        raise GluingExperimentError("G16 public fundamental-cycle attack failed exact verifier")

    reference_cycle = reference.cycle if reference is not None else None
    matches_reference = None if reference_cycle is None else witness == reference_cycle

    affine_mask, affine_rank, affine_nullity, affine_row_xors = _solve_affine_cycle(
        public.target, edges, alpha_mask
    )
    affine_support = frozenset(
        index for index in range(len(edges)) if (affine_mask >> index) & 1
    )
    affine_cycle, affine_tested, _, _, _ = _fundamental_odd_cycle(
        len(public.target.vertices), edges, public.alpha, allowed_edges=affine_support
    )
    affine_witness = _witness_from_indices(edges, affine_cycle)
    affine_validation = validate_cohomology_cycle_witness(public, affine_witness)
    if not affine_validation.valid:
        raise GluingExperimentError("G16 affine cross-check failed exact verifier")

    return CohomologyCycleRecovery(
        vertices=incidence.vertices,
        edges=incidence.edges,
        triangles=incidence.triangles,
        euler_characteristic=incidence.euler_characteristic,
        min_triangles_per_edge=incidence.min_triangles_per_edge,
        max_triangles_per_edge=incidence.max_triangles_per_edge,
        successful_flips=successful_flips,
        primal_vertex_degree_histogram=_primal_vertex_degree_histogram(public.target),
        normalization_improving_flips=_normalization_improving_flip_count(public.target),
        cycle_equations=len(public.target.vertices),
        cycle_variables=len(edges),
        cycle_rank=cycle_rref.rank,
        cycle_nullity=len(edges) - cycle_rref.rank,
        cycle_row_xors=cycle_rref.row_xors,
        cocycle_equations=cocycle_equations,
        cocycle_rank=cocycle_rank,
        cocycle_dimension=cocycle_dimension,
        coboundary_rank=coboundary_rank,
        h1_dimension=h1_dimension,
        cocycle_row_xors=cocycle_row_xors,
        alpha_weight=sum(public.alpha),
        tree_edges=tree_edges,
        non_tree_edges=len(edges) - tree_edges,
        fundamental_cycles_tested=tested,
        fundamental_path_edge_scans=path_scans,
        selected_cycle_length=len(witness),
        selected_cycle_accepted=validation.valid,
        selected_cycle_matches_reference=matches_reference,
        affine_rank=affine_rank,
        affine_nullity=affine_nullity,
        affine_row_xors=affine_row_xors,
        affine_support_edges=len(affine_support),
        affine_cycles_tested=affine_tested,
        affine_selected_cycle_length=len(affine_witness),
        affine_cycle_accepted=affine_validation.valid,
    )


def _secret_reference_cycle(
    target: SimplicialComplex,
    edges: tuple[Edge, ...],
    alpha: tuple[int, ...],
    seed: bytes,
) -> CycleWitness:
    vertex_count = len(target.vertices)
    adjacency = _adjacency(vertex_count, edges)
    parent = [-1] * vertex_count
    parent_edge = [-1] * vertex_count
    depth = [0] * vertex_count
    tree_edges: set[int] = set()
    root = int.from_bytes(hashlib.sha256(b"MORPH-KEM G16 reference root v1\x00" + seed).digest()[:8], "big") % vertex_count
    parent[root] = root
    queue = deque([root])
    while queue:
        current = queue.popleft()
        ordered = sorted(
            adjacency[current],
            key=lambda item: (
                hashlib.sha256(
                    b"MORPH-KEM G16 reference tree edge v1\x00"
                    + seed
                    + item[1].to_bytes(4, "big")
                ).digest(),
                item,
            ),
        )
        for neighbor, edge_index in ordered:
            if parent[neighbor] != -1:
                continue
            parent[neighbor] = current
            parent_edge[neighbor] = edge_index
            depth[neighbor] = depth[current] + 1
            tree_edges.add(edge_index)
            queue.append(neighbor)
    if any(value == -1 for value in parent):
        raise GluingExperimentError("G16 reference tree did not span public graph")
    tree = _Tree(tuple(parent), tuple(parent_edge), tuple(depth), frozenset(tree_edges))
    non_tree = [index for index in range(len(edges)) if index not in tree_edges]
    non_tree.sort(
        key=lambda index: hashlib.sha256(
            b"MORPH-KEM G16 reference cycle order v1\x00"
            + seed
            + index.to_bytes(4, "big")
        ).digest()
    )
    for edge_index in non_tree:
        left, right = edges[edge_index]
        cycle = tuple(sorted(_tree_path_edges(left, right, tree) + (edge_index,)))
        if _pairing(alpha, cycle) == 1:
            return _witness_from_indices(edges, cycle)
    raise GluingExperimentError("G16 reference tree exposed no odd cycle")


def generate_cohomology_cycle_instance(
    params: CohomologyCycleParameters,
    master_seed: bytes,
) -> tuple[CohomologyCyclePublicInstance, CohomologyCycleReference]:
    params.validate()
    if len(master_seed) < 16:
        raise GluingExperimentError("G16 master seed must contain at least 128 bits")

    base_seed = hashlib.sha256(
        b"MORPH-KEM G16 base torus v1\x00" + master_seed + params.name.encode("ascii")
    ).digest()
    base_public, _ = generate_surface_instance(
        SurfaceParameters(params.name + "-base", params.rows, params.cols), base_seed
    )
    flip_seed = hashlib.sha256(
        b"MORPH-KEM G16 flips v1\x00" + master_seed + params.name.encode("ascii")
    ).digest()
    target = _flip_surface(base_public.target, params.successful_flips, flip_seed)
    relabel_seed = hashlib.sha256(
        b"MORPH-KEM G16 relabel v1\x00" + master_seed + params.name.encode("ascii")
    ).digest()
    target = _final_relabel(target, relabel_seed)

    edges, alpha_mask, cocycle_rank, cocycle_dimension, coboundary_rank, h1_dimension, _, _ = _cochain_metrics(target)
    if h1_dimension != 2:
        raise GluingExperimentError("G16 torus does not expose measured H^1 dimension two")
    alpha = tuple((alpha_mask >> index) & 1 for index in range(len(edges)))
    if not any(alpha):
        raise GluingExperimentError("G16 selected zero cocycle")
    public = CohomologyCyclePublicInstance(params.name, target, alpha)

    reference_seed = hashlib.sha256(
        b"MORPH-KEM G16 hidden reference v1\x00" + master_seed + params.name.encode("ascii")
    ).digest()
    reference = CohomologyCycleReference(
        _secret_reference_cycle(target, edges, alpha, reference_seed)
    )
    if not validate_cohomology_cycle_witness(public, reference.cycle).valid:
        raise GluingExperimentError("G16 generated reference cycle does not validate")
    if cocycle_dimension - coboundary_rank != 2 or cocycle_rank < 1:
        raise GluingExperimentError("G16 cohomology accounting failed")
    return public, reference
