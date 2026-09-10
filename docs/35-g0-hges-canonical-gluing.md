# 35 — G0 HGES canonical-gluing negative control

## Status

**G0 is rejected as designed by A-024. The public dual-graph bridge attack recovers the canonical gluing decomposition exactly on the measured distribution.**

G0 is not a hardness candidate, trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction. Its job is to make sure the HGES attack harness breaks a distribution that is deliberately canonically decomposable.

## Why this experiment exists

K2.4 ranked **HGES — Hidden Gluing Equivalence Search** behind BTTS. T0/T1 then rejected the first BTTS/Pachner generated distributions. HGES therefore becomes the next executable frontier.

The main warning from K2.4 was that a gluing construction can publish enough topology/combinatorics to expose a canonical decomposition. G0 tests that warning in the simplest exact 3-dimensional setting before trying to hide or overlap pieces.

This is only a graph-theoretic canonical-separator control. It is **not** an implementation of JSJ decomposition or a claim that all 3-manifold gluings reduce to graph bridges.

## Piece family

The one allowed piece is the triangulated 3-ball obtained from the boundary of a 4-simplex by deleting one tetrahedral facet.

With local vertices `0,1,2,3,4`, the four retained tetrahedra are

~~~text
0234
0134
0124
0123
~~~

and the four boundary triangle ports are

~~~text
234
134
124
123
~~~

The tetrahedron dual graph inside one piece is `K4`: every pair of retained tetrahedra shares one triangular face.

One isolated piece has

~~~text
V/E/F/T = 5/10/10/4
boundary triangles = 4
Euler characteristic = 1
~~~

## Generated distribution

For `n` pieces:

1. make `n` disjoint copies of the allowed 3-ball;
2. choose a fixed toy assembly tree of maximum degree at most four;
3. assign a distinct boundary port to every incident assembly edge;
4. identify the two boundary triangles using a deterministic seeded permutation;
5. quotient the vertex identifications;
6. apply an independent deterministic seeded global vertex relabeling;
7. sort public tetrahedra and discard the planted local labels/partition from the public instance.

The reference partition, tree and port choices exist only as generation evidence.

The public instance contains only:

~~~text
parameter-set name
piece count n
quotient tetrahedron list
~~~

The planted assembly tree and local piece labels are not public inputs to A-024.

## Exact structural expectations

Because the assembly graph is a tree, no gluing path returns to identify two vertices inside the same piece. Each boundary-face gluing merges three vertex pairs, three edge pairs and the two copies of one triangular face.

Therefore the generated family has

~~~text
V = 2n + 3
E = 7n + 3
F = 9n + 1
T = 4n
chi = 1
boundary triangles = 2n + 2
~~~

The tetrahedron dual graph contains:

~~~text
6n       internal K4 edges
n - 1    inter-piece gluing edges
7n - 1   total dual edges
~~~

Every inter-piece edge is a graph bridge, while no internal `K4` edge is a bridge. Deleting all bridges must therefore recover exactly `n` four-tetrahedron blocks.

This is an analytic prediction of the negative-control break. CI tests the implementation and verifier, not cryptographic hardness.

## Public relation

A witness is any partition of all public tetrahedra into `n` groups such that:

- every tetrahedron occurs exactly once;
- every group contains four tetrahedra;
- the four tetrahedra use five vertices, have one common vertex and intersect pairwise in triangular faces, i.e. they form the allowed punctured-4-simplex 3-ball;
- public triangular-face incidence never exceeds two;
- cross-group shared triangular faces form a connected graph with exactly `n-1` edges.

The verifier never compares the candidate partition to generation history. Any accepted equivalent partition is attacker success.

## A-024 — dual-graph bridge gluing recovery

The public attack:

1. enumerates triangle incidence from the public tetrahedron list;
2. constructs the tetrahedron dual graph;
3. finds graph bridges with a DFS low-link computation;
4. removes the bridges;
5. returns the remaining connected components as the candidate piece partition;
6. submits that partition to the exact public verifier.

Measured work counters are structural rather than wall-clock based:

- tetrahedron-face occurrences inspected;
- dual edges;
- DFS adjacency-edge scans;
- bridge count;
- component-size profile;
- verifier acceptance;
- equality with the planted partition up to group order, used only after the public attack completes.

