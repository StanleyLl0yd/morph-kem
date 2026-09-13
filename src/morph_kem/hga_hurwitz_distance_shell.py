from __future__ import annotations

from dataclasses import dataclass
import hashlib

from .hga_hurwitz import (
    HGA4Error,
    HGA4Parameters,
    HGA4Public,
    HGA4Recovery,
    HGA4Reference,
    FreeState,
    _BRAID_GENERATORS,
    _sample_source,
    apply_braid_word,
    apply_hurwitz_generator,
    recover_hga4,
    state_product,
)


class HGA4CError(HGA4Error):
    """Raised when an HGA4c exact-distance calibration is malformed."""


@dataclass(frozen=True, slots=True)
class HGA4CParameters:
    name: str
    exact_distance: int

    def validate(self) -> None:
        if self.exact_distance not in (4, 6, 8):
            raise HGA4CError("HGA4c distance outside declared toy shell depths")


HGA4C_PARAMETER_SETS = {
    "hga4c-D4": HGA4CParameters("hga4c-D4", 4),
    "hga4c-D6": HGA4CParameters("hga4c-D6", 6),
    "hga4c-D8": HGA4CParameters("hga4c-D8", 8),
}


@dataclass(frozen=True, slots=True)
class HGA4CReference:
    selected_shortest_word: str
    generator_ball_states: int
    generator_shell_states: int
    generator_transitions: int
    selected_target_total_length: int
    shortest_path_multiplicity: int


@dataclass(frozen=True, slots=True)
class HGA4CRecovery:
    exact_distance: int
    generator_ball_states: int
    generator_shell_states: int
    generator_transitions: int
    selected_target_total_length: int
    shortest_path_multiplicity: int
    attacker_forward_states: int
    attacker_backward_states: int
    attacker_forward_transitions: int
    attacker_backward_transitions: int
    meet_states: int
    recovered_connector_length: int
    endpoint_verified: bool
    matches_generator_certificate_after_public_success: bool | None
    attacker_state_fraction_of_generator_ball: float


def _source_params(params: HGA4CParameters) -> HGA4Parameters:
    return HGA4Parameters(params.name, params.exact_distance)


def _target_tiebreak(seed: bytes, params: HGA4CParameters, state: FreeState) -> bytes:
    encoded = b"\x1f".join(word.encode("ascii") for word in state)
    return hashlib.sha256(
        b"MORPH-KEM HGA4c shell target v1\x00"
        + seed
        + params.name.encode("ascii")
        + b"\x00"
        + encoded
    ).digest()


def _exact_shell(
    source: FreeState,
    distance: int,
    *,
    state_cap: int = 200_000,
    path_count_cap: int = 1_000_000_000,
) -> tuple[
    dict[FreeState, str],
    dict[FreeState, int],
    tuple[FreeState, ...],
    int,
]:
    seen: dict[FreeState, str] = {source: ""}
    path_counts: dict[FreeState, int] = {source: 1}
    frontier = [source]
    transitions = 0

    for depth in range(1, distance + 1):
        next_frontier: list[FreeState] = []
        for state in frontier:
            prefix = seen[state]
            for generator in _BRAID_GENERATORS:
                transitions += 1
                candidate = apply_hurwitz_generator(state, generator)
                if candidate not in seen:
                    seen[candidate] = prefix + generator
                    path_counts[candidate] = path_counts[state]
                    next_frontier.append(candidate)
                    if len(seen) > state_cap:
                        raise HGA4CError("HGA4c exact shell state cap exceeded")
                elif len(seen[candidate]) == depth:
                    path_counts[candidate] = min(
                        path_count_cap,
                        path_counts[candidate] + path_counts[state],
                    )
        frontier = next_frontier
        if not frontier:
            raise HGA4CError("HGA4c exact-distance shell became empty")

    return seen, path_counts, tuple(frontier), transitions


def generate_hga4c_instance(
    params: HGA4CParameters,
    master_seed: bytes,
) -> tuple[HGA4Public, HGA4CReference]:
    params.validate()
    if len(master_seed) < 16:
        raise HGA4CError("HGA4c master seed must contain at least 128 bits")

    source = _sample_source(_source_params(params), master_seed)
    seen, path_counts, shell, transitions = _exact_shell(source, params.exact_distance)
    target = min(
        shell,
        key=lambda state: (
            -sum(len(word) for word in state),
            _target_tiebreak(master_seed, params, state),
        ),
    )
    certificate = seen[target]
    if len(certificate) != params.exact_distance:
        raise HGA4CError("HGA4c selected target lost exact-distance certificate")
    if apply_braid_word(source, certificate) != target:
        raise HGA4CError("HGA4c shell certificate does not reproduce the target")
    if state_product(source) != state_product(target):
        raise HGA4CError("HGA4c generator violated the Hurwitz product invariant")

    public = HGA4Public(params.name, source, target, params.exact_distance)
    reference = HGA4CReference(
        selected_shortest_word=certificate,
        generator_ball_states=len(seen),
        generator_shell_states=len(shell),
        generator_transitions=transitions,
        selected_target_total_length=sum(len(word) for word in target),
        shortest_path_multiplicity=path_counts[target],
    )
    return public, reference


def recover_hga4c(
    public: HGA4Public,
    *,
    reference: HGA4CReference | None = None,
) -> HGA4CRecovery:
    hga_reference = (
        None
        if reference is None
        else HGA4Reference(reference.selected_shortest_word)
    )
    recovered: HGA4Recovery = recover_hga4(public, reference=hga_reference)
    if recovered.recovered_connector_length != public.public_word_bound:
        raise HGA4CError("HGA4c public recovery contradicted exact shell distance")

    generator_ball = 0 if reference is None else reference.generator_ball_states
    generator_shell = 0 if reference is None else reference.generator_shell_states
    generator_transitions = 0 if reference is None else reference.generator_transitions
    target_total = sum(len(word) for word in public.target)
    multiplicity = 0 if reference is None else reference.shortest_path_multiplicity
    fraction = (
        0.0
        if generator_ball == 0
        else (recovered.forward_states + recovered.backward_states) / generator_ball
    )
    return HGA4CRecovery(
        exact_distance=public.public_word_bound,
        generator_ball_states=generator_ball,
        generator_shell_states=generator_shell,
        generator_transitions=generator_transitions,
        selected_target_total_length=target_total,
        shortest_path_multiplicity=multiplicity,
        attacker_forward_states=recovered.forward_states,
        attacker_backward_states=recovered.backward_states,
        attacker_forward_transitions=recovered.forward_transitions,
        attacker_backward_transitions=recovered.backward_transitions,
        meet_states=recovered.meet_states,
        recovered_connector_length=recovered.recovered_connector_length,
        endpoint_verified=recovered.endpoint_verified,
        matches_generator_certificate_after_public_success=(
            recovered.matches_planted_word_after_public_success
            if reference is not None
            else None
        ),
        attacker_state_fraction_of_generator_ball=fraction,
    )
