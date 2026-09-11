# 49 — G14 stacked-sphere reverse-normalization negative control

## Status

**G14 is an attack calibration in progress.** It uses a constructive non-toroidal simplicial carrier, so there is no carrier rejection sampling. The first security-relevant question is whether the stacking ancestry is publicly reversible.

G14 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Motivation

G13 abandoned torus ancestry but failed before cryptanalysis: naive random pairing of abstract triangle sides produced zero honest simplicial surfaces across the measured attempt budget. G14 therefore switches to a family that is valid by construction rather than by conditioning.

A stacked/Apollonian 2-sphere is generated from the tetrahedron boundary by repeatedly subdividing one current triangular face with a new vertex. Every step preserves a closed triangulated sphere.

This immediately creates an obvious attack surface: the fresh vertex initially has degree three and its link is the old triangular face. The attack-first question is whether the final public complex can be normalized all the way back to the tetrahedron boundary without any generation history.

## Construction

Start from the four triangular facets of a tetrahedron. At each deterministic seeded step choose one current face `(a,b,c)`, remove it, add a fresh vertex `v`, and insert

```text
(a,b,v)
(a,c,v)
(b,c,v)
```

After all steps, globally relabel every public vertex using an independent deterministic seed-derived permutation.

Toy sets:

```text
g14-36: 16 stacking steps, V/E/F = 20/54/36
g14-54: 25 stacking steps, V/E/F = 29/81/54
g14-72: 34 stacking steps, V/E/F = 38/108/72
```

Every generated carrier has Euler characteristic two and every public edge belongs to exactly two triangles. No carrier retry or rejection sampling is used.

## A-041 — public reverse-stacking normalization

From the final public complex only:

1. enumerate vertices of degree three;
2. require exactly three incident triangles and a three-vertex link;
3. require the link triangle itself to be absent;
4. remove the degree-three vertex and its three incident triangles;
5. restore the link triangle;
6. repeat deterministically until no legal reverse move remains.

The tetrahedron boundary is intentionally terminal: all four vertices have degree three, but each link triangle is already present, so none is a legal reverse-stacking move.

Record the number of legal candidates at every step, total moves, and the final `V/E/F`. If the public normalizer always performs exactly the planted number of steps and ends at `4/6/4`, the carrier ancestry is structurally exposed and G14 is rejected regardless of the second P3 experiment.

## Independent P3 hypercover diagnosis

G14 also retains the exact three-triangle P3-disk witness relation used in G11/G12, but **P3 satisfiability is not a generation condition**.

After a valid stacked sphere exists:

1. enumerate all public exact P3 candidates;
2. run deterministic MRV Algorithm-X exact cover up to an explicit cap;
3. if a cover exists, optionally select one by a secret deterministic ordering as post-attack reference evidence;
4. run a public SAT encoding with one Boolean variable per P3 candidate and exactly-one constraints per public triangle;
5. decode any SAT model through the exact repository verifier.

A carrier with no P3 cover is still rejected if A-041 reverse-normalization succeeds. The generator never retries merely to obtain a satisfiable witness relation.

## Measurements

Record at least:

- public `V/E/F`, Euler characteristic and closed edge incidence;
- primal degree histogram and initial degree-three count;
- reverse candidate counts, maximum simultaneous candidates and total moves;
- terminal `V/E/F` and whether the tetrahedron boundary is reached;
- dual graph degree histogram, bridges, articulations and bipartiteness;
- P3 candidate count, membership/overlap histograms and candidate incidence;
- exact-cover nodes/decisions/backtracks, solution count/cap and accepted witnesses;
- whether a reference cover happened to exist without conditioning;
- MiniSat variables/clauses/work and decoded verifier result;
- deterministic all-size / multi-seed sweep.

## Rejection gate

Reject G14 if public reverse-stacking routinely reconstructs the tetrahedron boundary. This is already a structural break and must not be repaired by increasing the number of stacking steps.

Cheap exact-cover/SAT recovery or equivalent-witness multiplicity is an independent additional failure mode, not a prerequisite for rejection.

## G15 gate

A successor must use a constructive non-toroidal carrier without a bounded-local inverse such as degree-three stellar contraction. It must immediately face public simplification/bistellar normalization, canonicalization, separator/treewidth analysis, candidate extraction, exact cover/CSP/SAT/CP-SAT, equivalent witnesses and generated-role leakage before any trapdoor work.

No security claim.
