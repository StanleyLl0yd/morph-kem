# 15 — H1 signed holonomy experiment specification

## Status

H1 is the first executable experiment for the H-series.

It is not a KEM, not a trapdoor primitive, and not a security candidate.

Its goal is to answer:

> Does Möbius/Escher-like global holonomy produce any nontrivial search structure once obvious gauge and linear-algebra reductions are implemented?

## 1. Public object

H1 uses a finite connected 2-dimensional polygonal/cellular complex (X).

The first implementation does **not** need exact floating-point hyperbolic coordinates. Instead it records combinatorics chosen to mimic negative-curvature tilings:

- polygon face sizes (pge 5) where practical;
- vertex links with more local branching than Euclidean square/triangular grids;
- no privileged boundary if a finite quotient can be constructed;
- deterministic canonical cell ordering.

Each oriented edge carries a transition label.

## 2. Transition group ladder

H1 must deliberately begin with groups that are easy to attack.

### H1-Z2

[
G=mathbb Z_2.
]

Labels mean orientation preserve/reverse.

Expected result: complete reduction to XOR/cycle-space linear algebra.

This is a calibration model and is expected to fail.

### H1-S3

[
G=S_3.
]

Each edge maps a local three-state frame to a neighboring frame.

This is the first non-abelian toy.

Reasons for using (S_3):

- tiny enough for exhaustive verification;
- non-commutative;
- easy to serialize canonically;
- no claim that (S_3) itself is hard.

If H1-S3 is easy, that is a useful negative result.

## 3. Gauge equivalence

A vertex gauge assignment is

[
g:V	o G.
]

It transforms edge labels by

[
T_{uv}mapsto g(v),T_{uv},g(u)^{-1}.
]

Witnesses differing only by such a gauge are equivalent.

The validator must never require recovery of the planted gauge.

## 4. Cycle holonomy

For a closed walk (C):

[
H(C)=prod_{ein C}T_e
]

with orientation handled by inversion.

The public target is **not** a list of every planted cycle value.

Instead H1 should expose a verifier relation such as:

- satisfy selected face-cycle conjugacy classes;
- satisfy a bounded set of overlapping long-cycle relations;
- satisfy one global relation plus all local face constraints.

Exact choice must be fixed before parameter scaling.

## 5. Planned generator

Deterministically from a master seed:

1. construct a finite polygonal complex;
2. choose a hidden vertex frame assignment;
3. choose a set of local defect/frustration elements;
4. derive edge transitions;
5. apply a random public relabeling of cells/vertices;
6. discard generation history;
7. publish only canonical complex, group identifier, edge labels, and witness target relation.

The hidden frame assignment is retained only as a reference witness.

## 6. Mandatory attacks

### H-A01: Z2 cycle-space solve

For H1-Z2, construct the incidence/cycle matrix over GF(2) and solve exactly.

Expected outcome: H1-Z2 is rejected as a hardness candidate.

### H-A02: spanning-tree gauge fixing

Choose a public spanning tree.

Fix vertex gauges along the tree so all tree transitions become identity.

Measure how many independent non-tree transition variables remain.

### H-A03: abelianization

For non-abelian (G), map labels to the abelianization

[
G/[G,G].
]

Test how much of the witness leaks immediately.

For (S_3), this exposes a (mathbb Z_2) quotient.

### H-A04: cycle-basis reconstruction

Compute a fundamental cycle basis from a spanning tree and compare its holonomies with the public relation.

### H-A05: exact CSP

Treat each vertex frame as a variable in (G).

Use brute force / branch-and-bound first.

Record:

- variables;
- domain size;
- constraints;
- treewidth/separator proxies;
- nodes;
- equivalent witness count.

Only then consider SAT/SMT.

### H-A06: canonicalization / automorphisms

Canonicalize the unlabeled 1-skeleton and face incidence structure.

Check whether the generator leaves role-specific or quotient-specific signatures.

### H-A07: local statistical distinguisher

Compare vertex/edge roles by:

- degree;
- face-size multiset;
- triangle/polygon incidence;
- radius-2 and radius-3 neighborhood signatures.

No ML is needed until these baselines fail.

## 7. Exit criteria

H1 is rejected if any of the following holds:

- the complete relation linearizes;
- a spanning-tree gauge leaves independent cycle variables with easy reconstruction;
- exact CSP solves all toy instances with negligible branching;
- public canonicalization reconstructs planted coordinates;
- local role signatures separate secret structure.

H1 may proceed to H2 only if some non-abelian global coupling survives all of the above.

## 8. Hyperbolic geometry upgrade gate

Do **not** add exact Lobachevsky coordinates merely for visual or conceptual complexity.

Metric hyperbolic geometry is added only if it changes the search relation or blocks a concrete attack.

Possible H2/H3 upgrades:

- true finite quotients of ({p,q}) tilings;
- orientation-reversing quotient identifications;
- irregular hyperbolic polygonal complexes;
- non-manifold links;
- larger non-abelian transition groups;
- coupling holonomy constraints to an equivalent discrete-Morse witness.

## 9. Security status

No one-wayness, post-quantum, IND-CPA, IND-CCA, or concrete-security claim exists.

H1 is designed to fail cheaply if the Möbius/Escher/Lobachevsky intuition reduces to standard algebra.
