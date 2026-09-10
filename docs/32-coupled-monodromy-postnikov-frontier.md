# 32 — Coupled monodromy / Postnikov search frontier

## Status

This note preserves the strongest theoretical successor to K2.3 that is **not** merely a longer Pachner path.

It is not implemented and is not a hardness/security claim.

## 1. Motivation

K2.2 exposed independent face-lift ambiguity in

~~~text
partial: Q8 -> Aut(Q8).
~~~

K2.3 coupled those face lifts across tetrahedra, but the edge/`pi1` layer was effectively fixed. The only remaining unknown was the central kernel

~~~text
pi2 ~= ker(partial) ~= C2,
~~~

so the complete 3-cell condition became affine GF(2) linear algebra.

The natural next mathematical question is therefore:

> What if the non-abelian monodromy/`pi1` layer and the abelian `pi2` layer are both unknown and the Postnikov/coherence equations couple them?

This is the first higher-topological formulation that does not immediately reduce to `solve one public cochain system` by definition.

## 2. 2-type data

A connected homotopy 2-type can be described, up to the relevant equivalence, by data of the form

~~~text
G      = pi1
A      = pi2, an abelian group
rho    = action G -> Aut(A)
kappa  = Postnikov class in H^3(G; A_rho)
~~~

Crossed modules provide a strict algebraic model of this information.

The key structural warning remains: `A = pi2` is abelian. Nonlinearity can only come from the **coupling to unknown G-data**, not from pretending the second homotopy group itself is non-abelian.

Background already used by the project:
- polynomial-time/Postnikov algorithms in restricted fixed-dimensional regimes: https://arxiv.org/abs/1211.3093
- classical crossed-module/Postnikov reference recorded in `docs/25-k2-crossed-module-frontier.md`.

## 3. Candidate relation: CMPS

### Coupled Monodromy–Postnikov Search

Let `X` be a finite 3-dimensional cell/simplicial complex.

Unknown witness data consists schematically of:

~~~text
g_e in G    for oriented edges e
a_f in A    for oriented faces f
~~~

modulo the exact gauge/equivalence relation fixed by the model.

Public constraints enforce:

1. face boundary/curvature relations coupling incident `g_e`;
2. compatibility of `a_f` with the local `G` action `rho`;
3. tetrahedral coherence of the form

   twisted_delta_g(a) = kappa(g around tetrahedron)

   or an equivalent exact crossed-module/2-group identity;
4. selected global quotient/holonomy conditions if and only if they are efficiently verifiable.

The search problem is:

> find **any** gauge-equivalence class representative `(g,a)` satisfying all public relations.

The planted assignment is never privileged.

## 4. Why CMPS is not K2.3

K2.3 had a fixed public coefficient matrix:

~~~text
A z = b over GF(2).
~~~

In CMPS the effective linear operator on the `A` variables depends on unknown monodromy:

~~~text
D(g) a = b(g).
~~~

For a fixed `g`, the `a` layer may still be solved by module/cohomology linear algebra.

The possible difficulty lies in finding a globally consistent `g` for which the induced twisted system has a solution.

That makes the natural attack **hybrid elimination**:

~~~text
search / constrain g
    -> solve A-layer exactly for each partial/full g
    -> feed inconsistency back into G search
~~~

This is structurally closer to SAT+linear-algebra, code-with-group-action, or non-abelian synchronization with a module side condition than to an ordinary cohomology problem.

## 5. Immediate fatal reductions

### CMPS-A1 — fixed-G elimination

If the `G` edge variables can be recovered independently, solve the `A` layer afterwards by twisted cohomology/module linear algebra.

Then the higher layer provides no trapdoor.

### CMPS-A2 — pure-gauge monodromy

If generated `g_e` values arise only from hidden vertex frames, spanning-tree gauge fixing removes them exactly as in H1/H3-E0.

### CMPS-A3 — small-domain CSP

If `G` is a fixed small finite group and `A` is a fixed small module, the whole relation is a bounded-domain CSP on the incidence hypergraph.

Industrial SAT/SMT/CP-SAT becomes mandatory before interpreting failed custom search as hardness.

