# MORPH-KEM

**MORPH-KEM** is exploratory public-key/post-quantum cryptography research based on discrete Morse theory, combinatorial topology, hyperbolic/non-orientable structures, and attack-first mathematical experimentation.

> **Research only. Not for production use. Not a security claim.**
>
> Do not use MORPH-KEM to protect real data, credentials, communications, or systems.

## Current status

**M0–M5, BTTS/Pachner calibrations T0–T1, and HGES controls G0–G6 are implemented and rejected. The H/Escher/covering and K0–K2.3 side tracks have also produced only negative results. No candidate primitive exists.**

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

The original ranking after prior-art/attack screening was:

1. **BTTS — Bounded Topological Transformation Search.**
2. **HGES — Hidden Gluing Equivalence Search.**
3. **HICQF — Hidden Intermediate Cover / Quotient Factorization.**
4. **CMPS — Coupled Monodromy–Postnikov Search**, still theoretical and without a trapdoor interface.

BTTS failed its first two generated-distribution calibrations, T0 and T1. HGES has now failed four controlled stages: G0 exposed tree-bridge decomposition; bridge-free G1 exposed every piece as an exact public `K4`; G2's stellar subdivision was publicly contracted back to the same fatal G1 macro relation; and G3 made local interfaces indistinguishable but thereby exposed a second accepted alternating perfect matching. None is positive hardness evidence.

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

## T1 — exact-distance Pachner calibration

T1 repairs T0's immediate generator defect by building complete canonical quotient BFS shells and selecting the target from an exact shortest-distance shell `S_D`. The target selection deliberately maximizes slack against the public tetrahedron-count lower bound and then minimizes capped shortest-path multiplicity.

**T1 is rejected by A-023 on the measured generated distribution.** Fixed Python 3.12 CI:

~~~text
t1-2: D=2, shells 1/8/31, ball 40, shortest paths 1,
      bidirectional 9/4 visited, 2 expanded

t1-3: D=3, shells 1/8/31/83, ball 123, target tet slack 2,
      shortest paths 1, bidirectional 9/14 visited, 5 expanded
~~~

The `t1-3` endpoint is genuinely at distance 3 and is not nearly certified by tetrahedron count, yet generic bidirectional recovery still needs only five quotient-state expansions. This triggers the pre-declared rejection condition. The project will not add depth 4 merely to inflate the work factor.

This remains a generated-distribution falsification, not an asymptotic theorem about Pachner reconfiguration.

See `docs/34-t1-distance-conditioned-results.md`.

## G0 — HGES canonical-gluing negative control

G0 deliberately uses a canonically decomposable gluing distribution: copies of one four-tetrahedron 3-ball are glued along a hidden tree, so every inter-piece shared face becomes a bridge in the public tetrahedron dual graph.

**G0 is rejected as designed by A-024.** The public attack builds triangle incidence, finds dual-graph bridges and recovers the bridge-block components without using the planted partition.

Fixed Python 3.12 `g0-8` baseline:

~~~text
public V/E/F/T:                    19/59/73/32
dual graph vertices/edges:         32/55
bridges:                           7
component sizes:                   4/4/4/4/4/4/4/4
face occurrence checks:            128
DFS edge scans:                    110
public witness accepted:           yes
matches planted partition:         yes
~~~

Across `g0-3`, `g0-5`, `g0-8` and eight deterministic seeds each, **24/24** public recoveries were accepted and matched the planted partition up to group order.

This validates the HGES decomposition-attack harness; it is not evidence for a hard problem.

See `docs/35-g0-hges-canonical-gluing.md`.

## G1 — bridge-free HGES clique-decomposition control

G1 removes G0's exact bridge shortcut by gluing the same allowed pieces in a simple cycle. The resulting public dual graph has no bridges and no articulation points.

**G1 is nevertheless rejected by A-028.** Each hidden four-tetrahedron piece remains an exact public `K4` in the tetrahedron dual graph. Enumerating four-vertex cliques, applying the exact allowed-piece predicate, and solving the induced exact cover recovers an accepted witness.

