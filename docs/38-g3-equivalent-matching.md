# 38 — G3 indistinguishable-edge equivalent-matching control

## Status

**G3 is an attack calibration in progress. No hardness or security conclusion is permitted until exact-head CI records the public matching attack.**

G3 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Motivation

G0 failed because the hidden assembly itself was canonically visible through dual-graph bridges. G1 removed those bridges but failed because every piece remained an exact public `K4`. G2 subdivided those pieces, but public stellar-center contraction reconstructed the already-broken G1 macro relation.

G3 changes the piece family instead of adding another representation layer. The goal is to remove a locally privileged planted boundary and ask what equivalent-witness semantics does when **every local adjacency is a plausible piece boundary choice**.

## Construction

One allowed piece consists of two tetrahedra

~~~text
A = 0123
B = 0124
~~~

sharing face `012`.

For `n` pieces, `B_i` is externally glued to `A_(i+1)` along one triangular boundary face. The canonical quotient is chosen so the tetrahedron dual graph is exactly

~~~text
A0 -- B0 -- A1 -- B1 -- ... -- A(n-1) -- B(n-1) -- A0
~~~

That is the even cycle `C_(2n)`.

Every dual edge, both planted internal and planted external, joins two tetrahedra sharing exactly one triangular face, using five total vertices. Therefore every dual edge satisfies the same public allowed-piece predicate.

Generation then applies an independently seeded global public vertex relabeling and sorts the tetrahedra. The planted alternating matching is retained only as reference evidence.

Toy sets:

~~~text
g3-3   3 pieces   6 tetrahedra
g3-5   5 pieces  10 tetrahedra
g3-8   8 pieces  16 tetrahedra
~~~

## Public relation

A witness is any partition of all public tetrahedra into `n` valid adjacent pairs such that the cross-group shared-face graph is a connected simple cycle.

The verifier never asks for the planted alternating phase. Any accepted equivalent decomposition is attacker success.

## Structural predictions

For the canonical gluing:

~~~text
V = 2n + 2
E = 6n + 1
F = 6n
T = 2n
chi = 1
boundary triangles = 4n
dual edges = 2n
~~~

The dual graph has degree histogram `{2: 2n}`, zero bridges and zero articulation vertices.

Public vertex stars are intentionally non-discriminating. There are two global vertices incident to all `2n` tetrahedra, while each of the remaining `2n` vertices is incident to exactly two adjacent tetrahedra. Those degree-two stars expose **all** dual edges, not the planted matching phase.

## A-030 — equivalent perfect-matching recovery

A-030 uses only public incidence:

1. build the tetrahedron dual graph;
2. keep every dual edge that satisfies the exact allowed two-tetrahedron piece predicate;
3. enumerate perfect matchings with a deterministic exact backtracking search;
4. submit each matching to the exact G3 verifier;
5. compare with the planted matching only after public acceptance has already been established.

A single even cycle has exactly two alternating perfect matchings. The expected negative-control result is that both are accepted and one differs from the planted partition.

If exact-head CI confirms this, **G3 is rejected**. Increasing `n` cannot repair the conceptual problem: local indistinguishability has produced another valid attacker witness rather than hiding the planted one.

## Measurements

The workflow records:

- public `V/E/F/T`, Euler characteristic, boundary faces and max face incidence;
- dual vertices/edges and degree histogram;
- bridges and articulation points;
- public allowed candidate dual edges;
- public degree-two vertex-star candidate pairs;
- vertex/tetrahedron incidence histogram;
- exact matching count, solution cap, nodes and backtracks;
- accepted matching count;
- accepted non-planted matching count;
- deterministic all-size, eight-seed sweep.

## Successor gate

If G3 fails as expected, G4 must introduce genuinely nonlocal coupling between otherwise plausible local decomposition choices. Before any positive interpretation, that coupling must be attacked as parity/cohomology/gauge, constrained matching, low-width CSP, exact cover, SAT/CP-SAT and equivalent-witness search.

No trapdoor work follows merely from hiding the planted local phase.

No security claim.
