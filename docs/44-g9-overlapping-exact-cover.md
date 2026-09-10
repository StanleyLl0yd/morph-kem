# G9 — overlapping-carrier HGES exact-cover negative control

## Status

**G9 is an attack calibration in progress. No hardness or security conclusion is permitted until exact-head CI records A-036.**

G9 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Motivation

G8/A-035 showed that G4–G7 expose independently enumerable two-element local witness domains. After public phase extraction the entire topological verifier factors exactly through an ordinary finite-domain CSP.

G9 therefore removes the disjoint local-gadget representation. It publishes one connected simplicial complex and makes the allowed candidate pieces overlap directly in public tetrahedra. The question is whether this defeats cheap preprocessing or merely changes it from independent phase extraction to overlapping candidate enumeration plus exact cover.

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

## Structural predictions

Writing `T` for the public tetrahedron count, the underlying cycle geometry predicts

```text
V = T + 2
E = 3T + 1
F = 3T
chi = 1
boundary triangles = 2T
dual vertices/edges = T/T
```

The dual graph has degree histogram `{2:T}`, zero bridges and zero articulation vertices.

Public candidate enumeration is expected to expose exactly `T` D2 and `T` D3 candidates. Each tetrahedron is in five candidates, giving candidate/tetrahedron incidence size `5T`. In the ideal cycle model a D2 candidate overlaps six other candidates and a D3 candidate overlaps eight, so the candidate-overlap degree histogram is predicted as `{6:T, 8:T}`.

These are structural regression predictions, not hardness evidence.

## A-036 — overlapping-piece enumeration + exact cover / cycle DP

A-036 deliberately uses two independent public attacks.

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

For this special cycle family, the analytic number of distinct cyclic tilings is expected to be

```text
N = (T / p) * binomial(p, a)
```

because every rooted boundary/length-sequence representation counts an unrooted tiling once for each of its `p` piece boundaries.

Predicted counts are:

```text
g9-18:  90
g9-24: 224
g9-30: 450
```

These counts must be confirmed by both public implementations before they are recorded as measured evidence.

## Rejection gate

If A-036 cheaply recovers any accepted witness, G9 is rejected. If the predicted large family of alternative covers verifies, equivalent-witness multiplicity is an additional fatal failure mode.

Increasing `T` is not a repair while the public candidate hypergraph remains a bounded-width interval/cycle exact-cover relation.

## G10 gate

A successor must change the public overlap structure itself. It must not remain an interval/cycle tiling problem after candidate extraction or cheap normalization. The first attacks must include separator/treewidth analysis, multiscale motif/link signatures, candidate-subcomplex enumeration, exact cover/set packing, matching, low-width dynamic programming, generic CSP/SAT/CP-SAT, contraction/quotient simplification, equivalent-witness enumeration and generated-role leakage.

No security claim.
