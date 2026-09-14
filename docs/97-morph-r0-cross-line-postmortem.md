# 97 — MORPH-R0 cross-line failure taxonomy and re-entry gate

## Status

MORPH-R0 is a **research postmortem and design gate**, not a primitive.

The project has now accumulated several mathematically different negative lineages:

- HGES / exact topology witnesses;
- HGA / action-recovery controls;
- NAT / noisy or residual representation relations;
- TDC / topology-derived sparse-code ensembles.

The purpose of this document is to record failure modes that recur **across** those lineages and to prevent the next construction from repeating them under a new geometric name.

No one-wayness, novelty, post-quantum, KEM, signature, IND-CPA/CCA or production-security claim exists.

## 1. Equivalent-witness failure

The planted secret is not the attacker target unless the public verifier makes it so.

The correct success condition throughout MORPH is:

```text
find any candidate accepted by the public verifier.
```

This principle invalidated several tempting interpretations:

- HGA1/HGA2 recovered actions need not match the planted word;
- HGA3 recovered conjugators need only lie on the valid public intertwiner line;
- NAT1 can succeed with a different minimum correction and different clean object;
- NAT4 admits huge families of gauge-equivalent decompositions;
- NAT9/NAT10 can hide the planted representation while making many alternative representations verifier-valid.

### Design rule

Every future proposal must define, before implementation,

```text
Equivalent(P) = {candidate : Verify(P, candidate)}
```

or the corresponding stabilizer/transporter quotient.

If noise, lossiness or quotienting mainly increases the size of `Equivalent(P)`, the construction is rejected even if the planted witness becomes hard to recognize.

## 2. Public canonicalization failure

Several apparently difficult inversion problems collapsed because public endpoints admit a canonical or nearly canonical reduction.

Measured examples include:

- Euclidean / continued-fraction reduction in HGA2;
- exact nullspace/intertwiner linearization in HGA3;
- graph/Schreier navigation in HGA-R1;
- tree normalization and fundamental-cycle extraction in NAT7/NAT8;
- quotient/fibre recovery in TDC2c.

### Design rule

Before a candidate is coded, explicitly test whether endpoint equality gives the attacker a canonical representative, normal form, spanning tree, quotient, shortest-path graph, module kernel or other deterministic connector.

A secret generation history is irrelevant if the public endpoints manufacture an accepted connector directly.

## 3. Low-dimensional and finite-quotient leakage

Nominally noncommutative or topological actions repeatedly leaked through simpler representations.

Examples:

- HGA0 linear translation control;
- HGA1 quotient-orbit plus MITM;
- HGA4d/e/f finite representation libraries;
- NAT2 sign quotient `S3 -> C2`;
- nonorientable/mapping-class ideas exposing homology of orientation or finite covers;
- `Out(F_n)` exposing the unavoidable `GL_n(Z)` action on abelianization.

### Design rule

Every new action candidate must list its cheap public representations before implementation:

- abelianization;
- sign/determinant/parity maps;
- finite quotients;
- homology/Prym representations;
- trace/character representations;
- permutation actions;
- low-dimensional matrix representations.

The attacker gets all of them for free.

## 4. Local topology can force bounded public witnesses

Topology can create structure that is beautiful mathematically and disastrous cryptographically.

Measured TDC examples:

- triangle boundaries produce weight-three codewords;
- tetrahedron boundaries produce weight-four codewords through `∂²=0`;
- suppressing those local boundaries merely moved the first visible relation to weight six;
- irregular expansion removed one symmetry leak while preserving topology-specific low-weight words.

### Design rule

A new cell/chain construction must search immediately for bounded-support relations implied by local incidence identities. Increasing the global complex size does not repair a constant-size public relation.

## 5. Lifts and relabeling do not automatically hide the quotient

Several constructions assumed that a generated base/fibre structure would become obscure after lifting and global relabeling.

TDC2c falsified this directly: public color refinement recovered exact fibres/base roles across the declared lift family.

Combinatorial cover theory also gives explicit monodromy/permutation-voltage descriptions, so cover isomorphism and automorphism structure are natural public attacks rather than hidden metadata.

