# 05 — Cryptanalysis ledger

This file is the canonical attack index for MORPH-KEM. Successful breaks are research results and remain part of the record.

Detailed attack records through A-024 are preserved verbatim in `docs/05-cryptanalysis-through-a024.md`. The compact index below is authoritative for attack IDs and current dispositions; new measured attacks are recorded here and in the chronological research log.

| ID | Attack | Assessment | Status |
|---|---|---|---|
| A-000 | Direct public coordinate recovery | **Fatal to M0** | Implemented |
| A-001 | Greedy Morse reduction/matching | Persistent risk | Implemented |
| A-002 | Shared hidden-structure recovery | Critical risk | Pending generic attack |
| A-003 | Canonical labeling/isomorphism | High risk | M1 weakness documented |
| A-004 | Exact SAT/CNF reconstruction | **Fatal to H2-H fixed generated instance** | Implemented (MiniSat) |
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
| A-019 | Tree-plus-extension equivalent Morse witness | **Fatal to M5 fixed generated baseline** | Implemented |
| A-020 | Independent Q8 boundary-fiber lifting | **Fatal to K2.2** | Implemented |
| A-021 | GF(2) kernel-coherence elimination | **Fatal to K2.3 relation family** | Implemented |
| A-022 | Short equivalent Pachner path + bidirectional recovery | **Fatal to T0 generator** | Implemented |
| A-023 | Exact-distance bidirectional Pachner recovery | **Fatal to T1 generated distribution** | Implemented |
| A-024 | Dual-graph canonical gluing recovery | **Fatal to G0 by design** | Implemented |
| A-028 | Public K4 / allowed-piece exact-cover recovery | **Fatal to G1 generated distribution** | Implemented |
| A-029 | Public stellar-center contraction + macro recovery | **Fatal to G2 generated distribution** | Implemented |
| A-030 | Equivalent perfect-matching gluing recovery | **Fatal to G3 generated distribution** | Implemented |
| A-031 | Public GF(2) coupled-phase synchronization | **Fatal to G4 generated distribution** | Implemented |
| A-032 | Public exact-one parity projection | **Fatal to G5 generated distribution** | Implemented |
| A-033 | Affine-coset residual exact-one enumeration | **Fatal to G6 generated distribution** | Implemented |
| A-034 | Public planted 3-SAT DPLL + independent MiniSat recovery | **Fatal to G7 generated distribution** | Implemented |

A-025 through A-027 are reserved cross-cutting frontier attacks, not yet implemented ledger entries: cover/subgroup/monodromy factorization, normal-form/geodesic/mapping-class canonicalization, and group-action/hidden-shift quantum reduction. Their definitions are maintained in `docs/29-k2-topological-hard-problem-frontier.md`.

## Persistent fatal-flaw classes

- generated/planted distribution leakage;
- local or global canonical decomposition;
- equivalent-witness multiplicity;
- easy recognizable homotopy/structural class;
- shared hidden structure;
- low-width or solver-friendly constraint structure;
- public quotient/gauge normalization;
- fixed-size local motifs that reveal hidden pieces;
- cosmetic representation layers with a public local inverse.

Every attack record must distinguish measured evidence from asymptotic claims and should include exact parameter sets, seeds, work metrics, verifier outcome, and interpretation.

## Prior detailed ledger

The detailed records for A-000 through A-024, including H-series/K-series auxiliary attack labels and exact historical measurements, are preserved without modification in:

- `docs/05-cryptanalysis-through-a024.md`

This archival split is bookkeeping only. It does not retire, weaken, supersede, or hide any earlier attack. All previous negative results remain applicable.

## A-028 — public K4 / allowed-piece exact-cover recovery

### Target

G1 bridge-free HGES clique-decomposition negative control.

G1 modifies G0 in exactly one structural way: the allowed punctured-4-simplex pieces are assembled in a simple cycle rather than a tree. This removes every inter-piece dual-graph bridge. The full public tetrahedron dual graph also has no articulation vertices.

That regression succeeds, but it does not create a hard gluing relation. Each hidden piece still consists of four tetrahedra whose public tetrahedron-dual induced subgraph is exactly `K4`.

### Public attack

A-028 uses only the public quotient tetrahedra and the public allowed-piece relation:

