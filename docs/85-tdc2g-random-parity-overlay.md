# 85 — TDC2g common random parity-overlay control

## Status

**TDC2g is a falsification experiment in progress.** TDC2f already matches public rows/columns/rank/dimension/rate, but its largest `n10` topology distribution still shows a weight-`<=8` excess (`8/32` versus `0/32` rank-matched controls).

TDC2g changes the ensemble structurally rather than rejecting attack-positive samples.

TDC2g is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Construction

Start from a paired TDC2f topology/control instance. Both public matrices already have identical column count and rank.

Then sample a deterministic topology-independent sequence of binary parity rows over the public column coordinates. A candidate row is accepted only if it is linearly independent of the existing row space in **both** paired matrices. The exact same accepted row is appended to topology and control.

The generator adds exactly six such common rows.

This guarantees:

- the same rank increment in both families;
- identical final rank/dimension/rate inside each pair;
- no query to low-weight search, Tanner statistics, decoder output, or attack success;
- no per-instance rejection based on whether a weight-seven/eight word survives.

The only rejection condition is the declared algebraic requirement that the next common row raise both public ranks.

## Why this is a useful repair control

A random additional parity equation kills any fixed nonzero codeword with probability roughly one half. Six independent overlays therefore strongly suppress inherited short kernel words without inspecting them individually.

If the TDC2f topology/control gap disappears under this fixed overlay, that is evidence that the previous difference came from a small inherited low-weight substructure rather than a broad decoding-hardness separation.

If topology remains distinguishable, the residual structure is stronger than a few accidental short dependencies.

Either outcome is scientifically useful.

## TDC-A009 attack suite

For every public paired instance record:

1. base rank and final rank;
2. overlay row count and sampling attempts;
3. exact final rank/dimension/rate equality;
4. row/column degree histograms;
5. exact kernel search through weight six;
6. exact meet-in-the-middle kernel search through weight eight;
7. Tanner 4-cycle count.

The deterministic sweep is:

```text
n8/n9/n10 x 8 seeds
```

and the largest size additionally receives the predeclared unchanged

```text
n10 x 32 seeds
```

screen.

## Rejection / survival gate

Reject TDC2g if topology remains cheaply distinguishable from controls by rank, degree or the same bounded low-weight search.

If the `<=8` profile becomes statistically indistinguishable on the declared toy screen, record that as **survival of this gate only** and proceed to BP/bit-flipping plus bounded OSD/ISD/MITM decoding comparisons. Do not infer cryptographic hardness.

## Important limitation

The common random overlay deliberately reduces code dimension. If enough random constraints are added, any code can be driven toward a trivial high-distance/low-rate regime. Therefore success is meaningful only as a diagnostic of the TDC2f low-weight gap, not as a candidate cryptosystem design by itself.

A useful successor would need to preserve an application-relevant rate while surviving matched decoding attacks.

No security claim.