# 00 - Overview

## Current objective (2026-10-14)

MORPH-KEM is a **research-only, attack-first search for an independently motivated mathematical inversion relation** that is not just a renamed classical cryptographic assumption or a hard-looking encoding. Its original discrete Morse / topological KEM concepts are historical negative controls, **not an active candidate architecture**.

**GLOBAL NO NOMINATION.** No OWF, PQ-security, trapdoor, PKE or KEM claim. No implementation is authorized until a mathematical relation survives the [MORPH-R0 15-field entry gate](97-morph-r0-cross-line-postmortem.md#11-re-entry-gate-for-any-new-morph-family).

## Current program

- ~80% genuinely new mathematics and public any-witness inversion attacks, recorded in [#196](https://github.com/StanleyLl0yd/morph-kem/issues/196).
- ~20% restricted HEPMR review through AP103 in [#195](https://github.com/StanleyLl0yd/morph-kem/issues/195); **BENCHMARK ONLY**, no wider scan.
- [N1-52 checkpoint](100-morph-n1-status-2026-10-14.md) records 593,305 exact toy protocol cases plus 40 controls since N1-34, all without a nominated candidate. Next gate: N1-53.

For every proposed public instance `P`, the attacker wins by producing **any** `candidate` satisfying `Verify(P,candidate)`; planted-source recovery is not required. Generated distribution, public bitlength, the fibre `Equivalent(P)`, polynomial verifier, known normal forms, classical/quantum attacks and Field-15 distinctness must be explicit *before* code.

## Historical materials

The older descriptions in `01` through `04`, `spec/morph-kem-v0.1.md`, and the M/H/K/G/HGA/NAT/TDC/BPT experiment files document **rejected research directions**. Preserve them for reproducibility; do not interpret historical `KeyGen`, `Decaps` or trapdoor sketches as a live roadmap.

Source of truth: [current status](100-morph-n1-status-2026-10-14.md), [research log](../notes/research-log.md), [cryptanalysis ledger](05-cryptanalysis.md), [MORPH-N1 #196](https://github.com/StanleyLl0yd/morph-kem/issues/196).
