# 36 — G1 HGES bridge-free cycle gluing

## Status

**G1 is rejected by A-028 and independently by A-029.**

The experiment successfully removes G0's bridge/articulation decomposition, but the retained punctured-4-simplex piece is itself publicly recognizable. The result isolates a second HGES failure mode: hiding the assembly graph is insufficient when each piece has a canonical local signature.

G1 is a falsification experiment, not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security claim.

## Goal

G0 was intentionally easy because every inter-piece gluing was a bridge in the public tetrahedron dual graph. G1 changes the assembly graph from a tree to a simple cycle while retaining the same piece for one controlled step.

The required structural gate was:

~~~text
connected tetrahedron dual graph
zero graph bridges
zero articulation vertices
4n dual vertices
7n dual edges = 6n internal K4 edges + n cycle attachments
~~~

Passing that gate is necessary but not evidence of hardness. It merely ensures that A-024's exact G0 shortcut is gone before testing piece recognizability.

## Piece and cycle construction

The allowed piece is still the four-tetrahedron 3-ball obtained by deleting one tetrahedral facet from the boundary of a 4-simplex:

~~~text
0234
0134
0124
0123
~~~

Its four boundary ports are:

~~~text
234
134
124
123
~~~

G1 uses port `134` as the outgoing port of piece `i` and port `234` as the incoming port of piece `i+1`.

The two ports share local coordinates 3 and 4. Generation fixes local coordinate `1 -> 2` and uses a seeded optional swap of `3 <-> 4`. The final cycle swap is chosen so total swap parity is even. This closes the cycle without identifying local coordinates 3 and 4 inside a piece, so no rejection-loop is needed.

After quotienting, a separate seeded global vertex permutation is applied and public tetrahedra are sorted. The planted piece partition, local apex labels, cycle order, and boundary maps are not public attack inputs.

## Public verifier

A candidate witness is any partition of all public tetrahedra into `n` groups such that:

- every tetrahedron occurs exactly once;
- every group is the allowed four-tetrahedron 3-ball under the exact combinatorial predicate;
- face incidence is at most two;
- exactly `n` cross-group triangular faces exist;
- those cross-group adjacencies are distinct, connected, and every group has degree two.

Thus the cross-piece graph must be a simple cycle. The verifier does not compare the candidate partition or cycle order with generation history.

## Exact public structure

For the parity-conditioned cycle family:

~~~text
V = 2n + 2
E = 7n + 1
F = 9n
T = 4n
chi = 1
boundary triangles = 2n
dual edges = 7n
~~~

Every piece contributes two tetrahedra of dual degree 3 and two of dual degree 4:

~~~text
dual degree histogram = {3: 2n, 4: 2n}
~~~

More importantly, the interior apex of each original piece is untouched by boundary gluing and belongs to exactly its four tetrahedra. Public vertex/tetrahedron incidence therefore contains:

~~~text
n vertices of tetrahedron-degree 4   <- one per hidden piece apex
n vertices of tetrahedron-degree 6
2 vertices of tetrahedron-degree 3n
~~~

That is the A-028 leakage.

## A-028 — public vertex-star piece recovery

A-028 uses only the public quotient:

1. build `vertex -> incident tetrahedra` incidence;
2. take stars containing exactly four tetrahedra;
3. validate each star against the public allowed-piece predicate;
4. solve exact cover of all public tetrahedra by valid stars;
5. submit the resulting partition to the public cycle verifier.

On every measured G1 instance, there are exactly `n` degree-4 candidate vertices and exactly `n` valid piece candidates. They are disjoint and already form the unique accepted exact cover found by the attack. No backtracking occurs.

## A-029 — public dual-K4 piece recovery

A-029 is an independent attack that does not use public vertex stars.

It:

1. builds the public tetrahedron dual graph from shared triangular faces;
2. enumerates four-vertex subsets;
3. keeps only 4-cliques;
4. filters those cliques through the exact allowed-piece predicate;
5. solves exact cover and verifies the resulting cycle decomposition.

The G1 dual graph contains exactly one `K4` per planted piece and no spurious 4-cliques on the measured family. Therefore A-029 also recovers the same decomposition without backtracking.

## Exact-head Python 3.12 baseline

