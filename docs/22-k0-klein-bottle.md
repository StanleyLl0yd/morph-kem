# 22 — K0 Klein-bottle orientation control

## Status

K0 is an executable **negative control** for the non-orientable branch.

It is not a KEM, one-way function, trapdoor primitive, or security candidate.

The question is deliberately narrow:

> does hiding local orientation labels on a genuine non-orientable surface create any asymmetry beyond a public Z2 gauge problem?

The expected answer is no.

## 1. Exact quotient

K0 constructs a rectangular triangular grid with periodic horizontal identification and the top/bottom identification

~~~text
(x, height) ~ (-x, 0)
~~~

directly at the vertex-incidence level.

The code checks the resulting finite simplicial complex rather than relying on a drawing.

For a width x height grid:

~~~text
V = width * height
E = 3 * width * height
F = 2 * width * height
chi = V - E + F = 0
~~~

Every primal edge is incident to exactly two triangles and there are no free collapse pairs.

## 2. Orientation cocycle

Every triangle receives a deterministic canonical local orientation from its ordered vertices.

For each shared edge, K0 computes one bit saying whether the two canonical face orientations must be relatively flipped in order to induce opposite directions on that edge.

Let that canonical public bit be b_fg.

A global orienting assignment x_f would need to solve

~~~text
x_f XOR x_g = b_fg
~~~

on every dual edge.

K0 solves this system by public spanning-tree propagation. The residual non-tree XOR values are the fundamental-cycle orientation syndromes.

At least one non-zero syndrome means the local orientation equations have no global solution.

## 3. Hidden-gauge calibration

Generation adds one secret/reference gauge bit phi_f per triangle and publishes

~~~text
T_fg = b_fg XOR phi_f XOR phi_g
~~~

This is intentionally a weak model.

The scaffold itself publicly determines b_fg, so an attacker obtains

~~~text
T_fg XOR b_fg = phi_f XOR phi_g.
~~~

On the connected dual graph, a spanning tree therefore reconstructs every phi_f relative to one root bit.

The only remaining ambiguity is

~~~text
phi_f -> phi_f XOR 1   for every face f,
~~~

which is one global gauge bit.

## 4. Public normalization attack K-A01

The same spanning tree can normalize all public tree transitions to zero.

After normalization, the public transition vector is exactly the canonical orientation cocycle in the same public tree gauge. Hidden face labels disappear completely.

The attack records:

- dual spanning-tree edges;
- fundamental cycle rank;
- non-zero orientation syndromes;
- recovered face gauges up to one global bit;
- public edge-check count.

## 5. Expected disposition

**K0 is expected to be rejected.**

That rejection demonstrates an important negative lesson:

- a real non-orientable surface can have genuinely global orientation obstruction;
- the obstruction can still be ordinary linear Z2 data;
- hiding local chart orientation labels only adds gauge, not a trapdoor.

K1 must therefore add structure that survives the orientation-character and orientation-double-cover attacks. Merely making the Klein-bottle triangulation larger is not a repair.

## 6. Security status

No one-wayness, average-case hardness, post-quantum, IND-CPA, IND-CCA, KEM, or production-security claim exists.


## 7. Measured result

Fixed master seed `30124490aabbccddeeff1029384756ab`.

Baseline `klein-bottle-5x4`:

~~~text
V/E/F:                                  20/60/40
Euler characteristic:                   0
dual V/E/cycle rank:                    40/60/21
orientable:                             false
non-zero fundamental syndromes:         7/21
public normalization = canonical:       true
hidden gauge recovery consistent:       true
hidden face gauges recovered up to root:true
public edge checks:                     60
residual global gauge choices:          2
~~~

Deterministic sweep:

| Set | V/E/F | Dual cycle rank | Non-zero syndromes | Gauge recovery |
|---|---|---:|---:|---:|
| klein-bottle-4x4 | 16/48/32 | 17 | 6 | yes |
| klein-bottle-5x4 | 20/60/40 | 21 | 7 | yes |
| klein-bottle-6x4 | 24/72/48 | 25 | 8 | yes |

The work grows linearly with the public dual-edge count in this implementation.

## 8. Disposition

**K0 is rejected exactly as intended.**

The experiment separates two facts that must not be conflated:

1. the surface really is non-orientable, and the cycle obstruction is genuinely global;
2. the hidden face labels are nevertheless just a Z2 gauge and are publicly reconstructible up to one global bit.

K1 must therefore attack something beyond the orientation character itself. Passing to a larger Klein-bottle mesh would add size but no asymmetry.
