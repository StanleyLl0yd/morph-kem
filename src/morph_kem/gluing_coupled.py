from __future__ import annotations

from dataclasses import dataclass
import hashlib

from .gluing import DualEdge, GluingExperimentError, TetrahedronGroup, _normalize_groups
from .gluing_matching import (
    G3_PARAMETER_SETS,
    MatchingGluingReference,
    generate_matching_gluing_instance,
    recover_matching_gluing,
    validate_matching_gluing_witness,
)


@dataclass(frozen=True, slots=True)
class CoupledPhaseParameters:
    name: str
    gadget_count: int
    coupling_edges: tuple[DualEdge, ...]

    def validate(self) -> None:
        if self.gadget_count < 2 or self.gadget_count > 32:
            raise GluingExperimentError("G4 gadget count outside toy bounds")
        adjacency = [set() for _ in range(self.gadget_count)]
        seen_edges: set[DualEdge] = set()
        for left, right in self.coupling_edges:
            if left == right or not (0 <= left < self.gadget_count) or not (0 <= right < self.gadget_count):
                raise GluingExperimentError("G4 coupling edge endpoint outside gadget range")
            edge = tuple(sorted((left, right)))
            if edge in seen_edges:
                raise GluingExperimentError("duplicate G4 coupling edge")
            seen_edges.add(edge)
            adjacency[left].add(right)
            adjacency[right].add(left)

        reached = {0}
        stack = [0]
        while stack:
            vertex = stack.pop()
            for neighbor in adjacency[vertex]:
                if neighbor not in reached:
                    reached.add(neighbor)
                    stack.append(neighbor)
        if len(reached) != self.gadget_count:
            raise GluingExperimentError("G4 coupling graph must be connected")


def _cube_edges() -> tuple[DualEdge, ...]:
    edges: list[DualEdge] = []
    for vertex in range(8):
        for bit in (1, 2, 4):
            neighbor = vertex ^ bit
            if vertex < neighbor:
                edges.append((vertex, neighbor))
    return tuple(edges)


def _hexagonal_prism_edges() -> tuple[DualEdge, ...]:
    edges: set[DualEdge] = set()
    for layer in (0, 6):
        for index in range(6):
            left = layer + index
            right = layer + ((index + 1) % 6)
            edges.add(tuple(sorted((left, right))))
    for index in range(6):
        edges.add((index, index + 6))
    return tuple(sorted(edges))


G4_PARAMETER_SETS = {
    "g4-4": CoupledPhaseParameters(
        "g4-4",
        4,
        tuple((left, right) for left in range(4) for right in range(left + 1, 4)),
    ),
    "g4-8": CoupledPhaseParameters("g4-8", 8, _cube_edges()),
    "g4-12": CoupledPhaseParameters("g4-12", 12, _hexagonal_prism_edges()),
}


@dataclass(frozen=True, slots=True)
class PhaseConstraint:
    left: int
    right: int
    parity: int


@dataclass(frozen=True, slots=True)
class CoupledPhasePublicInstance:
    name: str
    gadgets: tuple[object, ...]
    constraints: tuple[PhaseConstraint, ...]


@dataclass(frozen=True, slots=True)
class CoupledPhaseReference:
    phases: tuple[int, ...]
    groups: tuple[tuple[TetrahedronGroup, ...], ...]


@dataclass(frozen=True, slots=True)
class CoupledPhaseValidation:
    valid: bool
    reason: str
    phases: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class CoupledPhaseRecovery:
    recovered_groups: tuple[tuple[tuple[TetrahedronGroup, ...], ...], ...]
    recovered_phases: tuple[tuple[int, ...], ...]
    gadget_count: int
    total_tetrahedra: int
    coupling_edges: int
    coupling_cycle_rank: int
    gadget_matching_solutions: tuple[int, ...]
    gadget_matching_nodes: int
    gadget_matching_backtracks: int
    xor_equations: int
    xor_variables: int
    gf2_rank: int
    gf2_nullity: int
    gf2_row_xors: int
    propagation_tree_assignments: int
    propagation_constraint_checks: int
    phase_solutions: int
    accepted_solutions: int
    nonreference_accepted_solutions: int


