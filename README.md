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

M5 is now being implemented on a parallel branch as an irregular non-manifold equivalent-witness experiment.

## H-series side track

A separate **H-series** studies the Möbius / Escher / Lobachevsky direction without changing the M-series conclusions.

Working research label:

**Hyperbolic Frustrated MORPH (HFM)**

The H-series investigates finite hyperbolic-like quotients and cell complexes with negative-curvature combinatorics, orientation-reversing gluings, overlapping holonomy, non-manifold junctions, local-to-global constraints, and equivalent-witness semantics.

Hyperbolic geometry, non-orientability, and holonomy are never treated as hardness assumptions by themselves.

## Research discipline

- Any equivalent accepted witness counts as attacker success.
- Generated distributions are part of the attack surface.
- Worst-case hardness is not average-case cryptographic hardness.
- Negative results are preserved.
- Structural breaks are redesigned, not repaired by larger parameters.
- No KEM wrapper until a primitive survives dedicated attacks.
- "Hyperbolic", "non-orientable", "higher-gauge", or "Escher-like" are mathematical descriptions, never security arguments.

## Key files

- `src/morph_kem/` — constructions and attacks
- `tests/` — exact validators and attack tests
- `scripts/` — deterministic baselines and sweeps
- `docs/05-cryptanalysis.md` — attack ledger
- `docs/13-m4-closed-surface.md` — M4 result
- `docs/14-h-series-hyperbolic-charter.md` — H-series prior-art/threat charter
- `docs/15-h1-holonomy-experiment.md` — H1 signed-holonomy result
- `docs/16-h2e-escher-atlas.md` — H2-E1 edge-gain Escher result
- `docs/17-h2e2-higher-atlas.md` — H2-E2 higher-order chart experiment
- `docs/18-h2e3-frontier.md` — Goldreich/local-OWF frontier and H3-E novelty gate
- `docs/19-h3e-lifted-atlas.md` — graph-cover gauge-normalization calibration
- `docs/20-h3e-composite-cover-frontier.md` — graph-cover public-key interface gate
- `docs/21-h2-klein-quartic-a5.md` — exact hyperbolic Klein-quartic/A5 experiment
- `docs/22-k0-klein-bottle.md` — non-orientable Klein-bottle orientation control
- `docs/23-k1-nonorientable-hyperbolic.md` — exact N4:{6,4}_3 hyperbolic non-orientable control
- `docs/24-k2-twisted-a5-semidir.md` — orientation-twisted A5 / S5 semidirect-product calibration
- `docs/25-k2-crossed-module-frontier.md` — crossed-module / finite-2-group prior-art and trapdoor gate
- `docs/26-k2-q8-crossed-module.md` — executable Q8 crossed-module fake-flatness result
- `notes/research-log.md` — chronological record
- `spec/morph-kem-v0.1.md` — future-spec skeleton

## Next directions

**M5:** irregular non-manifold 2-complexes, exact equivalent-witness search, CSP/SAT-style attacks, and incidence/canonicalization analysis.

**H1:** rejected. Z2 collapses by spanning-tree/cycle-space recovery; the S3 verifier collapses exactly to Z2 parity.

**H2-E1:** rejected. Relative-height Escher atlas is ordinary gain/cocycle structure and equivalent seam repair is cheap.

**H2-E2:** rejected. Pairwise-compatible NAE charts are a solver-friendly planted deletion-CSP with visible role leakage.

**H2-E3:** rejected before code. A naive all-charts hidden-state construction is Goldreich/random-local-function/planted-CSP structure.

**H3-E0:** rejected. Public permutation-voltage path lifting exposes the same graph cover up to global sheet gauge.

**H3-E1:** rejected before code. Naive composite-cover public-key adaptations either reveal the decoder structure or lack a trapdoor recovery algorithm.

**H2-H / H2.1:** rejected on the fixed generated Klein-quartic/A5 instance by exact industrial MiniSat; the decoded SAT model passes the repository verifier.

**K0:** rejected as designed. Exact Klein-bottle non-orientability leaves only public Z2 orientation obstruction plus one global gauge bit.

**K1:** rejected as designed. Exact non-orientable hyperbolic N4:{6,4}_3 still exposes the orientation double cover and all face gauge up to one bit.

**K2.0:** rejected algebraically. Orientation-twisted A5 is exactly `A5 ⋊ C2 ~= S5`, with zero predicate mismatches over all 43,200 tested endpoint assignments.

**K2.1:** frontier review completed. Crossed modules/strict 2-groups are established 2-type machinery and already have cryptographic prior art; hiding higher gauge is not a trapdoor.

**K2.2:** implemented and rejected. For `partial: Q8 -> Aut(Q8)` the exact structure is kernel/image/cokernel `2/4/6`. On N4:{6,4}_3 all four public face holonomies lie in the boundary image, each has exactly two Q8 lifts, and the verifier therefore exposes `2^4 = 16` equivalent fake-flat witnesses. A public attack constructs an accepted witness with only 24 edge compositions and 32 Q8 preimage checks, and its witness differs from the planted representative. Fake-flatness alone is therefore independent face lifting, not higher-order asymmetry.

The next K-series experiment must couple those face lifts through genuinely higher coherence. Since the remaining Q8 boundary ambiguity is the abelian kernel `C2`, the first successor attack must be a GF(2)/cohomology reduction; a genuine Postnikov-style coupling may require moving to a 3-complex, but only after an exact public/trapdoor interface is specified.

No security or post-quantum claim exists.

## Naming

MORPH-KEM is a working research name: Morse Obfuscated Reduction Path KEM.
