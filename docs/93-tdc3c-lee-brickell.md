# 93 — TDC3c Lee–Brickell order-2 matched-control gate

## Status

**TDC3c is a predeclared falsification experiment in progress.** It strengthens TDC3b without changing the merged TDC2g-derived generator, parity overlay, matched controls or planted error schedule.

TDC3b survived bounded Prange/ISD on the declared toy distribution. TDC3c therefore allows a bounded number of error positions outside each candidate basis, following the basic Lee–Brickell idea.

This is not a decoding-hardness or security claim.

## Fixed ensemble

TDC3c reuses exactly:

- `tdc3-n8`, `tdc3-n9`, `tdc3-n10`;
- topology-derived and matched-random matrices from the merged TDC2g line;
- common planted support indices;
- public error weights `1..6`.

Any syndrome-equivalent error of weight at most the declared bound is attacker success. Planted equality is measured only after public success.

## TDC-A012 — bounded Lee–Brickell-style ISD

For a full-row-rank public parity-check matrix `H` and public target syndrome `s`, each information-set trial:

1. selects `r = rank(H)` columns using the existing public TDC3b information-set derivation;
2. rejects the trial if those columns are rank-deficient;
3. otherwise computes one public GF(2) coordinate map for the selected basis;
4. maps `s` and all nonbasis columns into basis coordinates;
5. enumerates nonbasis error subsets in deterministic order for exact outside orders `0`, `1`, and `2`;
6. linearly computes the unique basis completion for each outside subset;
7. forms the full error candidate;
8. checks the public weight bound and exact syndrome verifier.

Order zero is the Prange special case. Orders one and two strictly enlarge the public attack search.

## Fixed checkpoints

Before measurement, the cumulative information-set budgets are fixed at

```text
1
4
16
```

and cumulative outside orders are fixed at

```text
0
1
2.
```

The implementation evaluates the same sixteen public information sets once and records success for all nine `(max_order,budget)` checkpoints. Work snapshots at `1/4/16` are fixed-budget exhaustion costs, independent of whether an earlier accepted candidate exists. A separate snapshot records work up to the first strongest-attack accepted candidate.

No trial budget or outside order may be increased inside TDC3c after measurement.

## Exact GF(2) coordinate map

For selected basis matrix `M`, Gauss–Jordan elimination is run on

```text
[M | I]
```

to obtain

```text
[I | M^-1].
```

The right block maps any public syndrome to selected-column coordinates. Linearity then allows every outside subset to be compensated without repeating elimination.

Unit tests verify the coordinate map by reconstructing public unit syndromes and checking them through the same exact syndrome function used by the verifier.

## Work accounting

At each fixed trial checkpoint record:

- information sets attempted;
- rank-deficient sets;
- full-rank coordinate maps;
- pivot scans;
- row swaps;
- GF(2) row XORs;
- outside subsets enumerated at exact orders `0/1/2`;
- candidate weight tests;
- exact verifier calls.

For the strongest `(order<=2,budget<=16)` attack also record:

- first successful trial;
- outside order of the first accepted candidate;
- recovered weight;
- work accumulated at that first success;
- planted equality only after public success.

## Declared measurement

Unlike TDC3b, the larger `n10` validation is mandatory from the start:

```text
n8  ×  8 seeds × weights 1..6
n9  ×  8 seeds × weights 1..6
n10 × 32 seeds × weights 1..6
```

The `n10×32` distribution is not triggered by an observed signal. This avoids repeating the small-sample fluctuation seen in the TDC3b `n10×8` slice.

## Rejection gate

Reject the current topology-derived ensemble if topology instances show a reproducible easier-decoding signal than matched controls on the mandatory `n10×32` distribution at any fixed `(max_order,budget)` checkpoint, or materially lower exact public work for comparable recovery.

Do not repair a failed gate by adding overlay rows, changing error weights or altering the current generator.

## Survival gate

If topology/control success and work curves remain overlapping or topology is not easier under all predeclared checkpoints, record only survival of this bounded Lee–Brickell-style toy gate.

A successor would still need a stronger independent attack family — for example a bounded Stern/collision-style decoder or a more advanced ISD variant — before any trapdoor or KEM interface could be considered.

No trapdoor primitive, KEM, one-wayness, post-quantum, IND-CPA/CCA or production-security claim exists.
