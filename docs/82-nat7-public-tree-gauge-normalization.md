# 82 — NAT7 public spanning-tree gauge-normalization closure

## Status

**NAT7 is an architecture-level falsification/control experiment.** It formalizes the generic part of the NAT6 break: on a public connected carrier, an arbitrary normalized vertex gauge is removable by deterministic public spanning-tree integration. The statement does **not** require face flatness.

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

It provides:

1. deterministic BFS spanning-tree integration;
2. public residual normalization;
3. exact reconstruction;
4. normalized vertex-gauge transformation for invariance tests;
5. tree/non-tree and residual-work measurements.

The implementation does not inspect NAT6 secret/reference data.

## NAT6 regression

The first executable regression uses the already merged irregular-torus `A5` public connections because they contain genuine nontrivial global holonomy.

For each `6x6`, `6x9`, and `8x9` public instance:

- normalize the original public edge connection;
- independently sample a second normalized vertex gauge and regauge the same public connection;
- normalize the regauged presentation;
- require the same public spanning tree and **identical complete residual vector**;
- reconstruct both presentations exactly;
- compare the generic residual vector against NAT6's earlier specialized tree-normalization implementation.

The comparison gauge is test instrumentation only; the normalizer itself receives no reference witness.

## Gate / architectural closure

If the generic harness passes these exact identities on the declared sweep, retire **vertex gauge on a public connected carrier** as a hardness source.

Future NAT work may still investigate a hard residual representation/noisy global-holonomy inversion problem, but must not claim secrecy from the gauge variables themselves. Increasing group size, genus, vertex count, or changing the local gauge distribution cannot repair this normalization identity.

This closure does not claim that arbitrary residual global representations are easy to invert. NAT6's direct `H^1` solve remains a family-specific attack on its particular residual representation.

No security claim.