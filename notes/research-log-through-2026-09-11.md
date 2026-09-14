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

### G1 — bridge-free clique-decomposition control

Reused the G0 punctured-4-simplex pieces but changed the hidden assembly graph from a tree to a simple cycle. This removes the exact A-024 bridge shortcut without increasing parameters.

The bridge regression behaves as intended on `g1-12`:

~~~text
A-024 dual bridges = 0
A-024 bridge-block witness accepted by G1 = no
articulation points = 0
~~~

However the pieces themselves remain canonical in the public tetrahedron dual graph. A-028 enumerates public four-vertex dual cliques, filters them through the exact allowed-piece predicate, and solves the resulting exact cover.

Exact-head Python 3.12 `g1-12` baseline:

~~~text
public V/E/F/T = 26/85/108/48
boundary/max face incidence = 24/2
dual graph vertices/edges = 48/84
two-vertex separator pairs = 264
face occurrences = 192
4-subsets tested = 194580
dual K4 candidates = 12
allowed-piece candidates = 12
exact-cover solutions/cap = 1/64
exact-cover nodes/backtracks = 13/0
public A-028 witness accepted = yes
matches planted partition up to order = yes
~~~

The all-parameter, eight-seed sweep recovered and accepted **24/24** partitions and matched the planted partition in **24/24** cases. Per-size A-028 cover search remained deterministic under public relabeling: `g1-4` used 5/0 cover nodes/backtracks, `g1-8` 9/0, and `g1-12` 13/0.

**G1 rejected by A-028.**

Lesson: removing bridges and articulation vertices does not create gluing hardness when each hidden piece remains an exact fixed-size public clique. Do not scale the cycle. G2 must change the piece/overlap structure so the intended pieces are not directly the canonical `K4` blocks, and must still face separator, motif, local-role, automorphism, exact-cover/SAT/CP-SAT, equivalent-witness, and planted-role leakage attacks.

### G2 — stellar-subdivision contraction control

Every G1 macro tetrahedron was stellar-subdivided `1 -> 4`, turning each four-macro-tetrahedron piece into a sixteen-micro-tetrahedron public piece. The old A-028 regression no longer directly returns an accepted piece-level witness: on `g2-4` it finds 16 small `K4`/allowed center stars, but G2 requires four 16-tetrahedron piece groups.

A-029 uses those public local stars against the construction. It identifies candidate stellar centers from vertex incidence, exact-covers the micro tetrahedra by center stars, contracts them back to the G1 macro complex, applies macro A-028, then lifts the recovered partition and checks the exact G2 verifier.

Exact-head Python 3.12 `g2-8` baseline:

~~~text
public micro V/E/F/T = 50/185/264/128
micro dual edges = 248
bridges / articulation points = 0 / 0
two-vertex separator pairs = 112
candidate stellar centers = 32
candidate-center false positives/misses = 0/0
center exact-cover solutions/cap = 1/64
center cover nodes/backtracks = 33/0
reconstructed macro tetrahedra = 32
contracted macro V/E/F/T = 18/57/72/32
macro K4 / allowed candidates = 8/8
macro cover nodes/backtracks = 9/0
A-029 public witness accepted = yes
matches planted partition up to order = yes
~~~

The all-size eight-seed sweep recovered and accepted **24/24** G2 witnesses, matched the planted piece partition in **24/24** cases, and produced zero candidate-center false positives or misses. Center exact-cover and macro exact-cover search had zero backtracking on every measured set.

**G2 rejected by A-029.**

Lesson: subdivision/refinement is not hiding when the generated representation has a public local inverse that restores an already-fatal macro decomposition. Do not scale or repeat the stellar subdivision. G3 must eliminate both canonical small piece motifs and obvious public contraction/simplification paths, while still facing separator, multiscale motif, local-link, automorphism, exact-cover/SAT/CP-SAT, equivalent-witness, and planted-role leakage attacks.

