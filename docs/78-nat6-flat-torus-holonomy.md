# 78 — NAT6 flat-torus A5 global-holonomy control

## Status

**NAT6 is a falsification experiment in progress.** NAT3/NAT5 fail because non-flat sphere noise leaves curvature support. NAT4 fails because an exactly flat connection on a simply connected sphere is pure vertex gauge. NAT6 changes the carrier to an irregular torus so flat connections can carry genuine global holonomy.

NAT6 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Construction

Reuse the G16 flip-mixed irregular torus families `6x6`, `6x9`, and `8x9`. From the public triangulation compute two deterministic independent binary 1-cocycles `alpha,beta` spanning `H^1(T^2; F2)` modulo coboundaries.

Choose a seeded ordered pair of distinct commuting involutions `x,y in A5`. These generate a Klein-four subgroup. For each canonically oriented public edge `e=(u,v)` define

```text
c_e = x^alpha[e] y^beta[e].
```

Because `alpha,beta` are cocycles and `x,y` commute with order two, every triangular face has identity core holonomy while noncontractible torus cycles can retain nontrivial global holonomy.

Hide the core under a normalized seeded vertex gauge `g_v in A5`:

```text
observed_uv = g_u^-1 c_uv g_v,
g_0 = 1.
```

The verifier accepts any normalized `A5` gauge and any ordered pair of distinct commuting involutions that exactly reproduces all public edges. It never compares to the planted decomposition.

## NAT-A007

The public attack has two parts.

First, choose a deterministic spanning tree and integrate the observed connection as though the tree core were identity. Gauge-transform every public edge by this tree integration. All tree residuals become identity; non-tree residuals expose the finite set of global loop holonomies.

Second, enumerate the complete public set of ordered distinct commuting involution pairs in `A5`. For each pair:

1. build the public core labels from `alpha,beta`;
2. propagate the unique normalized vertex gauge along the public spanning tree;
3. recompute every public edge exactly;
4. retain every verifier-accepted decomposition.

There are only 30 ordered legal holonomy pairs in `A5`. The attack does not enumerate vertex-label assignments.

## Measurements

Record:

- V/E/F, Euler characteristic and edge-incidence range;
- public `H^1` dimension and alpha/beta weights;
- nonidentity face-holonomy count;
- tree/non-tree edge counts;
- nonidentity and distinct tree-normalized residual holonomies;
- total commuting-pair candidates and candidates tested;
- vertex-gauge propagation assignments;
- accepted decompositions;
- post-success planted pair/gauge equality;
- deterministic all-size/multi-seed curves.

## Gate

Reject NAT6 if tree normalization plus constant-size global-holonomy enumeration routinely yields a verifier-accepted decomposition. Such a result means that changing the topology from sphere to torus turns pure gauge into a small public representation-of-the-fundamental-group problem rather than a hidden trapdoor.

If this gate survives, representation quotients, larger nonabelian holonomy families, conjugacy normalization and generic constraint solving remain mandatory. Survival would not be evidence of one-wayness.

No security claim.
