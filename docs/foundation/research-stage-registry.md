# MORPH research coordination and canonical stage registry

**2026-10-16. Governance-only. [#206](https://github.com/StanleyLl0yd/morph-kem/issues/206).** This document controls the **allocation of canonical research stage labels**, not candidate approval, experiment authorization, software releases or the security of any proposal. Research remains **GLOBAL NO NOMINATION**; all F0 hypotheses HOLD. This document does not rewrite any historical experiment, #196 issue post or accepted candidate.

## Single serialized stage allocation record

| Field | Authoritative value |
| --- | --- |
| Canonical series | `N1` |
| Last published canonical stage | **N1-59** |
| Next unallocated label | **N1-60** |
| Reserved future labels | **none** |
| Active historical record | [MORPH-N1 #196](https://github.com/StanleyLl0yd/morph-kem/issues/196) |
| Parallel F0 research | [MORPH-F0 #208](https://github.com/StanleyLl0yd/morph-kem/issues/208), **not N1 numbering** |

**To reserve:** edit the *existing next-unallocated row in this file*, replacing the one value with the next value, and append a row to the reservation history below. A canonical label must appear only once, and the new PR must independently document all **15** MORPH-R0 fields, honest distribution, full accepted-verifier equivalence and Field-15 prior art evidence. A failing/rejected stage may be recorded canonically if the complete result is ready; a research sketch or paper-only F0 no-go is not eligible for a new N1 number. A registry edit alone does not pass the technical review. To prevent two researchers taking the same label, merging the reviewed edit into current main is the serialization point; two competing PRs changing the same `Next unallocated label` row cannot both be treated as having reserved the same stage. A stale PR **must be re-reviewed/rebased or withdrawn**, not force merged.

**History (append-only once an actual reservation PR merges):** none after N1-59. Historical N1-56/57/58 conflicts are archived in [#206](https://github.com/StanleyLl0yd/morph-kem/issues/206) and [the issue #196 reconciliation](https://github.com/StanleyLl0yd/morph-kem/issues/196#issuecomment-6176425069). Noncanonical S1/S2 preserved separately in [supplemental/](../supplemental/README.md), not reassigned sequential labels.

### Work-in-progress and parallel outputs

Before starting work, inspect current main, #196, the registry and all open N1 PRs. Use a collision-resistant provisional ID such as `X-YYYYMMDD-topic-8hex`, where the suffix is derived from a short hash of unique work context; **do not use proposed canonical stage numbers as filenames, issue titles or branch names**. The original provenance and research result may be preserved even if a parallel branch must later be renamed as a supplement.

### Pre-merge reconciliation (mandatory human/tool checklist)

1. Read the exact current `main` SHA, full PR head SHA, base SHA, diff paths, open PR list and any registry change. Check the canonical #196 header and original per-stage comments. If main advanced, **stop**, compare the intervening diff, explicitly reconcile affected files and restart exact-head review on a new base. Do not assume a green old check run validates a new commit.
2. Confirm all **applicable** exact PR-head CI check runs are **completed successfully**, inspect review threads and blockers, and verify the PR is mergeable. A docs-only PR can have fewer jobs than a code PR. Never invent `20/20` or `62/62` as a universal requirement.
3. For an N1 reservation specifically, verify the old registry row is the one current main still contains, the new monotone successor is correct, the appended history names the approved result and evidence, and no other current PR reserves or publishes that number.
4. Immediately before merging, re-check `main` and PR head; require the reconciled reviewed main base and invoke a merge with **expected head SHA**. If a mismatch occurs, stop and investigate, never force.
5. Confirm PR merged, get actual new `main` commit, inspect its parent(s) and diff, and distinguish post-merge **CI in progress** from post-merge **CI success**. Update #196 and the registry/history where a numbered result was accepted, retaining immutable original issue comment IDs and original experimental provenance.

A GitHub issue comment cannot itself create an atomic number reservation. This is a **process and review rule** unless enforced by branch protection/CI, not a claim that text instructions automatically lock GitHub ref updates.

### Unchanged research and safety boundaries

Research-only; no implementation branch, trapdoor/PKE/KEM, OWF/PQ hardness/security claim or new empirical source without prior 15-field admission and preregistration. Never infer security from a solver timeout, worst-case NP-hardness, dense graph coupling or fibre cardinality. Attacker target remains `Equivalent(P)={y:Verify(P,y)}` for **any** accepted witness. N1-19 PARTIAL 19/30, N1-23 PARTIAL 9/12, N1-26 HOLD/BENCHMARK and #199 missing archive bytes remain unchanged; HEPMR #195 BENCHMARK ONLY through AP103; 80/20 research split unchanged.
