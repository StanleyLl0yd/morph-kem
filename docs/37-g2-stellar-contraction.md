# 37 — G2 stellar-subdivision HGES contraction negative control

## Status

**G2 is rejected by A-029 on the measured generated distribution.** Public stellar-center recognition contracts the micro triangulation back to the same easy G1 macro-complex, after which the macro `K4`/allowed-piece recovery reconstructs an accepted G2 witness.

G2 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Question

G1 removed G0's dual-bridge shortcut but still exposed every hidden piece as one exact four-tetrahedron `K4` in the public tetrahedron dual graph. A-028 therefore recovered the piece partition directly.

G2 makes one deliberately cosmetic-looking change: stellar-subdivide every macro tetrahedron before publication.

The test is not whether the literal G1 piece-level `K4` disappears. It is whether the subdivision has a cheap public inverse that reconstructs the same easy macro-complex.

## Construction

Start with the G1 macro distribution: punctured-4-simplex 3-ball pieces glued in one simple bridge-free cycle.

For every macro tetrahedron `(a,b,c,d)`, insert one fresh center vertex `x` and replace the tetrahedron by

~~~text
xabc
xabd
xacd
xbcd
~~~

The old triangular faces remain as external faces of the stellar children. Hence the inter-macro and inter-piece face gluings are preserved exactly, but one macro tetrahedron becomes four micro tetrahedra.

For `n` pieces the fixed toy sets are:

~~~text
g2-4   4 pieces   16 macro tetrahedra    64 micro tetrahedra
g2-6   6 pieces   24 macro tetrahedra    96 micro tetrahedra
g2-8   8 pieces   32 macro tetrahedra   128 micro tetrahedra
~~~

After subdivision, all vertices are independently globally relabeled from the deterministic master seed and the micro tetrahedra are sorted. Planted piece labels, macro-tetrahedron roles and center roles are reference-only.

## Public relation

A witness is any partition of all public micro tetrahedra into `n` groups such that:

- every micro tetrahedron occurs exactly once;
- every group contains 16 micro tetrahedra;
- within each group the micro tetrahedra admit four disjoint stellar-center stars;
- contracting those four stars yields one valid G0/G1 punctured-4-simplex piece;
- public triangular-face incidence is at most two;
- exactly `n` faces cross candidate piece groups;
- those cross-piece faces define one connected simple cycle.

The verifier does not compare candidate centers, macro tetrahedra, piece labels or cycle order to generation history. Any accepted equivalent witness is attacker success.

## Structural counts

The G1 macro family has

~~~text
V = 2n + 2
E = 7n + 1
F = 9n
T = 4n
~~~

Stellar subdivision of each of the `4n` macro tetrahedra adds one vertex, four center-to-corner edges, six internal center-edge faces and three net tetrahedra. Therefore G2 has

~~~text
V = 6n + 2
E = 23n + 1
F = 33n
T = 16n
chi = 1
boundary triangles = 2n
micro dual edges = 31n
~~~

The dedicated workflow confirms these identities on all fixed sets. They are construction facts, not hardness evidence.

## A-028 regression

A stellar center together with the four micro tetrahedra in its star is itself a four-tetrahedron `K4` in the micro tetrahedron dual graph and satisfies the old four-tetrahedron local piece predicate.

Therefore G2 does **not** eliminate all micro-level `K4` motifs. Instead it changes their granularity: there are `4n` macro-tetrahedron stars, while an accepted G2 witness needs `n` sixteen-tetrahedron pieces.

On `g2-4`, the old A-028 regression finds exactly 16 dual `K4` / allowed four-tetrahedron candidates but does not produce an accepted G2 piece-level witness.

That regression is not positive evidence. Those sixteen small motifs are precisely the data used by A-029 to undo the subdivision.

## A-029 — public stellar-center contraction + macro recovery

A-029 uses only public incidence.

1. Enumerate every public vertex and the tetrahedra in its star.
2. Keep a vertex when its star contains exactly four tetrahedra and deleting the candidate center from those tetrahedra yields exactly the four triangular faces of one tetrahedron.
3. Treat every retained star as a candidate stellar contraction.
4. Solve the exact cover of public micro tetrahedra by candidate center stars, with an explicit solution cap.
5. Contract a public center-star cover to a macro tetrahedron list.
6. Run the G1 macro dual-`K4` / allowed-piece exact-cover attack on that contracted public macro complex.
7. Lift the recovered macro-piece partition back to micro tetrahedra.
8. Submit the lifted partition to the exact G2 verifier.
9. Compare candidate centers and recovered pieces with planted reference roles only after the public attack has succeeded.

