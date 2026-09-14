from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from functools import lru_cache
import hashlib


Point = tuple[int, int, int]
Word = tuple[int, ...]


class HGA1Error(ValueError):
    """Raised when an HGA-1 Markoff action experiment is malformed."""


@dataclass(frozen=True, slots=True)
class HGA1Parameters:
    name: str
    prime: int
    word_bound: int

    def validate(self) -> None:
        if self.prime not in (29, 43, 59):
            raise HGA1Error("HGA-1 fixes primes at 29/43/59")
        if self.word_bound not in (8, 16, 24):
            raise HGA1Error("HGA-1 fixes word bounds at 8/16/24")


HGA1_PARAMETER_SETS = {
    f"hga1-p{prime}-L{bound}": HGA1Parameters(
        f"hga1-p{prime}-L{bound}", prime, bound
    )
    for prime in (29, 43, 59)
    for bound in (8, 16, 24)
}


@dataclass(frozen=True, slots=True)
class HGA1Instance:
    params: HGA1Parameters
    source: Point
    target: Point
    planted_word: Word
    markoff_point_count: int
    generation_retries: int


@dataclass(frozen=True, slots=True)
class NavigationRecovery:
    accepted: bool
    recovered_word: Word
    recovered_length: int
    states_discovered: int
    states_expanded: int
    edge_scans: int


@dataclass(frozen=True, slots=True)
class MultiplicityResult:
    transporter_reduced_words_leq_bound: int
    stabilizer_nonempty_reduced_words_leq_bound: int


@dataclass(frozen=True, slots=True)
class HGA1Recovery:
    orbit_size: int
    orbit_edge_scans: int
    bfs: NavigationRecovery
    bidirectional: NavigationRecovery
    multiplicity: MultiplicityResult
    bfs_equals_planted_after_public_success: bool
    bidirectional_equals_planted_after_public_success: bool


def is_markoff_point(point: Point, prime: int) -> bool:
    x, y, z = point
    return (x * x + y * y + z * z - x * y * z) % prime == 0


def apply_generator(point: Point, generator: int, prime: int) -> Point:
    x, y, z = point
    if generator == 0:
        return ((y * z - x) % prime, y, z)
    if generator == 1:
        return (x, (x * z - y) % prime, z)
    if generator == 2:
        return (x, y, (x * y - z) % prime)
    raise HGA1Error("HGA-1 generator must be 0, 1 or 2")


def is_reduced_word(word: Word) -> bool:
    return all(
        generator in (0, 1, 2)
        and (index == 0 or generator != word[index - 1])
        for index, generator in enumerate(word)
    )


def apply_word(point: Point, word: Word, prime: int) -> Point:
    current = point
    for generator in word:
        current = apply_generator(current, generator, prime)
    return current


@lru_cache(maxsize=None)
def enumerate_markoff_points(prime: int) -> tuple[Point, ...]:
    if prime not in (29, 43, 59):
        raise HGA1Error("HGA-1 only enumerates the predeclared primes")
    points: list[Point] = []
    for x in range(prime):
        for y in range(prime):
            for z in range(prime):
                point = (x, y, z)
                if point != (0, 0, 0) and is_markoff_point(point, prime):
                    points.append(point)
    return tuple(points)


def _hash_int(seed: bytes, domain: bytes, counter: int) -> int:
    if not seed:
        raise HGA1Error("HGA-1 seed must be nonempty")
    digest = hashlib.sha256(
        b"MORPH-KEM HGA1 v1\x00"
        + domain
        + b"\x00"
        + seed
        + counter.to_bytes(8, "big")
    ).digest()
    return int.from_bytes(digest, "big")


