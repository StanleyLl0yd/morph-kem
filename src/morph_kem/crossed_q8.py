from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import hashlib
import json

from .nonorientable_map import RegularCellMap, generate_n4_6_4_3_map

Permutation = tuple[int, ...]
Edge = tuple[int, int]


class CrossedQ8Error(ValueError):
    """Raised when a K2.2 Q8 crossed-module experiment input is invalid."""


# Q8 = {1,-1,i,-i,j,-j,k,-k}.
# Each entry is (sign, basis), with basis 0=1, 1=i, 2=j, 3=k.
Q8_DATA: tuple[tuple[int, int], ...] = (
    (1, 0),
    (-1, 0),
    (1, 1),
    (-1, 1),
    (1, 2),
    (-1, 2),
    (1, 3),
    (-1, 3),
)
Q8_INDEX = {value: index for index, value in enumerate(Q8_DATA)}
Q8_IDENTITY = 0
Q8_MINUS_ONE = 1


def _q8_neg(element: int) -> int:
    sign, basis = Q8_DATA[element]
    return Q8_INDEX[(-sign, basis)]


def _basis_mul(left: int, right: int) -> tuple[int, int]:
    if left == 0:
        return 1, right
    if right == 0:
        return 1, left
    if left == right:
        return -1, 0
    table = {
        (1, 2): (1, 3),
        (2, 3): (1, 1),
        (3, 1): (1, 2),
        (2, 1): (-1, 3),
        (3, 2): (-1, 1),
        (1, 3): (-1, 2),
    }
    return table[(left, right)]


def q8_mul(left: int, right: int) -> int:
    if left < 0 or left >= 8 or right < 0 or right >= 8:
        raise CrossedQ8Error("Q8 element outside range")
    left_sign, left_basis = Q8_DATA[left]
    right_sign, right_basis = Q8_DATA[right]
    product_sign, product_basis = _basis_mul(left_basis, right_basis)
    return Q8_INDEX[(left_sign * right_sign * product_sign, product_basis)]


def q8_inv(element: int) -> int:
    if element < 0 or element >= 8:
        raise CrossedQ8Error("Q8 element outside range")
    for candidate in range(8):
        if (
            q8_mul(element, candidate) == Q8_IDENTITY
            and q8_mul(candidate, element) == Q8_IDENTITY
        ):
            return candidate
    raise CrossedQ8Error("Q8 inverse not found")


def _compose(after: Permutation, before: Permutation) -> Permutation:
    return tuple(after[before[index]] for index in range(len(before)))


def _perm_inverse(permutation: Permutation) -> Permutation:
    result = [0] * len(permutation)
    for source, target in enumerate(permutation):
        result[target] = source
    return tuple(result)


def _automorphism_from_images(image_i: int, image_j: int) -> Permutation:
    image_k = q8_mul(image_i, image_j)
    mapping = [0] * 8
    mapping[Q8_IDENTITY] = Q8_IDENTITY
    mapping[Q8_MINUS_ONE] = Q8_MINUS_ONE
    mapping[2] = image_i
    mapping[3] = _q8_neg(image_i)
    mapping[4] = image_j
    mapping[5] = _q8_neg(image_j)
    mapping[6] = image_k
    mapping[7] = _q8_neg(image_k)
    result = tuple(mapping)
    if len(set(result)) != 8:
        raise CrossedQ8Error("candidate Q8 automorphism is not bijective")
    for left in range(8):
        for right in range(8):
            if result[q8_mul(left, right)] != q8_mul(result[left], result[right]):
                raise CrossedQ8Error("candidate does not preserve Q8 multiplication")
    return result


@lru_cache(maxsize=1)
def q8_automorphisms() -> tuple[Permutation, ...]:
    order_four = (2, 3, 4, 5, 6, 7)
    values: set[Permutation] = set()
    for image_i in order_four:
        excluded = {image_i, _q8_neg(image_i)}
        for image_j in order_four:
            if image_j in excluded:
                continue
            values.add(_automorphism_from_images(image_i, image_j))
    result = tuple(sorted(values))
    if len(result) != 24:
        raise CrossedQ8Error("Aut(Q8) enumeration did not produce 24 elements")
    return result


@lru_cache(maxsize=1)
def _aut_index() -> dict[Permutation, int]:
    return {value: index for index, value in enumerate(q8_automorphisms())}


def aut_identity() -> int:
    return _aut_index()[tuple(range(8))]


def aut_mul(left: int, right: int) -> int:
    automorphisms = q8_automorphisms()
    return _aut_index()[_compose(automorphisms[left], automorphisms[right])]


