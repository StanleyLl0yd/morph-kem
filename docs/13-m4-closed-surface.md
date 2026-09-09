# 13 — M4 closed-surface tree-cotree experiment

## Status

M4 is a **rejected attack experiment**.

M4 removes M3's easiest shortcut. Its public targets are closed triangulated tori: genuinely 2-dimensional, every edge has exactly two incident triangles, and the tested instances have no free elementary-collapse pair. The public relation remains the M3 equivalent-witness relation.

Despite those changes, the family has a direct constructive public witness.

## Public relation

The public object is a finite 2D simplicial complex plus target critical vector (1,2,1). Any simplex-disjoint acyclic Hasse matching with that vector is accepted. No planted witness is privileged.

## A-018 — public tree-cotree witness

The attacker uses only public structure:

1. construct a spanning tree of the primal 1-skeleton;
2. match every non-root vertex with its primal-tree edge;
3. exclude those primal-tree edges;
4. build the triangle dual graph using remaining primal edges;
5. construct a dual spanning tree;
6. match each non-root triangle with its dual-tree primal edge;
7. submit the combined matching to the exact M3 validator.

For torus-4x4:

~~~text
V/E/F: 16/48/32
edge triangle incidence: 2/2
free collapse pairs: 0
critical target: (1,2,1)

primal tree edges: 15
dual tree edges: 31
critical edges: 2
tree-cotree accepted: yes

16 randomized trials:
  accepted: 16/16
  unique matchings: 16
~~~

## Fixed-seed scaling sweep

| Set | Simplices | Free pairs | Deterministic | Random | Unique |
|---|---:|---:|---:|---:|---:|
| torus-3x3 | 54 | 0 | yes | 32/32 | 32 |
| torus-4x4 | 96 | 0 | yes | 32/32 | 32 |
| torus-5x5 | 150 | 0 | yes | 32/32 | 32 |
| torus-6x6 | 216 | 0 | yes | 32/32 | 32 |
| torus-7x7 | 294 | 0 | yes | 32/32 | 32 |

These are reproducible observations for the repository's deterministic family and seeds, not a general complexity claim for arbitrary 2-complexes.

## Generic greedy comparison

For torus-4x4, four generic randomized greedy Hasse-matching trials produced zero target hits; the best total critical count was 6 versus target total 4. M4 is therefore rejected by the stronger structure-aware A-018 attack, not merely by the generic greedy baseline.

## Interpretation

**M4 is rejected as a security candidate.**

Genuine two-dimensionality and absence of free collapses are insufficient when the generated family exposes a simple label-invariant global decomposition that constructs an accepted equivalent witness.

## Consequence for M5

The next experiment should use irregular non-manifold 2-complexes rather than an easily recognizable manifold family, and should add exact/solver attacks early: generic greedy matching, bounded branch-and-bound, SAT/CSP, incidence-role distinguishers, width analysis, and equivalent-witness multiplicity.