1. enumerate public triangular-face incidence;
2. build the tetrahedron dual graph;
3. enumerate all four-tetrahedron subsets;
4. retain subsets whose four dual vertices form a clique;
5. apply the exact allowed-piece predicate to each clique;
6. solve the induced exact-cover relation over all public tetrahedra;
7. submit any cover whose groups satisfy the public G1 cycle verifier;
8. compare with planted generation history only after public success is established.

The current implementation deliberately uses exhaustive fixed-size subset enumeration. With candidate size fixed at four, this calibration is polynomial fourth-degree work in the tetrahedron count; no optimized clique enumeration is needed to reject the family.

### Exact Python 3.12 `g1-12` result

~~~text
pieces:                                  12
public V/E/F/T:                          26/85/108/48
Euler characteristic:                   1
boundary faces / max face incidence:    24/2
dual graph vertices / edges:            48/84
A-024 dual bridges:                      0
A-024 bridge-block witness accepted:    no
articulation points:                     0
two-vertex separator pairs:              264
face occurrences:                        192
4-subsets tested:                        194580
dual K4 candidates:                      12
allowed-piece candidates:                12
exact-cover solutions / cap:             1/64
exact-cover cap hit:                     no
exact-cover nodes / backtracks:          13/0
A-028 public witness accepted:            yes
matches planted partition up to order:   yes
~~~

Python 3.12 tested `g1-4`, `g1-8`, and `g1-12` over eight independently derived public relabel seeds each. All **24/24** public A-028 recoveries are accepted and all **24/24** match the planted partition up to group order.

**Result: G1 rejected by A-028.** The break is structural for the current generated family. Removing bridges and articulation vertices removes one decomposition route but leaves each piece as a public fixed-size clique. Do not increase the G1 cycle size as a repair.

## A-029 — public stellar-center contraction + macro recovery

### Target

G2 stellar-subdivision HGES negative control.

G2 applies a `1 -> 4` stellar subdivision independently to every G1 macro tetrahedron. One G1 four-tetrahedron piece therefore becomes a sixteen-micro-tetrahedron G2 piece. This defeats the literal piece-level interpretation of A-028 but preserves a recognizable local inverse.

### Public attack

A-029 uses only public incidence:

1. enumerate each public vertex star;
2. retain vertices whose four incident tetrahedra have link equal to the boundary of one tetrahedron;
3. exact-cover all public micro tetrahedra by these candidate center stars;
4. contract the selected stars to public macro tetrahedra;
5. run A-028 on the contracted macro complex;
6. lift the recovered macro partition back to micro tetrahedra;
7. submit the lifted partition to the exact G2 verifier;
8. compare to planted center/piece roles only after public success.

On this distribution, the public vertex-star signature is already exact: the valid four-tetrahedron center stars are precisely the planted subdivision centers on every measured seed.

### Exact Python 3.12 `g2-8` result

~~~text
pieces:                                  8
public micro V/E/F/T:                    50/185/264/128
Euler characteristic:                   1
boundary faces / max face incidence:    16/2
micro dual vertices / edges:             128/248
micro dual bridges:                       0
micro articulation points:                0
micro two-vertex separator pairs:        112
micro face occurrences:                  512
vertex-star histogram:                   4:32 / 12:8 / 18:8 / 72:2
candidate stellar centers:                32
candidate-center false positives/misses:   0/0
center exact-cover solutions / cap:        1/64
center exact-cover nodes / backtracks:    33/0
reconstructed macro tetrahedra:           32
contracted macro V/E/F/T:                18/57/72/32
contracted macro dual edges:              56
macro K4 / allowed candidates:             8/8
macro exact-cover solutions:                1
macro exact-cover nodes / backtracks:       9/0
A-029 public witness accepted:             yes
matches planted partition up to order:    yes
~~~

The old A-028 granularity regression on `g2-4` finds 16 micro `K4` / allowed four-tetrahedron center stars but no accepted G2 piece-level witness. Those motifs are nevertheless enough for A-029 to contract the representation.

### Deterministic sweep

Python 3.12 tested `g2-4`, `g2-6`, and `g2-8` over eight independently derived deterministic seeds each.

