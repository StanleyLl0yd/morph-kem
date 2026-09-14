# 98 — BPT-W0 stacked S^3 weak-control calibration

## Status

**BPT-W0 is a deliberately weak calibration experiment in progress.**

It does **not** implement the move relation from the 2026 Pachner-distance NP-hardness result. Instead it uses only the elementary 1–4 / 4–1 Pachner pair on stacked triangulations of `S^3` to test whether the new BPT harness correctly rejects a family that public simplification should trivialize.

No one-wayness, novelty, post-quantum, KEM, IND-CPA/CCA or production-security claim exists.

## Public objects

The common root is the boundary of the 4-simplex: five tetrahedra triangulating `S^3`.

For stack depth `d`, generation independently applies `d` deterministic seeded 1–4 moves to the common root to obtain public endpoints `T0,T1`.

Toy sets:

```text
bptw0-d1: d=1, public path bound 2
bptw0-d2: d=2, public path bound 4
bptw0-d3: d=3, public path bound 6
```

Generation rejects only identical endpoints; it never inspects simplification or shortest-path output.

## Public verifier

A move sequence is accepted iff:

1. every declared 1–4 / 4–1 move is legal on the current public triangulation;
2. sequence length is at most the public bound;
3. the final triangulation is combinatorially isomorphic to the target.

The toy isomorphism checker is an exact exhaustive relabeling of at most eight vertices. This is intentionally acceptable only for BPT-W0; a stronger BPT family must use an independent scalable canonicalization layer.

Any accepted path is attacker success. The planted path is reference-only.

## BPT-A000 — greedy common-root simplification

The public attack repeatedly applies the lexicographically first legal 4–1 move to each endpoint until no such move remains.

For this weak stacked family the expected behavior is:

```text
T0 --public 4-1 simplification--> boundary(4-simplex)
T1 --public 4-1 simplification--> boundary(4-simplex)
```

The attacker then concatenates the source simplification path with the inverse of the target simplification path.

If the resulting path is within the public bound and verifies, BPT-W0 is rejected as intended.

## Equivalent-path accounting

The implementation also recursively counts all public 4–1 simplification sequences from each endpoint to the common root, capped at one million. Their product is a lower bound on verifier-accepted common-root paths between the endpoints.

This is not used to make the attack succeed. It records the same lesson preserved elsewhere in MORPH: planted-path equality is irrelevant when multiple accepted public paths exist.

## Measurements

Record at least:

- source/target vertex counts;
- source/target tetrahedron counts;
- public move bound and recovered length;
- simplification steps on both endpoints;
- public vertex scans and number of legal 4–1 choices observed;
- exact source/target simplification-path counts in the toy range;
- accepted-path multiplicity lower bound;
- exact verifier acceptance;
- planted-path equality only after public success;
- deterministic `d=1/2/3 × 8 seeds` sweep.

## Calibration gate

BPT-W0 must be rejected on the declared distribution before any stronger BPT experiment is interpreted.

If public greedy simplification fails to recover accepted paths on this intentionally stacked family, stop and repair the harness rather than constructing a harder generator.

## What BPT-W0 does not test

BPT-W0 does **not** test:

- 2–3 / 3–2 Pachner transport hardness;
- the exact bistellar-plus-collapse move system of Tillmann–Tsvietkova;
- generic or average-case 3-sphere move distance;
- Regina/SnapPy simplification resistance;
- hyperbolic 3-manifold canonicalization;
- quantum hardness.

A successful calibration only permits BPT-1 to define a stronger move distribution and its matched controls.

No security claim.
