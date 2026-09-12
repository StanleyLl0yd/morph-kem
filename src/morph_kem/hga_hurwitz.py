from __future__ import annotations

from dataclasses import dataclass
import hashlib


class HGA4Error(ValueError):
    """Raised when an HGA4 toy action is malformed."""


FreeState = tuple[str, str, str]
AbelianVector = tuple[int, int]

_FREE_INVERSE = {"a": "A", "A": "a", "b": "B", "B": "b"}
_BRAID_INVERSE = {"p": "P", "P": "p", "q": "Q", "Q": "q"}
_BRAID_GENERATORS = ("p", "P", "q", "Q")
_FREE_ALPHABET = ("a", "A", "b", "B")


@dataclass(frozen=True, slots=True)
class HGA4Parameters:
    name: str
    planted_word_length: int

    def validate(self) -> None:
        if self.planted_word_length < 4 or self.planted_word_length > 24:
            raise HGA4Error("HGA4 planted word length outside toy bounds")


HGA4_PARAMETER_SETS = {
    "hga4-L8": HGA4Parameters("hga4-L8", 8),
    "hga4-L12": HGA4Parameters("hga4-L12", 12),
    "hga4-L16": HGA4Parameters("hga4-L16", 16),
}


@dataclass(frozen=True, slots=True)
class HGA4Public:
    name: str
    source: FreeState
    target: FreeState
    public_word_bound: int


@dataclass(frozen=True, slots=True)
class HGA4Reference:
    planted_word: str


@dataclass(frozen=True, slots=True)
class HGA4Recovery:
    planted_word_length: int
    source_component_lengths: tuple[int, int, int]
    target_component_lengths: tuple[int, int, int]
    invariant_product_length: int
    invariant_product_verified: bool
    source_abelianization: tuple[AbelianVector, AbelianVector, AbelianVector]
    target_abelianization: tuple[AbelianVector, AbelianVector, AbelianVector]
    recovered_strand_permutation: tuple[int, int, int]
    quotient_matches_planted: bool | None
    forward_depth: int
    backward_depth: int
    forward_states: int
    backward_states: int
    forward_transitions: int
    backward_transitions: int
    meet_states: int
    recovered_connector: str
    recovered_connector_length: int
    endpoint_verified: bool
    matches_planted_word_after_public_success: bool | None
    materially_shorter_than_planted: bool


def reduce_free_word(word: str) -> str:
    stack: list[str] = []
    for letter in word:
        if letter not in _FREE_INVERSE:
            raise HGA4Error(f"unknown free-group letter {letter!r}")
        if stack and _FREE_INVERSE[letter] == stack[-1]:
            stack.pop()
        else:
            stack.append(letter)
    return "".join(stack)


def inverse_free_word(word: str) -> str:
    return "".join(_FREE_INVERSE[letter] for letter in reversed(word))


def multiply_free_words(*words: str) -> str:
    return reduce_free_word("".join(words))


def abelianization(word: str) -> AbelianVector:
    reduced = reduce_free_word(word)
    return (
        reduced.count("a") - reduced.count("A"),
        reduced.count("b") - reduced.count("B"),
    )


def state_product(state: FreeState) -> str:
    return multiply_free_words(*state)


def apply_hurwitz_generator(state: FreeState, generator: str) -> FreeState:
    if generator not in _BRAID_INVERSE:
        raise HGA4Error(f"unknown braid generator {generator!r}")
    values = list(state)
    index = 0 if generator in ("p", "P") else 1
    left = values[index]
    right = values[index + 1]
    if generator in ("p", "q"):
        values[index] = multiply_free_words(left, right, inverse_free_word(left))
        values[index + 1] = left
    else:
        values[index] = right
        values[index + 1] = multiply_free_words(
            inverse_free_word(right), left, right
        )
    result = tuple(values)
    return result  # type: ignore[return-value]


def apply_braid_word(state: FreeState, word: str) -> FreeState:
    result = state
    for generator in word:
        result = apply_hurwitz_generator(result, generator)
    return result


def inverse_braid_word(word: str) -> str:
    try:
        return "".join(_BRAID_INVERSE[generator] for generator in reversed(word))
    except KeyError as exc:
        raise HGA4Error("HGA4 braid word contains an unknown generator") from exc


def _digest(domain: bytes, seed: bytes, name: str, counter: int = 0) -> bytes:
    return hashlib.sha256(
        domain + b"\x00" + seed + name.encode("ascii") + counter.to_bytes(8, "big")
    ).digest()


def _sample_source(params: HGA4Parameters, seed: bytes) -> FreeState:
    words: list[str] = []
    vectors: set[AbelianVector] = set()
    for counter in range(4096):
        digest = _digest(b"MORPH-KEM HGA4 source v1", seed, params.name, counter)
        length = 3 + digest[0] % 4
        candidate = reduce_free_word(
            "".join(_FREE_ALPHABET[digest[index + 1] % 4] for index in range(length))
        )
        if not candidate:
            continue
        vector = abelianization(candidate)
        if vector == (0, 0) or vector in vectors:
            continue
        words.append(candidate)
        vectors.add(vector)
        if len(words) == 3:
            state = tuple(words)
            return state  # type: ignore[return-value]
    raise HGA4Error("HGA4 failed to sample a source with distinct abelianization classes")