## Exact Python 3.12 `g2-8` result

~~~text
pieces:                                  8
public micro V/E/F/T:                    50/185/264/128
Euler characteristic:                   1
boundary faces / max face incidence:    16/2
micro dual vertices / edges:             128/248
micro dual bridges:                       0
micro articulation points:                0
micro two-vertex separator pairs:        112
micro face occurrences:                  512
vertex-star histogram:                   4:32 / 12:8 / 18:8 / 72:2
candidate stellar centers:                32
candidate-center false positives/misses:   0/0
center exact-cover solutions / cap:        1/64
center exact-cover nodes / backtracks:    33/0
reconstructed macro tetrahedra:           32
contracted macro V/E/F/T:                18/57/72/32
contracted macro dual edges:              56
macro K4 candidates:                       8
macro allowed-piece candidates:            8
macro exact-cover solutions:                1
macro exact-cover nodes / backtracks:       9/0
reference witness accepted:               yes
A-029 public witness accepted:             yes
matches planted partition up to order:    yes
~~~

The center-role leak is especially direct on this family: exactly the 32 planted stellar centers are the public vertices with valid four-tetrahedron tetrahedral-boundary stars; there are no false positives or misses on the baseline.

## Deterministic sweep

Python 3.12 tested `g2-4`, `g2-6`, and `g2-8` over eight independently derived deterministic seeds each. All **24/24** A-029 recoveries were accepted and all **24/24** matched the planted piece partition up to group order.

The measured per-size attack structure is deterministic under the public relabeling:

| Set | Micro V/E/F/T | Dual edges | Bridges / articulations | 2-vertex separators | Centers | False/missed | Center cover nodes/backtracks | Macro K4/allowed | Macro cover nodes/backtracks | Accepted/matched |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| g2-4 | 26/93/132/64 | 124 | 0 / 0 | 24 | 16 | 0 / 0 | 17 / 0 | 4 / 4 | 5 / 0 | 8/8 |
| g2-6 | 38/139/198/96 | 186 | 0 / 0 | 60 | 24 | 0 / 0 | 25 / 0 | 6 / 6 | 7 / 0 | 8/8 |
| g2-8 | 50/185/264/128 | 248 | 0 / 0 | 112 | 32 | 0 / 0 | 33 / 0 | 8 / 8 | 9 / 0 | 8/8 |

Each center exact cover and each macro exact cover has one measured solution under the cap and zero backtracking. Exact agreement with the planted partition is stronger than required; any accepted equivalent witness would already reject the candidate.

## Result

**G2 is rejected by A-029.**

Stellar subdivision changes the representation but not the effective public recovery problem on this generated family. The subdivision centers have a canonical public local signature, contraction reconstructs the G1 macro complex, and the already-fatal A-028 macro decomposition then applies unchanged.

Do not increase the number of pieces, micro tetrahedra, or repeated subdivisions as a repair. A larger instance preserves the same recognizable center-star relation and therefore only scales a publicly invertible representation layer.

This is not a theorem that general HGES is easy. It falsifies this subdivision-based generated distribution and establishes a stronger design requirement: the next stage must avoid both canonical piece motifs **and** an obvious public local inverse that restores them.

## G3 gate

A useful G3 must make macro-piece boundaries genuinely noncanonical or overlapping rather than wrapping the same decomposition in a locally reversible subdivision. Before any positive interpretation it must face:

- bridge, articulation and low-order separator decomposition;
- motif/subcomplex enumeration at several scales;
- local role, link and boundary-signature leakage;
- public simplification/contraction and bistellar normalization;
- piece automorphism normalization;
- exact-cover / SAT / CP-SAT recovery;
- equivalent-witness multiplicity;
- statistical leakage of planted roles.

A disappearance of literal `K4` blocks or degree-4 stellar centers alone is not a success condition. No trapdoor work is justified until a generated distribution survives these public attacks and a separate secret recovery advantage can be defined.

No one-wayness, average-case hardness, post-quantum hardness, IND-CPA, IND-CCA, KEM, or production-security claim exists.
