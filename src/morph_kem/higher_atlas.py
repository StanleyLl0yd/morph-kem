from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
import hashlib
import json
from statistics import mean

Chart = tuple[tuple[int, int, int], tuple[int, int, int]]


class HigherAtlasError(ValueError):
    """Raised when an H2-E2 higher-order atlas input is invalid."""


@dataclass(frozen=True, slots=True)
class HigherAtlasParameters:
    name: str
    variables: int
    charts: int
    seam_budget: int

    def validate(self) -> None:
        if self.variables < 6 or self.variables > 28:
            raise HigherAtlasError("H2-E2 variable count must be in [6, 28]")
        if self.charts <= self.seam_budget:
            raise HigherAtlasError("H2-E2 needs more charts than seams")
        if self.charts > self.variables * (self.variables - 1) * (self.variables - 2) // 6:
            raise HigherAtlasError("H2-E2 chart count exceeds unique variable triples")
        if self.seam_budget <= 0 or self.seam_budget > 6:
            raise HigherAtlasError("H2-E2 seam budget must be in [1, 6]")


HIGHER_ATLAS_PARAMETER_SETS = {
    "atlas-8": HigherAtlasParameters("atlas-8", variables=8, charts=18, seam_budget=1),
    "atlas-10": HigherAtlasParameters("atlas-10", variables=10, charts=24, seam_budget=1),
    "atlas-12": HigherAtlasParameters("atlas-12", variables=12, charts=30, seam_budget=2),
    "atlas-14": HigherAtlasParameters("atlas-14", variables=14, charts=36, seam_budget=2),
    "atlas-16": HigherAtlasParameters("atlas-16", variables=16, charts=42, seam_budget=3),
}


@dataclass(frozen=True, slots=True)
class HigherAtlasPublic:
    parameters: HigherAtlasParameters
    charts: tuple[Chart, ...]
    version: int = 1

    def __post_init__(self) -> None:
        self.parameters.validate()
        if self.version != 1:
            raise HigherAtlasError("unsupported H2-E2 public-instance version")
        if len(self.charts) != self.parameters.charts:
            raise HigherAtlasError("H2-E2 chart count does not match parameters")

        previous_vars: tuple[int, int, int] | None = None
        seen: set[tuple[int, int, int]] = set()
        for variables, negations in self.charts:
            if len(variables) != 3 or tuple(sorted(variables)) != variables:
                raise HigherAtlasError("chart variables must be three canonical distinct indices")
            if any(variable < 0 or variable >= self.parameters.variables for variable in variables):
                raise HigherAtlasError("chart variable outside public range")
            if variables in seen:
                raise HigherAtlasError("duplicate H2-E2 variable triple")
            if previous_vars is not None and variables <= previous_vars:
                raise HigherAtlasError("H2-E2 charts must be sorted by variable triple")
            if len(negations) != 3 or any(bit not in (0, 1) for bit in negations):
                raise HigherAtlasError("chart negations must be three bits")
            seen.add(variables)
            previous_vars = variables

    def encode(self) -> bytes:
        payload = {
            "charts": [
                {
                    "negations": list(negations),
                    "variables": list(variables),
                }
                for variables, negations in self.charts
            ],
            "parameters": {
                "charts": self.parameters.charts,
                "name": self.parameters.name,
                "seam_budget": self.parameters.seam_budget,
                "variables": self.parameters.variables,
            },
            "version": self.version,
        }
        return json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")


@dataclass(frozen=True, slots=True)
class HigherAtlasReference:
    assignment: tuple[int, ...]
    planted_seams: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class HigherAtlasValidation:
    accepted: bool
    failed_chart: int | None
    reason: str


@dataclass(frozen=True, slots=True)
class PairwiseAudit:
    chart_pairs: int
    compatible_pairs: int

    @property
    def all_compatible(self) -> bool:
        return self.chart_pairs == self.compatible_pairs


