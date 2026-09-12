from __future__ import annotations

from collections import Counter, defaultdict, deque
from dataclasses import dataclass
import hashlib
from itertools import combinations

from .gluing import _DeterministicRng
from .tdc_cycle_code import _gf2_rank


class TDC2SparseError(ValueError):
    """Raised when a TDC2 sparse-face control is malformed."""


@dataclass(frozen=True, slots=True)
class TDC2SparseParameters:
    name: str
    vertex_count: int
    max_random_attempts: int = 4096

    def validate(self) -> None:
        if self.vertex_count not in (8, 9, 10):
            raise TDC2SparseError("TDC2 sparse vertex count outside declared toy sets")
        if self.max_random_attempts < 1 or self.max_random_attempts > 20000:
            raise TDC2SparseError("TDC2 sparse random-attempt cap outside toy bounds")


TDC2_SPARSE_PARAMETER_SETS = {
    "tdc2b-n8": TDC2SparseParameters("tdc2b-n8", 8),
    "tdc2b-n9": TDC2SparseParameters("tdc2b-n9", 9),
    "tdc2b-n10": TDC2SparseParameters("tdc2b-n10", 10),
}


@dataclass(frozen=True, slots=True)
class SparseFaceCode:
    name: str
    row_count: int
    columns: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class TDC2SparseInstance:
    topology_code: SparseFaceCode
    matched_random: SparseFaceCode
    selected_face_count: int
    skipped_tetrahedron_completions: int
    random_generation_retries: int


@dataclass(frozen=True, slots=True)
class SparseFaceMetrics:
    rows: int
    columns: int
    rank: int
    dimension: int
    rate: float
    row_weight_histogram: tuple[tuple[int, int], ...]
    column_weight_histogram: tuple[tuple[int, int], ...]
    tetrahedron_boundary_count: int
    minimum_weight_leq6: int | None
    minimum_weight_multiplicity: int
    pair_syndrome_collision_buckets: int
    triple_syndrome_collision_buckets: int
    graphic_column_weight_obstruction: bool


def _digest(domain: bytes, seed: bytes, name: str, counter: int = 0) -> bytes:
    return hashlib.sha256(
        domain + b"\x00" + seed + name.encode("ascii") + counter.to_bytes(8, "big")
    ).digest()


def _tanner_connected(code: SparseFaceCode) -> bool:
    row_neighbors: list[list[int]] = [[] for _ in range(code.row_count)]
    col_neighbors: list[list[int]] = [[] for _ in range(len(code.columns))]
    for col_index, mask in enumerate(code.columns):
        for row in range(code.row_count):
            if (mask >> row) & 1:
                row_neighbors[row].append(col_index)
                col_neighbors[col_index].append(row)
    if any(not row for row in row_neighbors):
        return False
    seen_rows = {0}
    seen_cols: set[int] = set()
    queue: deque[tuple[int, int]] = deque([(0, 0)])
    while queue:
        kind, index = queue.popleft()
        if kind == 0:
            for col in row_neighbors[index]:
                if col not in seen_cols:
                    seen_cols.add(col)
                    queue.append((1, col))
        else:
            for row in col_neighbors[index]:
                if row not in seen_rows:
                    seen_rows.add(row)
                    queue.append((0, row))
    return len(seen_rows) == code.row_count and len(seen_cols) == len(code.columns)


def _selected_faces(
    params: TDC2SparseParameters, seed: bytes
) -> tuple[tuple[tuple[int, int, int], ...], int]:
    triangles = tuple(combinations(range(params.vertex_count), 3))
    ordered = sorted(
        triangles,
        key=lambda face: (
            hashlib.sha256(
                b"MORPH-KEM TDC2b face order v1\x00"
                + seed
                + params.name.encode("ascii")
                + bytes(face)
            ).digest(),
            face,
        ),
    )
    selected: set[tuple[int, int, int]] = set()
    skipped = 0
    for face in ordered:
        would_complete = False
        for extra in range(params.vertex_count):
            if extra in face:
                continue
            four = tuple(sorted(face + (extra,)))
            boundary = set(combinations(four, 3))
            if boundary.issubset(selected | {face}):
                would_complete = True
                break
        if would_complete:
            skipped += 1
            continue
        selected.add(face)
    return tuple(sorted(selected)), skipped