def _canonical_gadget_matchings(gadget: object) -> tuple[
    tuple[tuple[TetrahedronGroup, ...], tuple[TetrahedronGroup, ...]], int, int
]:
    recovery = recover_matching_gluing(gadget)  # type: ignore[arg-type]
    if recovery.matching_cap_hit or recovery.accepted_solutions != 2:
        raise GluingExperimentError("G4 local gadget does not expose exactly two public phases")
    ordered = tuple(sorted(recovery.accepted_groups))
    if len(ordered) != 2 or ordered[0] == ordered[1]:
        raise GluingExperimentError("G4 local gadget phase canonicalization failed")
    return (ordered[0], ordered[1]), recovery.matching_nodes, recovery.matching_backtracks


def _phase_for_groups(
    gadget: object,
    groups: tuple[TetrahedronGroup, ...],
) -> int | None:
    canonical, _, _ = _canonical_gadget_matchings(gadget)
    normalized = _normalize_groups(groups)
    if normalized == canonical[0]:
        return 0
    if normalized == canonical[1]:
        return 1
    return None


def validate_coupled_phase_witness(
    public: CoupledPhasePublicInstance,
    groups_by_gadget: tuple[tuple[TetrahedronGroup, ...], ...],
) -> CoupledPhaseValidation:
    if len(groups_by_gadget) != len(public.gadgets):
        return CoupledPhaseValidation(False, "wrong G4 gadget witness count", ())

    phases: list[int] = []
    for gadget, groups in zip(public.gadgets, groups_by_gadget, strict=True):
        if not validate_matching_gluing_witness(gadget, groups).valid:  # type: ignore[arg-type]
            return CoupledPhaseValidation(False, "invalid local G3 matching witness", ())
        phase = _phase_for_groups(gadget, groups)
        if phase is None:
            return CoupledPhaseValidation(False, "local witness is not a canonical G4 phase", ())
        phases.append(phase)

    phase_tuple = tuple(phases)
    for constraint in public.constraints:
        if constraint.parity not in (0, 1):
            return CoupledPhaseValidation(False, "invalid public G4 parity", phase_tuple)
        if phase_tuple[constraint.left] ^ phase_tuple[constraint.right] != constraint.parity:
            return CoupledPhaseValidation(False, "G4 coupling constraint violated", phase_tuple)

    return CoupledPhaseValidation(True, "accepted", phase_tuple)


def _gf2_rank_and_work(
    variable_count: int,
    constraints: tuple[PhaseConstraint, ...],
) -> tuple[int, int, bool]:
    rows = [
        [(1 << constraint.left) | (1 << constraint.right), constraint.parity]
        for constraint in constraints
    ]
    pivot_row = 0
    row_xors = 0

    for column in range(variable_count):
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
        pivot_row += 1
        if pivot_row == len(rows):
            break

    consistent = all(mask != 0 or rhs == 0 for mask, rhs in rows)
    return pivot_row, row_xors, consistent


def _propagate_phases(
    variable_count: int,
    constraints: tuple[PhaseConstraint, ...],
    root_bit: int,
) -> tuple[tuple[int, ...], int, int]:
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(variable_count)]
    for constraint in constraints:
        adjacency[constraint.left].append((constraint.right, constraint.parity))
        adjacency[constraint.right].append((constraint.left, constraint.parity))
    for neighbors in adjacency:
        neighbors.sort()

    values: list[int | None] = [None] * variable_count
    values[0] = root_bit
    stack = [0]
    assignments = 0
    while stack:
        current = stack.pop()
        current_value = values[current]
        assert current_value is not None
        for neighbor, parity in adjacency[current]:
            expected = current_value ^ parity
            if values[neighbor] is None:
                values[neighbor] = expected
                assignments += 1
                stack.append(neighbor)
            elif values[neighbor] != expected:
                raise GluingExperimentError("public G4 XOR constraints are inconsistent")

    if any(value is None for value in values):
        raise GluingExperimentError("public G4 coupling graph is disconnected")
    phase_tuple = tuple(int(value) for value in values)
    checks = 0
    for constraint in constraints:
        checks += 1
        if phase_tuple[constraint.left] ^ phase_tuple[constraint.right] != constraint.parity:
            raise GluingExperimentError("public G4 phase propagation failed a cycle constraint")
    return phase_tuple, assignments, checks


