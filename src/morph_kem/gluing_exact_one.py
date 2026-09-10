from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib

from .gluing import (
    GluingExperimentError,
    GluingPublicInstance,
    TetrahedronGroup,
    _normalize_groups,
)
from .gluing_matching import (
    G3_PARAMETER_SETS,
    generate_matching_gluing_instance,
    recover_matching_gluing,
    validate_matching_gluing_witness,
)


@dataclass(frozen=True, slots=True)
class ExactOneParameters:
    name: str
    gadget_count: int

    def validate(self) -> None:
        if self.gadget_count not in (12, 18, 24):
            raise GluingExperimentError("G5 gadget count outside declared toy sets")


G5_PARAMETER_SETS = {
    "g5-12": ExactOneParameters("g5-12", 12),
    "g5-18": ExactOneParameters("g5-18", 18),
    "g5-24": ExactOneParameters("g5-24", 24),
}


@dataclass(frozen=True, slots=True)
class ExactOneClause:
    variables: tuple[int, int, int]
    negations: tuple[int, int, int]


@dataclass(frozen=True, slots=True)
class ExactOnePublicInstance:
    name: str
    gadgets: tuple[GluingPublicInstance, ...]
    clauses: tuple[ExactOneClause, ...]


@dataclass(frozen=True, slots=True)
class ExactOneReference:
    phases: tuple[int, ...]
    groups: tuple[tuple[TetrahedronGroup, ...], ...]


@dataclass(frozen=True, slots=True)
class ExactOneValidation:
    valid: bool
    reason: str
    phases: tuple[int, ...]
    clause_checks: int


@dataclass(frozen=True, slots=True)
class ExactOneRecovery:
    recovered_groups: tuple[tuple[TetrahedronGroup, ...], ...]
    recovered_phases: tuple[int, ...]
    gadget_count: int
    total_tetrahedra: int
    clause_count: int
    variable_degree_histogram: tuple[tuple[int, int], ...]
    factor_components: int
    factor_cycle_rank: int
    gadget_matching_solutions: tuple[int, ...]
    gadget_matching_nodes: int
    gadget_matching_backtracks: int
    projected_equations: int
    projected_variables: int
    gf2_rank: int
    gf2_nullity: int
    gf2_row_xors: int
    affine_solution_count: int
    nonlinear_clause_checks: int
    accepted: bool
    matches_reference: bool


def _clause_triples(gadget_count: int) -> tuple[tuple[int, int, int], ...]:
    triples = [
        tuple(sorted((index, (index + 1) % gadget_count, (index + 3) % gadget_count)))
        for index in range(gadget_count)
    ]
    triples.extend(
        tuple(sorted((index, (index + 2) % gadget_count, (index + 5) % gadget_count)))
        for index in range(gadget_count)
    )
    result = tuple(triples)
    if len(set(result)) != 2 * gadget_count:
        raise GluingExperimentError("G5 clause template contains duplicates")
    return result


def _clause_is_well_formed(variable_count: int, clause: ExactOneClause) -> bool:
    return (
        len(clause.variables) == 3
        and len(set(clause.variables)) == 3
        and all(0 <= variable < variable_count for variable in clause.variables)
        and len(clause.negations) == 3
        and all(bit in (0, 1) for bit in clause.negations)
    )


def _canonical_gadget_matchings(
    gadget: GluingPublicInstance,
) -> tuple[
    tuple[tuple[TetrahedronGroup, ...], tuple[TetrahedronGroup, ...]],
    int,
    int,
]:
    recovery = recover_matching_gluing(gadget)
    if recovery.matching_cap_hit or recovery.accepted_solutions != 2:
        raise GluingExperimentError("G5 local gadget does not expose exactly two public phases")
    ordered = tuple(sorted(recovery.accepted_groups))
    if len(ordered) != 2 or ordered[0] == ordered[1]:
        raise GluingExperimentError("G5 local phase canonicalization failed")
    return (ordered[0], ordered[1]), recovery.matching_nodes, recovery.matching_backtracks


def _phase_for_groups(
    gadget: GluingPublicInstance,
    groups: tuple[TetrahedronGroup, ...],
) -> int | None:
    canonical, _, _ = _canonical_gadget_matchings(gadget)
    normalized = _normalize_groups(groups)
    if normalized == canonical[0]:
        return 0
    if normalized == canonical[1]:
        return 1
    return None


