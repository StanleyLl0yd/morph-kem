# G11 — toroidal P3-triomino hypergraph exact-cover negative control

## Status

**G11 is rejected by A-038.** Exact-head dedicated CI passes on Python 3.11, 3.12 and 3.13. Public Algorithm-X-style exact cover reaches the explicit solution cap on every measured instance, and an independent MiniSat encoding recovers another accepted non-reference witness on the fixed largest baseline.

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

## Structural measurements

The predicted regular candidate profile is confirmed exactly on every measured set. For `F` public triangles:

```text
P3 candidate count             = 3F
candidate memberships          = 9 per triangle
candidate/triangle incidences  = 9F
candidate overlap degree       = 18 for every candidate
```

The dual graph remains 3-regular with zero bridges and articulation points. Thus A-038 is not exploiting a return of G0/G9 separator or interval structure.

## A-038 — public P3 candidate enumeration + exact cover / SAT

### Algorithm-X-style path

A-038 uses only public simplicial incidence:

1. enumerate edge/triangle incidence and construct the public triangle-dual graph;
2. enumerate every public induced `P3` triple;
3. filter candidates through the exact simplicial piece predicate;
4. build the candidate/triangle incidence hypergraph;
5. choose the uncovered triangle with the fewest currently feasible candidates;
6. branch deterministically over those candidates and remove their three covered triangles;
7. enumerate covers up to an explicit solution cap;
8. submit every cover to the exact G11 verifier;
9. compare with the generation reference only after public success.

### Exact Python 3.12 `g11-6x9` result

```text
public V/E/F:                         54/162/108
Euler characteristic:                0
edge triangle incidence min/max:     2/2
witness pieces:                       36
dual vertices/edges:                 108/162
dual degree histogram:               ((3,108),)
bridges / articulation points:       0/0
public bipartition sizes:             54/54
P3 public candidates:                324
candidate memberships per triangle: ((9,108),)
candidate overlap degree histogram:  ((18,324),)
candidate/triangle incidence size:   972
exact-cover solutions / cap:         64/64
exact-cover cap hit:                  yes
exact-cover nodes/decisions/backtracks: 292/71/10
accepted public solutions:           64
accepted non-reference solutions:    64
reference witness accepted:          yes
```

All first 64 public covers found by the fixed baseline differ from the hidden reference. Exact planted recovery is neither requested nor needed.

### Deterministic sweep

Python 3.12 tested `g11-3x6`, `g11-6x6`, and `g11-6x9` over eight independently derived public relabel seeds each, with solution cap 32.

| Set | Candidates | Membership / overlap degree | Nodes range | Decisions range | Backtracks range | Accepted / cap | Non-reference |
|---|---:|---:|---:|---:|---:|---:|---:|
| g11-3x6 | 108 | 9 / 18 | 110–142 | 26–38 | 2–16 | 32/32 on 8/8 | 32 on 8/8 |
| g11-6x6 | 216 | 9 / 18 | 123–224 | 35–56 | 4–74 | 32/32 on 8/8 | 32 on 8/8 |
| g11-6x9 | 324 | 9 / 18 | 137–225 | 44–59 | 2–21 | 32/32 on 8/8 | 32 on 8/8 |

Across all **24/24** measured instances, the public exact-cover attack reaches the cap, every returned cover passes the exact verifier, and every returned cover differs from the hidden reference.

### Independent MiniSat path

The same public candidate hypergraph is encoded to CNF with one Boolean variable per candidate and an exactly-one constraint per public triangle. The regular membership nine gives `3F` variables and `37F` clauses.

Exact Python 3.12 `g11-6x9` cross-check:

```text
SAT variables:                    324
SAT clauses:                      3996
DIMACS bytes:                     47859
MiniSat return code:              10 (SAT)
MiniSat conflicts:                2
MiniSat decisions:                137
MiniSat propagations:             574
solver elapsed seconds:           0.004566
selected candidate pieces:        36
decoded accepted witness:         yes
matches reference after success:  no
```

MiniSat therefore independently recovers a verifier-valid non-reference hypercover.

## Result

**G11 is rejected by A-038.**

Moving from pairwise graph matching to a genuine three-uniform hypergraph relation removes the G10 polynomial matching reduction, but the generated regular toroidal P3 candidate family remains extremely easy for generic public exact-cover search and SAT. Equivalent-witness multiplicity is again severe: even the capped searches immediately return dozens of non-reference accepted covers.

Do not increase torus dimensions as a repair. This is a generated-distribution falsification, not a theorem that general hypergraph exact cover is easy.

## G12 gate

G12 must test whether the ease is primarily caused by the highly regular periodic carrier and its uniform local candidate dictionary. A useful successor should break the torus translation symmetry and repeated local role structure without reintroducing canonical separators, while immediately facing automorphism/role leakage, candidate extraction, separator/treewidth analysis, exact cover/set packing, SAT/CP-SAT, simplification/normalization and equivalent-witness enumeration.

No trapdoor/KEM work follows from G11. No security claim.