### G3 — indistinguishable-edge equivalent-matching control

Changed the piece family to a two-tetrahedron 3-ball and arranged the public tetrahedron dual graph as the even cycle `C_(2n)`. Every planted internal edge and every planted external gluing edge satisfies the same public allowed-piece predicate, so the planted matching phase is no longer locally canonical.

This does not create hardness. A-030 enumerates exact perfect matchings from the public allowed dual edges and submits them to the exact verifier. The first label-order DFS found the right solutions but had relabel-dependent dead ends; the final MRV attack removes that artifact.

Exact-head Python 3.12 `g3-8` baseline:

~~~text
public V/E/F/T = 18/49/48/16
boundary/max face incidence = 32/2
dual vertices/edges = 16/16
dual degree histogram = ((2,16),)
bridges / articulation points = 0/0
allowed candidate dual edges = 16
vertex-star candidate pairs = 16
vertex tetrahedron-degree histogram = ((2,16),(16,2))
face occurrences = 64
perfect matchings/cap = 2/16
matching nodes/backtracks = 17/0
accepted decompositions = 2
accepted non-planted decompositions = 1
reference witness accepted = yes
~~~

Across `g3-3`, `g3-5`, and `g3-8` with eight deterministic public relabel seeds each, all **24/24** instances have zero bridges/articulation points, every dual edge is a valid candidate piece, and A-030 finds exactly two accepted perfect-match decompositions. In every instance exactly one accepted decomposition differs from the planted partition. MRV matching work is relabel-stable: 7/0, 11/0, and 17/0 nodes/backtracks for `g3-3`, `g3-5`, and `g3-8` respectively.

**G3 rejected by A-030.**

Lesson: making local interfaces indistinguishable can make the attacker relation easier under equivalent-witness semantics. The hidden planted phase is irrelevant when the other alternating perfect matching is also accepted. Do not scale the even cycle. G4 must add genuinely nonlocal coupling and attack that coupling first as parity/cohomology/gauge, constrained matching, low-width DP/CSP, exact-cover/SAT/CP-SAT, automorphism/normalization, equivalent-witness, and planted-role leakage structure.

### G4 — coupled-phase parity-collapse control

Coupled many locally ambiguous `g3-3` gadgets with public pairwise phase differences on redundant connected graphs. Each local gadget still has exactly two accepted matching phases; generation reference phases are not used by the attack.

A-031 independently performs spanning-tree XOR propagation and full GF(2) row reduction. Exact-head Python 3.12 `g4-12` gives 12 gadgets / 72 tetrahedra, 18 coupling constraints, cycle rank 7, rank/nullity 11/1, 72 row XORs, 84/0 local matching nodes/backtracks, and two accepted global phase solutions, one non-reference.

Across `g4-4`, `g4-8`, `g4-12` × eight seeds, **24/24** instances have rank `g-1`, nullity 1, two accepted solutions and one non-reference solution.

**G4 rejected by A-031.**

Lesson: adding nonlocal coupling does not create hardness when the coupling factors exactly through public XOR differences. G5 must change the constraint algebra and immediately face quotient/abelianization, bounded-domain CSP, local consistency/belief propagation, low-width DP, SAT/CP-SAT, normalization and equivalent-witness attacks.

### G5 — nonlinear exact-one parity-projection control

Replaced explicit pairwise XOR coupling with signed ternary exact-one clauses over the same public two-phase G3 gadgets. Pre-code attack screening found that every accepted exact-one clause implies one affine GF(2) parity equation.

The chosen regular templates have degree six and connected factor graphs but full GF(2) rank. Exact-head Python 3.12 `g5-24` gives 24 gadgets / 144 tetrahedra, 48 clauses, factor cycle rank 73, rank/nullity 24/0, 436 row XORs, 168/0 local matching nodes/backtracks, and one affine solution. That public solution passes all 48 original nonlinear clause checks and equals the hidden reference only in post-attack comparison.

