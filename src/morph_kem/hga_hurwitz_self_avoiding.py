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
    generate_hga4_instance,
    recover_hga4,
    state_product,
)


class HGA4BError(HGA4Error):
    """Raised when the HGA4b self-avoiding toy generator is malformed."""


@dataclass(frozen=True, slots=True)
class HGA4BParameters:
    name: str
    planted_word_length: int

    def validate(self) -> None:
        if self.planted_word_length < 4 or self.planted_word_length > 20:
            raise HGA4BError("HGA4b planted word length outside declared toy bounds")

    @property
    def paired_hga4_name(self) -> str:
        return f"hga4-L{self.planted_word_length}"


HGA4B_PARAMETER_SETS = {
    "hga4b-L8": HGA4BParameters("hga4b-L8", 8),
    "hga4b-L12": HGA4BParameters("hga4b-L12", 12),
    "hga4b-L16": HGA4BParameters("hga4b-L16", 16),
    "hga4b-L20": HGA4BParameters("hga4b-L20", 20),
}


@dataclass(frozen=True, slots=True)
class HGA4BReference:
    planted_word: str
    path_states: tuple[FreeState, ...]
    dead_end_count: int

    @property
    def distinct_path_states(self) -> int:
        return len(set(self.path_states))


@dataclass(frozen=True, slots=True)
class HGA4BPairedRecovery:
    self_avoiding: HGA4Recovery
    locally_reduced: HGA4Recovery
    self_avoiding_distinct_path_states: int
    self_avoiding_dead_end_count: int


def _source_parameters(params: HGA4BParameters) -> HGA4Parameters:
    return HGA4Parameters(params.paired_hga4_name, params.planted_word_length)


def _generator_order(
    params: HGA4BParameters,
    seed: bytes,
    step: int,
    state: FreeState,
) -> tuple[str, ...]:
    state_bytes = b"\x1f".join(word.encode("ascii") for word in state)

    def key(generator: str) -> tuple[bytes, str]:
        digest = hashlib.sha256(
            b"MORPH-KEM HGA4b self-avoiding order v1\x00"
            + seed
            + params.name.encode("ascii")
            + step.to_bytes(4, "big")
            + generator.encode("ascii")
            + b"\x00"
            + state_bytes
        ).digest()
        return digest, generator

    return tuple(sorted(_BRAID_GENERATORS, key=key))


def _self_avoiding_word(
    params: HGA4BParameters,
    seed: bytes,
    source: FreeState,
) -> tuple[str, tuple[FreeState, ...]]:
    current = source
    states: list[FreeState] = [source]
    visited = {source}
    word: list[str] = []

    for step in range(params.planted_word_length):
        chosen_generator: str | None = None
        chosen_state: FreeState | None = None
        for generator in _generator_order(params, seed, step, current):
            candidate = apply_hurwitz_generator(current, generator)
            if candidate in visited:
                continue
            chosen_generator = generator
            chosen_state = candidate
            break
        if chosen_generator is None or chosen_state is None:
            raise HGA4BError(
                f"HGA4b self-avoiding generator reached a dead end at step {step}"
            )
        word.append(chosen_generator)
        current = chosen_state
        states.append(current)
        visited.add(current)

    return "".join(word), tuple(states)


def generate_hga4b_instance(
    params: HGA4BParameters,
    master_seed: bytes,
) -> tuple[HGA4Public, HGA4BReference]:
    params.validate()
    if len(master_seed) < 16:
        raise HGA4BError("HGA4b master seed must contain at least 128 bits")

    source = _sample_source(_source_parameters(params), master_seed)
    planted, path_states = _self_avoiding_word(params, master_seed, source)
    target = path_states[-1]

    if apply_braid_word(source, planted) != target:
        raise HGA4BError("HGA4b planted word does not reproduce generated target")
    if len(set(path_states)) != len(path_states):
        raise HGA4BError("HGA4b generated path is not self-avoiding")
    if state_product(source) != state_product(target):
        raise HGA4BError("HGA4b generator violated the Hurwitz product invariant")

    return (
        HGA4Public(params.name, source, target, params.planted_word_length),
        HGA4BReference(planted, path_states, 0),
    )


def recover_hga4b(
    public: HGA4Public,
    *,
    reference: HGA4BReference | None = None,
) -> HGA4Recovery:
    hga4_reference = None if reference is None else HGA4Reference(reference.planted_word)
    return recover_hga4(public, reference=hga4_reference)


def recover_hga4b_paired(
    params: HGA4BParameters,
    master_seed: bytes,
) -> HGA4BPairedRecovery:
    public, reference = generate_hga4b_instance(params, master_seed)
    self_avoiding = recover_hga4b(public, reference=reference)

    paired_params = _source_parameters(params)
    old_public, old_reference = generate_hga4_instance(paired_params, master_seed)
    if old_public.source != public.source:
        raise HGA4BError("HGA4b paired control did not preserve the source state")
    locally_reduced = recover_hga4(old_public, reference=old_reference)

    return HGA4BPairedRecovery(
        self_avoiding=self_avoiding,
        locally_reduced=locally_reduced,
        self_avoiding_distinct_path_states=reference.distinct_path_states,
        self_avoiding_dead_end_count=reference.dead_end_count,
    )
