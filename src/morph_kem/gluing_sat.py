from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib
from itertools import product

from .gluing import (
    GluingExperimentError,
    GluingPublicInstance,
    TetrahedronGroup,
    _normalize_groups,
)
from .gluing_exact_one import _canonical_gadget_matchings
from .gluing_matching import (
    G3_PARAMETER_SETS,
    generate_matching_gluing_instance,
    validate_matching_gluing_witness,
)


@dataclass(frozen=True, slots=True)
class SatPhaseParameters:
    name: str
    gadget_count: int

    def validate(self) -> None:
        if self.gadget_count not in (12, 18, 24):
            raise GluingExperimentError("G7 gadget count outside declared toy sets")


G7_PARAMETER_SETS = {
    "g7-12": SatPhaseParameters("g7-12", 12),
    "g7-18": SatPhaseParameters("g7-18", 18),
    "g7-24": SatPhaseParameters("g7-24", 24),
}


@dataclass(frozen=True, slots=True)
class SatClause:
    variables: tuple[int, int, int]
    negations: tuple[int, int, int]


@dataclass(frozen=True, slots=True)
class SatPublicInstance:
    name: str
    gadgets: tuple[GluingPublicInstance, ...]
    clauses: tuple[SatClause, ...]


@dataclass(frozen=True, slots=True)
class SatReference:
    phases: tuple[int, ...]
    groups: tuple[tuple[TetrahedronGroup, ...], ...]


@dataclass(frozen=True, slots=True)
class SatValidation:
    valid: bool
    reason: str
    phases: tuple[int, ...]
    clause_checks: int


@dataclass(frozen=True, slots=True)
class SatRecovery:
    first_groups: tuple[tuple[TetrahedronGroup, ...], ...]
    phase_solutions: tuple[tuple[int, ...], ...]
    gadget_count: int
    total_tetrahedra: int
    clause_count: int
    variable_degree_histogram: tuple[tuple[int, int], ...]
    factor_components: int
    factor_cycle_rank: int
    local_affine_implications: int
    gadget_matching_solutions: tuple[int, ...]
    gadget_matching_nodes: int
    gadget_matching_backtracks: int
    solution_cap: int
    solution_count: int
    solution_cap_hit: bool
    dpll_nodes: int
    dpll_decisions: int
    dpll_propagations: int
    dpll_conflicts: int
    dpll_backtracks: int
    exact_verifier_clause_checks: int
    accepted_solutions: int
    nonreference_accepted_solutions: int
    first_solution_matches_reference: bool


_SCOPE_FAMILIES = (
    (0, 1, 3),
    (0, 2, 5),
    (0, 4, 9),
    (0, 5, 11),
)


def _sat_clause_scopes(gadget_count: int) -> tuple[tuple[int, int, int], ...]:
    scopes = [
        tuple(sorted(((index + offset) % gadget_count for offset in offsets)))
        for offsets in _SCOPE_FAMILIES
        for index in range(gadget_count)
    ]
    result = tuple(scopes)
    if any(len(set(scope)) != 3 for scope in result):
        raise GluingExperimentError("G7 clause template contains repeated variables")
    if len(set(result)) != 4 * gadget_count:
        raise GluingExperimentError("G7 clause template contains duplicate scopes")
    return result


def _sat_clause_is_well_formed(variable_count: int, clause: SatClause) -> bool:
    return (
        len(clause.variables) == 3
        and len(set(clause.variables)) == 3
        and all(0 <= variable < variable_count for variable in clause.variables)
        and len(clause.negations) == 3
        and all(negation in (0, 1) for negation in clause.negations)
    )


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


def _factor_metrics(
    variable_count: int,
    clauses: tuple[SatClause, ...],
) -> tuple[tuple[tuple[int, int], ...], int, int]:
    degrees = [0] * variable_count
    adjacency = [set() for _ in range(variable_count + len(clauses))]
    for clause_index, clause in enumerate(clauses):
        clause_vertex = variable_count + clause_index
        for variable in clause.variables:
            degrees[variable] += 1
            adjacency[variable].add(clause_vertex)
            adjacency[clause_vertex].add(variable)

    seen: set[int] = set()
    components = 0
    for start in range(len(adjacency)):
        if start in seen:
            continue
        components += 1
        seen.add(start)
        stack = [start]
        while stack:
            vertex = stack.pop()
            for neighbor in adjacency[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)

    histogram = tuple(sorted(Counter(degrees).items()))
    edge_count = 3 * len(clauses)
    cycle_rank = edge_count - len(adjacency) + components
    return histogram, components, cycle_rank


