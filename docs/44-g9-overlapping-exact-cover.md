# G9 — overlapping-carrier HGES exact-cover negative control

## Status

**G9 is rejected by A-036.** Public overlapping-piece enumeration followed by exact cover, independently cross-checked by public cycle composition DP, recovers large families of accepted equivalent witnesses on every measured instance.

G9 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Motivation

G8/A-035 showed that G4–G7 expose independently enumerable two-element local witness domains. After public phase extraction the entire topological verifier factors exactly through an ordinary finite-domain CSP.

G9 removes that particular premise. It publishes one connected simplicial complex and makes the allowed candidate pieces overlap directly in public tetrahedra. There is no public tuple of disjoint local gadgets whose phases can be enumerated independently.

The measured result is still negative: the new overlap relation is a bounded-width interval/cycle exact-cover problem, and equivalent-witness multiplicity becomes much larger than in the phase-gadget line.

## Construction

The public tetrahedron dual graph is a simple cycle `C_T`. The allowed piece dictionary contains two types:

- **D2:** two consecutive dual vertices; the two tetrahedra form a five-vertex 3-ball with profile `V/E/F/T = 5/9/7/2` and one internal triangular face;
- **D3:** three consecutive dual vertices; the three tetrahedra form a six-vertex path 3-ball with profile `V/E/F/T = 6/12/10/3`, two internal triangular faces and pairwise vertex-intersection sizes `2,3,3`.

No disjoint carrier partition is public. Every tetrahedron belongs to two D2 candidates and three D3 candidates, so the local candidate carriers overlap from the start.

Toy sets:

```text
g9-18: T=18, pieces=7,  required D2/D3 = 3/4
g9-24: T=24, pieces=9,  required D2/D3 = 3/6
g9-30: T=30, pieces=11, required D2/D3 = 3/8
```

For a public witness with `T` tetrahedra and `p` pieces, the D2/D3 multiplicities are determined by

```text
a + b = p
2a + 3b = T
```

so `a = 3p-T` and `b = T-2p`.

Generation chooses one deterministic hidden cyclic D2/D3 tiling and retains it only for post-attack comparison. Public vertex relabeling and tetrahedron sorting come from the same deterministic cycle geometry used by G3.

## Public relation

A witness is any partition of all public tetrahedra into exactly `p` valid D2/D3 groups such that the cross-group shared-face graph is a connected simple cycle.

The verifier does not require the planted piece boundaries, cyclic offset, orientation or D2/D3 order. Any accepted equivalent tiling is attacker success.

## Structural measurements

Writing `T` for the public tetrahedron count, all measured instances satisfy

```text
V = T + 2
E = 3T + 1
F = 3T
chi = 1
boundary triangles = 2T
dual vertices/edges = T/T
```

The public dual graph has degree histogram `{2:T}`, zero bridges and zero articulation vertices.

Candidate enumeration exposes exactly `T` D2 and `T` D3 candidates. Every tetrahedron belongs to five candidates, giving candidate/tetrahedron incidence size `5T`. Every D2 candidate overlaps six other candidates and every D3 candidate overlaps eight, so the overlap-degree histogram is exactly `{6:T, 8:T}` on the full deterministic sweep.

## A-036 — overlapping-piece enumeration + exact cover / cycle DP

A-036 uses two independent public attacks.

### Exact-cover path

1. build public triangular-face incidence and the tetrahedron dual graph;
2. enumerate all D2 candidates from dual edges;
3. enumerate all D3 candidates from public length-two dual paths;
4. filter every candidate through the exact simplicial piece predicate;
5. build the candidate/tetrahedron incidence and overlap relations;
6. solve exact cover with the public piece-count constraint and deterministic MRV branching;
7. submit every recovered cover up to the explicit cap to the exact G9 verifier.

### Cycle-composition path

The attacker independently derives a canonical traversal of the public dual cycle. A bounded-state composition DP enumerates all length sequences containing the required numbers of 2s and 3s. Every public start position is tried, covers are canonicalized and duplicates removed, then submitted to the same verifier.

