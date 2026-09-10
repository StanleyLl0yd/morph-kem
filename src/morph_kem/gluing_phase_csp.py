from __future__ import annotations

from dataclasses import dataclass
from itertools import product
import json
from math import prod
from typing import TypeAlias

from .gluing import GluingExperimentError, TetrahedronGroup
from .gluing_coupled import (
    CoupledPhasePublicInstance,
    validate_coupled_phase_witness,
)
from .gluing_exact_one import (
    ExactOnePublicInstance,
    _canonical_gadget_matchings,
    validate_exact_one_witness,
)
from .gluing_sat import SatPublicInstance, validate_sat_witness


PhaseAssignment: TypeAlias = tuple[int, ...]
LocalWitness: TypeAlias = tuple[TetrahedronGroup, ...]
LocalDomain: TypeAlias = tuple[LocalWitness, ...]


@dataclass(frozen=True, slots=True)
class RelationConstraint:
    scope: tuple[int, ...]
    allowed: tuple[tuple[int, ...], ...]


@dataclass(frozen=True, slots=True)
class CompiledPhaseCSP:
    family: str
    domain_sizes: tuple[int, ...]
    constraints: tuple[RelationConstraint, ...]


@dataclass(frozen=True, slots=True)
class PhaseLiftTable:
    domains: tuple[LocalDomain, ...]
    extraction_nodes: int
    extraction_backtracks: int
    topological_tetrahedra: int


@dataclass(frozen=True, slots=True)
class CompiledPhaseInstance:
    csp: CompiledPhaseCSP
    lift: PhaseLiftTable


@dataclass(frozen=True, slots=True)
class GenericCSPRecovery:
    assignments: tuple[PhaseAssignment, ...]
    solution_cap: int
    solution_count: int
    solution_cap_hit: bool
    nodes: int
    decisions: int
    value_prunes: int
    conflicts: int
    backtracks: int


@dataclass(frozen=True, slots=True)
class SemanticEquivalenceAudit:
    assignments_checked: int
    compiled_accepts: int
    original_accepts: int
    mismatches: int


def _extract_public_domains(gadgets: tuple[object, ...]) -> PhaseLiftTable:
    domains: list[LocalDomain] = []
    nodes = 0
    backtracks = 0
    tetrahedra = 0
    for gadget in gadgets:
        canonical, gadget_nodes, gadget_backtracks = _canonical_gadget_matchings(gadget)  # type: ignore[arg-type]
        if len(canonical) != 2:
            raise GluingExperimentError("G8 expected exactly two public local phases")
        domains.append(canonical)
        nodes += gadget_nodes
        backtracks += gadget_backtracks
        tetrahedra += len(gadget.tetrahedra)  # type: ignore[attr-defined]
    return PhaseLiftTable(
        domains=tuple(domains),
        extraction_nodes=nodes,
        extraction_backtracks=backtracks,
        topological_tetrahedra=tetrahedra,
    )


def _validated_csp(
    family: str,
    domain_sizes: tuple[int, ...],
    constraints: tuple[RelationConstraint, ...],
) -> CompiledPhaseCSP:
    if not domain_sizes or any(size < 1 for size in domain_sizes):
        raise GluingExperimentError("G8 compiled CSP has invalid domains")
    for relation in constraints:
        if not relation.scope or len(set(relation.scope)) != len(relation.scope):
            raise GluingExperimentError("G8 compiled relation has invalid scope")
        if any(variable < 0 or variable >= len(domain_sizes) for variable in relation.scope):
            raise GluingExperimentError("G8 compiled relation variable outside domain table")
        if not relation.allowed:
            raise GluingExperimentError("G8 compiled relation has empty allowed table")
        if len(set(relation.allowed)) != len(relation.allowed):
            raise GluingExperimentError("G8 compiled relation table contains duplicates")
        for allowed_tuple in relation.allowed:
            if len(allowed_tuple) != len(relation.scope):
                raise GluingExperimentError("G8 compiled relation tuple has wrong arity")
            if any(
                value < 0 or value >= domain_sizes[variable]
                for variable, value in zip(relation.scope, allowed_tuple, strict=True)
            ):
                raise GluingExperimentError("G8 compiled relation value outside domain")
    return CompiledPhaseCSP(family, domain_sizes, constraints)


