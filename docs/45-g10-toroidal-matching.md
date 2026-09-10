# G10 — toroidal overlapping-pair HGES matching negative control

## Status

**G10 is an attack calibration in progress. No hardness or security conclusion is permitted until exact-head CI records A-037.**

G10 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Motivation

G9 removed the independent local phase domains broken by G8, but its overlapping candidate pieces still formed a one-dimensional interval/cycle exact-cover relation. A-036 recovered every accepted tiling by exact cover and tiny-state cycle DP.

G10 changes the overlap interaction itself. It reuses the exact closed torus triangulations from M4. Public candidate pieces are pairs of adjacent triangles, so the triangle-dual interaction graph is a two-dimensional, 3-regular toroidal graph rather than a cycle.

The mandatory first question is whether this genuinely harder-looking overlap relation is anything more than ordinary public perfect matching.

## Construction

For an `r x c` periodic triangulated torus,

```text
V = r c
E = 3 r c
F = 2 r c
chi = 0
```

and every public edge is incident to exactly two public triangles.

Allowed **D2-surface** pieces are any two triangles sharing exactly one edge. Their union is a two-triangle disk using four vertices.

Toy sets:

```text
g10-4x4: V/E/F = 16/48/32,  pieces = 16
g10-6x6: V/E/F = 36/108/72, pieces = 36
g10-8x8: V/E/F = 64/192/128, pieces = 64
```

The hidden reference is one deterministic seeded perfect matching selected from publicly valid matchings and retained only for post-attack comparison. The verifier does not prefer it.

## Public relation

A witness is any partition of all public triangles into valid adjacent pairs. Every triangle must appear exactly once.

Thus the relation is intentionally tested at its simplest exact semantics: accepted witnesses are perfect matchings of the public triangle-dual graph.

## Structural gate

The measured public object must satisfy:

- one connected closed 2D simplicial complex;
- every edge has triangle incidence exactly two;
- triangle-dual graph connected and 3-regular;
- zero dual bridges and articulation vertices;
- public bipartition recovered by graph coloring, not planted triangle orientation;
- equal bipartition sizes `rc/rc`;
- every dual edge passes the exact D2-surface predicate.

This removes G9's canonical interval/cycle ordering but is not hardness evidence.

## A-037 — public bipartite perfect-matching recovery

A-037 uses only public incidence:

1. enumerate edge/triangle incidence;
2. build the public triangle-dual graph;
3. recover its bipartition by BFS coloring;
4. run deterministic augmenting-path perfect matching;
5. lift matched dual edges directly to triangle-pair groups;
6. submit the groups to the exact G10 verifier;
7. force public non-matching edges one at a time and re-solve to recover alternative accepted matchings up to an explicit cap;
8. compare with the hidden reference only after public success.

The implementation records augmentations, recursive augmenting-search calls, public dual-edge scans, forced-edge attempts and alternative-search edge scans.

## Rejection gate

Any accepted public perfect matching rejects G10. Alternative accepted matchings strengthen the result under equivalent-witness semantics.

Increasing torus dimensions cannot repair a relation that is exactly bipartite perfect matching; the polynomial algorithm applies regardless of grid width or treewidth.

## G11 gate

If G10 fails as expected, G11 must change the allowed-piece relation beyond pairwise matching. The next useful control should use overlapping pieces of size greater than two so candidate selection is genuinely hypergraphic, while immediately testing planarity/toroidality, separators/treewidth, Pfaffian/matching reductions, local signatures, exact cover/set packing, low-width DP, generic CSP/SAT/CP-SAT, equivalent-witness multiplicity and generated-role leakage.

No security claim.
