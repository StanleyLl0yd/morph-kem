# 05 — Cryptanalysis ledger

This file is the canonical compact attack index for MORPH-KEM. Successful breaks are research results and remain part of the record.

Historical detail is preserved verbatim in:

- `docs/05-cryptanalysis-through-a024.md` — original detailed records through A-024;
- `docs/05-cryptanalysis-through-a048.md` — exact snapshot of the previous canonical ledger, including detailed A-028 through A-048 records.

The compact table below is authoritative for attack IDs and current dispositions. New measured attacks must also be recorded in `notes/research-log.md`.

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
| A-022 | Short equivalent Pachner path + bidirectional recovery | **Fatal to T0 generator; inherited BPT control** | Implemented |
| A-023 | Exact-distance bidirectional Pachner recovery | **Fatal to T1 generated distribution; inherited BPT control** | Implemented |
| A-024 | Dual-graph canonical gluing recovery | **Fatal to G0 by design** | Implemented |
| A-025 | Cover/subgroup/monodromy factorization | Cross-cutting frontier | Reserved |
| A-026 | Normal-form/geodesic/mapping-class canonicalization | Cross-cutting frontier | Reserved |
| A-027 | Group-action/hidden-shift quantum reduction | Cross-cutting frontier | Reserved |
| A-028 | Public K4 / allowed-piece exact-cover recovery | **Fatal to G1 generated distribution** | Implemented |
| A-029 | Public stellar-center contraction + macro recovery | **Fatal to G2 generated distribution** | Implemented |
| A-030 | Equivalent perfect-matching gluing recovery | **Fatal to G3 generated distribution** | Implemented |
| A-031 | Public GF(2) coupled-phase synchronization | **Fatal to G4 generated distribution** | Implemented |
| A-032 | Public exact-one parity projection | **Fatal to G5 generated distribution** | Implemented |
| A-033 | Affine-coset residual exact-one enumeration | **Fatal to G6 generated distribution** | Implemented |
| A-034 | Public planted 3-SAT DPLL + independent MiniSat recovery | **Fatal to G7 generated distribution** | Implemented |
| A-035 | Public local-phase extraction and topology-to-CSP factorization | **Structural break of G4–G7 design line** | Implemented |
| A-036 | Public overlapping-piece enumeration + exact cover / cycle DP | **Fatal to G9 generated distribution** | Implemented |
| A-037 | Public toroidal bipartite perfect-matching recovery | **Fatal to G10 generated distribution** | Implemented |
| A-038 | Public toroidal P3 hypergraph exact-cover + SAT recovery | **Fatal to G11 generated distribution** | Implemented |
| A-039 | Public irregular-carrier P3 extraction + exact-cover / SAT recovery | **Fatal to G12 generated distribution** | Implemented |
| A-040 | Configuration-pairing generator-conditioning audit | **Fatal to G13 carrier distribution** | Implemented |
| A-041 | Public reverse-stacking / stellar-center normalization | **Fatal to G14 carrier distribution** | Implemented |
| A-042 | Flip-mixed sphere normalization + P3 exact-cover / SAT recovery | **Fatal to G15 generated distribution** | Implemented |
| A-043 | Public fundamental-cycle cohomology-pairing recovery | **Fatal to G16 generated distribution** | Implemented |
| A-044 | Public tree-cotree primal-dual one-crossing recovery | **Fatal to G17 generated distribution** | Implemented |
| A-045 | Public shortest odd-cocycle cycle + constrained exact-one-crossing connector | **Fatal to G18 generated distribution** | Implemented |
| A-046 | Delete-one-cycle parity-cover recovery of bounded vertex-disjoint odd-cycle pair | **Fatal to G19 generated distribution** | Implemented |
| A-047 | Four-sheet distinct-class delete-and-recover multicurve recovery | **Fatal to G20 generated distribution** | Implemented |
| A-048 | Full genus-two tree-cotree exact crossing-matrix recovery | **Structural break of G21 generated relation** | Implemented |
| BPT-A000 | Greedy 4-1 simplification + public root-isomorphism path splice | **Fatal to BPT-W0 by design; validates BPT harness** | Implemented |

