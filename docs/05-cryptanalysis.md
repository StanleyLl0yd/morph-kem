# 05 — Cryptanalysis ledger

This file is the canonical **repository-implemented legacy attack ID index** for MORPH-KEM. Successful breaks are research results and remain part of the record. The subsequent MORPH-N1 paper/issue series N1-01..59 (with explicitly partial/held exceptions) is tracked separately in [#196](https://github.com/StanleyLl0yd/morph-kem/issues/196) and [current N1 snapshot](100-morph-n1-status-2026-10-14.md). **No new A-ID or executable attack is implied by a research issue comment.** N1-53..59 add **analytic-only**, non-implemented public-section no-go results: [resistance/Laplacian](101-morph-n1-53-resistance-no-go.md), [Hankel realization](102-morph-n1-54-hankel-realization-no-go.md), [2-adic digit trie](103-morph-n1-55-adic-trie-no-go.md), [cyclic bispectrum](104-morph-n1-56-finite-bispectrum-no-go.md), [Walsh-Radon tomography](105-morph-n1-57-radon-walsh-no-go.md), and [symmetric principal minors](106-morph-n1-58-principal-minors-no-go.md), and [rational hyperbolic-geodesic inversion](107-morph-n1-59-hyperbolic-geodesic-no-go.md). These do **not** claim new A-series attack IDs, source code, test cases or numerical evidence.

**Additional non-A-ID analytical screen (2026-10-16):** [finite-field matroid realization](foundation/F0-matroid-realization-boundaries.md) gives exact original-verifier accepted public sections for rank two, the frame-generated rank-three subclass, frame-free simple rank-three near-pencils (all finite fields), core-anchored simple rank-three configurations over `q>n²` (deterministic line/conic avoidance), and near-certain large-field uniform honest-source outputs for fixed rank. This is a scoped mathematical/source-distribution failure, not a universal matroid inversion theorem, a measured attack or a new A-ID. [Original research comment](https://github.com/StanleyLl0yd/morph-kem/issues/208#issuecomment-6216134094).

**Additional non-A-ID single-form analytical screen (2026-10-16):** [one alternating form](foundation/F0-one-alternating-form-rank-screen.md) admits a polynomial full-verifier TI witness at **every feasible dimension**; under the *ideal uniform* planted-vs-null laws, public matrix rank is exactly sufficient for optimal detection, with explicit finite-field counting formulas. This does **not** solve the general multi-form/tensor problem, does not introduce A-IDs or experiments, and is not new Field-15 evidence.

**Additional non-A-ID regular-pencil screen (2026-10-16):** [alternating two-form pencils](foundation/F0-regular-alternating-pencil-public-section.md) with a publicly nonsingular combination admit deterministic polynomial common-TI witnesses for every `d≤n/2` in even dimension, including `F_2`; redundant larger tuples of public span dimension ≤2 inherit this section. Under two independent uniformly conditioned planted slices, exact full-source inverter success is at least `455/2304` (strictly bounded exact binary-field sampler). This is a scoped analytic attack, not a general tensor inverter, code benchmark or A-ID.

**Additional non-A-ID hyperplane inversion screen (2026-10-16):** [arbitrary multislice alternating hyperplanes](foundation/F0-multislice-isotropic-hyperplane-linearization.md) at `d=n−1` admit public **linear** full-verifier decision/search for **all finite fields, any m**, exact hyperplane/basis fibre count, rank-of-wedge-kernel sufficient statistic for ideal planted/null detection, and strong unconditional null false-positive bounds. Codimension ≥2 still requires decomposable Plücker witnesses. This is analytic only, not a new A-ID, experimental run or general TI hardness statement.

**Additional non-A-ID fixed-codimension wedge screen (2026-10-16):** [one-dimensional public wedge kernels and full-span planted-form attack](foundation/F0-fixed-codimension-wedge-kernel-section.md). For **fixed c**, a decomposable kernel line constructs a full-original-verifier accepted `d=n−c` subspace. On honest conditionally uniform full-vanishing-form sources, `m≥D=binom(n,2)−binom(d,2)` public slices yield exact full-span inversion probability `prod(j=0..D−1)(1−q^(j−m))`. This is NOT an all-input attack for higher-dimensional wedge kernels, an implemented A-ID, a new staged protocol, or PQ-security evidence.

**Additional non-A-ID two-slice support attack (2026-10-16):** [intersection of public alternating-slice images](foundation/F0-two-slice-public-row-support-intersection.md) exactly recovers a high-dimensional planted totally isotropic subspace under the public certificate `rank A_1=rank A_2=2c, dim(im A_1∩im A_2)=c`. For two independent conditional-uniform planted slices, `d≥2c`, attack success on the complete honest distribution is **exactly** `prod(j=0..2c−1)(1−q^(j−d))`. This requires **only two** public slices and polynomial linear algebra even when c grows. Not a general high-m low-d inversion, code implementation, A-ID or security claim.

**Additional non-A-ID adaptive support attack (2026-10-16):** [all-m public image intersections](foundation/F0-adaptive-multislice-support-intersection.md) choose rank-`2c` alternating slices **without conditioning the generator**, intersect their covector images and verify the full original tuple. For the independent conditionally uniform planted source and **every d>c**, exact full-source attack success is a polynomial-bit finite sum from classical Gaussian-binomial Möbius inversion, with simple lower bound `max(0,1−((q^d−1)/(q−1))·(3/4)^m)`. The external `d<c` planted-TI conjectural regime is **not covered**. Analytical only; no A-ID, measured runs or security claim.

**Additional non-A-ID Plücker kernel-plane screen (2026-10-16):** [binary-field wedge-nullity two](foundation/F0-plucker-two-dimensional-kernel-section.md) admits deterministic polynomial full-original-verifier decision/search for fixed codimension c using the quadratic equations of the Grassmannian restricted to the public kernel's projective line. The **exact** accepted d-subspace count is 0, 1, 2 or q+1, without enumerating `GF(2^e)`; arbitrary higher-dimensional kernels remain unresolved. Analytical only, no A-ID, code, generated experiments or crypto claims.

**Additional unnumbered F0 sparse-TI rank null controls (2026-10-19):** [exact individual-slice rank distributions and high-corank MinRank threshold exclusion](foundation/F0-sparse-planted-ti-rank-profile-minrank-screen.md). In the externally conjectural `m~n/log n,d~n/C,C>=3` regime, all individual ranks jointly have negligible planted-vs-unrestricted TV; on either source no projective linear combination typically has corank `>=ceil(2 sqrt(m))+2`. This does **not** exclude lower-threshold adaptive MinRank, solve original witness inversion, introduce an A-ID or provide crypto evidence.

**Additional F0 fixed-field matroid no-go (2026-10-19):** [full labelled rank-table public inversion](foundation/F0-matroid-realization-boundaries.md#7-all-fixed-field-fixed-rank-labelled-matroids-finite-projective-point-enumeration) works **pointwise for every honest matrix** when finite q and rank r are fixed. Public zero/parallel classes compress to at most `M=(q^r−1)/(q−1)` projective directions, permitting ≤`M!` candidate assignments and complete original-verifier rank checks. For GF(2), r=3, this is ≤5040 assignments. Does **not** solve growing-field rank-three realizability or succinct rank interfaces; analytic only, no A-ID or novel crypto basis.

**Stronger F0 binary-matroid public inverter (2026-10-19):** [basis-exchange reconstruction for all honest GF(2) matroids](foundation/F0-matroid-realization-boundaries.md#8-all-honest-binary-matroids-exact-public-standard-representation-by-basis-exchanges) needs only `O(nr)` public rank **or independence** queries **even at growing rank**. Replacing one basis column and observing the rank reveals the corresponding normalized GF(2) bit. The output represents exactly the original matroid; a full rank-table verifier accepts. This **supersedes** the 5040-assignment GF(2), rank-three enumeration bound. Does not transfer to GF(q>2), adversarial nonrepresentable NO or a succinct polynomial verifier without separate evidence. Classical binary matroid theory, not a new A-ID or crypto candidate.

**Additional F0 arbitrary-rank GF(3) oracle inversion (2026-10-19):** [ternary chordless-cycle public section](foundation/F0-matroid-realization-boundaries.md#9-all-honest-ternary-matroids-polynomial-public-reconstruction-from-independence-queries) reconstructs a labelled GF(3) matrix of **any rank** with polynomial exact public independence-oracle queries. Fundamental replacement queries expose `[I|D]` support; induced-cycle determinant tests reveal edge-sign parities; binary cycle-space elimination recovers a representation differing from the planted only by rank-preserving gauges. This is established Seymour/Truemper ternary representability mathematics, **not** a new Field-15 candidate, a GF(q≥4) algorithm, code or any security claim.

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
