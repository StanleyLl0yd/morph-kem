from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import hashlib


Matrix2 = tuple[int, int, int, int]


class NAT10Error(ValueError):
    """Raised when a NAT10 noisy trace-sketch experiment is malformed."""


def identity() -> Matrix2:
    return (1, 0, 0, 1)


def multiply(left: Matrix2, right: Matrix2, p: int) -> Matrix2:
    a, b, c, d = left
    e, f, g, h = right
    return (
        (a * e + b * g) % p,
        (a * f + b * h) % p,
        (c * e + d * g) % p,
        (c * f + d * h) % p,
    )


def inverse(value: Matrix2, p: int) -> Matrix2:
    a, b, c, d = value
    if (a * d - b * c) % p != 1:
        raise NAT10Error("NAT10 inverse input is not in SL(2,p)")
    return (d % p, (-b) % p, (-c) % p, a % p)


def trace(value: Matrix2, p: int) -> int:
    return (value[0] + value[3]) % p


def commutator(left: Matrix2, right: Matrix2, p: int) -> Matrix2:
    return multiply(
        multiply(multiply(left, right, p), inverse(left, p), p),
        inverse(right, p),
        p,
    )


def surface_relator(values: tuple[Matrix2, Matrix2, Matrix2, Matrix2], p: int) -> Matrix2:
    a, b, c, d = values
    return multiply(commutator(a, b, p), commutator(c, d, p), p)


@lru_cache(maxsize=None)
def sl2_group(p: int) -> tuple[Matrix2, ...]:
    if p not in (5, 7):
        raise NAT10Error("NAT10 toy implementation supports only p=5 or p=7")
    values: list[Matrix2] = []
    for a in range(p):
        for b in range(p):
            for c in range(p):
                for d in range(p):
                    if (a * d - b * c) % p == 1:
                        values.append((a, b, c, d))
    expected = p * (p * p - 1)
    if len(values) != expected:
        raise NAT10Error("NAT10 SL(2,p) enumeration size mismatch")
    return tuple(values)


def cyclic_distance(left: int, right: int, p: int) -> int:
    forward = (left - right) % p
    backward = (right - left) % p
    return min(forward, backward)


_WORDS = {
    "A": (0,),
    "B": (1,),
    "C": (2,),
    "D": (3,),
    "AB": (0, 1),
    "CD": (2, 3),
    "AC": (0, 2),
    "BD": (1, 3),
}


def word_value(values: tuple[Matrix2, Matrix2, Matrix2, Matrix2], label: str, p: int) -> Matrix2:
    indices = _WORDS.get(label)
    if indices is None:
        raise NAT10Error("NAT10 unknown trace word")
    result = identity()
    for index in indices:
        result = multiply(result, values[index], p)
    return result


@dataclass(frozen=True, slots=True)
class NAT10Parameters:
    name: str
    p: int
    trace_words: tuple[str, ...]
    noise_radius: int = 1
    max_generation_attempts: int = 32768

    def validate(self) -> None:
        if self.p not in (5, 7):
            raise NAT10Error("NAT10 unsupported toy prime")
        if self.noise_radius != 1:
            raise NAT10Error("NAT10 first gate fixes noise radius at one")
        required = ("A", "B", "C", "D")
        if self.trace_words[:4] != required:
            raise NAT10Error("NAT10 trace word list must begin with A/B/C/D")
        if any(label not in _WORDS for label in self.trace_words):
            raise NAT10Error("NAT10 unknown trace word")
        if tuple(dict.fromkeys(self.trace_words)) != self.trace_words:
            raise NAT10Error("NAT10 trace words must be unique")
        if self.max_generation_attempts < 1 or self.max_generation_attempts > 131072:
            raise NAT10Error("NAT10 generation cap outside toy bounds")


NAT10_PARAMETER_SETS = {
    "nat10-p5-G4": NAT10Parameters("nat10-p5-G4", 5, ("A", "B", "C", "D")),
    "nat10-p5-X8": NAT10Parameters(
        "nat10-p5-X8", 5, ("A", "B", "C", "D", "AB", "CD", "AC", "BD")
    ),
    "nat10-p7-X8": NAT10Parameters(
        "nat10-p7-X8", 7, ("A", "B", "C", "D", "AB", "CD", "AC", "BD")
    ),
}


@dataclass(frozen=True, slots=True)
class NAT10Public:
    name: str
    p: int
    noise_radius: int
    trace_centers: tuple[tuple[str, int], ...]


@dataclass(frozen=True, slots=True)
class NAT10Reference:
    planted_generators: tuple[Matrix2, Matrix2, Matrix2, Matrix2]
    exact_traces: tuple[tuple[str, int], ...]
    noise_values: tuple[tuple[str, int], ...]
    generation_attempts: int


@dataclass(frozen=True, slots=True)
class NAT10Recovery:
    accepted: bool
    recovered_generators: tuple[Matrix2, Matrix2, Matrix2, Matrix2] | None
    generator_candidate_sizes: tuple[int, int, int, int]
    left_pairs_considered: int
    left_pairs_retained: int
    right_pairs_considered: int
    right_pairs_retained: int
    relator_join_candidates: int
    verifier_candidates_tested: int
    accepted_representations: int
    conjugacy_orbit_lower_bound: int
    recovered_matches_planted_after_public_success: bool | None


def _digest(domain: bytes, seed: bytes, name: str, counter: int, slot: int = 0) -> bytes:
    return hashlib.sha256(
        domain
        + b"\x00"
        + seed
        + name.encode("ascii")
        + counter.to_bytes(8, "big")
        + slot.to_bytes(4, "big")
    ).digest()


