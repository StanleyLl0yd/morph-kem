from __future__ import annotations

from dataclasses import dataclass
import hashlib
from itertools import combinations

from .tdc_random_overlay import (
    OverlayPair,
    TDC2G_PARAMETER_SETS,
    TDC2GError,
    TDC2GParameters,
    generate_tdc2g_instance,
)
from .tdc_sparse_faces import SparseFaceCode


class TDC3Error(TDC2GError):
    """Raised when a TDC3 matched decoder-work experiment is malformed."""


@dataclass(frozen=True, slots=True)
class TDC3Parameters:
    name: str
    base_name: str
    error_weights: tuple[int, ...]
    bitflip_max_iterations: int = 96
    exact_max_weight: int = 6

    def validate(self) -> None:
        if self.base_name not in TDC2G_PARAMETER_SETS:
            raise TDC3Error("unknown TDC2g base parameter set")
        if not self.error_weights:
            raise TDC3Error("TDC3 error-weight schedule is empty")
        if tuple(sorted(set(self.error_weights))) != self.error_weights:
            raise TDC3Error("TDC3 error weights must be sorted and distinct")
        if self.error_weights[0] < 1 or self.error_weights[-1] > self.exact_max_weight:
            raise TDC3Error("TDC3 error weights outside exact decoder bound")
        if self.exact_max_weight != 6:
            raise TDC3Error("TDC3 first gate fixes exact bound at weight six")
        if self.bitflip_max_iterations < 1 or self.bitflip_max_iterations > 512:
            raise TDC3Error("TDC3 bit-flip iteration cap outside toy bounds")


TDC3_PARAMETER_SETS = {
    "tdc3-n8": TDC3Parameters("tdc3-n8", "tdc2g-n8", (1, 2, 3, 4, 5, 6)),
    "tdc3-n9": TDC3Parameters("tdc3-n9", "tdc2g-n9", (1, 2, 3, 4, 5, 6)),
    "tdc3-n10": TDC3Parameters("tdc3-n10", "tdc2g-n10", (1, 2, 3, 4, 5, 6)),
}


@dataclass(frozen=True, slots=True)
class BitFlipRecovery:
    accepted: bool
    recovered_error_mask: int
    recovered_weight: int
    iterations: int
    score_evaluations: int
    syndrome_weight_initial: int
    syndrome_weight_final: int
    stopped_no_improvement: bool
    stopped_cycle: bool


@dataclass(frozen=True, slots=True)
class ExactSyndromeRecovery:
    accepted: bool
    recovered_error_mask: int
    recovered_weight: int
    subset_masks_indexed: int
    subset_masks_scanned: int
    syndrome_bucket_collisions: int
    candidate_pairs_tested: int


@dataclass(frozen=True, slots=True)
class DecoderPairRecovery:
    planted_weight: int
    planted_error_mask: int
    topology_bitflip: BitFlipRecovery
    random_bitflip: BitFlipRecovery
    topology_exact: ExactSyndromeRecovery
    random_exact: ExactSyndromeRecovery
    topology_exact_matches_planted_after_public_success: bool
    random_exact_matches_planted_after_public_success: bool


@dataclass(frozen=True, slots=True)
class TDC3Instance:
    params: TDC3Parameters
    pair: OverlayPair
    master_seed: bytes


def _digest(domain: bytes, seed: bytes, name: str, counter: int = 0) -> bytes:
    return hashlib.sha256(
        domain + b"\x00" + seed + name.encode("ascii") + counter.to_bytes(8, "big")
    ).digest()


def generate_tdc3_instance(params: TDC3Parameters, master_seed: bytes) -> TDC3Instance:
    params.validate()
    if len(master_seed) < 16:
        raise TDC3Error("TDC3 seed must contain at least 128 bits")
    pair = generate_tdc2g_instance(TDC2G_PARAMETER_SETS[params.base_name], master_seed)
    if len(pair.topology.columns) != len(pair.matched_random.columns):
        raise TDC3Error("TDC3 paired public column counts differ")
    return TDC3Instance(params, pair, master_seed)


def planted_error_mask(instance: TDC3Instance, weight: int) -> int:
    if weight not in instance.params.error_weights:
        raise TDC3Error("TDC3 requested error weight is not declared")
    column_count = len(instance.pair.topology.columns)
    if weight > column_count:
        raise TDC3Error("TDC3 error weight exceeds public column count")
    order = sorted(
        range(column_count),
        key=lambda index: (
            _digest(
                b"MORPH-KEM TDC3 common error support v1",
                instance.master_seed,
                instance.params.name,
                weight * column_count + index,
            ),
            index,
        ),
    )
    return sum(1 << index for index in order[:weight])


def syndrome(code: SparseFaceCode, error_mask: int) -> int:
    value = 0
    for index, column in enumerate(code.columns):
        if (error_mask >> index) & 1:
            value ^= column
    return value


def _verify_syndrome(code: SparseFaceCode, target: int, error_mask: int) -> bool:
    return syndrome(code, error_mask) == target


