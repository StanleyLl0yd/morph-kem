# 39 — G4 coupled-phase HGES parity-collapse negative control

## Status

**G4 is an attack calibration in progress. No hardness or security conclusion is permitted until exact-head CI records A-031.**

G4 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Motivation

G3 removed a locally privileged planted decomposition but exposed two accepted alternating perfect-match phases. G4 asks whether coupling many such locally ambiguous gadgets creates a genuinely harder global relation.

The calibration deliberately begins with the simplest nonlocal coupling: public pairwise XOR differences between gadget phases. The expected failure mode is public GF(2) synchronization.

## Construction

Each local gadget is a `g3-3` instance: six tetrahedra whose public dual graph is `C6`, with exactly two accepted alternating perfect-match decompositions. The two public decompositions are canonically sorted and labeled phase `0` and phase `1`.

For gadget phase bits `x_i`, generation publishes on every edge of a connected redundant coupling graph

~~~text
b_ij = x_i XOR x_j.
~~~

The hidden reference phase vector is not part of the public instance. It is retained only for post-attack comparison.

Toy sets:

~~~text
g4-4   4 gadgets   K4 coupling              6 constraints
g4-8   8 gadgets   cube coupling           12 constraints
g4-12 12 gadgets   hexagonal prism         18 constraints
~~~

The coupling cycle ranks are respectively `3`, `5`, and `7`.

## Public relation

A witness chooses one accepted G3 matching for every gadget. The verifier derives the public canonical phase of each chosen matching and accepts iff every published XOR constraint is satisfied.

The verifier does not ask for the planted phase vector. Any accepted global phase assignment and corresponding local decompositions are attacker success.

## A-031 — public GF(2) phase synchronization

A-031 uses only public data:

1. enumerate the two accepted G3 matchings for every gadget;
2. canonically map them to phase bits `0` and `1`;
3. build the public binary linear system from the coupling constraints;
4. independently row-reduce the system over GF(2), recording rank, nullity and row-XOR work;
5. propagate phases over the public connected coupling graph from root bit `0`;
6. repeat from root bit `1`;
7. check all redundant non-tree/cycle constraints;
8. lift each recovered phase vector to public G3 matching witnesses;
9. submit both to the exact G4 verifier;
10. compare to the hidden reference only after public success.

For a connected graph of pairwise phase differences, the analytic expectation is rank `g-1`, nullity `1`, and two solutions related by a global bit flip. That expectation is a break hypothesis, not evidence of security.

## Predicted deterministic work

For the current fixed graph ordering, the public GF(2) elimination is expected to record:

| Set | Gadgets | Coupling edges | Cycle rank | Rank/nullity | GF(2) row XORs | Local matching nodes/backtracks |
|---|---:|---:|---:|---:|---:|---:|
| g4-4 | 4 | 6 | 3 | 3/1 | 10 | 28/0 |
| g4-8 | 8 | 12 | 5 | 7/1 | 38 | 56/0 |
| g4-12 | 12 | 18 | 7 | 11/1 | 72 | 84/0 |

These values are regression predictions only until confirmed by exact-head CI.

## Rejection gate

Reject G4 if A-031 publicly recovers any accepted global witness by GF(2) synchronization. If the expected nullity-one structure is confirmed, increasing the number of gadgets or coupling edges is not a repair: pairwise XOR differences remain an abelian synchronization/cohomology relation.

## G5 gate

A successor must change the constraint algebra rather than the coupling graph size. It must immediately face quotient/abelianization tests, finite-domain CSP, belief propagation/local consistency, low-width dynamic programming, exact SAT/CP-SAT, automorphism normalization, equivalent-witness enumeration, and planted-role statistical leakage.

No security claim.