def _topology_code(
    params: TDC2SparseParameters, seed: bytes
) -> tuple[SparseFaceCode, int, int]:
    faces, skipped = _selected_faces(params, seed)
    edges = tuple(combinations(range(params.vertex_count), 2))
    edge_index = {edge: index for index, edge in enumerate(edges)}
    raw_columns = tuple(
        sum(1 << edge_index[edge] for edge in combinations(face, 2))
        for face in faces
    )

    row_labels = list(range(len(edges)))
    col_labels = list(range(len(raw_columns)))
    row_rng = _DeterministicRng(
        b"MORPH-KEM TDC2b row relabel v1", _digest(b"rows", seed, params.name)
    )
    col_rng = _DeterministicRng(
        b"MORPH-KEM TDC2b column relabel v1", _digest(b"cols", seed, params.name)
    )
    row_rng.shuffle(row_labels)
    col_rng.shuffle(col_labels)

    columns: list[int] = []
    for old_col in col_labels:
        old_mask = raw_columns[old_col]
        new_mask = 0
        for old_row, new_row in enumerate(row_labels):
            if (old_mask >> old_row) & 1:
                new_mask |= 1 << new_row
        columns.append(new_mask)
    code = SparseFaceCode(params.name + "-topology", len(edges), tuple(columns))
    if not _tanner_connected(code):
        raise TDC2SparseError("TDC2 sparse topology Tanner graph is disconnected")
    return code, len(faces), skipped


def _row_degrees(code: SparseFaceCode) -> tuple[int, ...]:
    values = [0] * code.row_count
    for column in code.columns:
        for row in range(code.row_count):
            values[row] += (column >> row) & 1
    return tuple(values)


def _matched_random(
    params: TDC2SparseParameters,
    seed: bytes,
    row_degrees: tuple[int, ...],
    column_count: int,
) -> tuple[SparseFaceCode, int]:
    if sum(row_degrees) != 3 * column_count:
        raise TDC2SparseError("TDC2 sparse matched-random degree accounting mismatch")
    for attempt in range(params.max_random_attempts):
        stubs = [row for row, degree in enumerate(row_degrees) for _ in range(degree)]
        rng = _DeterministicRng(
            b"MORPH-KEM TDC2b matched random v1",
            _digest(b"random", seed, params.name, attempt),
        )
        rng.shuffle(stubs)
        seen: set[int] = set()
        columns: list[int] = []
        valid = True
        for index in range(column_count):
            rows = stubs[3 * index : 3 * index + 3]
            if len(set(rows)) != 3:
                valid = False
                break
            mask = sum(1 << row for row in rows)
            if mask in seen:
                valid = False
                break
            seen.add(mask)
            columns.append(mask)
        if not valid:
            continue
        code = SparseFaceCode(params.name + "-random", len(row_degrees), tuple(columns))
        if not _tanner_connected(code):
            continue
        return code, attempt
    raise TDC2SparseError("TDC2 sparse matched-random attempt cap exhausted")


def generate_tdc2_sparse_instance(
    params: TDC2SparseParameters, master_seed: bytes
) -> TDC2SparseInstance:
    params.validate()
    if len(master_seed) < 16:
        raise TDC2SparseError("TDC2 sparse seed must contain at least 128 bits")
    topology, face_count, skipped = _topology_code(params, master_seed)
    random_code, retries = _matched_random(
        params,
        master_seed,
        _row_degrees(topology),
        len(topology.columns),
    )
    return TDC2SparseInstance(topology, random_code, face_count, skipped, retries)


def _tetrahedron_boundary_count(
    params: TDC2SparseParameters, seed: bytes
) -> int:
    faces, _ = _selected_faces(params, seed)
    selected = set(faces)
    return sum(
        set(combinations(four, 3)).issubset(selected)
        for four in combinations(range(params.vertex_count), 4)
    )


