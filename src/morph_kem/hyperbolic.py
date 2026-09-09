from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import permutations
import hashlib
import json
from statistics import mean

from .complex import SimplicialComplex

Permutation = tuple[int, ...]
Edge = tuple[int, int]


class HyperbolicExperimentError(ValueError):
    """Raised when an H2 Klein-quartic/A5 experiment input is invalid."""


@dataclass(frozen=True, slots=True)
class KleinQuartic:
    complex: SimplicialComplex
    vertices: tuple[int, ...]
    edges: tuple[Edge, ...]
    faces: tuple[tuple[int, int, int], ...]
    vertex_degrees: tuple[int, ...]
    edge_face_degrees: tuple[int, ...]
    group_order: int
    r_order: int
    s_order: int
    t_order: int
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise HyperbolicExperimentError("unsupported Klein-quartic scaffold version")
        if len(self.vertices) != 24:
            raise HyperbolicExperimentError("Klein quartic must have 24 vertices")
        if len(self.edges) != 84:
            raise HyperbolicExperimentError("Klein quartic must have 84 edges")
        if len(self.faces) != 56:
            raise HyperbolicExperimentError("Klein quartic must have 56 triangular faces")
        if self.group_order != 168:
            raise HyperbolicExperimentError("Klein quartic rotational group must have order 168")
        if (self.r_order, self.s_order, self.t_order) != (2, 3, 7):
            raise HyperbolicExperimentError("triangle generators must have orders 2,3,7")
        if any(degree != 7 for degree in self.vertex_degrees):
            raise HyperbolicExperimentError("every Klein vertex must have degree 7")
        if any(degree != 2 for degree in self.edge_face_degrees):
            raise HyperbolicExperimentError("every Klein edge must lie in exactly two faces")
        if self.euler_characteristic != -4:
            raise HyperbolicExperimentError("Klein quartic Euler characteristic must be -4")
        if self.genus != 3:
            raise HyperbolicExperimentError("Klein quartic orientable genus must be 3")

    @property
    def euler_characteristic(self) -> int:
        return len(self.vertices) - len(self.edges) + len(self.faces)

    @property
    def genus(self) -> int:
        return (2 - self.euler_characteristic) // 2

    def encode(self) -> bytes:
        payload = {
            "edges": [list(edge) for edge in self.edges],
            "faces": [list(face) for face in self.faces],
            "group_order": self.group_order,
            "triangle_orders": [self.r_order, self.s_order, self.t_order],
            "version": self.version,
            "vertices": list(self.vertices),
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


@dataclass(frozen=True, slots=True)
class A5PublicInstance:
    scaffold: KleinQuartic
    edge_labels: tuple[int, ...]
    conjugacy_class: tuple[int, ...]
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise HyperbolicExperimentError("unsupported H2 A5 instance version")
        if len(self.edge_labels) != len(self.scaffold.edges):
            raise HyperbolicExperimentError("A5 label count does not match Klein edges")
        if any(label < 0 or label >= len(A5_ELEMENTS) for label in self.edge_labels):
            raise HyperbolicExperimentError("invalid A5 edge label")
        if not self.conjugacy_class:
            raise HyperbolicExperimentError("A5 public conjugacy class must be non-empty")
        if any(value < 0 or value >= len(A5_ELEMENTS) for value in self.conjugacy_class):
            raise HyperbolicExperimentError("invalid A5 conjugacy-class element")

    def encode(self) -> bytes:
        payload = {
            "conjugacy_class": list(self.conjugacy_class),
            "edge_labels": list(self.edge_labels),
            "scaffold": json.loads(self.scaffold.encode().decode("ascii")),
            "version": self.version,
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


@dataclass(frozen=True, slots=True)
class A5Reference:
    frames: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class A5Validation:
    accepted: bool
    failed_edge: Edge | None


@dataclass(frozen=True, slots=True)
class A5GroupAudit:
    order: int
    conjugacy_class_size: int
    conjugacy_class_order: int
    commutator_subgroup_size: int
    generated_by_class_size: int


@dataclass(frozen=True, slots=True)
class A5LocalSearchResult:
    accepted: bool
    frames: tuple[int, ...] | None
    restarts_used: int
    sweeps_used: int
    moves: int
    best_violations: int


@dataclass(frozen=True, slots=True)
class A5CspResult:
    accepted: bool
    first_solution: tuple[int, ...] | None
    solutions_found: int
    nodes: int
    backtracks: int
    arc_revisions: int
    initial_mean_domain: float
    final_first_solution: bool
    hit_solution_cap: bool


class _DeterministicRng:
    def __init__(self, seed: bytes):
        self._seed = seed
        self._counter = 0

    def _block(self) -> bytes:
        block = hashlib.sha256(
            b"MORPH-KEM H2 deterministic rng v1\x00"
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


def _compose(after: Permutation, before: Permutation) -> Permutation:
    if len(after) != len(before):
        raise HyperbolicExperimentError("permutation size mismatch")
    return tuple(after[before[index]] for index in range(len(before)))


def _inverse(permutation: Permutation) -> Permutation:
    result = [0] * len(permutation)
    for source, target in enumerate(permutation):
        result[target] = source
    return tuple(result)


def _identity(size: int) -> Permutation:
    return tuple(range(size))


def _perm_order(permutation: Permutation) -> int:
    current = _identity(len(permutation))
    for order in range(1, 10_000):
        current = _compose(permutation, current)
        if current == _identity(len(permutation)):
            return order
    raise HyperbolicExperimentError("permutation order bound exceeded")


def _generated_subgroup(generators: tuple[Permutation, ...]) -> frozenset[Permutation]:
    if not generators:
        raise HyperbolicExperimentError("at least one subgroup generator is required")
    identity = _identity(len(generators[0]))
    seen = {identity}
    queue = [identity]
    closure_generators = generators + tuple(_inverse(value) for value in generators)
    while queue:
        current = queue.pop()
        for generator in closure_generators:
            candidate = _compose(generator, current)
            if candidate not in seen:
                seen.add(candidate)
                queue.append(candidate)
    return frozenset(seen)


def _gf2_rank3(columns: tuple[int, int, int]) -> bool:
    span = {0}
    for column in columns:
        span |= {value ^ column for value in tuple(span)}
    return len(span) == 8


def _linear_permutation(columns: tuple[int, int, int]) -> Permutation:
    result: list[int] = []
    for encoded in range(1, 8):
        value = 0
        if encoded & 1:
            value ^= columns[0]
        if encoded & 2:
            value ^= columns[1]
        if encoded & 4:
            value ^= columns[2]
        if value == 0:
            raise HyperbolicExperimentError("singular GF(2) matrix produced zero image")
        result.append(value - 1)
    return tuple(result)


@lru_cache(maxsize=1)
def gl32_group() -> tuple[Permutation, ...]:
    elements = {
        _linear_permutation(columns)
        for columns in permutations(range(1, 8), 3)
        if _gf2_rank3(columns)
    }
    result = tuple(sorted(elements))
    if len(result) != 168:
        raise HyperbolicExperimentError("GL(3,2) enumeration did not produce 168 elements")
    return result


@lru_cache(maxsize=1)
def klein_triangle_generators() -> tuple[Permutation, Permutation, Permutation]:
    group = gl32_group()
    order2 = tuple(value for value in group if _perm_order(value) == 2)
    order3 = tuple(value for value in group if _perm_order(value) == 3)

    for r in order2:
        for s in order3:
            t = _inverse(_compose(r, s))
            if _perm_order(t) != 7:
                continue
            if len(_generated_subgroup((r, s))) != 168:
                continue
            return r, s, t
    raise HyperbolicExperimentError("could not find deterministic (2,3,7) generators")


def _cyclic_subgroup(generator: Permutation) -> frozenset[Permutation]:
    identity = _identity(len(generator))
    values = {identity}
    current = identity
    while True:
        current = _compose(current, generator)
        if current == identity:
            break
        values.add(current)
    return frozenset(values)


def _left_coset(element: Permutation, subgroup: frozenset[Permutation]) -> frozenset[Permutation]:
    return frozenset(_compose(element, value) for value in subgroup)


def _coset_partition(
    group: tuple[Permutation, ...],
    subgroup: frozenset[Permutation],
) -> tuple[frozenset[Permutation], ...]:
    unseen = set(group)
    cosets: list[frozenset[Permutation]] = []
    while unseen:
        representative = min(unseen)
        coset = _left_coset(representative, subgroup)
        cosets.append(coset)
        unseen -= set(coset)
    cosets.sort(key=lambda item: min(item))
    return tuple(cosets)


@lru_cache(maxsize=1)
def generate_klein_quartic() -> KleinQuartic:
    group = gl32_group()
    r, s, t = klein_triangle_generators()

    vertex_cosets = _coset_partition(group, _cyclic_subgroup(t))
    edge_cosets = _coset_partition(group, _cyclic_subgroup(r))
    face_cosets = _coset_partition(group, _cyclic_subgroup(s))

    vertex_of = {element: index for index, coset in enumerate(vertex_cosets) for element in coset}
    edge_of = {element: index for index, coset in enumerate(edge_cosets) for element in coset}
    face_of = {element: index for index, coset in enumerate(face_cosets) for element in coset}

    face_vertices: list[set[int]] = [set() for _ in face_cosets]
    edge_vertices: list[set[int]] = [set() for _ in edge_cosets]
    edge_faces: list[set[int]] = [set() for _ in edge_cosets]

    for element in group:
        vertex = vertex_of[element]
        edge = edge_of[element]
        face = face_of[element]
        face_vertices[face].add(vertex)
        edge_vertices[edge].add(vertex)
        edge_faces[edge].add(face)

    if any(len(values) != 3 for values in face_vertices):
        raise HyperbolicExperimentError("Klein face does not have exactly three vertices")
    if any(len(values) != 2 for values in edge_vertices):
        raise HyperbolicExperimentError("Klein edge does not have exactly two vertices")
    if any(len(values) != 2 for values in edge_faces):
        raise HyperbolicExperimentError("Klein edge does not have exactly two incident faces")

    faces = tuple(sorted(tuple(sorted(values)) for values in face_vertices))
    edges = tuple(sorted(tuple(sorted(values)) for values in edge_vertices))
    if len(set(edges)) != len(edges):
        raise HyperbolicExperimentError("Klein quotient produced duplicate edges")
    if len(set(faces)) != len(faces):
        raise HyperbolicExperimentError("Klein quotient produced duplicate faces")

    degree = [0] * len(vertex_cosets)
    for left, right in edges:
        degree[left] += 1
        degree[right] += 1

    complex_ = SimplicialComplex.from_facets(faces)
    complex_edges = tuple(simplex for simplex in complex_.simplices if len(simplex) == 2)
    complex_faces = tuple(simplex for simplex in complex_.simplices if len(simplex) == 3)
    if complex_edges != edges or complex_faces != faces:
        raise HyperbolicExperimentError("Klein incidence disagrees with simplicial closure")

    return KleinQuartic(
        complex=complex_,
        vertices=tuple(range(len(vertex_cosets))),
        edges=edges,
        faces=faces,
        vertex_degrees=tuple(degree),
        edge_face_degrees=tuple(len(values) for values in edge_faces),
        group_order=len(group),
        r_order=_perm_order(r),
        s_order=_perm_order(s),
        t_order=_perm_order(t),
    )


def _parity(permutation: Permutation) -> int:
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return inversions & 1


A5_ELEMENTS: tuple[Permutation, ...] = tuple(
    value for value in permutations(range(5))
    if _parity(value) == 0
)
A5_INDEX = {value: index for index, value in enumerate(A5_ELEMENTS)}
A5_IDENTITY = A5_INDEX[_identity(5)]


def _a5_mul(left: int, right: int) -> int:
    return A5_INDEX[_compose(A5_ELEMENTS[left], A5_ELEMENTS[right])]


def _a5_inv(element: int) -> int:
    return A5_INDEX[_inverse(A5_ELEMENTS[element])]


def _a5_order(element: int) -> int:
    return _perm_order(A5_ELEMENTS[element])


A5_THREE_CYCLES: tuple[int, ...] = tuple(
    index for index in range(len(A5_ELEMENTS))
    if _a5_order(index) == 3
)
_A5_THREE_CYCLE_SET = set(A5_THREE_CYCLES)


def _a5_generated(indices: set[int]) -> set[int]:
    generators = tuple(A5_ELEMENTS[index] for index in sorted(indices))
    subgroup = _generated_subgroup(generators)
    return {A5_INDEX[value] for value in subgroup}


@lru_cache(maxsize=1)
def audit_a5() -> A5GroupAudit:
    if len(A5_ELEMENTS) != 60:
        raise HyperbolicExperimentError("A5 enumeration did not produce 60 elements")
    if len(A5_THREE_CYCLES) != 20:
        raise HyperbolicExperimentError("A5 3-cycle class must have size 20")

    commutators: set[int] = set()
    for left in range(len(A5_ELEMENTS)):
        for right in range(len(A5_ELEMENTS)):
            commutator = _a5_mul(
                _a5_mul(_a5_mul(left, right), _a5_inv(left)),
                _a5_inv(right),
            )
            commutators.add(commutator)

    return A5GroupAudit(
        order=len(A5_ELEMENTS),
        conjugacy_class_size=len(A5_THREE_CYCLES),
        conjugacy_class_order=3,
        commutator_subgroup_size=len(_a5_generated(commutators)),
        generated_by_class_size=len(_a5_generated(set(A5_THREE_CYCLES))),
    )


def _normalized_a5(frame_left: int, edge_label: int, frame_right: int) -> int:
    return _a5_mul(
        frame_right,
        _a5_mul(edge_label, _a5_inv(frame_left)),
    )


def generate_a5_instance(master_seed: bytes) -> tuple[A5PublicInstance, A5Reference]:
    if not isinstance(master_seed, bytes) or not master_seed:
        raise HyperbolicExperimentError("master_seed must be non-empty bytes")

    scaffold = generate_klein_quartic()
    rng = _DeterministicRng(hashlib.sha256(b"MORPH-KEM H2 A5 generator v1\x00" + master_seed).digest())
    frames = tuple(rng.randbelow(len(A5_ELEMENTS)) for _ in scaffold.vertices)

    labels: list[int] = []
    for left, right in scaffold.edges:
        canonical = A5_THREE_CYCLES[rng.randbelow(len(A5_THREE_CYCLES))]
        label = _a5_mul(
            _a5_inv(frames[right]),
            _a5_mul(canonical, frames[left]),
        )
        labels.append(label)

    public = A5PublicInstance(scaffold, tuple(labels), A5_THREE_CYCLES)
    reference = A5Reference(frames)
    if not validate_a5_frames(public, reference.frames).accepted:
        raise HyperbolicExperimentError("internal A5 reference validation failed")
    return public, reference


def validate_a5_frames(public: A5PublicInstance, frames: tuple[int, ...]) -> A5Validation:
    if len(frames) != len(public.scaffold.vertices):
        return A5Validation(False, None)
    if any(value < 0 or value >= len(A5_ELEMENTS) for value in frames):
        return A5Validation(False, None)

    allowed = set(public.conjugacy_class)
    for edge, label in zip(public.scaffold.edges, public.edge_labels):
        left, right = edge
        normalized = _normalized_a5(frames[left], label, frames[right])
        if normalized not in allowed:
            return A5Validation(False, edge)
    return A5Validation(True, None)


def _allowed_right_values(label: int, left_frame: int, conjugacy_class: tuple[int, ...]) -> frozenset[int]:
    label_inverse = _a5_inv(label)
    return frozenset(
        _a5_mul(canonical, _a5_mul(left_frame, label_inverse))
        for canonical in conjugacy_class
    )


def a5_violation_count(
    public: A5PublicInstance,
    frames: tuple[int, ...] | list[int],
) -> int:
    allowed = set(public.conjugacy_class)
    violations = 0
    for edge, label in zip(public.scaffold.edges, public.edge_labels):
        left, right = edge
        if _normalized_a5(frames[left], label, frames[right]) not in allowed:
            violations += 1
    return violations


def recover_a5_min_conflicts(
    public: A5PublicInstance,
    restarts: int = 32,
    max_sweeps: int = 200,
    attack_seed: bytes = b"H2-A5-min-conflicts",
) -> A5LocalSearchResult:
    if restarts <= 0 or restarts > 10_000:
        raise HyperbolicExperimentError("restarts must be in [1, 10000]")
    if max_sweeps <= 0 or max_sweeps > 100_000:
        raise HyperbolicExperimentError("max_sweeps must be in [1, 100000]")
    if not attack_seed:
        raise HyperbolicExperimentError("attack_seed must be non-empty bytes")

    rng = _DeterministicRng(
        hashlib.sha256(
            b"MORPH-KEM H2 A5 min-conflicts v1\x00" + attack_seed
        ).digest()
    )
    incident: list[list[tuple[int, Edge, int]]] = [
        [] for _ in public.scaffold.vertices
    ]
    for index, (edge, label) in enumerate(
        zip(public.scaffold.edges, public.edge_labels)
    ):
        left, right = edge
        incident[left].append((index, edge, label))
        incident[right].append((index, edge, label))

    compatibility_cache: dict[tuple[int, int], int] = {}

    def right_mask(label: int, left_value: int) -> int:
        key = (label, left_value)
        cached = compatibility_cache.get(key)
        if cached is None:
            mask = 0
            for value in _allowed_right_values(
                label,
                left_value,
                public.conjugacy_class,
            ):
                mask |= 1 << value
            cached = mask
            compatibility_cache[key] = cached
        return cached

    best_violations = len(public.scaffold.edges)
    best_frames: tuple[int, ...] | None = None
    total_moves = 0
    total_sweeps = 0

    def local_cost(vertex: int, candidate: int, frames: list[int]) -> int:
        cost = 0
        for _, edge, label in incident[vertex]:
            left, right = edge
            if vertex == left:
                valid = (right_mask(label, candidate) >> frames[right]) & 1
            else:
                valid = (right_mask(label, frames[left]) >> candidate) & 1
            if not valid:
                cost += 1
        return cost

    for restart in range(1, restarts + 1):
        if restart == 1:
            frames = [A5_IDENTITY] * len(public.scaffold.vertices)
        else:
            frames = [A5_IDENTITY] + [
                rng.randbelow(len(A5_ELEMENTS))
                for _ in range(len(public.scaffold.vertices) - 1)
            ]

        for sweep in range(1, max_sweeps + 1):
            total_sweeps += 1
            current_violations = a5_violation_count(public, frames)
            if current_violations < best_violations:
                best_violations = current_violations
                best_frames = tuple(frames)
            if current_violations == 0:
                candidate = tuple(frames)
                return A5LocalSearchResult(
                    True,
                    candidate,
                    restart,
                    total_sweeps,
                    total_moves,
                    0,
                )

            order = list(range(1, len(frames)))
            for index in range(len(order) - 1, 0, -1):
                other = rng.randbelow(index + 1)
                order[index], order[other] = order[other], order[index]

            for vertex in order:
                scored: list[tuple[int, int]] = []
                best_local = len(incident[vertex]) + 1
                for value in range(len(A5_ELEMENTS)):
                    cost = local_cost(vertex, value, frames)
                    if cost < best_local:
                        best_local = cost
                        scored = [(cost, value)]
                    elif cost == best_local:
                        scored.append((cost, value))

                chosen = scored[rng.randbelow(len(scored))][1]
                if chosen != frames[vertex]:
                    frames[vertex] = chosen
                    total_moves += 1

            # Deterministic small kick to escape plateaus.
            if sweep % 16 == 0:
                vertex = 1 + rng.randbelow(len(frames) - 1)
                frames[vertex] = rng.randbelow(len(A5_ELEMENTS))
                total_moves += 1

        final_violations = a5_violation_count(public, frames)
        if final_violations < best_violations:
            best_violations = final_violations
            best_frames = tuple(frames)
        if final_violations == 0:
            candidate = tuple(frames)
            return A5LocalSearchResult(
                True,
                candidate,
                restart,
                total_sweeps,
                total_moves,
                0,
            )

    return A5LocalSearchResult(
        False,
        best_frames,
        restarts,
        total_sweeps,
        total_moves,
        best_violations,
    )


def solve_a5_csp(
    public: A5PublicInstance,
    solution_cap: int = 16,
    max_nodes: int = 2_000_000,
    preferred_frames: tuple[int, ...] | None = None,
) -> A5CspResult:
    if solution_cap <= 0 or solution_cap > 10_000:
        raise HyperbolicExperimentError("solution_cap must be in [1, 10000]")
    if max_nodes <= 0 or max_nodes > 50_000_000:
        raise HyperbolicExperimentError("max_nodes must be in [1, 50000000]")

    vertex_count = len(public.scaffold.vertices)
    group_size = len(A5_ELEMENTS)
    if preferred_frames is not None:
        if len(preferred_frames) != vertex_count:
            raise HyperbolicExperimentError("preferred frame count does not match vertices")
        if any(value < 0 or value >= group_size for value in preferred_frames):
            raise HyperbolicExperimentError("preferred frame outside A5")
    full_mask = (1 << group_size) - 1
    domains: list[int] = [full_mask] * vertex_count
    domains[0] = 1 << A5_IDENTITY

    edge_labels = {
        edge: label
        for edge, label in zip(public.scaffold.edges, public.edge_labels)
    }
    incident: list[list[Edge]] = [[] for _ in range(vertex_count)]
    for edge in public.scaffold.edges:
        left, right = edge
        incident[left].append(edge)
        incident[right].append(edge)

    compatibility_cache: dict[tuple[int, int], int] = {}
    reverse_compatibility_cache: dict[tuple[int, int], int] = {}

    def compatible_mask(label: int, left_value: int) -> int:
        key = (label, left_value)
        cached = compatibility_cache.get(key)
        if cached is None:
            mask = 0
            for value in _allowed_right_values(
                label,
                left_value,
                public.conjugacy_class,
            ):
                mask |= 1 << value
            cached = mask
            compatibility_cache[key] = cached
        return cached

    def reverse_compatible_mask(label: int, right_value: int) -> int:
        key = (label, right_value)
        cached = reverse_compatibility_cache.get(key)
        if cached is None:
            mask = 0
            for left_value in range(group_size):
                if compatible_mask(label, left_value) & (1 << right_value):
                    mask |= 1 << left_value
            cached = mask
            reverse_compatibility_cache[key] = cached
        return cached

    def values(mask: int):
        while mask:
            bit = mask & -mask
            yield bit.bit_length() - 1, bit
            mask ^= bit

    nodes = 0
    backtracks = 0
    arc_revisions = 0
    solutions: list[tuple[int, ...]] = []
    hit_cap = False
    initial_mean = mean(mask.bit_count() for mask in domains)

    def prune(current: list[int]) -> bool:
        nonlocal arc_revisions
        changed = True
        while changed:
            changed = False
            for edge in public.scaffold.edges:
                left, right = edge
                label = edge_labels[edge]
                left_mask = current[left]
                right_mask = current[right]

                allowed_left = 0
                for left_value, left_bit in values(left_mask):
                    if compatible_mask(label, left_value) & right_mask:
                        allowed_left |= left_bit
                if allowed_left == 0:
                    return False
                if allowed_left != left_mask:
                    current[left] = allowed_left
                    left_mask = allowed_left
                    changed = True
                    arc_revisions += 1

                allowed_right_union = 0
                for left_value, _ in values(left_mask):
                    allowed_right_union |= compatible_mask(label, left_value)
                allowed_right = right_mask & allowed_right_union
                if allowed_right == 0:
                    return False
                if allowed_right != right_mask:
                    current[right] = allowed_right
                    changed = True
                    arc_revisions += 1
        return True

    def search(current: list[int]) -> None:
        nonlocal nodes, backtracks, hit_cap
        if len(solutions) >= solution_cap:
            hit_cap = True
            return
        if nodes >= max_nodes:
            return

        if not prune(current):
            backtracks += 1
            return

        unresolved = [
            vertex
            for vertex, mask in enumerate(current)
            if mask.bit_count() > 1
        ]
        if not unresolved:
            candidate = tuple(
                (mask & -mask).bit_length() - 1
                for mask in current
            )
            if validate_a5_frames(public, candidate).accepted:
                solutions.append(candidate)
            else:
                backtracks += 1
            return

        vertex = min(
            unresolved,
            key=lambda item: (
                current[item].bit_count(),
                -len(incident[item]),
                item,
            ),
        )
        scored_values: list[tuple[int, int, int]] = []
        preferred = preferred_frames[vertex] if preferred_frames is not None else None
        for value, bit in values(current[vertex]):
            support = 0
            for edge in incident[vertex]:
                left, right = edge
                label = edge_labels[edge]
                if vertex == left:
                    support += (
                        compatible_mask(label, value) & current[right]
                    ).bit_count()
                else:
                    support += (
                        reverse_compatible_mask(label, value) & current[left]
                    ).bit_count()
            preferred_rank = 0 if preferred is not None and value == preferred else 1
            scored_values.append((preferred_rank, -support, bit))

        scored_values.sort()
        before = len(solutions)
        for _, _, bit in scored_values:
            if len(solutions) >= solution_cap:
                hit_cap = True
                return
            if nodes >= max_nodes:
                return
            nodes += 1
            child = current.copy()
            child[vertex] = bit
            search(child)

        if len(solutions) == before:
            backtracks += 1

    search(domains.copy())
    first = solutions[0] if solutions else None
    accepted = first is not None and validate_a5_frames(public, first).accepted
    return A5CspResult(
        accepted=accepted,
        first_solution=first,
        solutions_found=len(solutions),
        nodes=nodes,
        backtracks=backtracks,
        arc_revisions=arc_revisions,
        initial_mean_domain=initial_mean,
        final_first_solution=accepted,
        hit_solution_cap=hit_cap,
    )