def recover_coupled_phases(
    public: CoupledPhasePublicInstance,
    *,
    reference: CoupledPhaseReference | None = None,
) -> CoupledPhaseRecovery:
    gadget_phases: list[tuple[tuple[TetrahedronGroup, ...], tuple[TetrahedronGroup, ...]]] = []
    matching_solutions: list[int] = []
    matching_nodes = 0
    matching_backtracks = 0
    total_tetrahedra = 0

    for gadget in public.gadgets:
        canonical, nodes, backtracks = _canonical_gadget_matchings(gadget)
        gadget_phases.append(canonical)
        matching_solutions.append(2)
        matching_nodes += nodes
        matching_backtracks += backtracks
        total_tetrahedra += len(gadget.tetrahedra)  # type: ignore[attr-defined]

    variable_count = len(public.gadgets)
    rank, row_xors, consistent = _gf2_rank_and_work(variable_count, public.constraints)
    if not consistent:
        raise GluingExperimentError("public G4 GF(2) system is inconsistent")
    nullity = variable_count - rank

    recovered_phases: list[tuple[int, ...]] = []
    recovered_groups: list[tuple[tuple[TetrahedronGroup, ...], ...]] = []
    total_assignments = 0
    total_checks = 0
    for root_bit in (0, 1):
        phases, assignments, checks = _propagate_phases(
            variable_count, public.constraints, root_bit
        )
        total_assignments += assignments
        total_checks += checks
        groups = tuple(
            gadget_phases[index][phase]
            for index, phase in enumerate(phases)
        )
        recovered_phases.append(phases)
        recovered_groups.append(groups)

    accepted = sum(
        validate_coupled_phase_witness(public, groups).valid
        for groups in recovered_groups
    )
    nonreference = 0
    if reference is not None:
        reference_groups = tuple(_normalize_groups(groups) for groups in reference.groups)
        nonreference = sum(
            tuple(_normalize_groups(groups) for groups in recovered) != reference_groups
            for recovered in recovered_groups
            if validate_coupled_phase_witness(public, recovered).valid
        )

    edge_count = len(public.constraints)
    cycle_rank = edge_count - variable_count + 1
    return CoupledPhaseRecovery(
        recovered_groups=tuple(recovered_groups),
        recovered_phases=tuple(recovered_phases),
        gadget_count=variable_count,
        total_tetrahedra=total_tetrahedra,
        coupling_edges=edge_count,
        coupling_cycle_rank=cycle_rank,
        gadget_matching_solutions=tuple(matching_solutions),
        gadget_matching_nodes=matching_nodes,
        gadget_matching_backtracks=matching_backtracks,
        xor_equations=edge_count,
        xor_variables=variable_count,
        gf2_rank=rank,
        gf2_nullity=nullity,
        gf2_row_xors=row_xors,
        propagation_tree_assignments=total_assignments,
        propagation_constraint_checks=total_checks,
        phase_solutions=len(recovered_phases),
        accepted_solutions=accepted,
        nonreference_accepted_solutions=nonreference,
    )


def generate_coupled_phase_instance(
    params: CoupledPhaseParameters,
    master_seed: bytes,
) -> tuple[CoupledPhasePublicInstance, CoupledPhaseReference]:
    params.validate()
    if len(master_seed) < 16:
        raise GluingExperimentError("G4 master seed must contain at least 128 bits")

    gadgets = []
    canonical_phases = []
    for gadget_index in range(params.gadget_count):
        gadget_seed = hashlib.sha256(
            b"MORPH-KEM G4 gadget v1\x00"
            + master_seed
            + params.name.encode("ascii")
            + gadget_index.to_bytes(4, "big")
        ).digest()
        gadget, _ = generate_matching_gluing_instance(G3_PARAMETER_SETS["g3-3"], gadget_seed)
        canonical, _, _ = _canonical_gadget_matchings(gadget)
        gadgets.append(gadget)
        canonical_phases.append(canonical)

    phases = tuple(
        hashlib.sha256(
            b"MORPH-KEM G4 hidden phase v1\x00"
            + master_seed
            + params.name.encode("ascii")
            + gadget_index.to_bytes(4, "big")
        ).digest()[0]
        & 1
        for gadget_index in range(params.gadget_count)
    )

    constraints = tuple(
        PhaseConstraint(left, right, phases[left] ^ phases[right])
        for left, right in params.coupling_edges
    )
    reference_groups = tuple(
        canonical_phases[index][phase]
        for index, phase in enumerate(phases)
    )

    public = CoupledPhasePublicInstance(
        name=params.name,
        gadgets=tuple(gadgets),
        constraints=constraints,
    )
    reference = CoupledPhaseReference(phases=phases, groups=reference_groups)

    if not validate_coupled_phase_witness(public, reference.groups).valid:
        raise GluingExperimentError("G4 generated reference witness does not validate")

    return public, reference
