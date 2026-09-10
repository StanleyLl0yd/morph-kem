# 23 — K1 non-orientable hyperbolic regular-map control

## Status

K1 is the first K-series experiment whose base cell map has genuinely hyperbolic regular-map type.

It is still a **negative control**, not a KEM, one-way function, trapdoor primitive, or security candidate.

## 1. Exact map

K1 uses the non-orientable regular map

~~~text
N4:{6,4}_3
~~~

with:

~~~text
V/E/F = 6/12/4
vertex degree = 4
face length = 6
Euler characteristic = -2
non-orientable genus = 4
underlying graph = K_{2,2,2}
~~~

Primary reference:

https://weddslist.com/rmdb/map.php?a=N4.2p

The database also states that its Petrie dual is the octahedron and that it has an orientable 2-fold cover S3:{6,4}.

Orientable cover reference:

https://www.weddslist.com/rmdb/map.php?a=R3.4p

Published small-genus classification:

Conder & Dobcsanyi, *Determination of all Regular Maps of Small Genus*, Journal of Combinatorial Theory, Series B 81 (2001), DOI 10.1006/jctb.2000.2008.

## 2. Construction

Rather than importing an opaque external permutation table, the implementation derives the four hexagonal faces as the four Petrie six-cycles of the octahedral skeleton K_{2,2,2}:

~~~text
(0,2,4,1,3,5)
(0,2,5,1,3,4)
(0,3,4,1,2,5)
(0,3,5,1,2,4)
~~~

Every one of the 12 skeleton edges occurs in exactly two face boundaries.

The computed Euler characteristic is:

~~~text
6 - 12 + 4 = -2
~~~

and the orientation equations are inconsistent.

## 3. Hyperbolic regular type

For a regular map of type {p,q}, K1 uses the exact combinatorial inequality

~~~text
2(p + q) < p q
~~~

which is equivalent to

~~~text
1/p + 1/q < 1/2.
~~~

For {6,4}:

~~~text
20 < 24.
~~~

Thus the universal regular tiling type is hyperbolic.

This geometric fact is not treated as a security argument.

## 4. Orientation-gauge relation

As in K0, each shared primal edge defines a public Z2 transition between adjacent face orientations.

Generation adds reference face gauges phi_f:

~~~text
T_fg = b_fg XOR phi_f XOR phi_g.
~~~

Because the base incidence publicly determines b_fg, a spanning tree recovers every phi_f relative to one global bit.

K1 therefore deliberately tests whether true hyperbolic/non-orientable combinatorics changes that conclusion.

## 5. Public orientation-double-cover attack

The public transitions also reconstruct the orientation double cover directly.

For each base face f and sheet s in {0,1}, create a local lifted face copy. Across a shared edge with transition T_fg, glue:

~~~text
(f, s)  <->  (g, s XOR T_fg).
~~~

No secret face gauge is needed.

The resulting public cover is then checked as a cell map.

Expected exact invariants:

~~~text
V/E/F = 12/24/8
Euler characteristic = -4
orientable = yes
orientable genus = 3
type {6,4}
~~~

These counts agree with the referenced orientable S3:{6,4} cover.

## 6. Exit criterion

K1 is rejected if:

- the hidden face gauges reduce to one global bit;
- the orientation cocycle is publicly normalized;
- the orientable double cover is publicly reconstructed.

That rejection would show that adding genuine hyperbolicity does not rescue an orientation-character trapdoor.

K2 must therefore use higher-order twisted data that cannot be removed by passing to the orientation double cover or by ordinary Z2 gauge fixing.

## 7. Security status

No one-wayness, average-case hardness, post-quantum, IND-CPA, IND-CCA, KEM, or production-security claim exists.


## 8. Measured result

Fixed master seed `34016490ffeeddccbbaa1234567890ab`, Python 3.12 CI runner.

~~~text
map: N4:{6,4}_3

base:
  V/E/F = 6/12/4
  vertex degree = 4
  face size = 6
  edge-face degree = 2
  chi = -2
  dual cycle rank = 9
  regular type hyperbolic = true
  orientable = false
  non-zero fundamental orientation syndromes = 6/9

gauge attack:
  public normalization = canonical normalization
  hidden face gauges recovered up to one global bit = true
  edge checks = 12

orientation double cover:
  V/E/F = 12/24/8
  chi = -4
  orientable = true
  genus = 3
  reconstructed from public transitions = true
~~~

## 9. Disposition

**K1 is rejected exactly as intended.**

The experiment distinguishes geometric/topological complexity from computational asymmetry:

1. the base map really is a non-orientable regular map of hyperbolic type;
2. the orientation obstruction is genuinely global;
3. nevertheless, the hidden face labels remain a linear Z2 gauge;
4. the public transition data reconstructs the orientable double cover directly.

Therefore K2 must not merely enlarge N4:{6,4}_3, switch to another regular non-orientable map, or add more orientation bits. It must introduce higher-order data whose useful witness does not collapse under the orientation character, orientation double cover, spanning-tree gauge normalization, or ordinary bounded-local CSP flattening.