Across `g5-12`, `g5-18`, `g5-24` × eight seeds, **24/24** public affine recoveries are accepted and **24/24** match the reference.

**G5 rejected by A-032.**

Lesson: changing the visible verifier from XOR to a nonlinear predicate is cosmetic when the predicate leaks a full-rank affine quotient that uniquely determines the satisfying witness. G6 must require that cheap quotient information leave genuine residual ambiguity and then attack that residual with CSP/SAT and structural methods.

### G6 — affine-coset residual control

Kept the nonlinear G5 exact-one verifier but changed the circulant clause scopes so the public parity projection has rank `g-2` and nullity `2`. Thus the attacker no longer obtains the witness directly from GF(2); it obtains a four-element affine coset.

A-033 enumerates that entire public coset and evaluates all nonlinear clauses for every candidate before exact-verifier confirmation. Exact-head Python 3.12 `g6-24` gives rank/nullity `22/2`, 308 row XORs, four affine candidates, 192 residual clause checks, one accepted candidate and 48 final verifier checks.

Across `g6-12`, `g6-18`, `g6-24` × eight seeds, **24/24** instances expose exactly four affine candidates and exactly one nonlinear-valid public witness; all accepted witnesses match the hidden reference only in post-attack comparison.

**G6 rejected by A-033.**

Lesson: making the affine quotient incomplete is necessary but not sufficient. A constant two-bit residual is still trivial. G7 must make cheap-quotient residual dimension grow with the instance and attack that growing residual with exact CSP/SAT and structural methods.

## 2026-09-10 — G7 rejected by A-034

Implemented G7 planted signed 3-SAT phase coupling as the first G-series predicate with zero non-trivial local affine GF(2) implications. Public deterministic DPLL nevertheless recovers accepted witnesses cheaply. Fixed Python 3.12 `g7-24`: 24 gadgets, 96 clauses, degree 12, factor cycle rank 169, 40 DPLL nodes / 22 decisions / 34 propagations / 2 conflicts / 2 backtracks, 16/16 capped accepted solutions, all 16 non-reference. The 24-instance all-size/eight-seed sweep succeeds on every instance with a measured maximum of 86 DPLL nodes and at least one non-reference accepted witness each. Independent MiniSat finds SAT with 3 conflicts / 13 decisions / 41 propagations and its decoded model passes the exact verifier.

Conclusion: G7 rejected. Eliminating the parity quotient alone does not make this planted distribution cryptographically hard; equivalent-witness multiplicity remains fatal. G8 must change the generated relation rather than scale G7. No security claim.

## 2026-09-10 — G8 confirms topology-to-CSP collapse via A-035

Implemented a generic public compiler for the G4–G7 HGES architecture. Each local G3 gadget's two accepted decompositions are enumerated/canonically ordered publicly; global constraints are compiled to finite relation tables with no simplicial identifiers; a generic GAC/MRV solver operates only on the compiled CSP; assignments are lifted afterward and checked by the original exact HGES verifier.

Exact Python 3.12 semantic audit: G4 `16/16`, G5 `4096/4096`, G6 `4096/4096`, G7 `4096/4096` phase assignments checked, **0 mismatches** in every family (12,304 total). Fixed large-family solver work is G4 `3/1`, G5 `3/1`, G6 `3/1`, G7 `38/22` nodes/decisions; all recovered assignments lift successfully, with G7 exposing 16/16 non-reference solutions in its capped batch. Four-seed/four-family sweep succeeds 16/16; G7 max generic work is 100 nodes / 53 decisions.

Conclusion: A-035 is a structural break of the G4–G7 design line. A harder global CSP predicate over the same independently enumerable local phase domains would be cosmetic with respect to topology. G9 must make public phase/domain extraction itself nontrivial by entangling local topology across boundaries, then attack that extraction aggressively. No security claim.