### Design rule

Any cover/lift construction must include public base/fibre/monodromy recovery as a first-class attack. “The labels were permuted” is not a hiding argument.

## 6. Noise can collapse to polynomial graph optimization

Adding noise repeatedly failed to create genuine uncertainty when the syndrome lived in a public graph/complex.

Examples:

- NAT1 exact minimum T-join decoding;
- NAT2 sign-quotient T-join followed by clean propagation;
- local syndrome/majority controls in NAT0;
- curvature localization in NAT3/NAT5.

### Design rule

Before treating a noisy relation as difficult, attempt to reduce it to:

- matching / T-join;
- min-cut / flow;
- shortest paths;
- local propagation;
- belief propagation / bit flipping;
- sparse recovery;
- SAT/ILP with exact toy counts.

Noise is not an assumption by itself.

## 7. Generator failure is distinct from action failure

HGA4 produced an important methodological correction.

The Hurwitz/free-group action did not immediately collapse through the same polynomial/canonical mechanisms as HGA1–HGA3. Instead:

- the planted-word generator produced many non-geodesic histories;
- a self-avoiding generator could hit deterministic dead ends;
- exact-distance shell generation cost more than the attack it was meant to calibrate;
- finite representation filters later exposed leakage of the endpoint family itself.

### Design rule

Record separately:

```text
action-family failure
generator/distribution failure
verifier/equivalence failure
```

Do not call a bad generator evidence that the abstract action is easy, and do not rescue a bad generator by silently conditioning on attack output.

## 8. Matched controls and predeclared validation are mandatory

TDC3b/TDC3c show why this matters.

TDC3b initially produced an apparent topology-easier signal on `n10×8`. The predeclared `n10×32` extension reversed it, so the small-sample result was retained as a fluctuation rather than promoted.

TDC3c then found a different topology-easier window at a same-weight fixed Lee–Brickell checkpoint. Because that checkpoint rule was declared before measurement, it froze the current ensemble even though the all-weight aggregate was mixed and the strongest checkpoint slightly favored controls.

### Design rule

Every comparative experiment must declare before measurement:

- matched control family;
- dimensions/rank/rate/degree matching rules;
- seed horizon;
- mandatory validation slice;
- exact attack budgets;
- checkpoint aggregation/rejection rule.

Do not redefine the statistic after observing results.

## 9. No parameter rescue

A family that fails a declared structural gate cannot be restored merely by changing:

- sizes;
- weights;
- number of overlay constraints;
- attack budget;
- seed filtering;
- noise radius;
- lift factor;
- matched-control construction after the fact.

Those changes are useful only in a **new** family with a new stated mechanism explaining why the old attack no longer applies.

## 10. Screen of the original geometry inspirations

The original project intentionally explored visual/topological ideas such as Möbius strips, Klein bottles, Lobachevsky geometry and Escher-like impossible figures. They remain useful sources of mathematical questions, but visual novelty must be converted into an exact public relation before it has cryptographic meaning.

### 10.1 Möbius strip / nonorientable surfaces

A concrete cryptographic use would likely involve one of:

- the nonorientable fundamental group;
- its mapping class group;
- a nonorientable cell complex/code;
- the orientation double cover and associated monodromy.

The immediate attack surface is already strong. A connected nonorientable surface has a canonical orientation double cover, and the nonorientable mapping class group embeds in the mapping class group of that cover in broad settings. Nonorientable mapping-class groups also admit homological representations derived from covers, including arithmetic images in known constructions.

Recent geometric work shows the embedding into the orientation-cover mapping-class group can even be quasi-isometric. Thus nonorientability by itself does **not** hide the action from the orientable machinery already attacked in HGA/TDC.

References:

- T. Katayama and E. Kuno, *The mapping class group of a nonorientable surface is quasi-isometrically embedded in the mapping class group of the orientation double cover*, Groups Geom. Dyn. 18 (2024).
- B. Szepietowski, *Low dimensional linear representations of the mapping class group of a nonorientable surface*, 2013.
- F. Deniz and W. Singhof, *Representations of the mapping class group of a non-orientable surface*.

