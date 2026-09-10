# 29 — K2.4 topological hard-problem frontier

## Status

K2.4 is a literature/design frontier after K2.3.

It is **not** a KEM, one-way function, trapdoor primitive, or security candidate.

The question is broader than the previous K-series experiments:

> Can a useful hard relation be formulated from global topology/geometry itself — orientation, gluings, coverings, lifts, homotopy, fundamental groups, geodesics, hyperbolic or quotient spaces, equivalent embeddings, or hidden transformations between representations — while retaining efficient public evaluation, efficient verification, and a real secret recovery advantage?

The repository answer at this stage is: **possibly, but only in sharply restricted reconfiguration/factorization relations. Most naive formulations collapse immediately to known algebra, canonicalization, solver problems, or an unusable undecidable problem.**

## 1. Non-negotiable cryptographic filter

A mathematical problem is relevant only if all four algorithms can eventually be defined:

~~~text
(pk, td) <- TrapdoorGen(lambda)
y        <- PublicEval(pk, r)
w        <- TrapdoorRecover(td, pk, y)
Verify(pk, y, w)
~~~

The generated distribution of `(pk,y)` is part of the problem definition.

Attacker success is **any** accepted equivalent witness. Recovering the planted coordinates, path, gluing, cover, or embedding is never required unless the verifier mathematically privileges it.

Worst-case NP-hardness, very large known upper bounds, or unrestricted undecidability do not establish cryptographic one-wayness.

## 2. Classification of the requested ingredients

| Ingredient | Standalone verdict | Potential useful role | First mandatory reduction |
|---|---|---|---|
| orientation | rejected | metadata/coupling only | `H^1(-; Z2)`, orientation double cover |
| gluings / attaching maps | promising with caution | hidden decomposition / quotient assembly | JSJ/canonical decomposition, boundary invariants |
| covering spaces | promising with strong caution | hidden intermediate factorization | subgroup/monodromy/block-system recovery |
| lift / projection | interface-sensitive | witness/recovery map | public lifting/gauge normalization |
| homotopy classes | restricted only | bounded equivalence witness | stable-range algorithms, normal forms, CSP |
| fundamental groups | weak standalone | algebraic shadow of topology | word/conjugacy/subgroup algorithms, Tietze prior art |
| geodesics | weak standalone | heuristic / canonical invariant | shortest/normal-form algorithms |
| hyperbolic spaces | scaffold only | force global geometry / expansion | rigidity, canonicalization, hyperbolic-group algorithms |
| quotient spaces | medium | hidden factorization/decomposition | group action, orbit/coset, HSP/hidden-shift |
| non-local properties | necessary but insufficient | prevents coordinate-local leakage | global invariants and decomposition |
| equivalent embeddings | promising as bounded search | reconfiguration witness | isotopy/Reidemeister/Pachner search |
| hidden transformations | strong meta-template | equivalence/reconfiguration relation | group-action/isomorphism/invariant-theory audit |

The important distinction is between a **geometric source of instances** and the **actual computational relation**. Hyperbolic geometry, non-orientability, or a complicated quotient can generate attractive objects while the relation itself remains XOR, subgroup search, graph isomorphism, SAT, or a public gauge choice.

## 3. Orientation

K0 and K1 already provide executable negative controls.

For the tested non-orientable surfaces, local orientation choices are a `Z2` gauge and the global obstruction is a public cohomological class. Passing from the Klein bottle to a genuine non-orientable hyperbolic regular map did not change that computational structure.

Therefore orientation cannot be the secret by itself.

A future construction may use orientation reversal only if it **acts nontrivially on another hard layer** and the combined relation does not split as a semidirect product, quotient bit, or orientation double cover. K2.0 already shows that the first obvious A5 twist simply completes to S5.

**Verdict: not a hard problem; potentially a coupling ingredient.**

## 4. Gluings and attaching maps

This is more promising because a global space can be assembled from locally ordinary pieces in many combinatorial ways.

### HGES — Hidden Gluing Equivalence Search

