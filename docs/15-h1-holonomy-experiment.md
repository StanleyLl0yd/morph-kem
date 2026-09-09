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


## H1 result: S3 also collapses completely

The first implementation produced a stronger result than merely "the CSP is small."

The public allowed normalized set is the set of all transpositions in (S_3). But the odd elements of (S_3) are **exactly** those three transpositions.

Therefore, for every edge,

[
x_v T_{uv} x_u^{-1}in {	ext{transpositions}}
]

is equivalent to the single parity equation

[
operatorname{sgn}(x_v)
oplus
operatorname{sgn}(T_{uv})
oplus
operatorname{sgn}(x_u)
=1.
]

There is no hidden residual non-abelian condition.

Once the public Z2 system is solved, choose any fixed even representative for parity 0 and any fixed transposition for parity 1. That lifted (S_3) assignment satisfies the original verifier.

The repository implements this direct attack as:

`recover_s3_via_abelianization`

Its work is linear graph propagation plus public edge verification.

### H-A03 result

**Fatal to H1-S3.**

H1-S3 is mathematically equivalent, for this verifier, to its Z2 abelianization.

The exact CSP implementation remains in the repository as a calibration harness, but it is no longer the best attack.

### Lesson

Using a non-commutative group is not sufficient if the accepted subset is an entire fiber of a cheap quotient homomorphism.

A successor must test the verifier relation against:

- abelianization;
- quotient groups;
- normal subgroups;
- conjugacy-class collapse;
- double-coset simplification;

**before** interpreting non-commutativity as useful complexity.

## H1 disposition

H1-Z2: **rejected as designed**.

H1-S3: **rejected by exact reduction to Z2**.

The next H-series milestone must change the accepted relation, not merely increase graph size.


## Measured CI baseline

Fixed seed, Python 3.12 CI runner:

~~~text
parameters: h1-12
vertices/edges/cycle-rank: 12/18/7
degree histogram: ((2, 3), (3, 6), (4, 3))

Z2 tree recovery accepted: True
Z2 edge checks: 18

S3 parity vertices recovered: 12
S3 direct abelianization recovery accepted: True
S3 direct recovery edge checks: 54

S3 CSP accepted: True
S3 CSP solutions found: 64
S3 CSP nodes/backtracks: 104/0
S3 CSP elapsed seconds: ~0.017
~~~

The direct attack is the meaningful result; CSP timing is only diagnostic.

Scaling sweep with CSP solution cap 8:

| Set | V | E | Cycle rank | Direct S3 | Direct edge checks | CSP nodes | Backtracks |
|---|---:|---:|---:|---:|---:|---:|---:|
| h1-8 | 8 | 12 | 5 | accepted | 36 | 16 | 0 |
| h1-10 | 10 | 15 | 6 | accepted | 45 | 18 | 0 |
| h1-12 | 12 | 18 | 7 | accepted | 54 | 20 | 0 |
| h1-16 | 16 | 24 | 9 | accepted | 72 | 24 | 0 |
| h1-20 | 20 | 30 | 11 | accepted | 90 | 28 | 0 |

This is empirical confirmation of the exact algebraic reduction, not evidence for an asymptotic conjecture.

## Final H1 conclusion

**H1 is rejected.**

The Möbius/Escher intuition is not disproved in general. What is disproved is this particular pairwise edge-transition relation.

The next experiment must not be ordinary finite-group synchronization with a verifier subset that is a fiber/union of fibers of an easy quotient.
