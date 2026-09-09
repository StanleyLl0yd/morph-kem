# MORPH-KEM

**MORPH-KEM** is exploratory post-quantum public-key cryptography research based on discrete Morse theory, combinatorial topology, and attack-first mathematical experimentation.

> **Research only. Not for production use. Not a security claim.**
>
> Do not use MORPH-KEM to protect real data, credentials, communications, or systems.

## Current status

**M0–M4 have all been implemented and rejected. No candidate primitive exists.**

- **M0** — broken by A-000 direct public coordinate recovery.
- **M1** — broken by A-008 meet-in-the-middle path recovery.
- **M2** — broken by A-014 structural hidden-core reconstruction.
- **M3** — honest equivalent-witness relation; broken by A-016 collapse plus spanning-tree construction.
- **M4** — closed triangulated tori with zero free collapses; broken by A-018 public primal/dual tree-cotree construction.

M5 remains the next M-series experiment: irregular non-manifold 2-complexes with exact equivalent-witness search.

## H-series side track

A separate **H-series** now studies the user's Möbius / Escher / Lobachevsky direction without changing the M-series conclusions.

Working research label:

**Hyperbolic Frustrated MORPH (HFM)**

The H-series investigates finite hyperbolic-like quotients and cell complexes with:

- negative-curvature combinatorics;
- orientation-preserving and orientation-reversing gluings;
- overlapping cycle holonomy;
- non-manifold junctions where useful;
- locally similar patches but globally coupled consistency constraints;
- equivalent-witness verification rather than recovery of one planted path.

**H0 is literature/threat-model work first.** Hyperbolic geometry, non-orientability, and holonomy are not assumed hard. In particular, the project explicitly rejects schemes whose secret reduces to ordinary orientability, first homology/cohomology, a simple surface-group word/conjugacy problem, or recoverable canonical quotient data.

See:

- docs/14-h-series-hyperbolic-charter.md
- docs/15-h1-holonomy-experiment.md

## Research discipline

- Any equivalent accepted witness counts as attacker success.
- Generated distributions are part of the attack surface.
- Worst-case hardness is not average-case cryptographic hardness.
- Negative results are preserved.
- Structural breaks are redesigned, not repaired by larger parameters.
- No KEM wrapper until a primitive survives dedicated attacks.
- "Hyperbolic", "non-orientable", or "Escher-like" are geometric descriptions, never security arguments.

## Key files

- src/morph_kem/ — constructions and attacks
- tests/ — exact validators and attack tests
- scripts/ — deterministic baselines and sweeps
- docs/05-cryptanalysis.md — attack ledger
- docs/13-m4-closed-surface.md — M4 result
- docs/14-h-series-hyperbolic-charter.md — H-series prior-art/threat charter
- docs/15-h1-holonomy-experiment.md — H1 signed-holonomy result
- docs/16-h2e-escher-atlas.md — Escher local-to-global frustration experiment
- notes/research-log.md — chronological record
- spec/morph-kem-v0.1.md — future-spec skeleton

## Next directions

**M5:** irregular non-manifold 2-complexes, exact witness search, CSP/SAT-style attacks, and incidence/canonicalization analysis.

**H1:** implemented and rejected. Z2 collapses by spanning-tree/cycle-space recovery; the S3 verifier also collapses exactly to Z2 because "normalized transition is a transposition" is equivalent to odd permutation parity.

**H2-E:** active Escher/Penrose branch. It models locally valid relative-height constraints with global cycle frustration and accepts any bounded seam repair. The first implementation is intentionally attacked as a gain-graph balancing problem.

**H2-H (#17):** parallel hyperbolic/Klein-quartic branch, currently deferred while H2-E is tested.

No security or post-quantum claim exists.

## Naming

MORPH-KEM is a working research name: Morse Obfuscated Reduction Path KEM.
