from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass
from itertools import combinations

from .hga_hurwitz import (
    HGA4Error,
    HGA4Public,
    FreeState,
    _BRAID_GENERATORS,
    apply_braid_word,
    apply_hurwitz_generator,
    recover_hga4,
)
from .hga_hurwitz_distance_shell import (
    HGA4CParameters,
    HGA4CReference,
    generate_hga4c_instance,
)
from .hga_hurwitz_finite_quotient import (
    Permutation,
    QuotientState,
    _compose,
    _identity,
    _inverse,
)


class HGA4FError(HGA4Error):
    """Raised when an HGA4f adaptive quotient experiment is malformed."""


@dataclass(frozen=True, slots=True)
class HGA4FParameters:
    name: str
    exact_distance: int
    top_single_count: int = 3

    def validate(self) -> None:
        if self.exact_distance not in (4, 6, 8):
            raise HGA4FError("HGA4f distance outside declared toy shell depths")
        if self.top_single_count != 3:
            raise HGA4FError("HGA4f top-single count differs from declared attack")


HGA4F_PARAMETER_SETS = {
    "hga4f-D4": HGA4FParameters("hga4f-D4", 4),
    "hga4f-D6": HGA4FParameters("hga4f-D6", 6),
    "hga4f-D8": HGA4FParameters("hga4f-D8", 8),
}


@dataclass(frozen=True, slots=True)
class Representation:
    label: str
    generator_a: Permutation
    generator_b: Permutation

    @property
    def degree(self) -> int:
        return len(self.generator_a)


@dataclass(frozen=True, slots=True)
class AdaptiveFilterMetric:
    label: str
    components: tuple[str, ...]
    reverse_states: tuple[int, ...]
    reverse_transitions: tuple[int, ...]
    quotient_distances: tuple[int | None, ...]
    exact_states_kept: int
    exact_transitions_tested: int
    exact_candidate_prunes: int
    exact_duplicate_skips: int
    distinct_product_states: int
    maximum_exact_states_per_product_state: int
    exact_state_fraction_of_generator_ball: float
    exact_state_fraction_of_ordinary_mitm_states: float
    recovered_connector_length: int
    endpoint_verified: bool


@dataclass(frozen=True, slots=True)
class HGA4FRecovery:
    exact_distance: int
    generator_ball_states: int
    generator_shell_states: int
    generator_transitions: int
    ordinary_mitm_states: int
    ordinary_mitm_transitions: int
    ordinary_connector_length: int
    ordinary_endpoint_verified: bool
    library_size: int
    singles: tuple[AdaptiveFilterMetric, ...]
    selected_single_labels: tuple[str, ...]
    products: tuple[AdaptiveFilterMetric, ...]
    best_single_label: str
    best_single_states: int
    best_product_label: str
    best_product_states: int
    best_product_fraction_of_generator_ball: float
    best_product_fraction_of_ordinary_mitm_states: float


_LIBRARY: tuple[Representation, ...] = (
    Representation("S3-a", (1, 0, 2), (0, 2, 1)),
    Representation("S3-b", (1, 2, 0), (2, 1, 0)),
    Representation("S4-a", (1, 0, 2, 3), (1, 2, 3, 0)),
    Representation("S4-b", (1, 2, 0, 3), (0, 2, 3, 1)),
    Representation("A5-a", (1, 2, 0, 3, 4), (3, 1, 2, 4, 0)),
    Representation("A5-b", (1, 2, 3, 4, 0), (1, 2, 0, 3, 4)),
    Representation("A5-c", (2, 0, 1, 3, 4), (0, 2, 3, 1, 4)),
    Representation("A5-d", (2, 3, 4, 0, 1), (0, 1, 3, 4, 2)),
)
_REPRESENTATIONS = {item.label: item for item in _LIBRARY}


def _validate_representation(rep: Representation) -> None:
    if len(rep.generator_a) != len(rep.generator_b) or rep.degree < 2:
        raise HGA4FError("HGA4f representation generator degrees disagree")
    expected = tuple(range(rep.degree))
    if tuple(sorted(rep.generator_a)) != expected or tuple(sorted(rep.generator_b)) != expected:
        raise HGA4FError("HGA4f representation generator is not a permutation")