Public instance:

~~~text
piece library P1,...,Pm
allowed boundary types / attaching-map class
unlabeled quotient complex X
size bounds
~~~

Witness:

~~~text
gluing graph + boundary identifications +
certificate that the resulting quotient is equivalent to X
~~~

Attacker wins with any accepted gluing, not the planted one.

The main danger is **canonical decomposition**. Three-manifold topology has strong canonical splitting machinery such as JSJ decomposition, and hyperbolic pieces can be rigid enough that the geometry helps align pieces rather than hide them.

Sources:
- Neumann–Swarup, canonical JSJ decompositions: https://arxiv.org/abs/math/9712227
- hyperbolic 3-manifold homeomorphism has an explicit bounded algorithm: https://arxiv.org/abs/2108.00779

Before any generator is considered, HGES must be attacked with:
- JSJ / prime decomposition;
- boundary homology and peripheral subgroup data;
- canonical labeling of incidence graphs;
- automorphism groups of pieces;
- SAT/CP-SAT over boundary pairings;
- length/trace spectra when geometric structures are available.

**Verdict: second-best frontier candidate.** The hard part, if any, must survive canonical decomposition.

## 5. Covering spaces, lift and projection

Covering-space theory has a direct algebraic shadow: connected covers correspond to subgroups of the fundamental group. Hatcher's standard reference makes this correspondence explicit.

Source:
https://pi.math.cornell.edu/~hatcher/AT/AT-doublepage.pdf

Graph covering projection is also exactly a locally bijective homomorphism. Broad fixed-target `H-Cover` families are NP-complete.

Sources:
- https://arxiv.org/abs/2507.00564
- https://arxiv.org/abs/2502.20151

But this does **not** yet give a cryptographic trapdoor.

H3-E0 already shows the first failure mode: if edge transition/permutation-voltage data is public enough to lift paths, a public spanning-tree gauge recovers an equivalent cover representation.

H3-E1 shows the second failure mode: if the projection is omitted, both receiver and attacker face the same covering-projection search unless a separate secret recovery algorithm is proved.

### HICQF — Hidden Intermediate Cover / Quotient Factorization

Promise a factorization

~~~text
X -> Y -> B
~~~

while publishing only representations of `X`, `B`, degree constraints, and carefully selected invariants.

Witness is any valid intermediate `Y` and explicit maps.

This is interesting only if the hidden intermediate factor is not recoverable as:
- a subgroup chain of `pi1(B)`;
- a block system of a public monodromy action;
- a quotient of a public deck group;
- a graph-cover CSP;
- an orbit/hidden-subgroup problem.

The public-key question is especially severe: the sender must be able to evaluate without learning the secret factorization, while the receiver must exploit it to invert/recover something substantially faster.

**Verdict: mathematically natural but currently below BTTS/HGES because the trapdoor interface is missing.**

## 6. Homotopy classes

Unrestricted homotopy questions are too broad. Some regimes are polynomial-time computable, while dropping stability/connectivity restrictions can lead to undecidability.

Sources:
- polynomial-time fixed-dimensional/Postnikov computations: https://arxiv.org/abs/1211.3093
- homotopy classes in stable regimes and undecidability outside them: https://arxiv.org/abs/2104.10152

This is exactly why `homotopy is hard` is not a usable assumption.

A credible relation must be restricted so that witnesses have polynomial size, verification is polynomial, generated positive instances are efficiently sampleable, the secret gives a measurable advantage, and no stable-range/cohomological algorithm solves the generated distribution.

The most useful role for homotopy is therefore not `decide whether X ~ Y`, but **find a short explicit equivalence certificate under a fixed move calculus**.

That leads directly to BTTS below.

## 7. Fundamental groups and hidden presentations

Fundamental groups are useful because they capture global loop structure, covers, and quotient information. They are dangerous because many natural formulations become classical combinatorial group theory.

For hyperbolic groups, even compressed word and simultaneous-conjugacy problems have polynomial-time algorithms.