| Set | Micro dual edges | Bridges / articulations | 2-vertex separators | Centers | False/missed | Center cover nodes/backtracks | Macro K4/allowed | Macro cover nodes/backtracks | Accepted/matched |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| g2-4 | 124 | 0 / 0 | 24 | 16 | 0 / 0 | 17 / 0 | 4 / 4 | 5 / 0 | 8/8 |
| g2-6 | 186 | 0 / 0 | 60 | 24 | 0 / 0 | 25 / 0 | 6 / 6 | 7 / 0 | 8/8 |
| g2-8 | 248 | 0 / 0 | 112 | 32 | 0 / 0 | 33 / 0 | 8 / 8 | 9 / 0 | 8/8 |

All **24/24** public A-029 recoveries are accepted and all **24/24** match the planted piece partition up to group order. Exact planted recovery is stronger than required under equivalent-witness semantics.

### Result

**G2 is rejected by A-029.**

The stellar subdivision is a cosmetic representation layer for this family. It destroys the old piece-level four-tetrahedron presentation but introduces publicly recognizable stellar-center stars. Contracting them reconstructs the exact G1 macro relation, where A-028 remains fatal.

Do not repair G2 with more pieces, repeated stellar subdivisions, or deeper local refinement. Those changes preserve a public simplification/contraction path unless the next construction changes the relation itself.

This is not a theorem that general HGES is easy. It is a falsification of the current generated distribution.

## A-030 — equivalent perfect-matching gluing recovery

### Target

G3 indistinguishable-edge HGES matching control.

G3 changes the piece family to a two-tetrahedron 3-ball and arranges `n` pieces so the public tetrahedron dual graph is exactly the even cycle `C_(2n)`. Every dual edge—planted internal or planted external—passes the same exact allowed-piece predicate. Thus the planted alternating phase is not locally distinguished.

### Public attack

A-030 uses only public incidence:

1. build triangle incidence and the tetrahedron dual graph;
2. retain every dual edge whose two tetrahedra form the allowed five-vertex 3-ball;
3. enumerate exact perfect matchings using MRV branching on the unmatched dual vertex with the fewest remaining candidate edges;
4. submit every recovered matching, up to the explicit solution cap, to the exact G3 verifier;
5. compare to the planted partition only after public acceptance.

The first implementation used a label-order pivot and correctly found the two matchings but performed relabel-dependent dead-end branches. The exact-head attack was strengthened to MRV; on an even cycle this leaves the initial two-way phase choice and then forces each remaining path, making the measured search relabel-stable.

### Exact Python 3.12 `g3-8` result

~~~text
pieces:                                  8
public V/E/F/T:                          18/49/48/16
Euler characteristic:                   1
boundary faces / max face incidence:    32/2
dual graph vertices / edges:            16/16
dual degree histogram:                  ((2,16),)
bridges / articulation points:           0/0
allowed candidate dual edges:            16
vertex-star candidate pairs:              16
vertex tetrahedron-degree histogram:     ((2,16),(16,2))
face occurrence checks:                  64
perfect matchings / cap:                  2/16
matching nodes / backtracks:             17/0
accepted decompositions:                  2
accepted non-planted decompositions:      1
reference witness accepted:              yes
~~~

### Deterministic sweep

Python 3.12 tested `g3-3`, `g3-5`, and `g3-8` over eight independently derived public relabel seeds each.

| Set | V/E/F/T | Dual edges | Candidate edges | Vertex-star pairs | Matching nodes/backtracks | Accepted | Non-planted accepted |
|---|---|---:|---:|---:|---:|---:|---:|
| g3-3 | 8/19/18/6 | 6 | 6 | 6 | 7/0 | 2 | 1 |
| g3-5 | 12/31/30/10 | 10 | 10 | 10 | 11/0 | 2 | 1 |
| g3-8 | 18/49/48/16 | 16 | 16 | 16 | 17/0 | 2 | 1 |

Across all **24/24** generated instances, the structural gate has zero bridges and zero articulation vertices, every dual edge is a valid candidate piece, A-030 finds exactly two accepted perfect-match decompositions, and exactly one accepted decomposition differs from the planted partition.

### Result

**G3 is rejected by A-030.**

This failure is the opposite of G1's piece recognizability. In G3 the local interfaces are intentionally indistinguishable, but that creates equivalent-witness multiplicity: the public object admits two alternating valid decompositions and either is sufficient for attacker success. Increasing the even-cycle length cannot repair this structural fact.

