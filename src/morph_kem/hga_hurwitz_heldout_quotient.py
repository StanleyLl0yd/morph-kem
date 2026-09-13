from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib

from .hga_hurwitz import (
    HGA4Error,
    HGA4Parameters,
    HGA4Public,
    FreeState,
    _BRAID_GENERATORS,
    _sample_source,
    apply_braid_word,
    apply_hurwitz_generator,
    recover_hga4,
    state_product,
)
from .hga_hurwitz_distance_shell import _exact_shell
from .hga_hurwitz_finite_quotient import (
    Permutation,
    QuotientState,
    _compose,
    _identity,
    _inverse,
)


class HGA4EError(HGA4Error):
    """Raised when an HGA4e held-out quotient control is malformed."""


@dataclass(frozen=True, slots=True)
class HGA4EParameters:
    name: str
    exact_distance: int

    def validate(self) -> None:
        if self.exact_distance not in (4, 6, 8):
            raise HGA4EError("HGA4e distance outside declared toy shell depths")


HGA4E_PARAMETER_SETS = {
    "hga4e-D4": HGA4EParameters("hga4e-D4", 4),
    "hga4e-D6": HGA4EParameters("hga4e-D6", 6),
    "hga4e-D8": HGA4EParameters("hga4e-D8", 8),
}


@dataclass(frozen=True, slots=True)
class TrainingQuotientMetric:
    quotient_name: str
    selected_retained_proxy_states: int
    selected_retained_proxy_fraction: float
    shell_targets_below_selected_retention: int
    actual_exact_states_retained: int
    actual_exact_transitions: int
    actual_endpoint_verified: bool


@dataclass(frozen=True, slots=True)
class HGA4EReference:
    selected_shortest_word: str
    generator_ball_states: int
    generator_shell_states: int
    generator_transitions: int
    selected_target_total_length: int
    training_metrics: tuple[TrainingQuotientMetric, ...]


@dataclass(frozen=True, slots=True)
class HeldoutQuotientRecovery:
    quotient_label: str
    quotient_components: tuple[str, ...]
    reverse_states: tuple[int, ...]
    reverse_transitions: tuple[int, ...]
    quotient_distances: tuple[int | None, ...]
    exact_states_kept: int
    exact_transitions_tested: int
    exact_candidate_prunes: int
    exact_duplicate_skips: int
    distinct_product_quotient_states_seen: int
    max_exact_states_per_product_state: int
    exact_state_fraction_of_generator_ball: float
    exact_state_fraction_of_ordinary_mitm_states: float
    recovered_connector_length: int
    endpoint_verified: bool


@dataclass(frozen=True, slots=True)
class HGA4ERecovery:
    exact_distance: int
    generator_ball_states: int
    generator_shell_states: int
    generator_transitions: int
    ordinary_mitm_states: int
    ordinary_mitm_transitions: int
    ordinary_connector_length: int
    ordinary_endpoint_verified: bool
    training_metrics: tuple[TrainingQuotientMetric, ...]
    heldout: tuple[HeldoutQuotientRecovery, ...]


_QUOTIENT_GENERATORS: dict[str, tuple[Permutation, Permutation]] = {
    # Training maps: exactly the public HGA4d maps.
    "S3-train": ((1, 0, 2), (0, 2, 1)),
    "A5-train": ((1, 2, 0, 3, 4), (3, 1, 2, 4, 0)),
    # Held-out maps: never consulted by target selection.
    "A4-heldout": ((1, 2, 0, 3), (1, 3, 2, 0)),
    "S4-heldout": ((1, 0, 2, 3), (1, 2, 3, 0)),
    "A5-heldout": ((1, 2, 3, 4, 0), (1, 2, 0, 3, 4)),
}

_TRAINING = ("S3-train", "A5-train")
_HELDOUT_ATTACKS = (
    ("A4", ("A4-heldout",)),
    ("S4", ("S4-heldout",)),
    ("A5-alt", ("A5-heldout",)),
    ("A4xS4", ("A4-heldout", "S4-heldout")),
    ("S4xA5-alt", ("S4-heldout", "A5-heldout")),
)


def _source_params(params: HGA4EParameters) -> HGA4Parameters:
    return HGA4Parameters(params.name, params.exact_distance)


def _quotient_word(word: str, quotient_name: str) -> Permutation:
    try:
        a, b = _QUOTIENT_GENERATORS[quotient_name]
    except KeyError as exc:
        raise HGA4EError(f"unknown HGA4e quotient {quotient_name!r}") from exc
    values = {"a": a, "A": _inverse(a), "b": b, "B": _inverse(b)}
    result = _identity(len(a))
    for letter in word:
        try:
            result = _compose(result, values[letter])
        except KeyError as exc:
            raise HGA4EError("unknown free-group letter in held-out quotient map") from exc
    return result