## 2026-09-10 — G9 rejected by A-036

G9 removed the G4–G8 independent local phase-domain architecture by publishing one connected tetrahedron-cycle complex with overlapping D2/D3 candidate carriers. Every tetrahedron belongs to five public candidates.

A-036 enumerates those candidates and solves exact cover; an independent cycle-composition DP derives the same witness family from the public dual cycle. Fixed Python 3.12 `g9-30`: 30 tetrahedra / 11 pieces, 30 D2 + 30 D3 candidates, exact-cover 450 solutions in 2820 nodes / 899 backtracks, cycle DP 36 states / 70 transition checks / 450 tilings, all 450 accepted and 449 non-reference.

Across `g9-18`, `g9-24`, `g9-30` × eight seeds, **24/24** instances produce exact agreement between exact cover and cycle DP: respectively 90, 224 and 450 accepted tilings, with all but the planted reference available as equivalent attacker witnesses.

**G9 rejected by A-036.** Lesson: breaking independent phase extraction is necessary but not sufficient. If public candidate carriers form a low-width interval/cycle overlap relation, decomposition remains a cheap exact-cover/DP problem and equivalent-witness multiplicity becomes even worse. G10 must change the overlap interaction graph and measure separator/treewidth structure before any solver growth is interpreted. No security claim.

## 2026-09-10 — G10 rejected by A-037

G10 moved the overlap interaction from G9's one-dimensional cycle to the closed periodic torus triangulation. The public triangle-dual graph is connected, 3-regular and bipartite with zero bridges/articulation points, so G9's cycle-DP shortcut is genuinely gone.

A-037 nevertheless reduces the exact public witness relation to ordinary bipartite perfect matching. Fixed Python 3.12 `g10-8x8`: 64/192/128 public V/E/F, dual 128/192, bipartition 64/64, base matching 64 augmentations / 455 DFS calls / 770 edge scans. Forced-edge re-solving reaches the 64-solution cap using 49,473 additional edge scans; all 64 returned witnesses verify and 63 are non-reference.

Across `g10-4x4`, `g10-6x6`, `g10-8x8` × eight seeds, **24/24** base public matchings verify and every instance yields a non-reference witness. All eight `g10-8x8` runs hit the 64-solution cap.

**G10 rejected by A-037.** Lesson: increasing geometric dimension/overlap width is irrelevant when the witness relation still collapses to a known polynomial graph problem. G11 must use pieces of size greater than two so candidate selection becomes genuinely hypergraphic, then attack exact cover/set packing, toroidal special structure, low-width methods and SAT/CP-SAT before any positive interpretation. No security claim.

## 2026-09-10 — G11 rejected by A-038

G11 replaced G10's adjacent-pair pieces by three-triangle `P3` disks on the periodic torus. This makes the public decomposition relation genuinely 3-uniform hypergraph exact cover: `g11-6x9` exposes 324 candidates over 108 triangles, each triangle belongs to 9 candidates, and every candidate overlaps 18 others.

A-038 still breaks the generated family cheaply. Fixed Python 3.12 `g11-6x9` reaches 64/64 capped exact covers in 292 nodes / 71 decisions / 10 backtracks; all 64 returned witnesses are non-reference. Across all three sizes × eight seeds, **24/24** runs reach cap 32 and every returned witness is accepted and non-reference.

Independent MiniSat cross-check on the same largest candidate hypergraph uses 324 variables / 3996 clauses and returns SAT with 2 conflicts, 137 decisions and 574 propagations. Its decoded 36-piece cover passes the exact verifier and differs from reference.

**G11 rejected by A-038.** Lesson: leaving graph matching for generic hypergraph exact cover is not enough when the public generated carrier is highly regular and exposes a dense family of equivalent local covers. G12 must break the periodic/repeated-role carrier structure before any solver growth is interpreted. No security claim.

## 2026-09-11 — G12 rejected by A-039

