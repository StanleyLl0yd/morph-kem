# MORPH-KEM

**MORPH-KEM** is exploratory public-key/post-quantum cryptography research based on discrete Morse theory, combinatorial topology, hyperbolic/non-orientable structures, and attack-first mathematical experimentation.

> **Research only. Not for production use. Not a security claim.**
>
> Do not use MORPH-KEM to protect real data, credentials, communications, or systems.

## Current status

**M0–M5 and the first T0 reconfiguration calibration are implemented and rejected. The H/Escher/covering and K0–K2.3 side tracks have also produced only negative results. No candidate primitive exists.**

Core M-series:

- **M0** — A-000 direct public coordinate recovery.
- **M1** — A-008 meet-in-the-middle path recovery.
- **M2** — A-014 structural hidden-core reconstruction.
- **M3** — A-016 collapse + spanning-tree equivalent witness.
- **M4** — A-018 public primal/dual tree-cotree witness.
- **M5** — irregular non-manifold 2-core with zero free collapses, but public tree-plus-extension search reaches an accepted equivalent Morse witness in 30 nodes on the fixed baseline.

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

- **K0:** Klein-bottle orientation data collapses to public Z2 gauge/cohomology.
- **K1:** exact non-orientable hyperbolic `N4:{6,4}_3` still exposes its orientation double cover and local gauge.
- **K2.0:** orientation-twisted `A5 ⋊ C2` is exactly ordinary `S5` transport.
- **K2.1:** crossed modules/strict 2-groups are established 2-type machinery; hidden higher gauge is not itself a trapdoor.
- **K2.2:** for `partial: Q8 -> Aut(Q8)`, fake-flatness factorizes into independent public face lifts. Four faces expose `2^4 = 16` equivalent witnesses.
- **K2.3:** genuine 3D kernel coherence also collapses exactly: residual face choices lie in `C2`, tetrahedral coherence is affine GF(2), and the boundary-of-4-simplex baseline exposes 64 equivalent witnesses.

## K2.4 topological hard-problem frontier

K2.4 broadened the search beyond one higher-gauge construction. It screened hard-problem candidates based on orientation, gluings, covering spaces, lift/projection, homotopy classes, fundamental groups, geodesics, hyperbolic and quotient spaces, non-local properties, equivalent embeddings, and hidden transformations between different representations of the same space.

Current ranking after prior-art/attack screening:

1. **BTTS — Bounded Topological Transformation Search**, using state-dependent reconfiguration paths as the first executable direction.
2. **HGES — Hidden Gluing Equivalence Search.**
3. **HICQF — Hidden Intermediate Cover / Quotient Factorization.**
4. **CMPS — Coupled Monodromy–Postnikov Search**, still theoretical and without a trapdoor interface.

The common abstraction for BTTS and equivalent embeddings is a **bounded path in an equivalence groupoid/reconfiguration graph**: local moves are state-dependent and compose only when their source/target representations match. This avoids assuming that every hidden transformation is a single global group action, but group-action reductions, canonicalization, low-width structure and bidirectional search remain mandatory attacks.

Orientation alone, hyperbolicity/geodesics alone, and hidden Tietze-presentation rewriting are not accepted as new hardness assumptions.

See:
- `docs/29-k2-topological-hard-problem-frontier.md`
- `docs/30-t0-bounded-pachner-spec.md`
- `docs/31-equivalence-groupoid-hardness.md`
- `docs/32-coupled-monodromy-postnikov-frontier.md`

## T0 — bounded Pachner calibration

T0 is the first executable BTTS experiment. Public endpoints are closed 3D simplicial states, vertex labels are quotiented by exact toy canonicalization, and witnesses are arbitrary legal state-dependent `2-3` / `3-2` Pachner paths within a public bound.

**T0 is rejected by A-022.** On the fixed Python 3.12 CI sweep:

~~~text
t0-4: planted 4, shortest 4, bidirectional expanded 13
t0-6: planted 6, shortest 6, bidirectional expanded 75
t0-8: planted 8, shortest 4, bidirectional expanded 13
~~~

For `t0-8`, BFS visits only 170 canonical states and bidirectional search visits 40/65 states from the two sides. The mean unique branching is 20 while only 17 of 1,821 tested move pairs commute, so the failure is not merely a fixed binary path or a mostly commuting product decomposition.

The result is a generated-distribution break, not a theorem that bounded Pachner search is easy. It establishes that **planted walk length is not a hardness parameter**.

See `docs/33-t0-pachner-results.md`.

## Research discipline

- Any equivalent accepted witness counts as attacker success.
- Generated distributions are part of the attack surface.
- Worst-case hardness is not average-case cryptographic hardness.
- Negative results are preserved.
- Structural breaks are redesigned, not repaired by larger parameters.
- Hyperbolic, non-orientable, higher-gauge, Escher-like, high-dimensional, or long-path are mathematical descriptions, never security arguments.
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
- `docs/29-k2-topological-hard-problem-frontier.md` — topological hard-problem screening
- `docs/30-t0-bounded-pachner-spec.md` — T0 design
- `docs/31-equivalence-groupoid-hardness.md` — reconfiguration/groupoid abstraction and fatal reductions
- `docs/32-coupled-monodromy-postnikov-frontier.md` — CMPS theory note
- `docs/33-t0-pachner-results.md` — measured T0/A-022 result
- `notes/research-log.md` — chronological record
- `spec/morph-kem-v0.1.md` — future-spec skeleton

## Next gate

The next executable experiment may be **T1 — distance-conditioned Pachner endpoint generation**, but it remains a falsification experiment rather than a trapdoor primitive.

T1 must sample endpoints by **measured shortest quotient distance**, not by generation-path length. It must report exact shell/ball growth, shortest-path multiplicity, bidirectional frontier size, canonical-state collisions, and move-interaction structure. Industrial bounded planning/SAT/CP-SAT attacks remain part of the gate.

Only if the reconfiguration relation itself shows meaningful generated-instance resistance may the project search for a trapdoor distribution with:

~~~text
(pk, td) <- TrapdoorGen(lambda)
y        <- PublicEval(pk, r)
w        <- TrapdoorRecover(td, pk, y)
Verify(pk, y, w)
~~~

The secret must give a recovery advantage that survives quotienting by all equivalent representations/witnesses.

No security or post-quantum claim exists.

## Naming

MORPH-KEM is a working research name: Morse Obfuscated Reduction Path KEM.
