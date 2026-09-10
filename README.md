# MORPH-KEM

**MORPH-KEM** is exploratory public-key/post-quantum cryptography research based on discrete Morse theory, combinatorial topology, hyperbolic/non-orientable structures, and attack-first mathematical experimentation.

> **Research only. Not for production use. Not a security claim.**
>
> Do not use MORPH-KEM to protect real data, credentials, communications, or systems.

## Current status

**M0–M5 are implemented and rejected. The H/Escher/covering and K0–K2.3 side tracks have also produced only negative results. No candidate primitive exists.**

Core M-series:

- **M0** — A-000 direct public coordinate recovery.
- **M1** — A-008 meet-in-the-middle path recovery.
- **M2** — A-014 structural hidden-core reconstruction.
- **M3** — A-016 collapse + spanning-tree equivalent witness.
- **M4** — A-018 public primal/dual tree-cotree witness.
- **M5** — irregular non-manifold 2-core with zero free collapses, but a public tree-plus-extension search reaches an accepted equivalent Morse witness in 30 nodes on the fixed baseline.

The project does not interpret increasingly elaborate topology as security. Every new relation is attacked before scaling.

## H / Escher / covering results

- **H1:** S3 holonomy verifier factors exactly through Z2 parity.
- **H2-E1:** Escher relative-height atlas reduces to gain/cocycle cycle balance.
- **H2-E2:** higher-order NAE charts reduce to solver-friendly planted deletion-CSP; role leakage also appears.
- **H2-E3:** naive all-charts variant rejected pre-code as Goldreich/random-local-function/planted-CSP structure.
- **H3-E0:** hidden graph-cover fiber coordinates are public gauge after spanning-tree normalization.
- **H3-E1:** naive composite-cover public-key adaptation fails the public-evaluation/trapdoor interface gate.
- **H2-H/H2.1:** exact `{3,7}` Klein-quartic/A5 relation is broken on the fixed generated instance by exact MiniSat; the decoded SAT assignment passes the repository verifier.

## K-series results

The K-series tests non-orientable and higher-gauge variants.

- **K0:** Klein-bottle orientation data collapses to public Z2 gauge/cohomology.
- **K1:** exact non-orientable hyperbolic `N4:{6,4}_3` still exposes its orientation double cover and local gauge.
- **K2.0:** orientation-twisted `A5 ⋊ C2` is exactly ordinary `S5` transport.
- **K2.1:** crossed modules/strict 2-groups are established 2-type machinery; hidden higher gauge is not itself a trapdoor.
- **K2.2:** for `partial: Q8 -> Aut(Q8)`, fake-flatness factorizes into independent public face lifts. Four faces expose `2^4 = 16` equivalent witnesses.
- **K2.3:** the first genuine 3D coherence calibration also collapses exactly. Once one public lift per Q8 boundary fiber is chosen, the remaining face choices are `C2` bits and tetrahedral coherence is `A z = b` over GF(2). On the boundary of a 4-simplex the public matrix has 5 equations, 10 variables, rank 4, nullity 6, and therefore 64 equivalent witnesses. Gaussian elimination constructs an accepted non-planted witness in the measured CI baseline.

## Research discipline

- Any equivalent accepted witness counts as attacker success.
- Generated distributions are part of the attack surface.
- Worst-case hardness is not average-case cryptographic hardness.
- Negative results are preserved.
- Structural breaks are redesigned, not repaired by larger parameters.
- Hyperbolic, non-orientable, higher-gauge, Escher-like, or high-dimensional are mathematical descriptions, never security arguments.
- No KEM wrapper until a mathematical primitive survives dedicated attacks and has a complete public-evaluation/trapdoor-recovery interface.

## Key files

- `src/morph_kem/` — executable constructions and attacks
- `tests/` — exact validators and regression tests
- `scripts/` — deterministic baselines and sweeps
- `docs/05-cryptanalysis.md` — attack ledger
- `docs/21-h2-klein-quartic-a5.md` — exact hyperbolic/A5 experiment
- `docs/22-k0-klein-bottle.md` — Klein-bottle control
- `docs/23-k1-nonorientable-hyperbolic.md` — hyperbolic non-orientable control
- `docs/24-k2-twisted-a5-semidir.md` — A5/S5 flattening
- `docs/25-k2-crossed-module-frontier.md` — crossed-module prior-art/trapdoor gate
- `docs/26-k2-q8-crossed-module.md` — K2.2 fake-flatness result
- `docs/27-m5-irregular-nonmanifold.md` — M5 result
- `docs/28-k2-3d-kernel-coherence.md` — K2.3 3D/GF(2) result
- `notes/research-log.md` — chronological record
- `spec/morph-kem-v0.1.md` — future-spec skeleton

## Next gate

Do **not** continue by merely increasing genus, group order, cover degree, kernel size, or complex dimension.

A successor must begin with an explicit interface such as:

~~~text
(pk, td) <- TrapdoorGen(lambda)
y        <- PublicEval(pk, r)
w        <- TrapdoorRecover(td, pk, y)
Verify(pk, y, w)
~~~

and demonstrate why `td` gives an invariant recovery advantage on the generated positive distribution. Before implementation, the relation must be reduced against gauge/canonicalization, homology/cohomology, finite-module linear algebra, group synchronization, graph-cover recovery, and CSP/SAT/CP-SAT.

No security or post-quantum claim exists.

## Naming

MORPH-KEM is a working research name: Morse Obfuscated Reduction Path KEM.