For this cycle family, the analytic number of distinct cyclic tilings is

```text
N = (T / p) * binomial(p, a)
```

because every rooted boundary/length-sequence representation counts an unrooted tiling once for each of its `p` piece boundaries.

Both implementations exactly match this count on every measured seed.

## Exact Python 3.12 `g9-30` baseline

```text
public tetrahedra / witness pieces:       30/11
required D2/D3 pieces:                    3/8
public V/E/F/T:                           32/91/90/30
Euler characteristic:                    1
boundary faces / max face incidence:      60/2
dual graph vertices / edges:              30/30
dual degree histogram:                    ((2,30),)
bridges / articulation points:             0/0
D2 / D3 public candidates:                30/30
candidate memberships per tetrahedron:    ((5,30),)
candidate overlap-degree histogram:       ((6,30),(8,30))
candidate/tetrahedron incidence size:     150
face occurrence checks:                   120
exact-cover solutions / cap:              450/1024
exact-cover cap hit:                      no
exact-cover nodes / backtracks:           2820/899
cycle-DP states / transitions / tilings:  36/70/450
analytic cyclic tilings:                  450
accepted public solutions:                450
accepted non-reference solutions:        449
reference witness accepted:               yes
```

## Deterministic sweep

Python 3.12 tested `g9-18`, `g9-24`, and `g9-30` over eight independently derived deterministic seeds each.

| Set | V/E/F/T | D2/D3 candidates | Membership | Candidate incidence | Exact-cover solutions | Exact-cover nodes/backtracks | DP states/transitions/tilings | Accepted | Non-reference |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| g9-18 | 20/55/54/18 | 18/18 | 5×18 | 90 | 90 | 420/102 | 20/38/90 | 90 | 89 |
| g9-24 | 26/73/72/24 | 24/24 | 5×24 | 120 | 224 | 1211/345 | 28/54/224 | 224 | 223 |
| g9-30 | 32/91/90/30 | 30/30 | 5×30 | 150 | 450 | 2820/899 | 36/70/450 | 450 | 449 |

All **24/24** instances have zero bridges and articulation points, exactly `T` candidates of each piece type, the same candidate-membership/overlap signatures, and exact agreement between analytic count, exact-cover enumeration and cycle-DP enumeration. Every recovered cover passes the exact public verifier.

The result is independent of public relabeling in the measured sweep: exact-cover and DP work are identical within each parameter set.

## Result

**G9 is rejected by A-036.**

G9 does successfully remove the direct G8 premise of a public tuple of disjoint independently enumerable local phase gadgets. That is not enough. The overlapping candidates form a public interval hypergraph over a recovered cycle order, so candidate extraction followed by exact cover or bounded-state DP remains cheap.

The failure is stronger under equivalent-witness semantics. The largest toy set has 450 accepted decompositions and 449 of them differ from the planted reference. Hiding the planted tiling therefore provides no useful asymmetry.

Increasing `T` is not a repair while the public candidate hypergraph remains a bounded-width interval/cycle exact-cover relation.

This rejects the current generated family only. It is not a theorem that general HGES or general exact cover is easy.

## G10 gate

A successor must change the public overlap structure itself. It must not remain an interval/cycle tiling problem after candidate extraction or cheap normalization. The first attacks must include separator/treewidth analysis, multiscale motif/link signatures, candidate-subcomplex enumeration, exact cover/set packing, matching, low-width dynamic programming, generic CSP/SAT/CP-SAT, contraction/quotient simplification, equivalent-witness enumeration and generated-role leakage.

More specifically, G10 should use an overlap interaction graph with nontrivial branching and no fixed-width cycle/path ordering exposed by the public dual graph. Before interpreting any solver growth, the repository must measure treewidth/separator structure of the candidate-overlap graph and test whether a public decomposition gives an efficient dynamic program.

No security claim.
