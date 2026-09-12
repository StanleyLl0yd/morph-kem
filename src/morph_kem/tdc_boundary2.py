from __future__ import annotations

from collections import Counter, defaultdict, deque
from dataclasses import dataclass
import hashlib
from itertools import combinations
from math import comb

from .gluing import _DeterministicRng
from .tdc_cycle_code import _gf2_rank


class TDC2Error(ValueError):
    """Raised when a TDC2 toy boundary-code experiment is malformed."""


@dataclass(frozen=True, slots=True)
class TDC2Parameters:
    name: str
    vertex_count: int
    max_random_attempts: int = 4096

    def validate(self) -> None:
        if self.vertex_count < 6 or self.vertex_count > 10:
            raise TDC2Error("TDC2 simplex vertex count outside toy bounds")
        if self.max_random_attempts < 1 or self.max_random_attempts > 20000:
            raise TDC2Error("TDC2 random-control attempt cap outside toy bounds")

    @property
    def row_count(self) -> int:
        return comb(self.vertex_count, 2)

    @property
    def column_count(self) -> int:
        return comb(self.vertex_count, 3)

    @property
    def row_weight(self) -> int:
        return self.vertex_count - 2


TDC2_PARAMETER_SETS = {
    "tdc2-n6": TDC2Parameters("tdc2-n6", 6),
    "tdc2-n7": TDC2Parameters("tdc2-n7", 7),
    "tdc2-n8": TDC2Parameters("tdc2-n8", 8),
}


@dataclass(frozen=True, slots=True)
class SparseBinaryCode:
    name: str
    row_count: int
    columns: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class TDC2Instance:
    topology_code: SparseBinaryCode
    matched_random: SparseBinaryCode
    random_generation_retries: int
    expected_tetrahedron_boundaries: int


@dataclass(frozen=True, slots=True)
class BoundaryCodeMetrics:
    rows: int
    columns: int
    rank: int
    dimension: int
    rate: float
    row_weight_histogram: tuple[tuple[int, int], ...]
    column_weight_histogram: tuple[tuple[int, int], ...]
    minimum_weight_leq3: int | None
    weight4_codewords: int
    pair_syndrome_buckets_with_collisions: int
    maximum_pair_syndrome_bucket: int
    graphic_column_weight_obstruction: bool


def _digest(domain: bytes, seed: bytes, name: str, counter: int = 0) -> bytes:
    return hashlib.sha256(
        domain + b"\x00" + seed + name.encode("ascii") + counter.to_bytes(8, "big")
    ).digest()


def _row_histogram(code: SparseBinaryCode) -> tuple[tuple[int, int], ...]:
    weights = [0] * code.row_count
    for column in code.columns:
        for row in range(code.row_count):
            if (column >> row) & 1:
                weights[row] += 1
    return tuple(sorted(Counter(weights).items()))


def _column_histogram(code: SparseBinaryCode) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(column.bit_count() for column in code.columns).items()))


def _tanner_connected(code: SparseBinaryCode) -> bool:
    row_neighbors: list[list[int]] = [[] for _ in range(code.row_count)]
    col_neighbors: list[list[int]] = [[] for _ in range(len(code.columns))]
    for col_index, column in enumerate(code.columns):
        for row in range(code.row_count):
            if (column >> row) & 1:
                row_neighbors[row].append(col_index)
                col_neighbors[col_index].append(row)
    seen_rows = {0}
    seen_cols: set[int] = set()
    queue: deque[tuple[int, int]] = deque([(0, 0)])  # kind 0=row, 1=column
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


def _topology_boundary_code(params: TDC2Parameters, seed: bytes) -> SparseBinaryCode:
    vertices = tuple(range(params.vertex_count))
    edges = tuple(combinations(vertices, 2))
    triangles = tuple(combinations(vertices, 3))
    edge_index = {edge: index for index, edge in enumerate(edges)}
    columns: list[int] = []
    for triangle in triangles:
        mask = 0
        for edge in combinations(triangle, 2):
            mask |= 1 << edge_index[edge]
        columns.append(mask)

    row_labels = list(range(len(edges)))
    col_labels = list(range(len(columns)))
    row_rng = _DeterministicRng(
        b"MORPH-KEM TDC2 row relabel v1", _digest(b"rows", seed, params.name)
    )
    col_rng = _DeterministicRng(
        b"MORPH-KEM TDC2 column relabel v1", _digest(b"cols", seed, params.name)
    )
    row_rng.shuffle(row_labels)
    col_rng.shuffle(col_labels)

    relabelled_columns: list[int] = []
    for old_col in col_labels:
        old_mask = columns[old_col]
        new_mask = 0
        for old_row, new_row in enumerate(row_labels):
            if (old_mask >> old_row) & 1:
                new_mask |= 1 << new_row
        relabelled_columns.append(new_mask)
    code = SparseBinaryCode(params.name + "-boundary2", len(edges), tuple(relabelled_columns))
    if not _tanner_connected(code):
        raise TDC2Error("TDC2 topology Tanner graph unexpectedly disconnected")
    return code


