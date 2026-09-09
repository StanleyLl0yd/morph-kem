# Research log

## 2026-09-09 — project initialization

Selected combinatorial topology and discrete Morse reductions as the initial research family.

Provisional research labels:

- HMCP — Hidden Morse Coordinate Problem
- HMRP — Hidden Morse Reduction Path Problem
- HMCR — Hidden Morse Conjugacy Recovery

The project starts with no security claim. Negative results and successful breaks are first-class outputs.

## 2026-09-09 — M0 executable relation

Implemented canonical finite simplicial complexes, deterministic toy generation, planted elementary-collapse certificates, exact forward/accept/invert functions, and exhaustive baselines.

A-000 directly recovers every M0 seed from public coordinate-local triangle recipes.

**Result:** M0 rejected.

## 2026-09-09 — M1 non-local branching path

Replaced local M0 markers with globally supported public vertex permutations.

A-008 meet-in-the-middle recovers the hidden branch path in roughly 2^(ell/2) state enumeration.

**Result:** M1 rejected.

**Lesson:** global support is not inversion asymmetry.

## 2026-09-09 — M2 collapse maze

Implemented genuine elementary expansion/collapse branching around a hidden 3-regular graph core.

A-013 bounded collapse DFS recovers the small fixed-seed core, but A-014 is stronger: zero-triangle-incidence edges plus the public 3-regular generator invariant recover the hidden core directly.

Fixed-seed A-014 nodes:

~~~text
maze-4:  13
maze-6:  59
maze-8:  520
maze-10: 51
maze-12: 441
~~~

A-015 also shows many same-sized irreducible residuals.

**Result:** M2 rejected.

**Lesson:** the generator can leak an easier reconstruction problem than the nominal reduction maze, and the planted residual is not automatically the right security witness.

## 2026-09-09 — M3 equivalent-witness Morse relation

### Relation correction

M3 removes the planted-core digest from the success relation.

The public instance contains only the 2D simplicial complex and a target critical vector.

Any simplex-disjoint acyclic Hasse matching with that critical vector is accepted.

The exact validator checks incidence, disjointness, directed-Hasse acyclicity, and critical counts.

### Generator

M3 replaces M2's 3-regular graph with a variable-degree connected graph, applies edge/triangle expansions, and relabels vertices.

The planted witness combines expansion edge/triangle pairs with a spanning-tree vertex/edge matching on the graph core.

### A-016 constructive equivalent witness

The attacker collapses public free edge/triangle pairs until any graph residual is reached, then builds a spanning-tree matching on that residual.

Fixed-seed sweep:

~~~text
morse-6:  lex yes, reverse yes, random 32/32
morse-8:  lex yes, reverse yes, random 32/32
morse-10: lex yes, reverse yes, random 32/32
morse-12: lex yes, reverse yes, random 32/32
morse-16: lex yes, reverse yes, random 32/32
~~~

Every set produced 32 distinct residuals in 32 random trials, and every residual yielded an accepted equivalent witness.

### A-017 generic greedy matching

Eight randomized greedy acyclic-Hasse trials per set hit the exact target:

~~~text
morse-6:  8/8
morse-8:  5/8
morse-10: 3/8
morse-12: 3/8
morse-16: 4/8
~~~

### Result

**M3 rejected.**

### Main lesson

Equivalent-witness semantics are the correct security discipline, but "graph + collapsible 2D decoration" has an elementary public witness construction.

The next model must have a genuinely higher-dimensional useful witness structure and must be tested against generic Hasse-matching and solver attacks before scaling.
