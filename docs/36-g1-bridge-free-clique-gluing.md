# 36 — G1 bridge-free HGES clique-decomposition negative control

## Status

**G1 is rejected by A-028.** Removing G0's dual-bridge shortcut does not hide the allowed pieces: the public tetrahedron dual graph exposes each four-tetrahedron piece as an exact `K4`, and a public exact-cover pass recovers an accepted partition.

This is a generated-distribution falsification result. It is not a theorem about general gluing-equivalence problems and is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Question

G0 was intentionally broken by A-024 because its hidden assembly graph was a tree. Every inter-piece triangular-face gluing became a bridge in the public tetrahedron dual graph, so deleting all bridges recovered the pieces exactly.

G1 asks a narrower question:

> If the exact bridge shortcut is removed, does the same piece family remain publicly decomposable for another structural reason?

The answer on this distribution is yes.

## Construction

The allowed piece is unchanged from G0: the 3-ball obtained from the boundary of a 4-simplex by deleting one tetrahedral facet.

It has four tetrahedra

~~~text
0234
0134
0124
0123
~~~

and four boundary triangle ports

~~~text
234
134
124
123
~~~

Its tetrahedron dual graph is exactly `K4`.

For `n` pieces, G1:

1. creates `n` disjoint copies of the allowed piece;
2. arranges the piece indices in one simple cycle;
3. uses two distinct boundary ports per piece;
4. identifies each paired boundary triangle by the fixed canonical vertex order;
5. forms the vertex quotient;
6. applies an independently seeded global public vertex relabeling;
7. sorts the public tetrahedra;
8. retains the planted partition/cycle/port data only as reference evidence.

The fixed toy sets are:

~~~text
g1-4   4 pieces   16 tetrahedra
g1-8   8 pieces   32 tetrahedra
g1-12 12 pieces   48 tetrahedra
~~~

The master seed affects only the final public relabeling in this calibration. The cycle gluing itself is fixed so that the structural attack question is isolated from rejection-sampling or face-map-distribution effects.

## Public relation

A witness is any partition of all public tetrahedra into `n` four-tetrahedron groups such that:

- every tetrahedron appears exactly once;
- every group is an allowed punctured-4-simplex 3-ball under the same exact local predicate used by G0;
- public triangular-face incidence is at most two;
- exactly `n` triangular faces are shared between distinct candidate groups;
- those cross-group faces define `n` distinct group pairs;
- the cross-group graph is connected and every group has degree two.

Thus the accepted cross-piece graph is a simple cycle.

The verifier never asks whether the submitted cycle or partition is the planted one. Any accepted equivalent witness is attacker success.

## Exact structural counts

For the fixed canonical cycle gluing, CI confirms

~~~text
V = 2n + 2
E = 7n + 1
F = 9n
T = 4n
chi = 1
boundary triangles = 2n
dual edges = 7n
~~~

The dual graph consists of `n` internal `K4` blocks plus `n` inter-piece edges arranged cyclically.

Consequently the measured graph has no bridge and no articulation vertex, but it still has many two-vertex separators and an exact fixed-size clique decomposition.

## A-024 regression gate

The existing G0 bridge attack was re-run unchanged on G1.

For the Python 3.12 `g1-12` baseline:

~~~text
A-024 dual bridges:                    0
A-024 bridge-block witness accepted:  no
articulation points:                   0
~~~

This confirms only that G1 removed the exact G0 bridge shortcut. It is not positive hardness evidence.

## A-028 — public K4 / allowed-piece exact-cover recovery

A-028 uses only the public quotient tetrahedra.

1. Build triangular-face incidence and the tetrahedron dual graph.
2. Enumerate public four-tetrahedron subsets.
3. Keep subsets whose four dual vertices induce a `K4`.
4. Apply the exact allowed-piece predicate to each retained subset.
5. Build the exact-cover relation over public tetrahedra.
6. Enumerate accepted covers up to an explicit solution cap.
7. Submit the first accepted cover to the G1 public verifier.
8. Compare to the planted partition only after public success has already been established.

The implementation intentionally uses transparent exhaustive `4`-subset enumeration for the toy calibration. Candidate size is fixed at four, so this baseline is polynomial fourth-degree work in the tetrahedron count; it is not an optimized clique algorithm.

### Exact Python 3.12 `g1-12` result

~~~text
pieces:                                  12
public V/E/F/T:                          26/85/108/48
Euler characteristic:                   1
boundary faces / max face incidence:    24/2
dual graph vertices / edges:            48/84
A-024 dual bridges:                      0
A-024 bridge-block witness accepted:    no
articulation points:                     0
two-vertex separator pairs:              264
face occurrences:                        192
4-subsets tested:                        194580
dual K4 candidates:                      12
allowed-piece candidates:                12
exact-cover solutions / cap:             1/64
exact-cover cap hit:                     no
exact-cover nodes / backtracks:          13/0
reference witness accepted:              yes
A-028 public witness accepted:            yes
matches planted partition up to order:   yes
~~~

A-028 therefore finds exactly the twelve planted-size public clique candidates and needs no exact-cover backtracking.

## Multi-size / multi-seed sweep

The Python 3.12 workflow tested all three parameter sets across eight independently derived public relabel seeds each. All **24/24** A-028 recoveries were accepted and all **24/24** matched the planted partition up to group order.

Per-size counters were invariant under the public relabeling, as expected:

| Set | V/E/F/T | Dual edges | Bridges | Articulations | 2-vertex separators | 4-subsets | K4 / allowed | Covers | Cover nodes/backtracks |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| g1-4 | 10/29/36/16 | 28 | 0 | 0 | 24 | 1,820 | 4 / 4 | 1 | 5 / 0 |
| g1-8 | 18/57/72/32 | 56 | 0 | 0 | 112 | 35,960 | 8 / 8 | 1 | 9 / 0 |
| g1-12 | 26/85/108/48 | 84 | 0 | 0 | 264 | 194,580 | 12 / 12 | 1 | 13 / 0 |

The dedicated G1 workflow succeeded on Python 3.11, 3.12, and 3.13. The Python 3.12 job also completed the full 24-instance sweep.

## Interpretation

**G1 is rejected.** The result isolates an important methodological point:

- G0 failed because the *assembly edges* were canonical graph bridges;
- G1 removes those bridges and even removes articulation vertices;
- nevertheless the *pieces themselves* remain canonical fixed-size dual cliques;
- public decomposition is therefore still immediate.

The disappearance of one separator class must never be promoted to evidence of a hard gluing problem while another cheap canonical representation remains.

Increasing the number of cycle pieces cannot repair this structural leak. The transparent exhaustive implementation already has fixed-degree polynomial work, and the construction exposes the exact candidate blocks before the exact-cover phase does meaningful search.

## Next gate

The next HGES stage must change the structural family rather than scale G1. A useful G2 should make the planted pieces non-canonical in the public dual graph, for example through controlled overlap, subdivision, mixed local piece types, or a construction in which an accepted witness is not simply a partition into maximal fixed-size cliques.

Before any trapdoor work, G2 must still face:

- bridge/articulation/low-order separator decomposition;
- maximal subcomplex / clique / motif enumeration;
- local apex, boundary-port, and incidence-role signatures;
- piece automorphism normalization;
- exact-cover / SAT / CP-SAT recovery;
- equivalent-witness enumeration;
- statistical leakage of planted roles.

No security claim.
