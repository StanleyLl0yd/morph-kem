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

- Source of truth for active research: the latest numbered `docs/10*-morph-n1-*.md` outcome (currently `docs/105-morph-n1-57-arithmetic-matroid-no-go.md`), frozen N1-52 summary `docs/100-morph-n1-status-2026-10-14.md`, issue #196 and the complete 15-field gate in `docs/97-morph-r0-cross-line-postmortem.md`.
- **GLOBAL NO NOMINATION**. Strategy ~80% independent new mathematics, ~20% bounded HEPMR (#195, BENCHMARK ONLY through AP103). Research-only; no trapdoor, PKE/KEM, OWF/PQ claim or implementation branch for an unadmitted primitive.
- For every public `P`, attacker success is any member of `Equivalent(P)={candidate:Verify(P,candidate)}`. Require generation distribution, polynomial public verifier, full public-bitlength and entropy analysis, known canonicals/normal forms/attacks, matched controls, frozen validation, quantum screen and independently justified Field 15 *before* code.
- Historical N1-19 PARTIAL 19/30, N1-23 PARTIAL 9/12, N1-26 HOLD/BENCHMARK must not be silently completed. Do not rescue rejected results by parameter changes; do not restart broad HEPMR AP scans.
- Distinguish GitHub-issue-only N1 result claims from code, scripts, tests and archived artifacts actually committed to this repository. Never claim uncommitted datasets or case totals were locally reproduced.
- Prefer updates to active status and indexes over rewriting historical observations. After a checkpoint changes, synchronize the README, overview, open questions, cryptanalysis index and research log without deleting earlier findings.

## Workflow

- Prefer small, reviewable research milestones.
- Update `notes/research-log.md` when a result changes the state of the proposal.
- Update `docs/05-cryptanalysis.md` whenever an attack is proposed, tested, improved, or found fatal.
- Keep `spec/` normative and `docs/` explanatory.
- Keep parameter sets explicitly labeled `toy`, `experimental`, or `candidate`; never use `secure` as a parameter-set label.
- Before merging changes that affect the construction, verify consistency among the hard-problem definition, construction, security model, and attack model.

## Publication discipline

A public release should state what remains unproven and list known attacks and limitations. Do not rely on branding, novelty, obscurity, or code complexity as a security argument.
