# 98 — BPT-W0 stacked S^3 weak-control calibration

## Status

**BPT-W0 is rejected as intended by BPT-A000 on the declared weak-control distribution.**

It does **not** implement the move relation from the 2026 Pachner-distance NP-hardness result. Instead it uses only the elementary 1–4 / 4–1 Pachner pair on stacked triangulations of `S^3` to test whether the new BPT harness correctly rejects a family that public simplification should trivialize.

Exact-head CI passes on Python 3.11, 3.12 and 3.13. The Python 3.12 fixed baseline and full `d=1/2/3 × 8 seeds` sweep recover an accepted public path on **24/24** instances.

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

## Exact measured result

Fixed Python 3.12 `bptw0-d3` baseline:

```text
source/target vertices:                 8/8
source/target tetrahedra:               14/14
move bound / recovered length:          6/6
source/target simplification steps:     3/3
combined vertex scans:                  52
combined legal 4-1 moves seen:          13
source/target simplification paths:     8/12
accepted-path multiplicity lower bound: 96
public recovered path accepted:         yes
recovered path equals planted path:     no
```

The deterministic 24-instance sweep gives:

| Set | Instances accepted | Recovered length | Source paths | Target paths | Multiplicity lower bound |
|---|---:|---:|---:|---:|---:|
| `bptw0-d1` | 8/8 | 2 | 2 | 2 | 4 |
| `bptw0-d2` | 8/8 | 4 | 4 | 4 | 16 |
| `bptw0-d3` | 8/8 | 6 | 8–12 | 8 | 64–96 |

Every recovered sweep witness differs from the planted path after public success. One `d1` seed requires one generation retry only because source and target initially coincide; generation never filters on attack output.

The first exact-head implementation run exposed a harness error rather than a candidate property: it required literal equality of the two greedy roots. Once the attack was corrected to respect the verifier's isomorphism semantics, the weak control is broken uniformly.

## Equivalent-path accounting

The implementation recursively counts all public 4–1 simplification sequences from each endpoint that reach **any** five-tetrahedron root combinatorially isomorphic to the boundary of the 4-simplex, capped at one million. Their product is a lower bound on verifier-accepted simplification/splice paths between the endpoints.

This is not used to make the attack succeed. It records the same lesson preserved elsewhere in MORPH: planted-path equality is irrelevant when multiple accepted public paths exist.

## Calibration decision

**BPT-W0 passes the harness calibration by being rejected.** Public greedy simplification plus exact root-isomorphism transport recovers accepted paths on the complete declared distribution.

This permits further BPT research only at the specification/falsification level. It does not erase the earlier T0/T1 Pachner results: those experiments already rejected ordinary generated 2–3/3–2 transport and exact-distance-conditioned 2–3/3–2 endpoints. A successor must explicitly inherit those negative controls instead of recreating them under a new name.

## What BPT-W0 does not test

BPT-W0 does **not** test:

- 2–3 / 3–2 Pachner transport hardness;
- the exact bistellar-plus-collapse move system of Tillmann–Tsvietkova;
- generic or average-case 3-sphere move distance;
- Regina/SnapPy simplification resistance;
- hyperbolic 3-manifold canonicalization;
- quantum hardness.

The 2026 Tillmann–Tsvietkova worst-case NP-hardness result is not itself a BPT successor justification: its hard family is obtained by a reduction from modified planar Hamiltonian path. A future BPT candidate must state why its generated distribution is not merely that mature NP-hard problem encoded as triangulations and why it differs materially from the already-rejected T0/T1 distributions.

No security claim.
