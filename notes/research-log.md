# MORPH-KEM research log

This is the active compact chronological research log.

The prior detailed log through 2026-09-11 is preserved verbatim in `notes/research-log-through-2026-09-11.md`. Repository commits and the numbered research documents remain the authoritative detailed evidence for individual experiments.

## 2026-09-14 — HGA4 finite-representation line frozen

The HGA4 Hurwitz/free-group endpoint line was pushed through exact-distance generation, held-out finite quotients and finally an adaptive endpoint-independent library of small finite representations. HGA4f recovered all measured exact endpoints while retaining fewer exact states than ordinary MITM on every declared endpoint. Training-conditioned generation had already failed to generalize to held-out representations.

**Decision:** freeze the HGA4 Hurwitz/free-group lineage. Do not condition generation against a growing representation library.

## 2026-09-14 — HGA re-entry survey ends with no nomination

A separate action-family literature gate was applied after HGA4. A finite Markoff-surface action was implemented only as a negative control and was recovered publicly on 72/72 declared instances. The subsequent binding-action survey found no candidate that cleared the HGA1–HGA4f failure classes strongly enough to justify another implementation.

**Decision:** HGA-R2 ends with **NO NOMINATION**. Trapdoor/KEM gate remains closed.

## 2026-09-14 — NAT residual-representation line frozen

NAT7/NAT8 showed that public tree normalization removes vertex-gauge secrecy and exposes the complete residual connection / free-generator representation. NAT9 then tested lossy `A5` observables; a public finite-domain CSP still recovered verifier-valid equivalent representations. NAT10 replaced exact/lossy publication with noisy `SL(2)` trace sketches, but public relator CSP again recovered large accepted representation families.

**Decision:** freeze the current NAT residual-representation family. Hiding the planted representation is irrelevant when public verification accepts many recoverable alternatives.

## 2026-09-14 — TDC current ensemble frozen after predeclared Lee–Brickell gate

The TDC2g common-overlay ensemble removed the earlier bounded low-weight word signal and survived matched decoder-work, reliability and bounded Prange/ISD checks. The predeclared TDC3c Lee–Brickell checkpoint then produced the declared topology-easier failure at the fixed comparison point. Aggregate evidence remained mixed, but the checkpoint rule had been fixed before measurement.

**Decision:** freeze the exact current TDC2g-derived ensemble. No parameter rescue by changing size, weights, overlay count, seeds or attack budget.

## 2026-09-14 — MORPH-R0 cross-line reset

The negative corpus across HGES, HGA, NAT and TDC was consolidated into `docs/97-morph-r0-cross-line-postmortem.md`.

Recurring failure classes were made explicit: verifier-equivalent witnesses, public canonicalization, low-dimensional/finite-quotient leakage, local topological relations, lift/base recovery, noise-to-polynomial reductions, generator-vs-action failure, matched-control discipline and no parameter rescue.

The original geometry inspirations—Möbius/nonorientable surfaces, Klein bottle, hyperbolic/Lobachevsky geometry and Escher/impossible-figure encodings—were re-screened against the measured attacks.

**Decision:** before any new implementation branch, require a complete mathematical re-entry specification including public relation, verifier/equivalence, known quotients, canonicalization attack, matched control, validation distribution, quantum screen and a concrete reason the proposal is not a renamed mature assumption. Trapdoor/KEM gate remains closed.

## 2026-09-14 — BPT-W0 harness bug found and corrected

The first BPT experiment was deliberately weak: stacked `S^3` endpoints generated with `1-4` moves, attacked by public `4-1` simplification.

The first exact-head CI failed two new BPT tests while 442/444 tests passed. The failure was in the attack harness, not evidence for the candidate. Greedy simplification can legally collapse an original root vertex, so source and target can simplify to differently labelled but combinatorially isomorphic boundary-of-4-simplex roots. The implementation incorrectly required literal root equality although the public verifier uses isomorphism equality.

The attack was corrected to recover a deterministic exact public root isomorphism, extend it to removed target vertices with fresh labels, transport the inverse target simplification path and splice the two public paths.

**Lesson:** canonicalization/equivalence semantics must be applied to the attack itself; generation labels are not part of the public relation.

## 2026-09-14 — BPT-W0 rejected by BPT-A000 as intended

After the label-invariant fix, the dedicated BPT workflow passes on Python 3.11/3.12/3.13.

Fixed Python 3.12 depth-three baseline:

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

The declared `d=1/2/3 × 8 seeds` sweep recovers accepted paths on **24/24** instances. Multiplicity lower bounds are 4, 16 and 64–96 by depth. Every recovered sweep path differs from the planted path after public success.

**Decision:** BPT-W0 is rejected exactly as required for a weak control. The BPT harness calibration passes through candidate failure. See `docs/98-bpt0-stacked-s3-weak-control.md` and BPT-A000 in `docs/05-cryptanalysis.md`.

## 2026-09-14 — prior Pachner corpus rediscovered as mandatory BPT inheritance

Repository-wide reconciliation found that ordinary `2-3 / 3-2` bounded Pachner transport had already been investigated in T0/T1.

T0/A-022: fixed `t0-8` plants an eight-move non-self-repeating path but has true quotient distance four; bidirectional recovery expands only 13 states.

T1/A-023: exact-distance shell generation repairs the planted-length defect, yet fixed `D=3` still falls to bidirectional recovery after only five expansions. The project explicitly declined to add a larger shell merely to inflate work.

**Decision:** T0/A-022 and T1/A-023 are inherited BPT negative controls. A future BPT proposal cannot re-enter as “the same `2-3 / 3-2` search at larger depth”.

## 2026-09-14 — BPT-R1 theorem/representation reconciliation

Issue #192 and `docs/99-bpt-r1-pachner-reconciliation.md` apply MORPH-R0 to the 2026 Tillmann–Tsvietkova NP-hardness result before more code is written.

Key findings:

- the theorem uses topological triangulations defined by tetrahedra with affine face pairings; quotient cells may have boundary self-identifications;
- MORPH's current `SimplicialComplex` is an abstract simplicial complex of unique vertex subsets and therefore does not faithfully represent that general category;
- the theorem's sparse degree-two collapse is narrower than a generic topology-preserving edge collapse;
- the hard family is obtained by a Karp reduction from modified planar Hamiltonian path, with graph-edge deletion represented by sparse collapses;
- Regina already exposes public isomorphism signatures, Pachner navigation, exhaustive simplification and topology-preserving edge-collapse machinery that must be treated as attacker capability;
- no BPT-specific quantum algorithm was identified in the screening pass, but generic Grover/quantum-walk speedups remain relevant and absence of a special algorithm is not post-quantum evidence.

**Decision: NO NOMINATION.**

Do not build a generalized face-pairing engine, theorem-reduction generator, BPT-R2 implementation, trapdoor, PKE or KEM from the current state. Re-open BPT only when a concrete generated relation is materially distinct from both T0/T1 and the Hamiltonian-path reduction family and clears the full MORPH-R0 specification on paper first.

No security claim.
