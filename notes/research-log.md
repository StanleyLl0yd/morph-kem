# Research log

## 2026-09-09

### M0
Canonical toy relation implemented; A-000 directly recovers coordinates. **Rejected.**

### M1
Global reversible path implemented; A-008 meet-in-the-middle recovers paths. **Rejected.**

### M2
Genuine collapse maze implemented; A-014 reconstructs the 3-regular planted core from generator invariants; A-015 shows many alternative residuals. **Rejected.**

### M3
Equivalent-witness relation formalized: any valid acyclic Hasse matching with public target vector is accepted. A-016 collapses graph-expanded instances to arbitrary graph residuals and completes a spanning-tree witness; A-017 generic greedy matching also succeeds frequently. **Rejected.**

### M4 — closed surface

M4 uses periodic triangulated tori to remove M3's free-collapse-to-graph shortcut.

For all fixed-seed tested sets, every edge has two incident triangles and free collapse pair count is zero.

A-018 constructs a public primal/dual tree-cotree Morse matching.

Baseline torus-4x4:

~~~text
V/E/F: 16/48/32
free pairs: 0
target: (1,2,1)
primal/dual tree edges: 15/31
critical edges: 2
tree-cotree accepted: yes
randomized survey: 16/16 accepted, 16 unique
generic greedy: 0/4 target hits, best total critical 6
~~~

Scaling:

~~~text
torus-3x3: accepted, random 32/32, unique 32
torus-4x4: accepted, random 32/32, unique 32
torus-5x5: accepted, random 32/32, unique 32
torus-6x6: accepted, random 32/32, unique 32
torus-7x7: accepted, random 32/32, unique 32
~~~

**M4 rejected.**

Main lesson: genuine 2D structure and absence of free collapses do not create hardness if the public family has a simple global witness decomposition.

### H0 — Hyperbolic / non-orientable side track

Opened a separate H-series for the Möbius / Escher / Lobachevsky direction.

Working label: **Hyperbolic Frustrated MORPH (HFM)**.

Literature scan immediately rules out several naive hardness stories:

- ordinary word/conjugacy problems in standard hyperbolic groups are often algorithmically efficient;
- hyperbolic tessellations and finite quotients are established mathematical machinery;
- non-orientability by itself is a simple topological invariant;
- canonical/Delaunay tiling machinery creates a direct normalization/canonicalization attack surface.

H0 therefore separates geometry, topology, transition/holonomy, and witness layers.

### H1 — signed holonomy calibration

Implemented Z2 and S3 vertex-frame/edge-transition experiments. H1-Z2 collapses through spanning-tree gauge fixing. H1-S3 fails more strongly: its transposition verifier is exactly the sign/parity quotient `S3 -> Z2`.

**H1 rejected.**

### H2-E1 — Escher gain atlas

Implemented relative-height local charts in Z/7Z. Every single edge is locally satisfiable, but global inconsistency is exactly cycle-gain/cohomology data. Exact unbalanced-cycle branching finds equivalent seam repairs cheaply.

**H2-E1 rejected.**

### H2-E2 — higher-order NAE atlas

Raised local data to pairwise-compatible signed NAE-3 charts. Exact minimum-violation CSP still finds one-chart equivalent repairs across the toy ladder; simple public signatures expose planted seam roles in several sets.

**H2-E2 rejected.**

### H2-E3 — local-function frontier

The natural all-charts hidden-state formulation was stopped before code because it maps directly to Goldreich random/local functions and planted CSP.

**Naive H2-E3 rejected before implementation.**

### H3-E0 — lifted graph atlas

Implemented a hidden finite graph cover with secret per-fiber labels. Public spanning-tree gauge normalization recovers the same cover up to one global sheet conjugation while preserving path lifting.

**H3-E0 rejected.**

### H3-E1 — composite-cover public-key frontier

Naive public-key adaptations of composite covering fail the interface: publishing common decoder structure gives it to the attacker; hiding it prevents public encoding; omitting the outer projection leaves a public cover-projection search problem with no demonstrated trapdoor recovery algorithm.

**Naive H3-E1 rejected before code.**

### H2-H / H2.1 — Klein quartic + A5

Built the exact `{3,7}` Klein-quartic triangulation with V/E/F = 24/84/56, genus 3 and A5 3-cycle synchronization. Bounded Python attacks initially stopped one violated edge short, but an exact CNF encoding with 1,440 Boolean variables and 47,545 clauses was solved by MiniSat. The decoded assignment passed the exact repository verifier.

**H2-H rejected on the fixed generated instance.**