def aut_inv(element: int) -> int:
    automorphisms = q8_automorphisms()
    return _aut_index()[_perm_inverse(automorphisms[element])]


def aut_action(automorphism: int, element: int) -> int:
    return q8_automorphisms()[automorphism][element]


@lru_cache(maxsize=8)
def boundary(element: int) -> int:
    inverse = q8_inv(element)
    mapping = tuple(
        q8_mul(q8_mul(element, value), inverse)
        for value in range(8)
    )
    return _aut_index()[mapping]


@dataclass(frozen=True, slots=True)
class CrossedModuleAudit:
    q8_order: int
    automorphism_order: int
    kernel_size: int
    image_size: int
    cokernel_cosets: int
    first_identity_checks: int
    second_identity_checks: int
    identities_hold: bool


@lru_cache(maxsize=1)
def audit_crossed_module() -> CrossedModuleAudit:
    automorphisms = q8_automorphisms()
    identity = aut_identity()
    kernel = {element for element in range(8) if boundary(element) == identity}
    image = {boundary(element) for element in range(8)}

    unseen = set(range(len(automorphisms)))
    cosets = 0
    while unseen:
        representative = min(unseen)
        coset = {aut_mul(representative, member) for member in image}
        unseen -= coset
        cosets += 1

    first_checks = 0
    second_checks = 0
    identities_hold = True

    for automorphism in range(len(automorphisms)):
        for element in range(8):
            first_checks += 1
            left = boundary(aut_action(automorphism, element))
            right = aut_mul(
                aut_mul(automorphism, boundary(element)),
                aut_inv(automorphism),
            )
            if left != right:
                identities_hold = False

    for left in range(8):
        for right in range(8):
            second_checks += 1
            lhs = aut_action(boundary(left), right)
            rhs = q8_mul(q8_mul(left, right), q8_inv(left))
            if lhs != rhs:
                identities_hold = False

    return CrossedModuleAudit(
        q8_order=8,
        automorphism_order=len(automorphisms),
        kernel_size=len(kernel),
        image_size=len(image),
        cokernel_cosets=cosets,
        first_identity_checks=first_checks,
        second_identity_checks=second_checks,
        identities_hold=identities_hold,
    )


@dataclass(frozen=True, slots=True)
class Q8FakeFlatPublic:
    base_map: RegularCellMap
    edge_labels: tuple[int, ...]
    version: int = 1

    def __post_init__(self) -> None:
        if self.version != 1:
            raise CrossedQ8Error("unsupported K2.2 public version")
        if len(self.edge_labels) != len(self.base_map.edges):
            raise CrossedQ8Error("edge-label count mismatch")
        if any(value < 0 or value >= 24 for value in self.edge_labels):
            raise CrossedQ8Error("edge label outside Aut(Q8)")

    def encode(self) -> bytes:
        payload = {
            "base_map": json.loads(self.base_map.encode().decode("ascii")),
            "edge_labels": list(self.edge_labels),
            "version": self.version,
        }
        return json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")


@dataclass(frozen=True, slots=True)
class Q8FakeFlatReference:
    face_values: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class Q8LiftAttackResult:
    accepted: bool
    face_values: tuple[int, ...]
    fiber_sizes: tuple[int, ...]
    total_equivalent_witnesses: int
    boundary_image_faces: int
    nonidentity_curvatures: int
    edge_compositions: int
    q8_preimage_checks: int


class _DeterministicRng:
    def __init__(self, seed: bytes):
        self._seed = seed
        self._counter = 0

    def randbelow(self, upper: int) -> int:
        if upper <= 0:
            raise ValueError("upper bound must be positive")
        limit = (1 << 256) - ((1 << 256) % upper)
        while True:
            block = hashlib.sha256(
                b"MORPH-KEM K2.2 Q8 rng v1\x00"
                + self._seed
                + self._counter.to_bytes(8, "big")
            ).digest()
            self._counter += 1
            candidate = int.from_bytes(block, "big")
            if candidate < limit:
                return candidate % upper


def _edge_index(base_map: RegularCellMap) -> dict[Edge, int]:
    return {edge: index for index, edge in enumerate(base_map.edges)}


def face_boundary_holonomy(
    public: Q8FakeFlatPublic,
    face_index: int,
) -> int:
    if face_index < 0 or face_index >= len(public.base_map.faces):
        raise CrossedQ8Error("face index outside range")
    face = public.base_map.faces[face_index]
    edge_index = _edge_index(public.base_map)
    accumulated = aut_identity()
    for index, source in enumerate(face):
        target = face[(index + 1) % len(face)]
        edge = tuple(sorted((source, target)))
        label = public.edge_labels[edge_index[edge]]
        step = label if source < target else aut_inv(label)
        accumulated = aut_mul(step, accumulated)
    return accumulated