@dataclass(frozen=True, slots=True)
class RoleSignatureAudit:
    planted_seams: int
    seam_signatures_seen_in_normal: int
    unique_seam_signatures: int


@dataclass(frozen=True, slots=True)
class HigherAtlasRepair:
    found: bool
    assignment: tuple[int, ...]
    seams: tuple[int, ...]
    minimum_seams: int | None
    nodes: int
    backtracks: int
    best_updates: int
    proven_minimum: bool
    exhausted_node_cap: bool


@dataclass(frozen=True, slots=True)
class HigherAtlasSweepRow:
    name: str
    variables: int
    charts: int
    budget: int
    pairwise_compatible: bool
    found: bool
    minimum_seams: int | None
    nodes: int
    backtracks: int
    seam_signatures_seen_in_normal: int


class _DeterministicRng:
    def __init__(self, seed: bytes):
        self._seed = seed
        self._counter = 0

    def _block(self) -> bytes:
        block = hashlib.sha256(
            b"MORPH-KEM H2-E2 deterministic rng v1\x00"
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


def _shuffle(values: list, seed: bytes) -> None:
    rng = _DeterministicRng(seed)
    for index in range(len(values) - 1, 0, -1):
        other = rng.randbelow(index + 1)
        values[index], values[other] = values[other], values[index]


def _chart_satisfied(chart: Chart, assignment: tuple[int, ...] | list[int | None]) -> bool | None:
    variables, negations = chart
    effective: list[int] = []
    for variable, negation in zip(variables, negations):
        value = assignment[variable]
        if value is None:
            return None
        effective.append(int(value) ^ negation)
    return not (effective[0] == effective[1] == effective[2])


def _violated_charts(charts: tuple[Chart, ...], assignment: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        index
        for index, chart in enumerate(charts)
        if _chart_satisfied(chart, assignment) is False
    )


def validate_higher_atlas_witness(
    public: HigherAtlasPublic,
    seams: tuple[int, ...],
    assignment: tuple[int, ...],
) -> HigherAtlasValidation:
    if len(seams) > public.parameters.seam_budget:
        return HigherAtlasValidation(False, None, "seam budget exceeded")
    if tuple(sorted(set(seams))) != seams:
        return HigherAtlasValidation(False, None, "seams must be unique sorted chart indices")
    if any(index < 0 or index >= len(public.charts) for index in seams):
        return HigherAtlasValidation(False, None, "seam chart index outside public range")
    if len(assignment) != public.parameters.variables:
        return HigherAtlasValidation(False, None, "assignment length does not match variables")
    if any(bit not in (0, 1) for bit in assignment):
        return HigherAtlasValidation(False, None, "assignment values must be bits")

    seam_set = set(seams)
    for index, chart in enumerate(public.charts):
        if index in seam_set:
            continue
        if _chart_satisfied(chart, assignment) is not True:
            return HigherAtlasValidation(False, index, "retained chart rejects assignment")
    return HigherAtlasValidation(True, None, "accepted")


def _pair_jointly_satisfiable(left: Chart, right: Chart) -> bool:
    variables = tuple(sorted(set(left[0]) | set(right[0])))
    for values in product((0, 1), repeat=len(variables)):
        mapping = dict(zip(variables, values))
        assignment: list[int | None] = [None] * (max(variables) + 1)
        for variable, value in mapping.items():
            assignment[variable] = value
        if _chart_satisfied(left, assignment) is True and _chart_satisfied(right, assignment) is True:
            return True
    return False


def pairwise_compatibility_audit(public: HigherAtlasPublic) -> PairwiseAudit:
    total = 0
    compatible = 0
    for left_index in range(len(public.charts)):
        for right_index in range(left_index + 1, len(public.charts)):
            total += 1
            compatible += int(
                _pair_jointly_satisfiable(
                    public.charts[left_index],
                    public.charts[right_index],
                )
            )
    return PairwiseAudit(total, compatible)


def _find_models(
    charts: tuple[Chart, ...],
    variables: int,
    cap: int,
    max_nodes: int = 2_000_000,
) -> tuple[tuple[int, ...], ...]:
    if cap <= 0:
        raise ValueError("model cap must be positive")

    occurrence = [0] * variables
    for chart_variables, _ in charts:
        for variable in chart_variables:
            occurrence[variable] += 1
    order = tuple(sorted(range(variables), key=lambda item: (-occurrence[item], item)))

    assignment: list[int | None] = [None] * variables
    assignment[0] = 0  # global complement symmetry
    models: list[tuple[int, ...]] = []
    nodes = 0

    def consistent() -> bool:
        for chart in charts:
            if _chart_satisfied(chart, assignment) is False:
                return False
        return True

    def search(position: int) -> None:
        nonlocal nodes
        if len(models) >= cap or nodes >= max_nodes:
            return
        while position < len(order) and assignment[order[position]] is not None:
            position += 1
        if position == len(order):
            models.append(tuple(int(value) for value in assignment))
            return

        variable = order[position]
        for value in (0, 1):
            nodes += 1
            assignment[variable] = value
            if consistent():
                search(position + 1)
            assignment[variable] = None
            if len(models) >= cap or nodes >= max_nodes:
                return

    search(0)
    return tuple(models)


def _canonical_chart(
    variables: tuple[int, int, int],
    negations: tuple[int, int, int],
) -> Chart:
    paired = sorted(zip(variables, negations))
    return (
        tuple(item[0] for item in paired),  # type: ignore[return-value]
        tuple(item[1] for item in paired),  # type: ignore[return-value]
    )


def generate_higher_atlas(
    parameters: HigherAtlasParameters,
    master_seed: bytes,
) -> tuple[HigherAtlasPublic, HigherAtlasReference]:
    parameters.validate()
    if not isinstance(master_seed, bytes) or not master_seed:
        raise HigherAtlasError("master_seed must be non-empty bytes")

    normal_count = parameters.charts - parameters.seam_budget

    for attempt in range(1024):
        attempt_seed = hashlib.sha256(
            b"MORPH-KEM H2-E2 generation attempt v1\x00"
            + parameters.name.encode("ascii")
            + b"\x00"
            + master_seed
            + attempt.to_bytes(4, "big")
        ).digest()
        rng = _DeterministicRng(
            hashlib.sha256(
                b"MORPH-KEM H2-E2 assignment/sign generator v1\x00" + attempt_seed
            ).digest()
        )
        hidden = tuple(rng.randbelow(2) for _ in range(parameters.variables))

        triples = list(combinations(range(parameters.variables), 3))
        _shuffle(
            triples,
            hashlib.sha256(
                b"MORPH-KEM H2-E2 triple order v1\x00" + attempt_seed
            ).digest(),
        )

        normal_charts: list[Chart] = []
        cursor = 0
        while len(normal_charts) < normal_count and cursor < len(triples):
            variables = triples[cursor]
            cursor += 1
            choices = list(product((0, 1), repeat=3))
            _shuffle(
                choices,
                hashlib.sha256(
                    b"MORPH-KEM H2-E2 normal signs v1\x00"
                    + attempt_seed
                    + len(normal_charts).to_bytes(4, "big")
                ).digest(),
            )
            selected: Chart | None = None
            for negations in choices:
                chart = _canonical_chart(variables, negations)
                if _chart_satisfied(chart, hidden) is True:
                    selected = chart
                    break
            if selected is not None:
                normal_charts.append(selected)

        if len(normal_charts) != normal_count:
            continue

        models = _find_models(tuple(normal_charts), parameters.variables, cap=3)
        hidden_rooted = hidden if hidden[0] == 0 else tuple(bit ^ 1 for bit in hidden)
        complement_rooted = tuple(bit ^ 1 for bit in hidden_rooted)
        expected = {hidden_rooted, complement_rooted}
        # With root fixed to zero only one complement representative remains.
        rooted_expected = {model for model in expected if model[0] == 0}
        if set(models) != rooted_expected:
            continue

        seam_charts: list[Chart] = []
        while len(seam_charts) < parameters.seam_budget and cursor < len(triples):
            variables = triples[cursor]
            cursor += 1
            choices = list(product((0, 1), repeat=3))
            _shuffle(
                choices,
                hashlib.sha256(
                    b"MORPH-KEM H2-E2 seam signs v1\x00"
                    + attempt_seed
                    + len(seam_charts).to_bytes(4, "big")
                ).digest(),
            )
            selected = None
            for negations in choices:
                chart = _canonical_chart(variables, negations)
                if _chart_satisfied(chart, hidden) is False:
                    selected = chart
                    break
            if selected is not None:
                seam_charts.append(selected)

        if len(seam_charts) != parameters.seam_budget:
            continue

        tagged = [(chart, False) for chart in normal_charts] + [
            (chart, True) for chart in seam_charts
        ]
        tagged.sort(key=lambda item: item[0][0])
        charts = tuple(item[0] for item in tagged)
        planted_seams = tuple(
            index for index, item in enumerate(tagged) if item[1]
        )
        public = HigherAtlasPublic(parameters, charts)
        reference = HigherAtlasReference(hidden, planted_seams)

        if not validate_higher_atlas_witness(
            public,
            reference.planted_seams,
            reference.assignment,
        ).accepted:
            raise HigherAtlasError("internal H2-E2 planted witness validation failed")

        audit = pairwise_compatibility_audit(public)
        if not audit.all_compatible:
            continue

        full_models = _find_models(public.charts, parameters.variables, cap=1)
        if full_models:
            continue

        return public, reference

    raise HigherAtlasError("could not generate pairwise-compatible globally inconsistent H2-E2 atlas")


def _partial_lower_bound(
    charts: tuple[Chart, ...],
    assignment: list[int | None],
) -> int:
    definitely_violated = 0
    forced_by_variable: dict[int, list[int]] = {}

    for chart in charts:
        variables, negations = chart
        values: list[int | None] = []
        unassigned_positions: list[int] = []
        for position, (variable, negation) in enumerate(zip(variables, negations)):
            raw = assignment[variable]
            if raw is None:
                values.append(None)
                unassigned_positions.append(position)
            else:
                values.append(int(raw) ^ negation)

        if not unassigned_positions:
            if values[0] == values[1] == values[2]:
                definitely_violated += 1
            continue

        if len(unassigned_positions) == 1:
            missing = unassigned_positions[0]
            known = [values[index] for index in range(3) if index != missing]
            if known[0] == known[1]:
                variable = variables[missing]
                negation = negations[missing]
                # Effective missing value must differ from known value.
                required_raw = (1 - int(known[0])) ^ negation
                forced_by_variable.setdefault(variable, []).append(required_raw)

    unavoidable = 0
    for requirements in forced_by_variable.values():
        zeros = requirements.count(0)
        ones = requirements.count(1)
        unavoidable += min(zeros, ones)

    return definitely_violated + unavoidable


def solve_higher_atlas_repair(
    public: HigherAtlasPublic,
    max_nodes: int = 2_000_000,
) -> HigherAtlasRepair:
    if max_nodes <= 0 or max_nodes > 50_000_000:
        raise HigherAtlasError("max_nodes must be in [1, 50000000]")

    variables = public.parameters.variables
    occurrence = [0] * variables
    for chart_variables, _ in public.charts:
        for variable in chart_variables:
            occurrence[variable] += 1
    order = tuple(sorted(range(variables), key=lambda item: (-occurrence[item], item)))

    assignment: list[int | None] = [None] * variables
    assignment[0] = 0  # quotient the global complement symmetry

    best_count = public.parameters.seam_budget + 1
    best_assignment: tuple[int, ...] | None = None
    best_seams: tuple[int, ...] = ()
    nodes = 0
    backtracks = 0
    best_updates = 0
    exhausted = False

    def projected_cost(variable: int, value: int) -> int:
        assignment[variable] = value
        cost = _partial_lower_bound(public.charts, assignment)
        assignment[variable] = None
        return cost

    def search(position: int) -> None:
        nonlocal best_count, best_assignment, best_seams
        nonlocal nodes, backtracks, best_updates, exhausted

        if exhausted:
            return
        nodes += 1
        if nodes > max_nodes:
            exhausted = True
            return

        lower_bound = _partial_lower_bound(public.charts, assignment)
        if lower_bound >= best_count or lower_bound > public.parameters.seam_budget:
            backtracks += 1
            return

        while position < len(order) and assignment[order[position]] is not None:
            position += 1

        if position == len(order):
            candidate = tuple(int(value) for value in assignment)
            seams = _violated_charts(public.charts, candidate)
            if len(seams) < best_count and len(seams) <= public.parameters.seam_budget:
                best_count = len(seams)
                best_assignment = candidate
                best_seams = seams
                best_updates += 1
            return

        variable = order[position]
        choices = sorted(
            ((projected_cost(variable, value), value) for value in (0, 1)),
            key=lambda item: (item[0], item[1]),
        )
        for _, value in choices:
            assignment[variable] = value
            search(position + 1)
            assignment[variable] = None
            if exhausted or best_count == 0:
                return

    search(0)

    if best_assignment is None:
        return HigherAtlasRepair(
            False,
            (),
            (),
            None,
            nodes,
            backtracks,
            best_updates,
            not exhausted,
            exhausted,
        )

    validation = validate_higher_atlas_witness(public, best_seams, best_assignment)
    if not validation.accepted:
        raise HigherAtlasError("internal H2-E2 solver produced an invalid witness")

    return HigherAtlasRepair(
        True,
        best_assignment,
        best_seams,
        best_count,
        nodes,
        backtracks,
        best_updates,
        not exhausted,
        exhausted,
    )


def chart_role_signature_audit(
    public: HigherAtlasPublic,
    reference: HigherAtlasReference,
) -> RoleSignatureAudit:
    degrees = [0] * public.parameters.variables
    for variables, _ in public.charts:
        for variable in variables:
            degrees[variable] += 1

    def signature(chart: Chart) -> tuple[int, tuple[int, int, int]]:
        variables, negations = chart
        return (
            sum(negations),
            tuple(sorted(degrees[variable] for variable in variables)),
        )

    seam_set = set(reference.planted_seams)
    normal_signatures = {
        signature(chart)
        for index, chart in enumerate(public.charts)
        if index not in seam_set
    }
    seam_signatures = [
        signature(chart)
        for index, chart in enumerate(public.charts)
        if index in seam_set
    ]
    seen = sum(item in normal_signatures for item in seam_signatures)
    unique = len(set(seam_signatures) - normal_signatures)
    return RoleSignatureAudit(len(seam_signatures), seen, unique)


def higher_atlas_scaling_sweep(
    master_seed: bytes,
    max_nodes: int = 2_000_000,
) -> tuple[HigherAtlasSweepRow, ...]:
    rows: list[HigherAtlasSweepRow] = []
    for parameters in HIGHER_ATLAS_PARAMETER_SETS.values():
        public, reference = generate_higher_atlas(parameters, master_seed)
        pairwise = pairwise_compatibility_audit(public)
        role = chart_role_signature_audit(public, reference)
        repair = solve_higher_atlas_repair(public, max_nodes=max_nodes)
        rows.append(
            HigherAtlasSweepRow(
                parameters.name,
                parameters.variables,
                parameters.charts,
                parameters.seam_budget,
                pairwise.all_compatible,
                repair.found,
                repair.minimum_seams,
                repair.nodes,
                repair.backtracks,
                role.seam_signatures_seen_in_normal,
            )
        )
    return tuple(rows)