### CMPS-A4 — quotient/representation leakage

For every nontrivial quotient or low-dimensional representation of `G`, project the constraints and test whether the projected assignment can be recovered first.

H1 failed exactly this way through `S3 -> Z2`.

### CMPS-A5 — trivialized Postnikov class

If `kappa` becomes zero/coboundary on the generated monodromy subgroup, change variables to absorb the coupling and reduce to ordinary twisted cocycles.

### CMPS-A6 — module decomposition

Decompose finite `A` into primary/isotypic components and decompose the `G` action wherever possible.

If the witness relation factors over components, solve independently and recombine.

### CMPS-A7 — low-width incidence

The natural factor graph has edge variables, face variables and tetrahedron constraints. Treewidth/hypertree-width attacks are mandatory.

## 6. Public-key problem

CMPS can define an NP-style search relation if witness size and verification are bounded, but that is still not a trapdoor.

A trapdoor version would need an efficiently generated family where secret structural data makes the coupled system easy to solve for fresh public outputs.

Examples of **ideas to test, not assumptions**:

### Hidden decomposition trapdoor

Secretly generate `X` from pieces whose coupled systems are individually easy and whose boundary states can be joined efficiently with secret assembly data.

Public key exposes only a globally retriangulated equivalent representation.

Fatal question: does JSJ/canonical decomposition or canonical labeling recover the same piece structure?

### Hidden lift tower

Secret provides a tower of covers/quotients on which monodromy and module constraints split into smaller systems.

Public representation hides the tower.

Fatal question: can the tower be recovered as subgroup/block-system/monodromy factorization, or does publishing enough lift data reveal it directly?

### Hidden basis/module filtration

Secret basis makes the `G` action on `A` triangular/block structured.

Fatal question: this risks becoming code equivalence, module isomorphism, tensor isomorphism, or simultaneous conjugacy — all established group-action/isomorphism territory.

None of these currently passes the trapdoor gate.

## 7. Relationship to the user's topological ingredients

CMPS can genuinely combine several requested themes:

- **orientation:** as one component of the `G` action, but not the whole secret;
- **gluings:** determine how local coefficient systems are coupled;
- **covers / lift / projection:** change or split monodromy representations;
- **homotopy classes:** encoded by the underlying 2-type data;
- **fundamental group:** supplies `G` and its monodromy;
- **quotient spaces:** induce quotient/subgroup representations;
- **non-local properties:** global consistency only appears after combining many cells;
- **hidden transformations:** retriangulation/gauge changes alter presentation without changing the represented 2-type.

Geodesic/hyperbolic structure could be used to choose the base complex or supply canonical metrics, but is not needed to define CMPS and may help the attacker canonicalize it.

## 8. Why CMPS is not the immediate executable next step

There is not yet evidence that CMPS gives a useful generated average-case problem, and there is no trapdoor recovery algorithm.

By contrast, BTTS/T0 has:
- an exact elementary move relation;
- trivial positive-instance sampling;
- polynomial witness verification;
- recent worst-case complexity evidence;
- an obvious falsification harness.

Therefore the current priority remains:

~~~text
T0 / BTTS first
CMPS in parallel as a theory frontier
~~~

If T0 is trivially broken, CMPS remains available as a fundamentally different direction rather than responding by merely increasing Pachner path length.

## 9. Research gate before implementation

Do not implement a full CMPS generator until a paper specification can answer:

1. exact finite groups/modules `(G,A,rho,kappa)`;
2. exact orientation conventions and cell equations;
3. exact gauge-equivalence relation;
4. polynomial verifier;
5. generated positive distribution;
6. why public constraints do not determine `g` by synchronization;
7. best quotient/representation attacks on `G`;
8. linear elimination attack on `A`;
9. SAT/SMT factor-graph encoding;
10. candidate secret data and explicit `TrapdoorRecover` algorithm.

Without item 10 this is a hard-relation experiment, not a public-key primitive.

## 10. Security status

No one-wayness, average-case hardness, post-quantum security, KEM, IND-CPA, IND-CCA, or production-security claim exists.
