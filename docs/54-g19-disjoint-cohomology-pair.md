# 54 — G19 vertex-disjoint cohomology-cycle pair control

## Status

**G19 is rejected by A-046 on the measured generated distribution.**

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

Independently build one canonical public spanning tree, enumerate every odd fundamental cycle of that tree, and scan its vertex-disjoint cycle pairs against the same exact verifier and bounds. This cross-check does not use the parity-cover/deletion construction or hidden generation ordering.

The cross-check is intentionally recorded separately from the primary attack: it succeeds on only 4/24 measured sweep instances, while the primary A-046 attack succeeds on 24/24. Its incompleteness therefore does not contribute to the rejection claim.

## Fixed Python 3.12 `g19-8x9` result

```text
successful carrier flips / generation retries: 72/0
public V/E/F:                                  72/216/144
Euler characteristic / edge incidence:        0 / 2..2
primal degree histogram:                      ((3,11),(4,11),(5,8),(6,12),(7,11),(8,10),(9,7),(10,1),(13,1))
normalization-improving legal flips:           66
public alpha weight / H1 dimension:            21/2
public short/long bounds:                       8/9
reference short/long lengths:                   8/9
reference seeded-tree attempts:                12
first-stage roots / queue pops / edge scans:   72/9740/58574
first-stage distinct candidates:               52
first-stage length histogram:                  ((5,1),(6,13),(7,25),(8,12),(9,1))
first candidates attempted:                     1
second-stage calls:                             1
second-stage roots / reachable roots:          67/67
second-stage queue pops / edge scans:          8232/43580
second-stage decomposition cycles/path scans:  67/431
second-stage candidates:                       44
selected deleted vertices / edges:              5/41
selected short/long lengths:                    5/6
selected cocycle pairings / shared vertices:    1/1/0
selected accepted:                             yes
selected matches reference:                    no
independent odd fundamental cycles/pair tests: 24/276
independent pair found/accepted:               no/no
```

The public attack deletes the five vertices of its first cycle, then immediately finds a second odd cycle in the remaining graph. The resulting two cycles are vertex-disjoint, both pair oddly with the public cocycle, fit substantially inside the generation-derived `8/9` bounds, and pass the exact verifier.

## Deterministic sweep

Python 3.12 tested `g19-6x6`, `g19-6x9`, `g19-8x9` over eight independently derived seeds each.

- **24/24** carriers require zero generation retries.
- **24/24** primary attacks accept the very first first-stage candidate and make exactly one second-stage call.
- **24/24** recovered pairs have cocycle pairings `1/1`, zero shared vertices, and exact-verifier acceptance.
- **24/24** recovered pairs differ from the hidden reference after public success.
- Maximum selected lengths are `4/6`, `6/6`, and `6/7` for the three sizes.
- Maximum second-stage edge scans are `9450`, `23146`, and `43485` respectively.
- The independent canonical fundamental-cycle scan succeeds on only `1/8`, `3/8`, and `0/8` instances respectively, i.e. **4/24 total**. This weaker cross-check is preserved as measured evidence rather than upgraded into a claim.

## Result

**G19 is rejected by A-046.** Requiring two simultaneous vertex-disjoint global representatives is still insufficient on this generated torus family. Once one short odd cycle is exposed publicly, deleting its vertices leaves another public odd cycle accessible by the same parity-cover machinery, and both generated bounds are met on every measured instance.

This is not a theorem that arbitrary disjoint noncontractible-cycle problems are easy. It rejects the measured construction and its bound-generation rule. Increasing torus dimensions is not a repair while the same delete-and-recover reduction continues to work.

## G20 gate

G20 must prevent repeated recovery of parallel representatives on a single torus handle. A useful successor should move to multiple independent homology directions—for example a genus-two carrier with several cycles constrained to distinct public cohomology classes and a prescribed disjointness/intersection pattern.

Mandatory attacks include symplectic homology-basis algorithms, vertex-splitting/max-flow and disjoint-path reductions, matching, shortest-cycle methods, separator/treewidth analysis, ILP/SAT/CP-SAT, normalization, equivalent-witness enumeration and generated-role leakage.

No trapdoor/KEM work begins before such a multicurve relation survives these public attacks.

No security claim.