This is not a theorem that general HGES is easy. It rejects this generated distribution and shows that hiding the planted local phase is not enough when another public phase verifies.

### G4 gate

A successor may add genuinely nonlocal coupling between otherwise plausible local decomposition choices, but that coupling must be attacked before any trapdoor work as:

- parity / cycle-space / cohomology / gauge reduction;
- constrained matching and factor-graph propagation;
- low-width dynamic programming;
- exact-cover / CSP / SAT / CP-SAT recovery;
- automorphism and normalization attacks;
- equivalent-witness enumeration;
- planted-role statistical leakage.

No one-wayness, average-case hardness, post-quantum hardness, IND-CPA, IND-CCA, KEM, or production-security claim exists.

## A-031 — public GF(2) coupled-phase synchronization

### Target

G4 coupled-phase HGES negative control.

G4 starts from locally ambiguous `g3-3` gadgets. Each gadget has exactly two accepted public perfect-match decompositions, canonically represented by one phase bit. Generation publishes only pairwise phase differences `b_ij = x_i XOR x_j` on a connected redundant coupling graph.

### Public attack

A-031 uses no hidden reference phases:

1. enumerate and canonically order the two accepted G3 matchings for every gadget;
2. translate every public coupling edge into one binary linear equation;
3. recover phases by spanning-tree propagation from an arbitrary root bit;
4. check every redundant cycle constraint;
5. independently row-reduce the full public equation system over GF(2);
6. repeat propagation for both root bits;
7. lift both public phase vectors to local matching witnesses;
8. submit both to the exact G4 verifier;
9. compare to generation history only after public acceptance.

### Exact Python 3.12 `g4-12` result

~~~text
gadgets:                                  12
total public tetrahedra:                  72
coupling vertices / edges:                12/18
coupling cycle rank:                       7
per-gadget perfect matchings:              twelve copies of 2
total local matching nodes/backtracks:    84/0
XOR equations / variables:                18/12
GF(2) rank / nullity:                     11/1
GF(2) row XORs:                           72
propagation tree assignments:             22
propagation constraint checks:            36
recovered phase solutions:                 2
accepted public solutions:                 2
accepted non-reference solutions:          1
reference witness accepted:               yes
~~~

### Deterministic sweep

Python 3.12 tested `g4-4`, `g4-8`, and `g4-12` over eight independently derived deterministic seeds each.

| Set | Gadgets | Coupling edges | Cycle rank | Rank/nullity | Row XORs | Local matching nodes/backtracks | Propagation assignments/checks | Accepted | Non-reference |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| g4-4 | 4 | 6 | 3 | 3/1 | 10 | 28/0 | 6/12 | 2 | 1 |
| g4-8 | 8 | 12 | 5 | 7/1 | 38 | 56/0 | 14/24 | 2 | 1 |
| g4-12 | 12 | 18 | 7 | 11/1 | 72 | 84/0 | 22/36 | 2 | 1 |

All **24/24** generated instances have rank `g-1`, nullity `1`, two accepted public phase assignments, and exactly one accepted assignment different from the hidden reference.

### Result

**G4 is rejected by A-031.**

The new nonlocal coupling is exactly public binary synchronization/cohomology. Redundant cycles add consistency checks but no secret asymmetry; on a connected graph the only residual freedom is the common global phase flip, which is itself an accepted equivalent witness. Increasing the number of gadgets or coupling edges cannot repair the algebraic collapse.

This is not a theorem that general HGES is easy. It rejects this generated relation and shows that nonlocality alone is not useful when it factors through an abelian binary quotient.

### G5 gate

A successor must change the constraint algebra, not merely the graph. It must first face quotient/abelianization tests, finite-domain CSP, belief propagation/local consistency, low-width dynamic programming, exact SAT/CP-SAT, automorphism/normalization, equivalent-witness enumeration, and generated-role leakage. No trapdoor work begins from a parity-coupled relation.

## A-032 — public exact-one parity projection

### Target

G5 nonlinear exact-one HGES negative control.

G5 replaces G4's explicit pairwise XOR coupling by signed ternary exact-one clauses over the same publicly canonicalized two-phase G3 gadgets. A clause accepts when exactly one of `x_i XOR n_i`, `x_j XOR n_j`, `x_k XOR n_k` is true.

