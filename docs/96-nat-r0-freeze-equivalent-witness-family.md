# 96 — NAT-R0 freeze of the equivalent-witness residual-representation family

## Status

**The current NAT residual-representation family is frozen as a cryptographic progression target.**

NAT7 through NAT10 exposed the same semantic failure under increasingly different publication models:

1. exact public residual data exposes the represented connection/representation;
2. lossy publication can hide the planted witness while leaving many verifier-accepted alternatives;
3. adding bounded noise can increase accepted-witness multiplicity instead of creating a binding inversion problem.

No novelty, one-wayness, post-quantum, KEM, signature, IND-CPA/CCA or production-security claim exists.

## The failure is semantic, not merely algorithmic

Earlier NAT stages failed for concrete algorithms such as local syndrome recovery, majority recovery, T-join decoding, quotient propagation and curvature support localization.

NAT9 and NAT10 show a deeper problem: even when those particular algorithms are no longer the whole story, the **public verifier itself** can make inversion too permissive.

For cryptographic use, hiding the planted witness is not enough. The attacker succeeds whenever it finds any candidate accepted by the public verifier.

If lossiness or noise transforms

```text
one planted witness
```

into

```text
hundreds / thousands / millions of cheap verifier-accepted alternatives,
```

then planted secrecy has not become a useful one-way relation.

## NAT7/NAT8 — exact connection publication

NAT7 showed that a public exact group-valued edge connection on a connected carrier can be normalized along a deterministic spanning tree. The normalized residual vector is gauge-invariant and public.

NAT8 strengthened this into an architectural closure:

- choose a deterministic spanning tree;
- each non-tree edge closes one public fundamental cycle;
- the tree-normalized residual on that edge is exactly the image of that free fundamental-group generator;
- there are `E-V+1` such public generator images;
- the original exact connection is reconstructible from the public tree gauge plus those residuals.

On a flat 2-complex, face relators simply impose public relations among the same already-visible generator images.

Therefore exact edge-label publication cannot hide the residual representation merely by calling it gauge/topology data.

## NAT9 — lossy finite-group observables

NAT9 stopped publishing exact residual elements and exposed only coarse `A5` cycle-type data on generators and short products.

This successfully hid the planted representation in the literal sense, but it did **not** create a binding public relation.

Across the measured set:

- public CSP recovery found a verifier-accepted representation on every instance;
- the first accepted representation was not the planted one;
- even the richest declared observable retained large numbers of accepted representations.

Thus lossiness created attacker freedom faster than it created search hardness.

## NAT10 — bounded-noise trace observables

NAT10 moved to genus-two `SL(2,p)` representations and noisy modular trace sketches with bounded radius.

Again, exact matrices were absent from the public instance. The attack used public trace-window filtering plus commutator/relator joins.

The result repeated NAT9 more strongly:

- public recovery succeeds throughout the declared toy set;
- planted-first recovery is absent;
- the verifier accepts very large numbers of quadruples;
- even after quotienting by simultaneous conjugation, rigorous lower bounds still leave many distinct accepted representation classes.

The noise therefore does not bind the witness. It expands the public equivalence class.

## Frozen changes

Do **not** continue this family by merely:

- increasing the finite target group or field size;
- increasing genus/dimension;
- publishing more words of the same cycle-type/trace form;
- shrinking or enlarging the same noise radius;
- demanding planted equality after public recovery;
- wrapping a harder generic CSP around the same permissive verifier;
- choosing parameters after measuring accepted-witness multiplicity.

Those do not address the semantic defect.

## Re-entry requirement: binding first

Any future NAT-like construction must define before implementation:

```text
PublicGen(params, seed) -> public instance P
WitnessGen(params, seed) -> planted witness w
Verify(P, candidate) -> bool
Equivalent(P) = {c : Verify(P,c)}
```

It must then predeclare how one of the following is measured or bounded:

- exact `|Equivalent(P)|`;
- equivalence classes modulo unavoidable public symmetry;
- rigorous lower/upper bounds on accepted multiplicity;
- stabilizer/transporter size in an action formulation.

A construction is rejected if making the publication lossy/noisy primarily increases `Equivalent(P)` while public search remains cheap.

## Preferred reformulation

The preferred direction identified by NAT-R0 is no longer

```text
recover any hidden decomposition / representation satisfying a permissive verifier.
```

Instead use an explicitly binding action relation:

```text
public X
secret action s
public Y = Apply(s, X)
recover any explicitly verifier-equivalent action X -> Y.
```

The stabilizer, action kernel and transporter multiplicity must be part of the public problem definition.

This recommendation led directly to HGA-0/HGA-R1 and the later HGA-R2 survey. It is a design constraint, not a claim that a suitable action has already been found.

## Preserved NAT corpus

Keep the NAT lineage as calibration evidence:

- NAT0 — local syndrome / repeated-sample controls;
- NAT1 — single-sample multi-error relation collapses to public T-join decoding;
- NAT2 — nonabelian `S3` relation collapses through its sign quotient and clean propagation;
- NAT3 — perfect-group `A5` removes abelianization but full nonabelian curvature localizes sparse noise;
- NAT4 — locally-flat deformation becomes a public gauge decomposition with huge equivalent-witness multiplicity;
- NAT5 — cycle-coupled noise still localizes by curvature;
- NAT6 — torus global holonomy reduces to a tiny/public representation problem and then direct algebraic recovery;
- NAT7/NAT8 — exact public connections expose gauge-invariant residual/free-generator images;
- NAT9 — coarse lossiness hides planted data but creates many accepted alternatives;
- NAT10 — noisy traces repeat the multiplicity failure even modulo conjugation.

Do not reinterpret these negative controls as security evidence.

## Research consequence

The NAT name may be reused only for a materially different, binding public relation. The exact/lossy/noisy residual-representation family itself should remain frozen.

No security claim.
