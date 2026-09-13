from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
from itertools import combinations

from .gluing import _DeterministicRng
from .tdc_sparse_faces import (
    SparseFaceCode,
    TDC2SparseParameters,
    TDC2_SPARSE_PARAMETER_SETS,
    generate_tdc2_sparse_instance,
)


class TDC2CLiftError(ValueError):
    """Raised when a TDC2c cyclic Tanner-lift control is malformed."""


@dataclass(frozen=True, slots=True)
class TDC2CLiftParameters:
    name: str
    base_name: str
    lift_degree: int

    def validate(self) -> None:
        if self.base_name not in TDC2_SPARSE_PARAMETER_SETS:
            raise TDC2CLiftError("unknown TDC2b base parameter set")
        if self.lift_degree not in (2, 3, 4):
            raise TDC2CLiftError("TDC2c lift degree outside declared toy values")


TDC2C_LIFT_PARAMETER_SETS = {
    "tdc2c-n8-L2": TDC2CLiftParameters("tdc2c-n8-L2", "tdc2b-n8", 2),
    "tdc2c-n9-L3": TDC2CLiftParameters("tdc2c-n9-L3", "tdc2b-n9", 3),
    "tdc2c-n10-L4": TDC2CLiftParameters("tdc2c-n10-L4", "tdc2b-n10", 4),
}


@dataclass(frozen=True, slots=True)
class TDC2CLiftInstance:
    topology: SparseFaceCode
    matched_random: SparseFaceCode
    lift_degree: int
    base_topology_rows: int
    base_topology_columns: int
    base_random_rows: int
    base_random_columns: int


@dataclass(frozen=True, slots=True)
class QuotientRecovery:
    stabilized_rounds: int
    color_class_histogram: tuple[tuple[int, int], ...]
    row_class_count: int
    column_class_count: int
    exact_fiber_partition: bool
    quotient_valid: bool
    quotient: SparseFaceCode | None
    quotient_column_classes: tuple[tuple[int, ...], ...]
    quotient_kernel_support: tuple[int, ...]
    quotient_kernel_weight: int | None
    lifted_kernel_weight: int | None
    lifted_kernel_verified: bool


@dataclass(frozen=True, slots=True)
class TDC2CLiftRecovery:
    topology: QuotientRecovery
    matched_random: QuotientRecovery


def _digest(domain: bytes, seed: bytes, name: str, counter: int = 0) -> bytes:
    return hashlib.sha256(
        domain + b"\x00" + seed + name.encode("ascii") + counter.to_bytes(8, "big")
    ).digest()


def _row_degrees(code: SparseFaceCode) -> tuple[int, ...]:
    values = [0] * code.row_count
    for column in code.columns:
        for row in range(code.row_count):
            values[row] += (column >> row) & 1
    return tuple(values)


def _cyclic_lift(
    code: SparseFaceCode,
    lift_degree: int,
    seed: bytes,
    domain: bytes,
    name: str,
) -> SparseFaceCode:
    lifted_rows = code.row_count * lift_degree
    lifted_columns: list[int] = [0] * (len(code.columns) * lift_degree)

    for base_col, mask in enumerate(code.columns):
        for base_row in range(code.row_count):
            if not ((mask >> base_row) & 1):
                continue
            shift = int.from_bytes(
                _digest(domain + b" shift", seed, name, base_col * code.row_count + base_row)[:8],
                "big",
            ) % lift_degree
            for sheet in range(lift_degree):
                public_row = base_row * lift_degree + ((sheet + shift) % lift_degree)
                lifted_col = base_col * lift_degree + sheet
                lifted_columns[lifted_col] |= 1 << public_row

    row_order = list(range(lifted_rows))
    col_order = list(range(len(lifted_columns)))
    row_rng = _DeterministicRng(domain + b" row relabel", _digest(domain + b" rows", seed, name))
    col_rng = _DeterministicRng(domain + b" col relabel", _digest(domain + b" cols", seed, name))
    row_rng.shuffle(row_order)
    col_rng.shuffle(col_order)

    relabeled: list[int] = []
    for old_col in col_order:
        old_mask = lifted_columns[old_col]
        new_mask = 0
        for old_row, new_row in enumerate(row_order):
            if (old_mask >> old_row) & 1:
                new_mask |= 1 << new_row
        relabeled.append(new_mask)

    return SparseFaceCode(name, lifted_rows, tuple(relabeled))


