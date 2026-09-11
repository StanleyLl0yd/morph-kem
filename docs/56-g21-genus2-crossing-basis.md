# 56 — G21 genus-two full crossing-matrix negative control

## Status

**G21 is rejected by A-048: the full simultaneous 4x4 crossing-matrix witness is publicly constructed by tree-cotree decomposition.**

G21 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Motivation

G20 moved to genus two and required two vertex-disjoint representatives in distinct public cohomology classes. A-047 still recovered the classes sequentially with a four-sheet parity cover and vertex deletion.

G21 removes that sequential structure from the verifier. The witness is an eight-cycle family whose complete primal-dual geometric crossing matrix must be the 4x4 identity. All diagonal and off-diagonal conditions are checked simultaneously.

The negative-control question is whether this stronger coupled relation survives public topology, or whether a genus-two tree-cotree decomposition already constructs the whole family at once.

## Carrier

G21 reuses the G20 carrier idea without its reference-pair conditioning. Two triangulated tori are connected-summed, the closed genus-two surface is globally mixed by deterministic legal `2 <-> 2` edge flips, and vertices are independently relabelled.

Toy sets:

```text
g21-4x4: V/E/F = 29/93/62,   124 successful flips
g21-6x6: V/E/F = 69/213/142, 284 successful flips
g21-6x9: V/E/F = 105/321/214, 428 successful flips
```

Every carrier must have Euler characteristic `-2`, exact edge incidence two and measured `dim H^1(F2)=4`.

## Public witness

A witness contains four simple primal cycles `P0..P3` and four simple triangle-dual cycles `D0..D3`.

The exact geometric crossing-count matrix must be

```text
1 0 0 0
0 1 0 0
0 0 1 0
0 0 0 1
```

The verifier checks exact crossing counts, not only parity. All cycles on each side must be distinct. No planted or reference basis is part of acceptance.

## A-048 — full genus-two tree-cotree basis recovery

A-048 uses only public cellular incidence.

1. Build a deterministic public primal spanning tree `T`.
2. Forbid all dual edges crossing `T`.
3. Build a deterministic public dual spanning tree `T*` from the remaining dual graph.
4. Collect the primal edges in neither `T` nor crossed by `T*`.
5. A closed genus-two surface should expose exactly four tree-cotree leftovers.
6. For each leftover `ei`, construct the primal fundamental cycle `Pi = ei + path_T(ei)`.
7. Construct the dual fundamental cycle `Di = ei* + path_T*(ei*)` through the crossing dual edge.
8. Submit all four pairs simultaneously to the exact verifier.

### Structural prediction

Every `Pi` contains only primal-tree edges plus its own leftover `ei`. The dual tree contains no edge crossing a primal-tree edge, and `Di` closes only through `ei*`. Therefore `Di` crosses `Pi` exactly once and crosses every `Pk`, `k != i`, zero times.

The predicted exact crossing matrix is therefore the identity, not merely a rank-four matrix over GF(2).

## Independent cross-check

Separately enumerate the full ordinary primal and dual fundamental-cycle bases and build their complete mod-2 crossing matrix. The measured rank should be four, exposing the four-dimensional genus-two homological quotient even though the graph cycle spaces are much larger.

This full-basis calculation is independent evidence. The exact tree-cotree identity family remains the primary A-048 attack.

## Measurements

Record:

- public `V/E/F`, Euler characteristic and edge-incidence range;
- measured `H^1` dimension;
- primal and dual degree histograms;
- normalization-improving legal flips;
- primal tree, forbidden-dual and dual-tree sizes;
- tree-cotree leftover count;
- primal and dual path scans;
- four primal and four dual cycle lengths;
- exact 4x4 crossing-count matrix and off-diagonal nonzero count;
- exact verifier result;
- full primal/dual cycle-basis sizes and path scans;
- full crossing-matrix weight, GF(2) rank and row-XOR work;
- deterministic all-size / multi-seed sweep.

## Rejection gate

If A-048 routinely constructs the complete exact identity crossing family publicly, **reject G21**. Increasing the genus-two carrier size or flip count is not a repair while the cellular embedding exposes this tree-cotree basis.

## G22 gate

A successor must impose constraints not automatically satisfied by a tree-cotree basis. In particular, it should couple cycles on the same side through vertex-disjointness, exact geometric intersections, shared avoidance regions or length constraints, rather than only prescribe primal-dual pairings.

It must immediately face symplectic-basis algorithms, disjoint paths and vertex-splitting/max-flow, matching, shortest-cycle methods, ILP/SAT/CP-SAT, separator/treewidth, normalization and equivalent-witness enumeration.

No security claim.

## Measured A-048 result

Exact-head Python 3.12 `g21-6x9`:

~~~text
successful flips:                           428
public V/E/F:                               105/321/214
Euler characteristic:                       -2
edge triangle incidence min/max:            2/2
H1 dimension:                               4
primal degree histogram:                    ((3,18),(4,23),(5,12),(6,14),(7,5),(8,12),(9,11),(10,4),(11,1),(13,1),(14,3),(16,1))
dual degree histogram:                      ((3,214),)
normalization-improving legal flips:         114
primal tree / forbidden dual / dual tree:    104/104/213
tree-cotree leftovers:                       4
primal / dual path scans:                    25/63
primal cycle lengths:                        (7,7,9,6)
dual cycle lengths:                          (6,31,10,20)
exact crossing matrix:                       I4
off-diagonal nonzero entries:                0
exact verifier accepted:                     yes
full primal / dual basis cycles:             217/108
full primal / dual path scans:               923/1104
full crossing matrix weight:                 632
full crossing matrix GF(2) rank:             4
full crossing matrix row XORs:               65
~~~

Python 3.12 sweep over `g21-4x4`, `g21-6x6`, `g21-6x9` x eight deterministic seeds gives **24/24** public tree-cotree decompositions with exactly four leftovers, **24/24** exact identity crossing matrices, zero off-diagonal crossings in every instance, and **24/24** exact-verifier accepted eight-cycle families. The independent full primal/dual basis crossing matrix has GF(2) rank exactly four on all **24/24** instances.

Measured primary path work remains small. Maximum total primal/dual path scans are `23/55`, `30/82`, and `34/126` for the three sizes. The full basis sizes are seed-invariant: `65x32`, `145x72`, and `217x108`.

### Result

**G21 rejected by A-048.** Simultaneously prescribing the complete primal-dual identity crossing matrix does not create a joint inversion barrier. A public tree-cotree decomposition exposes all `2g=4` leftover edges at once, and their paired primal/dual fundamental cycles satisfy every exact diagonal and off-diagonal verifier constraint mechanically.

This is a structural cellular-topology break. Increasing carrier size or flip count is not a repair while the public embedding exposes the same tree-cotree basis. G22 must constrain cycles on the same side or otherwise impose geometry not supplied automatically by a tree-cotree decomposition.

No security claim.