Source:
https://arxiv.org/abs/1808.06886

Mapping-class-group word problems also admit strong algorithms; a 2025 result gives `O(n log^3 n)` time for a compact surface.

Source:
https://arxiv.org/abs/2511.02459

Tietze transformations connect finite presentations of the same group. They are an obvious hidden-transformation mechanism, but they are not a fresh cryptographic foundation: group-cryptography literature already studies presentation/Tietze-based hiding, and GAP directly supports tracing generator images through Tietze transformations.

Sources:
- https://www.math.rwth-aachen.de/~Greg.Gamble/gap4r3/doc/htm/ref/CHAP046.htm
- https://shpilrain.ccny.cuny.edu/cryptogroups_survey.pdf

**Verdict: fundamental groups are valuable attack invariants and may participate in a coupled construction, but presentation obfuscation alone is not a new hard problem.**

## 8. Geodesics and hyperbolic spaces

Negative curvature often creates **more** algorithmic structure: thin triangles, contracting projections, normal forms, and rigid geometry.

The repository has already seen this lesson in H2-H: a true `{3,7}` hyperbolic Klein-quartic scaffold made naive search substantially harder, but the exact public relation still fell to SAT.

Further warnings:
- compressed decision problems in hyperbolic groups are polynomial-time in important cases: https://arxiv.org/abs/1808.06886
- hyperbolicity can support linear-time word solvers once a suitable structure is available: https://arxiv.org/abs/1905.09770
- closed hyperbolic 3-manifold homeomorphism is decidable by an explicit bounded algorithm: https://arxiv.org/abs/2108.00779

Geodesic distance itself is normally a **canonicalization/optimization tool for the attacker**, not a secret.

Potentially useful nonlocal quantities include a marked length spectrum, systems of interacting geodesics, or constrained geodesic laminations, but any such proposal must first show that it is not simply an isometry/group-conjugacy problem.

**Verdict: excellent source of rigid nonlocal geometry, poor standalone hardness assumption.**

## 9. Quotient spaces

A quotient can hide how local pieces are identified, but the moment the quotient is induced by a public group action, the relation risks becoming `find g such that g.x = y` or a related orbit/isomorphism problem.

That is a legitimate cryptographic template — code equivalence, lattice isomorphism, and isogeny constructions all use group-action ideas — but it is established territory rather than automatically new MORPH mathematics.

Current post-quantum research continues to build on isomorphism/group-action assumptions, and invariant-theoretic attacks explicitly target hidden transformations by removing easy action components and solving for the residual transformation.

Examples/frontier:
- https://pqcrypto.cs.ru.nl/ampqc/abstracts.html
- https://link.springer.com/article/10.1007/s12095-026-00879-x

Quantum analysis must immediately ask whether a proposed quotient/orbit problem reduces to hidden subgroup, hidden shift, period finding, or another Fourier-sampling structure.

**Verdict: usable only if the action is genuinely different from a standard efficiently describable group action and survives invariant decomposition.**

## 10. Non-local properties

`Non-local` is a design requirement, not a hardness assumption.

A property may depend on the whole space and still be cheaply computable: Euler characteristic, orientability, homology, cycle-space syndrome, canonical JSJ graph, or a public monodromy representation.

The project should require two separate tests:

1. **local indistinguishability:** no bounded-radius signature reveals planted roles;
2. **global computational resistance:** no canonical invariant/decomposition reconstructs an equivalent witness.

M2 and H2-E2 show why both are necessary: a globally described problem can still leak planted roles or admit a simpler global reconstruction.

## 11. Equivalent embeddings

This is one of the stronger directions because the public objects can be known equivalent while the certificate of equivalence is a reconfiguration path.

The unrestricted embedding problem is too broad and can enter undecidable regimes. That is not useful cryptographic evidence.

A better formulation is bounded transformation search between **low-dimensional finite representations**.

Knot theory gives concrete complexity evidence:
- bounded Reidemeister transformation problems are NP-hard / NP-complete: https://arxiv.org/abs/1809.10334
- bounded unknotting by Reidemeister moves is NP-hard: https://arxiv.org/abs/1810.03502

