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

A-025 through A-027 are reserved cross-cutting frontier attacks, not yet implemented ledger entries: cover/subgroup/monodromy factorization, normal-form/geodesic/mapping-class canonicalization, and group-action/hidden-shift quantum reduction. Their definitions are maintained in `docs/29-k2-topological-hard-problem-frontier.md`.

## Persistent fatal-flaw classes

- generated/planted distribution leakage;
- local or global canonical decomposition;
- equivalent-witness multiplicity;
- easy recognizable homotopy/structural class;
- shared hidden structure;
- low-width or solver-friendly constraint structure;
- public quotient/gauge normalization;
- fixed-size local motifs that reveal hidden pieces.

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

### Deterministic sweep

Python 3.12 tested `g1-4`, `g1-8`, and `g1-12` over eight independently derived public relabel seeds each.

| Set | Dual edges | Bridges | Articulations | 2-vertex separators | 4-subsets | K4 / allowed | Covers | Cover nodes/backtracks | Accepted/matched |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| g1-4 | 28 | 0 | 0 | 24 | 1,820 | 4 / 4 | 1 | 5 / 0 | 8/8 |
| g1-8 | 56 | 0 | 0 | 112 | 35,960 | 8 / 8 | 1 | 9 / 0 | 8/8 |
| g1-12 | 84 | 0 | 0 | 264 | 194,580 | 12 / 12 | 1 | 13 / 0 | 8/8 |

All **24/24** public A-028 recoveries are accepted and all **24/24** match the planted partition up to group order. Exact recovery of the planted partition is stronger than required: any accepted equivalent witness would already be attacker success.

### Result

**G1 is rejected by A-028.**

The break is structural for the current generated family. Removing bridges and articulation vertices only removes one canonical decomposition route; it does not hide the pieces themselves. Each piece remains a public fixed-size clique, and the exact-cover phase has one candidate per planted block and zero backtracking on the measured sets.

Do not increase the G1 cycle size as a repair. The next HGES stage must alter the public piece/overlap structure so the planted pieces are not directly recognizable fixed-size dual motifs.

This is not a theorem that general Hidden Gluing Equivalence Search is easy. It is a falsification of this generated distribution and a calibration of the next decomposition attack layer.

### G2 gate

Before any trapdoor work, a successor must face at least:

- bridge, articulation, and low-order separator decomposition;
- maximal subcomplex / clique / motif enumeration;
- local apex, boundary-port, and incidence-role signatures;
- piece automorphism normalization;
- exact-cover / SAT / CP-SAT recovery;
- equivalent-witness enumeration;
- planted-role statistical leakage.

A natural next negative control is to destroy the literal `K4` motif by an interior stellar subdivision and then test whether public contraction of those subdivision centers reconstructs the same macro-`K4` decomposition. If that contraction succeeds, subdivision is only cosmetic obfuscation and the successor must be rejected rather than scaled.

No one-wayness, average-case hardness, post-quantum hardness, IND-CPA, IND-CCA, KEM, or production-security claim exists.
