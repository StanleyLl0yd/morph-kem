# 69 — TDC2b tetrahedron-free sparse 2-complex control

## Status

**TDC2b is rejected by TDC-A004.** Constructive tetrahedron avoidance removes the TDC2 weight-four boundary failure, but the resulting topology-derived codes still expose deterministic public weight-six kernel relations on every measured instance.

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

For every topology-derived matrix, construct a simple connected random sparse matrix with exactly the same row/column counts, exact individual row-degree sequence, column weight three, and no duplicate columns. Generation uses bounded retries and records them.

## TDC-A004 — exact low-weight search

The public attack searches the kernel through weight six using zero/duplicate-column tests, pair-syndrome hashing and pair/triple or disjoint-triple syndrome collisions. Exact supports are deduplicated and the multiplicity of the first observed weight is recorded. The identical search is run on the matched-random control.

## Fixed Python 3.12 result

For `tdc2b-n10`:

```text
selected faces / skipped tetra completions: 65 / 55
rows / columns:                              45 / 65
topology rank / dimension / rate:            36 / 29 / 0.446153846
topology tetrahedron boundaries:             0
topology minimum weight <=6:                 6
topology minimum-weight multiplicity:         48
topology pair / triple collision buckets:     0 / 461

matched-random rank / dimension / rate:       45 / 20 / 0.307692308
matched-random minimum weight <=6:            none
matched-random pair / triple collision buckets: 0 / 0
matched-random retries:                       79
```

The exact individual row-degree profile is preserved by the matched-random control.

## Eight-seed sweep

Across `n=8,9,10` × eight deterministic seeds:

- all **24/24** topology matrices contain no tetrahedron boundary;
- all **24/24** topology matrices have first detected kernel weight exactly **6**;
- topology weight-six multiplicity ranges from **13 to 77**;
- exactly **6/24** matched-random controls contain a codeword of weight at most six;
- every one of those six random low-weight cases has multiplicity exactly **1**;
- the other **18/24** matched-random controls have no codeword through weight six.

By size, topology multiplicities are:

```text
n=8:  13..33
n=9:  28..41
n=10: 54..77
```

The topology signal therefore becomes stronger, not weaker, over this toy range even after all tetrahedron boundaries are removed.

## Interpretation

The first TDC2 failure was not only an artifact of complete four-vertex boundaries. The explicit tetrahedron-free repair shifts the bounded public kernel leakage from weight four to weight six rather than producing a growing-distance mechanism.

The matched-random comparison is important: identical row degrees and column weight three do not routinely create this effect. The repeated weight-six family is specific to the generated incidence structure in this control.

Increasing only `n` is not a justified repair while the same bounded relation persists.

## Successor gate

The next TDC candidate must use an actual sparse lift/cover, quotient or another explicit complex family that destroys the measured weight-six relation while keeping nontrivial rate. Before decoder interpretation it must face:

- base-role and quotient recovery;
- low-weight search beyond six;
- Tanner short-cycle/trapping-set analysis;
- BP / bit-flipping;
- OSD / ISD / MITM;
- matched-random decoding controls.

No trapdoor primitive, KEM, one-wayness, post-quantum, IND-CPA/CCA, or production-security claim exists.