def _quotient_state(state: FreeState, quotient_name: str) -> QuotientState:
    values = tuple(_quotient_word(word, quotient_name) for word in state)
    return values  # type: ignore[return-value]


def _quotient_hurwitz(state: QuotientState, generator: str) -> QuotientState:
    if generator not in _BRAID_GENERATORS:
        raise HGA4EError("unknown braid generator in held-out quotient action")
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


def _reverse_distances(
    target: QuotientState,
    distance: int,
) -> tuple[dict[QuotientState, int], int]:
    distances: dict[QuotientState, int] = {target: 0}
    frontier = [target]
    transitions = 0
    for depth in range(distance):
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


def _retained_proxy_count(
    seen: dict[FreeState, str],
    qstates: dict[FreeState, QuotientState],
    reverse: dict[QuotientState, int],
    distance: int,
) -> int:
    retained = 0
    for state, word in seen.items():
        depth = len(word)
        qdistance = reverse.get(qstates[state])
        if qdistance is not None and qdistance <= distance - depth:
            retained += 1
    return retained


def _target_tiebreak(seed: bytes, params: HGA4EParameters, state: FreeState) -> bytes:
    encoded = b"\x1f".join(word.encode("ascii") for word in state)
    return hashlib.sha256(
        b"MORPH-KEM HGA4e training-conditioned target v1\x00"
        + seed
        + params.name.encode("ascii")
        + b"\x00"
        + encoded
    ).digest()


def _public_pruned_recovery(
    public: HGA4Public,
    quotient_names: tuple[str, ...],
    generator_ball_states: int,
    ordinary_mitm_states: int,
) -> HeldoutQuotientRecovery:
    distance = public.public_word_bound
    reverse_tables: list[dict[QuotientState, int]] = []
    reverse_states: list[int] = []
    reverse_transitions: list[int] = []
    quotient_distances: list[int | None] = []
    for name in quotient_names:
        reverse, transitions = _reverse_distances(
            _quotient_state(public.target, name), distance
        )
        reverse_tables.append(reverse)
        reverse_states.append(len(reverse))
        reverse_transitions.append(transitions)
        quotient_distances.append(reverse.get(_quotient_state(public.source, name)))

    seen: dict[FreeState, str] = {public.source: ""}
    frontier = [public.source]
    exact_transitions = 0
    candidate_prunes = 0
    duplicate_skips = 0
    for depth in range(distance):
        remaining = distance - depth - 1
        next_frontier: list[FreeState] = []
        for state in frontier:
            prefix = seen[state]
            for generator in _BRAID_GENERATORS:
                exact_transitions += 1
                candidate = apply_hurwitz_generator(state, generator)
                if candidate in seen:
                    duplicate_skips += 1
                    continue
                admissible = True
                for name, reverse in zip(quotient_names, reverse_tables, strict=True):
                    qdistance = reverse.get(_quotient_state(candidate, name))
                    if qdistance is None or qdistance > remaining:
                        admissible = False
                        break
                if not admissible:
                    candidate_prunes += 1
                    continue
                seen[candidate] = prefix + generator
                next_frontier.append(candidate)
        frontier = next_frontier
        if not frontier and public.target not in seen:
            raise HGA4EError("held-out quotient pruning removed every exact path")

    connector = seen.get(public.target)
    if connector is None:
        raise HGA4EError("held-out quotient pruning lost the exact target")
    endpoint_verified = apply_braid_word(public.source, connector) == public.target
    if not endpoint_verified:
        raise HGA4EError("held-out quotient attack failed exact endpoint verification")

    product_buckets = Counter(
        tuple(_quotient_state(state, name) for name in quotient_names)
        for state in seen
    )
    return HeldoutQuotientRecovery(
        quotient_label="+".join(quotient_names),
        quotient_components=quotient_names,
        reverse_states=tuple(reverse_states),
        reverse_transitions=tuple(reverse_transitions),
        quotient_distances=tuple(quotient_distances),
        exact_states_kept=len(seen),
        exact_transitions_tested=exact_transitions,
        exact_candidate_prunes=candidate_prunes,
        exact_duplicate_skips=duplicate_skips,
        distinct_product_quotient_states_seen=len(product_buckets),
        max_exact_states_per_product_state=max(product_buckets.values()),
        exact_state_fraction_of_generator_ball=len(seen) / generator_ball_states,
        exact_state_fraction_of_ordinary_mitm_states=(
            len(seen) / ordinary_mitm_states if ordinary_mitm_states else 0.0
        ),
        recovered_connector_length=len(connector),
        endpoint_verified=True,
    )


