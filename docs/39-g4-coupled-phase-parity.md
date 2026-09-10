# 39 — G4 coupled-phase HGES parity-collapse negative control

## Status

**G4 is rejected by A-031.** Public nonlocal coupling collapses exactly to GF(2) phase synchronization on the measured generated distribution.

This is a falsification result only. G4 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Construction

Each local gadget is a `g3-3` instance: six tetrahedra whose public dual graph is `C6`, with exactly two accepted alternating perfect-match decompositions. Those two public decompositions are canonically sorted and labeled phase `0` and phase `1`.

For gadget phase bits `x_i`, generation publishes on every edge of a connected redundant coupling graph

~~~text
b_ij = x_i XOR x_j.
~~~

The hidden reference phase vector is retained only for post-attack comparison.

Toy sets:

~~~text
g4-4   4 gadgets   K4 coupling       6 constraints
g4-8   8 gadgets   cube coupling    12 constraints
g4-12 12 gadgets   hexagonal prism  18 constraints
~~~

## Public relation

A witness chooses one accepted G3 matching for every gadget. The verifier derives the public canonical phase of each chosen matching and accepts iff every published XOR constraint is satisfied. It never asks for the hidden reference vector. Any accepted equivalent phase assignment is attacker success.

## A-031 — public GF(2) phase synchronization

A-031 uses only public data:

1. enumerate the two accepted G3 matchings for every gadget;
2. canonically map them to phase bits;
3. form the public binary linear system from the coupling constraints;
4. row-reduce it over GF(2), recording rank, nullity and row-XOR work;
5. independently propagate phases over a public spanning tree from root bit `0` and root bit `1`;
6. check all redundant cycle constraints;
7. lift both phase vectors to public local matching witnesses;
8. submit both to the exact G4 verifier;
9. compare with generation history only after public acceptance.

The attack does not use the hidden reference. Reference data is passed only to count how many accepted public solutions differ from generation history.

## Exact Python 3.12 `g4-12` result

~~~text
gadgets:                                  12
total public tetrahedra:                  72
coupling vertices / edges:                12/18
coupling cycle rank:                       7
per-gadget perfect matchings:              twelve copies of 2
total local matching nodes/backtracks:    84/0
XOR equations / variables:                18/12
GF(2) rank / nullity:                     11/1
GF(2) row XORs:                           72
propagation tree assignments:             22
propagation constraint checks:            36
recovered phase solutions:                 2
accepted public solutions:                 2
accepted non-reference solutions:          1
reference witness accepted:               yes
~~~

## Deterministic sweep

Python 3.12 tested `g4-4`, `g4-8`, and `g4-12` over eight independently derived deterministic seeds each.

| Set | Gadgets | Edges | Cycle rank | Rank/nullity | Row XORs | Local matching nodes/backtracks | Propagation assignments/checks | Accepted | Non-reference |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| g4-4 | 4 | 6 | 3 | 3/1 | 10 | 28/0 | 6/12 | 2 | 1 |
| g4-8 | 8 | 12 | 5 | 7/1 | 38 | 56/0 | 14/24 | 2 | 1 |
| g4-12 | 12 | 18 | 7 | 11/1 | 72 | 84/0 | 22/36 | 2 | 1 |

All **24/24** instances have rank `g-1`, nullity `1`, two accepted public global phase assignments, and exactly one accepted assignment different from the hidden reference.

The dedicated G4 workflow passes on Python 3.11, 3.12, and 3.13.

## Interpretation

The new nonlocal coupling is exactly public binary synchronization/cohomology. Redundant cycles add consistency checks but no secret asymmetry. On a connected graph of pairwise XOR differences, choosing one root bit fixes every other bit; the second root choice is the common global flip and is itself another accepted witness.

Therefore scaling the gadget count, increasing coupling density, or adding more redundant cycles cannot repair G4 while the relation remains pairwise XOR phase differences.

This does **not** show that general HGES is easy. It rejects this generated relation and demonstrates that nonlocality alone is not useful when it factors through an abelian binary quotient.

## G5 gate

G5 must change the constraint algebra, not merely the coupling graph. Before any positive interpretation it must face:

- quotient and abelianization tests;
- finite-domain CSP and constraint propagation;
- belief propagation / local consistency;
- low-width dynamic programming;
- exact SAT / CP-SAT;
- automorphism and normalization attacks;
- equivalent-witness enumeration;
- generated-role statistical leakage.

No trapdoor work begins from a parity-coupled relation.

No security claim.