def bitflip_decode(
    code: SparseFaceCode,
    target_syndrome: int,
    max_iterations: int,
) -> BitFlipRecovery:
    residual = target_syndrome
    error_mask = 0
    initial_weight = residual.bit_count()
    seen = {residual}
    evaluations = 0
    stopped_no_improvement = False
    stopped_cycle = False
    iterations = 0

    while residual and iterations < max_iterations:
        best_index = -1
        best_gain = 0
        best_new_weight = residual.bit_count()
        for index, column in enumerate(code.columns):
            evaluations += 1
            new_residual = residual ^ column
            new_weight = new_residual.bit_count()
            gain = residual.bit_count() - new_weight
            candidate = (gain, -new_weight, -index)
            best = (best_gain, -best_new_weight, -best_index) if best_index >= 0 else None
            if gain > 0 and (best is None or candidate > best):
                best_index = index
                best_gain = gain
                best_new_weight = new_weight

        if best_index < 0:
            stopped_no_improvement = True
            break

        residual ^= code.columns[best_index]
        error_mask ^= 1 << best_index
        iterations += 1
        if residual in seen:
            stopped_cycle = True
            break
        seen.add(residual)

    accepted = residual == 0 and _verify_syndrome(code, target_syndrome, error_mask)
    return BitFlipRecovery(
        accepted=accepted,
        recovered_error_mask=error_mask,
        recovered_weight=error_mask.bit_count(),
        iterations=iterations,
        score_evaluations=evaluations,
        syndrome_weight_initial=initial_weight,
        syndrome_weight_final=residual.bit_count(),
        stopped_no_improvement=stopped_no_improvement,
        stopped_cycle=stopped_cycle,
    )


def _support_mask(indices: tuple[int, ...]) -> int:
    value = 0
    for index in indices:
        value |= 1 << index
    return value


def exact_syndrome_decode_leq6(
    code: SparseFaceCode,
    target_syndrome: int,
) -> ExactSyndromeRecovery:
    """Exact meet-in-the-middle decoder through total error weight six.

    Enumerate every public subset through weight three and index its syndrome.
    Pair two disjoint indexed subsets whose syndromes XOR to the target.  Scan all
    candidates to return the minimum-weight, then lexicographically smallest,
    syndrome-equivalent error.  The planted error is never consulted.
    """

    entries: list[tuple[int, int, int]] = []
    buckets: dict[int, list[tuple[int, int]]] = {}
    collision_count = 0
    column_count = len(code.columns)

    for weight in range(0, 4):
        for support in combinations(range(column_count), weight):
            mask = _support_mask(support)
            value = 0
            for index in support:
                value ^= code.columns[index]
            bucket = buckets.setdefault(value, [])
            collision_count += len(bucket)
            bucket.append((mask, weight))
            entries.append((value, mask, weight))

    best: tuple[int, tuple[int, ...], int] | None = None
    candidate_pairs = 0
    scanned = 0
    for value, mask, weight in entries:
        scanned += 1
        complement = target_syndrome ^ value
        for other_mask, other_weight in buckets.get(complement, ()):
            candidate_pairs += 1
            if mask & other_mask:
                continue
            total_weight = weight + other_weight
            if total_weight > 6:
                continue
            combined = mask | other_mask
            if combined.bit_count() != total_weight:
                continue
            support = tuple(
                index for index in range(column_count) if (combined >> index) & 1
            )
            candidate = (total_weight, support, combined)
            if best is None or candidate < best:
                best = candidate

    if best is None:
        return ExactSyndromeRecovery(
            accepted=False,
            recovered_error_mask=0,
            recovered_weight=0,
            subset_masks_indexed=len(entries),
            subset_masks_scanned=scanned,
            syndrome_bucket_collisions=collision_count,
            candidate_pairs_tested=candidate_pairs,
        )

    recovered = best[2]
    accepted = _verify_syndrome(code, target_syndrome, recovered)
    if not accepted:
        raise TDC3Error("TDC3 exact decoder produced invalid syndrome")
    return ExactSyndromeRecovery(
        accepted=True,
        recovered_error_mask=recovered,
        recovered_weight=best[0],
        subset_masks_indexed=len(entries),
        subset_masks_scanned=scanned,
        syndrome_bucket_collisions=collision_count,
        candidate_pairs_tested=candidate_pairs,
    )


def recover_tdc3_weight(instance: TDC3Instance, weight: int) -> DecoderPairRecovery:
    planted = planted_error_mask(instance, weight)
    top_target = syndrome(instance.pair.topology, planted)
    rnd_target = syndrome(instance.pair.matched_random, planted)

    top_bitflip = bitflip_decode(
        instance.pair.topology, top_target, instance.params.bitflip_max_iterations
    )
    rnd_bitflip = bitflip_decode(
        instance.pair.matched_random, rnd_target, instance.params.bitflip_max_iterations
    )
    top_exact = exact_syndrome_decode_leq6(instance.pair.topology, top_target)
    rnd_exact = exact_syndrome_decode_leq6(instance.pair.matched_random, rnd_target)

    return DecoderPairRecovery(
        planted_weight=weight,
        planted_error_mask=planted,
        topology_bitflip=top_bitflip,
        random_bitflip=rnd_bitflip,
        topology_exact=top_exact,
        random_exact=rnd_exact,
        topology_exact_matches_planted_after_public_success=(
            top_exact.accepted and top_exact.recovered_error_mask == planted
        ),
        random_exact_matches_planted_after_public_success=(
            rnd_exact.accepted and rnd_exact.recovered_error_mask == planted
        ),
    )
