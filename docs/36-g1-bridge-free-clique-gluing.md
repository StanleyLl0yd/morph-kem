# 36 — G1 bridge-free HGES clique-decomposition negative control

## Status

**G1 is an attack calibration in progress. No hardness or security conclusion is permitted until the dedicated exact-head workflow records the public attacks.**

G1 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Question

G0 was intentionally broken by A-024 because its hidden assembly graph was a tree. Every inter-piece triangular-face gluing became a bridge in the public tetrahedron dual graph, so deleting all bridges recovered the pieces exactly.

G1 asks a narrower question:

> If the exact bridge shortcut is removed, does the same piece family remain publicly decomposable for an even simpler local reason?

The expected answer is yes. G1 deliberately keeps the G0 piece family so that the next attack harness can be calibrated against the public `K4` signature before any less canonical piece family is considered.

## Construction

The allowed piece is unchanged from G0: the 3-ball obtained from the boundary of a 4-simplex by deleting one tetrahedral facet.

It has four tetrahedra

~~~text
0234
0134
0124
0123
~~~

and four boundary triangle ports

~~~text
234
134
124
123
~~~

Its tetrahedron dual graph is exactly `K4`.

For `n` pieces, G1:

1. creates `n` disjoint copies of the allowed piece;
2. arranges the piece indices in one simple cycle;
3. uses two distinct boundary ports per piece;
4. identifies each paired boundary triangle by the fixed canonical vertex order;
5. forms the vertex quotient;
6. applies an independently seeded global public vertex relabeling;
7. sorts the public tetrahedra;
8. retains the planted partition/cycle/port data only as reference evidence.

The fixed toy sets are:

~~~text
g1-4   4 pieces   16 tetrahedra
g1-8   8 pieces   32 tetrahedra
g1-12 12 pieces   48 tetrahedra
~~~

The master seed affects only the final public relabeling in this calibration. The cycle gluing itself is fixed so that the structural attack question is isolated from rejection-sampling or face-map-distribution effects.

## Public relation

A witness is any partition of all public tetrahedra into `n` four-tetrahedron groups such that:

- every tetrahedron appears exactly once;
- every group is an allowed punctured-4-simplex 3-ball under the same exact local predicate used by G0;
- public triangular-face incidence is at most two;
- exactly `n` triangular faces are shared between distinct candidate groups;
- those cross-group faces define `n` distinct group pairs;
- the cross-group graph is connected and every group has degree two.

Thus the accepted cross-piece graph is a simple cycle.

The verifier never asks whether the submitted cycle or partition is the planted one. Any accepted equivalent witness is attacker success.

## Structural predictions

For the fixed canonical cycle gluing, the expected public counts are

~~~text
V = 2n + 2
E = 7n + 1
F = 9n
T = 4n
chi = 1
boundary triangles = 2n
dual edges = 7n
~~~

The dual graph consists of `n` internal `K4` blocks plus `n` inter-piece edges arranged cyclically.

Therefore:

- no inter-piece dual edge is a bridge;
- the full dual graph has no articulation vertex;
- low-order separators can still exist;
- every planted piece remains a four-vertex dual clique;
- because only one dual edge joins each adjacent pair of blocks, no cross-block four-vertex set can become a `K4`.

The final point is the intended G1 failure mode.

## A-024 regression gate

G1 first re-runs the existing public bridge attack.

Expected result:

~~~text
bridge count = 0
bridge-block decomposition = one 4n-tetrahedron component
G1 verifier acceptance = no
~~~

This is not positive evidence. It only proves that the exact G0 shortcut was removed.

## A-028 — public K4 / allowed-piece exact-cover recovery

A-028 uses only the public quotient tetrahedra.

1. Build triangular-face incidence and the tetrahedron dual graph.
2. Enumerate public four-tetrahedron subsets.
3. Keep subsets whose four dual vertices induce a `K4`.
4. Apply the exact allowed-piece predicate to each retained subset.
5. Build the exact-cover relation over public tetrahedra.
6. Enumerate accepted covers up to an explicit solution cap.
7. Submit the first accepted cover to the G1 public verifier.
8. Compare to the planted partition only after public success has already been established.

The implementation intentionally uses transparent exhaustive `4`-subset enumeration for the toy calibration. This is at most polynomial fourth-degree work in the number of tetrahedra because the candidate size is fixed at four; it is not intended as an optimized clique algorithm.

For the current dual graph construction, the analytic expectation is stronger: exactly the `n` planted internal `K4` blocks survive the clique test, so the exact cover is unique up to group order.

If exact-head CI confirms this, **G1 must be rejected**. Increasing `n` would not repair the structural leak.

## Separator measurement

The workflow also records:

- dual bridge count;
- articulation-point count;
- the number of unordered pairs of dual vertices whose removal disconnects the graph.

The two-vertex-separator measurement is diagnostic. A-028 does not depend on finding those separators, but recording them prevents the research log from treating 2-edge/2-vertex connectivity as synonymous with decomposition resistance.

## Rejection gate

Reject G1 if the public A-028 attack finds any accepted partition with practical toy work. Exact recovery of generation history is not required.

If G1 is rejected as expected, the next HGES stage must change the structural family rather than merely increase the cycle size. In particular, it should remove the exact `K4` piece signature through overlap, subdivision, mixed piece types, or another construction in which the planted pieces are not directly the maximal fixed-size dual cliques.

Before any trapdoor work, that successor must still face:

- bridge/articulation/low-order separator decomposition;
- local role and apex/boundary signatures;
- piece automorphism normalization;
- exact-cover / SAT / CP-SAT recovery;
- equivalent-witness enumeration;
- statistical leakage of planted roles.

No security claim.
