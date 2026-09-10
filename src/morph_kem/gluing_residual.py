from __future__ import annotations

from dataclasses import dataclass
import hashlib
from itertools import product

from .gluing import GluingExperimentError, TetrahedronGroup
from .gluing_exact_one import (
    ExactOneClause,
    ExactOnePublicInstance,
    ExactOneReference,
    _canonical_gadget_matchings,
    _clause_is_well_formed,
    _factor_metrics,
    validate_exact_one_witness,
)
from .gluing_matching import G3_PARAMETER_SETS, generate_matching_gluing_instance


@dataclass(frozen=True, slots=True)
class ResidualExactOneParameters:
    name: str
    gadget_count: int

    def validate(self) -> None:
        if self.gadget_count not in (12, 18, 24):
            raise GluingExperimentError("G6 gadget count outside declared toy sets")


G6_PARAMETER_SETS = {
    "g6-12": ResidualExactOneParameters("g6-12", 12),
    "g6-18": ResidualExactOneParameters("g6-18", 18),
    "g6-24": ResidualExactOneParameters("g6-24", 24),
}


@dataclass(frozen=True, slots=True)
class ResidualExactOneRecovery:
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
    affine_candidate_count: int
    residual_clause_checks: int
    accepted_candidate_count: int
    exact_verifier_clause_checks: int
    nonreference_accepted_candidates: int
    first_accepted_matches_reference: bool


def _residual_clause_triples(gadget_count: int) -> tuple[tuple[int, int, int], ...]:
    triples = [
        tuple(sorted((index, (index + 1) % gadget_count, (index + 2) % gadget_count)))
        for index in range(gadget_count)
    ]
    triples.extend(
        tuple(sorted((index, (index + 1) % gadget_count, (index + 5) % gadget_count)))
        for index in range(gadget_count)
    )
    result = tuple(triples)
    if len(set(result)) != 2 * gadget_count:
        raise GluingExperimentError("G6 clause template contains duplicate scopes")
    return result


def _projected_rows(clauses: tuple[ExactOneClause, ...]) -> list[list[int]]:
    rows: list[list[int]] = []
    for clause in clauses:
        mask = 0
        for variable in clause.variables:
            mask ^= 1 << variable
        rhs = 1
        for negation in clause.negations:
            rhs ^= negation
        rows.append([mask, rhs])
    return rows


def _enumerate_affine_candidates(
    variable_count: int,
    clauses: tuple[ExactOneClause, ...],
) -> tuple[tuple[tuple[int, ...], ...], int, int, int]:
    rows = _projected_rows(clauses)
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

    if any(mask == 0 and rhs != 0 for mask, rhs in rows):
        raise GluingExperimentError("public G6 parity projection is inconsistent")

    rank = pivot_row
    free_columns = tuple(
        column for column in range(variable_count) if column not in set(pivot_columns)
    )
    nullity = len(free_columns)
    if nullity > 12:
        raise GluingExperimentError("G6 affine residual exceeds exhaustive toy bound")

    candidates: list[tuple[int, ...]] = []
    for free_values in product((0, 1), repeat=nullity):
        solution = [0] * variable_count
        for column, value in zip(free_columns, free_values, strict=True):
            solution[column] = value
        for row_index, pivot_column in enumerate(pivot_columns):
            mask, rhs = rows[row_index]
            value = rhs
            for free_column in free_columns:
                if (mask >> free_column) & 1:
                    value ^= solution[free_column]
            solution[pivot_column] = value
        candidate = tuple(solution)
        if any(
            (sum(candidate[variable] for variable in clause.variables) & 1)
            != (1 ^ clause.negations[0] ^ clause.negations[1] ^ clause.negations[2])
            for clause in clauses
        ):
            raise GluingExperimentError("G6 affine candidate reconstruction failed")
        candidates.append(candidate)

    return tuple(candidates), rank, nullity, row_xors


def _check_phase_candidate(
    phases: tuple[int, ...],
    clauses: tuple[ExactOneClause, ...],
) -> tuple[bool, int]:
    valid = True
    checks = 0
    for clause in clauses:
        checks += 1
        literal_sum = sum(
            phases[variable] ^ negation
            for variable, negation in zip(clause.variables, clause.negations, strict=True)
        )
        if literal_sum != 1:
            valid = False
    return valid, checks


