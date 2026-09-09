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
- docs/16-h2e-escher-atlas.md — H2-E1 edge-gain Escher result
- docs/17-h2e2-higher-atlas.md — H2-E2 higher-order chart experiment
- docs/18-h2e3-frontier.md — Goldreich/local-OWF frontier and H3-E novelty gate
- docs/19-h3e-lifted-atlas.md — graph-cover prior art and public gauge-normalization calibration
- docs/20-h3e-composite-cover-frontier.md — public-key adaptation/interface gate
- docs/21-h2-klein-quartic-a5.md — exact hyperbolic Klein-quartic/A5 experiment
- docs/22-k0-klein-bottle.md — non-orientable Klein-bottle orientation control
- notes/research-log.md — chronological record
- spec/morph-kem-v0.1.md — future-spec skeleton

## Next directions

**M5:** irregular non-manifold 2-complexes, exact witness search, CSP/SAT-style attacks, and incidence/canonicalization analysis.

**H1:** implemented and rejected. Z2 collapses by spanning-tree/cycle-space recovery; the S3 verifier also collapses exactly to Z2 because "normalized transition is a transposition" is equivalent to odd permutation parity.

**H2-E1:** implemented and rejected. The Escher/Penrose relative-height atlas is genuinely locally satisfiable and globally frustrated, but its obstruction is exactly ordinary cycle-gain data and minimum equivalent seam repairs are found cheaply by unbalanced-cycle branching.

**H2-E2:** implemented and rejected. Every tested chart pair is locally compatible, but exact Max/NAE-CSP repair finds a one-chart equivalent repair across the full toy ladder; simple chart signatures also expose planted roles in several sets.

**H2-E3:** naive all-charts variant rejected before code. Once written as one hidden global state observed by many overlapping bounded-local predicates, it is essentially Goldreich random local functions / planted CSP, an established and actively studied cryptographic family.

**H3-E0:** implemented and rejected. If permutation-voltage transitions are public enough for an untrusted sender to lift paths, a public spanning-tree gauge attack recovers the hidden canonical cover up to one global sheet relabeling. If those transitions are hidden, the sender cannot evaluate the proposed forward operation.

**H3-E1:** naive attempt to adapt composite graph-cover cryptography to a public-key interface is rejected before code. Publishing the common-key base reveals decoding structure; hiding it prevents public encoding; sending only an unlabeled outer cover leaves an undefined public cover-projection search problem with no demonstrated trapdoor algorithm.

**H3-E:** may proceed only after defining a trapdoor positive cover distribution with a concrete efficient secret recovery algorithm.

**H2-H / H2.1:** rejected on the fixed generated instance by an exact industrial SAT attack. The exact {3,7} Klein-quartic/A5 relation encodes to 1,440 Boolean variables and 47,545 CNF clauses after fixing the global gauge. MiniSat returned SAT and the decoded assignment passed the repository's exact A5 verifier. On the recorded CI run it used 2,810,606 conflicts, 6,909,361 decisions, 172,452,978 propagations and about 115 CPU seconds. This is a concrete generated-instance break, not an asymptotic theorem; increasing genus or group size is not an acceptable repair.

**K0:** active non-orientable control. It uses an exact finite Klein-bottle triangulation and deliberately tests whether hidden local orientation labels are anything more than a Z2 gauge. The expected public attack is spanning-tree XOR normalization and recovery up to one global bit.

No security or post-quantum claim exists.

## Naming

MORPH-KEM is a working research name: Morse Obfuscated Reduction Path KEM.
