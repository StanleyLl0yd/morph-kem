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


## H-series attacks

### H-A01 — Z2 spanning-tree / cycle-space recovery

H1-Z2 publishes a connected graph, edge bits, and a fundamental-cycle target.

Fixing one root gauge and propagating over a public spanning tree recovers an accepted equivalent witness in linear graph work. Non-tree labels are exactly the fundamental-cycle coordinates.

**Result:** H1-Z2 rejected as designed.

### H-A03 — S3 verifier factors through sign

H1-S3 accepts a candidate frame assignment when every normalized edge transition is a transposition.

In S3, the odd permutations are exactly the three transpositions. Therefore:

~~~text
normalized transition is a transposition
    iff
sign(normalized transition) = 1
~~~

and every edge constraint factors through the public homomorphism:

~~~text
S3 --sign--> Z2.
~~~

Solving the resulting Z2 graph equations recovers one parity per vertex up to a global flip. Choosing any fixed even S3 representative for parity 0 and any fixed transposition for parity 1 gives an accepted full S3 witness.

The implementation `recover_s3_via_abelianization` performs this construction.

Fixed-seed H1 sweep:

| Set | V | E | Cycle rank | Z2 recovered | S3 direct recovered | Direct edge checks | CSP nodes | CSP backtracks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| h1-8 | 8 | 12 | 5 | yes | yes | 36 | 16 | 0 |
| h1-10 | 10 | 15 | 6 | yes | yes | 45 | 18 | 0 |
| h1-12 | 12 | 18 | 7 | yes | yes | 54 | 20 | 0 |
| h1-16 | 16 | 24 | 9 | yes | yes | 72 | 24 | 0 |
| h1-20 | 20 | 30 | 11 | yes | yes | 90 | 28 | 0 |

The CSP column uses solution cap 8. It is included only as a calibration: H-A03 is strictly stronger and already gives a direct linear construction.

For the h1-12 CI baseline with CSP solution cap 64:

~~~text
V/E/cycle rank: 12/18/7
direct S3 recovery: accepted
direct edge checks: 54
CSP solutions found: 64
CSP nodes/backtracks: 104/0
CSP elapsed: ~0.017 s on the CI runner
~~~

Wall-clock time is environment-dependent and is not a complexity claim.

**Result:** H1-S3 structurally broken.

**Lesson:** choosing a non-commutative group does not help when the verifier accepts an entire fiber of a cheap quotient homomorphism.
