# MORPH-KEM

**Attack-first research into independently motivated mathematical inverse relations.** This is a research project, **not a usable KEM**.

> **GLOBAL NO NOMINATION. Research-only. Do not use for securing any data.** No accepted OWF or post-quantum security assumption; no approved trapdoor, PKE, KEM or production implementation.

## Research status (2026-10-21)

- **Current research:** [independent-foundation pivot](docs/foundation/F0-independent-foundation-pivot-2026-10-21.md) and [#208](https://github.com/StanleyLl0yd/morph-kem/issues/208). **Planted-TI is FROZEN/comparator**, not active candidate work. First independent attack-first screen: [finite-ring deformation lifting](docs/foundation/F0-deformation-tower-public-lift-screen.md), an analytic **NO-GO** under its hypotheses; singular-obstruction D0 **HOLD**. [H-A/H-B/H-C](docs/foundation/F0-hypothesis-ledger.md) **HOLD**; no Field 15 admission.
- **Canonical N1:** [#196](https://github.com/StanleyLl0yd/morph-kem/issues/196), latest **N1-59** ([analysis](docs/107-morph-n1-59-hyperbolic-geodesic-no-go.md)); **N1-60 is unallocated**, not an automatic next experiment. [Stage registry](docs/foundation/research-stage-registry.md).
- **Mathematical no-go boundaries:** [failure map](docs/foundation/F0-failure-mechanisms.md), [coupled residual/acyclic joins](docs/foundation/F0-residual-core-and-acyclic-join.md), [finite-field matroid realization](docs/foundation/F0-matroid-realization-boundaries.md). These results do **not** nominate a new mathematical foundation.
- **Attacker wins** by finding any `y` accepted by the **full original** `Verify(P,y)`, not by recovering the planted secret. An **unconditional polynomial-time honest generator**, its true distribution, and the complete [15-field MORPH-R0 admission](docs/97-morph-r0-cross-line-postmortem.md#11-re-entry-gate-for-any-new-morph-family) are mandatory before experiments.
- **Strategy:** approximately **80%** source-first new mathematics, **20%** bounded HEPMR audit ([#195](https://github.com/StanleyLl0yd/morph-kem/issues/195), **BENCHMARK ONLY** through AP103). No code or samples for unadmitted candidates.

## Evidence and limitations

- [N1-52 frozen numerical checkpoint](docs/100-morph-n1-status-2026-10-14.md): **593,305** historical exact toy cases plus **40** controls as previously reported, **not independently reproduced in this update**. Newer F0 notes are analytical only.
- Historical exceptions: **N1-19 PARTIAL 19/30; N1-23 PARTIAL 9/12; N1-26 HOLD/BENCHMARK**. Original N1-46/47/51 ZIP archives remain **missing** ([#199](https://github.com/StanleyLl0yd/morph-kem/issues/199)).
- Worst-case complexity, high entropy, solver timeouts and structural novelty slogans are **not** evidence of average-case or PQ hardness.

## Navigation

[Overview](docs/00-overview.md) · [Research log](notes/research-log.md) · [Cryptanalysis index](docs/05-cryptanalysis.md) · [Original negative results and detailed legacy README](docs/archive/README-legacy-2026-10-14.md) · [Parallel supplements](docs/supplemental/README.md) · [Contributor/research rules](AGENTS.md) · [Security policy](SECURITY.md)

**MORPH-KEM** is a historical working name (Morse Obfuscated Reduction Path KEM), not a claim that a working cryptographic KEM exists.
