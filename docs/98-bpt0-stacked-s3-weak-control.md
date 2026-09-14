# 98 — BPT-W0 stacked S^3 weak-control calibration

## Status

**BPT-W0 is a deliberately weak calibration experiment in progress.**

It does **not** implement the move relation from the 2026 Pachner-distance NP-hardness result. Instead it uses only the elementary 1–4 / 4–1 Pachner pair on stacked triangulations of `S^3` to test whether the new BPT harness correctly rejects a family that public simplification should trivialize.

No one-wayness, novelty, post-quantum, KEM, IND-CPA/CCA or production-security claim exists.

## Public objects

The common root type is the boundary of the 4-simplex: five tetrahedra triangulating `S^3`.

For stack depth `d`, generation independently applies `d` deterministic seeded 1–4 moves to the same labelled root to obtain public endpoints `T0,T1`.

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

## BPT-A000 — greedy simplification plus public root transport

The public attack repeatedly applies the lexicographically first legal 4–1 move to each endpoint until no such move remains.

A subtle but important calibration fact is that lexicographic greedy simplification need not undo the planted 1–4 history. It can legally collapse one of the original root vertices after earlier simplifications. Therefore the two greedy outputs are not required to have identical vertex labels.

The required weak-control behavior is instead:

```text
T0 --public 4-1 simplification--> R0 ~= boundary(4-simplex)
T1 --public 4-1 simplification--> R1 ~= boundary(4-simplex)
R0 ~= R1
```

The attacker recovers a deterministic exact public vertex isomorphism `R1 -> R0`. Vertices removed from the target during simplification are assigned fresh labels not present in `R0`. The inverse target simplification path is transported through this map and concatenated with the source simplification path.

The resulting endpoint only needs to be combinatorially isomorphic to the public target, exactly matching verifier semantics. Requiring literal root equality would incorrectly make the attack depend on generator labels rather than the public relation.

If the transported path is within the public bound and verifies, BPT-W0 is rejected as intended.

## Equivalent-path accounting

The implementation recursively counts all public 4–1 simplification sequences from each endpoint that reach **any** five-tetrahedron root combinatorially isomorphic to the boundary of the 4-simplex, capped at one million. Their product is a lower bound on verifier-accepted simplification/splice paths between the endpoints.

This is not used to make the attack succeed. It records the same lesson preserved elsewhere in MORPH: planted-path equality is irrelevant when multiple accepted public paths exist.

## Measurements

Record at least:

- source/target vertex counts;
- source/target tetrahedron counts;
- public move bound and recovered length;
- simplification steps on both endpoints;
- public vertex scans and number of legal 4–1 choices observed;
- whether greedy roots are literally equal and whether they are isomorphic;
- exact source/target simplification-path counts in the toy range;
- accepted-path multiplicity lower bound;
- exact verifier acceptance;
- planted-path equality only after public success;
- deterministic `d=1/2/3 × 8 seeds` sweep.

## Calibration gate

BPT-W0 must be rejected on the declared distribution before any stronger BPT experiment is interpreted.

If public greedy simplification plus exact root-isomorphism transport fails to recover accepted paths on this intentionally stacked family, stop and repair the harness rather than constructing a harder generator.

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
