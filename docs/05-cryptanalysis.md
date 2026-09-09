# 05 — Cryptanalysis ledger

This file preserves attacks including successful breaks.

| ID | Attack | Assessment | Status |
|---|---|---|---|
| A-000 | Direct public coordinate recovery | **Fatal to M0** | Implemented |
| A-001 | Greedy Morse reduction/matching | Persistent risk | Implemented |
| A-002 | Shared hidden-structure recovery | Critical risk | Pending generic attack |
| A-003 | Canonical labeling/isomorphism | High risk | M1 weakness documented |
| A-004 | SAT reconstruction | High risk | Pending |
| A-005 | MILP reconstruction | High risk | Pending |
| A-006 | Treewidth/separator methods | High risk | Pending |
| A-007 | Statistical/invariant distinguisher | High risk | Pending |
| A-008 | Meet-in-the-middle path recovery | **Fatal to M1** | Implemented |
| A-009 | Learned gadget recognition | Unknown/high | Pending |
| A-010 | Invalid-ciphertext/oracle leakage | Future KEM risk | Initial tests only |
| A-011 | Generic quantum search | Baseline | Analytical only |
| A-012 | Quantum walk/structure exploitation | Unknown | Pending |
| A-013 | Bounded public collapse DFS | Effective on small M2 | Implemented |
| A-014 | 3-regular hidden-core reconstruction | **Fatal to M2** | Implemented |
| A-015 | Alternative irreducible residuals | Structural result | Observed |
| A-016 | Collapse + spanning-tree witness | **Fatal to M3** | Implemented |
| A-017 | Generic greedy acyclic Hasse matching | Strong M3 baseline | Implemented |
| A-018 | Primal/dual tree-cotree witness | **Fatal to M4** | Implemented |

## M0–M3 summary

M0 leaks coordinate-local choices directly (A-000). M1's public reversible path is vulnerable to balanced meet-in-the-middle (A-008). M2 creates real collapse branching but leaks a simpler 3-regular core reconstruction problem (A-014), while A-015 shows the planted residual is not a privileged witness. M3 fixes equivalent-witness semantics, but graph-expanded complexes are constructively easy: collapse to any graph residual and complete a spanning-tree matching (A-016).

## A-018 — primal/dual tree-cotree equivalent witness

### Target

M4 closed triangulated torus family.

### Why M4 differs from M3

Every tested M4 edge has exactly two incident triangles and every tested target has zero free collapse pairs. The M3 collapse-to-graph attack is therefore unavailable.

### Attack

A-018 builds a primal spanning tree, matches non-root vertices with its edges, then builds a spanning tree in the triangle dual graph using primal edges outside the primal tree, and matches those edges with non-root triangles.

The combined witness is checked by the exact equivalent-witness validator.

For torus-4x4:

~~~text
V/E/F: 16/48/32
free collapse pairs: 0
critical target: (1,2,1)
primal/dual tree edges: 15/31
critical edges: 2
accepted: yes
randomized: 16/16 accepted, 16 unique
~~~

Fixed-seed sweep:

| Set | Simplices | Free pairs | Deterministic | Random | Unique |
|---|---:|---:|---:|---:|---:|
| torus-3x3 | 54 | 0 | yes | 32/32 | 32 |
| torus-4x4 | 96 | 0 | yes | 32/32 | 32 |
| torus-5x5 | 150 | 0 | yes | 32/32 | 32 |
| torus-6x6 | 216 | 0 | yes | 32/32 | 32 |
| torus-7x7 | 294 | 0 | yes | 32/32 | 32 |

Generic greedy matching on the torus-4x4 baseline hit the target 0/4 times, with best total critical count 6. Thus A-018 is a stronger structure-aware break.

**Result:** M4 rejected.

**Lesson:** genuine 2D structure and absence of free collapses do not imply equivalent-witness hardness; a simple global decomposition can still construct a witness.

## Persistent fatal-flaw classes

- generated/planted distribution leakage;
- local or global decomposition;
- equivalent-witness multiplicity;
- easy recognizable homotopy/structural class;
- shared hidden structure;
- low-width or solver-friendly Hasse structure.

Every future attack record should include the exact parameter set, seeds, work metric, outcome, and interpretation.
