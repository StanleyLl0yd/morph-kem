from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import permutations
import hashlib
import json

from .hyperbolic import A5_ELEMENTS, A5_THREE_CYCLES
from .nonorientable_map import RegularCellMap, generate_n4_6_4_3_map

Permutation = tuple[int, ...]


class TwistedA5Error(ValueError):
    """Raised when a K2.0 orientation-twisted A5 calibration input is invalid."""


def _compose(after: Permutation, before: Permutation) -> Permutation:
    if len(after) != len(before):
        raise TwistedA5Error("permutation size mismatch")
    return tuple(after[before[index]] for index in range(len(before)))


def _inverse(permutation: Permutation) -> Permutation:
    result = [0] * len(permutation)
    for source, target in enumerate(permutation):
        result[target] = source
    return tuple(result)


def _parity(permutation: Permutation) -> int:
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return inversions & 1


A5_INDEX = {value: index for index, value in enumerate(A5_ELEMENTS)}
S5_ELEMENTS: tuple[Permutation, ...] = tuple(permutations(range(5)))
S5_INDEX = {value: index for index, value in enumerate(S5_ELEMENTS)}
S5_IDENTITY = S5_INDEX[tuple(range(5))]
ODD_REPRESENTATIVE: Permutation = (1, 0, 2, 3, 4)
ODD_REPRESENTATIVE_INDEX = S5_INDEX[ODD_REPRESENTATIVE]


def _a5_mul(left: int, right: int) -> int:
    return A5_INDEX[_compose(A5_ELEMENTS[left], A5_ELEMENTS[right])]


def _a5_inv(element: int) -> int:
    return A5_INDEX[_inverse(A5_ELEMENTS[element])]


def _alpha(element: int) -> int:
    """Apply the non-trivial outer automorphism represented by odd conjugation."""
    conjugated = _compose(
        ODD_REPRESENTATIVE,
        _compose(
            A5_ELEMENTS[element],
            _inverse(ODD_REPRESENTATIVE),
        ),
    )
    return A5_INDEX[conjugated]


def _alpha_power(element: int, orientation: int) -> int:
    if orientation not in (0, 1):
        raise TwistedA5Error("orientation must be a bit")
    return _alpha(element) if orientation else element


def _s5_mul(left: int, right: int) -> int:
    return S5_INDEX[_compose(S5_ELEMENTS[left], S5_ELEMENTS[right])]


def _s5_inv(element: int) -> int:
    return S5_INDEX[_inverse(S5_ELEMENTS[element])]


@dataclass(frozen=True, slots=True)
class TwistedElement:
    a5: int
    orientation: int

    def __post_init__(self) -> None:
        if self.a5 < 0 or self.a5 >= len(A5_ELEMENTS):
            raise TwistedA5Error("A5 component outside A5")
        if self.orientation not in (0, 1):
            raise TwistedA5Error("orientation component must be a bit")


def twisted_mul(left: TwistedElement, right: TwistedElement) -> TwistedElement:
    return TwistedElement(
        _a5_mul(
            left.a5,
            _alpha_power(right.a5, left.orientation),
        ),
        left.orientation ^ right.orientation,
    )


def embed_twisted_s5(element: TwistedElement) -> int:
    orientation_part = (
        ODD_REPRESENTATIVE
        if element.orientation
        else tuple(range(5))
    )
    permutation = _compose(
        A5_ELEMENTS[element.a5],
        orientation_part,
    )
    return S5_INDEX[permutation]


@dataclass(frozen=True, slots=True)
class SemidirectAudit:
    twisted_elements: int
    s5_image_elements: int
    multiplication_checks: int
    parity_checks: int
    bijective: bool
    homomorphic: bool
    orientation_equals_s5_parity: bool


@lru_cache(maxsize=1)
def audit_semidirect_product() -> SemidirectAudit:
    elements = tuple(
        TwistedElement(a5, orientation)
        for a5 in range(len(A5_ELEMENTS))
        for orientation in (0, 1)
    )
    image = {
        embed_twisted_s5(element)
        for element in elements
    }

    parity_checks = 0
    parity_ok = True
    for element in elements:
        parity_checks += 1
        parity_ok = parity_ok and (
            _parity(S5_ELEMENTS[embed_twisted_s5(element)])
            == element.orientation
        )

    multiplication_checks = 0
    homomorphic = True
    for left in elements:
        left_image = embed_twisted_s5(left)
        for right in elements:
            multiplication_checks += 1
            expected = embed_twisted_s5(
                twisted_mul(left, right)
            )
            actual = _s5_mul(
                left_image,
                embed_twisted_s5(right),
            )
            if expected != actual:
                homomorphic = False
                break
        if not homomorphic:
            break

    return SemidirectAudit(
        twisted_elements=len(elements),
        s5_image_elements=len(image),
        multiplication_checks=multiplication_checks,
        parity_checks=parity_checks,
        bijective=len(image) == len(S5_ELEMENTS) == len(elements),
        homomorphic=homomorphic,
        orientation_equals_s5_parity=parity_ok,
    )