def _sample_braid_word(params: HGA4Parameters, seed: bytes) -> str:
    word: list[str] = []
    counter = 0
    while len(word) < params.planted_word_length:
        digest = _digest(b"MORPH-KEM HGA4 planted braid v1", seed, params.name, counter)
        counter += 1
        candidate = _BRAID_GENERATORS[int.from_bytes(digest[:8], "big") % 4]
        if word and _BRAID_INVERSE[word[-1]] == candidate:
            continue
        word.append(candidate)
    return "".join(word)


def generate_hga4_instance(
    params: HGA4Parameters,
    master_seed: bytes,
) -> tuple[HGA4Public, HGA4Reference]:
    params.validate()
    if len(master_seed) < 16:
        raise HGA4Error("HGA4 master seed must contain at least 128 bits")
    source = _sample_source(params, master_seed)
    planted = _sample_braid_word(params, master_seed)
    target = apply_braid_word(source, planted)
    if state_product(source) != state_product(target):
        raise HGA4Error("HGA4 generator violated the Hurwitz product invariant")
    return (
        HGA4Public(params.name, source, target, params.planted_word_length),
        HGA4Reference(planted),
    )


def _state_abelianization(
    state: FreeState,
) -> tuple[AbelianVector, AbelianVector, AbelianVector]:
    values = tuple(abelianization(word) for word in state)
    return values  # type: ignore[return-value]


def _strand_permutation(source: FreeState, target: FreeState) -> tuple[int, int, int]:
    source_vectors = _state_abelianization(source)
    target_vectors = _state_abelianization(target)
    if len(set(source_vectors)) != 3:
        raise HGA4Error("HGA4 source abelianization classes are not distinct")
    try:
        result = tuple(source_vectors.index(vector) for vector in target_vectors)
    except ValueError as exc:
        raise HGA4Error("HGA4 target abelianization is not a source permutation") from exc
    if sorted(result) != [0, 1, 2]:
        raise HGA4Error("HGA4 strand quotient is not a permutation")
    return result  # type: ignore[return-value]


def _word_permutation(word: str) -> tuple[int, int, int]:
    values = [0, 1, 2]
    for generator in word:
        if generator in ("p", "P"):
            values[0], values[1] = values[1], values[0]
        elif generator in ("q", "Q"):
            values[1], values[2] = values[2], values[1]
        else:
            raise HGA4Error(f"unknown braid generator {generator!r}")
    return tuple(values)  # type: ignore[return-value]


def _bfs_ball(
    start: FreeState,
    max_depth: int,
    *,
    state_cap: int = 200_000,
) -> tuple[dict[FreeState, str], int]:
    seen: dict[FreeState, str] = {start: ""}
    frontier = [start]
    transitions = 0
    for _ in range(max_depth):
        next_frontier: list[FreeState] = []
        for state in frontier:
            prefix = seen[state]
            for generator in _BRAID_GENERATORS:
                transitions += 1
                candidate = apply_hurwitz_generator(state, generator)
                if candidate in seen:
                    continue
                seen[candidate] = prefix + generator
                next_frontier.append(candidate)
                if len(seen) > state_cap:
                    raise HGA4Error("HGA4 MITM state cap exceeded")
        frontier = next_frontier
        if not frontier:
            break
    return seen, transitions


def recover_hga4(
    public: HGA4Public,
    *,
    reference: HGA4Reference | None = None,
) -> HGA4Recovery:
    forward_depth = public.public_word_bound // 2
    backward_depth = public.public_word_bound - forward_depth
    forward, forward_transitions = _bfs_ball(public.source, forward_depth)
    backward, backward_transitions = _bfs_ball(public.target, backward_depth)
    meets = set(forward).intersection(backward)
    if not meets:
        raise HGA4Error("HGA4 bounded MITM found no connector within public bound")

    candidates: list[tuple[int, str, FreeState]] = []
    for state in meets:
        connector = forward[state] + inverse_braid_word(backward[state])
        candidates.append((len(connector), connector, state))
    _, connector, _ = min(candidates)
    endpoint_verified = apply_braid_word(public.source, connector) == public.target

    source_product = state_product(public.source)
    target_product = state_product(public.target)
    permutation = _strand_permutation(public.source, public.target)
    quotient_match = None
    planted_match = None
    if reference is not None:
        quotient_match = permutation == _word_permutation(reference.planted_word)
        planted_match = connector == reference.planted_word

    return HGA4Recovery(
        planted_word_length=public.public_word_bound,
        source_component_lengths=tuple(len(word) for word in public.source),  # type: ignore[arg-type]
        target_component_lengths=tuple(len(word) for word in public.target),  # type: ignore[arg-type]
        invariant_product_length=len(source_product),
        invariant_product_verified=source_product == target_product,
        source_abelianization=_state_abelianization(public.source),
        target_abelianization=_state_abelianization(public.target),
        recovered_strand_permutation=permutation,
        quotient_matches_planted=quotient_match,
        forward_depth=forward_depth,
        backward_depth=backward_depth,
        forward_states=len(forward),
        backward_states=len(backward),
        forward_transitions=forward_transitions,
        backward_transitions=backward_transitions,
        meet_states=len(meets),
        recovered_connector=connector,
        recovered_connector_length=len(connector),
        endpoint_verified=endpoint_verified,
        matches_planted_word_after_public_success=planted_match,
        materially_shorter_than_planted=(len(connector) * 4 <= public.public_word_bound * 3),
    )