def generate_tdc2c_lift_instance(
    params: TDC2CLiftParameters,
    master_seed: bytes,
) -> TDC2CLiftInstance:
    params.validate()
    if len(master_seed) < 16:
        raise TDC2CLiftError("TDC2c seed must contain at least 128 bits")
    base_params = TDC2_SPARSE_PARAMETER_SETS[params.base_name]
    base = generate_tdc2_sparse_instance(base_params, master_seed)
    topology = _cyclic_lift(
        base.topology_code,
        params.lift_degree,
        master_seed,
        b"MORPH-KEM TDC2c topology lift v1",
        params.name + "-topology",
    )
    random = _cyclic_lift(
        base.matched_random,
        params.lift_degree,
        master_seed,
        b"MORPH-KEM TDC2c random lift v1",
        params.name + "-random",
    )
    return TDC2CLiftInstance(
        topology,
        random,
        params.lift_degree,
        base.topology_code.row_count,
        len(base.topology_code.columns),
        base.matched_random.row_count,
        len(base.matched_random.columns),
    )


def _adjacency(code: SparseFaceCode) -> tuple[tuple[int, ...], ...]:
    total = code.row_count + len(code.columns)
    values: list[list[int]] = [[] for _ in range(total)]
    for col, mask in enumerate(code.columns):
        node = code.row_count + col
        for row in range(code.row_count):
            if (mask >> row) & 1:
                values[row].append(node)
                values[node].append(row)
    return tuple(tuple(sorted(neighbors)) for neighbors in values)


def _color_refinement(
    code: SparseFaceCode,
) -> tuple[tuple[int, ...], int, tuple[tuple[int, int], ...]]:
    adjacency = _adjacency(code)
    colors = tuple(
        (0 if node < code.row_count else 1, len(adjacency[node]))
        for node in range(len(adjacency))
    )
    palette = {signature: index for index, signature in enumerate(sorted(set(colors)))}
    current = tuple(palette[value] for value in colors)
    rounds = 0
    while True:
        signatures = tuple(
            (current[node], tuple(sorted(current[neighbor] for neighbor in adjacency[node])))
            for node in range(len(adjacency))
        )
        unique = {value: index for index, value in enumerate(sorted(set(signatures)))}
        refined = tuple(unique[value] for value in signatures)
        rounds += 1
        if refined == current:
            histogram = tuple(sorted(Counter(Counter(refined).values()).items()))
            return refined, rounds, histogram
        current = refined
        if rounds > len(adjacency):
            raise TDC2CLiftError("TDC2c color refinement failed to stabilize")


def _first_kernel_support_leq6(columns: tuple[int, ...]) -> tuple[int, ...]:
    for index, value in enumerate(columns):
        if value == 0:
            return (index,)
    seen_single: dict[int, int] = {}
    for index, value in enumerate(columns):
        if value in seen_single:
            return (seen_single[value], index)
        seen_single[value] = index

    pair_buckets: dict[int, list[tuple[int, int]]] = defaultdict(list)
    value_to_indices: dict[int, list[int]] = defaultdict(list)
    for index, value in enumerate(columns):
        value_to_indices[value].append(index)
    for left in range(len(columns)):
        for right in range(left + 1, len(columns)):
            syndrome = columns[left] ^ columns[right]
            for third in value_to_indices.get(syndrome, ()):
                if third not in (left, right):
                    return tuple(sorted((left, right, third)))
            pair_buckets[syndrome].append((left, right))
    for pairs in pair_buckets.values():
        for first, second in combinations(pairs, 2):
            support = tuple(sorted(set(first + second)))
            if len(support) == 4:
                return support

    triple_buckets: dict[int, list[tuple[int, int, int]]] = defaultdict(list)
    for first in range(len(columns)):
        for second in range(first + 1, len(columns)):
            partial = columns[first] ^ columns[second]
            for third in range(second + 1, len(columns)):
                syndrome = partial ^ columns[third]
                for pair in pair_buckets.get(syndrome, ()):
                    support = tuple(sorted({first, second, third, *pair}))
                    if len(support) == 5:
                        return support
                triple_buckets[syndrome].append((first, second, third))
    for triples in triple_buckets.values():
        for first, second in combinations(triples, 2):
            support = tuple(sorted(set(first + second)))
            if len(support) == 6:
                return support
    return ()


