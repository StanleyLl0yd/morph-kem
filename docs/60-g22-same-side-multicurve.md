# 60 — G22 same-side coupled genus-two multicurve control

## Status

**G22 is the final planned control of the HGES exact-witness line.** No hardness or rejection conclusion is permitted until exact-head CI measures A-049.

G22 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Motivation

G21 removes sequential recovery and asks for eight cycles simultaneously, but a public tree-cotree decomposition mechanically supplies the complete primal-dual identity crossing matrix.

G22 changes the geometry rather than the carrier. All four witness cycles now live in the **same primal graph**. Tree-cotree duality no longer supplies their target relation automatically.

## Public carrier

Reuse the flip-mixed genus-two carrier calibrated by G21. The carrier remains closed with Euler characteristic `-2` and `dim H^1(F2)=4`.

Toy sets:

```text
g22-4x4: public cycle-length bound 16
g22-6x6: public cycle-length bound 24
g22-6x9: public cycle-length bound 30
```

The bounds are fixed by the public parameter set, not derived from a hidden witness.

## Public witness

A witness contains four distinct public simple primal cycles `(a1,b1,a2,b2)`.

The exact verifier requires:

- every cycle length is within the public bound;
- their four public cohomology signatures have GF(2) rank four, so the cycles span `H_1`;
- `a1` and `b1` share exactly one public vertex;
- `a2` and `b2` share exactly one public vertex;
- every cross-handle pair is vertex-disjoint.

Thus the off-diagonal vertex-intersection matrix is exactly

```text
0 1 0 0
1 0 0 0
0 0 0 1
0 0 1 0
```

Diagonal entries are ignored because they are the cycle's own vertex count.

There are no hidden role labels in the verifier beyond the submitted ordering.

## A-049 — public short-cycle compatibility search

The primary attack deliberately avoids SAT/ILP.

1. derive a public four-dimensional cohomology basis;
2. derive 16 deterministic public spanning trees from a hash of the final public complex;
3. enumerate every fundamental cycle from each tree;
4. discard cycles over the public length bound or with zero public homology signature;
5. deduplicate exact public cycles;
6. retain the ten shortest cycles per nonzero four-bit signature;
7. enumerate candidate pairs sharing exactly one public vertex;
8. search two such pairs whose vertex unions are disjoint and whose four signatures have rank four;
9. submit the resulting family to the exact verifier.

The retained-per-signature cap and number of public tree samples are explicit toy attack parameters. If they fail, increasing attack coverage is permitted because they are attacker resources, not security parameters.

## Measurements

Record at least:

- public `V/E/F`, Euler characteristic and H1 dimension;
- raw fundamental cycles enumerated;
- distinct bounded nonzero cycles;
- candidate count by public homology signature;
- retained candidate count;
- exact-one vertex-intersection pair count;
- pair-of-pairs compatibility tests;
- selected lengths and signatures;
- signature rank;
- exact vertex-intersection matrix;
- exact verifier outcome;
- deterministic all-size / multi-seed sweep.

## Rejection gate

If A-049 routinely finds an accepted four-cycle family, **reject G22 and freeze the HGES exact-witness line**. Do not continue to G23 with another local strengthening.

If the bounded public candidate attack fails, the next steps are stronger public shortest-homology-cycle enumeration, vertex-splitting/disjoint-paths/max-flow and generic CSP/SAT/CP-SAT. A failure of this first attack alone is not positive hardness evidence.

## Research pivot

Regardless of G22 outcome, the main research program now continues through:

- HGA — hidden geometric/algebraic actions;
- TDC — topology-derived codes/decoding;
- NAT — noisy algebraic/topological relations.

No security claim.
