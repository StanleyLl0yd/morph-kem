# 87 — TDC3 matched decoder-work control

## Status

**TDC3 is a falsification experiment in progress.** TDC2g is the first stage in the current TDC lineage that survives its predeclared largest-size rank + exact weight-`<=8` gate. TDC3 therefore moves from cheap structural distinguishers to explicit syndrome-decoding work on the same paired ensemble.

TDC3 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Fixed starting ensemble

TDC3 uses TDC2g without changing generation:

- six common topology-independent parity overlays;
- identical public rows/columns/rank/dimension/rate inside each topology/control pair;
- no per-instance low-weight or decoder conditioning;
- fixed toy n10 rate about `0.382353`.

For each seed and declared error weight, topology and control receive **the same public error support indices**. Their syndromes differ because their parity-check matrices differ, but the planted Hamming weight and coordinate support are matched exactly.

## Error schedule

The first decoder gate uses planted weights

```text
1, 2, 3, 4, 5, 6
```

for `n8`, `n9`, and `n10`.

The public decoder never receives the planted support. It sees only the public matrix and target syndrome.

Any syndrome-equivalent recovered error is attacker success. Equality with the planted error is recorded only after public success.

## TDC-A010 attack 1 — deterministic greedy bit flipping

Starting from zero error and the target syndrome:

1. for every public column, compute the reduction in residual syndrome Hamming weight if that bit is flipped;
2. choose the positive-gain flip with deterministic public tie breaking;
3. update the residual syndrome;
4. stop on zero syndrome, no improving flip, a repeated residual state, or the declared iteration cap.

Record iterations, score evaluations, initial/final syndrome weights, and exact public acceptance.

This is intentionally a cheap baseline. The TDC2g public matrices are relatively dense after row/column mixing and parity overlay, so failure of naive bit flipping is not evidence of hardness.

## TDC-A010 attack 2 — exact meet-in-the-middle syndrome decoder through weight six

Enumerate every public column subset of weight at most three and index its XOR syndrome. Pair two disjoint indexed subsets whose syndromes XOR to the target.

This searches all syndrome-equivalent errors of total weight at most six. Scan all candidate pairs and return the minimum-weight, then lexicographically smallest, accepted error.

Record:

- indexed/scanned subset counts;
- syndrome-bucket collisions;
- candidate pairs tested;
- recovered minimum weight;
- exact public syndrome acceptance;
- post-success equality with planted support.

The exact decoder is a bounded toy ground truth, not an efficient large-parameter algorithm.

## Declared sweep

Run:

```text
n8/n9/n10 × 8 deterministic seeds × weights 1..6
```

for both topology and paired controls.

An extended n10 screen is added only if this first sweep shows a reproducible topology/control separation in decoder success or work; it is not selected post hoc to rescue a weak signal.

## Gate

Reject the current TDC2g-derived ensemble if topology instances are routinely easier to decode than paired controls at matched public dimensions/rank/rate/error weight, or if equivalent lower-weight errors appear disproportionately in topology.

If bit-flipping behavior overlaps and the exact bounded decoder shows no topology-specific advantage, record survival of **this first decoder-work gate only** and proceed to stronger reliability-guided/OSD/ISD attacks.

## Rate warning

The TDC2g common overlay spends six parity constraints to suppress inherited short codewords. TDC3 must keep reporting the resulting rate cost. Surviving toy decoder comparisons by collapsing rate is not a useful cryptographic design.

No security claim.