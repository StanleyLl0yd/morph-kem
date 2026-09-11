from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import hashlib

from .hga_actions import HGAError


@dataclass(frozen=True, slots=True)
class HeisenbergElement:
    x: int
    y: int
    z: int


@dataclass(frozen=True, slots=True)
class HeisenbergState:
    g: HeisenbergElement
    h: HeisenbergElement


@dataclass(frozen=True, slots=True)
class HGA1Parameters:
    name: str
    prime: int
    secret_word_length: int

    def validate(self) -> None:
        if self.prime not in (5, 7, 11):
            raise HGAError("HGA1 prime outside calibrated toy set")
        if self.secret_word_length < 4 or self.secret_word_length > 20:
            raise HGAError("HGA1 secret word length outside toy bounds")


HGA1_PARAMETER_SETS = {
    "hga1-p5": HGA1Parameters("hga1-p5", 5, 8),
    "hga1-p7": HGA1Parameters("hga1-p7", 7, 10),
    "hga1-p11": HGA1Parameters("hga1-p11", 11, 12),
}


MOVES = ("L", "l", "R", "r")
INVERSE_MOVE = {"L": "l", "l": "L", "R": "r", "r": "R"}


@dataclass(frozen=True, slots=True)
class HGA1PublicInstance:
    name: str
    prime: int
    source: HeisenbergState
    target: HeisenbergState
    public_word_bound: int


@dataclass(frozen=True, slots=True)
class HGA1Reference:
    secret_word: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class HGA1Recovery:
    quotient_orbit_size: int
    quotient_bfs_transitions: int
    quotient_shortest_length: int
    forward_states: int
    backward_states: int
    mitm_transitions: int
    meet_states: int
    recovered_word: tuple[str, ...]
    recovered_length: int
    accepted: bool
    matches_reference_after_public_success: bool | None


def _mod(value: int, prime: int) -> int:
    return value % prime


def multiply(left: HeisenbergElement, right: HeisenbergElement, prime: int) -> HeisenbergElement:
    return HeisenbergElement(
        _mod(left.x + right.x, prime),
        _mod(left.y + right.y, prime),
        _mod(left.z + right.z + left.x * right.y, prime),
    )


def inverse(value: HeisenbergElement, prime: int) -> HeisenbergElement:
    return HeisenbergElement(
        _mod(-value.x, prime),
        _mod(-value.y, prime),
        _mod(-value.z + value.x * value.y, prime),
    )


def apply_move(state: HeisenbergState, move: str, prime: int) -> HeisenbergState:
    if move == "L":
        return HeisenbergState(multiply(state.g, state.h, prime), state.h)
    if move == "l":
        return HeisenbergState(multiply(state.g, inverse(state.h, prime), prime), state.h)
    if move == "R":
        return HeisenbergState(state.g, multiply(state.h, state.g, prime))
    if move == "r":
        return HeisenbergState(state.g, multiply(state.h, inverse(state.g, prime), prime))
    raise HGAError(f"HGA1 unknown move: {move}")


def apply_word(state: HeisenbergState, word: tuple[str, ...], prime: int) -> HeisenbergState:
    result = state
    for move in word:
        result = apply_move(result, move, prime)
    return result


