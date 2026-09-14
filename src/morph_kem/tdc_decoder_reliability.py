from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from .tdc_decoder_work import TDC3Error, syndrome
from .tdc_sparse_faces import SparseFaceCode


@dataclass(frozen=True, slots=True)
class ReliabilityRecovery:
    accepted: bool
    recovered_error_mask: int
    recovered_weight: int
    pool_size: int
    score_evaluations: int
    subset_masks_indexed: int
    subset_masks_scanned: int
    candidate_pairs_tested: int
    syndrome_bucket_collisions: int
    selected_indices: tuple[int, ...]


def _support_mask(indices: tuple[int, ...]) -> int:
    value = 0
    for index in indices:
        value |= 1 << index
    return value


def reliability_order(code: SparseFaceCode, target_syndrome: int) -> tuple[int, ...]:
    """Rank columns by one-step public syndrome-weight reduction.

    This is a deterministic toy reliability proxy, not soft channel information.
    It depends only on the public parity-check matrix and public target syndrome.
    """

    target_weight = target_syndrome.bit_count()
    ranked = []
    for index, column in enumerate(code.columns):
        overlap = (column & target_syndrome).bit_count()
        new_weight = (target_syndrome ^ column).bit_count()
        gain = target_weight - new_weight
        ranked.append((gain, overlap, -column.bit_count(), -index, index))
    ranked.sort(reverse=True)
    return tuple(item[-1] for item in ranked)


def reliability_guided_decode_leq6(
    code: SparseFaceCode,
    target_syndrome: int,
    *,
    pool_size: int = 24,
) -> ReliabilityRecovery:
    """Exact <=6 search restricted to the top public reliability pool."""

    if pool_size < 6 or pool_size > len(code.columns):
        raise TDC3Error("TDC3 reliability pool outside public column bounds")
    order = reliability_order(code, target_syndrome)
    selected = tuple(sorted(order[:pool_size]))

    entries: list[tuple[int, int, int]] = []
    buckets: dict[int, list[tuple[int, int]]] = {}
    collision_count = 0

    for weight in range(0, 4):
        for support in combinations(selected, weight):
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
        for other_mask, other_weight in buckets.get(target_syndrome ^ value, ()):
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
                index for index in selected if (combined >> index) & 1
            )
            candidate = (total_weight, support, combined)
            if best is None or candidate < best:
                best = candidate

    if best is None:
        return ReliabilityRecovery(
            accepted=False,
            recovered_error_mask=0,
            recovered_weight=0,
            pool_size=pool_size,
            score_evaluations=len(code.columns),
            subset_masks_indexed=len(entries),
            subset_masks_scanned=scanned,
            candidate_pairs_tested=candidate_pairs,
            syndrome_bucket_collisions=collision_count,
            selected_indices=selected,
        )

    recovered = best[2]
    accepted = syndrome(code, recovered) == target_syndrome
    if not accepted:
        raise TDC3Error("TDC3 reliability decoder produced invalid syndrome")
    return ReliabilityRecovery(
        accepted=True,
        recovered_error_mask=recovered,
        recovered_weight=best[0],
        pool_size=pool_size,
        score_evaluations=len(code.columns),
        subset_masks_indexed=len(entries),
        subset_masks_scanned=scanned,
        candidate_pairs_tested=candidate_pairs,
        syndrome_bucket_collisions=collision_count,
        selected_indices=selected,
    )
