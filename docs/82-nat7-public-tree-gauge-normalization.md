# 82 — NAT7 public spanning-tree gauge-normalization closure

## Status

**NAT7 closes normalized vertex gauge on a public connected carrier as a hardness source.** Deterministic public spanning-tree integration removes that gauge exactly. The algebraic identity does **not** require flatness; the executable NAT6 regression confirms exact normalization, reconstruction and gauge invariance over the declared 24-instance sweep.

NAT7 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Generic public connection

Let a public connected graph have canonically oriented edges `e=(u,v)` and public labels `A_e` in any group `G`. Choose a deterministic public spanning tree rooted at vertex zero.

Define public tree-integration labels `t_v` by

```text
t_0 = 1,
t_v = t_u A_uv
```

when the tree traversal follows the stored edge orientation, using `A_uv^-1` when it traverses in reverse.

For every public edge define the tree-normalized residual

```text
R_uv = t_u A_uv t_v^-1.
```

Every tree edge has `R_uv = 1` by construction. Every non-tree residual is the holonomy of the corresponding public fundamental cycle.

The original public connection is recovered exactly from

```text
A_uv = t_u^-1 R_uv t_v.
```

No flatness assumption appears anywhere in this normalization/reconstruction identity.

## Gauge invariance

Apply any **normalized** vertex gauge `h` with `h_0=1`:

```text
A'_uv = h_u^-1 A_uv h_v.
```

Deterministic integration on the same public tree yields

```text
t'_v = t_v h_v,
```

therefore

```text
R'_uv = t'_u A'_uv (t'_v)^-1 = R_uv.
```

So the complete residual connection is exactly invariant under normalized vertex gauge. If the root gauge is not fixed, the residuals are only simultaneously conjugated by the root value; fixing one public root removes even that global ambiguity.

This is stronger than NAT6: **hidden vertex gauge cannot itself supply hardness for any public group-valued connection on a connected carrier.** Flatness only constrains the surviving residual holonomies.

## NAT-A009 generic harness

`nat_tree_gauge.py` uses only a minimal group interface:

- identity;
- multiplication;
- inverse;
- equality of elements.

It provides deterministic BFS tree integration, public residual normalization, exact reconstruction, normalized vertex-regauging for invariance tests, and explicit tree/non-tree work counters. It receives no NAT6 reference witness.

## Fixed Python 3.12 regression

Using the already merged `nat6-8x9` irregular-torus public connection:

```text
vertices / edges:                              72 / 216
tree / non-tree edges:                         71 / 145
tree assignments:                                     71
tree identity residuals:                              71
nonidentity residuals:                                36
distinct nonidentity residuals:                        3
exact reconstruction:                               yes
independently regauged reconstruction:               yes
same deterministic tree after normalized gauge:      yes
identical complete residual vector after regauge:     yes
```

The generic residual vector also matches NAT6's earlier specialized tree-normalization implementation in the unit regression.

## Deterministic 24-instance sweep

Python 3.12 tests `nat6-6x6`, `nat6-6x9`, and `nat6-8x9` over eight seeds each. For **24/24** public connections:

- tree assignments equal exactly `V-1`;
- every tree residual is identity;
- the original connection reconstructs exactly;
- an independently sampled normalized vertex regauge reconstructs exactly;
- the deterministic public spanning tree is unchanged;
- the **entire residual-label vector is identical** before and after regauging.

Tree/non-tree sizes are respectively `35/73`, `53/109`, and `71/145`. The number of distinct nonidentity residual group elements is three on every measured NAT6 torus instance; that final fact is NAT6-family-specific and is not required by the generic normalization theorem.

Dedicated NAT7 CI passes on Python 3.11, 3.12 and 3.13 on the measured head.

## Architectural closure

**Retire vertex gauge on a public connected carrier as a hardness source.** Future NAT work may still investigate a hard residual representation/noisy global-holonomy inversion problem, but must not claim secrecy from the gauge variables themselves.

Increasing group size, genus, vertex count, or changing the local gauge distribution cannot repair this normalization identity. The public gauge degrees of freedom are canonically removable before attacking the residual problem.

This closure does **not** claim that arbitrary residual global representations are easy to invert. NAT6's direct `H^1` solve remains a family-specific attack on its particular residual representation.

No security claim.