Fixed Python 3.12 `g1-12` baseline:

~~~text
public V/E/F/T:                    26/85/108/48
dual vertices/edges:               48/84
bridges / articulation points:     0 / 0
two-vertex separator pairs:        264
4-subsets tested:                  194580
dual K4 / allowed candidates:      12 / 12
exact-cover solutions:             1
exact-cover nodes/backtracks:      13 / 0
public witness accepted:           yes
matches planted partition:         yes
~~~

Across `g1-4`, `g1-8`, `g1-12` and eight deterministic public relabel seeds each, **24/24** public A-028 recoveries were accepted and **24/24** matched the planted partition up to group order.

The important negative result is structural: removing one canonical separator class did not hide the pieces themselves. Increasing the cycle size is not a repair.

See `docs/36-g1-bridge-free-clique-gluing.md`.

## G2 — stellar-subdivision HGES contraction control

G2 stellar-subdivides every G1 macro tetrahedron `1 -> 4`. A four-macro-tetrahedron G1 piece therefore becomes a sixteen-micro-tetrahedron public G2 piece. The old A-028 no longer directly returns a G2 piece partition, but every subdivision center has a public four-tetrahedron vertex-star signature.

**G2 is rejected by A-029.** The public attack recognizes those center stars, exact-covers the micro tetrahedra, contracts them back to the G1 macro complex, applies macro A-028, lifts the recovered partition, and passes the exact G2 verifier.

Fixed Python 3.12 `g2-8` baseline:

~~~text
public micro V/E/F/T:              50/185/264/128
micro dual vertices/edges:         128/248
bridges / articulation points:     0 / 0
two-vertex separator pairs:        112
candidate stellar centers:         32
false positives / misses:          0 / 0
center cover nodes/backtracks:     33 / 0
contracted macro V/E/F/T:          18/57/72/32
macro K4 / allowed candidates:     8 / 8
macro cover nodes/backtracks:      9 / 0
public witness accepted:           yes
matches planted partition:         yes
~~~

Across `g2-4`, `g2-6`, `g2-8` and eight deterministic seeds each, **24/24** public A-029 recoveries were accepted and **24/24** matched the planted partition up to group order; candidate-center false positives and misses were zero throughout the measured sweep.

The negative result is again structural: local refinement is not hiding when the representation exposes a public inverse that reconstructs an already-broken macro relation. More pieces or repeated stellar subdivision are not repairs.

See `docs/37-g2-stellar-contraction.md`.

## G3 — indistinguishable-edge HGES equivalent-matching control

G3 changes the piece family to a two-tetrahedron 3-ball and arranges the public tetrahedron dual graph as an even cycle. Every dual edge—whether planted internal or planted external—satisfies the same exact allowed-piece predicate, so the planted matching phase is not locally privileged.

**G3 is rejected by A-030.** The public attack enumerates exact perfect matchings of the allowed dual-edge graph. An even cycle has two alternating perfect matchings; both pass the exact public verifier, and one differs from the planted partition.

Fixed Python 3.12 `g3-8` baseline:

~~~text
public V/E/F/T:                    18/49/48/16
dual vertices/edges:               16/16
dual degree histogram:             ((2,16),)
bridges / articulation points:     0 / 0
allowed candidate dual edges:      16
vertex-star candidate pairs:       16
perfect matchings:                 2
matching nodes/backtracks:         17 / 0
accepted decompositions:           2
accepted non-planted:              1
~~~

Across `g3-3`, `g3-5`, `g3-8` and eight deterministic public relabel seeds each, all **24/24** instances expose exactly two accepted perfect-match decompositions, and in every instance exactly one accepted decomposition is non-planted. MRV matching recovery uses 7/0, 11/0 and 17/0 nodes/backtracks respectively and is stable under public relabeling.

The failure is structural but different from G1: local indistinguishability creates equivalent-witness multiplicity rather than inversion hardness. Scaling the even cycle is not a repair.

