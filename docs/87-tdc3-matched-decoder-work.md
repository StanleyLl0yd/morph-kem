# 87 — TDC3 matched decoder-work control

## Status

**TDC3 survives TDC-A010 on the measured toy distribution.** The unchanged TDC2g topology/control ensemble shows no reproducible topology-easier signal under greedy bit flipping, exact bounded syndrome decoding, or a predeclared public reliability-guided search. This is survival of a decoder-work falsification gate only, not evidence of asymptotic, post-quantum, or production-security hardness.

TDC3 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Fixed starting ensemble

TDC3 uses TDC2g without changing generation:

- six common topology-independent parity overlays;
- identical public rows/columns/rank/dimension/rate inside each topology/control pair;
- no per-instance low-weight or decoder conditioning;
- fixed toy n10 rate near `0.38` in the measured TDC2g family.

For each seed and declared error weight, topology and control receive **the same public error-support indices**. Their syndromes differ because their parity-check matrices differ, but planted Hamming weight and coordinate support are matched exactly.

The public decoder never receives the planted support. It sees only the public matrix and target syndrome. Any syndrome-equivalent recovered error is attacker success. Equality with the planted error is reference-only after public success.

## Error schedule

The decoder gate fixes planted weights

```text
1, 2, 3, 4, 5, 6
```

for `n8`, `n9`, and `n10`.

## TDC-A010 attack 1 — deterministic greedy bit flipping

Starting from zero error and the target syndrome:

1. score every public column by its one-step reduction in residual-syndrome Hamming weight;
2. choose the positive-gain flip with deterministic public tie breaking;
3. update the residual syndrome;
4. stop on zero syndrome, no improving flip, a repeated residual state, or the declared iteration cap.

The clean `n8/n9/n10 × 8 × weights 1..6` sweep contains 144 paired syndromes per family. Measured public success is exactly

```text
topology: 26 / 144
control:  26 / 144
```

Per size:

```text
n8:   9 / 48  vs  9 / 48
n9:   9 / 48  vs  9 / 48
n10:  8 / 48  vs  8 / 48
```

No topology advantage appears at this cheap iterative gate.

## TDC-A010 attack 2 — exact meet-in-the-middle through weight six

Enumerate every public column subset of weight at most three and index its XOR syndrome. Pair two disjoint indexed subsets whose syndromes XOR to the target. Scan all candidate pairs and return the minimum-weight, then lexicographically smallest, accepted error.

Across the same clean 144-case sweep:

```text
exact accepted:
  topology: 144 / 144
  control:  144 / 144

exact result equals planted support:
  topology: 144 / 144
  control:  143 / 144
```

The single control mismatch is not a decoder failure: the public decoder found a verifier-accepted lower-weight error for a planted weight-six syndrome. Under the project attack semantics that is attacker success.

This exact decoder is a bounded toy ground truth through total weight six, not an efficient large-parameter algorithm.

## TDC-A010 attack 3 — reliability-guided bounded exact search

For every public target syndrome, rank all columns by the deterministic public tuple:

```text
one-step syndrome-weight gain,
overlap with current syndrome,
smaller column weight,
smaller public column index.
```

Fix the top **24** public columns as the reliability pool and run the same exact `<=6` MITM search restricted to that pool. This is not channel soft information; it is a purely public coordinate heuristic.

The predeclared `n8/n9/n10 × 8 × weights 1..6` measurement gives:

```text
size   topology success   control success   delta
n8          17 / 48           21 / 48        -4
n9          14 / 48           12 / 48        +2
n10         10 / 48           11 / 48        -1
```

The sign changes with size, so the eight-seed sweep does not support a topology-easier interpretation.

The predeclared larger `n10 × 32 × weights 1..6` extension gives:

```text
weight   topology   control   delta
1          32/32      32/32      0
2           5/32       7/32     -2
3           2/32       3/32     -1
4           1/32       1/32      0
5           0/32       0/32      0
6           0/32       0/32      0
-----------------------------------
total      40/192     43/192     -3
```

Thus the larger screen again does **not** make topology easier. The reference-only count of planted coordinates appearing in the top-24 pool is also not larger for topology on this n10 extension: by weights 1..6 the cumulative counts are

```text
topology: 32, 22, 32, 41, 50, 53
control:  32, 26, 35, 44, 64, 77
```

This latter measurement is diagnostic only; public attack success remains the primary gate.

## Interpretation

TDC2g removed the earlier cheap rank/low-weight distinction by structurally changing the ensemble. TDC3 now shows that three predeclared public decoders also fail to expose a reproducible topology-easier distribution on the tested toy sizes.

The correct result is **gate survival**, not a hardness claim. The next falsification stage must use a stronger bounded information-set / OSD-style decoder with explicit public work accounting while keeping the TDC2g generator and error distribution fixed.

## Rate warning

The TDC2g common overlay spends six parity constraints to suppress inherited short codewords. TDC3 keeps that rate cost. Surviving toy decoder comparisons by collapsing rate is not a useful cryptographic design by itself.

No security claim.
