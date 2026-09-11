# 60 — G22 same-side coupled genus-two multicurve control

## Status

**G22 is rejected by A-049, and the HGES exact-witness line is frozen after G22.** Public short-cycle enumeration plus compatibility search recovers accepted same-side rank-four multicurves on every measured instance.

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

The retained-per-signature cap and number of public tree samples are explicit attacker resources, not security parameters.

## Measured A-049 result

Exact Python 3.12 fixed `g22-6x9`:

```text
public V/E/F:                         105/321/214
Euler characteristic:                 -2
H1 dimension:                         4
public cycle-length bound:             30
public spanning-tree samples:          16
raw fundamental cycles:              3472
distinct bounded nonzero cycles:      884
retained candidates:                  105
exact-one candidate pairs:           1458
pair-pair compatibility tests:           3
selected lengths:                    (3,4,3,5)
selected signatures:                 (2,4,1,8)
selected signature rank:                4
selected vertex intersection matrix:  3,1,0,0 / 1,4,0,0 / 0,0,3,1 / 0,0,1,5
exact verifier accepted:              yes
```

The fixed candidate-signature histogram is:

```text
1:185, 2:191, 4:155, 5:22, 6:117,
8:91, 9:80, 11:11, 12:6, 13:17, 15:9
```

Python 3.12 sweep over `g22-4x4`, `g22-6x6`, `g22-6x9` × eight deterministic seeds gives **24/24** accepted public four-cycle families. Every selected family has signature rank four and the exact same-side vertex-intersection pattern required by the verifier.

Measured attack scale:

- `g22-4x4`: 1040 raw cycles; 309–380 distinct bounded nonzero cycles; 98–133 retained candidates; 1590–3899 exact-one pairs; successful compatibility search in 23–27,587 pair-pair tests;
- `g22-6x6`: 2320 raw cycles; 552–753 distinct cycles; 66–149 retained; 563–3652 exact-one pairs; success in 1–6801 tests;
- `g22-6x9`: 3472 raw cycles; 656–1029 distinct cycles; 73–147 retained; 689–3418 exact-one pairs; success in 3–67 tests.

Selected cycles are very short despite the public bounds: measured accepted lengths range from 3 to 12, and most selected cycles have length 3–5.

The dedicated G22 workflow passes on Python 3.11, 3.12 and 3.13 after the initial compile-only annotation fix.

## Result and freeze decision

**G22 is rejected by A-049.** Moving all cycles to the same side and requiring exact-one same-side intersections plus cross-pair vertex-disjointness does not create a useful inversion barrier. Public topology still supplies a dense family of short nontrivial cycles; a small compatibility search assembles an accepted rank-four witness.

This closes the planned HGES exact-witness program. There will be **no G23 incremental strengthening**. G0–G22 remain preserved as a negative-results corpus and as mandatory anti-pattern tests for future constructions.

The freeze is architectural, not a theorem that every topological problem is easy. The failed pattern is specifically: publish enough exact combinatorial structure for a verifier to recognize any equivalent witness, then hope one particular hidden witness is hard to recover.

## Research pivot

The active program continues through:

- **HGA** — hidden geometric/algebraic actions, where the secret is an action rather than an accepted decomposition;
- **TDC** — topology-derived codes/decoding, where hardness must come from noisy decoding rather than exact structure recovery;
- **NAT** — noisy algebraic/topological relations, where the public relation is deliberately approximate and denoising is the attack surface.

G22 receives no successor allocation unless a genuinely new exact-witness architecture is proposed that does not inherit the G0–G22 anti-patterns.

No security claim.
