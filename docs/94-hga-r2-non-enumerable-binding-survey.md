# 94 — HGA-R2 non-enumerable binding-action survey

## Status

**HGA-R2 nominates no HGA-R3 implementation candidate.**

That is a positive outcome for the falsification process: after HGA-R1 rejected finite Markoff navigation, the next action family is not being chosen merely because it sounds more sophisticated. Every family screened below still exposes at least one of the failure classes that HGA-R2 was created to exclude.

No one-wayness, novelty, post-quantum, KEM, signature, IND-CPA/CCA or production-security claim is made.

## Mandatory HGA interface retained

Every future action candidate still has to define, before toy implementation,

```text
ObjectGen(params, seed) -> public X
ActionGen(params, seed) -> secret action s
Apply(s, X) -> public Y
VerifyAction(X, Y, candidate) -> bool
EquivalentActions(X,Y)
```

Attacker success is **any** verifier-accepted action in the declared equivalence class. The planted action is reference-only.

The candidate must additionally state or measure the stabilizer of `X`, the transporter from `X` to `Y`, the kernel of the represented action, cheap quotient representations, canonicalization cost and classical/quantum generic attack surface.

## Screen A — mapping-class actions through finite covers / Prym or homological representations

This was the most natural post-Markoff direction: retain topology, make the geometric object much larger than a finite Markoff orbit, and publish information derived from a finite cover or local system.

The literature gives a strong reason **not** to nominate this family yet.

Finite covers generate a large supply of explicit finite-dimensional representations of mapping class groups and `Out(F_n)` through their action on cover homology. These representations are not uniformly faithful, but they are powerful enough to expose substantial information about mapping classes. In particular:

- Hadari shows that every infinite-order mapping class on a surface with free fundamental group acts with infinite order on the homology of some finite solvable cover;
- work on higher Prym / homological representations studies arithmetic images and large linear quotients of mapping-class subgroups;
- Hadari's work on Johnson-filtration subgroups shows that individual finite-cover homological representations have large kernels, so simply choosing one cover does not give a clean binding action;
- recent work on twisted `SL_n` character varieties again reduces part of the mapping-class action to homology of canonical finite covers.

Thus a finite-cover endpoint risks landing directly in a tractable linear representation while still having a large kernel/stabilizer. That is exactly the bad combination for MORPH: public linear leakage plus uncontrolled equivalent actions.

Useful references:

- A. Hadari, *Every infinite order mapping class has an infinite order action on the homology of some finite cover*, 2015/2017.
- A. Hadari, *Separating subgroups of mapping class groups in homological representations*, 2019.
- I. Spiridonov, *On the mapping class group action on the homology of surface covers*, 2024.
- T. Lucas, *Homological representations of low genus mapping class groups*, Journal of Algebra 647 (2024).
- A. Larsen, *Mapping class group action on the cohomology of the `SL_n` character variety*, 2026, arXiv:2603.12484.

**HGA-R2 verdict:** no nomination. A future cover-based candidate would need a concrete reason why *all* efficiently computable homological/Prym representations fail to help transporter recovery, not merely an assertion that the full mapping-class group is nonlinear.

## Screen B — graph/surface covers with public monodromy or permutation-voltage data

A second possibility is to hide the action in a combinatorial cover rather than in homology.

This also fails the nomination screen in its obvious form. Finite graph covers admit concrete encodings by permutation-voltage assignments, and isomorphism/automorphism questions for covering projections have long been studied through exactly this data. Publishing enough cover structure for cheap equality also exposes base, deck and monodromy constraints that can be fed to canonicalization, graph-isomorphism and quotient-recovery attacks.

This is closely related to the TDC2c failure mode: global relabeling did not make the underlying quotient/fibres cryptographically hidden.

Reference:

- M. Hofmeister, *Isomorphisms and automorphisms of graph coverings*, Discrete Mathematics 98 (1991), 175–183.

**HGA-R2 verdict:** no nomination. A cover/monodromy construction must demonstrate a specific obstruction to public base/fibre recovery before it can be treated as a binding action candidate.

## Screen C — mapping-class actions on higher character varieties

Moving from finite Markoff surfaces to higher-genus character varieties removes the immediately tiny finite Schreier graph. The mathematics is rich and the action can be faithful in strong senses.

However, the current literature does not provide the binding property needed for a MORPH candidate.

Recent results show that generic mapping-class orbits on real, complex or p-adic character varieties can be dense or almost minimal, while other work proves faithfulness of actions on odd character varieties. These are strong dynamical statements, but **dense orbit is not a hard transporter problem**. For MORPH we still need:

1. a compact finite public encoding of endpoints;
2. cheap public equality/verifier semantics;
3. controlled stabilizer/transporter multiplicity;
4. no small trace/character/linear quotient that materially prunes the action;
5. no canonical path/navigation algorithm on the chosen discretization.

The obvious finite-field discretization returns to the HGA-R1 problem: one obtains a finite public orbit graph that can be navigated. The continuous/p-adic forms avoid finite enumeration but do not yet give a clean finite binding relation suitable for a toy cryptographic assumption.

Useful references:

- A. S. Golsefidy and N. Tamam, *Closure of orbits of the pure mapping class group in the character variety*, PNAS 122 (2025).
- J. Marché and M. Wolff, *Transitivity of normal subgroups of the mapping class groups on character varieties*, Groups Geom. Dyn. 19 (2025).
- Y. Bouilly, G. Faraco and A. Maret, *Mapping class group orbit closures for Deroin–Tholozan representations*, J. Mod. Dyn. 21 (2025).
- A. Daemi and C. Scaduto, *The mapping class group action on the odd character variety is faithful*, 2025, arXiv:2503.13350.

**HGA-R2 verdict:** no nomination. Large or dense orbit dynamics are interesting context, but they do not by themselves satisfy the HGA binding/transporter interface.

## Screen D — `Out(F_n)` / automorphism actions

Automorphism groups of free groups are a natural non-surface analogue of mapping class groups. They also have immediate quotient structure.

The standard abelianization map

```text
Out(F_n) -> GL_n(Z)
```

is unavoidable, and low-dimensional linear representations are strongly constrained by this quotient. Existing work also constructs additional finite-dimensional representations, including those coming from finite covers of graphs.

For a cryptographic action this means the first public attack would be exactly the HGA0/HGA3 lesson again: project the action into every cheap linear quotient and test whether the transporter is already mostly determined there.

Useful references:

- D. Kielak, *Outer automorphism groups of free groups: linear and free representations*, J. London Math. Soc. 87 (2013).
- X. Flamm, *Subrepresentations in the homology of finite covers of graphs*, Glasgow Math. J. (2023).

**HGA-R2 verdict:** no nomination. Nothing identified in this screen gives a concrete reason that the abelian/linear quotient would be irrelevant to transporter recovery.

## Screen E — nonabelian homogeneous/action spaces

Noncommutativity by itself is not enough. The historical HGA controls already demonstrated three distinct collapses:

- small finite orbit / MITM;
- canonical endpoint reduction;
- direct linear intertwiner recovery.

The broader group-action literature makes the same warning. Modern work on representations of group actions introduces quantitative linearity notions such as q-linear dimension and proves that several cryptographic assumptions fail when the action admits sufficiently small public linear representations. Surveys of noncommutative group-action cryptography likewise emphasize word-length and linear-representation attacks.

References:

- *Representations of group actions and their applications in cryptography*, Finite Fields Appl. 99 (2024), 102476.
- J. Zumbrägel, *Noncommutative Group Actions for Cryptography*, in *Finitely Presented Groups* (2024).

**HGA-R2 verdict:** no nomination without a concrete, testable non-linearity argument and explicit stabilizer/transporter control.

## Why HGA-R2 deliberately stops here

Issue #184 required a nominated HGA-R3 toy family to avoid all five of the following simultaneously:

1. small enumerable orbit;
2. cheap public canonical transporter;
3. low-dimensional linear recovery;
4. uncontrolled verifier-equivalent multiplicity;
5. an already-standard hard problem merely renamed without new structure.

The current survey found no family for which all five conditions can honestly be asserted with a concrete toy experiment.

The closest-looking directions each fail for a different reason:

```text
finite covers / Prym       -> rich public linear representations
cover monodromy            -> quotient/base/canonicalization attack surface
higher character varieties -> binding finite endpoint relation not yet defined
Out(F_n) actions           -> unavoidable GL_n(Z) and cover-linear quotients
class-group/isogeny        -> mature external assumptions, not MORPH novelty
```

Therefore **HGA-R2 makes no HGA-R3 nomination**.

## Re-entry rule

A future HGA-R3 proposal should begin as a one-page mathematical specification, not code, and must contain all of the following before a branch is created:

1. exact public object and finite encoding;
2. exact action representation and composition law;
3. exact verifier/equivalence relation;
4. explicit stabilizer/kernel expectation;
5. at least one known public representation/quotient and why it is insufficient;
6. a matched deliberately weak variant that the same attack harness should reject;
7. classical navigation/MITM baseline;
8. quantum HSP/hidden-shift screen;
9. a novelty statement distinguishing the relation from a renamed established assumption.

Until such a specification exists, HGA should remain paused rather than regress into parameter-driven experimentation.

No security claim.
