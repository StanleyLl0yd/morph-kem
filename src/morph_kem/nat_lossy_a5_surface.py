from __future__ import annotations

from dataclasses import dataclass
import hashlib

from .nat_a5 import (
    Permutation5,
    _A5,
    _IDENTITY,
    _cycle_type,
    compose,
    inverse,
)


class NAT9Error(ValueError):
    """Raised when a NAT9 lossy-representation experiment is malformed."""


def _class_label(value: Permutation5) -> str:
    cycle = _cycle_type(value)
    if cycle == ():
        return "identity"
    return "-".join(str(length) for length in cycle)


def _commutator(left: Permutation5, right: Permutation5) -> Permutation5:
    return compose(compose(compose(left, right), inverse(left)), inverse(right))


def _surface_relator(values: tuple[Permutation5, Permutation5, Permutation5, Permutation5]) -> Permutation5:
    a, b, c, d = values
    return compose(_commutator(a, b), _commutator(c, d))


def _product(left: Permutation5, right: Permutation5) -> Permutation5:
    return compose(left, right)


@dataclass(frozen=True, slots=True)
class NAT9Parameters:
    name: str
    observable_products: tuple[str, ...]
    max_generation_attempts: int = 4096

    def validate(self) -> None:
        allowed = {"ab", "cd", "ac", "bd"}
        if any(item not in allowed for item in self.observable_products):
            raise NAT9Error("NAT9 unknown product observable")
        if tuple(dict.fromkeys(self.observable_products)) != self.observable_products:
            raise NAT9Error("NAT9 product observables must be unique")
        if self.max_generation_attempts < 1 or self.max_generation_attempts > 65536:
            raise NAT9Error("NAT9 generation attempt cap outside toy bounds")


NAT9_PARAMETER_SETS = {
    "nat9-C4": NAT9Parameters("nat9-C4", ()),
    "nat9-P2": NAT9Parameters("nat9-P2", ("ab", "cd")),
    "nat9-X4": NAT9Parameters("nat9-X4", ("ab", "cd", "ac", "bd")),
}


@dataclass(frozen=True, slots=True)
class NAT9Public:
    name: str
    generator_classes: tuple[str, str, str, str]
    product_classes: tuple[tuple[str, str], ...]


@dataclass(frozen=True, slots=True)
class NAT9Reference:
    planted_generators: tuple[Permutation5, Permutation5, Permutation5, Permutation5]
    generation_attempts: int


@dataclass(frozen=True, slots=True)
class NAT9Recovery:
    accepted: bool
    recovered_generators: tuple[Permutation5, Permutation5, Permutation5, Permutation5] | None
    generator_candidate_sizes: tuple[int, int, int, int]
    left_pairs_considered: int
    left_pairs_retained: int
    right_pairs_considered: int
    right_pairs_retained: int
    relator_join_candidates: int
    verifier_candidates_tested: int
    accepted_representations: int
    recovered_matches_planted_after_public_success: bool | None


def _digest(seed: bytes, name: str, attempt: int, slot: int) -> bytes:
    return hashlib.sha256(
        b"MORPH-KEM NAT9 A5 surface v1\x00"
        + seed
        + name.encode("ascii")
        + attempt.to_bytes(8, "big")
        + slot.to_bytes(2, "big")
    ).digest()


def _deterministic_quadruple(seed: bytes, name: str, attempt: int) -> tuple[Permutation5, Permutation5, Permutation5, Permutation5]:
    values = tuple(
        _A5[int.from_bytes(_digest(seed, name, attempt, slot)[:8], "big") % len(_A5)]
        for slot in range(4)
    )
    return values  # type: ignore[return-value]


def _product_value(values: tuple[Permutation5, Permutation5, Permutation5, Permutation5], label: str) -> Permutation5:
    a, b, c, d = values
    pairs = {
        "ab": (a, b),
        "cd": (c, d),
        "ac": (a, c),
        "bd": (b, d),
    }
    left, right = pairs[label]
    return _product(left, right)


def generate_nat9_instance(
    params: NAT9Parameters,
    master_seed: bytes,
) -> tuple[NAT9Public, NAT9Reference]:
    params.validate()
    if len(master_seed) < 16:
        raise NAT9Error("NAT9 master seed must contain at least 128 bits")

    selected = None
    attempts = 0
    for attempt in range(params.max_generation_attempts):
        attempts = attempt + 1
        values = _deterministic_quadruple(master_seed, params.name, attempt)
        if any(value == _IDENTITY for value in values):
            continue
        if _surface_relator(values) != _IDENTITY:
            continue
        selected = values
        break
    if selected is None:
        raise NAT9Error("NAT9 generation attempt cap exhausted")

    public = NAT9Public(
        name=params.name,
        generator_classes=tuple(_class_label(value) for value in selected),  # type: ignore[arg-type]
        product_classes=tuple(
            (label, _class_label(_product_value(selected, label)))
            for label in params.observable_products
        ),
    )
    return public, NAT9Reference(selected, attempts)


def validate_nat9_representation(
    public: NAT9Public,
    values: tuple[Permutation5, Permutation5, Permutation5, Permutation5],
) -> bool:
    if any(value == _IDENTITY for value in values):
        return False
    if tuple(_class_label(value) for value in values) != public.generator_classes:
        return False
    if _surface_relator(values) != _IDENTITY:
        return False
    expected = dict(public.product_classes)
    return all(
        _class_label(_product_value(values, label)) == class_label
        for label, class_label in expected.items()
    )


def _class_candidates(label: str) -> tuple[Permutation5, ...]:
    return tuple(value for value in _A5 if value != _IDENTITY and _class_label(value) == label)


def recover_nat9(
    public: NAT9Public,
    *,
    reference: NAT9Reference | None = None,
) -> NAT9Recovery:
    candidate_sets = tuple(_class_candidates(label) for label in public.generator_classes)
    if any(not values for values in candidate_sets):
        raise NAT9Error("NAT9 public class has no A5 candidates")
    a_values, b_values, c_values, d_values = candidate_sets
    product_classes = dict(public.product_classes)

    left_pairs: list[tuple[Permutation5, Permutation5, Permutation5]] = []
    left_considered = 0
    for a in a_values:
        for b in b_values:
            left_considered += 1
            if "ab" in product_classes and _class_label(_product(a, b)) != product_classes["ab"]:
                continue
            left_pairs.append((a, b, _commutator(a, b)))

    right_by_commutator: dict[Permutation5, list[tuple[Permutation5, Permutation5]]] = {}
    right_considered = 0
    right_retained = 0
    for c in c_values:
        for d in d_values:
            right_considered += 1
            if "cd" in product_classes and _class_label(_product(c, d)) != product_classes["cd"]:
                continue
            right_retained += 1
            right_by_commutator.setdefault(_commutator(c, d), []).append((c, d))

    accepted_count = 0
    first = None
    join_candidates = 0
    verifier_tests = 0
    for a, b, left_commutator in left_pairs:
        needed = inverse(left_commutator)
        for c, d in right_by_commutator.get(needed, ()):
            join_candidates += 1
            values = (a, b, c, d)
            if "ac" in product_classes and _class_label(_product(a, c)) != product_classes["ac"]:
                continue
            if "bd" in product_classes and _class_label(_product(b, d)) != product_classes["bd"]:
                continue
            verifier_tests += 1
            if not validate_nat9_representation(public, values):
                continue
            accepted_count += 1
            if first is None:
                first = values

    matches = None
    if first is not None and reference is not None:
        matches = first == reference.planted_generators

    return NAT9Recovery(
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
        recovered_matches_planted_after_public_success=matches,
    )
