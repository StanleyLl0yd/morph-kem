# MORPH-KEM

**MORPH-KEM** is exploratory public-key/post-quantum cryptography research based on discrete Morse theory, combinatorial topology, hyperbolic/non-orientable structures, and attack-first mathematical experimentation.

> **Research only. Not for production use. Not a security claim.**
>
> Do not use MORPH-KEM to protect real data, credentials, communications, or systems.

## Current status

**M0–M5, BTTS/Pachner calibrations T0–T1, and HGES controls G0–G14 are implemented and rejected. The H/Escher/covering and K0–K2.3 side tracks have also produced only negative results. No candidate primitive exists.**

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

BTTS failed its first two generated-distribution calibrations, T0 and T1. HGES has now failed G0–G8: G0–G2 exposed canonical separator/motif/refinement structure; G3 exposed equivalent local decompositions; G4–G6 collapsed through parity/affine structure; G7 remained generic-SAT friendly even after the affine shortcut was removed; and G8 confirms the deeper architectural failure that G4–G7 factor exactly through an ordinary finite-domain CSP after cheap public local-phase extraction. None is positive hardness evidence.

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

## G7 — planted signed 3-SAT HGES control

G7 is the first control in the G4–G7 phase-coupling line whose local signed 3-OR predicate has no non-trivial affine GF(2) implication. That removes the direct parity shortcut, but not generic solver attacks.

**G7 is rejected by A-034.** On fixed Python 3.12 `g7-24`, public unit propagation + deterministic DPLL finds 16/16 capped accepted solutions in 40 nodes and 22 decisions; all 16 differ from the hidden reference. Across `g7-12`, `g7-18`, `g7-24` × eight deterministic seeds, all **24/24** instances yield an accepted public witness and an accepted non-reference witness, with at most 86 DPLL nodes in the measured sweep.

An independent MiniSat check on the fixed 24-variable/96-clause baseline reports SAT using 3 conflicts, 13 decisions and 41 propagations; the decoded model passes the exact repository verifier. This is generated-distribution evidence only, not a theorem about arbitrary 3-SAT.

See `docs/42-g7-planted-3sat.md`.

## G8 — topology-to-CSP collapse audit

G8 attacks the architecture shared by G4–G7 rather than another clause predicate. The public attacker independently enumerates each G3 gadget's two accepted local decompositions, compiles all global constraints to integer finite-domain relation tables, solves that topology-free CSP, and mechanically lifts assignments back to topological witnesses.

**G8 is rejected by A-035, and A-035 confirms a structural G4–G7 topology-to-CSP collapse.** Exhaustive Python 3.12 comparison checks 12,304 phase assignments across the smallest G4/G5/G6/G7 instances with **zero semantic mismatches** between the compiled CSP and the original HGES verifiers. On larger fixed baselines the generic solver needs 3 nodes/1 decision for G4–G6 and 38 nodes/22 decisions for G7; every recovered assignment lifts to an accepted original witness. A four-seed/four-family regression succeeds 16/16, with G7 requiring at most 100 generic-CSP nodes.

The solver serialization contains no tetrahedra, faces, vertices, simplicial labels, or witness groups. Topology survives only in a separate public lift table after the solve. Therefore choosing a harder CSP predicate over the same independently enumerable local domains is not additional topological hardness.

See `docs/43-g8-topology-csp-collapse.md`.

## G9 — overlapping-carrier HGES exact-cover control

G9 removes the independent local phase domains broken by G8. It publishes one connected tetrahedron-cycle complex whose allowed D2/D3 candidate pieces overlap directly in public tetrahedra.

**G9 is rejected by A-036.** Public candidate-subcomplex enumeration followed by exact cover finds 90, 224 and 450 accepted tilings for `g9-18`, `g9-24` and `g9-30`; an independent public cycle-composition DP obtains exactly the same counts. On `g9-30`, exact cover uses 2820 nodes / 899 backtracks and all 450 recovered covers verify, including 449 non-reference witnesses.

Across all three sets and eight deterministic seeds each, **24/24** instances reproduce the same break. Overlap by itself is therefore not enough when the candidate hypergraph is a bounded-width interval/cycle relation.

See `docs/44-g9-overlapping-exact-cover.md`.

## G10 — toroidal overlapping-pair HGES matching control

G10 replaces G9's interval/cycle candidate interaction with a closed periodic torus. Public candidate pieces are adjacent triangle pairs, so the dual interaction graph is genuinely two-dimensional and 3-regular.

**G10 is rejected by A-037.** The public dual graph is bipartite, and deterministic augmenting-path perfect matching directly constructs an accepted witness. Fixed `g10-8x8` has dual 128/192 and bipartition 64/64; the base attack uses 64 augmentations, 455 DFS calls and 770 edge scans. Forced-edge re-solving reaches the 64-solution cap, with 63 returned witnesses non-reference. Across all three sizes and eight seeds each, **24/24** public base matchings verify and every instance exposes an accepted non-reference decomposition.