Most importantly for MORPH, a 2026 result proves NP-hardness of a bounded bistellar-move problem between triangulations of the 3-sphere, giving the first NP-hardness result for moves between triangulations of a 3-manifold:

https://arxiv.org/abs/2606.14413

This is the strongest current reason to test a topological reconfiguration relation rather than another gauge system.

## 12. Hidden transformations between representations

This is the broad meta-template:

~~~text
R1 = tau(R0)
~~~

with `tau` hidden and verification performed by replaying/validating a transformation certificate.

There are two fundamentally different cases.

### Case 1 — transformations form an efficiently represented group action

Then the problem is an isomorphism/action problem. Mandatory attacks include invariants, stabilizers/orbits, decomposition into easy subactions, canonical representatives, hidden-shift/HSP analysis, and meet-in-the-middle if words in generators are exposed.

### Case 2 — transformations are state-dependent local rewrites

Examples: Reidemeister, Pachner/bistellar, elementary collapses/expansions, local retriangulations.

There is no single fixed group element acting independently of state. The natural object is a **reconfiguration graph** whose vertices are representations and edges are legal local equivalence moves.

This is currently the more promising branch.

## 13. Candidate A — BTTS

### Bounded Topological Transformation Search

Let `Rep` be a class of finite representations and `Move(R)` the finite set of legal local equivalence-preserving moves from state `R`.

Define:

~~~text
BTTS(R0, R1, L):
    find any sequence (m1,...,mt), t <= L,
    such that mi is legal at the current state and
    mt(...m2(m1(R0))...) = R1
~~~

Equality is canonical encoded equality after vertex/cell relabeling normalization specified by the experiment.

The relation is in NP whenever each move and endpoint comparison are polynomial and `L` is polynomially bounded.

### Why this differs from M1

M1 used two **public, globally invertible** permutations at every layer. Every reverse branch was syntactically valid, giving generic `2^(ell/2)` MITM.

BTTS instead requires the legal move set to depend on the current triangulation, branching factors and available inverse moves to vary by state, many paths to merge at the same representation, attacker success to include every path within the bound, canonicalization after moves so labels cannot carry the planted route, and generation not to expose a monotone reverse trail.

This does not remove bidirectional search; it makes it a mandatory measured attack rather than an automatic fixed binary decomposition.

### Generator for T0

The first T-series calibration should use a small triangulated 3-manifold family.

1. sample a canonical base triangulation `R0`;
2. apply a deterministic-seeded sequence of legal bistellar/Pachner-style moves, recording the route;
3. reject paths with obvious immediate cancellation or monotonically recognizable reverse markers;
4. canonical-relabel the endpoint `R1`;
5. publish `(R0,R1,L)` with `L` at least the planted length;
6. attacker wins by any legal path of length <= L.

T0 is **not** a trapdoor experiment. It asks only whether the generated endpoint distribution has any nontrivial reconfiguration-search resistance.

### Mandatory T0 attacks

- exhaustive BFS at tiny sizes;
- bidirectional BFS / frontier intersection;
- meet-in-the-middle with canonical states;
- A* / IDA* using simplex-count and degree-profile lower bounds;
- greedy simplification/retriangulation;
- random walks / restart search;
- automorphism-aware canonical hashing;
- SAT/CP-SAT bounded planning encoding;
- path multiplicity and collision measurement;
- compare planted path length to shortest recovered path.

If these attacks recover short paths routinely, BTTS is rejected before any trapdoor attempt.

## 14. Candidate B — HGES

HGES uses gluings rather than a move path. Its attraction is that local pieces can be individually non-distinguishing while only the global attachment pattern determines the quotient.

Its central risk is the opposite: topology often supplies canonical decompositions that reconstruct the assembly graph.

A first HGES experiment should therefore use a piece family for which the canonical decomposition is intentionally known and then verify that the attack harness recovers it. Only later should it attempt a noncanonical overlapping decomposition.

