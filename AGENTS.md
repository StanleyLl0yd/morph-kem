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

## Workflow

- Prefer small, reviewable research milestones.
- Update `notes/research-log.md` when a result changes the state of the proposal.
- Update `docs/05-cryptanalysis.md` whenever an attack is proposed, tested, improved, or found fatal.
- Keep `spec/` normative and `docs/` explanatory.
- Keep parameter sets explicitly labeled `toy`, `experimental`, or `candidate`; never use `secure` as a parameter-set label.
- Before merging changes that affect the construction, verify consistency among the hard-problem definition, construction, security model, and attack model.

## Publication discipline

A public release should state what remains unproven and list known attacks and limitations. Do not rely on branding, novelty, obscurity, or code complexity as a security argument.
