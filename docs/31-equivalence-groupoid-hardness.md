# 31 — Equivalence groupoid / reconfiguration abstraction

## Status

This note extracts the common mathematical shape behind BTTS, equivalent embeddings, hidden gluings, and hidden transformations between different representations of one space.

It is a modeling abstraction, not a hardness or novelty claim.

## 1. From a group action to a groupoid

A standard hidden-transformation problem has the form

~~~text
find g in G such that g.x = y.
~~~

The same element `g` can act wherever the action is defined, so the transformation algebra is globally organized by a group.

Topological local moves are different.

A 2-3 Pachner move is defined only when the **current** triangulation contains the required local star/link. A Reidemeister move is defined only at a suitable local diagram pattern. A collapse is legal only when the current face is free.

Thus the natural category has:

~~~text
objects     = finite representations R
morphisms   = equivalence-preserving transformation sequences R -> R'
composition = concatenate compatible sequences
inverse     = reverse each reversible local move
~~~

This is a groupoid whenever the chosen elementary moves are reversible.

The cryptanalytic problem is then not necessarily `recover one global group element`; it is a **bounded path problem in the generated equivalence groupoid**, or equivalently in its reconfiguration graph after forgetting path labels.

## 2. Why this abstraction is useful

It cleanly separates three things that earlier MORPH models mixed together:

1. **equivalence:** which representations denote the same underlying object;
2. **local move calculus:** which certificates can transform one representation into another;
3. **cost:** move count, weighted move cost, maximum intermediate size, or another public bound.

A bounded search relation becomes:

~~~text
BEGP(R0, R1, L):
    find any morphism gamma: R0 -> R1
    with cost(gamma) <= L.
~~~

Attacker success is any such morphism.

BTTS is the Pachner/Reidemeister specialization of BEGP.

## 3. This is not automatically outside prior art

Groupoids and partial actions are standard mathematics, and group/groupoid actions are already being discussed as post-quantum cryptographic frameworks. Therefore the word `groupoid` does not create novelty or security.

Example frontier material:
https://summerschool-croatia.cs.ru.nl/2025/slides/2025-06-30-croatia.pdf

Local reconfiguration systems also have an established geometric theory. Abrams, Ghrist and Peterson associate cubical state complexes to local reconfiguration systems; CAT(0) structure can make their geometry highly tractable.

Reference:
https://doi.org/10.1016/j.aam.2005.08.009

This creates a new mandatory attack:

> Does the generated reconfiguration system secretly have median/CAT(0)/commuting-move structure that turns shortest path search into a normal-form problem?

## 4. Fatal reductions for BEGP

### 4.1 Global-action reduction

If every local move sequence has a compact normal form in a public group action, reduce BEGP to orbit/action inversion.

### 4.2 Independent commuting regions

If moves supported on disjoint regions commute and the state complex factors into a product, solve each factor separately and interleave the paths.

This is the reconfiguration analogue of the old MORPH coordinate-decomposition failure.

### 4.3 CAT(0) / median normal form

If the relevant state complex is CAT(0) with efficiently visible hyperplanes/normal cube paths, shortest or canonical paths may be efficiently recoverable.

### 4.4 Public potential function

If a public integer/vector potential decreases monotonically along every planted step, reverse generation is exposed by greedy descent.

### 4.5 Small separator / bounded width

If the dependency graph of move supports has small treewidth/pathwidth, dynamic programming or CSP decomposition may recover a path.

### 4.6 Bidirectional frontier collapse

Even without a global group action, small branching and low collision entropy can make bidirectional search cheap.

## 5. Non-locality requirement

A useful BEGP family must make the legality and consequences of local moves interact globally.

But `globally interacting` must be demonstrated quantitatively.

Record at minimum:
- move-support overlap graph;
- commuting-pair fraction;
- branching-factor distribution;
- duplicate/collision ratio in BFS frontiers;
- separator/treewidth proxies;
- shortest-path multiplicity;
- how far a local move perturbs radius-r signatures;
- whether a public potential correlates with distance to target.

A merely large state graph is not enough.

## 6. Relation to equivalent embeddings

An embedding/diagram/triangulation can have many finite descriptions.

If a complete local move calculus is known, equivalence search can be represented as BEGP:

~~~text
embedding representation E0
        | local isotopy / Reidemeister / bistellar generators
        v
embedding representation E1
~~~

This is preferable to using unrestricted ambient-isotopy or homeomorphism decision directly, because a bounded move sequence is an explicit efficiently checkable certificate.

## 7. Relation to gluings and quotients

Gluing problems can also be phrased groupoid-theoretically if local changes alter decompositions while preserving the quotient space.

This suggests a possible later hybrid:

~~~text
object = (piece decomposition, attaching maps, quotient triangulation)
move   = local decomposition/gluing transformation preserving quotient type
~~~

However, if a canonical JSJ/prime decomposition collapses all objects to one public normal form, the groupoid path ceases to be useful as a trapdoor source.

## 8. Relation to covers and lifts

A cover with fixed explicit projection is usually better viewed through monodromy/subgroup data than through BEGP. H3-E0 showed that changing fiber coordinates is gauge.

A cover enters BEGP only if the representation itself can be transformed through nontrivial local equivalences whose paths are not equivalent to public gauge normalization.

Therefore cover/lift problems remain a separate lower-ranked frontier until a concrete trapdoor distribution exists.

## 9. Quantum warning

Replacing a group by a groupoid does not establish post-quantum hardness.

The attack sequence is:

1. search for a hidden global group action or torsor quotient;
2. quotient obvious stabilizers/gauge;
3. search for periodic/translation structure on path labels;
4. test whether the residual problem embeds into hidden-subgroup/hidden-shift or known isomorphism-action frameworks;
5. only then treat the residual reconfiguration problem as distinct.

If no such structure is found, generic quantum search can still reduce exhaustive-search exponents and must be included in any eventual concrete-security estimate.

## 10. T0 consequence

T0 should be treated explicitly as a BEGP calibration.

The implementation should export not just `find_path`, but measurements that could falsify the entire abstraction early:

~~~text
branching distribution
commuting-move fraction
frontier collision ratio
bidirectional work
shortest path vs planted path
support-overlap graph
coarse potential correlation
~~~

If T0's move groupoid has an easy normal form or decomposes into weakly interacting regions, the result should be recorded as a structural break rather than repaired by a longer planted path.

## Security status

No security, one-wayness, average-case hardness, post-quantum hardness, KEM, IND-CPA, or IND-CCA claim exists.