def local_or_affine_implication_count() -> int:
    """Count non-trivial affine equations true on all satisfying 3-OR tuples."""
    satisfying = tuple(bits for bits in product((0, 1), repeat=3) if any(bits))
    implications = 0
    for mask in range(1, 1 << 3):
        for rhs in (0, 1):
            if all(
                (sum(bits[index] for index in range(3) if (mask >> index) & 1) & 1)
                == rhs
                for bits in satisfying
            ):
                implications += 1
    return implications


def validate_sat_witness(
    public: SatPublicInstance,
    groups_by_gadget: tuple[tuple[TetrahedronGroup, ...], ...],
) -> SatValidation:
    if len(groups_by_gadget) != len(public.gadgets):
        return SatValidation(False, "wrong G7 gadget witness count", (), 0)

    phases: list[int] = []
    for gadget, groups in zip(public.gadgets, groups_by_gadget, strict=True):
        if not validate_matching_gluing_witness(gadget, groups).valid:
            return SatValidation(False, "invalid local G3 matching witness", (), 0)
        phase = _phase_for_groups(gadget, groups)
        if phase is None:
            return SatValidation(False, "local witness is not a canonical G7 phase", (), 0)
        phases.append(phase)

    phase_tuple = tuple(phases)
    seen_clauses: set[tuple[tuple[int, int, int], tuple[int, int, int]]] = set()
    checks = 0
    for clause in public.clauses:
        if not _sat_clause_is_well_formed(len(public.gadgets), clause):
            return SatValidation(False, "malformed public G7 clause", phase_tuple, checks)
        key = (clause.variables, clause.negations)
        if key in seen_clauses:
            return SatValidation(False, "duplicate public G7 clause", phase_tuple, checks)
        seen_clauses.add(key)
        checks += 1
        if not any(
            phase_tuple[variable] ^ negation
            for variable, negation in zip(clause.variables, clause.negations, strict=True)
        ):
            return SatValidation(False, "G7 SAT clause violated", phase_tuple, checks)

    return SatValidation(True, "accepted", phase_tuple, checks)


def _phase_clause_state(
    assignment: list[int | None],
    clause: SatClause,
) -> tuple[bool, list[tuple[int, int]]]:
    unassigned: list[tuple[int, int]] = []
    for variable, negation in zip(clause.variables, clause.negations, strict=True):
        value = assignment[variable]
        if value is None:
            unassigned.append((variable, negation))
        elif value ^ negation:
            return True, []
    return False, unassigned


def _solve_sat_dpll(
    variable_count: int,
    clauses: tuple[SatClause, ...],
    solution_cap: int,
) -> tuple[tuple[tuple[int, ...], ...], int, int, int, int, int]:
    incidence: list[list[int]] = [[] for _ in range(variable_count)]
    for clause_index, clause in enumerate(clauses):
        for variable in clause.variables:
            incidence[variable].append(clause_index)

    solutions: list[tuple[int, ...]] = []
    nodes = 0
    decisions = 0
    propagations = 0
    conflicts = 0
    backtracks = 0

    def propagate(assignment: list[int | None]) -> bool:
        nonlocal propagations, conflicts
        changed = True
        while changed:
            changed = False
            for clause in clauses:
                satisfied, unassigned = _phase_clause_state(assignment, clause)
                if satisfied:
                    continue
                if not unassigned:
                    conflicts += 1
                    return False
                if len(unassigned) == 1:
                    variable, negation = unassigned[0]
                    value = 1 ^ negation
                    if assignment[variable] is None:
                        assignment[variable] = value
                        propagations += 1
                        changed = True
                    elif assignment[variable] != value:
                        conflicts += 1
                        return False
        return True

    def choose_variable(assignment: list[int | None]) -> int | None:
        best_variable: int | None = None
        best_score = -1
        for variable in range(variable_count):
            if assignment[variable] is not None:
                continue
            score = 0
            for clause_index in incidence[variable]:
                satisfied, _ = _phase_clause_state(assignment, clauses[clause_index])
                if not satisfied:
                    score += 1
            if score > best_score:
                best_score = score
                best_variable = variable
        return best_variable

    def search(assignment: list[int | None]) -> None:
        nonlocal nodes, decisions, backtracks
        if len(solutions) >= solution_cap:
            return
        nodes += 1
        work = assignment.copy()
        if not propagate(work):
            return

        variable = choose_variable(work)
        if variable is None:
            solutions.append(tuple(int(value) for value in work))
            return

        decisions += 1
        for value in (0, 1):
            if len(solutions) >= solution_cap:
                break
            before = len(solutions)
            child = work.copy()
            child[variable] = value
            search(child)
            if len(solutions) == before:
                backtracks += 1

    search([None] * variable_count)
    return tuple(solutions), nodes, decisions, propagations, conflicts, backtracks


