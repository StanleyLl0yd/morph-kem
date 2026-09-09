# 15 — H1 signed-holonomy experiment

## Status

H1 is an executable falsification experiment for the H-series.

It is **not** a KEM, trapdoor primitive, or security candidate.

The question is:

> Does Möbius/Escher-like global transition structure remain difficult after gauge fixing, cycle analysis, abelianization, and exact constraint solving?

## Prior-art warning: this resembles group synchronization

Recovering unknown group elements at graph vertices from public pairwise group relations is a well-studied problem usually called **group synchronization**.

Relevant prior art:

- Gilad Lerman, Yunpeng Shi, *Robust Group Synchronization via Cycle-Edge Message Passing*, Foundations of Computational Mathematics 2021:
  https://link.springer.com/article/10.1007/s10208-021-09532-w
- Bradley Stich, *Strong Recovery In Group Synchronization*, 2021:
  https://arxiv.org/abs/2111.03705
- *Higher-order group synchronization*, Research in the Mathematical Sciences, 2026:
  https://link.springer.com/article/10.1007/s40687-026-00627-w

Cycle consistency and recovery up to a common global group action are standard features of this literature.

Therefore H1 is **not proposed as a novel cryptographic problem**. It is a calibration step intended to identify exactly which extra structure would be needed beyond ordinary group synchronization.

## H1 scaffold

The first executable H1 intentionally uses a finite connected graph rather than a true hyperbolic surface.

Generation begins from a cycle and adds deterministic pseudo-random chords. This gives:

- connectedness;
- multiple independent cycles;
- locally tree-like branching at small radii;
- no claim of being a genuine finite quotient of a hyperbolic tiling.

True `{p,q}` quotients remain gated to a later H-series milestone. Adding metric Lobachevsky geometry before the algebraic baseline survives would only add complexity without evidence of hardness.

For a connected graph:

[
r = |E|-|V|+1
]

is the cycle rank.

## H1-Z2 calibration

### Generation

Each vertex receives a hidden bit (g_v).

A deterministic public spanning tree is selected. In canonical hidden gauge:

- tree edges carry 0;
- non-tree edges carry deterministic target bits.

The public edge label for edge ((u,v)) is:

[
T_{uv}=g_uoplus a_{uv}oplus g_v.
]

The public object contains:

- graph;
- public edge labels;
- ordered non-tree target bits.

### Equivalent witness

Any vertex-bit assignment (x_v) is accepted if gauge-normalizing all tree edges gives 0 and the ordered non-tree values equal the public cycle target.

The planted (g_v) is only a reference witness.

### Attack H-A01 / H-A02

Fix one root bit and propagate along the public spanning tree.

This recovers one representative of the entire gauge orbit in (O(|V|+|E|)) work.

The non-tree values are exactly the fundamental-cycle signature.

**Expected result: H1-Z2 is completely broken.**

This is the intended calibration.

## H1-S3

### Transition group

[
G=S_3.
]

Elements are serialized as permutations of three symbols.

The allowed normalized edge set is the conjugacy class of the three transpositions.

### Generation

Choose hidden frames (g_vin S_3).

For every canonical public edge ((u,v)), choose a transposition (a_{uv}) and publish:

[
T_{uv}=g_v^{-1}a_{uv}g_u.
]

The reference frames satisfy:

[
g_vT_{uv}g_u^{-1}=a_{uv},
]

so every normalized transition is a transposition.

### Equivalent witness

Any frame assignment (x_vin S_3) is accepted if for every public edge:

[
x_vT_{uv}x_u^{-1}
]

is a transposition.

The verifier never asks for the planted frame assignment.

Because the allowed set is a conjugacy class, common left multiplication gives a global gauge symmetry. The exact solver fixes vertex 0 to the identity only to choose one representative.

## H-A03 — abelianization leak

The sign homomorphism gives:

[
S_3/[S_3,S_3]congmathbb Z_2.
]

A transposition has odd parity, so every edge exposes:

[
operatorname{sgn}(x_v)
oplus
operatorname{sgn}(T_{uv})
oplus
operatorname{sgn}(x_u)
=1.
]

Thus one parity bit per vertex is recoverable by graph propagation up to a global flip.

The H1 solver uses this attack first, reducing each (S_3) domain from 6 elements to 3.

## H-A05 — exact CSP

After abelianization, H1 solves the remaining finite-domain CSP directly.

Implementation:

- root gauge fixed to identity;
- 3-element parity-compatible domains;
- exact binary edge compatibility;
- repeated arc-consistency pruning;
- minimum-remaining-values variable selection;
- bounded equivalent-solution enumeration.

Metrics:

- search nodes;
- backtracks;
- solutions found;
- solution-cap hit;
- mean domain after abelianization.

## What H1 does not yet implement

The first calibration does not yet claim or implement:

- a true hyperbolic `{p,q}` quotient;
- non-orientable polygon gluings;
- explicit 2-cell holonomy relations;
- non-manifold junctions;
- canonical-labeling attack;
- SAT/SMT backend;
- treewidth computation.

Those are justified only if the basic non-abelian synchronization relation survives exact CSP attack.

## Exit criteria

H1 is rejected as a hardness direction if:

- Z2 behaves as predicted and linearizes completely;
- S3 is cheaply solved across the toy ladder;
- abelianization plus local propagation removes most search;
- equivalent satisfying witnesses are abundant.

If rejected, H2 must change the **relation**, not merely use a larger finite group or a prettier hyperbolic drawing.

## Security status

No one-wayness, post-quantum, IND-CPA, IND-CCA, or concrete-security claim exists.
