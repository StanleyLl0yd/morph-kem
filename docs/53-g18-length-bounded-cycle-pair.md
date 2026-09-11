# 53 — G18 length-bounded exact-one-crossing cycle-pair control

## Status

**G18 is an attack calibration in progress. No hardness or security conclusion is permitted until exact-head CI records A-045.**

G18 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Motivation

G17 introduced an explicitly bilinear global topological witness, but public tree-cotree decomposition directly constructs primal/dual simple cycles that cross exactly once. G18 therefore adds geometry that is not determined by the mod-2 intersection form alone: public length bounds on both cycles while retaining the exact-one-crossing verifier.

The intended question is narrow: does a generated reference pair with public length bounds create any measured search barrier, or do ordinary shortest-path constructions recover another accepted pair inside the same bounds?

## Carrier and public bounds

G18 reuses the irregular edge-flipped torus family from G16/G17:

```text
g18-6x6: 36 vertices, 108 edges, 72 triangles, 36 successful flips
g18-6x9: 54 vertices, 162 edges, 108 triangles, 54 successful flips
g18-8x9: 72 vertices, 216 edges, 144 triangles, 72 successful flips
```

Generation uses a separate seeded spanning-tree/cotree ordering to choose one exact-one-crossing reference pair. Its primal and dual cycle lengths become the public bounds `L_p` and `L_d`. The public attack does not reuse this generation-only ordering.

The reference is post-attack evidence only. Any verifier-accepted pair inside the bounds is attacker success.

## Public verifier

A witness is a pair `(P,D)` where `P` is a simple primal cycle and `D` is a simple triangle-dual cycle. The verifier requires:

1. both cycles are valid simple public graph cycles;
2. their exact geometric primal/dual crossing count is exactly one;
3. `|P| <= L_p`;
4. `|D| <= L_d`.

The verifier never compares to the reference pair.

## A-045 — shortest odd-cocycle cycle plus constrained dual connector

A-045 uses only public incidence, the public bounds, and a canonical public nontrivial GF(2) cocycle `alpha`.

### Phase 1 — parity-cover shortest noncontractible cycle

For every public primal root `r`, build the two-sheet state graph `(v,b)`. Traversing edge `e` toggles the sheet by `alpha[e]`. BFS from `(r,0)` to `(r,1)` yields a shortest odd-pairing closed walk for that root.

Repeated edge traversals are XOR-cancelled. The resulting Eulerian support is decomposed with the existing public fundamental-cycle machinery and one odd-pairing simple cycle is retained. Distinct candidates are canonicalized and ordered by measured cycle length.

### Phase 2 — exact-one-crossing dual connector

For each primal candidate `P` within `L_p` and each anchor edge `e` of `P`:

- forbid every dual edge crossing an edge of `P`;
- BFS between the endpoints of the dual edge `e*` while `e*` is absent;
- add `e*` back to close the dual cycle.

The resulting dual cycle crosses `P` only at `e`. A candidate is accepted only when its exact verifier result is valid and its dual length is at most `L_d`.

This is public shortest-path work, not a hardness assumption.

## Independent comparison

G18 also records the ordinary canonical tree-cotree pair from G17 and tests whether that older construction happens to satisfy the new public length bounds. It is not the primary A-045 attack and uses an ordering independent of the hidden reference generation.

## Measurements

The implementation records:

- public `V/E/F`, Euler characteristic and closed-edge incidence;
- primal/dual degree histograms and normalization-improving public flips;
- public/reference length bounds;
- public cocycle weight and measured `H^1` dimension;
- parity-cover vertices/arcs, roots attempted, queue pops and edge scans;
- shortest odd walk/support sizes and decomposition work;
- number of distinct primal candidates and candidates inside `L_p`;
- constrained-dual BFS calls, queue pops and edge scans;
- selected primal/dual lengths, exact crossing count and verifier acceptance;
- post-success reference equality;
- canonical tree-cotree lengths and whether that older attack also fits the bounds;
- deterministic all-size / multi-seed regression.

## Rejection gate

If A-045 routinely constructs an accepted exact-one-crossing pair within the public bounds using cheap parity-cover BFS plus constrained dual BFS, **reject G18**.

Do not repair by merely increasing torus dimensions while the same generated-bound construction and public shortest-path reduction remain effective.

## G19 gate

If G18 fails, G19 must add a coupling that is not reducible to one noncontractible shortest cycle plus one connector. The next controlled direction is multiple internally vertex-disjoint representatives with prescribed homology/geometric constraints, immediately attacked by vertex-splitting max-flow, disjoint-path algorithms, matching, ILP/SAT/CP-SAT, separator/treewidth methods, shortest-cycle algorithms, normalization and equivalent-witness enumeration.

No security claim.