def _reduced_word(seed: bytes, length: int, retry: int) -> Word:
    if length < 1:
        raise HGA1Error("HGA-1 planted word length must be positive")
    first = _hash_int(seed, b"word-first" + retry.to_bytes(4, "big"), 0) % 3
    word = [first]
    for index in range(1, length):
        choice = _hash_int(
            seed,
            b"word-next" + retry.to_bytes(4, "big"),
            index,
        ) % 2
        previous = word[-1]
        alternatives = tuple(g for g in (0, 1, 2) if g != previous)
        word.append(alternatives[choice])
    return tuple(word)


def generate_hga1_instance(params: HGA1Parameters, master_seed: bytes) -> HGA1Instance:
    params.validate()
    points = enumerate_markoff_points(params.prime)
    if not points:
        raise HGA1Error("HGA-1 Markoff point set is unexpectedly empty")
    source = points[_hash_int(master_seed, b"source", 0) % len(points)]
    for retry in range(256):
        word = _reduced_word(master_seed, params.word_bound, retry)
        target = apply_word(source, word, params.prime)
        if target != source:
            return HGA1Instance(
                params=params,
                source=source,
                target=target,
                planted_word=word,
                markoff_point_count=len(points),
                generation_retries=retry,
            )
    raise HGA1Error("HGA-1 could not generate a nontrivial public target")


def verify_action(
    prime: int,
    source: Point,
    target: Point,
    word_bound: int,
    candidate_word: Word,
) -> bool:
    if not (1 <= len(candidate_word) <= word_bound):
        return False
    if not is_reduced_word(candidate_word):
        return False
    if not is_markoff_point(source, prime) or not is_markoff_point(target, prime):
        return False
    return apply_word(source, candidate_word, prime) == target


def _reconstruct_path(
    parents: dict[Point, tuple[Point, int] | None],
    endpoint: Point,
) -> Word:
    reversed_word: list[int] = []
    current = endpoint
    while parents[current] is not None:
        parent, generator = parents[current]  # type: ignore[misc]
        reversed_word.append(generator)
        current = parent
    reversed_word.reverse()
    return tuple(reversed_word)


def shortest_bfs(
    prime: int,
    source: Point,
    target: Point,
    word_bound: int,
) -> NavigationRecovery:
    if source == target:
        return NavigationRecovery(False, (), 0, 1, 0, 0)
    parents: dict[Point, tuple[Point, int] | None] = {source: None}
    depths: dict[Point, int] = {source: 0}
    queue: deque[Point] = deque((source,))
    expanded = 0
    scans = 0
    while queue:
        current = queue.popleft()
        depth = depths[current]
        if depth >= word_bound:
            continue
        expanded += 1
        for generator in (0, 1, 2):
            scans += 1
            neighbour = apply_generator(current, generator, prime)
            if neighbour in parents:
                continue
            parents[neighbour] = (current, generator)
            depths[neighbour] = depth + 1
            if neighbour == target:
                word = _reconstruct_path(parents, neighbour)
                return NavigationRecovery(
                    verify_action(prime, source, target, word_bound, word),
                    word,
                    len(word),
                    len(parents),
                    expanded,
                    scans,
                )
            queue.append(neighbour)
    return NavigationRecovery(False, (), 0, len(parents), expanded, scans)


def _bounded_bfs_tree(
    prime: int,
    root: Point,
    radius: int,
) -> tuple[
    dict[Point, tuple[Point, int] | None],
    dict[Point, int],
    int,
    int,
]:
    parents: dict[Point, tuple[Point, int] | None] = {root: None}
    depths: dict[Point, int] = {root: 0}
    queue: deque[Point] = deque((root,))
    expanded = 0
    scans = 0
    while queue:
        current = queue.popleft()
        depth = depths[current]
        if depth >= radius:
            continue
        expanded += 1
        for generator in (0, 1, 2):
            scans += 1
            neighbour = apply_generator(current, generator, prime)
            if neighbour in parents:
                continue
            parents[neighbour] = (current, generator)
            depths[neighbour] = depth + 1
            queue.append(neighbour)
    return parents, depths, expanded, scans