def _low_weight_leq6(
    columns: tuple[int, ...]
) -> tuple[int | None, int, int, int]:
    if any(column == 0 for column in columns):
        return 1, sum(column == 0 for column in columns), 0, 0
    duplicate_count = len(columns) - len(set(columns))
    if duplicate_count:
        return 2, duplicate_count, 0, 0

    column_set = set(columns)
    weight3: set[tuple[int, int, int]] = set()
    pair_buckets: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for left in range(len(columns)):
        for right in range(left + 1, len(columns)):
            syndrome = columns[left] ^ columns[right]
            if syndrome in column_set:
                third = columns.index(syndrome)
                if third not in (left, right):
                    weight3.add(tuple(sorted((left, right, third))))
            pair_buckets[syndrome].append((left, right))
    if weight3:
        return 3, len(weight3), sum(len(v) > 1 for v in pair_buckets.values()), 0

    weight4: set[tuple[int, int, int, int]] = set()
    for pairs in pair_buckets.values():
        for first in range(len(pairs)):
            for second in range(first + 1, len(pairs)):
                support = set(pairs[first] + pairs[second])
                if len(support) == 4:
                    weight4.add(tuple(sorted(support)))
    pair_collisions = sum(len(v) > 1 for v in pair_buckets.values())
    if weight4:
        return 4, len(weight4), pair_collisions, 0

    triple_buckets: dict[int, list[tuple[int, int, int]]] = defaultdict(list)
    weight5: set[tuple[int, int, int, int, int]] = set()
    for first in range(len(columns)):
        for second in range(first + 1, len(columns)):
            pair_syndrome = columns[first] ^ columns[second]
            for third in range(second + 1, len(columns)):
                syndrome = pair_syndrome ^ columns[third]
                for pair in pair_buckets.get(syndrome, ()):
                    support = {first, second, third, *pair}
                    if len(support) == 5:
                        weight5.add(tuple(sorted(support)))
                triple_buckets[syndrome].append((first, second, third))
    triple_collisions = sum(len(v) > 1 for v in triple_buckets.values())
    if weight5:
        return 5, len(weight5), pair_collisions, triple_collisions

    weight6: set[tuple[int, int, int, int, int, int]] = set()
    for triples in triple_buckets.values():
        for first in range(len(triples)):
            for second in range(first + 1, len(triples)):
                support = set(triples[first] + triples[second])
                if len(support) == 6:
                    weight6.add(tuple(sorted(support)))
    if weight6:
        return 6, len(weight6), pair_collisions, triple_collisions
    return None, 0, pair_collisions, triple_collisions


def sparse_face_metrics(
    code: SparseFaceCode,
    *,
    tetrahedron_boundaries: int = 0,
) -> SparseFaceMetrics:
    rank = _gf2_rank(list(code.columns))
    row_hist = tuple(sorted(Counter(_row_degrees(code)).items()))
    col_hist = tuple(sorted(Counter(column.bit_count() for column in code.columns).items()))
    minimum, multiplicity, pair_collisions, triple_collisions = _low_weight_leq6(
        code.columns
    )
    dimension = len(code.columns) - rank
    return SparseFaceMetrics(
        rows=code.row_count,
        columns=len(code.columns),
        rank=rank,
        dimension=dimension,
        rate=dimension / len(code.columns),
        row_weight_histogram=row_hist,
        column_weight_histogram=col_hist,
        tetrahedron_boundary_count=tetrahedron_boundaries,
        minimum_weight_leq6=minimum,
        minimum_weight_multiplicity=multiplicity,
        pair_syndrome_collision_buckets=pair_collisions,
        triple_syndrome_collision_buckets=triple_collisions,
        graphic_column_weight_obstruction=any(weight != 2 for weight, _ in col_hist),
    )


def topology_sparse_face_metrics(
    params: TDC2SparseParameters,
    master_seed: bytes,
    code: SparseFaceCode,
) -> SparseFaceMetrics:
    return sparse_face_metrics(
        code,
        tetrahedron_boundaries=_tetrahedron_boundary_count(params, master_seed),
    )
