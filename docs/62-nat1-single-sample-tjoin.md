# 62 — NAT1 single-sample multi-error T-join negative control

## Status

**NAT1 is rejected by NAT-A002.** A single multi-error noisy sample remains publicly decodable because the triangle syndrome is exactly a dual-graph defect set and minimum correction is an ordinary T-join problem.

NAT1 is not a KEM, one-way function, post-quantum assumption, or production-security construction.

## Carrier

NAT1 reuses the constructive flip-mixed sphere machinery from G15 only as a public sparse complex. The carrier starts from an icosahedral sphere, grows to the requested size, performs a deterministic legal edge-flip walk, and is globally relabelled.

Toy sets:

```text
nat1-36: F=36, 360 successful flips, t in {1,2,3,4}
nat1-54: F=54, 540 successful flips, t in {1,2,3,4,5}
nat1-72: F=72, 720 successful flips, t in {1,2,3,4,5,6}
```

The sphere choice is deliberate for this gate. `H^1(S^2; F2)=0`, so once an attacker finds any public error set with the observed triangle syndrome, subtracting it leaves a public coboundary rather than an unresolved homology sector. NAT1 therefore isolates the noise-decoding question cleanly.

## Noisy relation

A hidden vertex 0-cochain induces a clean public edge coboundary. Generation chooses `t` distinct public edges by a deterministic uniform-style seeded ordering and flips exactly those bits. Only one observed edge vector is published.

There is no repeated-sample majority, no enforced spacing between errors, and no hidden reference requirement in recovery.

## NAT-A002 — public minimum T-join decoding

On a closed triangulated surface, every noisy primal edge corresponds to one dual edge joining the two incident triangles. The odd triangle parities are therefore exactly the boundary defects of the dual error subgraph.

The public attacker:

1. computes all violated triangle parities;
2. builds the public dual graph;
3. runs BFS from each defect to obtain all defect-pair distances and canonical shortest paths;
4. solves the exact minimum perfect pairing of defects by bitmask dynamic programming;
5. XORs the selected shortest paths to obtain a minimum T-join correction;
6. removes that correction from the observed edge data;
7. reconstructs a public vertex assignment from the resulting coboundary;
8. verifies the clean coboundary directly.

Any accepted clean object is attacker success. The recovered correction need not equal the planted error set and the recovered normalized vertex assignment need not equal the planted one.

## Fixed Python 3.12 result

For `nat1-72`, the fixed public carrier has `V/E/F = 38/108/72`; generation recorded 327 rejected flip proposals. The full one-sample recovery curve is:

| planted `t` | syndrome defects | DP states | pair tests | minimum correction weight | accepted | planted correction? |
|---:|---:|---:|---:|---:|:---:|:---:|
| 1 | 2 | 2 | 1 | 1 | yes | yes |
| 2 | 4 | 5 | 6 | 2 | yes | yes |
| 3 | 6 | 13 | 26 | 3 | yes | yes |
| 4 | 6 | 13 | 26 | 4 | yes | yes |
| 5 | 10 | 89 | 332 | 5 | yes | yes |
| 6 | 8 | 34 | 97 | **4** | yes | **no** |

For `t=6`, the public attacker therefore finds a weight-four correction with the same syndrome as the planted weight-six error set. Removing it yields a different accepted clean coboundary and a different normalized vertex assignment. This is attacker success, not a decoding ambiguity to be hidden by reference comparison.

## Deterministic sweep

Python 3.12 tested every declared noise weight over eight deterministic seeds for every toy size:

- `nat1-36`: 32 samples;
- `nat1-54`: 40 samples;
- `nat1-72`: 48 samples;
- total: **120 single-sample noisy instances**.

The exact public T-join decoder returns an accepted clean object on **120/120** instances. It matches the planted error set on 112/120 and returns a different accepted minimum correction on 8/120. Post-success normalized hidden-vertex equality changes in exactly those alternative-correction cases.

Maximum measured exact matching work is 233 DP states and 1,076 pair tests, occurring for a 12-defect syndrome. The attack uses no repeated samples and no reference data.

Dedicated NAT1 CI passes on Python 3.11, 3.12 and 3.13.

## Result

**NAT1 is rejected by NAT-A002.** Moving from one local error to a single multi-error sample does not help while the noisy relation remains a public surface boundary problem. The syndrome is a defect set in the public dual graph, and exact minimum correction is a small T-join/matching computation on the generated distribution.

The appearance of alternative minimum corrections is especially important: the noisy architecture already has its own equivalent-witness phenomenon. Hiding the planted error set or planted clean object is irrelevant when another accepted clean object is publicly reachable.

Do not repair NAT1 by increasing only `t` while the same public T-join reduction remains valid.

## NAT2 gate

NAT2 must change the noisy relation so residual uncertainty is not equivalent to ordinary defect matching on a public graph. A successor should couple multiple algebraic/topological constraints nonlinearly or move to a relation whose syndrome is not the boundary of an edge set in a publicly known low-dimensional complex. It must immediately face sparse recovery, BP/bit-flipping, matching/flow reductions, generic SAT/ILP, quotient leakage and equivalent-clean-object enumeration.

No security claim.
