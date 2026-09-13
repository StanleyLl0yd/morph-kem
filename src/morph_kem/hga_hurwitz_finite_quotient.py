from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

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


class HGA4DError(HGA4Error):
    """Raised when an HGA4d finite-quotient experiment is malformed."""


Permutation = tuple[int, ...]
QuotientState = tuple[Permutation, Permutation, Permutation]


@dataclass(frozen=True, slots=True)
class HGA4DParameters:
    name: str
    exact_distance: int

    def validate(self) -> None:
        if self.exact_distance not in (4, 6, 8):
            raise HGA4DError("HGA4d distance outside declared toy shell depths")


HGA4D_PARAMETER_SETS = {
    "hga4d-D4": HGA4DParameters("hga4d-D4", 4),
    "hga4d-D6": HGA4DParameters("hga4d-D6", 6),
    "hga4d-D8": HGA4DParameters("hga4d-D8", 8),
}


@dataclass(frozen=True, slots=True)
class HGA4DReference:
    shell: HGA4CReference


@dataclass(frozen=True, slots=True)
class QuotientPruningRecovery:
    quotient_name: str
    quotient_degree: int
    quotient_reverse_states: int
    quotient_reverse_transitions: int
    quotient_shortest_distance: int | None
    quotient_distance_gap: int | None
    exact_states_kept: int
    exact_transitions_tested: int
    exact_candidate_prunes: int
    exact_duplicate_skips: int
    distinct_quotient_states_seen: int
    max_exact_states_per_quotient: int
    exact_state_fraction_of_generator_ball: float
    recovered_connector_length: int
    endpoint_verified: bool


@dataclass(frozen=True, slots=True)
class HGA4DRecovery:
    exact_distance: int
    generator_ball_states: int
    generator_shell_states: int
    ordinary_mitm_states: int
    ordinary_mitm_transitions: int
    ordinary_mitm_connector_length: int
    ordinary_mitm_endpoint_verified: bool
    quotients: tuple[QuotientPruningRecovery, ...]


def _identity(degree: int) -> Permutation:
    return tuple(range(degree))


def _compose(left: Permutation, right: Permutation) -> Permutation:
    if len(left) != len(right):
        raise HGA4DError("finite quotient permutation degree mismatch")
    return tuple(left[right[index]] for index in range(len(left)))


def _inverse(value: Permutation) -> Permutation:
    result = [0] * len(value)
    for source, target in enumerate(value):
        result[target] = source
    return tuple(result)


def _quotient_generators(name: str) -> tuple[Permutation, Permutation]:
    if name == "S3":
        return (1, 0, 2), (0, 2, 1)
    if name == "A5":
        # a=(0 1 2), b=(0 3 4), both even and together generate A5.
        return (1, 2, 0, 3, 4), (3, 1, 2, 4, 0)
    raise HGA4DError(f"unknown finite quotient {name!r}")


def _quotient_word(word: str, quotient_name: str) -> Permutation:
    a, b = _quotient_generators(quotient_name)
    values = {
        "a": a,
        "A": _inverse(a),
        "b": b,
        "B": _inverse(b),
    }
    result = _identity(len(a))
    for letter in word:
        try:
            result = _compose(result, values[letter])
        except KeyError as exc:
            raise HGA4DError("unknown free-group letter in quotient map") from exc
    return result


def _quotient_state(state: FreeState, quotient_name: str) -> QuotientState:
    values = tuple(_quotient_word(word, quotient_name) for word in state)
    return values  # type: ignore[return-value]


def _quotient_hurwitz(state: QuotientState, generator: str) -> QuotientState:
    if generator not in _BRAID_GENERATORS:
        raise HGA4DError("unknown braid generator in quotient action")
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
    result = tuple(values)
    return result  # type: ignore[return-value]


def _quotient_reverse_distances(
    target: QuotientState,
    max_depth: int,
) -> tuple[dict[QuotientState, int], int]:
    distances: dict[QuotientState, int] = {target: 0}
    frontier = [target]
    transitions = 0
    for depth in range(max_depth):
        next_frontier: list[QuotientState] = []
        for state in frontier:
            for generator in _BRAID_GENERATORS:
                transitions += 1
                candidate = _quotient_hurwitz(state, generator)
                if candidate in distances:
                    continue
                distances[candidate] = depth + 1
                next_frontier.append(candidate)
        frontier = next_frontier
        if not frontier:
            break
    return distances, transitions


