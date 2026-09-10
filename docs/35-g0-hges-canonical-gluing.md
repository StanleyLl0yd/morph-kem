# 35 — G0 HGES canonical-gluing negative control

## Status

**Negative control under exact-head CI. Expected outcome: A-024 recovers the gluing decomposition publicly.**

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

This is an analytic prediction of the negative-control break. CI is testing the implementation and verifier, not looking for evidence of hardness.

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

## Toy parameter sets

~~~text
g0-3: 3 pieces, path assembly
g0-5: 5 pieces, branched tree
g0-8: 8 pieces, larger branched tree
~~~

The exact-head baseline uses `g0-8`. The Python 3.12 sweep additionally runs all three parameter sets over eight independently derived deterministic seeds. Python 3.11 and 3.13 run the unit tests and fixed baseline.

## Rejection interpretation

Expected result:

> **A-024 recovers an accepted gluing witness and G0 is rejected as designed.**

If this fails, the correct interpretation is a bug in the generator, verifier, or attack harness — never evidence of hardness.

A G1 successor is permitted only after G0 behaves as expected. G1 should first remove the exact bridge shortcut, for example by using a 2-edge-connected assembly/overlapping gluing pattern, and then face richer public attacks: separator decomposition, piece automorphisms, boundary signatures, SAT/CP-SAT pairing recovery, isomorphism normalization, and equivalent-witness search.

No trapdoor search starts at G0.

## Relation to established triangulation machinery

Dual/face-pairing graphs and relabeling-invariant triangulation representations are standard tools in computational low-dimensional topology; they are an attack surface, not a security feature. The broader canonical-decomposition warning is also established 3-manifold territory. G0 intentionally uses a much simpler bridge-block decomposition so the first HGES attack is completely auditable inside this repository.

References:

- B. A. Burton, *Enumeration of non-orientable 3-manifolds using face-pairing graphs and union-find*, Discrete & Computational Geometry 38 (2007), 527–571. DOI: `10.1007/s00454-007-1307-x`.
- R. Burke, B. Burton, J. Spreer, *Small Triangulations of 4-Manifolds and the 4-Manifold Census*, Discrete & Computational Geometry (2026). DOI: `10.1007/s00454-026-00818-w`. The paper explicitly treats dual/face-pairing graphs and isomorphism signatures as core triangulation machinery.
- W. D. Neumann, G. A. Swarup, *Canonical decompositions of 3-manifolds*, Geometry & Topology 1 (1997), 21–40, arXiv:`math/9712227`.

## Security status

No one-wayness, average-case hardness, post-quantum hardness, IND-CPA, IND-CCA, KEM, or production-security claim exists.