Fixed seed:

~~~text
76120450aabbccddeeff001122334455
~~~

`g1-8`:

~~~text
pieces:                                  8
public V/E/F/T:                          18/57/72/32
Euler characteristic:                   1
boundary faces / max face incidence:    16/2
dual graph vertices / edges:            32/56
dual bridges / articulation vertices:   0/0
dual degree histogram:                  ((3,16),(4,16))
vertex tetrahedron-degree histogram:     ((4,8),(6,8),(24,2))
face occurrences / DFS edge scans:       128/112
cycle swap bits:                         (0,0,0,1,0,1,1,1)
reference witness accepted:              yes

A-028:
  candidate vertices / valid pieces:     8/8
  exact-cover nodes/backtracks/solutions: 9/0/1
  accepted:                              yes
  matches planted partition up to order: yes

A-029:
  4-subset checks:                       35,960
  K4 candidates / valid pieces:          8/8
  exact-cover nodes/backtracks/solutions: 9/0/1
  accepted:                              yes
  matches planted partition up to order: yes
~~~

## Deterministic sweep

Python 3.12 tested `g1-3`, `g1-5`, and `g1-8` over eight independently derived seeds each.

| Set | Pieces | V/E/F/T | Dual edges | Bridges/articulations | A-028 candidates | A-028 nodes/backtracks | A-029 subset checks | A-029 candidates | A-029 nodes/backtracks |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| g1-3 | 3 | 8/22/27/12 | 21 | 0/0 | 3 | 4/0 | 495 | 3 | 4/0 |
| g1-5 | 5 | 12/36/45/20 | 35 | 0/0 | 5 | 6/0 | 4,845 | 5 | 6/0 |
| g1-8 | 8 | 18/57/72/32 | 56 | 0/0 | 8 | 9/0 | 35,960 | 8 | 9/0 |

Across all 24 generated instances:

~~~text
structural gate with zero bridges:       24/24
structural gate with zero articulations: 24/24
A-028 accepted recovery:                 24/24
A-028 matched planted partition:         24/24
A-029 accepted recovery:                 24/24
A-029 matched planted partition:         24/24
~~~

Python 3.11, 3.12 and 3.13 all pass compile, G0/G1 unit tests, and the fixed G1 baseline. Python 3.12 additionally passes the full 24-instance sweep.

## Decision

**Reject G1. Do not scale the cycle.**

This is a stronger diagnostic than G0 because A-024's assembly separator has actually been removed: the public dual graph has no bridges and no articulation vertices. The failure persists for a different reason.

A-028 is structural across the whole current family. As long as every hidden piece has a private interior apex belonging to exactly four tetrahedra and boundary gluing never touches it, the piece partition is explicitly visible in public vertex-star incidence. Increasing `n` cannot repair that.

A-029 independently shows that even deleting or obscuring apex metadata would not be enough while each piece remains the unique `K4` block of the tetrahedron dual graph.

The next successor therefore must change the **piece family**, not just the assembly graph.

## Next gate — G2

G2 should deliberately make internal and external gluing faces locally indistinguishable before attempting any sophisticated hardness claim.

The cleanest next control is a two-tetrahedron 3-ball piece. Assemble `n` copies so the entire public tetrahedron dual graph is one even cycle `C_{2n}`:

~~~text
internal piece edge
external gluing edge
internal piece edge
external gluing edge
...
~~~

Every adjacent tetrahedron pair then has the same local allowed-piece type. The public graph has two alternating perfect matchings, either of which partitions the cycle into valid two-tetrahedron pieces. Under equivalent-witness semantics both are attacker successes.

This intentionally tests a third failure mode:

> removing local piece signatures may create many cheap equivalent decompositions instead of hardness.

The mandatory G2 attack should therefore be public perfect-matching / exact-cover recovery plus enumeration of equivalent decompositions. If the two alternating decompositions are accepted as predicted, G2 is another negative control and the next design problem becomes coupling piece choice to genuinely nonlocal boundary data without reintroducing canonical labels.

No trapdoor search begins at G2.

## Security status

No one-wayness, average-case hardness, post-quantum hardness, IND-CPA, IND-CCA, KEM, or production-security claim exists.