def _recover_quotient(code: SparseFaceCode, lift_degree: int) -> QuotientRecovery:
    colors, rounds, histogram = _color_refinement(code)
    classes: dict[int, list[int]] = defaultdict(list)
    for node, color in enumerate(colors):
        classes[color].append(node)

    row_classes = [
        tuple(nodes)
        for nodes in classes.values()
        if nodes and all(node < code.row_count for node in nodes)
    ]
    column_classes_nodes = [
        tuple(node - code.row_count for node in nodes)
        for nodes in classes.values()
        if nodes and all(node >= code.row_count for node in nodes)
    ]
    mixed_class = any(
        any(node < code.row_count for node in nodes)
        and any(node >= code.row_count for node in nodes)
        for nodes in classes.values()
    )
    exact = (
        not mixed_class
        and all(len(nodes) == lift_degree for nodes in row_classes)
        and all(len(nodes) == lift_degree for nodes in column_classes_nodes)
        and len(row_classes) * lift_degree == code.row_count
        and len(column_classes_nodes) * lift_degree == len(code.columns)
    )
    if not exact:
        return QuotientRecovery(
            rounds,
            histogram,
            len(row_classes),
            len(column_classes_nodes),
            False,
            False,
            None,
            tuple(sorted(column_classes_nodes)),
            (),
            None,
            None,
            False,
        )

    row_classes = sorted(row_classes, key=min)
    column_classes_nodes = sorted(column_classes_nodes, key=min)
    row_role: dict[int, int] = {
        node: role for role, nodes in enumerate(row_classes) for node in nodes
    }
    quotient_columns: list[int] = []
    quotient_valid = True
    for col_class in column_classes_nodes:
        role_sets = []
        for col in col_class:
            roles = {
                row_role[row]
                for row in range(code.row_count)
                if (code.columns[col] >> row) & 1
            }
            role_sets.append(roles)
        if not role_sets or any(roles != role_sets[0] for roles in role_sets[1:]):
            quotient_valid = False
            break
        if len(role_sets[0]) != 3:
            quotient_valid = False
            break
        for role in role_sets[0]:
            rows = set(row_classes[role])
            incidence_count = sum(
                1
                for col in col_class
                for row in rows
                if (code.columns[col] >> row) & 1
            )
            if incidence_count != lift_degree:
                quotient_valid = False
                break
        if not quotient_valid:
            break
        quotient_columns.append(sum(1 << role for role in role_sets[0]))

    if not quotient_valid:
        return QuotientRecovery(
            rounds,
            histogram,
            len(row_classes),
            len(column_classes_nodes),
            True,
            False,
            None,
            tuple(column_classes_nodes),
            (),
            None,
            None,
            False,
        )

    quotient = SparseFaceCode("public-color-quotient", len(row_classes), tuple(quotient_columns))
    support = _first_kernel_support_leq6(quotient.columns)
    lifted_columns = tuple(
        col
        for quotient_col in support
        for col in column_classes_nodes[quotient_col]
    )
    syndrome = 0
    for col in lifted_columns:
        syndrome ^= code.columns[col]
    lifted_verified = bool(support) and syndrome == 0
    return QuotientRecovery(
        rounds,
        histogram,
        len(row_classes),
        len(column_classes_nodes),
        True,
        True,
        quotient,
        tuple(column_classes_nodes),
        support,
        len(support) if support else None,
        len(lifted_columns) if support else None,
        lifted_verified,
    )


def recover_tdc2c_lift(instance: TDC2CLiftInstance) -> TDC2CLiftRecovery:
    return TDC2CLiftRecovery(
        topology=_recover_quotient(instance.topology, instance.lift_degree),
        matched_random=_recover_quotient(instance.matched_random, instance.lift_degree),
    )