def _quotient_word(word: str, label: str) -> Permutation:
    try:
        rep = _REPRESENTATIONS[label]
    except KeyError as exc:
        raise HGA4FError(f"unknown HGA4f representation {label!r}") from exc
    values = {
        "a": rep.generator_a,
        "A": _inverse(rep.generator_a),
        "b": rep.generator_b,
        "B": _inverse(rep.generator_b),
    }
    result = _identity(rep.degree)
    for letter in word:
        try:
            result = _compose(result, values[letter])
        except KeyError as exc:
            raise HGA4FError("unknown free-group letter in quotient map") from exc
    return result


def quotient_state(state: FreeState, label: str) -> QuotientState:
    return tuple(_quotient_word(word, label) for word in state)  # type: ignore[return-value]


def quotient_hurwitz(state: QuotientState, generator: str) -> QuotientState:
    if generator not in _BRAID_GENERATORS:
        raise HGA4FError("unknown braid generator in quotient action")
    values = list(state)
    index = 0 if generator in ("p", "P") else 1
    left = values[index]
    right = values[index + 1]
    if generator in ("p", "q"):
        values[index] = _compose(_compose(left, right), _inverse(left))
        values[index + 1] = left
    else:
        values[index] = right
        values[index + 1] = _compose(_compose(_inverse(right), left), right)
    return tuple(values)  # type: ignore[return-value]


def _reverse_distances(
    target: QuotientState, distance: int
) -> tuple[dict[QuotientState, int], int]:
    distances: dict[QuotientState, int] = {target: 0}
    queue = deque([target])
    transitions = 0
    while queue:
        state = queue.popleft()
        depth = distances[state]
        if depth >= distance:
            continue
        for generator in _BRAID_GENERATORS:
            transitions += 1
            candidate = quotient_hurwitz(state, generator)
            if candidate in distances:
                continue
            distances[candidate] = depth + 1
            queue.append(candidate)
    return distances, transitions


def _pruned_recovery(
    public: HGA4Public,
    labels: tuple[str, ...],
    generator_ball_states: int,
    ordinary_mitm_states: int,
) -> AdaptiveFilterMetric:
    if not labels:
        raise HGA4FError("HGA4f adaptive filter has no components")
    distance = public.public_word_bound
    reverse_tables: list[dict[QuotientState, int]] = []
    reverse_states: list[int] = []
    reverse_transitions: list[int] = []
    quotient_distances: list[int | None] = []
    for label in labels:
        reverse, transitions = _reverse_distances(quotient_state(public.target, label), distance)
        reverse_tables.append(reverse)
        reverse_states.append(len(reverse))
        reverse_transitions.append(transitions)
        quotient_distances.append(reverse.get(quotient_state(public.source, label)))

    seen: dict[FreeState, str] = {public.source: ""}
    frontier = [public.source]
    transitions = 0
    prunes = 0
    duplicate_skips = 0
    for depth in range(distance):
        remaining = distance - depth - 1
        next_frontier: list[FreeState] = []
        for state in frontier:
            prefix = seen[state]
            for generator in _BRAID_GENERATORS:
                transitions += 1
                candidate = apply_hurwitz_generator(state, generator)
                if candidate in seen:
                    duplicate_skips += 1
                    continue
                admissible = True
                for label, reverse in zip(labels, reverse_tables, strict=True):
                    qdistance = reverse.get(quotient_state(candidate, label))
                    if qdistance is None or qdistance > remaining:
                        admissible = False
                        break
                if not admissible:
                    prunes += 1
                    continue
                seen[candidate] = prefix + generator
                next_frontier.append(candidate)
        frontier = next_frontier
        if not frontier and public.target not in seen:
            raise HGA4FError("adaptive quotient pruning removed every exact path")

    connector = seen.get(public.target)
    if connector is None:
        raise HGA4FError("adaptive quotient pruning lost the exact target")
    if apply_braid_word(public.source, connector) != public.target:
        raise HGA4FError("adaptive quotient connector failed exact endpoint verification")

    product_buckets = Counter(
        tuple(quotient_state(state, label) for label in labels) for state in seen
    )
    return AdaptiveFilterMetric(
        label="+".join(labels),
        components=labels,
        reverse_states=tuple(reverse_states),
        reverse_transitions=tuple(reverse_transitions),
        quotient_distances=tuple(quotient_distances),
        exact_states_kept=len(seen),
        exact_transitions_tested=transitions,
        exact_candidate_prunes=prunes,
        exact_duplicate_skips=duplicate_skips,
        distinct_product_states=len(product_buckets),
        maximum_exact_states_per_product_state=max(product_buckets.values()),
        exact_state_fraction_of_generator_ball=(
            len(seen) / generator_ball_states if generator_ball_states else 0.0
        ),
        exact_state_fraction_of_ordinary_mitm_states=(
            len(seen) / ordinary_mitm_states if ordinary_mitm_states else 0.0
        ),
        recovered_connector_length=len(connector),
        endpoint_verified=True,
    )