def bidirectional_bfs(
    prime: int,
    source: Point,
    target: Point,
    word_bound: int,
) -> NavigationRecovery:
    if source == target:
        return NavigationRecovery(False, (), 0, 1, 0, 0)
    left_radius = (word_bound + 1) // 2
    right_radius = word_bound // 2
    left_parents, left_depths, left_expanded, left_scans = _bounded_bfs_tree(
        prime, source, left_radius
    )
    right_parents, right_depths, right_expanded, right_scans = _bounded_bfs_tree(
        prime, target, right_radius
    )
    intersections = set(left_parents).intersection(right_parents)
    if not intersections:
        return NavigationRecovery(
            False,
            (),
            0,
            len(left_parents) + len(right_parents),
            left_expanded + right_expanded,
            left_scans + right_scans,
        )
    meeting = min(
        intersections,
        key=lambda point: (left_depths[point] + right_depths[point], point),
    )
    left_word = _reconstruct_path(left_parents, meeting)
    right_word: list[int] = []
    current = meeting
    while right_parents[current] is not None:
        parent, generator = right_parents[current]  # type: ignore[misc]
        # Every V_i is an involution, so the same label moves child back to parent.
        right_word.append(generator)
        current = parent
    word = left_word + tuple(right_word)
    return NavigationRecovery(
        verify_action(prime, source, target, word_bound, word),
        word,
        len(word),
        len(set(left_parents).union(right_parents)),
        left_expanded + right_expanded,
        left_scans + right_scans,
    )


def orbit_size(prime: int, source: Point) -> tuple[int, int]:
    seen = {source}
    queue: deque[Point] = deque((source,))
    scans = 0
    while queue:
        current = queue.popleft()
        for generator in (0, 1, 2):
            scans += 1
            neighbour = apply_generator(current, generator, prime)
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append(neighbour)
    return len(seen), scans


def reduced_word_multiplicity(
    prime: int,
    source: Point,
    target: Point,
    word_bound: int,
) -> MultiplicityResult:
    # State is (public point, last generator).  Restricting transitions to a
    # different next generator counts exactly the verifier's reduced-word language.
    current: dict[tuple[Point, int], int] = {}
    transporter = 0
    stabilizer = 0
    for generator in (0, 1, 2):
        point = apply_generator(source, generator, prime)
        key = (point, generator)
        current[key] = current.get(key, 0) + 1
    for length in range(1, word_bound + 1):
        if length > 1:
            next_counts: dict[tuple[Point, int], int] = {}
            for (point, last_generator), count in current.items():
                for generator in (0, 1, 2):
                    if generator == last_generator:
                        continue
                    neighbour = apply_generator(point, generator, prime)
                    key = (neighbour, generator)
                    next_counts[key] = next_counts.get(key, 0) + count
            current = next_counts
        transporter += sum(
            count for (point, _), count in current.items() if point == target
        )
        stabilizer += sum(
            count for (point, _), count in current.items() if point == source
        )
    return MultiplicityResult(transporter, stabilizer)


def recover_hga1(instance: HGA1Instance) -> HGA1Recovery:
    params = instance.params
    public_orbit_size, orbit_scans = orbit_size(params.prime, instance.source)
    bfs = shortest_bfs(
        params.prime, instance.source, instance.target, params.word_bound
    )
    bidirectional = bidirectional_bfs(
        params.prime, instance.source, instance.target, params.word_bound
    )
    multiplicity = reduced_word_multiplicity(
        params.prime, instance.source, instance.target, params.word_bound
    )
    return HGA1Recovery(
        orbit_size=public_orbit_size,
        orbit_edge_scans=orbit_scans,
        bfs=bfs,
        bidirectional=bidirectional,
        multiplicity=multiplicity,
        bfs_equals_planted_after_public_success=(
            bfs.accepted and bfs.recovered_word == instance.planted_word
        ),
        bidirectional_equals_planted_after_public_success=(
            bidirectional.accepted
            and bidirectional.recovered_word == instance.planted_word
        ),
    )