def validate_exact_one_witness(
    public: ExactOnePublicInstance,
    groups_by_gadget: tuple[tuple[TetrahedronGroup, ...], ...],
) -> ExactOneValidation:
    variable_count = len(public.gadgets)
    if len(groups_by_gadget) != variable_count:
        return ExactOneValidation(False, "wrong G5 gadget witness count", (), 0)

    phases: list[int] = []
    for gadget, groups in zip(public.gadgets, groups_by_gadget, strict=True):
        if not validate_matching_gluing_witness(gadget, groups).valid:
            return ExactOneValidation(False, "invalid local G3 matching witness", (), 0)
        phase = _phase_for_groups(gadget, groups)
        if phase is None:
            return ExactOneValidation(False, "local witness is not a canonical G5 phase", (), 0)
        phases.append(phase)

    phase_tuple = tuple(phases)
    checks = 0
    seen_clauses: set[tuple[tuple[int, int, int], tuple[int, int, int]]] = set()
    for clause in public.clauses:
        if not _clause_is_well_formed(variable_count, clause):
            return ExactOneValidation(False, "malformed public G5 clause", phase_tuple, checks)
        key = (clause.variables, clause.negations)
        if key in seen_clauses:
            return ExactOneValidation(False, "duplicate public G5 clause", phase_tuple, checks)
        seen_clauses.add(key)
        checks += 1
        literal_sum = sum(
            phase_tuple[variable] ^ negation
            for variable, negation in zip(clause.variables, clause.negations, strict=True)
        )
        if literal_sum != 1:
            return ExactOneValidation(False, "G5 exact-one clause violated", phase_tuple, checks)

    return ExactOneValidation(True, "accepted", phase_tuple, checks)


def _factor_metrics(
    variable_count: int,
    clauses: tuple[ExactOneClause, ...],
) -> tuple[tuple[tuple[int, int], ...], int, int]:
    degrees = Counter(variable for clause in clauses for variable in clause.variables)
    histogram = tuple(sorted(Counter(degrees.get(index, 0) for index in range(variable_count)).items()))

    clause_count = len(clauses)
    total_vertices = variable_count + clause_count
    adjacency = [set() for _ in range(total_vertices)]
    incidence_edges = 0
    for clause_index, clause in enumerate(clauses):
        clause_vertex = variable_count + clause_index
        for variable in clause.variables:
            adjacency[variable].add(clause_vertex)
            adjacency[clause_vertex].add(variable)
            incidence_edges += 1

    components = 0
    seen: set[int] = set()
    for start in range(total_vertices):
        if start in seen:
            continue
        components += 1
        seen.add(start)
        stack = [start]
        while stack:
            current = stack.pop()
            for neighbor in adjacency[current]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)

    cycle_rank = incidence_edges - total_vertices + components
    return histogram, components, cycle_rank


def _solve_projected_gf2(
    variable_count: int,
    clauses: tuple[ExactOneClause, ...],
) -> tuple[tuple[int, ...], int, int, int, bool]:
    rows: list[list[int]] = []
    for clause in clauses:
        mask = 0
        for variable in clause.variables:
            mask ^= 1 << variable
        rhs = 1
        for negation in clause.negations:
            rhs ^= negation
        rows.append([mask, rhs])

    pivot_columns: list[int] = []
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
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break

    consistent = all(mask != 0 or rhs == 0 for mask, rhs in rows)
    if not consistent:
        return (), pivot_row, variable_count - pivot_row, row_xors, False

    solution = [0] * variable_count
    for row_index, column in enumerate(pivot_columns):
        solution[column] = rows[row_index][1]
    return tuple(solution), pivot_row, variable_count - pivot_row, row_xors, True


