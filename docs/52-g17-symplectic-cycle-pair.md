# 52 — G17 primal-dual symplectic cycle-pair negative control

## Status

**G17 is rejected by A-044.** It is the first HGES control whose witness predicate is explicitly bilinear in two independently global cycles.

The carrier is an irregular closed triangulated torus. A witness consists of one simple cycle in the public primal graph and one simple cycle in the public triangle-dual graph. The verifier accepts exactly when their primal-dual crossing count is odd.

This is a falsification experiment, not a hardness claim or cryptographic primitive.

## Why G17 exists

G16 removed bounded-radius local witnesses but still failed because a public nontrivial cocycle is a linear functional on a public cycle space. A spanning-tree fundamental-cycle basis therefore exposed a valid witness immediately.

G17 removes the single affine equation. The intersection predicate

```text
I(p,d) = 1 mod 2
```

is bilinear in a primal cycle `p` and a dual cycle `d`.

## A-044 — public tree-cotree one-crossing recovery

Attack-first analysis gives a stronger public construction than generic bilinear solving.

Choose a public primal spanning tree `T`. Delete from the dual graph every dual edge crossing `T`, then choose a public dual spanning tree `T*` in what remains. On a closed genus-`g` orientable surface exactly `2g` primal edges lie in neither `T` nor the set crossed by `T*`. The torus therefore leaves exactly two edges.

For any leftover edge `e`, its primal fundamental cycle relative to `T` and the dual fundamental cycle of the crossing edge `e*` relative to `T*` intersect exactly once. The reason is structural: the primal path uses only edges of `T`, while the dual tree was forbidden from crossing `T`; the only common primal/dual crossing index is the leftover edge itself.

The implementation submits this pair to the exact verifier and requires exact crossing count `1`, not merely odd parity.

## Independent full-basis cross-check

Independently build ordinary public spanning trees in the primal and dual graphs, enumerate all simple fundamental cycles, and construct the complete GF(2) crossing matrix between the two bases. Measure its dimensions, weight and rank, scan the first odd entry, and exact-verifier-check that pair.

On the torus the homological intersection form has rank two. The measured graph-cycle pairing matrix exposes this rank-two quotient even though the primal and dual graph cycle spaces are much larger.

## Toy sets

```text
g17-6x6: 36 vertices / 108 edges / 72 triangles
g17-6x9: 54 vertices / 162 edges / 108 triangles
g17-8x9: 72 vertices / 216 edges / 144 triangles
```

Each carrier is independently edge-flip irregularized and globally relabelled before publication.

## Fixed Python 3.12 result

Fixed `g17-8x9`:

```text
successful carrier flips:                 72
public V/E/F:                              72/216/144
Euler characteristic / edge incidence:    0 / 2..2
primal degree histogram:                  ((3,5),(4,11),(5,17),(6,15),(7,5),(8,11),(9,5),(10,3))
dual degree histogram:                    ((3,144),)
normalization-improving legal flips:       59
primal tree / dual cotree edges:           71/143
forbidden dual edges:                      71
tree-cotree leftover edges:                2
primary primal / dual path scans:          9/23
primary primal / dual cycle lengths:       10/24
primary exact crossing count / parity:     1/1
primary exact verifier accepted:           yes
primary pair matches reference:            no
full primal / dual basis cycles:           145/73
full primal / dual path scans:             657/779
crossing matrix dimensions:                145 x 73
crossing matrix weight:                    550
crossing matrix GF(2) rank:                2
crossing matrix row XORs:                  48
full-basis pairs tested to first odd:       230
full-basis selected cycle lengths:         8/19
full-basis selected crossing count:        1
full-basis exact verifier accepted:        yes
```

The primary tree-cotree pair is therefore obtained directly from two public spanning trees and one of exactly two leftover edges. No generic SAT, ILP or pair search is needed.

## Eight-seed sweep

Python 3.12 over all three sizes × eight deterministic seeds gives:

- **24/24** tree-cotree decompositions with exactly two leftover edges;
- **24/24** primary witnesses with exact crossing count `1`;
- **24/24** primary witnesses accepted by the exact verifier;
- **24/24** primary witnesses different from the canonical second-leftover reference pair;
- **24/24** full-basis crossing matrices with GF(2) rank exactly `2`;
- **24/24** independent full-basis witnesses accepted by the exact verifier.

Maximum primary public path work remains small:

```text
g17-6x6: primal path <= 7 edges, dual path <= 17 edges
g17-6x9: primal path <= 8 edges, dual path <= 24 edges
g17-8x9: primal path <= 8 edges, dual path <= 31 edges
```

The complete-basis cross-check is intentionally heavier but still small at these toy sizes. The maximum row-major pairs examined before its first odd entry are 192, 565 and 1251 respectively. Full crossing-matrix dimensions are seed-invariant: `73 x 37`, `109 x 55`, `145 x 73`, and the measured rank is always two.

## Result

**G17 is rejected by A-044.** Moving from a single affine cohomology condition to a bilinear global intersection condition does not create hardness when the public cellular embedding exposes a standard tree-cotree decomposition. On the torus, the decomposition constructively returns two homology handles; either leftover edge supplies a primal/dual simple-cycle pair with exactly one crossing.

The result is stronger than merely observing that a solver succeeds: the generated relation has a direct public topological construction. Increasing torus dimensions, carrier flip counts or generic solver budgets cannot repair that structural failure.

G18 must require geometric information not determined by the mod-2 homology intersection form—for example internally vertex-disjoint representatives, constrained lengths, or a prescribed geometric-intersection pattern not supplied automatically by tree-cotree. Such a successor must immediately face disjoint-path/flow/matching, shortest noncontractible-cycle algorithms, ILP/SAT/CP-SAT, separator/treewidth methods, normalization and equivalent-witness enumeration.

No trapdoor/KEM work begins here. No security claim.
