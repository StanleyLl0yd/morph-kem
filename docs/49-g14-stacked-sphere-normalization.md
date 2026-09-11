# 49 — G14 stacked-sphere reverse-normalization negative control

## Status

**G14 is an attack calibration in progress.** The first gate is public reverse-stacking normalization. P3 exact-cover/SAT is intentionally secondary: if the carrier ancestry is already publicly reversible, the cheaper structural attack decides the experiment.

G14 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Motivation

G13 failed before cryptanalysis because naive random triangle-side pairing did not produce a healthy simplicial-surface distribution. G14 therefore switches to a constructive random family whose validity is guaranteed: stacked/Apollonian 2-spheres.

The price of guaranteed validity is an obvious possible public inverse. Each stacking step stellar-subdivides one triangular face by adding a new degree-three vertex. G14 asks whether the final globally relabelled sphere still exposes a complete reverse-stacking sequence.

## Construction

Start from the tetrahedron boundary. One stacking step selects a current triangular facet `(a,b,c)`, introduces one fresh vertex `v`, removes `(a,b,c)`, and inserts

```text
(a,b,v)
(a,c,v)
(b,c,v)
```

A deterministic seeded rule selects each face. After all steps, vertices are independently globally relabelled before publication.

Toy sets:

```text
g14-36: 36 triangles / 16 stacking steps
g14-54: 54 triangles / 25 stacking steps
g14-72: 72 triangles / 34 stacking steps
```

Every output is a closed triangulated 2-sphere by construction. For `F` triangles the public counts are `V = F/2 + 2`, `E = 3V - 6`, and Euler characteristic `2`.

No rejection sampling is used.

## A-041 — public reverse-stacking normalization

Using only the final public simplicial complex:

1. enumerate public vertices of degree three;
2. require the three neighbors to form the complete link triangle;
3. require that link triangle not already be a facet;
4. require the incident facets to be exactly the three triangles joining the candidate vertex to the three link edges;
5. deterministically choose the smallest public candidate label;
6. remove the candidate vertex and its three incident triangles;
7. restore the link triangle;
8. repeat until no legal candidate remains.

The attack records the number of simultaneous public reverse candidates at every step. It does not know the planted stacking order and does not need to recover it. Any complete public normalization to the tetrahedron boundary shows that the generated ancestry is structurally exposed.

## Rejection gate

Reject G14 if public reverse-stacking reaches the tetrahedron boundary on the deterministic all-size/multi-seed sweep using exactly `(F-4)/2` moves.

If that gate fires, do not spend effort on P3 exact-cover/SAT merely to demonstrate a heavier attack. Increasing the number of stacking steps is not a repair while the same local inverse remains available.

If reverse-stacking unexpectedly fails on some generated instances, only then continue to the P3 candidate-extraction/exact-cover/SAT gate specified in issue #88.

## Measurements

Record at least:

- public `V/E/F` and Euler characteristic;
- edge incidence range;
- primal vertex-degree histogram;
- planted stacking-step count as a generation parameter;
- public reverse-stacking move count;
- simultaneous reverse-candidate count histogram and maximum;
- terminal `V/E/F/chi`;
- whether the terminal complex is exactly a tetrahedron boundary;
- deterministic all-size / eight-seed sweep.

## Successor gate

If G14 fails by A-041, G15 must use a constructive non-toroidal carrier without an obvious bounded-local inverse such as degree-three stellar contraction. A natural next control is a sphere triangulation subjected to a long public-semantics-preserving bistellar mixing walk, followed immediately by degree-profile normalization, canonicalization, separator/treewidth, candidate-extraction and exact-cover/SAT attacks.

No trapdoor/KEM work begins before such gates survive.

No security claim.