def generate_hga4e_instance(
    params: HGA4EParameters,
    master_seed: bytes,
) -> tuple[HGA4Public, HGA4EReference]:
    params.validate()
    if len(master_seed) < 16:
        raise HGA4EError("HGA4e master seed must contain at least 128 bits")

    source = _sample_source(_source_params(params), master_seed)
    seen, path_counts, shell, transitions = _exact_shell(source, params.exact_distance)
    qstates_by_name = {
        name: {state: _quotient_state(state, name) for state in seen}
        for name in _TRAINING
    }

    target_counts: dict[FreeState, tuple[int, ...]] = {}
    for target in shell:
        counts: list[int] = []
        for name in _TRAINING:
            reverse, _ = _reverse_distances(
                qstates_by_name[name][target], params.exact_distance
            )
            counts.append(
                _retained_proxy_count(
                    seen,
                    qstates_by_name[name],
                    reverse,
                    params.exact_distance,
                )
            )
        target_counts[target] = tuple(counts)

    target = max(
        shell,
        key=lambda state: (
            min(target_counts[state]),
            sum(target_counts[state]),
            sum(len(word) for word in state),
            _target_tiebreak(master_seed, params, state),
        ),
    )
    certificate = seen[target]
    if len(certificate) != params.exact_distance:
        raise HGA4EError("HGA4e target lost exact-distance certificate")
    if apply_braid_word(source, certificate) != target:
        raise HGA4EError("HGA4e certificate does not reproduce selected target")
    if state_product(source) != state_product(target):
        raise HGA4EError("HGA4e generator violated Hurwitz product invariant")

    public = HGA4Public(params.name, source, target, params.exact_distance)
    ordinary = recover_hga4(public)
    training_metrics: list[TrainingQuotientMetric] = []
    selected_counts = target_counts[target]
    for index, name in enumerate(_TRAINING):
        attack = _public_pruned_recovery(
            public,
            (name,),
            len(seen),
            ordinary.forward_states + ordinary.backward_states,
        )
        training_metrics.append(
            TrainingQuotientMetric(
                quotient_name=name,
                selected_retained_proxy_states=selected_counts[index],
                selected_retained_proxy_fraction=selected_counts[index] / len(seen),
                shell_targets_below_selected_retention=sum(
                    counts[index] < selected_counts[index]
                    for counts in target_counts.values()
                ),
                actual_exact_states_retained=attack.exact_states_kept,
                actual_exact_transitions=attack.exact_transitions_tested,
                actual_endpoint_verified=attack.endpoint_verified,
            )
        )

    return public, HGA4EReference(
        selected_shortest_word=certificate,
        generator_ball_states=len(seen),
        generator_shell_states=len(shell),
        generator_transitions=transitions,
        selected_target_total_length=sum(len(word) for word in target),
        training_metrics=tuple(training_metrics),
    )


def recover_hga4e(
    public: HGA4Public,
    *,
    reference: HGA4EReference | None = None,
) -> HGA4ERecovery:
    ordinary = recover_hga4(public)
    ordinary_states = ordinary.forward_states + ordinary.backward_states
    generator_ball = 0 if reference is None else reference.generator_ball_states
    generator_shell = 0 if reference is None else reference.generator_shell_states
    generator_transitions = 0 if reference is None else reference.generator_transitions
    if generator_ball <= 0:
        # Public recovery remains possible without reference; the exact-distance
        # generator metrics are then intentionally omitted from fractions.
        generator_ball = ordinary_states

    heldout = tuple(
        _public_pruned_recovery(
            public,
            components,
            generator_ball,
            ordinary_states,
        )
        for _, components in _HELDOUT_ATTACKS
    )
    for attack in heldout:
        if attack.recovered_connector_length != public.public_word_bound:
            raise HGA4EError("held-out quotient contradicted exact shell distance")

    return HGA4ERecovery(
        exact_distance=public.public_word_bound,
        generator_ball_states=(0 if reference is None else reference.generator_ball_states),
        generator_shell_states=generator_shell,
        generator_transitions=generator_transitions,
        ordinary_mitm_states=ordinary_states,
        ordinary_mitm_transitions=ordinary.forward_transitions + ordinary.backward_transitions,
        ordinary_connector_length=ordinary.recovered_connector_length,
        ordinary_endpoint_verified=ordinary.endpoint_verified,
        training_metrics=(() if reference is None else reference.training_metrics),
        heldout=heldout,
    )