### Public attack

Exact-one-of-three has an immediate necessary parity consequence:

~~~text
(x_i XOR n_i) XOR (x_j XOR n_j) XOR (x_k XOR n_k) = 1,
~~~

so every public clause exposes

~~~text
x_i XOR x_j XOR x_k = 1 XOR n_i XOR n_j XOR n_k.
~~~

A-032 enumerates the two accepted local G3 matching phases, constructs this public affine system, performs Gauss-Jordan elimination over GF(2), lifts the recovered phase vector to public matching witnesses, and checks the original nonlinear exact-one verifier. Reference phases are used only after public acceptance.

### Exact Python 3.12 `g5-24` result

~~~text
gadgets:                                  24
total public tetrahedra:                 144
clauses:                                  48
variable degree histogram:               ((6,24),)
factor components / cycle rank:          1/73
per-gadget perfect matchings:             twenty-four copies of 2
local matching nodes / backtracks:        168/0
projected GF(2) equations / variables:    48/24
GF(2) rank / nullity:                     24/0
GF(2) row XORs:                           436
affine solution count:                    1
nonlinear clause checks:                  48
public parity witness accepted:           yes
public affine solution = reference:       yes
reference witness accepted:               yes
~~~

### Deterministic sweep

Python 3.12 tested `g5-12`, `g5-18`, and `g5-24` over eight independently derived deterministic seeds each.

| Set | Gadgets | Clauses | Degree | Factor cycle rank | Rank/nullity | Row XORs | Local matching nodes/backtracks | Nonlinear checks | Accepted/matched |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| g5-12 | 12 | 24 | 6 | 37 | 12/0 | 127 | 84/0 | 24 | 8/8 |
| g5-18 | 18 | 36 | 6 | 55 | 18/0 | 261 | 126/0 | 36 | 8/8 |
| g5-24 | 24 | 48 | 6 | 73 | 24/0 | 436 | 168/0 | 48 | 8/8 |

All **24/24** public parity recoveries are accepted by the original nonlinear verifier and all **24/24** equal the hidden reference phase vector after post-attack comparison.

### Result

**G5 is rejected by A-032.**

The nonlinear surface predicate does not help because this generated clause family publishes a full-rank solver-complete affine quotient. The parity equations are only necessary in general, but here they have a unique solution; the planted satisfying assignment is necessarily that solution, and the attacker confirms it with the public nonlinear verifier.

DPLL/SAT is not required to reject G5 because it would be a heavier attack than the already-fatal GF(2) projection. Increasing gadget count or clause density while retaining the same full-rank projection is not a repair.

This is not a theorem that general exact-one CSP or HGES is easy. It falsifies the current generated relation.

### G6 gate

A successor must use an accepted predicate whose cheap affine/quotient consequences are insufficient to reconstruct a verifier-valid witness. It must still face quotient tests, CSP/SAT, local consistency, low-width algorithms, automorphism/normalization, equivalent-witness multiplicity, and generated-role leakage before any trapdoor work.

## A-033 — affine-coset residual exact-one enumeration

### Target

G6 residual-affine HGES negative control.

G6 keeps G5's nonlinear signed exact-one verifier but changes the public clause scopes so the necessary GF(2) parity projection is deliberately incomplete: the coefficient matrix has rank `g-2`, nullity `2`, leaving four public affine phase candidates.

### Public attack

A-033 uses no hidden reference phases:

1. enumerate and canonically order the two public G3 matching phases for every gadget;
2. project every exact-one clause to its necessary affine GF(2) equation;
3. Gauss-Jordan reduce the public system;
4. recover a particular solution and the two-dimensional nullspace;
5. enumerate all four affine phase candidates;
6. evaluate every public nonlinear exact-one clause for every candidate;
7. lift surviving phase candidates to local matching witnesses;
8. submit survivors to the exact nonlinear verifier;
9. compare to generation history only after public acceptance.

### Exact Python 3.12 `g6-24` result

~~~text
gadgets:                                  24
total public tetrahedra:                 144
clauses:                                  48
variable degree histogram:               ((6,24),)
factor components / cycle rank:          1/73
local matching nodes / backtracks:       168/0
projected equations / variables:          48/24
GF(2) rank / nullity:                     22/2
GF(2) row XORs:                           308
affine candidates:                         4
residual nonlinear clause checks:         192
accepted affine candidates:                 1
exact verifier clause checks:              48
accepted non-reference candidates:          0
first accepted candidate = reference:      yes
reference witness accepted:                yes
~~~

