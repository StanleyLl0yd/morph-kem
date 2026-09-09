# 14 — H-series hyperbolic / non-orientable research charter

## Status

H0 is a research charter and prior-art map. It does **not** define a cryptographic primitive.

Working label: **Hyperbolic Frustrated MORPH (HFM)**.

The motivating ideas are:

- Möbius-style non-orientability: local neighborhoods can look ordinary while a global loop reverses orientation;
- Escher-style frustration: locally admissible pieces can participate in globally nontrivial consistency conditions;
- Lobachevsky / hyperbolic geometry: negative curvature creates rapid combinatorial growth and rich finite quotient structures.

These are sources of mathematical structure only. None is a security claim.

## 1. What is already standard

### Hyperbolic surfaces and tilings

Finite-genus hyperbolic surfaces admit rich tessellation theories, including canonical/Delaunay-type decompositions and flip algorithms.

Relevant prior art:

- Jason DeBlois, *Tessellations of hyperbolic surfaces*, 2011:
  https://arxiv.org/abs/1103.4604
- Carl O. R. Lutz, *Canonical tessellations of decorated hyperbolic surfaces*, 2022:
  https://arxiv.org/abs/2206.13461
- Vincent Despré, Jean-Marc Schlenker, Monique Teillaud, *Flipping Geometric Triangulations on Hyperbolic Surfaces*, 2019:
  https://arxiv.org/abs/1912.04640

Consequence for MORPH:

> A hidden tessellation or gluing is not automatically hidden merely because it lives on a hyperbolic surface. Canonicalization and flip-normalization are immediate attack classes.

### Non-orientable hyperbolic tilings

Hyperbolic tiling theory already covers finite-genus surfaces that may be non-orientable, punctured, or have boundary.

Relevant prior art:

- Benedikt Kolbe, Myfanwy E. Evans, *Isotopic tiling theory for hyperbolic surfaces*, 2020:
  https://link.springer.com/article/10.1007/s10711-020-00554-2

Consequence:

> Möbius-like orientation reversal is useful as a constraint, but non-orientability itself is a standard, efficiently recognizable topological property and cannot carry the secret by itself.

### Finite quotients are standard machinery

Finite hyperbolic tilings can be obtained from quotient/compactification constructions. Related quotient machinery is routinely used in hyperbolic surface-code constructions and other combinatorial settings.

Relevant examples:

- David Futer, Anne Thomas, *Surface quotients of hyperbolic buildings*, 2010:
  https://arxiv.org/abs/1007.5140
- Oscar Higgott, Nikolas P. Breuckmann, *Constructions and Performance of Hyperbolic and Semi-Hyperbolic Floquet Codes*, PRX Quantum 2024:
  https://doi.org/10.1103/PRXQuantum.5.040327

Consequence:

> "Take a regular hyperbolic tiling and quotient it secretly" is not enough. The quotient description, automorphisms, homology, or group presentation may expose a simpler recovery problem.

## 2. Hyperbolic-group warning

The H-series must not rely on a generic claim that word or conjugacy problems in hyperbolic groups are difficult.

Relevant algorithmic results include:

- David Buckley, Derek Holt, *The conjugacy problem in hyperbolic groups for finite lists of group elements*, 2011:
  https://arxiv.org/abs/1111.1554
- Inna Bumagin, *Time complexity of the conjugacy problem in relatively hyperbolic groups*, 2014:
  https://arxiv.org/abs/1407.4528
- Derek Holt, Sarah Rees, *The compressed conjugacy problem in relatively hyperbolic groups*, Journal of Algebra 2024:
  https://doi.org/10.1016/j.jalgebra.2024.03.009

These works give efficient algorithms in substantial hyperbolic/relatively-hyperbolic settings.

Therefore HFM explicitly excludes as its intended hardness source:

- ordinary word problem;
- ordinary conjugacy search in a standard hyperbolic group;
- shortest geodesic normal form by itself;
- a simple hidden surface-group presentation.

## 3. Four layers that must remain separate

### Geometric layer

A metric or combinatorial approximation to negative curvature.

Examples:

- {p,q}-type local polygon incidence;
- variable-curvature polygonal complexes;
- finite quotients or finite patches with identified boundaries.

This layer creates growth and local symmetry, but not automatically hardness.

