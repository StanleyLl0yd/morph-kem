# 55 — G20 flip-mixed genus-two multicurve negative control

## Status

**G20 is an attack calibration in progress. No hardness or security conclusion is permitted until exact-head CI records A-047.**

G20 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Motivation

G19 requires two bounded vertex-disjoint global representatives, but both are detected by one torus cocycle. A-046 finds one short odd cycle, deletes it, and finds another parallel-type representative on the remaining graph.

G20 changes the topology and the class coupling together. The carrier has genus two and measured `H^1(F2)` dimension four. The witness cycles must occupy two different public cohomology signatures `(1,0)` and `(0,1)` with respect to two independent public cocycles.

## Carrier

Two independently generated tori are connected-summed by deleting one triangle from each and identifying their boundary 3-cycles. The raw connected-sum counts are

```text
g20-4x4: V/E/F = 29/93/62
g20-6x6: V/E/F = 69/213/142
g20-6x9: V/E/F = 105/321/214
```

The resulting closed genus-two surface has `chi=-2`. A deterministic global legal edge-flip walk performs respectively 124, 284 and 428 successful flips, followed by an independent public vertex relabeling.

The final carrier must preserve exact edge incidence two and measured `dim H^1(F2)=4`.

## Separator gate

Connected sum plants a potential public seam. G20 therefore measures articulation points, every two-vertex separator, and every separating primal 3-cycle after mixing. A cheap surviving separator is itself a structural rejection result; mixing is not assumed to hide the seam.

## Public classes and verifier

The final public cochain complex is row-reduced over GF(2). A canonical basis of the quotient cocycle space modulo coboundaries is extracted; the first two independent representatives are published as `alpha` and `beta`.

A witness `(C_alpha,C_beta)` is accepted iff:

- both are simple public primal cycles;
- `C_alpha` has signature `(1,0)` against `(alpha,beta)`;
- `C_beta` has signature `(0,1)`;
- their vertex sets are disjoint;
- `|C_alpha| <= L_alpha` and `|C_beta| <= L_beta`.

Reference generation uses an independent seeded spanning-tree search only to guarantee satisfiability and set the public role-specific length bounds. Reference identity is not part of verification.

## A-047 — four-sheet class recovery

Public edge labels are the two-bit vectors `(alpha[e],beta[e])`. The attack uses the four-sheet cover `(v,s)`, `s in F2^2`.

1. For every public root, BFS from `(r,00)` to `(r,10)`.
2. XOR-cancel projected repeated edges and extract exact-signature `(1,0)` simple cycles.
3. For each bounded alpha candidate, delete all of its vertices and incident edges.
4. On the remaining graph, BFS from `(r,00)` to `(r,01)` for every remaining root.
5. Extract bounded exact-signature `(0,1)` simple cycles.
6. Submit candidate pairs to the exact verifier.

A separate canonical spanning-tree fundamental-cycle scan supplies an independent cross-check.

## Rejection gate

Reject G20 if either the connected-sum seam remains cheaply public or the class-aware four-sheet delete-and-recover attack routinely constructs accepted bounded pairs.

Do not scale dimensions or flip counts while either reduction remains effective.

No security claim.
