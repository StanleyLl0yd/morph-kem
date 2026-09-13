# 80 — TDC2f rank-matched public-kernel control

## Status

**TDC2f is a falsification experiment in progress.** TDC2e is rejected because invertible variable mixing preserves the public binary rank, while its topology and degree-matched random controls have different rank/dimension profiles. TDC2f removes that exact confounder before any decoding conclusion is considered.

TDC2f is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Construction

For each TDC2b topology matrix with `n` columns and rank `r`:

1. compute a deterministic independent basis of its public row space, yielding an equivalent `r x n` parity-check matrix with the same kernel;
2. apply two rounds of invertible row additions to remove the canonical basis presentation;
3. apply two complete rounds of the TDC2e invertible variable-coordinate additions;
4. publicly relabel rows and columns.

The matched control is generated directly as an independent full-rank binary `r x n` matrix with nonzero distinct columns. It receives independent row scrambling, the same declared two-round variable-mixing budget, and public relabeling.

Consequently topology and control are required to have identical public:

- row count;
- column count;
- rank;
- dimension;
- rate.

Generation never queries low-weight search or Tanner statistics.

## TDC-A008 first gates

### Rank/dimension regression

Every generated topology/control pair must match exactly on `(rows, columns, rank, dimension, rate)`. Any drift is a generator failure rather than an attack result.

### Direct bounded-weight kernel search

Run the exact public kernel search through weight six on both families. Record first weight, multiplicity and syndrome-collision counts. If this gate does not distinguish the families, the next attack is exact/meet-in-the-middle search through weight eight on the declared toy sizes.

### Public dependency profile

Record pair/triple syndrome-collision buckets and exact Tanner 4-cycle counts after the row and column transformations. These are calibration invariants/profiles only; a difference is useful only if it is stable against the rank-matched random control.

## Measurements

Record:

- rows/columns/rank/dimension/rate;
- row-scramble and column-mixing operation counts;
- rejected local mixing candidates;
- random-control generation attempts;
- row/column weight histograms;
- minimum public kernel weight through six and multiplicity;
- pair/triple syndrome-collision buckets;
- exact Tanner 4-cycle count;
- deterministic `n8/n9/n10 x 8` sweep.

## Gate

Reject TDC2f if the rank-matched topology family still exposes a stable cheap public invariant or excess bounded-weight kernel relations. If the first gates survive, extend to weight eight, sparse-coordinate recovery and generic OSD/ISD/MITM/BP attacks before considering any successor relation.

Survival of these toy gates would not establish hardness or security.

No security claim.