def groups_for_sat_phases(
    public: SatPublicInstance,
    phases: tuple[int, ...],
) -> tuple[tuple[TetrahedronGroup, ...], ...]:
    if len(phases) != len(public.gadgets) or any(phase not in (0, 1) for phase in phases):
        raise GluingExperimentError("invalid G7 phase vector")
    result = []
    for gadget, phase in zip(public.gadgets, phases, strict=True):
        canonical, _, _ = _canonical_gadget_matchings(gadget)
        result.append(canonical[phase])
    return tuple(result)


def recover_sat_by_dpll(
    public: SatPublicInstance,
    *,
    solution_cap: int = 16,
    reference: SatReference | None = None,
) -> SatRecovery:
    variable_count = len(public.gadgets)
    if variable_count < 1:
        raise GluingExperimentError("public G7 instance has no gadgets")
    if solution_cap < 1 or solution_cap > 256:
        raise GluingExperimentError("G7 solution cap outside toy bounds")
    if not public.clauses:
        raise GluingExperimentError("public G7 instance has no clauses")
    if any(not _sat_clause_is_well_formed(variable_count, clause) for clause in public.clauses):
        raise GluingExperimentError("malformed public G7 clause")
    if len({(clause.variables, clause.negations) for clause in public.clauses}) != len(public.clauses):
        raise GluingExperimentError("duplicate public G7 clause")

    matching_solutions: list[int] = []
    matching_nodes = 0
    matching_backtracks = 0
    total_tetrahedra = 0
    for gadget in public.gadgets:
        _, nodes, backtracks = _canonical_gadget_matchings(gadget)
        matching_solutions.append(2)
        matching_nodes += nodes
        matching_backtracks += backtracks
        total_tetrahedra += len(gadget.tetrahedra)

    histogram, components, cycle_rank = _factor_metrics(variable_count, public.clauses)
    solutions, nodes, decisions, propagations, conflicts, backtracks = _solve_sat_dpll(
        variable_count, public.clauses, solution_cap
    )

    accepted = 0
    verifier_checks = 0
    for phases in solutions:
        groups = groups_for_sat_phases(public, phases)
        validation = validate_sat_witness(public, groups)
        verifier_checks += validation.clause_checks
        if not validation.valid:
            raise GluingExperimentError("G7 DPLL solution failed exact verifier")
        accepted += 1

    nonreference = 0
    first_matches_reference = False
    if reference is not None:
        nonreference = sum(phases != reference.phases for phases in solutions)
        first_matches_reference = bool(solutions) and solutions[0] == reference.phases

    first_groups = groups_for_sat_phases(public, solutions[0]) if solutions else ()
    return SatRecovery(
        first_groups=first_groups,
        phase_solutions=solutions,
        gadget_count=variable_count,
        total_tetrahedra=total_tetrahedra,
        clause_count=len(public.clauses),
        variable_degree_histogram=histogram,
        factor_components=components,
        factor_cycle_rank=cycle_rank,
        local_affine_implications=local_or_affine_implication_count(),
        gadget_matching_solutions=tuple(matching_solutions),
        gadget_matching_nodes=matching_nodes,
        gadget_matching_backtracks=matching_backtracks,
        solution_cap=solution_cap,
        solution_count=len(solutions),
        solution_cap_hit=len(solutions) >= solution_cap,
        dpll_nodes=nodes,
        dpll_decisions=decisions,
        dpll_propagations=propagations,
        dpll_conflicts=conflicts,
        dpll_backtracks=backtracks,
        exact_verifier_clause_checks=verifier_checks,
        accepted_solutions=accepted,
        nonreference_accepted_solutions=nonreference,
        first_solution_matches_reference=first_matches_reference,
    )