def invert_word(word: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(INVERSE_MOVE[move] for move in reversed(word))


def _digest(domain: bytes, seed: bytes, name: str, counter: int = 0) -> bytes:
    return hashlib.sha256(
        domain + b"\x00" + seed + name.encode("ascii") + counter.to_bytes(8, "big")
    ).digest()


def _secret_word(params: HGA1Parameters, seed: bytes) -> tuple[str, ...]:
    word: list[str] = []
    counter = 0
    while len(word) < params.secret_word_length:
        block = _digest(b"MORPH-KEM HGA1 secret word v1", seed, params.name, counter)
        counter += 1
        move = MOVES[block[0] % len(MOVES)]
        if word and INVERSE_MOVE[move] == word[-1]:
            continue
        word.append(move)
    return tuple(word)


def generate_hga1_instance(
    params: HGA1Parameters,
    master_seed: bytes,
) -> tuple[HGA1PublicInstance, HGA1Reference]:
    params.validate()
    if len(master_seed) < 16:
        raise HGAError("HGA1 master seed must contain at least 128 bits")
    p = params.prime
    z_bytes = _digest(b"MORPH-KEM HGA1 source center v1", master_seed, params.name)
    source = HeisenbergState(
        HeisenbergElement(1, 0, z_bytes[0] % p),
        HeisenbergElement(0, 1, z_bytes[1] % p),
    )
    word = _secret_word(params, master_seed)
    target = apply_word(source, word, p)
    return (
        HGA1PublicInstance(
            name=params.name,
            prime=p,
            source=source,
            target=target,
            public_word_bound=params.secret_word_length,
        ),
        HGA1Reference(secret_word=word),
    )


def _quotient(state: HeisenbergState) -> tuple[int, int, int, int]:
    return state.g.x, state.g.y, state.h.x, state.h.y


def _quotient_move(state: tuple[int, int, int, int], move: str, prime: int) -> tuple[int, int, int, int]:
    gx, gy, hx, hy = state
    if move == "L":
        return (_mod(gx + hx, prime), _mod(gy + hy, prime), hx, hy)
    if move == "l":
        return (_mod(gx - hx, prime), _mod(gy - hy, prime), hx, hy)
    if move == "R":
        return (gx, gy, _mod(hx + gx, prime), _mod(hy + gy, prime))
    if move == "r":
        return (gx, gy, _mod(hx - gx, prime), _mod(hy - gy, prime))
    raise HGAError(f"HGA1 unknown quotient move: {move}")


def _quotient_bfs(
    public: HGA1PublicInstance,
) -> tuple[int, int, int]:
    start = _quotient(public.source)
    goal = _quotient(public.target)
    queue = deque([start])
    distance = {start: 0}
    transitions = 0
    shortest = -1
    while queue:
        current = queue.popleft()
        current_distance = distance[current]
        if current == goal and shortest < 0:
            shortest = current_distance
        for move in MOVES:
            transitions += 1
            nxt = _quotient_move(current, move, public.prime)
            if nxt in distance:
                continue
            distance[nxt] = current_distance + 1
            queue.append(nxt)
    if shortest < 0:
        raise HGAError("HGA1 quotient endpoint is outside the public quotient orbit")
    return len(distance), transitions, shortest


def _bounded_bfs(
    start: HeisenbergState,
    prime: int,
    depth: int,
) -> tuple[dict[HeisenbergState, tuple[str, ...]], int]:
    paths: dict[HeisenbergState, tuple[str, ...]] = {start: ()}
    queue = deque([start])
    transitions = 0
    while queue:
        current = queue.popleft()
        word = paths[current]
        if len(word) >= depth:
            continue
        for move in MOVES:
            transitions += 1
            if word and INVERSE_MOVE[move] == word[-1]:
                continue
            nxt = apply_move(current, move, prime)
            if nxt in paths:
                continue
            paths[nxt] = word + (move,)
            queue.append(nxt)
    return paths, transitions


def recover_hga1(
    public: HGA1PublicInstance,
    *,
    reference: HGA1Reference | None = None,
) -> HGA1Recovery:
    quotient_orbit, quotient_transitions, quotient_shortest = _quotient_bfs(public)
    forward_depth = public.public_word_bound // 2
    backward_depth = public.public_word_bound - forward_depth
    forward, forward_transitions = _bounded_bfs(public.source, public.prime, forward_depth)
    backward, backward_transitions = _bounded_bfs(public.target, public.prime, backward_depth)
    meets = sorted(
        set(forward) & set(backward),
        key=lambda state: (
            len(forward[state]) + len(backward[state]),
            forward[state],
            backward[state],
            state,
        ),
    )
    if not meets:
        raise HGAError("HGA1 bounded bidirectional search found no connector")
    meet = meets[0]
    recovered = forward[meet] + invert_word(backward[meet])
    accepted = apply_word(public.source, recovered, public.prime) == public.target
    matches = None if reference is None else recovered == reference.secret_word
    return HGA1Recovery(
        quotient_orbit_size=quotient_orbit,
        quotient_bfs_transitions=quotient_transitions,
        quotient_shortest_length=quotient_shortest,
        forward_states=len(forward),
        backward_states=len(backward),
        mitm_transitions=forward_transitions + backward_transitions,
        meet_states=len(meets),
        recovered_word=recovered,
        recovered_length=len(recovered),
        accepted=accepted,
        matches_reference_after_public_success=matches,
    )