def generate_hga4f_instance(
    params: HGA4FParameters, master_seed: bytes
) -> tuple[HGA4Public, HGA4CReference]:
    params.validate()
    if len(master_seed) < 16:
        raise HGA4FError("HGA4f master seed must contain at least 128 bits")
    # Deliberately unconditioned HGA4c exact-distance generation.
    return generate_hga4c_instance(
        HGA4CParameters(params.name, params.exact_distance), master_seed
    )


def recover_hga4f(
    public: HGA4Public,
    *,
    reference: HGA4CReference | None = None,
    top_single_count: int = 3,
) -> HGA4FRecovery:
    for rep in _LIBRARY:
        _validate_representation(rep)
    if top_single_count != 3:
        raise HGA4FError("HGA4f recovery top-single count differs from declared attack")

    ordinary = recover_hga4(public)
    ordinary_states = ordinary.forward_states + ordinary.backward_states
    ordinary_transitions = ordinary.forward_transitions + ordinary.backward_transitions
    generator_ball = reference.generator_ball_states if reference is not None else ordinary_states

    singles = tuple(
        _pruned_recovery(public, (rep.label,), generator_ball, ordinary_states)
        for rep in _LIBRARY
    )
    ranked = tuple(
        sorted(
            singles,
            key=lambda item: (item.exact_states_kept, item.exact_transitions_tested, item.label),
        )
    )
    selected = tuple(item.label for item in ranked[:top_single_count])
    products = tuple(
        _pruned_recovery(public, pair, generator_ball, ordinary_states)
        for pair in combinations(selected, 2)
    )
    best_product = min(
        products,
        key=lambda item: (item.exact_states_kept, item.exact_transitions_tested, item.label),
    )
    best_single = ranked[0]

    for metric in singles + products:
        if metric.recovered_connector_length != public.public_word_bound:
            raise HGA4FError("adaptive quotient contradicted certified exact distance")

    return HGA4FRecovery(
        exact_distance=public.public_word_bound,
        generator_ball_states=(reference.generator_ball_states if reference is not None else 0),
        generator_shell_states=(reference.generator_shell_states if reference is not None else 0),
        generator_transitions=(reference.generator_transitions if reference is not None else 0),
        ordinary_mitm_states=ordinary_states,
        ordinary_mitm_transitions=ordinary_transitions,
        ordinary_connector_length=ordinary.recovered_connector_length,
        ordinary_endpoint_verified=ordinary.endpoint_verified,
        library_size=len(_LIBRARY),
        singles=singles,
        selected_single_labels=selected,
        products=products,
        best_single_label=best_single.label,
        best_single_states=best_single.exact_states_kept,
        best_product_label=best_product.label,
        best_product_states=best_product.exact_states_kept,
        best_product_fraction_of_generator_ball=best_product.exact_state_fraction_of_generator_ball,
        best_product_fraction_of_ordinary_mitm_states=best_product.exact_state_fraction_of_ordinary_mitm_states,
    )
