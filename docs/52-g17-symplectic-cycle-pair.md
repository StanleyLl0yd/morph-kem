# 52 — G17 primal-dual symplectic cycle-pair negative control

## Status

G17 is the first HGES control whose witness predicate is explicitly bilinear in two independently global cycles.

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

On the torus the homological intersection form has rank two. The measured graph-cycle pairing matrix is expected to expose this rank-two quotient even though the primal and dual graph cycle spaces are much larger.

## Toy sets

```text
g17-6x6: 36 vertices / 108 edges / 72 triangles
g17-6x9: 54 vertices / 162 edges / 108 triangles
g17-8x9: 72 vertices / 216 edges / 144 triangles
```

Each carrier is independently edge-flip irregularized and globally relabelled before publication.

## Rejection gate

If tree-cotree decomposition routinely returns an accepted exact-one-crossing pair, G17 is rejected. The complete crossing matrix serves as an independent semantic/algebraic check.

Exact measurements are appended only after the dedicated Python 3.12 baseline and multi-seed sweep complete.

No trapdoor/KEM work begins here. No security claim.
