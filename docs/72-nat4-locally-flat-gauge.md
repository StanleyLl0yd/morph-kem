# 72 — NAT4 locally-flat coupled A5 deformation control

## Status

**NAT4 is rejected by NAT-A005 through a public gauge/equivalent-witness collapse.** Making the deformation exactly locally flat removes NAT3's curvature-support oracle, but also makes the published edge field itself a directly integrable public synchronization state.

NAT4 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Construction

Reuse normalized hidden vertex labels `g_v in A5`. Sample an auxiliary deformation field `q_v in A5` with exactly `k` nonidentity non-root entries, each a 3-cycle, and `q_0=1`.

Publish edge labels

```text
observed_uv = q_u^-1 * (g_u^-1 g_v) * q_v.
```

Equivalently define

```text
s_v = g_v q_v.
```

Then

```text
observed_uv = s_u^-1 s_v,
```

so every public face holonomy is exactly identity.

The verifier accepts any normalized pair `(g,q)` where `q` has exactly public weight `k`, every nonidentity `q_v` is a 3-cycle, and the formula above reproduces every public edge label. It never compares to the planted decomposition.

## NAT-A005 — public gauge/equivalent-witness attack

The attack never attempts planted recovery.

1. Integrate the flat public edge labels over a spanning tree to recover the effective normalized state `s`.
2. Verify every remaining public edge for path consistency.
3. Choose a canonical set of `k` non-root vertices.
4. Put one fixed public 3-cycle on each selected vertex and identity elsewhere, obtaining a legal `q'`.
5. Define

```text
g'_v = s_v (q'_v)^-1.
```

6. Submit `(g',q')` to the exact verifier.

Every legal `q'` yields another accepted decomposition of the same public effective field. Since `A5` has 20 three-cycles, the explicit lower bound on verifier-equivalent witnesses is

```text
C(V-1,k) * 20^k.
```

## Fixed Python 3.12 result

For `nat4-F36`, with `V/E/F = 20/54/36`:

```text
k   nonidentity face holonomies   integration checks   equivalent-witness lower bound   accepted
1              0                         108                         380                    yes
2              0                         108                      68,400                    yes
3              0                         108                   7,752,000                    yes
4              0                         108                 620,160,000                    yes
```

For the fixed baseline, the canonical public support differs from the planted support at every measured weight, the reconstructed clean state differs from the planted clean state, yet the integrated effective state matches exactly and the verifier accepts. This is the intended equivalent-witness criterion.

## Multi-seed sweep

The Python 3.12 sweep covers:

- `nat4-F24`: eight seeds, `k=1..3`;
- `nat4-F30`: eight seeds, `k=1..3`;
- `nat4-F36`: eight seeds, `k=1..4`.

Across all **80/80** measured public instances:

- the number of nonidentity public face holonomies is exactly **0**;
- spanning-tree integration is path-consistent;
- the canonical constructed `(g',q')` witness passes the exact public verifier;
- the recovered effective field equals the planted effective field after public success;
- the canonical clean-state decomposition is non-planted on **80/80**;
- the canonical support is non-planted on **79/80**; one accidental support coincidence does not affect attacker success;
- no search over the `C(V-1,k)20^k` witness family is needed: one canonical legal choice is constructed directly.

Dedicated NAT4 CI passes on Python 3.11, 3.12 and 3.13 for the measured branch run.

## Interpretation

NAT3 and NAT4 now expose the two opposite local extremes of this edge-synchronization design:

- isolated edge noise creates public nontrivial face curvature and reveals corruption support;
- forcing local flatness makes the deformation removable by a public gauge reparameterization and yields enormous equivalent-witness multiplicity.

Changing only the group size, carrier size, or sparsity parameter cannot repair NAT4 while the verifier depends only on the product field `s=gq`.

A successor must make the deformation globally coupled and verifier-visible without either (a) localizing individual corruption through face curvature or (b) factoring completely into an unconstrained gauge field. It must immediately face representation quotients, normalization/gauge elimination, message passing, exact SAT/ILP/CP-SAT and equivalent-witness enumeration.

No one-wayness, post-quantum, IND-CPA/CCA, or production-security claim exists.
