# 54 — G19 vertex-disjoint cohomology-cycle pair control

## Status

**G19 is an attack calibration in progress. No hardness or security conclusion is permitted until exact-head CI records A-046.**

G19 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Motivation

G18 added public geometric length bounds and exact geometric crossing, but one public noncontractible cycle plus one constrained connector was still enough. G19 is the first control in this line that requires two simultaneously global geometric representatives in the same public primal graph.

A witness contains two vertex-disjoint simple cycles. Both must pair oddly with one public nontrivial GF(2) cocycle, and their two sorted lengths must fit generation-derived public bounds.

On the torus this is a real coupling: two disjoint noncontractible simple curves cannot have nonzero mutual intersection, so the two odd-pairing representatives must be compatible parallel-type representatives rather than arbitrary independent cycles.

## Carrier

G19 reuses the irregular edge-flipped torus family:

```text
g19-6x6: 36 vertices / 72 triangles / 36 successful flips
g19-6x9: 54 vertices / 108 triangles / 54 successful flips
g19-8x9: 72 vertices / 144 triangles / 72 successful flips
```

Carrier construction is deliberately unchanged so only the witness coupling is under test.

## Public cocycle and bounds

The final public carrier exposes the same canonical nontrivial GF(2) cocycle construction used in G16/G18. The public instance stores the cocycle bits explicitly.

Reference generation uses an independent hidden seeded spanning-tree ordering. It enumerates odd fundamental cycles of that hidden tree and searches for a vertex-disjoint pair. The selected pair is reference evidence only; its sorted cycle lengths become the public bounds `(L_1,L_2)`.

If one carrier exposes no reference pair after the bounded hidden-tree search, carrier generation retries with an explicit deterministic retry counter. No retry is silent.

## Public verifier

A canonical witness `(C_1,C_2)` is accepted only if:

1. both are canonical simple public primal cycles;
2. both pair oddly with public `alpha`;
3. their vertex sets are disjoint;
4. after canonical length ordering, `|C_1| <= L_1` and `|C_2| <= L_2`.

The verifier never compares with the hidden reference pair.

## A-046 — delete-one-cycle parity-cover recovery

### First stage

Run the G18 two-sheet public parity-cover attack on the full primal graph for every public root. XOR-cancel repeated edge traversals, decompose each odd support to a simple odd cycle, canonicalize duplicates and sort candidates by length.

### Second stage

For each first-stage candidate in deterministic order:

1. delete every vertex of that candidate and every incident primal edge;
2. rebuild the two-sheet parity-cover search on the remaining public graph;
3. run all remaining public roots and keep reachable odd-support cycles;
4. decompose/canonicalize those supports to simple odd cycles;
5. test canonical pairs against the exact public bounds and verifier.

Deleting the first cycle makes vertex-disjointness part of the recovery procedure rather than a post-hoc pair filter.

## Independent cross-check

Independently build one canonical public spanning forest, enumerate every odd fundamental cycle of that tree, and scan its vertex-disjoint cycle pairs against the same exact verifier and bounds. This cross-check does not use the parity-cover/deletion construction or hidden generation ordering.

## Measurements

Record at least:

- public `V/E/F`, Euler characteristic and edge-incidence range;
- successful flips, generation retries and hidden-tree reference attempts;
- primal degree histogram and public normalization-improving flip count;
- public alpha weight / measured `H^1` dimension;
- public/reference `L_1/L_2`;
- first-stage parity-cover roots, queue pops, edge scans, candidate count and length histogram;
- first candidates attempted;
- second-stage calls, roots, reachable roots, queue pops and edge scans;
- second-stage decomposition and candidate counts;
- deleted vertex/edge counts for the selected first cycle;
- selected two lengths, cocycle pairings and shared-vertex count;
- exact verifier acceptance and post-success reference equality;
- independent fundamental-cycle pool size / pair tests / verifier result;
- deterministic all-size / eight-seed sweep.

## Rejection gate

If A-046 routinely recovers an accepted bounded vertex-disjoint odd-cycle pair using cheap public parity-cover/deletion work, **reject G19**.

If the independent canonical fundamental-cycle pool is even cheaper, preserve it as a stronger attack. Do not increase torus dimensions while the same public delete/recover or cycle-pair reduction remains effective.

## G20 gate

If G19 fails, G20 must require a multicurve relation not reducible to repeated recovery of parallel torus representatives. Candidate directions include a genus-two carrier with multiple independent handles, three or more cycles with a prescribed pairwise intersection matrix, or simultaneous disjointness and independent class constraints. Mandatory attacks include vertex-splitting max-flow, multi-commodity/disjoint-path algorithms, matching, symplectic-basis methods, ILP/SAT/CP-SAT, separator/treewidth, normalization and equivalent-witness enumeration.

No security claim.