def _matched_random_code(
    params: TDC2Parameters, seed: bytes
) -> tuple[SparseBinaryCode, int]:
    row_count = params.row_count
    column_count = params.column_count
    row_degree = params.row_weight
    total = row_count * row_degree
    if total != 3 * column_count:
        raise TDC2Error("TDC2 degree accounting mismatch")

    for attempt in range(params.max_random_attempts):
        row_stubs = [row for row in range(row_count) for _ in range(row_degree)]
        rng = _DeterministicRng(
            b"MORPH-KEM TDC2 matched random incidence v1",
            _digest(b"random", seed, params.name, attempt),
        )
        rng.shuffle(row_stubs)
        columns: list[int] = []
        valid = True
        seen: set[int] = set()
        for col in range(column_count):
            rows = row_stubs[3 * col : 3 * col + 3]
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
        code = SparseBinaryCode(params.name + "-random", row_count, tuple(columns))
        if not _tanner_connected(code):
            continue
        return code, attempt
    raise TDC2Error("TDC2 matched-random incidence attempt cap exhausted")


def generate_tdc2_instance(params: TDC2Parameters, master_seed: bytes) -> TDC2Instance:
    params.validate()
    if len(master_seed) < 16:
        raise TDC2Error("TDC2 master seed must contain at least 128 bits")
    topology = _topology_boundary_code(params, master_seed)
    random_code, retries = _matched_random_code(params, master_seed)
    return TDC2Instance(
        topology_code=topology,
        matched_random=random_code,
        random_generation_retries=retries,
        expected_tetrahedron_boundaries=comb(params.vertex_count, 4),
    )


def _low_weight_leq3(code: SparseBinaryCode) -> int | None:
    columns = code.columns
    if any(column == 0 for column in columns):
        return 1
    if len(set(columns)) != len(columns):
        return 2
    column_set = set(columns)
    for left in range(len(columns)):
        for right in range(left + 1, len(columns)):
            value = columns[left] ^ columns[right]
            if value in column_set and value not in (columns[left], columns[right]):
                return 3
    return None


def _weight4_codewords(code: SparseBinaryCode) -> tuple[int, int, int]:
    buckets: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for left in range(len(code.columns)):
        for right in range(left + 1, len(code.columns)):
            buckets[code.columns[left] ^ code.columns[right]].append((left, right))

    words: set[tuple[int, int, int, int]] = set()
    collision_buckets = 0
    maximum_bucket = 0
    for pairs in buckets.values():
        maximum_bucket = max(maximum_bucket, len(pairs))
        if len(pairs) < 2:
            continue
        collision_buckets += 1
        for first_index in range(len(pairs)):
            a, b = pairs[first_index]
            for second_index in range(first_index + 1, len(pairs)):
                c, d = pairs[second_index]
                vertices = {a, b, c, d}
                if len(vertices) != 4:
                    continue
                words.add(tuple(sorted(vertices)))
    return len(words), collision_buckets, maximum_bucket


def boundary_code_metrics(code: SparseBinaryCode) -> BoundaryCodeMetrics:
    rank = _gf2_rank(list(code.columns))
    weight4, collision_buckets, maximum_bucket = _weight4_codewords(code)
    dimension = len(code.columns) - rank
    column_hist = _column_histogram(code)
    return BoundaryCodeMetrics(
        rows=code.row_count,
        columns=len(code.columns),
        rank=rank,
        dimension=dimension,
        rate=dimension / len(code.columns),
        row_weight_histogram=_row_histogram(code),
        column_weight_histogram=column_hist,
        minimum_weight_leq3=_low_weight_leq3(code),
        weight4_codewords=weight4,
        pair_syndrome_buckets_with_collisions=collision_buckets,
        maximum_pair_syndrome_bucket=maximum_bucket,
        # A binary graph-incidence representation has every nonzero column of
        # weight exactly two.  Row/column permutations preserve column weight.
        graphic_column_weight_obstruction=any(weight != 2 for weight, _ in column_hist),
    )