## BPT-A000 — label-invariant stacked-S3 simplification splice

### Target

BPT-W0, the deliberately weak stacked-`S^3` calibration family in `docs/98-bpt0-stacked-s3-weak-control.md`.

### Public attack

The attacker uses no generation history:

1. greedily apply the lexicographically first legal `4-1` move to the source endpoint;
2. do the same independently to the target endpoint;
3. recover an exact public combinatorial isomorphism between the resulting five-tetrahedron roots;
4. extend this mapping with fresh labels for target vertices removed during simplification;
5. transport the inverse target simplification path through the recovered isomorphism;
6. splice it after the source simplification path;
7. submit the resulting path to the ordinary public verifier.

The first implementation incorrectly required literal equality of the two simplified roots. Exact-head CI exposed that bug: greedy simplification may legally collapse an original root vertex, so the roots can be differently labelled while remaining combinatorially isomorphic. The corrected attack follows verifier semantics instead of generation labels.

### Exact measured result

Dedicated exact-head CI passes on Python 3.11, 3.12 and 3.13. The Python 3.12 fixed depth-three baseline records:

```text
source/target vertices:                 8/8
source/target tetrahedra:               14/14
move bound / recovered length:          6/6
source/target simplification steps:     3/3
combined vertex scans:                  52
combined legal 4-1 moves seen:          13
source/target simplification paths:     8/12
accepted-path multiplicity lower bound: 96
public recovered path accepted:         yes
recovered path equals planted path:     no
```

The declared `d=1/2/3 × 8 seeds` sweep succeeds on **24/24** instances. Recovered lengths are exactly `2/4/6`; accepted-path multiplicity lower bounds are `4`, `16`, and `64–96` respectively. Every recovered sweep path differs from the planted path after public success.

### Result

**BPT-W0 is rejected by BPT-A000 exactly as intended.**

This is a harness calibration, not cryptographic evidence. It confirms that BPT attacks are label-invariant and use the actual equivalent-witness relation. A-022 and A-023 remain mandatory inherited controls for any stronger Pachner proposal.

## Current BPT re-entry state

`docs/99-bpt-r1-pachner-reconciliation.md` applies MORPH-R0 before additional implementation. Current decision: **NO NOMINATION**.

Reasons include:

- ordinary generated `2-3 / 3-2` transport was already rejected by A-022/A-023;
- MORPH's current abstract `SimplicialComplex` does not faithfully model the more general face-pairing triangulations used by the 2026 Tillmann–Tsvietkova theorem;
- the theorem's worst-case hard family is obtained by a Karp reduction from modified planar Hamiltonian path, so direct implementation would not by itself establish a new average-case or post-quantum assumption;
- mature Regina-style simplification, isomorphism signatures, edge collapses and Pachner navigation must be treated as attacker capabilities.

Do not build a generalized triangulation engine, theorem-reduction generator, trapdoor, PKE or KEM until a materially new generated relation clears the MORPH-R0 paper gate.

## Persistent fatal-flaw classes

- generated/planted distribution leakage;
- local or global canonical decomposition;
- equivalent-witness multiplicity;
- easy recognizable homotopy/structural class;
- shared hidden structure;
- low-width or solver-friendly constraint structure;
- public quotient/gauge normalization;
- fixed-size local motifs that reveal hidden pieces;
- cosmetic representation layers with a public local inverse;
- planted path length that does not equal or predict public quotient distance;
- worst-case NP-hardness imported through an explicit mature-problem reduction without an independent average-case distribution.

Every attack record must distinguish measured evidence from asymptotic claims and include exact parameter sets, seed horizon, work metrics, verifier outcome and interpretation.

No security claim.
