# 27 — M5 irregular non-manifold 2-core

## Status

M5 returns to the equivalent-Morse-witness line after the M3 graph-expanded and M4 closed-surface failures.

It is an attack-first experiment, not a KEM or security candidate.

## Generator

Deterministically from a master seed:

1. sample a dense set of triangles on a fixed vertex set;
2. repeatedly peel every triangle touching an edge of triangle-incidence below two;
3. reject unless all vertices survive and the 1-skeleton is connected;
4. reject unless every surviving edge has incidence at least two;
5. require at least one edge of incidence above two, making the complex non-manifold at that edge;
6. reject any instance with a free elementary-collapse pair;
7. apply a final deterministic vertex relabeling.

This is not generated as a graph plus collapsible decoration and is not a closed 2-manifold.

## Public relation

The public object is only:

~~~text
irregular simplicial 2-complex X
critical target vector c
~~`

A witness is any acyclic discrete-Morse matching accepted by the exact M3 validator with critical vector c.

The reference witness is selected from multiple deterministic randomized tree-plus-triangle greedy matchings. It is not privileged by the verifier.

## Attacks

### M5-A01 — public multi-start tree/triangle greedy

A public spanning tree first matches all but one vertex. Remaining edge/triangle incidence pairs are considered in deterministic pseudo-random order and are accepted only when the exact Hasse orientation remains acyclic.

The attack repeats this with independent public seeds and records target hits and witness multiplicity.

### M5-A02 — bounded exact triangle extension

For each public spanning-tree trial, the attack fixes the vertex/edge tree matching and exactly branches over edge/triangle choices needed to meet the target number of critical triangles.

Every partial addition is checked by the exact acyclic-matching validator. Search stops at a public node budget.

This is exact conditional on the selected spanning tree, not a proof of global optimality.

## Exit criteria

Reject M5 if public greedy or bounded extension search routinely constructs equivalent target witnesses.

If the baseline survives, the next attack must be an industrial SAT/CP-SAT encoding before parameter growth.

No one-wayness, average-case hardness, post-quantum, IND-CPA, IND-CCA, KEM, or production-security claim exists.