@dataclass(frozen=True, slots=True)
class TwistedA5Public:
    base_map: RegularCellMap
    orientation_bits: tuple[int, ...]
    edge_labels: tuple[int, ...]
    allowed_class: tuple[int, ...]
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise TwistedA5Error("unsupported K2.0 instance version")
        edge_count = len(self.base_map.dual_edges)
        if len(self.orientation_bits) != edge_count:
            raise TwistedA5Error("orientation-bit count mismatch")
        if len(self.edge_labels) != edge_count:
            raise TwistedA5Error("edge-label count mismatch")
        if any(bit not in (0, 1) for bit in self.orientation_bits):
            raise TwistedA5Error("orientation bits must be binary")
        if any(label < 0 or label >= len(A5_ELEMENTS) for label in self.edge_labels):
            raise TwistedA5Error("edge label outside A5")
        if not self.allowed_class:
            raise TwistedA5Error("allowed A5 class must be non-empty")

    def encode(self) -> bytes:
        payload = {
            "allowed_class": list(self.allowed_class),
            "base_map": json.loads(self.base_map.encode().decode("ascii")),
            "edge_labels": list(self.edge_labels),
            "orientation_bits": list(self.orientation_bits),
            "version": self.version,
        }
        return json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")


@dataclass(frozen=True, slots=True)
class TwistedA5Reference:
    face_frames: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class FlatteningAudit:
    edges: int
    endpoint_assignments_checked: int
    relation_mismatches: int
    public_edge_parity_matches: int
    planted_twisted_accepted: bool
    planted_flattened_accepted: bool

    @property
    def exact_relation_match(self) -> bool:
        return self.relation_mismatches == 0


class _DeterministicRng:
    def __init__(self, seed: bytes):
        self._seed = seed
        self._counter = 0

    def randbelow(self, upper: int) -> int:
        if upper <= 0:
            raise ValueError("upper bound must be positive")
        while True:
            block = hashlib.sha256(
                b"MORPH-KEM K2 twisted A5 rng v1\x00"
                + self._seed
                + self._counter.to_bytes(8, "big")
            ).digest()
            self._counter += 1
            value = int.from_bytes(block, "big")
            limit = (1 << 256) - ((1 << 256) % upper)
            if value < limit:
                return value % upper


def _twisted_edge_accept(
    label: int,
    orientation: int,
    left_frame: int,
    right_frame: int,
    allowed: set[int],
) -> bool:
    normalized = _a5_mul(
        right_frame,
        _a5_mul(
            label,
            _alpha_power(_a5_inv(left_frame), orientation),
        ),
    )
    return normalized in allowed


def _flattened_edge_label(label: int, orientation: int) -> int:
    return embed_twisted_s5(TwistedElement(label, orientation))


def _flattened_allowed_set(
    allowed_class: tuple[int, ...],
    orientation: int,
) -> frozenset[int]:
    return frozenset(
        embed_twisted_s5(TwistedElement(value, orientation))
        for value in allowed_class
    )


def _flattened_edge_accept(
    label: int,
    orientation: int,
    left_frame: int,
    right_frame: int,
    allowed_class: tuple[int, ...],
) -> bool:
    left = embed_twisted_s5(TwistedElement(left_frame, 0))
    right = embed_twisted_s5(TwistedElement(right_frame, 0))
    transport = _flattened_edge_label(label, orientation)
    normalized = _s5_mul(
        right,
        _s5_mul(
            transport,
            _s5_inv(left),
        ),
    )
    return normalized in _flattened_allowed_set(
        allowed_class,
        orientation,
    )


