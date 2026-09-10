# 38 — G3 indistinguishable-edge equivalent-matching control

## Status

**G3 is rejected by A-030 on the measured generated distribution.**

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

## Structural formulas

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
3. enumerate perfect matchings using MRV branching on the unmatched vertex with the fewest remaining candidate edges;
4. submit each matching to the exact G3 verifier;
5. compare with the planted matching only after public acceptance has already been established.

The first implementation used the smallest public vertex label as its branch pivot. It still found the two valid matchings, but public tetrahedron relabeling changed the amount of dead-end search. The final exact-head attack uses MRV. On an even cycle, after the initial two-way phase choice every remaining choice is forced, giving relabel-stable work counters.

## Exact Python 3.12 `g3-8` result

~~~text
pieces:                                  8
public V/E/F/T:                          18/49/48/16
Euler characteristic:                   1
boundary faces / max face incidence:    32/2
dual graph vertices / edges:            16/16
dual degree histogram:                  ((2,16),)
bridges / articulation points:           0/0
allowed candidate dual edges:            16
vertex-star candidate pairs:              16
vertex tetrahedron-degree histogram:     ((2,16),(16,2))
face occurrence checks:                  64
perfect matchings / cap:                  2/16
matching cap hit:                        no
matching nodes / backtracks:             17/0
accepted decompositions:                  2
accepted non-planted decompositions:      1
reference witness accepted:              yes
~~~

## Deterministic sweep

Python 3.12 tested `g3-3`, `g3-5`, and `g3-8` over eight independently derived public relabel seeds each.

| Set | V/E/F/T | Boundary | Dual edges | Candidate edges | Vertex-star pairs | Matching nodes/backtracks | Accepted | Non-planted accepted |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| g3-3 | 8/19/18/6 | 12 | 6 | 6 | 6 | 7/0 | 2 | 1 |
| g3-5 | 12/31/30/10 | 20 | 10 | 10 | 10 | 11/0 | 2 | 1 |
| g3-8 | 18/49/48/16 | 32 | 16 | 16 | 16 | 17/0 | 2 | 1 |

Across all **24/24** generated instances:

- the dual graph has zero bridges and zero articulation vertices;
- every dual edge is a valid allowed-piece candidate;
- all degree-two public vertex stars expose the same full candidate-edge set;
- A-030 finds exactly two perfect matchings;
- both matchings pass the exact G3 verifier;
- exactly one accepted decomposition differs from the planted partition;
- matching search has zero backtracking after MRV strengthening.

The dedicated workflow succeeds on Python 3.11, 3.12 and 3.13.

## Result

**G3 is rejected by A-030.**

This failure is deliberately different from G1. The pieces are no longer singled out by a unique public fixed-size motif: every local adjacency is plausible. But under equivalent-witness semantics this creates another public solution rather than hiding the planted one. The two alternating perfect matchings of the even cycle are both accepted witnesses.

Increasing `n` cannot repair this structural fact. The attack remains a public matching problem with two alternating solutions; the measured MRV search uses `2n+1` nodes and zero backtracking on the current family.

This is not a theorem that general HGES is easy. It is a falsification of this generated distribution.

## G4 gate

G4 may add genuinely nonlocal coupling between otherwise plausible local decomposition choices. Before any positive interpretation, that coupling must be attacked as:

- parity / cycle-space / cohomology / gauge reduction;
- constrained matching and factor-graph propagation;
- low-width dynamic programming;
- exact-cover / CSP / SAT / CP-SAT recovery;
- automorphism and normalization attacks;
- equivalent-witness enumeration;
- planted-role statistical leakage.

No trapdoor work follows merely from hiding the planted local phase.

No security claim.