G12 tested whether G11 failed only because of periodic torus symmetry. The carrier is first irregularized by 36/54/72 deterministic legal edge flips and only then conditioned on existence of a public P3 exact cover. All 24 measured instances required zero generation retries.

The irregularity gate is real: fixed `g12-8x9` has nine primal vertex-degree classes, a non-bipartite 3-regular dual, 82 combined local signature classes, nonuniform P3 candidate memberships, and 59 legal public flips that move the degree profile toward the regular torus.

A-039 still breaks the relation cheaply. Fixed `g12-8x9`: 408 candidates, exact cover 64/64 accepted non-reference solutions in 456 nodes / 119 decisions / 119 backtracks. MiniSat on 408 variables / 4824 clauses returns an accepted non-reference witness with 105 conflicts / 807 decisions / 4699 propagations. Across all three sizes × eight seeds, **24/24** runs hit the 32-solution cap and every returned cover is non-reference; max exact-cover work is 761 nodes.

**G12 rejected by A-039.** Lesson: local edge-flip irregularization is cosmetic with respect to this candidate-extraction relation. G13 must abandon the periodic-torus/local-flip carrier family rather than add more disorder. No security claim.

## 2026-09-11 — G13 rejected by A-040 at generator gate

G13 tried to leave torus ancestry entirely by sampling random simple cubic triangle-dual pairings and gluing oriented triangle sides. Before adding any witness relation, A-040 audited whether this raw random-map distribution yields honest simplicial closed surfaces without severe rejection conditioning.

Fixed Python 3.12 audit: 4096 attempts at each of 36/54/72 triangles give zero successes. Eight additional 1024-attempt seeds per size also give zero successes in all 24/24 batches. Aggregated per size: 12,288 attempts, zero valid carriers, elementary `3/N = 0.000244141`.

All samples that survive dual loops/parallel edges already fail by collapsing at least one quotient triangle to fewer than three distinct vertices. No sample reaches the later simplicial edge/link/genus gates.

**G13 rejected by A-040 before P3 cryptanalysis.** An unbounded rejection sampler would hide a severe generated-distribution conditioning problem. G14 must use a constructive non-toroidal simplicial family, beginning with a random stacked/Apollonian sphere and immediate public reverse-subdivision plus exact-cover/SAT attacks. No security claim.

## 2026-09-11 — G14 rejected by A-041

G14 replaced G13's unhealthy random-map sampler with guaranteed-valid random stacked/Apollonian 2-spheres. The carrier is globally relabelled, but public degree-three stellar centers remain a complete inverse.

Fixed Python 3.12 `g14-72`: 38/108/72 public V/E/F, chi 2, degree histogram `((3,15),(4,8),(5,2),(6,4),(7,2),(8,1),(10,2),(12,2),(15,1),(24,1))`. A-041 performs exactly 34 reverse-stacking moves and reaches 4/6/4, chi 2. Up to 15 reverse candidates coexist on the baseline.

Across `g14-36`, `g14-54`, `g14-72` x eight seeds, **24/24** instances normalize completely in exactly 16/25/34 moves. Maximum simultaneous candidates are 8/12/17.

**G14 rejected by A-041.** Generator validity by construction is not useful when the construction has a public bounded-local inverse. P3/SAT is not run after the cheaper structural break. No security claim.

## 2026-09-11 — G15 rejected by A-042

G15 starts from a non-stacked icosahedral sphere, grows it to 36/54/72 triangles, then performs 720/1080/1440 successful legal edge flips. This largely defeats the G14 complete reverse-stacking failure: fixed `g15-72` stalls after 20 reverse moves at 18/48/32 rather than reaching the tetrahedron. All 24 official sweep instances likewise stall before the tetrahedron.