def face_boundary_preimages(
    public: Q8FakeFlatPublic,
    face_index: int,
) -> tuple[int, ...]:
    holonomy = face_boundary_holonomy(public, face_index)
    return tuple(element for element in range(8) if boundary(element) == holonomy)


def validate_fake_flatness(
    public: Q8FakeFlatPublic,
    face_values: tuple[int, ...],
) -> bool:
    if len(face_values) != len(public.base_map.faces):
        return False
    if any(value < 0 or value >= 8 for value in face_values):
        return False
    return all(
        boundary(face_value) == face_boundary_holonomy(public, face_index)
        for face_index, face_value in enumerate(face_values)
    )


def generate_q8_fake_flat_instance(
    master_seed: bytes,
) -> tuple[Q8FakeFlatPublic, Q8FakeFlatReference]:
    if not isinstance(master_seed, bytes) or not master_seed:
        raise CrossedQ8Error("master_seed must be non-empty bytes")

    base_map = generate_n4_6_4_3_map()
    image = tuple(sorted({boundary(element) for element in range(8)}))
    automorphism_count = len(q8_automorphisms())

    for attempt in range(256):
        rng = _DeterministicRng(
            hashlib.sha256(
                b"MORPH-KEM K2.2 generator v1\x00"
                + master_seed
                + attempt.to_bytes(4, "big")
            ).digest()
        )
        vertex_gauges = tuple(
            rng.randbelow(automorphism_count)
            for _ in base_map.vertices
        )
        labels: list[int] = []
        for left, right in base_map.edges:
            inner = image[rng.randbelow(len(image))]
            label = aut_mul(
                aut_inv(vertex_gauges[right]),
                aut_mul(inner, vertex_gauges[left]),
            )
            labels.append(label)

        public = Q8FakeFlatPublic(base_map, tuple(labels))
        preimages = tuple(
            face_boundary_preimages(public, face_index)
            for face_index in range(len(base_map.faces))
        )
        if any(len(values) != 2 for values in preimages):
            continue
        holonomies = tuple(
            face_boundary_holonomy(public, face_index)
            for face_index in range(len(base_map.faces))
        )
        if all(value == aut_identity() for value in holonomies):
            continue
        face_values = tuple(
            values[rng.randbelow(len(values))]
            for values in preimages
        )
        reference = Q8FakeFlatReference(face_values)
        if validate_fake_flatness(public, reference.face_values):
            return public, reference

    raise CrossedQ8Error("could not generate deterministic fake-flat Q8 instance")


def public_face_lift_attack(public: Q8FakeFlatPublic) -> Q8LiftAttackResult:
    image = {boundary(element) for element in range(8)}
    face_values: list[int] = []
    fiber_sizes: list[int] = []
    boundary_image_faces = 0
    nonidentity_curvatures = 0
    edge_compositions = 0
    q8_preimage_checks = 0
    total_equivalent_witnesses = 1

    for face_index, face in enumerate(public.base_map.faces):
        holonomy = face_boundary_holonomy(public, face_index)
        edge_compositions += len(face)
        if holonomy in image:
            boundary_image_faces += 1
        if holonomy != aut_identity():
            nonidentity_curvatures += 1
        preimages: list[int] = []
        for element in range(8):
            q8_preimage_checks += 1
            if boundary(element) == holonomy:
                preimages.append(element)
        fiber_sizes.append(len(preimages))
        if not preimages:
            return Q8LiftAttackResult(
                accepted=False,
                face_values=(),
                fiber_sizes=tuple(fiber_sizes),
                total_equivalent_witnesses=0,
                boundary_image_faces=boundary_image_faces,
                nonidentity_curvatures=nonidentity_curvatures,
                edge_compositions=edge_compositions,
                q8_preimage_checks=q8_preimage_checks,
            )
        total_equivalent_witnesses *= len(preimages)
        face_values.append(min(preimages))

    candidate = tuple(face_values)
    return Q8LiftAttackResult(
        accepted=validate_fake_flatness(public, candidate),
        face_values=candidate,
        fiber_sizes=tuple(fiber_sizes),
        total_equivalent_witnesses=total_equivalent_witnesses,
        boundary_image_faces=boundary_image_faces,
        nonidentity_curvatures=nonidentity_curvatures,
        edge_compositions=edge_compositions,
        q8_preimage_checks=q8_preimage_checks,
    )