def _pruned_exact_recovery(
    public: HGA4Public,
    quotient_name: str,
    generator_ball_states: int,
) -> QuotientPruningRecovery:
    distance = public.public_word_bound
    target_quotient = _quotient_state(public.target, quotient_name)
    reverse, reverse_transitions = _quotient_reverse_distances(target_quotient, distance)
    source_quotient = _quotient_state(public.source, quotient_name)
    quotient_distance = reverse.get(source_quotient)

    seen: dict[FreeState, str] = {public.source: ""}
    frontier = [public.source]
    exact_transitions = 0
    candidate_prunes = 0
    duplicate_skips = 0

    for depth in range(distance):
        next_frontier: list[FreeState] = []
        remaining = distance - (depth + 1)
        for state in frontier:
            prefix = seen[state]
            for generator in _BRAID_GENERATORS:
                exact_transitions += 1
                candidate = apply_hurwitz_generator(state, generator)
                if candidate in seen:
                    duplicate_skips += 1
                    continue
                quotient = _quotient_state(candidate, quotient_name)
                qdistance = reverse.get(quotient)
                if qdistance is None or qdistance > remaining:
                    candidate_prunes += 1
                    continue
                seen[candidate] = prefix + generator
                next_frontier.append(candidate)
        frontier = next_frontier
        if not frontier and public.target not in seen:
            raise HGA4DError(
                f"{quotient_name} pruning removed every exact path before the target"
            )

    connector = seen.get(public.target)
    if connector is None:
        raise HGA4DError(f"{quotient_name} pruning lost the exact target")
    endpoint_verified = apply_braid_word(public.source, connector) == public.target

    buckets = Counter(_quotient_state(state, quotient_name) for state in seen)
    max_bucket = max(buckets.values()) if buckets else 0
    fraction = (
        0.0
        if generator_ball_states <= 0
        else len(seen) / generator_ball_states
    )
    return QuotientPruningRecovery(
        quotient_name=quotient_name,
        quotient_degree=len(_quotient_generators(quotient_name)[0]),
        quotient_reverse_states=len(reverse),
        quotient_reverse_transitions=reverse_transitions,
        quotient_shortest_distance=quotient_distance,
        quotient_distance_gap=(
            None if quotient_distance is None else distance - quotient_distance
        ),
        exact_states_kept=len(seen),
        exact_transitions_tested=exact_transitions,
        exact_candidate_prunes=candidate_prunes,
        exact_duplicate_skips=duplicate_skips,
        distinct_quotient_states_seen=len(buckets),
        max_exact_states_per_quotient=max_bucket,
        exact_state_fraction_of_generator_ball=fraction,
        recovered_connector_length=len(connector),
        endpoint_verified=endpoint_verified,
    )


def generate_hga4d_instance(
    params: HGA4DParameters,
    master_seed: bytes,
) -> tuple[HGA4Public, HGA4DReference]:
    params.validate()
    if len(master_seed) < 16:
        raise HGA4DError("HGA4d master seed must contain at least 128 bits")
    public, reference = generate_hga4c_instance(
        HGA4CParameters(params.name, params.exact_distance), master_seed
    )
    return public, HGA4DReference(reference)


def recover_hga4d(
    public: HGA4Public,
    *,
    reference: HGA4DReference | None = None,
) -> HGA4DRecovery:
    ordinary = recover_hga4(public)
    generator_ball = 0 if reference is None else reference.shell.generator_ball_states
    generator_shell = 0 if reference is None else reference.shell.generator_shell_states
    quotients = tuple(
        _pruned_exact_recovery(public, name, generator_ball)
        for name in ("S3", "A5")
    )
    for result in quotients:
        if result.recovered_connector_length != public.public_word_bound:
            raise HGA4DError("finite-quotient attack contradicted exact shell distance")
        if not result.endpoint_verified:
            raise HGA4DError("finite-quotient attack produced an invalid endpoint")
    return HGA4DRecovery(
        exact_distance=public.public_word_bound,
        generator_ball_states=generator_ball,
        generator_shell_states=generator_shell,
        ordinary_mitm_states=ordinary.forward_states + ordinary.backward_states,
        ordinary_mitm_transitions=(
            ordinary.forward_transitions + ordinary.backward_transitions
        ),
        ordinary_mitm_connector_length=ordinary.recovered_connector_length,
        ordinary_mitm_endpoint_verified=ordinary.endpoint_verified,
        quotients=quotients,
    )
