# 69 — TDC2b tetrahedron-free sparse 2-complex control

## Status

**TDC2b is a falsification experiment in progress.** It directly repairs the first TDC2 boundary-family failure by preventing every public tetrahedron boundary from being present in the generated 2-complex, then immediately searches for the next bounded-weight kernel relation.

TDC2b is not a KEM, one-way function, post-quantum assumption, or production-security construction.

## Construction

For `n in {8,9,10}`, begin with all public triangle faces on `n` vertices and visit them in deterministic seeded order. A candidate face is included unless adding it would complete all four triangular faces of some public four-vertex set.

Thus generation guarantees by construction:

```text
no complete tetrahedron boundary occurs.
```

This is an explicit local generation rule. It does not query rank, minimum distance, low-weight attack output, matched-random behavior, or decoder success.

The resulting binary parity-check matrix again has triangle variables and edge checks. Every column has weight three, so the same direct graph-incidence obstruction remains: it is not an ordinary binary graph incidence matrix under row/column permutation.

Independent public row and column relabeling removes lexicographic generation labels.

## Matched-random control

For every topology-derived matrix, construct a simple connected random sparse matrix with:

- exactly the same number of rows and columns;
- exactly the same **individual row-degree sequence**;
- column weight exactly three;
- no duplicate columns.

Generation uses a bounded configuration-model retry loop and records the exact retry count.

## TDC-A004 — exact low-weight kernel search through weight six

The attack is completely public and independent of the face-generation labels.

1. test zero/duplicate columns for weights 1–2;
2. hash pair syndromes to detect weight-three and weight-four relations;
3. hash triple syndromes and compare pair/triple buckets for weight-five relations;
4. collide disjoint triples for weight-six relations;
5. deduplicate exact supports and record the multiplicity of the first observed weight.

The same search is run unchanged on the matched-random control.

## Measurements

Record at least:

- selected face count and number of skipped tetrahedron completions;
- rows/columns, exact rank/dimension/rate;
- row/column degree histograms;
- explicit tetrahedron-boundary count;
- first kernel weight up to six and its multiplicity;
- pair/triple syndrome collision-bucket counts;
- matched-random first weight/multiplicity under the same search;
- matched-random generation retries;
- deterministic all-size / multi-seed sweep.

## Rejection gate

Reject TDC2b if eliminating tetrahedron boundaries merely exposes another deterministic bounded-weight topology relation that appears routinely and materially more often than in degree-matched random controls.

Do not repair by increasing only `n` while the same bounded local cycle persists.

If no codeword through weight six is found on growing toy sizes, that only means this specific low-weight gate survives; it is not a distance or security proof. The next stage must then face quotient recovery, Tanner structure, BP/bit-flipping, OSD/ISD/MITM and generic exact decoding.

## Successor gate

A rejected TDC2b should move to an actual sparse cover/lift or another explicit complex family that destroys the newly identified bounded cycle while preserving a nontrivial code rate. Any lift must immediately face base-role/quotient recovery and matched-random controls.

No security claim.
