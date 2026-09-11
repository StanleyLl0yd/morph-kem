from __future__ import annotations

from dataclasses import dataclass
import hashlib


class HGAError(ValueError):
    """Raised when an HGA toy-control input is invalid."""


def _digest(domain: bytes, seed: bytes, name: str, counter: int = 0) -> bytes:
    return hashlib.sha256(
        domain + b"\x00" + seed + name.encode("ascii") + counter.to_bytes(8, "big")
    ).digest()


def _seeded_order(size: int, domain: bytes, seed: bytes, name: str) -> tuple[int, ...]:
    return tuple(
        sorted(
            range(size),
            key=lambda index: (_digest(domain, seed, name, index), index),
        )
    )


@dataclass(frozen=True, slots=True)
class LinearActionParameters:
    name: str
    dimension: int
    secret_weight: int

    def validate(self) -> None:
        if self.dimension < 4 or self.dimension > 64:
            raise HGAError("HGA0 linear dimension outside toy bounds")
        if self.secret_weight < 1 or self.secret_weight > self.dimension:
            raise HGAError("HGA0 linear secret weight outside toy bounds")


HGA0_LINEAR_PARAMETER_SETS = {
    "hga0-linear-8": LinearActionParameters("hga0-linear-8", 8, 3),
    "hga0-linear-16": LinearActionParameters("hga0-linear-16", 16, 5),
    "hga0-linear-24": LinearActionParameters("hga0-linear-24", 24, 7),
}


@dataclass(frozen=True, slots=True)
class LinearActionPublicInstance:
    name: str
    dimension: int
    x: int
    y: int


@dataclass(frozen=True, slots=True)
class LinearActionReference:
    secret_mask: int


@dataclass(frozen=True, slots=True)
class LinearActionRecovery:
    recovered_secret_mask: int
    recovered_word: tuple[int, ...]
    representation_rank: int
    xor_operations: int
    accepted: bool
    matches_reference_after_public_success: bool | None


def _mask_for_dimension(dimension: int) -> int:
    return (1 << dimension) - 1


def apply_linear_action(public_x: int, secret_mask: int, dimension: int) -> int:
    mask = _mask_for_dimension(dimension)
    if public_x < 0 or public_x > mask or secret_mask < 0 or secret_mask > mask:
        raise HGAError("HGA0 linear state outside public dimension")
    return public_x ^ secret_mask


def generate_linear_action_instance(
    params: LinearActionParameters,
    master_seed: bytes,
) -> tuple[LinearActionPublicInstance, LinearActionReference]:
    params.validate()
    if len(master_seed) < 16:
        raise HGAError("HGA0 master seed must contain at least 128 bits")

    mask = _mask_for_dimension(params.dimension)
    x = int.from_bytes(
        _digest(b"MORPH-KEM HGA0 linear public x v1", master_seed, params.name),
        "big",
    ) & mask
    positions = _seeded_order(
        params.dimension,
        b"MORPH-KEM HGA0 linear secret order v1",
        master_seed,
        params.name,
    )[: params.secret_weight]
    secret_mask = sum(1 << position for position in positions)
    public = LinearActionPublicInstance(
        name=params.name,
        dimension=params.dimension,
        x=x,
        y=apply_linear_action(x, secret_mask, params.dimension),
    )
    return public, LinearActionReference(secret_mask=secret_mask)


def recover_linear_action(
    public: LinearActionPublicInstance,
    *,
    reference: LinearActionReference | None = None,
) -> LinearActionRecovery:
    mask = _mask_for_dimension(public.dimension)
    if public.x < 0 or public.x > mask or public.y < 0 or public.y > mask:
        raise HGAError("HGA0 malformed public linear instance")

    recovered = public.x ^ public.y
    word = tuple(index for index in range(public.dimension) if (recovered >> index) & 1)
    accepted = apply_linear_action(public.x, recovered, public.dimension) == public.y
    matches = None if reference is None else recovered == reference.secret_mask
    return LinearActionRecovery(
        recovered_secret_mask=recovered,
        recovered_word=word,
        representation_rank=public.dimension,
        xor_operations=1,
        accepted=accepted,
        matches_reference_after_public_success=matches,
    )


@dataclass(frozen=True, slots=True)
class DihedralActionParameters:
    name: str
    polygon_size: int

    def validate(self) -> None:
        if self.polygon_size < 5 or self.polygon_size > 64:
            raise HGAError("HGA0 dihedral polygon size outside toy bounds")


