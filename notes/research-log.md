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
independent equations = 1
row XOR operations = 7
equivalent witnesses = 64
public Gaussian-elimination witness = accepted
same as planted representative = no
elapsed = 0.000111 s
~~~

**K2.3 rejected exactly.**

The important result is algebraic, not the runtime: any larger instance with the same central-C2 fiber semantics and product/parity 3-cell coherence remains an affine GF(2) solve.

### K2.4 — topological hard-problem frontier

Systematically screened orientation, gluings, covers/lifts, homotopy classes, fundamental groups, geodesics, hyperbolic spaces, quotient spaces, non-local properties, equivalent embeddings, and hidden transformations.

The main conclusion is that geometry/topology is useful only if it changes the **computational relation**. Orientation alone collapses to cohomology/gauge; hyperbolicity/geodesics frequently help canonicalization; covers expose subgroup/monodromy/gauge structure unless a separate trapdoor recovery algorithm exists.

The most promising executable template is **BTTS — Bounded Topological Transformation Search**, interpreted as bounded path search in an equivalence groupoid/reconfiguration graph with state-dependent local moves.

Other retained frontiers:
- HGES — hidden gluing equivalence search;
- HICQF — hidden intermediate cover/quotient factorization;
- CMPS — coupled non-abelian monodromy + abelian pi2/Postnikov layer.

No one of these is yet a cryptographic primitive.

### T0 — bounded Pachner equivalence search

Implemented the first BTTS calibration using closed 3D simplicial states and exact canonical quotienting of vertex labels. Challenge moves are state-dependent `2-3` / `3-2` Pachner moves. The verifier accepts any path within the public bound.

Fixed exact-head Python 3.12 CI sweep:

~~~text
t0-4: planted 4, shortest 4, BFS 154 visited / 47 expanded,
      bidir 40/55 visited / 13 expanded

t0-6: planted 6, shortest 6, BFS 588 visited / 316 expanded,
      bidir 149/187 visited / 75 expanded

t0-8: planted 8, shortest 4, BFS 170 visited / 51 expanded,
      bidir 40/65 visited / 13 expanded
~~~

For `t0-8` the mean unique branching factor along the planted path is 20.0. Only 17 of 1,821 tested move pairs commute, so the failure is not explained by a mostly commuting Cartesian-product move system.

**T0 generator rejected by A-022.**

The generator produced a non-self-repeating eight-move planted walk but its endpoint lies only four quotient moves away. Therefore planted walk length is not a meaningful hardness parameter.

This is a generated-distribution falsification, not an asymptotic result about Pachner reconfiguration.

### T1 gate

Do not repair T0 by increasing planted path length.

A T1 calibration must sample targets from a measured/certified **shortest-distance shell** in the canonical quotient reconfiguration graph and record:

- true shortest distance;
- shell and ball size;
- number/capped count of shortest paths;
- bidirectional frontier growth;
- neighbor/state collisions;
- move-support interaction and commuting structure;
- canonicalization cost;
- public lower-bound/potential correlations.

T1 is still not a trapdoor experiment. Only if exact-distance generated endpoints show meaningful public search resistance should a later stage attempt a secret decomposition/gluing-based navigator and require the complete interface:

~~~text
(pk, td) <- TrapdoorGen(lambda)
y        <- PublicEval(pk, r)
w        <- TrapdoorRecover(td, pk, y)
Verify(pk, y, w)
~~~

Any secret advantage must survive quotienting by all equivalent representations and equivalent accepted witnesses.

### T1 — exact-distance Pachner endpoint calibration

T1 fixes T0's immediate generator defect by building exact canonical quotient BFS shells and choosing the target from `S_D` rather than from a planted walk endpoint. Target selection first maximizes slack against the public tetrahedron-count lower bound and then minimizes capped shortest-path multiplicity.

Measured Python 3.12 dedicated CI:

~~~text
t1-2: D=2, shells 1/8/31, ball 40,
      target delta/slack 0/2, shortest paths 1,
      bidir 9/4 visited, 2 expanded

t1-3: D=3, shells 1/8/31/83, ball 123,
      target delta/slack 1/2, shortest paths 1,
      bidir 9/14 visited, 5 expanded,
      BFS 119 visited / 36 expanded,
      tetrahedron A* 119 visited / 36 expanded
~~~

The `t1-3` target is genuinely at distance 3, has one measured shortest path and is deliberately poorly predicted by tetrahedron count, yet bidirectional recovery still expands only five quotient states.

**T1 rejected by A-023 on the measured generated distribution.**

This triggers the pre-declared rejection condition. Do not add depth 4 merely to inflate the work factor. The result is not a theorem that bounded Pachner reconfiguration is easy; it rejects this generated BTTS/Pachner distribution as evidence of cryptographic hardness.

Next frontier: HGES canonical-gluing recovery negative control.

### G0 — HGES canonical gluing recovery control

Implemented a tree assembly of punctured-4-simplex 3-ball pieces. Each piece has four tetrahedra with internal dual graph `K4`; hidden inter-piece face gluings become bridges in the public tetrahedron dual graph.

A-024 computes public triangle incidence, finds dual-graph bridges, removes them and returns the remaining components as an equivalent gluing witness.

Exact-head Python 3.12 baseline `g0-8`:

~~~text
public V/E/F/T = 19/59/73/32
boundary/max face incidence = 18/2
dual graph vertices/edges = 32/55
bridges = 7
component sizes = eight copies of 4
face occurrences = 128
DFS edge scans = 110
public witness accepted = yes
matches planted partition up to order = yes
~~~

The all-parameter, eight-seed sweep recovered and accepted **24/24** partitions, all matching the planted partition up to group order.

**G0 rejected as designed by A-024.**

Lesson: hiding local piece labels and gluing permutations does not help when the quotient exposes a canonical separator decomposition. G1 must structurally remove the bridge shortcut before any further HGES interpretation.