def recover_residual_exact_one(
    public: ExactOnePublicInstance,
    *,
    reference: ExactOneReference | None = None,
) -> ResidualExactOneRecovery:
    variable_count = len(public.gadgets)
    if variable_count < 1:
        raise GluingExperimentError("public G6 instance has no gadgets")
    if not public.clauses:
        raise GluingExperimentError("public G6 instance has no clauses")
    if any(not _clause_is_well_formed(variable_count, clause) for clause in public.clauses):
        raise GluingExperimentError("malformed public G6 clause")
    if len({(clause.variables, clause.negations) for clause in public.clauses}) != len(public.clauses):
        raise GluingExperimentError("duplicate public G6 clause")

    gadget_phases: list[
        tuple[tuple[TetrahedronGroup, ...], tuple[TetrahedronGroup, ...]]
    ] = []
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
    candidates, rank, nullity, row_xors = _enumerate_affine_candidates(
        variable_count, public.clauses
    )

    residual_checks = 0
    accepted_phases: list[tuple[int, ...]] = []
    for candidate in candidates:
        valid, checks = _check_phase_candidate(candidate, public.clauses)
        residual_checks += checks
        if valid:
            accepted_phases.append(candidate)

    accepted_groups: list[tuple[tuple[TetrahedronGroup, ...], ...]] = []
    verifier_checks = 0
    for phases in accepted_phases:
        groups = tuple(
            gadget_phases[index][phase]
            for index, phase in enumerate(phases)
        )
        validation = validate_exact_one_witness(public, groups)
        verifier_checks += validation.clause_checks
        if not validation.valid:
            raise GluingExperimentError("G6 phase screen disagrees with exact verifier")
        accepted_groups.append(groups)

    nonreference = 0
    first_matches_reference = False
    if reference is not None:
        nonreference = sum(phases != reference.phases for phases in accepted_phases)
        first_matches_reference = bool(accepted_phases) and accepted_phases[0] == reference.phases

    recovered_groups = accepted_groups[0] if accepted_groups else ()
    recovered_phases = accepted_phases[0] if accepted_phases else ()
    return ResidualExactOneRecovery(
        recovered_groups=recovered_groups,
        recovered_phases=recovered_phases,
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
        affine_candidate_count=len(candidates),
        residual_clause_checks=residual_checks,
        accepted_candidate_count=len(accepted_phases),
        exact_verifier_clause_checks=verifier_checks,
        nonreference_accepted_candidates=nonreference,
        first_accepted_matches_reference=first_matches_reference,
    )


def generate_residual_exact_one_instance(
    params: ResidualExactOneParameters,
    master_seed: bytes,
) -> tuple[ExactOnePublicInstance, ExactOneReference]:
    params.validate()
    if len(master_seed) < 16:
        raise GluingExperimentError("G6 master seed must contain at least 128 bits")

    gadgets = []
    canonical_phases = []
    for gadget_index in range(params.gadget_count):
        gadget_seed = hashlib.sha256(
            b"MORPH-KEM G6 gadget v1\x00"
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
            b"MORPH-KEM G6 hidden phase v1\x00"
            + master_seed
            + params.name.encode("ascii")
            + index.to_bytes(4, "big")
        ).digest()[0]
        & 1
        for index in range(params.gadget_count)
    )

    clauses: list[ExactOneClause] = []
    for clause_index, variables in enumerate(_residual_clause_triples(params.gadget_count)):
        target = hashlib.sha256(
            b"MORPH-KEM G6 exact-one target v1\x00"
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

    if not validate_exact_one_witness(public, reference.groups).valid:
        raise GluingExperimentError("G6 generated reference witness does not validate")
    degree_histogram, components, _ = _factor_metrics(params.gadget_count, public.clauses)
    if degree_histogram != ((6, params.gadget_count),) or components != 1:
        raise GluingExperimentError("G6 clause template failed regular connected controls")
    candidates, rank, nullity, _ = _enumerate_affine_candidates(
        params.gadget_count, public.clauses
    )
    if rank != params.gadget_count - 2 or nullity != 2 or len(candidates) != 4:
        raise GluingExperimentError("G6 clause template failed residual affine controls")

    return public, reference
