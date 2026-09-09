from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from .hyperbolic import (
    A5_ELEMENTS,
    A5_IDENTITY,
    A5PublicInstance,
    HyperbolicExperimentError,
    _allowed_right_values,
    validate_a5_frames,
)


@dataclass(frozen=True, slots=True)
class A5SatEncoding:
    vertex_count: int
    group_size: int
    variable_count: int
    clauses: tuple[tuple[int, ...], ...]

    def variable(self, vertex: int, value: int) -> int:
        if vertex < 0 or vertex >= self.vertex_count:
            raise HyperbolicExperimentError("SAT vertex outside scaffold")
        if value < 0 or value >= self.group_size:
            raise HyperbolicExperimentError("SAT A5 value outside domain")
        return vertex * self.group_size + value + 1

    def to_dimacs(self) -> str:
        lines = [f"p cnf {self.variable_count} {len(self.clauses)}"]
        lines.extend(
            " ".join(str(literal) for literal in clause) + " 0"
            for clause in self.clauses
        )
        return "\n".join(lines) + "\n"


@dataclass(frozen=True, slots=True)
class A5SatModel:
    frames: tuple[int, ...]
    accepted: bool


def encode_a5_sat(public: A5PublicInstance) -> A5SatEncoding:
    """Encode the exact H2 A5 equivalent-witness relation as CNF.

    Each vertex has one one-hot variable for every A5 element. Binary edge
    compatibility is represented by one implication clause per left endpoint
    value. Root frame 0 is fixed to the A5 identity to quotient the global
    gauge orbit.
    """
    vertex_count = len(public.scaffold.vertices)
    group_size = len(A5_ELEMENTS)
    variable_count = vertex_count * group_size

    def variable(vertex: int, value: int) -> int:
        return vertex * group_size + value + 1

    clauses: list[tuple[int, ...]] = []

    # Exactly one A5 frame per vertex.
    for vertex in range(vertex_count):
        clauses.append(
            tuple(variable(vertex, value) for value in range(group_size))
        )
        for left_value, right_value in combinations(range(group_size), 2):
            clauses.append(
                (
                    -variable(vertex, left_value),
                    -variable(vertex, right_value),
                )
            )

    # Choose one representative of the common-left-multiplication gauge orbit.
    clauses.append((variable(0, A5_IDENTITY),))

    # For a fixed left value, the right endpoint must be one of the exact
    # public compatibility values for that edge.
    for edge, label in zip(public.scaffold.edges, public.edge_labels):
        left, right = edge
        for left_value in range(group_size):
            allowed_right = tuple(
                sorted(
                    _allowed_right_values(
                        label,
                        left_value,
                        public.conjugacy_class,
                    )
                )
            )
            clauses.append(
                (-variable(left, left_value),)
                + tuple(variable(right, value) for value in allowed_right)
            )

    return A5SatEncoding(
        vertex_count=vertex_count,
        group_size=group_size,
        variable_count=variable_count,
        clauses=tuple(clauses),
    )


def frames_to_sat_literals(
    encoding: A5SatEncoding,
    frames: tuple[int, ...],
) -> tuple[int, ...]:
    if len(frames) != encoding.vertex_count:
        raise HyperbolicExperimentError("SAT frame count does not match vertices")
    if any(value < 0 or value >= encoding.group_size for value in frames):
        raise HyperbolicExperimentError("SAT frame outside A5")
    return tuple(
        encoding.variable(vertex, value)
        for vertex, value in enumerate(frames)
    )


def sat_encoding_accepts_frames(
    encoding: A5SatEncoding,
    frames: tuple[int, ...],
) -> bool:
    positive = set(frames_to_sat_literals(encoding, frames))
    for clause in encoding.clauses:
        satisfied = False
        for literal in clause:
            if literal > 0:
                satisfied = literal in positive
            else:
                satisfied = -literal not in positive
            if satisfied:
                break
        if not satisfied:
            return False
    return True


def decode_a5_sat_model(
    public: A5PublicInstance,
    encoding: A5SatEncoding,
    model_literals: tuple[int, ...],
) -> A5SatModel:
    positive = {literal for literal in model_literals if literal > 0}
    frames: list[int] = []
    for vertex in range(encoding.vertex_count):
        values = [
            value
            for value in range(encoding.group_size)
            if encoding.variable(vertex, value) in positive
        ]
        if len(values) != 1:
            raise HyperbolicExperimentError(
                "SAT model does not select exactly one A5 value per vertex"
            )
        frames.append(values[0])

    candidate = tuple(frames)
    accepted = (
        sat_encoding_accepts_frames(encoding, candidate)
        and validate_a5_frames(public, candidate).accepted
    )
    return A5SatModel(candidate, accepted)
