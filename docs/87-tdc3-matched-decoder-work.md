# 87 — TDC3 matched decoder-work control

## Status

**TDC3 is a falsification experiment in progress.** TDC2g is the first stage in the current TDC lineage that survives its predeclared largest-size rank + exact weight-`<=8` gate. TDC3 therefore moves from cheap structural distinguishers to explicit syndrome-decoding work on the same paired ensemble.

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

The first decoder gate fixes planted weights

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

Record iterations, score evaluations, initial/final syndrome weights, and exact public acceptance.

This is intentionally a cheap baseline. The public matrices are relatively dense after row/column mixing and parity overlay, so failure of naive bit flipping is not evidence of hardness.

## TDC-A010 attack 2 — exact meet-in-the-middle through weight six

Enumerate every public column subset of weight at most three and index its XOR syndrome. Pair two disjoint indexed subsets whose syndromes XOR to the target. Scan all candidate pairs and return the minimum-weight, then lexicographically smallest, accepted error.

This is an exact bounded toy ground truth through total weight six, not an efficient large-parameter algorithm.

### Pre-clean-branch measurement

The precursor stacked implementation measured `n8/n9/n10 × 8 × weights 1..6`, 144 paired syndromes per family:

- greedy bit-flip success: `26/144` topology and `26/144` matched controls;
- exact `<=6` decoder acceptance: `144/144` topology and `144/144` controls;
- exact result equals planted support: `144/144` topology and `143/144` controls;
- the single control mismatch is still attacker success: an accepted lower-weight error was found for a planted weight-six syndrome.

These numbers are retained as precursor evidence only until reproduced on the clean branch based directly on merged TDC2g.

## TDC-A010 attack 3 — reliability-guided bounded exact search

For every public target syndrome, rank all columns by the deterministic public tuple:

```text
one-step syndrome-weight gain,
overlap with current syndrome,
smaller column weight,
smaller public column index.
```

Fix the top **24** public columns as the reliability pool and run the same exact `<=6` MITM search restricted to that pool.

This is not channel soft information. It is a purely public reliability proxy intended to test whether topology exposes a more useful coordinate ordering than matched random controls.

Record:

- public acceptance;
- recovered weight;
- planted coordinates that happen to fall in the top-24 pool, reference-only;
- indexed subsets and candidate-pair work;
- syndrome-bucket collisions.

The declared reliability experiment is fixed **before** observing its clean-branch results:

```text
n8/n9/n10 × 8 seeds × weights 1..6, pool=24
n10 × 32 seeds × weights 1..6, pool=24
```

## Gate

Reject the current TDC2g-derived ensemble if topology instances are routinely easier to decode than paired controls at matched public dimensions/rank/rate/error weight, or if equivalent lower-weight errors appear disproportionately in topology.

If greedy, exact-bounded and reliability-guided behavior overlap without a reproducible topology advantage, record survival of **this decoder-work gate only** and proceed to a bounded OSD/ISD-style successor attack. Do not infer asymptotic or post-quantum hardness.

## Rate warning

The TDC2g common overlay spends six parity constraints to suppress inherited short codewords. TDC3 must keep reporting the rate cost. Surviving toy decoder comparisons by collapsing rate is not a useful cryptographic design.

No security claim.
