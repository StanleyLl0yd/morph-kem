# AGENTS.md

## Scope

This repository is a cryptographic research project, not a production cryptography library.

## Non-negotiable rules

1. Never claim MORPH-KEM is secure, post-quantum secure, IND-CPA secure, IND-CCA secure, or production-ready without an explicit proved result and independent review supporting that exact statement.
2. Preserve negative results. A successful attack is a research result and must not be hidden or rewritten as a success.
3. Distinguish clearly between:
   - definitions,
   - assumptions,
   - conjectures,
   - empirical observations,
   - proven statements.
4. Worst-case NP-hardness is not evidence of average-case cryptographic hardness.
5. Generated/planted instance distributions are part of the attack surface.
6. Do not introduce bespoke symmetric ciphers, hashes, PRNGs, or home-grown entropy sources.
7. Experimental code must be deterministic when given a seed and must record parameters needed for reproduction.
8. Security-sensitive comparisons and decapsulation experiments must avoid accidental oracle leakage when testing CCA-style behavior.
9. Do not delete attack code or failed experiments merely because they weaken the proposal.
10. Any external factual or literature claim added to research documents must include a source.

## Current MORPH-N1 gate (2026-10-14)

- Source of truth for active research: the latest numbered `docs/10*-morph-n1-*.md` outcome (currently `docs/107-morph-n1-59-hyperbolic-geodesic-no-go.md`), frozen N1-52 summary `docs/100-morph-n1-status-2026-10-14.md`, issue #196 and the complete 15-field gate in `docs/97-morph-r0-cross-line-postmortem.md`.
- **GLOBAL NO NOMINATION**. Strategy ~80% independent new mathematics, ~20% bounded HEPMR (#195, BENCHMARK ONLY through AP103). Research-only; no trapdoor, PKE/KEM, OWF/PQ claim or implementation branch for an unadmitted primitive.
- For every public `P`, attacker success is any member of `Equivalent(P)={candidate:Verify(P,candidate)}`. Require generation distribution, polynomial public verifier, full public-bitlength and entropy analysis, known canonicals/normal forms/attacks, matched controls, frozen validation, quantum screen and independently justified Field 15 *before* code.
- Historical N1-19 PARTIAL 19/30, N1-23 PARTIAL 9/12, N1-26 HOLD/BENCHMARK must not be silently completed. Do not rescue rejected results by parameter changes; do not restart broad HEPMR AP scans.
- Distinguish GitHub-issue-only N1 result claims from code, scripts, tests and archived artifacts actually committed to this repository. Never claim uncommitted datasets or case totals were locally reproduced.
- Prefer updates to active status and indexes over rewriting historical observations. After a checkpoint changes, synchronize the README, overview, open questions, cryptanalysis index and research log without deleting earlier findings.

## Git branch lifecycle (owner instruction, 2026-10-16)

- **No branch accumulation.** Create a branch only for a concrete PR; prefer reuse of an already-safe disposable branch when practical. Do not reserve a fresh branch for analytical discussion or an issue comment.
- After each PR merge, automatically prune its original merged branch with `branch-housekeeping.yml` only when its head SHA matches the merged PR record. The job may also remove no-PR branches already ancestral to `main`. **Never delete** `main`, protected branches, open-PR branches, closed-unmerged PR branches, SHA-mismatched branches, or unmerged/untracked unique commits.
- Existing unmerged divergent branches require individual provenance review before deletion. Never discard research evidence just to reduce branch count.
- Use the same normal exact-head CI, current-base review and expected-head merge gate. Delete merged temporary branches rather than retaining a branch per completed milestone.
- The cleanup can be dry-run via the GitHub Actions manual dispatch. If the workflow token lacks delete-ref permission, report the blocker instead of claiming branches were removed.

- The eight exceptional historical divergent branches dated 2026-10-16 are preserved before retirement through exact-SHA immutable Git tags; see [archive manifest](docs/archive/retired-branch-provenance-2026-10-16.md). Never delete historical divergent branches by assuming a closed unmerged PR is equal to its later clean replacement. Only the narrow reviewed `archive_legacy_branches.py` manifest is authorized for the one-time retirement.

## Per-pass repository sync (owner instruction, 2026-10-16)

- **Every completed research pass must update durable project files in GitHub**, not stop at an issue comment. Put scoped analytical proofs and source links under `docs/foundation/` (or another topic-appropriate path); keep `notes/research-log.md` current and synchronize status/index files only where the result changes them. Do not invent a numbered N1/F0-K stage, test, run, branch artifact, or empirical count merely to satisfy this rule.
- Prefer a **single focused PR per pass**, a reviewed current-base commit, exact-head applicable CI, and verified post-merge `main`. If CI or permissions block merging, leave an accurately identified open PR and report the blocker; **never claim project files on `main` were updated before merge**.
- Keep root `README.md` a **compact landing page** (research status, safety warning, live navigation); detailed proofs and historical case-by-case material belong in versioned `docs/`, with archive links intact. Avoid appending pass-by-pass prose to README.
- Research issue comments may provide review discussion and immutable evidence links, but **do not substitute for repository documentation**. Preserve rejected results and links, not only positive hypotheses.

## Workflow

- Prefer small, reviewable research milestones.
- Update `notes/research-log.md` when a result changes the state of the proposal.
- Update `docs/05-cryptanalysis.md` whenever an attack is proposed, tested, improved, or found fatal.
- Keep `spec/` normative and `docs/` explanatory.
- Keep parameter sets explicitly labeled `toy`, `experimental`, or `candidate`; never use `secure` as a parameter-set label.
- Before merging changes that affect the construction, verify consistency among the hard-problem definition, construction, security model, and attack model.

## Parallel research and canonical stage numbering (MORPH #206)

- **Working IDs:** Use collision-resistant unnumbered research identifiers (for example `X-20261016-topic-abcd1234` or `F0-Kn`) while working in parallel. Such labels **do not** reserve any `N1-xx` number, approve experiments or indicate a candidate.
- **Only canonical numbering authority:** [the research stage registry](docs/foundation/research-stage-registry.md), synchronized with active issue [#196](https://github.com/StanleyLl0yd/morph-kem/issues/196). The current last published stage is **N1-59**; **N1-60 is not reserved**. Comments, branch names, drafts and chat messages are not reservations.
- **Serialize reservation through main:** A research stage can receive the next `N1-xx` only in a reviewed PR that changes the registry's **single** `next_unallocated` line, identifies the exact 15-field evidence and public original verifier, and proves the stage label is not duplicated in open PRs. Its merge must compare current main to the reviewed base and reconcile any movement. A stage may have a negative result; reserving a number does not nominate a primitive.
- **Reconcile collisions, never overwrite:** Abandon conflicting stale numbering; retain issue comments and scientific evidence, and move nonoverlapping results to uniquely named supplements. Do not change historical conclusions or experiment counts to resolve collisions.
- **Exact-head merge gate:** Compare PR head, main head, review threads, changed paths, applicable CI and stage registry **again immediately before merge**. No assumed fixed number of checks, no force/stale merge. After merge check new main and independently triggered CI. See the executable manual checklist in the registry.

## Publication discipline

A public release should state what remains unproven and list known attacks and limitations. Do not rely on branding, novelty, obscurity, or code complexity as a security argument.