See `docs/38-g3-equivalent-matching.md`.

## G4 — coupled-phase HGES parity-collapse control

G4 couples the two public matching phases of many G3 gadgets through redundant pairwise XOR constraints. This is the first HGES control with explicit nonlocal coupling.

**G4 is rejected by A-031.** Public spanning-tree phase propagation and independent GF(2) elimination recover both accepted global phase assignments. On `g4-12`, the 18×12 system has rank/nullity `11/1`; the attack uses 72 row XORs and returns two accepted witnesses, one different from the hidden reference.

Across `g4-4`, `g4-8`, `g4-12` and eight deterministic seeds each, **24/24** instances have rank `g-1`, nullity 1, two accepted public solutions and one non-reference solution. The coupling is therefore binary synchronization/cohomology, not evidence of hardness.

See `docs/39-g4-coupled-phase-parity.md`.

## G5 — nonlinear exact-one HGES parity-projection control

G5 replaces G4's explicit XOR edges by signed ternary exact-one constraints over public two-phase G3 gadgets. The verifier is genuinely nonlinear, but every accepted clause still implies one public XOR equation.

**G5 is rejected by A-032.** On `g5-24`, the resulting 48×24 public affine system has rank/nullity `24/0`; Gauss-Jordan elimination uses 436 row XORs, recovers one phase vector, and that vector passes all 48 original nonlinear clause checks.

Across `g5-12`, `g5-18`, `g5-24` and eight deterministic seeds each, **24/24** public parity recoveries are accepted and match the hidden reference after post-attack comparison. DPLL/SAT is unnecessary because the cheaper affine projection is already fatal.

See `docs/40-g5-exact-one-parity.md`.

## G6 — affine-coset residual HGES control

G6 keeps G5's nonlinear exact-one verifier but deliberately reduces the rank of its public parity projection so two affine bits remain free. Every instance therefore exposes four public affine candidates rather than one.

**G6 is rejected by A-033.** On `g6-24`, the public 48×24 parity system has rank/nullity `22/2`; the attacker enumerates four affine candidates, performs 192 nonlinear clause checks, and exactly one candidate survives and passes the exact verifier.

Across `g6-12`, `g6-18`, `g6-24` and eight deterministic seeds each, **24/24** instances expose four candidates and exactly one accepted public witness. The residual dimension is constant, so scaling the gadget count is not a repair.

See `docs/41-g6-affine-coset-residual.md`.

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
- `docs/05-cryptanalysis.md` — compact canonical attack index and newest detailed attacks
- `docs/05-cryptanalysis-through-a024.md` — verbatim detailed attack ledger through A-024
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
- `docs/34-t1-distance-conditioned-results.md` — measured T1/A-023 result
- `docs/35-g0-hges-canonical-gluing.md` — measured G0/A-024 negative control
- `docs/36-g1-bridge-free-clique-gluing.md` — measured G1/A-028 negative control
- `docs/37-g2-stellar-contraction.md` — measured G2/A-029 negative control
- `docs/38-g3-equivalent-matching.md` — measured G3/A-030 negative control
- `docs/39-g4-coupled-phase-parity.md` — measured G4/A-031 negative control
- `docs/40-g5-exact-one-parity.md` — measured G5/A-032 negative control
- `docs/41-g6-affine-coset-residual.md` — measured G6/A-033 negative control
- `notes/research-log.md` — chronological record
- `spec/morph-kem-v0.1.md` — future-spec skeleton

## Next gate

The next controlled HGES experiment is **G7**, not a trapdoor construction. G6 showed that a cheap quotient may leave genuine ambiguity and still fail when the residual search dimension is constant.

G7 must make every known cheap quotient leave residual dimension growing with the generated instance, then attack that growing residual with exact CSP/SAT, local consistency, low-width dynamic programming, automorphism/normalization, equivalent-witness enumeration, and generated-role leakage tests.

Only an HGES distribution that survives these public attacks could justify asking whether a secret decomposition supplies a real recovery advantage with:

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