def _sample_quadruple(group: tuple[Matrix2, ...], seed: bytes, name: str, attempt: int) -> tuple[Matrix2, Matrix2, Matrix2, Matrix2]:
    values = tuple(
        group[
            int.from_bytes(
                _digest(b"MORPH-KEM NAT10 generator v1", seed, name, attempt, slot)[:8],
                "big",
            )
            % len(group)
        ]
        for slot in range(4)
    )
    return values  # type: ignore[return-value]


def generate_nat10_instance(
    params: NAT10Parameters,
    master_seed: bytes,
) -> tuple[NAT10Public, NAT10Reference]:
    params.validate()
    if len(master_seed) < 16:
        raise NAT10Error("NAT10 master seed must contain at least 128 bits")
    group = sl2_group(params.p)
    selected = None
    attempts = 0
    for attempt in range(params.max_generation_attempts):
        attempts = attempt + 1
        values = _sample_quadruple(group, master_seed, params.name, attempt)
        if any(value == identity() for value in values):
            continue
        if surface_relator(values, params.p) != identity():
            continue
        selected = values
        break
    if selected is None:
        raise NAT10Error("NAT10 generation attempt cap exhausted")

    exact: list[tuple[str, int]] = []
    noise: list[tuple[str, int]] = []
    centers: list[tuple[str, int]] = []
    width = 2 * params.noise_radius + 1
    for index, label in enumerate(params.trace_words):
        exact_trace = trace(word_value(selected, label, params.p), params.p)
        noise_value = (
            int.from_bytes(
                _digest(
                    b"MORPH-KEM NAT10 trace noise v1",
                    master_seed,
                    params.name,
                    0,
                    index,
                )[:8],
                "big",
            )
            % width
        ) - params.noise_radius
        center = (exact_trace + noise_value) % params.p
        exact.append((label, exact_trace))
        noise.append((label, noise_value))
        centers.append((label, center))

    public = NAT10Public(params.name, params.p, params.noise_radius, tuple(centers))
    reference = NAT10Reference(selected, tuple(exact), tuple(noise), attempts)
    if not validate_nat10_representation(public, selected):
        raise NAT10Error("NAT10 planted representation failed its noisy verifier")
    return public, reference


def validate_nat10_representation(
    public: NAT10Public,
    values: tuple[Matrix2, Matrix2, Matrix2, Matrix2],
) -> bool:
    p = public.p
    if any(value == identity() for value in values):
        return False
    if surface_relator(values, p) != identity():
        return False
    for label, center in public.trace_centers:
        observed = trace(word_value(values, label, p), p)
        if cyclic_distance(observed, center, p) > public.noise_radius:
            return False
    return True


def _generator_candidates(public: NAT10Public, label: str) -> tuple[Matrix2, ...]:
    centers = dict(public.trace_centers)
    center = centers[label]
    return tuple(
        value
        for value in sl2_group(public.p)
        if value != identity()
        and cyclic_distance(trace(value, public.p), center, public.p) <= public.noise_radius
    )


def recover_nat10(
    public: NAT10Public,
    *,
    reference: NAT10Reference | None = None,
) -> NAT10Recovery:
    p = public.p
    centers = dict(public.trace_centers)
    candidate_sets = tuple(_generator_candidates(public, label) for label in ("A", "B", "C", "D"))
    if any(not values for values in candidate_sets):
        raise NAT10Error("NAT10 noisy trace window has no generator candidates")
    a_values, b_values, c_values, d_values = candidate_sets

    def product_ok(left: Matrix2, right: Matrix2, label: str) -> bool:
        center = centers.get(label)
        if center is None:
            return True
        observed = trace(multiply(left, right, p), p)
        return cyclic_distance(observed, center, p) <= public.noise_radius

    left_pairs: list[tuple[Matrix2, Matrix2, Matrix2]] = []
    left_considered = 0
    for a in a_values:
        for b in b_values:
            left_considered += 1
            if not product_ok(a, b, "AB"):
                continue
            left_pairs.append((a, b, commutator(a, b, p)))

    right_by_commutator: dict[Matrix2, list[tuple[Matrix2, Matrix2]]] = {}
    right_considered = 0
    right_retained = 0
    for c in c_values:
        for d in d_values:
            right_considered += 1
            if not product_ok(c, d, "CD"):
                continue
            right_retained += 1
            right_by_commutator.setdefault(commutator(c, d, p), []).append((c, d))

    accepted_count = 0
    first = None
    join_candidates = 0
    verifier_tests = 0
    for a, b, left_commutator in left_pairs:
        needed = inverse(left_commutator, p)
        for c, d in right_by_commutator.get(needed, ()):
            join_candidates += 1
            if not product_ok(a, c, "AC") or not product_ok(b, d, "BD"):
                continue
            values = (a, b, c, d)
            verifier_tests += 1
            if not validate_nat10_representation(public, values):
                continue
            accepted_count += 1
            if first is None:
                first = values

    effective_conjugation_group = len(sl2_group(p)) // 2
    orbit_lower_bound = (
        (accepted_count + effective_conjugation_group - 1) // effective_conjugation_group
        if accepted_count
        else 0
    )
    matches = None
    if first is not None and reference is not None:
        matches = first == reference.planted_generators

    return NAT10Recovery(
        accepted=first is not None,
        recovered_generators=first,
        generator_candidate_sizes=tuple(len(values) for values in candidate_sets),  # type: ignore[arg-type]
        left_pairs_considered=left_considered,
        left_pairs_retained=len(left_pairs),
        right_pairs_considered=right_considered,
        right_pairs_retained=right_retained,
        relator_join_candidates=join_candidates,
        verifier_candidates_tested=verifier_tests,
        accepted_representations=accepted_count,
        conjugacy_orbit_lower_bound=orbit_lower_bound,
        recovered_matches_planted_after_public_success=matches,
    )