The witness relation nevertheless remains fatal. Fixed `g15-72` exposes 186 public P3 candidates; exact cover reaches 64/64 solutions in 467 nodes / 148 decisions / 188 backtracks, all accepted and non-reference. Across all three sizes x eight seeds, **24/24** runs hit cap 32 and every returned witness is non-reference; maximum nodes are 202/260/427. MiniSat solves the fixed 186-variable / 2034-clause instance in about 0.004 s and returns an accepted non-reference cover.

One auxiliary direct-byte seed still fully reverse-stacks after mixing, so no universal defeat of A-041 is claimed.

**G15 rejected by A-042.** This separates carrier hardness from witness hardness: changing the carrier is no longer a justified next move while P3 validity remains a fixed-radius public motif. G16 must change the witness predicate and immediately face topology-to-CSP, SAT/CP-SAT, low-width, normalization and equivalent-witness attacks. No security claim.

## 2026-09-11 — G16 rejected by A-043

G16 changed the witness predicate itself: the verifier accepts a simple primal cycle with odd pairing against a public nontrivial GF(2) cocycle on an irregular torus. This is genuinely global and no local P3 dictionary is involved.

Attack-first analysis improved the planned affine solve to a cheaper theorem-driven attack: fundamental cycles of any public spanning tree form the cycle-space basis, so a non-coboundary cocycle must pair oddly with at least one of them. Fixed `g16-8x9` needs only 4 cycle tests / 24 tree-path edge scans to find an accepted 9-edge non-reference cycle. The independent affine cross-check also produces an accepted simple odd cycle.

Across `g16-6x6`, `g16-6x9`, `g16-8x9` × eight seeds, both paths succeed **24/24**, and all primary recovered witnesses differ from the hidden reference. Measured `H^1` dimension is exactly two throughout.

**G16 rejected by A-043.** Lesson: nonlocal topology does not create hardness when the accepted relation remains affine on a public chain/cycle space. G17 must introduce a genuinely nonlinear relation among multiple global cycles and attack it immediately with symplectic bases, flow/matching, ILP/SAT/CP-SAT and equivalent-witness search. No security claim.

## 2026-09-11 — G17 rejected by A-044

G17 moved beyond G16's single affine cohomology predicate to a bilinear relation between two independently global simple cycles: one primal, one dual, with odd crossing parity.

Attack-first analysis found a stronger break than generic bilinear solving. A public tree-cotree decomposition leaves exactly two edges on every measured torus. The fundamental primal and dual cycles generated by either leftover edge cross exactly once by construction. Fixed `g17-8x9` needs only 9 primal-tree and 23 dual-tree path scans to produce accepted 10/24-edge cycles.

The independent full-cycle-basis crossing matrix is 145×73 on the fixed baseline, has weight 550 and GF(2) rank exactly two. Across all three sizes × eight seeds, **24/24** primary exact-one-crossing pairs and **24/24** full-basis cross-check pairs pass the exact verifier; all primary witnesses differ from the reference.

**G17 rejected by A-044.** Lesson: bilinear homological intersection is still publicly constructive on an explicitly embedded surface. G18 must impose geometry not fixed by the homology intersection form and face flow/matching/disjoint-path and generic solver attacks immediately. No security claim.

## 2026-09-11 — G18 rejected by A-045

G18 added genuine geometric constraints to the G17 global cycle-pair verifier: exact crossing count one plus public primal/dual length bounds derived from a separate hidden tree-cotree reference. Fixed `g18-8x9` bounds are 11/20. The old canonical G17 tree-cotree pair is 9/21 and therefore fails the new dual bound.

A-045 nevertheless recovers a public 6/15 pair with exactly one crossing. It searches a two-sheet cocycle parity cover (72 roots, 9913 queue pops, 59311 edge scans), then needs only six constrained-dual connector attempts / 2406 dual edge scans. The recovered pair passes the exact verifier and differs from the reference.