### K0 — Klein-bottle orientation control

Exact finite Klein-bottle triangulations confirm that genuine non-orientability still leaves ordinary Z2 gauge/cohomology when the hidden data is only local orientation. Public spanning-tree normalization recovers every hidden face gauge up to one global bit.

**K0 rejected as designed.**

### K1 — non-orientable hyperbolic control

Exact `N4:{6,4}_3` has V/E/F = 6/12/4, chi = -2 and hyperbolic type `{6,4}`. The hidden orientation gauge is recovered publicly and the orientable genus-3 double cover is reconstructed from public transitions.

**K1 rejected as designed.**

### K2.0 — orientation-twisted A5

Exhaustive algebra confirms `A5 ⋊ C2 ~= S5`; all 14,400 multiplication checks and all 43,200 endpoint predicate comparisons agree with the ordinary S5 flattening.

**K2.0 rejected algebraically.**

### K2.1 — crossed-module frontier

Crossed modules/strict 2-groups are established models of homotopy 2-types. The structural decomposition exposes `pi1 ~= coker(partial)` and abelian `pi2 ~= ker(partial)` plus action/Postnikov data. Higher gauge by itself is not a trapdoor.

**Naive hidden-higher-gauge variant rejected before code.**

## 2026-09-10

### K2.2 — Q8 automorphism crossed module

Implemented genuine edge+face data for

~~~text
partial: Q8 -> Aut(Q8)
partial(q) = conjugation by q.
~~~

Exact audit:

~~~text
|Q8| = 8
|Aut(Q8)| = 24
|ker(partial)| = 2
|im(partial)| = 4
|coker(partial)| = 6
~~~

On `N4:{6,4}_3`, every public face boundary lies in the boundary image and has exactly two Q8 lifts. Therefore four faces expose 16 equivalent fake-flat witnesses. Public independent lifting needs 24 edge compositions and 32 Q8 preimage checks and returns a valid witness different from the planted one.

**K2.2 rejected.**

Lesson: face variables alone do not create higher-order coupling when verification factorizes over boundary-preimage fibers.

### M5 — irregular non-manifold equivalent Morse witness

M5 removes both the M3 graph-decoration shortcut and the M4 closed-surface structure.

Fixed baseline:

~~~text
V/E/F = 8/27/29
edge triangle incidence = 2..6
free collapse pairs = 0
critical target = (1,0,9)
~~~

Public tree/triangle greedy finds two distinct accepted target witnesses in 32 trials. More decisively, bounded exact extension reaches an accepted equivalent witness in 30 nodes on its first public spanning-tree trial.

**M5 rejected on the fixed generated baseline.**

This is a generated-distribution break, not an asymptotic theorem. More vertices or triangles are not an acceptable repair.

### K2.3 — three-dimensional kernel coherence

Moved to the boundary of a 4-simplex to test the first actual 3-cell coherence coupling of the K2.2 face lifts.

Scaffold:

~~~text
V/E/F/T = 5/10/10/5
Euler characteristic = 0
each triangular face belongs to two tetrahedra
~~~

Each public Q8 boundary fiber still has exactly two lifts. After choosing one canonical public lift, every face witness is

~~~text
h_f = (-1)^z_f h_f^0,
z_f in GF(2).
~~~

Thus the implemented tetrahedral coherence is exactly the affine system `A z = b`.

Measured Python 3.12 CI:

~~~text
equations / variables = 5 / 10
rank / nullity = 4 / 6
dependent equations = 1
row XOR operations = 7
equivalent witnesses = 64
public Gaussian-elimination witness = accepted
same as planted representative = no
elapsed = 0.000111 s
~~~

**K2.3 rejected exactly.**

The important result is algebraic, not the runtime: any larger instance with the same central-C2 fiber semantics and product/parity 3-cell coherence remains an affine GF(2) solve.

### Next research gate

Do not escalate dimension, genus, group order, or parameter size by itself.

The only higher-topological direction still worth formulating must couple a genuinely unknown `pi1`-level object to the abelian `pi2` module/Postnikov layer and, before implementation, provide a complete public-key-style interface:

~~~text
(pk, td) <- TrapdoorGen(lambda)
y        <- PublicEval(pk, r)
w        <- TrapdoorRecover(td, pk, y)
Verify(pk, y, w)
~~~

The secret must give an invariant recovery advantage on a generated positive distribution. Hidden gauge, canonical representatives, cohomology representatives, finite linear-code syndromes, and ordinary bounded-local CSPs do not qualify as a trapdoor.
