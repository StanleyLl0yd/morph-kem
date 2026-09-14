# 84 — NAT8 public residual-representation closure

## Status

**NAT8 closes exact public group-valued connections as a source of hidden residual/global representation hardness.** After NAT7 removes normalized vertex gauge, the remaining non-tree residuals are already the public images of a free fundamental-group basis. There is no additional secret global representation to invert while exact edge labels remain public.

NAT8 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Generic statement

Let a connected public graph have `V` vertices, `E` canonically oriented public edges, and exact public labels `A_e` in any group `G`.

Choose the deterministic public rooted spanning tree used by NAT7. Tree integration yields public labels `t_v`, and the normalized residual on edge `(u,v)` is

```text
R_uv = t_u A_uv t_v^-1.
```

Every tree residual is identity. Each non-tree edge closes exactly one rooted fundamental cycle, so its residual is precisely the holonomy of that cycle.

A connected graph has free fundamental-group rank

```text
r = E - V + 1.
```

There are exactly `r` non-tree edges. Therefore the tuple of public non-tree residuals is already the image of a public free basis under the connection holonomy representation.

The full residual vector is reconstructed by placing identity on tree edges and those generator images on non-tree edges. NAT7 reconstruction then recovers the original exact public connection.

No flatness assumption is required.

## Adding public 2-cells

If the graph is the one-skeleton of a public 2-complex and the connection is flat, the public face relators simply impose equations among the already-public generator images.

For a triangular face `(a,b,c)` the canonical public relator evaluation is

```text
A_ab A_bc A_ac^-1.
```

Flatness requires this value to be identity. This constrains the public representation; it does not hide it.

Thus an exact public flat connection determines a public representation of the 2-complex fundamental group up to the same root/basepoint convention already fixed by NAT7.

## NAT-A010 generic harness

`nat_residual_representation.py`:

1. applies NAT7 deterministic tree normalization;
2. identifies the `E-V+1` non-tree edges;
3. exports their public residuals as fundamental-generator images;
4. reconstructs the complete residual vector from those images alone;
5. reconstructs the original edge connection exactly;
6. optionally evaluates public triangular face relators.

The harness uses only the minimal NAT7 group interface: identity, multiplication, inverse and equality.

## Fixed Python 3.12 regression

Using the merged NAT6 `nat6-8x9` flat `A5` connection:

```text
vertices / edges / triangles:          72 / 216 / 144
tree / generator edges:                71 / 145
free rank E-V+1:                             145
public generator images:                     145
nonidentity generator images:                 36
tree identity residuals:                      71
public triangular relators:                  144
nonidentity triangular relators:               0
residual vector reconstructed:                yes
exact connection reconstructed:               yes
```

The public generator-image count equals the free rank exactly. No hidden reference witness is used by extraction or reconstruction.

## Deterministic 24-instance flat-torus regression

Python 3.12 tests NAT6 `6x6/6x9/8x9 × 8` deterministic seeds. On **24/24** instances:

- public generator-image count equals `E-V+1` exactly;
- tree residual count equals `V-1` and every tree residual is identity;
- all public triangular relators evaluate to identity;
- the complete residual vector reconstructs exactly;
- the exact public edge connection reconstructs exactly.

The free ranks are:

```text
6x6:   E-V+1 = 73
6x9:   E-V+1 = 109
8x9:   E-V+1 = 145
```

Measured nonidentity public generator-image counts vary by seed as expected (`21..26`, `28..34`, `32..43` for the three sizes); this variation is irrelevant to the closure because the entire generator-image tuple is public in every case.

A synthetic non-flat `Z/5Z` triangle additionally demonstrates that extraction/reconstruction does not depend on flatness: the one public free-generator image reconstructs the exact connection even though the face relator is nonidentity.

Dedicated NAT8 CI passes on Python 3.11, 3.12 and 3.13 on the measured head.

## Architectural closure

NAT7 already removed hidden normalized vertex gauge. NAT8 removes the next apparent hiding place:

> **With exact public edge labels on a connected carrier, the residual global representation is itself public after deterministic tree normalization.**

Therefore future NAT work must change the publication model. A meaningful successor may publish a lossy/noisy function of the residual representation, noisy relator evaluations, commitments to global holonomies, or another incomplete observable. It cannot obtain hardness merely by increasing genus, group size, carrier size, or representation complexity while still publishing the exact connection.

This closure does not claim that inversion from a lossy/noisy residual observable is easy. That is the only remaining NAT direction worth testing.

## Successor gate

A NAT9 candidate must specify:

- the hidden residual/global representation;
- the exact lossy/noisy public observable derived from it;
- an exact or probabilistic verifier that does not simply reveal the full representation;
- quotient/character/conjugacy/SAT attacks on that observable;
- equivalent-representation semantics.

No security claim.