Ranking: **second**.

## 15. Candidate C — HICQF

Intermediate covers/quotients naturally combine covering spaces, lifts/projections, fundamental groups, quotient spaces, and hidden transformations.

But they also naturally expose subgroup and monodromy structure. Connected covers correspond to subgroups of `pi1`, so a public explicit projection gives the attacker a powerful algebraic representation of the same object.

Ranking: **third until a real TrapdoorRecover algorithm is found**.

## 16. Candidate D — HHEE

Hidden Homotopy / Embedding Equivalence is best viewed as a generalization of BTTS.

The safe version is not `are R0 and R1 equivalent?`, but `find a polynomial-size certificate in a fixed low-dimensional move system`.

Reidemeister moves for knot diagrams and Pachner moves for triangulations provide concrete calculi.

Ranking: **merge into BTTS for the first executable research phase**.

## 17. Candidate ranking

| Rank | Candidate | Research value | Main blocker |
|---:|---|---|---|
| 1 | BTTS / bounded Pachner-reconfiguration search | high | planted random paths may be easy; no trapdoor yet |
| 2 | HGES / hidden gluing equivalence | medium-high | canonical decomposition may reveal assembly |
| 3 | HICQF / intermediate cover-quotient factorization | medium | subgroup/monodromy recovery + public-eval dilemma |
| 4 | HHEE as a separate family | medium | mostly subsumed by BTTS; unrestricted forms unusable |
| — | orientation alone | reject | linear/cohomological |
| — | hyperbolicity/geodesics alone | reject | often aid normal forms/canonicalization |
| — | hidden Tietze presentation alone | reject as novelty | established group-theoretic/prior-art territory |

## 18. Mandatory cross-cutting attacks after T0/T1

The original K2.4 draft reserved A-022 through A-026 before executable T-series experiments existed. T0 and T1 now occupy A-022 and A-023 with concrete bidirectional Pachner attacks. The remaining cross-cutting attack IDs are therefore realigned here to avoid collisions.

### A-024 — canonical decomposition / gluing recovery

Try to recover a canonical or near-canonical decomposition before searching the planted representation.

Targets: HGES, quotient spaces, equivalent embeddings.

The first executable instance is G0, where public tetrahedron-dual bridges recover the planted punctured-4-simplex blocks exactly on the measured distribution.

### A-025 — cover/subgroup/monodromy factorization

Translate public cover data into `pi1` subgroups, permutation actions, block systems, deck groups, or locally-bijective-homomorphism CSPs.

Targets: HICQF and any lift/projection proposal.

### A-026 — normal-form/geodesic/mapping-class canonicalization

Use negative-curvature and surface structure against the construction: normal forms, shortest representatives, curve complexes, mapping-class algorithms, geometric rigidity.

Targets: hyperbolic/geodesic and gluing proposals.

### A-027 — group-action / hidden-shift quantum reduction

Before claiming post-quantum relevance, determine whether hidden transformations define a group action amenable to hidden subgroup/hidden shift/period-finding style quantum algorithms or known group-action attacks.

Targets: all hidden-transformation and quotient-space candidates.

## 19. Decision

K2.4 does **not** identify a cryptographic primitive.

It identified BTTS as the first falsification experiment. T0 and T1 subsequently rejected the first two generated Pachner distributions, so the executable frontier has moved to HGES.

G0 is deliberately a negative control for the HGES attack harness: its canonical bridge decomposition must be recoverable publicly. Only after that control succeeds may G1 remove the exact bridge shortcut and test richer separator/decomposition attacks.

The critical methodology remains:

~~~text
old approach:
  invent secret topology -> hope inversion is hard

new approach:
  choose an explicit equivalence-search relation
  -> measure generated-instance hardness
  -> then search for a trapdoor distribution
  -> only then discuss public-key construction
~~~

## 20. Security status

No one-wayness, average-case hardness, post-quantum hardness, IND-CPA, IND-CCA, KEM, or production-security claim exists.