## Exact-head measurements

Fixed master seed:

~~~text
76120450aabbccddeeff001122334455
~~~

Python 3.12 exact-head baseline for `g0-8`:

~~~text
pieces:                                      8
public V/E/F/T:                              19/59/73/32
Euler characteristic:                       1
boundary faces / max face incidence:         18/2
dual graph vertices / edges:                 32/55
dual bridges:                                7
bridge component sizes:                      (4,4,4,4,4,4,4,4)
face occurrence checks:                      128
DFS edge scans:                              110
reference witness accepted:                  yes
public bridge witness accepted:              yes
recovered partition = planted up to order:   yes
~~~

The deterministic Python 3.12 sweep covered all three parameter sets and eight independently derived seeds each: **24/24 public bridge recoveries were accepted and 24/24 matched the planted partition up to group order.**

Per-size structural counters were invariant across the eight tested seeds:

| Set | Pieces | V/E/F/T | Boundary | Dual edges | Bridges | Component sizes | Face occurrences | DFS scans | Accepted/matched |
|---|---:|---|---:|---:|---:|---|---:|---:|---:|
| g0-3 | 3 | 9/24/28/12 | 8 | 20 | 2 | 4/4/4 | 48 | 40 | 8/8 |
| g0-5 | 5 | 13/38/46/20 | 12 | 34 | 4 | 4/4/4/4/4 | 80 | 68 | 8/8 |
| g0-8 | 8 | 19/59/73/32 | 18 | 55 | 7 | 4/4/4/4/4/4/4/4 | 128 | 110 | 8/8 |

Python 3.11, 3.12 and 3.13 all passed compile, unit-test and fixed-baseline jobs; Python 3.12 additionally passed the complete 24-instance sweep.

## Decision

**A-024 succeeds exactly as the negative-control analysis predicts. G0 is rejected as designed, and the HGES public decomposition attack harness is validated.**

The result is stronger than an isolated runtime observation for this family: the tree-of-`K4` dual-graph structure makes every inter-piece gluing edge a bridge by construction. Increasing the number of pieces leaves the same public linear-time graph decomposition.

This does not show that arbitrary hidden gluing equivalence search is easy. It rejects this deliberately canonical distribution and establishes the minimum attack that every successor must defeat.

## Next gate — G1

G1 may now remove the exact bridge shortcut, but it must change structure rather than merely scale G0. The minimal controlled successor should use a 2-edge-connected assembly or overlapping gluing pattern and immediately test whether the pieces are still publicly recoverable as maximal `K4`-like dual subgraphs or via other low-order separators.

Mandatory G1 attacks include:

- bridge, articulation and low-order separator decomposition;
- enumeration of allowed piece subcomplexes / maximal `K4`-like dual blocks;
- local apex and boundary-port signatures;
- piece-automorphism normalization;
- exact-cover / SAT / CP-SAT partition and pairing search;
- equivalent-witness enumeration where tractable.

No trapdoor search starts merely because the bridge attack has been removed.

## Relation to established triangulation machinery

Dual/face-pairing graphs and relabeling-invariant triangulation representations are standard tools in computational low-dimensional topology; they are an attack surface, not a security feature. The broader canonical-decomposition warning is also established 3-manifold territory. G0 intentionally uses a much simpler bridge-block decomposition so the first HGES attack is completely auditable inside this repository.

References:

- B. A. Burton, *Enumeration of non-orientable 3-manifolds using face-pairing graphs and union-find*, Discrete & Computational Geometry 38 (2007), 527–571. DOI: `10.1007/s00454-007-1307-x`.
- R. Burke, B. Burton, J. Spreer, *Small Triangulations of 4-Manifolds and the 4-Manifold Census*, Discrete & Computational Geometry (2026). DOI: `10.1007/s00454-026-00818-w`.
- W. D. Neumann, G. A. Swarup, *Canonical decompositions of 3-manifolds*, Geometry & Topology 1 (1997), 21–40, arXiv:`math/9712227`.

## Security status

No one-wayness, average-case hardness, post-quantum hardness, IND-CPA, IND-CCA, KEM, or production-security claim exists.