def generate_twisted_a5_instance(
    master_seed: bytes,
) -> tuple[TwistedA5Public, TwistedA5Reference]:
    if not isinstance(master_seed, bytes) or not master_seed:
        raise TwistedA5Error("master_seed must be non-empty bytes")

    base_map = generate_n4_6_4_3_map()
    orientation_bits = tuple(
        edge.canonical_transition
        for edge in base_map.dual_edges
    )
    rng = _DeterministicRng(
        hashlib.sha256(
            b"MORPH-KEM K2 twisted A5 instance v1\x00"
            + master_seed
        ).digest()
    )
    frames = tuple(
        rng.randbelow(len(A5_ELEMENTS))
        for _ in base_map.faces
    )

    labels: list[int] = []
    for edge, orientation in zip(
        base_map.dual_edges,
        orientation_bits,
    ):
        canonical = A5_THREE_CYCLES[
            rng.randbelow(len(A5_THREE_CYCLES))
        ]
        left_frame = frames[edge.left_face]
        right_frame = frames[edge.right_face]
        label = _a5_mul(
            _a5_inv(right_frame),
            _a5_mul(
                canonical,
                _alpha_power(left_frame, orientation),
            ),
        )
        labels.append(label)

    public = TwistedA5Public(
        base_map=base_map,
        orientation_bits=orientation_bits,
        edge_labels=tuple(labels),
        allowed_class=A5_THREE_CYCLES,
    )
    reference = TwistedA5Reference(frames)

    if not validate_twisted_frames(public, reference.face_frames):
        raise TwistedA5Error("internal twisted A5 reference validation failed")
    if not validate_flattened_s5_frames(public, reference.face_frames):
        raise TwistedA5Error("internal S5 flattening validation failed")
    return public, reference


def validate_twisted_frames(
    public: TwistedA5Public,
    frames: tuple[int, ...],
) -> bool:
    if len(frames) != len(public.base_map.faces):
        return False
    if any(value < 0 or value >= len(A5_ELEMENTS) for value in frames):
        return False
    allowed = set(public.allowed_class)
    for edge, orientation, label in zip(
        public.base_map.dual_edges,
        public.orientation_bits,
        public.edge_labels,
    ):
        if not _twisted_edge_accept(
            label,
            orientation,
            frames[edge.left_face],
            frames[edge.right_face],
            allowed,
        ):
            return False
    return True


def validate_flattened_s5_frames(
    public: TwistedA5Public,
    frames: tuple[int, ...],
) -> bool:
    if len(frames) != len(public.base_map.faces):
        return False
    if any(value < 0 or value >= len(A5_ELEMENTS) for value in frames):
        return False
    for edge, orientation, label in zip(
        public.base_map.dual_edges,
        public.orientation_bits,
        public.edge_labels,
    ):
        if not _flattened_edge_accept(
            label,
            orientation,
            frames[edge.left_face],
            frames[edge.right_face],
            public.allowed_class,
        ):
            return False
    return True


def flattened_public_edge_labels(
    public: TwistedA5Public,
) -> tuple[int, ...]:
    return tuple(
        _flattened_edge_label(label, orientation)
        for label, orientation in zip(
            public.edge_labels,
            public.orientation_bits,
        )
    )


def audit_twisted_flattening(
    public: TwistedA5Public,
    reference: TwistedA5Reference,
) -> FlatteningAudit:
    mismatches = 0
    checked = 0
    allowed = set(public.allowed_class)

    for orientation, label in zip(
        public.orientation_bits,
        public.edge_labels,
    ):
        for left_frame in range(len(A5_ELEMENTS)):
            for right_frame in range(len(A5_ELEMENTS)):
                checked += 1
                twisted = _twisted_edge_accept(
                    label,
                    orientation,
                    left_frame,
                    right_frame,
                    allowed,
                )
                flattened = _flattened_edge_accept(
                    label,
                    orientation,
                    left_frame,
                    right_frame,
                    public.allowed_class,
                )
                if twisted != flattened:
                    mismatches += 1

    flattened_labels = flattened_public_edge_labels(public)
    parity_matches = sum(
        _parity(S5_ELEMENTS[label]) == orientation
        for label, orientation in zip(
            flattened_labels,
            public.orientation_bits,
        )
    )

    return FlatteningAudit(
        edges=len(public.base_map.dual_edges),
        endpoint_assignments_checked=checked,
        relation_mismatches=mismatches,
        public_edge_parity_matches=parity_matches,
        planted_twisted_accepted=validate_twisted_frames(
            public,
            reference.face_frames,
        ),
        planted_flattened_accepted=validate_flattened_s5_frames(
            public,
            reference.face_frames,
        ),
    )