### Deterministic sweep

Python 3.12 tested `g6-12`, `g6-18`, and `g6-24` over eight independently derived deterministic seeds each.

| Set | Rank/nullity | Affine candidates | GF(2) row XORs | Local matching nodes/backtracks | Residual checks | Accepted | Non-reference |
|---|---:|---:|---:|---:|---:|---:|---:|
| g6-12 | 10/2 | 4 | 92 | 84/0 | 96 | 1 | 0 |
| g6-18 | 16/2 | 4 | 188 | 126/0 | 144 | 1 | 0 |
| g6-24 | 22/2 | 4 | 308 | 168/0 | 192 | 1 | 0 |

All **24/24** generated instances expose exactly four affine candidates. A-033 finds exactly one nonlinear-valid public candidate in every instance; all **24/24** accepted candidates equal the hidden reference only under post-attack comparison.

### Result

**G6 is rejected by A-033.**

Unlike G5, the cheap affine quotient is genuinely incomplete, but its residual dimension is a fixed two bits. Exhaustively checking four public candidates is therefore a constant-size residual attack, not a cryptographic hardness source. Increasing `g` while preserving nullity two cannot repair the relation.

This is not a theorem that exact-one CSP or general HGES is easy. It falsifies this generated family and sharpens the next gate: quotient residual complexity must itself grow and survive dedicated solver attacks.

### G7 gate

A successor must ensure that every cheap quotient leaves residual entropy/search dimension growing with the generated instance, then face exact CSP/SAT, local consistency, low-width algorithms, normalization, equivalent-witness enumeration, and generated-role leakage before any trapdoor work.

## A-034 — public planted 3-SAT DPLL + independent MiniSat recovery

### Target

G7 planted signed 3-SAT phase-CSP negative control. G7 deliberately removes the direct affine shortcuts that rejected G4–G6: exhaustive local affine-hull enumeration confirms that the signed 3-OR predicate has no non-trivial GF(2) equation shared by all accepted local tuples.

### Public attack

A-034 uses only public gadgets and signed clauses:

1. recover and canonically order the two accepted G3 matchings for every gadget;
2. run iterative public unit propagation;
3. branch deterministically on the unresolved variable with highest current clause incidence;
4. enumerate phase assignments up to an explicit cap;
5. lift every assignment to local matching witnesses and submit it to the exact G7 verifier;
6. classify non-reference solutions only after public acceptance;
7. independently encode the fixed baseline as DIMACS, solve it with MiniSat, decode the model, lift it, and recheck it with the repository verifier.

### Exact Python 3.12 `g7-24` result

~~~text
gadgets:                                24
total public tetrahedra:               144
clauses:                                96
variable degree histogram:             ((12,24),)
factor components / cycle rank:        1/169
local affine implications:             0
local matching nodes / backtracks:     168/0
DPLL solutions / cap:                  16/16
DPLL cap hit:                           yes
DPLL nodes / decisions:                40/22
DPLL propagations / conflicts:         34/2
DPLL backtracks:                       2
exact verifier clause checks:          1536
accepted DPLL solutions:               16
accepted non-reference solutions:      16
first solution equals reference:       no
~~~

The independent MiniSat fixed-baseline run is SAT and records 3 conflicts, 13 decisions, and 41 propagations. Its decoded witness passes all 96 public clauses in the exact G7 verifier. Solver wall-clock timing is not used as stable evidence.

Python 3.12 also tests `g7-12`, `g7-18`, and `g7-24` over eight deterministic seeds each. All **24/24** instances yield at least one accepted public witness and at least one accepted non-reference witness. Measured DPLL node counts range from 23 to 86.

### Result

**G7 is rejected by A-034.** Removing an obvious affine quotient was necessary but not sufficient: the current deterministic planted 3-SAT distribution remains solver-friendly and exposes equivalent accepted witnesses. Do not repair this relation merely by increasing the variable or clause count. Worst-case 3-SAT hardness is not average-case cryptographic hardness.

This is not a theorem that arbitrary 3-SAT or general HGES is easy.
