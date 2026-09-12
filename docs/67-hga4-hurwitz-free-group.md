# 67 — HGA4 infinite Hurwitz action on free-group tuples

## Status

**HGA4 is a falsification/calibration experiment in progress.** It deliberately avoids the primary causes of HGA1–HGA3 failure: the endpoint orbit is infinite, there is no Euclidean endpoint normal form, and inversion is not an obvious homogeneous linear system in the hidden action.

HGA4 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Public action

Let `F(a,b)` be the rank-two free group. A public state is an ordered triple of exactly reduced free-group words `(g1,g2,g3)`.

The braid-group generators act by Hurwitz moves:

```text
p = sigma_1:      (x,y,z) -> (x y x^-1, x, z)
P = sigma_1^-1:   (x,y,z) -> (y, y^-1 x y, z)
q = sigma_2:      (x,y,z) -> (x, y z y^-1, y)
Q = sigma_2^-1:   (x,y,z) -> (x, z, z^-1 y z)
```

Generation samples three source words with distinct nonzero free abelianizations and a locally reduced planted braid word. The exact target tuple is obtained by applying the planted word.

Toy planted lengths are `8`, `12`, and `16`.

The verifier accepts **any** braid word carrying the exact public source tuple to the exact public target tuple. Equality with the planted word is reference-only.

## Infinite orbit and public invariants

Unlike HGA1, the exact endpoint state space is not a small finite group orbit: reduced free-group component lengths can grow without bound.

Two cheap public invariants are still mandatory attack inputs:

1. the reduced product `g1 g2 g3` is exactly Hurwitz-invariant;
2. free abelianization of each component is only permuted by Hurwitz generators.

Because generation requires the three source abelianization vectors to be distinct, the target abelianization tuple reveals the induced public strand permutation in `S3`.

This quotient does not by itself construct the full braid connector; it is recorded as public leakage and checked against the planted quotient only after public recovery.

## HGA-A005 — bounded exact MITM

The attack performs exact bidirectional BFS directly in reduced tuple states.

For a public word bound `L`:

- enumerate the source ball to depth `floor(L/2)`;
- enumerate the target ball to depth `ceil(L/2)` using the same four invertible generators;
- state deduplication automatically removes immediate backtracking and braid-relation collisions;
- intersect the two exact state maps;
- for every meet state compose the source-side word with the inverse target-side word;
- return the shortest deterministic connector and submit it to the exact endpoint verifier.

The attack uses no reference data.

## Interpretation rule

HGA4 is the first HGA stage where **toy MITM success alone is not a structural rejection criterion**. Deliberately short planted words are expected to be searchable.

The measurements distinguish:

- generic square-root/exponential search growth, which is merely a baseline;
- public quotient/canonical reductions that directly construct connectors, which are structural failures;
- routinely much shorter equivalent connectors than planted words, which are generated-distribution failures.

A toy family that exhibits only generic growing MITM work may survive this gate, but that still creates no hardness or post-quantum claim.

## Measurements

Record at least:

- planted braid length;
- source/target component reduced lengths;
- exact invariant-product length and verification;
- source/target abelianization tuples;
- recovered strand permutation and planted-quotient comparison;
- forward/backward depths;
- exact state and transition counts;
- number of meet states;
- recovered connector length;
- exact endpoint verification;
- post-success planted-word equality;
- whether the connector is at least 25% shorter than planted;
- deterministic all-size / multi-seed growth curve.

## Gate

Reject HGA4 if public quotient/canonical processing constructs connectors directly, or if the generated distribution routinely collapses to materially shorter equivalent actions with tiny work.

Do not claim structural rejection merely because generic MITM solves length-8/12/16 toy words.

## Successor gate

If the only observed recovery mechanism is generic growing exact search, HGA5 may increase action rank/complexity and must add finite quotient representations, stabilizer analysis, canonical forms, generated-distribution tests and explicit quantum hidden-shift/subgroup screening before any cryptographic interpretation.

No security claim.