**MORPH-R0 verdict:** no candidate yet. A Möbius/nonorientable proposal must explain why the public orientation-cover and homological attacks do not recover or heavily prune the transporter.

### 10.2 Klein bottle

The Klein bottle is a genuine nonorientable manifold with a simple algebraic fundamental group. That simplicity is a warning rather than a benefit.

A construction based directly on its fundamental group or low-dimensional covers would immediately face:

- explicit group normal forms;
- abelian/solvable quotients;
- orientation-cover reduction to the torus;
- canonical conjugacy/word algorithms;
- low-dimensional homological actions.

**MORPH-R0 verdict:** the bare Klein-bottle group is better treated as a negative control than as a hardness source. A useful future role would be to test whether a proposed nonorientable harness rejects an obviously normal-form-friendly example.

### 10.3 Lobachevsky / hyperbolic geometry

Negative curvature is attractive because global geometry can be rich while local rules remain simple. But hyperbolic-group theory was built precisely to make many algorithmic problems tractable.

For large classes of hyperbolic and relatively hyperbolic groups there are effective geodesic/automatic structures and solvable word/conjugacy problems. Recent work continues to characterize when conjugacy remains decidable even in structured products of hyperbolic groups.

That means a naive proposal of the form

```text
secret = path/geodesic/group word in a hyperbolic object
public = endpoints
```

risks replaying HGA2: public geometry supplies a canonical or efficiently searchable connector.

Reference context:

- standard automatic/geodesic theory of hyperbolic groups;
- I. Bumagin, *The conjugacy problem for relatively hyperbolic groups*, 2004;
- M. Bridson, *On the conjugacy problem for subdirect products of hyperbolic groups*, Math. Ann. 395 (2026).

**MORPH-R0 verdict:** hyperbolic geometry remains mathematically interesting, but a candidate must identify a public relation whose inversion is **not** simply geodesic normal-form or conjugacy/navigation.

### 10.4 Escher / impossible figures / orbifold-style encodings

“Impossible figure” is not itself a mathematical hardness source. To become one, it must be encoded as something such as:

- an orbifold/fundamental-group presentation;
- a graph with local consistency constraints;
- a covering/monodromy problem;
- a tiling substitution system;
- a nontrivial holonomy representation.

Every one of those immediately lands in an already-known attack family:

```text
orbifold group           -> normal forms / linear or finite quotients
graph constraints        -> GI / CSP / SAT / local propagation
cover / monodromy        -> base/fibre recovery
holonomy representation  -> NAT7/NAT8 residual extraction and quotient attacks
tiling substitution      -> automaton / spectral / canonicalization analysis
```

**MORPH-R0 verdict:** Escher-like geometry is still a useful design metaphor for local/global incompatibility, but it becomes a candidate only after an exact relation is stated and survives the corresponding attack class.

## 11. Re-entry gate for any new MORPH family

Before a new implementation branch is created, require a one-page mathematical specification with these exact fields:

```text
1. PublicInstance
2. Secret/Witness or Action
3. Generation distribution
4. Public verifier
5. Attacker-success equivalence
6. Stabilizer / kernel / accepted multiplicity
7. Known quotients and representations
8. Canonicalization / navigation attack
9. Local-relation / low-weight attack
10. Noise-to-optimization attack, if noise exists
11. Cover/base/fibre recovery, if a lift exists
12. Matched weak/random control
13. Mandatory validation distribution
14. Quantum hidden-shift/HSP or other quantum screen
15. Reason this is not a renamed mature assumption
```

If the specification cannot state a concrete reason it avoids the major known failure classes, stop before code.

## 12. Trapdoor/KEM gate remains closed

A trapdoor or KEM interface is still premature.

No future branch should define `TrapdoorGen`, encapsulation or security notions until a public primitive has survived meaningful falsification under an explicit interface such as

```text
PublicGen
PublicEval
Recover / Invert attack suite
Verify
```

and its accepted-witness semantics are binding enough to make inversion meaningful.

The negative corpus is currently more valuable than a premature scheme.

No security claim.
