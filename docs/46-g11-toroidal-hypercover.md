# G11 — toroidal P3-triomino hypergraph exact-cover negative control

## Status

**G11 is an attack calibration in progress. No hardness or security conclusion is permitted until exact-head CI records A-038.**

G11 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Motivation

G10 removed G9's interval/cycle overlap geometry but still failed because every allowed piece contained only two adjacent triangles. The exact public relation was therefore ordinary bipartite perfect matching.

G11 changes the relation, not just the carrier. It keeps the closed periodic torus but allows three-triangle `P3` pieces, so public candidate selection is genuinely 3-uniform hypergraph exact cover.

The experiment asks whether the regular generated toroidal hypergraph resists ordinary public exact-cover/SAT attacks. Worst-case exact-cover hardness is not evidence about this distribution.

## Construction

The underlying public surface is the same exact periodic torus triangulation used by M4/G10. For an `r x c` torus:

```text
V = r c
E = 3 r c
F = 2 r c
chi = 0
```

Every public edge belongs to exactly two public triangles and the public triangle-dual graph is connected, bipartite and 3-regular.

An allowed **P3-surface piece** consists of three public triangles whose induced dual graph is a path `P3`. The exact simplicial predicate additionally requires the local disk profile

```text
vertices = 5
edges = 7
triangles = 3
internal shared edges = 2
boundary edges = 5
chi = 1
```

so the attack cannot accept a graph-shape false positive.

Toy sets:

```text
g11-3x6: V/E/F = 18/54/36,   pieces = 12
g11-6x6: V/E/F = 36/108/72,  pieces = 24
g11-6x9: V/E/F = 54/162/108, pieces = 36
```

Generation chooses one deterministic seeded exact cover from the valid candidate family only to guarantee a satisfiable calibration instance. That cover and its candidate ordering seed are reference-only and do not define verifier acceptance.

## Public relation

A witness is any partition of all public triangles into groups of exactly three, each passing the exact P3-surface predicate.

The verifier does not require the reference cover, torus coordinates, orientation, triangle colors, or generation order. Any accepted equivalent cover is attacker success.

## Structural predictions

For the periodic torus dual graph, each triangle has three dual neighbors. Choosing any two neighbors gives one centered `P3`, so the expected candidate count is

```text
3F
```

for `F` public triangles.

Each triangle occurs as the center of three candidates and as an endpoint of six more, hence the predicted public candidate membership is exactly nine per triangle. Direct combinatorial enumeration of the target family predicts:

```text
candidate count               = 3F
candidate memberships         = 9 per triangle
candidate/triangle incidences = 9F
candidate overlap degree      = 18 for every candidate
```

These values are regression predictions, not hardness evidence.

## A-038 — public P3 candidate enumeration + exact cover / SAT

### Algorithm-X-style path

A-038 first uses only public simplicial incidence:

1. enumerate edge/triangle incidence and construct the public triangle-dual graph;
2. enumerate every public induced `P3` triple;
3. filter candidates through the exact simplicial piece predicate;
4. build the candidate/triangle incidence hypergraph;
5. choose the uncovered triangle with the fewest currently feasible candidates;
6. branch deterministically over those candidates and remove their three covered triangles;
7. enumerate covers up to an explicit solution cap;
8. submit every cover to the exact G11 verifier;
9. compare with the generation reference only after public success.

The implementation records exact-cover nodes, branching decisions and backtracks in addition to candidate and overlap statistics.

### Independent MiniSat path

The same public candidate hypergraph is independently encoded to CNF with one Boolean variable per candidate. For each public triangle, the encoding requires exactly one incident candidate:

- one at-least-one clause;
- pairwise at-most-one clauses.

With the predicted regular membership nine, this gives

```text
SAT variables = 3F
SAT clauses   = F * (1 + C(9,2)) = 37F
```

The dedicated Python 3.12 workflow runs MiniSat on `g11-6x9`, decodes the selected public candidates and checks the resulting cover again with the exact repository verifier.

## Rejection gate

If either public exact-cover search or independent SAT finds an accepted witness cheaply, G11 is rejected. If many accepted covers exist, equivalent-witness multiplicity is an additional failure mode.

Do not increase torus dimensions as a repair while this same regular generated candidate hypergraph remains vulnerable.

## G12 gate

A successor must distinguish genuine topological structure from generic exact-cover/SAT difficulty. A useful G12 would replace the highly regular periodic carrier or otherwise break its obvious repeated local candidate structure, while immediately testing automorphisms, periodic/generated-role leakage, separator/treewidth methods, candidate extraction, exact cover/set packing, SAT/CP-SAT, normalization/contraction and equivalent-witness multiplicity.

No trapdoor/KEM work follows from G11 merely because the relation is hypergraphic. No security claim.