def sat_dimacs(public: SatPublicInstance) -> str:
    variable_count = len(public.gadgets)
    if any(not _sat_clause_is_well_formed(variable_count, clause) for clause in public.clauses):
        raise GluingExperimentError("cannot encode malformed G7 clause")
    lines = [f"p cnf {variable_count} {len(public.clauses)}"]
    for clause in public.clauses:
        literals = [
            -(variable + 1) if negation else variable + 1
            for variable, negation in zip(clause.variables, clause.negations, strict=True)
        ]
        lines.append(" ".join(str(literal) for literal in literals) + " 0")
    return "\n".join(lines) + "\n"


def parse_minisat_model(model_text: str, variable_count: int) -> tuple[int, ...]:
    tokens = model_text.split()
    if not tokens or tokens[0] != "SAT":
        raise GluingExperimentError("MiniSat did not return a SAT G7 model")
    assignment: list[int | None] = [None] * variable_count
    for token in tokens[1:]:
        literal = int(token)
        if literal == 0:
            continue
        variable = abs(literal) - 1
        if not 0 <= variable < variable_count:
            raise GluingExperimentError("MiniSat model variable outside G7 range")
        value = 1 if literal > 0 else 0
        if assignment[variable] is not None and assignment[variable] != value:
            raise GluingExperimentError("contradictory MiniSat G7 model")
        assignment[variable] = value
    if any(value is None for value in assignment):
        raise GluingExperimentError("incomplete MiniSat G7 model")
    return tuple(int(value) for value in assignment)


def generate_sat_phase_instance(
    params: SatPhaseParameters,
    master_seed: bytes,
) -> tuple[SatPublicInstance, SatReference]:
    params.validate()
    if len(master_seed) < 16:
        raise GluingExperimentError("G7 master seed must contain at least 128 bits")

    gadgets = []
    canonical_phases = []
    for gadget_index in range(params.gadget_count):
        gadget_seed = hashlib.sha256(
            b"MORPH-KEM G7 gadget v1\x00"
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
            b"MORPH-KEM G7 hidden phase v1\x00"
            + master_seed
            + params.name.encode("ascii")
            + index.to_bytes(4, "big")
        ).digest()[0]
        & 1
        for index in range(params.gadget_count)
    )

    clauses: list[SatClause] = []
    for clause_index, variables in enumerate(_sat_clause_scopes(params.gadget_count)):
        digest = hashlib.sha256(
            b"MORPH-KEM G7 clause pattern v1\x00"
            + master_seed
            + params.name.encode("ascii")
            + clause_index.to_bytes(4, "big")
        ).digest()
        pattern = (int.from_bytes(digest[:2], "big") % 7) + 1
        desired = tuple((pattern >> position) & 1 for position in range(3))
        negations = tuple(
            phases[variable] ^ desired[position]
            for position, variable in enumerate(variables)
        )
        clauses.append(SatClause(variables=variables, negations=negations))

    reference_groups = tuple(
        canonical_phases[index][phase]
        for index, phase in enumerate(phases)
    )
    public = SatPublicInstance(
        name=params.name,
        gadgets=tuple(gadgets),
        clauses=tuple(clauses),
    )
    reference = SatReference(phases=phases, groups=reference_groups)

    validation = validate_sat_witness(public, reference.groups)
    if not validation.valid:
        raise GluingExperimentError("G7 generated reference witness does not validate")
    histogram, components, _ = _factor_metrics(params.gadget_count, public.clauses)
    if histogram != ((12, params.gadget_count),) or components != 1:
        raise GluingExperimentError("G7 clause template failed regular connected controls")
    if local_or_affine_implication_count() != 0:
        raise GluingExperimentError("G7 OR relation unexpectedly exposes affine implication")

    return public, reference