HGA0_DIHEDRAL_PARAMETER_SETS = {
    "hga0-dihedral-9": DihedralActionParameters("hga0-dihedral-9", 9),
    "hga0-dihedral-17": DihedralActionParameters("hga0-dihedral-17", 17),
    "hga0-dihedral-25": DihedralActionParameters("hga0-dihedral-25", 25),
}


@dataclass(frozen=True, slots=True)
class DihedralElement:
    rotation: int
    reflected: bool


@dataclass(frozen=True, slots=True)
class DihedralActionPublicInstance:
    name: str
    labels: tuple[int, ...]
    transformed_labels: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class DihedralActionReference:
    element: DihedralElement


@dataclass(frozen=True, slots=True)
class DihedralActionRecovery:
    recovered_element: DihedralElement
    matching_elements: tuple[DihedralElement, ...]
    candidate_elements_tested: int
    label_checks: int
    stabilizer_size: int
    accepted: bool
    matches_reference_after_public_success: bool | None


def apply_dihedral_action(
    labels: tuple[int, ...],
    element: DihedralElement,
) -> tuple[int, ...]:
    size = len(labels)
    if size < 1:
        raise HGAError("HGA0 dihedral action needs a nonempty public object")
    rotation = element.rotation % size
    if element.reflected:
        return tuple(labels[(rotation - index) % size] for index in range(size))
    return tuple(labels[(index - rotation) % size] for index in range(size))


def generate_dihedral_action_instance(
    params: DihedralActionParameters,
    master_seed: bytes,
) -> tuple[DihedralActionPublicInstance, DihedralActionReference]:
    params.validate()
    if len(master_seed) < 16:
        raise HGAError("HGA0 master seed must contain at least 128 bits")

    labels = _seeded_order(
        params.polygon_size,
        b"MORPH-KEM HGA0 dihedral public labels v1",
        master_seed,
        params.name,
    )
    secret_bytes = _digest(
        b"MORPH-KEM HGA0 dihedral secret v1", master_seed, params.name
    )
    element = DihedralElement(
        rotation=int.from_bytes(secret_bytes[:4], "big") % params.polygon_size,
        reflected=bool(secret_bytes[4] & 1),
    )
    transformed = apply_dihedral_action(labels, element)
    return (
        DihedralActionPublicInstance(
            name=params.name,
            labels=labels,
            transformed_labels=transformed,
        ),
        DihedralActionReference(element=element),
    )


def recover_dihedral_action(
    public: DihedralActionPublicInstance,
    *,
    reference: DihedralActionReference | None = None,
) -> DihedralActionRecovery:
    if len(public.labels) != len(public.transformed_labels) or not public.labels:
        raise HGAError("HGA0 malformed public dihedral instance")
    if len(set(public.labels)) != len(public.labels):
        raise HGAError("HGA0 dihedral control expects unique public labels")

    size = len(public.labels)
    matching: list[DihedralElement] = []
    tested = 0
    label_checks = 0
    for reflected in (False, True):
        for rotation in range(size):
            tested += 1
            element = DihedralElement(rotation=rotation, reflected=reflected)
            candidate = apply_dihedral_action(public.labels, element)
            equal = True
            for left, right in zip(candidate, public.transformed_labels, strict=True):
                label_checks += 1
                if left != right:
                    equal = False
                    break
            if equal:
                matching.append(element)

    if not matching:
        raise HGAError("HGA0 dihedral public endpoints are not in one tested orbit")
    recovered = min(matching, key=lambda element: (element.reflected, element.rotation))

    stabilizer_size = 0
    identity_target = public.labels
    for reflected in (False, True):
        for rotation in range(size):
            element = DihedralElement(rotation=rotation, reflected=reflected)
            if apply_dihedral_action(public.labels, element) == identity_target:
                stabilizer_size += 1

    accepted = apply_dihedral_action(public.labels, recovered) == public.transformed_labels
    matches = None if reference is None else recovered == reference.element
    return DihedralActionRecovery(
        recovered_element=recovered,
        matching_elements=tuple(matching),
        candidate_elements_tested=tested,
        label_checks=label_checks,
        stabilizer_size=stabilizer_size,
        accepted=accepted,
        matches_reference_after_public_success=matches,
    )
