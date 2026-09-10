# 27 — M5 irregular non-manifold 2-core

## Status

M5 returns to the equivalent-Morse-witness line after the M3 graph-expanded and M4 closed-surface failures.

It is an attack-first experiment, not a KEM or security candidate.

**Disposition: rejected on the fixed generated baseline.** Public greedy search finds equivalent target witnesses, and the bounded exact extension attack finds one in only 30 search nodes.

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
~~~

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

## Measured CI result

Fixed master seed `50126490aabbccddeeff1234567890ab`, parameter set `m5-8`, Python 3.12 CI:

~~~text
V/E/F:                              8/27/29
edge triangle incidence min/max:    2/6
incidence histogram:                ((2,7),(3,10),(4,8),(5,1),(6,1))
free collapse pairs:                0
critical target:                    (1,0,9)
reference accepted:                 true

greedy trials:                      32
greedy target hits:                 2
greedy unique critical vectors:     6
greedy unique target matchings:     2
greedy best/mean total critical:    10 / 15.00

bounded exact extension:
  accepted equivalent witness:      yes
  search nodes:                     30
  public spanning-tree trials:      1
  search exhausted:                 false
~~~

The baseline therefore clears the intended structural conditions — zero free collapse pairs and strongly non-manifold edge incidence — but still exposes accepted equivalent Morse witnesses to simple public algorithms.

The bounded extension attack is especially decisive: it reaches the public critical target after only 30 nodes on its first spanning-tree trial. No planted reference information is used.

## Disposition

**M5 is rejected on the fixed generated baseline.**

This is a generated-distribution break, not an asymptotic theorem. It nevertheless falsifies the current M5 generator/relation as a cryptographic hardness candidate.

Two lessons are important:

1. removing free collapses and manifold structure does not by itself create equivalent-witness hardness;
2. selecting the public target from the best of many easy reference matchings can leave the target reachable by the same broad family of public tree-plus-extension methods.

Parameter growth is not an acceptable repair. Any M6 successor would need a fundamentally different generated relation and should be attacked with industrial SAT/CP-SAT before scaling.

## Security status

No one-wayness, average-case hardness, post-quantum, IND-CPA, IND-CCA, KEM, or production-security claim exists.