### Topological layer

Global topology:

- orientability;
- genus / Euler characteristic;
- homology/cohomology;
- non-manifold singular strata;
- covering-space structure.

These are mostly attack-visible invariants and should not directly encode the secret.

### Transition / holonomy layer

Every oriented adjacency carries a local state transformation:

[
T_{uv}in G
]

for a small chosen transition group (G), with

[
T_{vu}=T_{uv}^{-1}.
]

For a closed walk

[
C=(v_0,v_1,ldots,v_k=v_0)
]

define holonomy

[
H(C)=T_{v_{k-1}v_k}cdots T_{v_0v_1}.
]

The intended "Escher" effect is:

- each local transition is valid;
- many overlapping cycles exist;
- globally the cycle holonomies impose coupled constraints.

### Witness layer

The witness must be a global object accepted up to equivalence.

Candidate witness components:

- local frame/state assignment;
- gauge transformation;
- selected transition corrections;
- discrete-Morse matching;
- global reduction certificate.

The public verifier must accept any mathematically equivalent witness, not one planted encoding.

## 4. First fatal reductions to test

### A-H01 — Z2 orientation linearization

If every transition is only "preserve/reverse orientation", then:

[
T_ein mathbb Z_2
]

and cycle consistency becomes XOR parity.

That is linear algebra over GF(2).

**Rule:** orientation parity alone is rejected as a hardness source.

### A-H02 — abelian holonomy linearization

If (G) is a small abelian group, cycle constraints can often be represented by a cycle basis and solved using linear algebra or Smith normal form.

**Rule:** H1 must explicitly implement this attack before interpreting any search cost.

### A-H03 — spanning-tree gauge fixing

For a connected graph/1-skeleton, a gauge can often be fixed along a spanning tree, leaving only cycle-edge degrees of freedom.

This may reduce a visually huge complex to roughly:

[
|E|-|V|+1
]

independent cycle variables.

**Rule:** report the dimension after tree gauge fixing.

### A-H04 — homology/cohomology collapse

If the accepted witness depends only on a first cohomology class, then the problem may collapse to standard boundary/coboundary matrices.

**Rule:** compute chain-complex ranks and compare witness information to (H^1).

### A-H05 — canonical quotient / isomorphism recovery

If all local patches are regular, the quotient may have enough symmetry for canonical labeling, automorphism, or tiling-normalization algorithms to recover the intended coordinates.

**Rule:** role labels and generator history are adversarially visible through every invariant the public complex exposes.

### A-H06 — ordinary hyperbolic-group algorithms

If the "secret holonomy" can be rewritten as an ordinary word/conjugacy problem in a well-behaved hyperbolic group, existing algorithms may solve it efficiently.

### A-H07 — SAT/CSP factorization

Even a non-abelian local transition system may reduce to a bounded-domain CSP with low treewidth or small separators.

**Rule:** H1/H2 must measure primal/constraint graph width before parameter scaling.

## 5. What would count as genuinely interesting

The H-series proceeds only if a generated distribution exhibits all of the following at toy scale:

1. Local role indistinguishability: secret-role cells are not trivially separated by degrees/incidence.
2. No reduction to orientation parity or first cohomology.
3. No simple tree-gauge elimination to independent cycle variables.
4. No easy canonical-coordinate recovery.
5. Equivalent witnesses are included in attacker success.
6. Generic solver cost grows because of genuine global coupling, not because the verifier hides one planted target.
7. The public evaluator does not publish an efficiently invertible low-branching path.
8. Any proposed asymmetry survives direct structural attacks.

## 6. Novelty discipline

The possible novelty is **not**:

- hyperbolic geometry itself;
- Möbius twists;
- holonomy;
- finite quotients;
- discrete Morse theory;
- group actions.

A potentially novel result would have to be a new **generated-instance relation** combining these ingredients in a way that gives a useful trapdoor/equivalent-witness asymmetry and survives known reductions.

Until then the project must describe HFM as:

> an experimental combination of known mathematical structures with an unproven new search relation.

## 7. H0 decision

H0 does **not** reject the direction, but it sharply narrows it.

Proceed to H1 only as a falsification experiment.

H1 must start with a finite signed/transition polygonal complex and immediately test whether its apparent global frustration collapses to cycle-basis algebra or an easy CSP.