def compile_g4(public: CoupledPhasePublicInstance) -> CompiledPhaseInstance:
    lift = _extract_public_domains(public.gadgets)
    domain_sizes = tuple(len(domain) for domain in lift.domains)
    constraints = tuple(
        RelationConstraint(
            scope=(constraint.left, constraint.right),
            allowed=tuple(
                bits
                for bits in product((0, 1), repeat=2)
                if bits[0] ^ bits[1] == constraint.parity
            ),
        )
        for constraint in public.constraints
    )
    csp = _validated_csp("G4", domain_sizes, constraints)
    return CompiledPhaseInstance(csp, lift)


def _compile_exact_one(
    family: str,
    public: ExactOnePublicInstance,
) -> CompiledPhaseInstance:
    if family not in ("G5", "G6"):
        raise GluingExperimentError("G8 exact-one adapter requires G5 or G6")
    lift = _extract_public_domains(public.gadgets)
    domain_sizes = tuple(len(domain) for domain in lift.domains)
    constraints = tuple(
        RelationConstraint(
            scope=clause.variables,
            allowed=tuple(
                bits
                for bits in product((0, 1), repeat=3)
                if sum(
                    bit ^ negation
                    for bit, negation in zip(bits, clause.negations, strict=True)
                )
                == 1
            ),
        )
        for clause in public.clauses
    )
    csp = _validated_csp(family, domain_sizes, constraints)
    return CompiledPhaseInstance(csp, lift)


def compile_g5(public: ExactOnePublicInstance) -> CompiledPhaseInstance:
    return _compile_exact_one("G5", public)


def compile_g6(public: ExactOnePublicInstance) -> CompiledPhaseInstance:
    return _compile_exact_one("G6", public)


def compile_g7(public: SatPublicInstance) -> CompiledPhaseInstance:
    lift = _extract_public_domains(public.gadgets)
    domain_sizes = tuple(len(domain) for domain in lift.domains)
    constraints = tuple(
        RelationConstraint(
            scope=clause.variables,
            allowed=tuple(
                bits
                for bits in product((0, 1), repeat=3)
                if any(
                    bit ^ negation
                    for bit, negation in zip(bits, clause.negations, strict=True)
                )
            ),
        )
        for clause in public.clauses
    )
    csp = _validated_csp("G7", domain_sizes, constraints)
    return CompiledPhaseInstance(csp, lift)


