# G10 — toroidal overlapping-pair HGES matching negative control

## Status

**G10 is rejected by A-037.** Exact-head Python 3.11/3.12/3.13 dedicated CI and the common repository CI pass. The public toroidal decomposition relation is ordinary bipartite perfect matching, and equivalent accepted matchings are abundant on the measured family.

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

The measured public object satisfies:

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

## Exact Python 3.12 `g10-8x8` result

```text
torus rows/cols:                              8/8
public V/E/F:                                64/192/128
Euler characteristic:                        0
edge triangle incidence min/max:             2/2
dual vertices/edges:                         128/192
dual degree histogram:                       ((3,128),)
bridges/articulation points:                  0/0
public bipartition sizes:                     (64,64)
allowed candidate dual edges:                192
base matching augmentations/DFS calls/scans: 64/455/770
alternative forced-edge attempts:             63
alternative matching edge scans:           49473
matching solutions/cap:                       64/64
matching cap hit:                             yes
accepted public solutions:                    64
accepted non-reference solutions:            63
reference witness accepted:                  yes
```

The base public recovery therefore produces a verifier-valid decomposition in polynomial matching work. The alternative search immediately reaches the explicit 64-solution cap; 63 of those accepted witnesses differ from the hidden reference.

## Deterministic sweep

Python 3.12 tested `g10-4x4`, `g10-6x6`, and `g10-8x8` over eight independently derived deterministic public relabel seeds each.

| Set | Dual V/E | Bipartition | Base augmentations | Base DFS calls range | Base edge scans range | Accepted solutions range | Non-reference range | Cap behavior |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| g10-4x4 | 32/48 | 16/16 | 16 | 59–76 | 98–132 | 22–26 | 21–25 | cap 64 not reached |
| g10-6x6 | 72/108 | 36/36 | 36 | 151–271 | 237–474 | 62–64 | 61–63 | cap reached on 6/8 seeds |
| g10-8x8 | 128/192 | 64/64 | 64 | 390–564 | 655–986 | 64 | 63 | cap reached on 8/8 seeds |

Across all **24/24** measured instances, the public graph is 3-regular and bipartite with zero bridges/articulation points, A-037 finds an accepted public perfect matching, and at least one accepted non-reference matching is recovered. On every `g10-8x8` seed the alternative search reaches the 64-solution cap.

## Result

**G10 is rejected by A-037.**

The move from one-dimensional cyclic overlap to a genuinely two-dimensional toroidal interaction changes the geometry but not the computational relation. Because each accepted piece contains exactly two adjacent triangles, public decomposition is exactly a graph perfect-matching problem. The recovered bipartition makes deterministic polynomial matching sufficient, regardless of the torus width or separator growth.

Do not increase torus dimensions as a repair. Equivalent-witness multiplicity is also substantial and helps the attacker under MORPH-KEM semantics.

This is a generated-relation falsification, not a theorem that arbitrary HGES or hypergraph decomposition is easy.

## G11 gate

G11 must change the allowed-piece relation beyond pairwise matching. The next useful control should use overlapping pieces of size greater than two so candidate selection is genuinely hypergraphic. It must immediately test planarity/toroidality, separators/treewidth, matching/Pfaffian reductions, local signatures, exact cover/set packing, low-width DP, generic CSP/SAT/CP-SAT, equivalent-witness multiplicity and generated-role leakage.

No trapdoor work begins from G10. No security claim.