Across `g18-6x6`, `g18-6x9`, `g18-8x9` × eight seeds, **24/24** public attacks succeed within the generation-derived bounds and **24/24** selected pairs are non-reference. The older canonical tree-cotree pair fits the bounds only 0/8, 2/8 and 2/8 times, so A-045 is a distinct stronger break rather than a restatement of A-044.

**G18 rejected by A-045.** Length-bounded geometric topology still reduces to cheap public shortest-path constructions on this distribution. G19 must couple multiple representatives so one shortest noncontractible cycle plus one connector is insufficient. No security claim.

## 2026-09-11 — G19 rejected by A-046

G19 strengthened G18 by requiring two vertex-disjoint simple primal cycles, both odd against the same public nontrivial cocycle and both inside generation-derived sorted length bounds. Reference generation is independent and explicit; no measured carrier required a generation retry.

A-046 breaks the measured family by repeated public parity-cover recovery. Find one short odd cycle, delete all its vertices and incident edges, then run the same odd-cycle recovery on the remaining graph. Fixed `g19-8x9` uses public bounds `8/9` but returns a `5/6` accepted non-reference pair after one first candidate and one second-stage call; the second stage scans 43,580 edges.

Across all three sizes × eight seeds, **24/24** primary attacks recover accepted bounded pairs with cocycle pairings `1/1`, zero shared vertices and non-reference identity. Maximum selected lengths are `4/6`, `6/6`, `6/7`; maximum second-stage scans are `9450`, `23146`, `43485`.

The independent canonical fundamental-cycle pair scan succeeds only 4/24 times. This weaker result is preserved separately and does not weaken the primary break.

**G19 rejected by A-046.** G20 must prevent repeated recovery of parallel representatives on a single torus handle, likely by moving to multiple independent homology directions and a prescribed multicurve relation. No security claim.

## 2026-09-11 — G20 rejected by A-047

G20 moved from one torus handle to a flip-mixed genus-two connected sum with measured `H^1(F2)=4`. The verifier requires vertex-disjoint simple cycles of two distinct public signatures `(1,0)` and `(0,1)` under independent generation-derived length bounds.

A-047 still wins publicly: four-sheet parity-cover recovery finds an alpha-class cycle, deletes its vertices, then finds the beta-class cycle in the remaining graph. Fixed `g20-6x9` recovers an accepted non-reference `4/3` pair inside `6/4` bounds after one beta-stage call. Across three sizes x eight seeds, **24/24** primary attacks verify, all have zero shared vertices and exact signatures, and **23/24** are non-reference.

No articulation or two-vertex separator appears in the measured sweep; separating triangles are variable and the primary attack does not depend on them. The independent canonical fundamental-cycle pair scan succeeds on only 5/24, so it is recorded as an incomplete cross-check rather than part of the rejection argument.

**G20 rejected by A-047.** Genus and distinct public classes are not sufficient while the relation decomposes into finite-state class recovery plus deletion. G21 must couple several cycles simultaneously through a prescribed intersection/disjointness pattern. No security claim.

## 2026-09-11 — G21 rejected by A-048

G21 removed G20's sequential verifier structure and required eight global cycles simultaneously: four primal and four dual, with exact geometric crossing matrix `I4`.

A-048 constructs the whole family publicly in one tree-cotree decomposition. Fixed `g21-6x9`: four leftovers, 25/63 primal/dual path scans, primal lengths `7/7/9/6`, dual lengths `6/31/10/20`, exact identity matrix, exact-verifier accepted. The independent `217x108` full crossing matrix has GF(2) rank four.

Across three sizes x eight seeds, **24/24** instances expose exactly four leftovers, exact `I4`, zero off-diagonal crossings and accepted witnesses; full-basis rank is four throughout.

**G21 rejected by A-048.** Simultaneous primal-dual coupling alone is not enough when public tree-cotree topology mechanically supplies the complete symplectic-style family. G22 must add same-side geometric coupling such as vertex-disjointness/intersection/avoidance or bounds that tree-cotree does not automatically satisfy. No security claim.