def recover_exact_one_via_parity(
    public: ExactOnePublicInstance,
    *,
    reference: ExactOneReference | None = None,
) -> ExactOneRecovery:
    variable_count = len(public.gadgets)
    if variable_count < 1:
        raise GluingExperimentError("public G5 instance has no gadgets")
    if not public.clauses:
        raise GluingExperimentError("public G5 instance has no clauses")
    if any(not _clause_is_well_formed(variable_count, clause) for clause in public.clauses):
        raise GluingExperimentError("malformed public G5 clause")
    if len({(clause.variables, clause.negations) for clause in public.clauses}) != len(public.clauses):
        raise GluingExperimentError("duplicate public G5 clause")

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
        total_tetrahedra += len(gadget.tetrahedra)

    degree_histogram, components, factor_cycle_rank = _factor_metrics(
        variable_count, public.clauses
    )
    phases, rank, nullity, row_xors, consistent = _solve_projected_gf2(
        variable_count, public.clauses
    )
    if not consistent:
        raise GluingExperimentError("public G5 parity projection is inconsistent")

    groups: tuple[tuple[TetrahedronGroup, ...], ...] = ()
    validation = ExactOneValidation(False, "non-unique affine projection", phases, 0)
    if nullity == 0:
        groups = tuple(
            gadget_phases[index][phase]
            for index, phase in enumerate(phases)
        )
        validation = validate_exact_one_witness(public, groups)

    matches_reference = reference is not None and phases == reference.phases
    return ExactOneRecovery(
        recovered_groups=groups,
        recovered_phases=phases,
        gadget_count=variable_count,
        total_tetrahedra=total_tetrahedra,
        clause_count=len(public.clauses),
        variable_degree_histogram=degree_histogram,
        factor_components=components,
        factor_cycle_rank=factor_cycle_rank,
        gadget_matching_solutions=tuple(matching_solutions),
        gadget_matching_nodes=matching_nodes,
        gadget_matching_backtracks=matching_backtracks,
        projected_equations=len(public.clauses),
        projected_variables=variable_count,
        gf2_rank=rank,
        gf2_nullity=nullity,
        gf2_row_xors=row_xors,
        affine_solution_count=1 << nullity,
        nonlinear_clause_checks=validation.clause_checks,
        accepted=validation.valid,
        matches_reference=matches_reference,
    )


def generate_exact_one_instance(
    params: ExactOneParameters,
    master_seed: bytes,
) -> tuple[ExactOnePublicInstance, ExactOneReference]:
    params.validate()
    if len(master_seed) < 16:
        raise GluingExperimentError("G5 master seed must contain at least 128 bits")

    gadgets: list[GluingPublicInstance] = []
    canonical_phases: list[
        tuple[tuple[TetrahedronGroup, ...], tuple[TetrahedronGroup, ...]]
    ] = []
    for gadget_index in range(params.gadget_count):
        gadget_seed = hashlib.sha256(
            b"MORPH-KEM G5 gadget v1\x00"
            + master_seed
            + params.name.encode("ascii")
            + gadget_index.to_bytes(4, "big")
        ).digest()
        gadget, _ = generate_matching_gluing_instance(
            G3_PARAMETER_SETS["g3-3"], gadget_seed
        )
        canonical, _, _ = _canonical_gadget_matchings(gadget)
        gadgets.append(gadget)
        canonical_phases.append(canonical)

    phases = tuple(
        hashlib.sha256(
            b"MORPH-KEM G5 hidden phase v1\x00"
            + master_seed
            + params.name.encode("ascii")
            + index.to_bytes(4, "big")
        ).digest()[0]
        & 1
        for index in range(params.gadget_count)
    )

    clauses: list[ExactOneClause] = []
    for clause_index, variables in enumerate(_clause_triples(params.gadget_count)):
        target = hashlib.sha256(
            b"MORPH-KEM G5 exact-one target v1\x00"
            + master_seed
            + params.name.encode("ascii")
            + clause_index.to_bytes(4, "big")
        ).digest()[0] % 3
        desired = tuple(1 if position == target else 0 for position in range(3))
        negations = tuple(
            phases[variable] ^ desired[position]
            for position, variable in enumerate(variables)
        )
        clauses.append(ExactOneClause(variables=variables, negations=negations))

    reference_groups = tuple(
        canonical_phases[index][phase]
        for index, phase in enumerate(phases)
    )
    public = ExactOnePublicInstance(
        name=params.name,
        gadgets=tuple(gadgets),
        clauses=tuple(clauses),
    )
    reference = ExactOneReference(phases=phases, groups=reference_groups)

    validation = validate_exact_one_witness(public, reference.groups)
    if not validation.valid:
        raise GluingExperimentError("G5 generated reference witness does not validate")
    degree_histogram, components, _ = _factor_metrics(params.gadget_count, public.clauses)
    if degree_histogram != ((6, params.gadget_count),) or components != 1:
        raise GluingExperimentError("G5 clause template failed regular connected controls")

    return public, reference
