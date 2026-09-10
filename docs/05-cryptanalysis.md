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

### G3 gate

A successor must remove both canonical fixed-size piece motifs and obvious public local inverses. It must immediately face:

- bridge, articulation, and low-order separator decomposition;
- multiscale motif/subcomplex enumeration;
- vertex-link and boundary-signature role leakage;
- public simplification/contraction and bistellar normalization;
- piece automorphism normalization;
- exact-cover / SAT / CP-SAT recovery;
- equivalent-witness enumeration;
- planted-role statistical leakage.

No one-wayness, average-case hardness, post-quantum hardness, IND-CPA, IND-CCA, KEM, or production-security claim exists.
