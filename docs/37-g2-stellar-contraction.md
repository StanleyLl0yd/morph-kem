# 37 — G2 stellar-subdivision HGES contraction negative control

## Status

**G2 is an attack calibration in progress. No hardness or security conclusion is permitted until the dedicated exact-head workflow records A-029.**

G2 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Question

G1 removed G0's dual-bridge shortcut but still exposed every hidden piece as one exact four-tetrahedron `K4` in the public tetrahedron dual graph. A-028 therefore recovered the piece partition directly.

G2 makes one deliberately cosmetic-looking change: stellar-subdivide every macro tetrahedron before publication.

The test is not whether the literal G1 `K4` disappears. It is whether the subdivision has a cheap public inverse that reconstructs the same easy macro-complex.

## Construction

Start with the G1 macro distribution: punctured-4-simplex 3-ball pieces glued in one simple bridge-free cycle.

For every public macro tetrahedron `(a,b,c,d)`, insert one fresh center vertex `x` and replace the tetrahedron by

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

Stellar subdivision of each of the `4n` macro tetrahedra adds one vertex, four center-to-corner edges, six internal center-edge faces and three net tetrahedra. Therefore G2 predicts

~~~text
V = 6n + 2
E = 23n + 1
F = 33n
T = 16n
chi = 1
boundary triangles = 2n
micro dual edges = 31n
~~~

These are deterministic construction identities for the current toy family, not hardness evidence.

## A-028 regression

A stellar center together with the four micro tetrahedra in its star is itself a four-vertex clique in the micro tetrahedron dual graph and satisfies the old four-tetrahedron local piece predicate.

Therefore G2 does **not** aim to eliminate all micro-level `K4` motifs. Instead it changes their granularity: there are `4n` macro-tetrahedron stars, while an accepted G2 witness needs `n` sixteen-tetrahedron pieces.

The old G1 A-028 attack is re-run on `g2-4` as a regression. It must not directly return an accepted G2 piece-level partition.

## A-029 — public stellar-center contraction + macro recovery

A-029 uses only public incidence.

1. Enumerate every public vertex and the tetrahedra in its star.
2. Keep a vertex when its star contains exactly four tetrahedra and deleting the candidate center from those tetrahedra yields exactly the four triangular faces of one tetrahedron.
3. Treat every retained star as a candidate stellar contraction.
4. Solve the exact cover of public micro tetrahedra by candidate center stars, with an explicit solution cap.
5. Contract one public center-star cover to a macro tetrahedron list.
6. Run the G1 macro dual-`K4` / allowed-piece exact-cover attack on that contracted public macro complex.
7. Lift the recovered macro-piece partition back to micro tetrahedra.
8. Submit the lifted partition to the exact G2 verifier.
9. Compare candidate centers and recovered pieces with planted reference roles only after the public attack has succeeded.

If this attack succeeds cheaply, G2 is rejected. Increasing the number of stellar-subdivided pieces is not a repair because the representation change has a public inverse on the generated family.

## Measurements

The dedicated workflow records:

- public micro `V/E/F/T`, Euler characteristic, boundary faces and max face incidence;
- micro dual edges, bridges, articulation points and two-vertex separator count;
- public vertex-star histogram;
- candidate center count and post-attack false-positive/miss count against reference roles;
- center-star exact-cover solutions/cap/nodes/backtracks;
- reconstructed macro tetrahedron count and macro `V/E/F/T`;
- macro dual edges, `K4` candidates and allowed-piece candidates;
- macro exact-cover solutions/nodes/backtracks;
- exact G2 verifier acceptance and post-success reference comparison;
- deterministic all-size/eight-seed sweep.

## Rejection gate

Reject G2 if A-029 finds any accepted public witness with practical toy work. Exact recovery of the planted representative is not required.

If center-star ambiguity appears, enumerate it up to the explicit cap and treat multiple accepted contractions as additional attacker freedom, not as protection.

## Successor gate

If G2 is rejected as expected, G3 must stop using a transformation with an obvious local inverse. A useful successor must make macro-piece boundaries genuinely noncanonical or overlapping, while immediately facing:

- low-order separator and decomposition attacks;
- motif/subcomplex enumeration;
- local role and boundary-signature leakage;
- automorphism normalization;
- exact-cover / SAT / CP-SAT recovery;
- equivalent-witness multiplicity;
- statistical leakage of planted roles.

No trapdoor work is justified merely because literal `K4` pieces or stellar centers are no longer obvious.

No security claim.
