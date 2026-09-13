# 78 — NAT6 flat-torus A5 global-holonomy control

## Status

**NAT6 is rejected structurally.** NAT-A007 already showed that an irregular torus with genuine flat global holonomy is not hidden: public tree normalization plus enumeration of 30 legal `A5` commuting-involution pairs recovers the unique verifier-accepted decomposition on every measured instance.

A stronger independent attack, **NAT-A008**, removes even that constant-size group enumeration. Two public fundamental cycles with independent `(alpha,beta)` pairings determine the hidden holonomy generators algebraically, after which one tree propagation recovers the normalized vertex gauge. This succeeds on all 24 measured instances.

NAT6 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Construction

Reuse the G16 flip-mixed irregular torus families `6x6`, `6x9`, and `8x9`. From the public triangulation compute two deterministic independent binary 1-cocycles `alpha,beta` spanning `H^1(T^2; F2)` modulo coboundaries.

Choose a seeded ordered pair of distinct commuting involutions `x,y in A5`. These generate a Klein-four subgroup. For each canonically oriented public edge `e=(u,v)` define

```text
c_e = x^alpha[e] y^beta[e].
```

Because `alpha,beta` are cocycles and `x,y` commute with order two, every triangular face has identity core holonomy while noncontractible torus cycles can retain nontrivial global holonomy.

Hide the core under a normalized seeded vertex gauge `g_v in A5`:

```text
observed_uv = g_u^-1 c_uv g_v,
g_0 = 1.
```

The verifier accepts any normalized `A5` gauge and any ordered pair of distinct commuting involutions that exactly reproduces all public edges. It never compares to the planted decomposition.

## NAT-A007 — finite representation enumeration

Choose a deterministic public spanning tree and integrate the observed connection along it. Gauge-transform every public edge by this tree integration. Tree residuals become identity and non-tree residuals are holonomies of public fundamental cycles.

NAT-A007 enumerates the 30 ordered pairs of distinct commuting involutions in `A5`. For each pair it builds the public `alpha,beta` core, propagates one normalized gauge on the tree, and checks every edge exactly.

Across all measured instances this returns exactly one accepted pair/gauge decomposition, equal to the planted pair/gauge after public success.

## NAT-A008 — direct fundamental-holonomy solve

The 30-pair enumeration is unnecessary for the actual NAT6 relation.

For any non-tree edge `e`, let `z_e` be the corresponding public fundamental cycle formed by `e` plus the unique tree path between its endpoints. The public cocycles give

```text
p_e = (<alpha,z_e>, <beta,z_e>) in F2^2.
```

After tree normalization, the residual on `e` is exactly

```text
h_e = x^p_e[0] y^p_e[1].
```

Scan public non-tree edges until two nonzero, distinct pairing vectors are found. In `F2^2`, any two distinct nonzero vectors are linearly independent. If

```text
p1 = (a,b)
p2 = (c,d)
```

then the determinant `ad + bc = 1`, and the two public residual holonomies `h1,h2` determine `x,y` directly using the inverse binary 2x2 matrix. Because the current NAT6 hidden generators are commuting involutions, the required exponent arithmetic is exactly over `F2`.

After recovering `(x,y)`, propagate the unique normalized gauge once along the public tree and submit the result to the original exact verifier. The planted reference is consulted only after public acceptance.

This attack never enumerates `A5`, never searches vertex assignments, and never needs the generation history.

## Fixed Python 3.12 result

For `nat6-8x9`, the original NAT-A007 calibration is:

```text
V/E/F:                              72 / 216 / 144
Euler characteristic:                         0
edge incidence min/max:                    2 / 2
H1 dimension:                                  2
alpha / beta weights:                    20 / 23
nonidentity face holonomies:                   0
tree / non-tree edges:                   71 / 145
normalized nonidentity residuals:              39
normalized distinct nonidentity residuals:      3
commuting pair candidates / tested:       30 / 30
vertex propagation assignments:              2130
accepted decompositions:                        1
```

The stronger NAT-A008 fixed baseline needs only:

```text
fundamental cycles scanned:                    24
fundamental path-edge scans:                  109
pairing vectors:                     (1,1) / (0,1)
vertex propagation assignments:               71
exact verifier accepted:                      yes
recovered pair matches planted:               yes
recovered gauge matches planted:              yes
```

So the direct attack replaces 30 full gauge propagations by one.

## Eight-seed / multi-size direct sweep

Across `nat6-6x6`, `nat6-6x9`, and `nat6-8x9` × eight deterministic seeds (**24 public instances**):

- NAT-A008 finds two independent public fundamental-cycle pairing vectors on **24/24**;
- exact verifier acceptance succeeds on **24/24**;
- recovered holonomy pair matches planted after public success on **24/24**;
- recovered normalized gauge matches planted after public success on **24/24**;
- only one gauge propagation is performed per instance: exactly `35`, `53`, or `71 = V-1` assignments;
- fundamental cycles scanned range from **7 to 51**;
- tree-path edge scans range from **24 to 218**.

The fixed-size group enumeration is therefore not the source of the break.

## Structural interpretation

NAT6 confirms a real topological distinction from NAT4: flatness on a torus is not pure gauge. Genuine global holonomy survives.

But the specific hidden relation still publishes enough structure to reconstruct that holonomy. Once a spanning tree is fixed, the remaining non-tree residuals are a public representation of fundamental cycles. Because the hidden core is explicitly parameterized by a public `H^1(T^2;F2)` basis and two commuting involutions, two independent cycle evaluations solve the hidden generators directly.

For this architecture, increasing the torus dimensions does nothing, and merely enlarging the ambient finite group does not repair the direct algebraic recovery as long as the secret is still two commuting order-two generators carried on the same public binary cohomology basis.

A successor must change the global relation itself: for example, a representation problem not linearly coordinatized by a public cohomology basis and not exposed by tree gauge normalization. Such a successor must still be attacked immediately by spanning-tree normalization, fundamental-group representation recovery, conjugacy normalization, finite quotients and generic constraint solving.

No security claim.