def serialize_compiled_csp(csp: CompiledPhaseCSP) -> str:
    payload = {
        "family": csp.family,
        "domain_sizes": list(csp.domain_sizes),
        "constraints": [
            {
                "scope": list(relation.scope),
                "allowed": [list(values) for values in relation.allowed],
            }
            for relation in csp.constraints
        ],
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def compiled_accepts(csp: CompiledPhaseCSP, assignment: PhaseAssignment) -> bool:
    if len(assignment) != len(csp.domain_sizes):
        return False
    if any(
        value < 0 or value >= csp.domain_sizes[index]
        for index, value in enumerate(assignment)
    ):
        return False
    return all(
        tuple(assignment[variable] for variable in relation.scope) in relation.allowed
        for relation in csp.constraints
    )


def lift_assignment(lift: PhaseLiftTable, assignment: PhaseAssignment) -> tuple[LocalWitness, ...]:
    if len(assignment) != len(lift.domains):
        raise GluingExperimentError("G8 assignment length does not match lift table")
    result: list[LocalWitness] = []
    for domain, value in zip(lift.domains, assignment, strict=True):
        if value < 0 or value >= len(domain):
            raise GluingExperimentError("G8 assignment value outside lift domain")
        result.append(domain[value])
    return tuple(result)


def original_accepts(
    family: str,
    public: CoupledPhasePublicInstance | ExactOnePublicInstance | SatPublicInstance,
    groups: tuple[LocalWitness, ...],
) -> bool:
    if family == "G4" and isinstance(public, CoupledPhasePublicInstance):
        return validate_coupled_phase_witness(public, groups).valid
    if family in ("G5", "G6") and isinstance(public, ExactOnePublicInstance):
        return validate_exact_one_witness(public, groups).valid
    if family == "G7" and isinstance(public, SatPublicInstance):
        return validate_sat_witness(public, groups).valid
    raise GluingExperimentError("G8 family/public-instance adapter mismatch")


def solve_compiled_csp(
    csp: CompiledPhaseCSP,
    *,
    solution_cap: int = 16,
) -> GenericCSPRecovery:
    if solution_cap < 1 or solution_cap > 256:
        raise GluingExperimentError("G8 solution cap outside toy bounds")
    _validated_csp(csp.family, csp.domain_sizes, csp.constraints)

    incidence: list[list[int]] = [[] for _ in csp.domain_sizes]
    for constraint_index, relation in enumerate(csp.constraints):
        for variable in relation.scope:
            incidence[variable].append(constraint_index)

    solutions: list[PhaseAssignment] = []
    nodes = 0
    decisions = 0
    value_prunes = 0
    conflicts = 0
    backtracks = 0

    def propagate(domains: list[set[int]]) -> bool:
        nonlocal value_prunes, conflicts
        changed = True
        while changed:
            changed = False
            for relation in csp.constraints:
                compatible = tuple(
                    values
                    for values in relation.allowed
                    if all(
                        value in domains[variable]
                        for variable, value in zip(relation.scope, values, strict=True)
                    )
                )
                if not compatible:
                    conflicts += 1
                    return False
                for position, variable in enumerate(relation.scope):
                    supported = {values[position] for values in compatible}
                    removed = domains[variable] - supported
                    if removed:
                        domains[variable].difference_update(removed)
                        value_prunes += len(removed)
                        changed = True
                        if not domains[variable]:
                            conflicts += 1
                            return False
        return True

    def choose_variable(domains: list[set[int]]) -> int | None:
        candidates = [index for index, domain in enumerate(domains) if len(domain) > 1]
        if not candidates:
            return None
        return min(candidates, key=lambda index: (len(domains[index]), -len(incidence[index]), index))

    def search(domains: list[set[int]]) -> None:
        nonlocal nodes, decisions, backtracks
        if len(solutions) >= solution_cap:
            return
        nodes += 1
        work = [set(domain) for domain in domains]
        if not propagate(work):
            return
        variable = choose_variable(work)
        if variable is None:
            assignment = tuple(next(iter(domain)) for domain in work)
            if not compiled_accepts(csp, assignment):
                raise GluingExperimentError("G8 propagated singleton assignment violates compiled CSP")
            solutions.append(assignment)
            return

        decisions += 1
        for value in sorted(work[variable]):
            if len(solutions) >= solution_cap:
                break
            before = len(solutions)
            child = [set(domain) for domain in work]
            child[variable] = {value}
            search(child)
            if len(solutions) == before:
                backtracks += 1

    search([set(range(size)) for size in csp.domain_sizes])
    return GenericCSPRecovery(
        assignments=tuple(solutions),
        solution_cap=solution_cap,
        solution_count=len(solutions),
        solution_cap_hit=len(solutions) >= solution_cap,
        nodes=nodes,
        decisions=decisions,
        value_prunes=value_prunes,
        conflicts=conflicts,
        backtracks=backtracks,
    )


def semantic_equivalence_audit(
    family: str,
    public: CoupledPhasePublicInstance | ExactOnePublicInstance | SatPublicInstance,
    compiled: CompiledPhaseInstance,
    *,
    max_assignments: int = 8192,
) -> SemanticEquivalenceAudit:
    assignment_count = prod(compiled.csp.domain_sizes)
    if assignment_count > max_assignments:
        raise GluingExperimentError("G8 exhaustive semantic audit exceeds configured bound")

    compiled_count = 0
    original_count = 0
    mismatches = 0
    checked = 0
    for assignment in product(*(range(size) for size in compiled.csp.domain_sizes)):
        phase_assignment = tuple(assignment)
        compiled_valid = compiled_accepts(compiled.csp, phase_assignment)
        groups = lift_assignment(compiled.lift, phase_assignment)
        original_valid = original_accepts(family, public, groups)
        checked += 1
        compiled_count += int(compiled_valid)
        original_count += int(original_valid)
        mismatches += int(compiled_valid != original_valid)

    return SemanticEquivalenceAudit(
        assignments_checked=checked,
        compiled_accepts=compiled_count,
        original_accepts=original_count,
        mismatches=mismatches,
    )