The failure is structural: a two-dimensional overlap graph does not help when the relation itself is ordinary bipartite matching.

See `docs/45-g10-toroidal-matching.md`.

## G11 — toroidal P3 hypergraph exact-cover control

G11 moves beyond pairwise perfect matching by using three-triangle `P3` disks on the periodic torus. The resulting public relation is a genuine 3-uniform hypergraph exact-cover problem.

**G11 is rejected by A-038.** Fixed `g11-6x9` exposes 324 public candidates over 108 triangles; Algorithm-X-style MRV reaches 64/64 capped accepted covers in 292 nodes / 71 decisions / 10 backtracks, all non-reference. Across all three sizes and eight deterministic seeds each, **24/24** attacks reach cap 32 and every returned witness is accepted and non-reference.

An independent 324-variable / 3996-clause MiniSat encoding also returns an accepted non-reference cover, with 2 conflicts, 137 decisions and 574 propagations on the fixed baseline.

The graph-matching reduction is gone, but the regular periodic hypergraph is still easy and has massive equivalent-witness multiplicity.

See `docs/46-g11-toroidal-hypercover.md`.

## G12 — irregular-torus P3 hypercover control

G12 destroys G11's periodic local-role symmetry with many legal edge flips before reference-cover selection. The fixed `g12-8x9` carrier has nine primal degree classes, is dual-non-bipartite, exposes 82 public local signature classes, and has nonuniform P3 candidate memberships.

**G12 is rejected by A-039.** Public exact cover still reaches 64/64 accepted covers in 456 nodes / 119 decisions / 119 backtracks, all non-reference. Independent MiniSat solves the 408-variable / 4824-clause candidate hypergraph in about 0.005 s and its decoded witness passes the exact verifier. Across `g12-6x6`, `g12-6x9`, `g12-8x9` × eight seeds, **24/24** instances hit the 32-solution cap with every returned cover non-reference and no generation retries.

See `docs/47-g12-irregular-torus-hypercover.md`.

## G13 — random cubic-dual generator conditioning audit

G13 abandons torus ancestry and asks whether raw random pairings of oriented triangle sides can directly supply a healthy random simplicial-surface carrier.

**G13 is rejected by A-040 before any P3 relation is studied.** For each of 36, 54 and 72 triangles, 4096 fixed attempts plus eight independent 1024-attempt batches produce **0/12,288** honest simplicial surfaces. Pairings either contain a dual loop/parallel edge or, after those checks, collapse at least one quotient triangle. The per-size `3/N` scale after 12,288 zero-success attempts is `0.000244141`.

The project will not hide this behind unbounded rejection sampling. See `docs/48-g13-random-pairing-generator.md`.

## G14 — stacked-sphere reverse-normalization control

G14 uses guaranteed-valid random stacked/Apollonian 2-spheres to avoid G13's rejection-conditioned generator.

**G14 is rejected by A-041.** Public degree-three stellar-center contraction removes every stacking step and returns the tetrahedron boundary. On `g14-72`, 34/34 public reverse moves take `38/108/72` to `4/6/4`; up to 15 legal reverse candidates coexist. Across all three sizes x eight seeds, **24/24** carriers fully normalize, with exact move counts 16/25/34.

The failure is carrier-structural, so heavier P3 exact-cover/SAT is unnecessary. See `docs/49-g14-stacked-sphere-normalization.md`.

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
- `docs/42-g7-planted-3sat.md` — measured G7/A-034 negative control
- `docs/43-g8-topology-csp-collapse.md` — measured G8/A-035 structural collapse audit
- `docs/44-g9-overlapping-exact-cover.md` — measured G9/A-036 negative control
- `docs/45-g10-toroidal-matching.md` — measured G10/A-037 negative control
- `docs/46-g11-toroidal-hypercover.md` — measured G11/A-038 negative control
- `docs/47-g12-irregular-torus-hypercover.md` — measured G12/A-039 negative control
- `docs/48-g13-random-pairing-generator.md` — measured G13/A-040 generator-conditioning rejection
- `docs/49-g14-stacked-sphere-normalization.md` — measured G14/A-041 reverse-normalization rejection
- `notes/research-log.md` — chronological record
- `spec/morph-kem-v0.1.md` — future-spec skeleton

## Next gate

The next controlled HGES experiment is **G15**, not a trapdoor construction. G14 shows that guaranteed-valid constructive randomness is still useless when the construction exposes a bounded-local public inverse.

G15 must use a constructive non-toroidal carrier without degree-three stellar-center ancestry. A first control should start from a non-stacked sphere such as the icosahedral triangulation and apply a long deterministic legal bistellar/edge-flip mixing walk, then immediately attack public simplification, canonicalization, separator/treewidth structure, candidate extraction, exact cover/CSP/SAT, equivalent witnesses and generated-role leakage.

No trapdoor/KEM work begins before both carrier normalization and the witness relation survive these attacks.

No security or post-quantum claim exists.

## Naming

MORPH-KEM is a working research name: Morse Obfuscated Reduction Path KEM.
