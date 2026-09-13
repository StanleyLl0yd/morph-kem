# 71 — NAT3 A5 perfect-group noisy synchronization

## Status

**NAT3 is rejected by NAT-A004.** Moving from `S3` to the perfect simple group `A5` removes NAT2's sign/abelian quotient, but the sparse edge-noise distribution remains locally visible through exact public nonabelian face curvature.

NAT3 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Public relation

A flip-mixed triangulated sphere is used only as a public sparse factor graph. Each public vertex has a hidden normalized label `g_v in A5`, with public vertex 0 fixed to the identity.

For every public oriented edge `u<v`:

```text
h_uv = g_u^-1 g_v.
```

Exactly `t` public edges are right-multiplied by deterministic seeded 3-cycles in `A5`. Toy sets are `F=24,30,36` with `t in {1,2,3}`.

The verifier accepts any normalized vertex assignment for which exactly `t` edge residuals are 3-cycles and every other edge is exact. It never compares with the planted hidden state.

## Quotient screen

`A5` has trivial abelianization, so the NAT2 sign/T-join attack is absent by construction. All hidden states, clean edge labels and allowed noise elements remain inside `A5`.

This removes the previous failure mechanism but does not hide local nonabelian curvature.

## NAT-A004 — curvature-support attack

For every oriented public triangle `a<b<c`, compute exact nonabelian face holonomy

```text
H_abc = observed_ab * observed_bc * observed_ac^-1.
```

If all three boundary edges are clean, `H_abc = 1`. Therefore every public face with nonidentity holonomy must contain at least one noisy edge.

The attack:

1. enumerates all public size-`t` edge supports;
2. keeps only supports hitting every nonidentity-curvature face;
3. deletes each candidate support;
4. propagates normalized `A5` labels deterministically through the remaining clean subgraph;
5. rejects disconnected or path-inconsistent candidates;
6. submits every completed state to the exact verifier.

The support enumeration is used only to measure how strongly curvature localizes the support. Generic fixed-`t` enumeration alone is not the rejection criterion.

## Fixed Python 3.12 result

For `nat3-F36`:

```text
t=1: V/E/F=20/54/36, curvature defects=2,
     C(E,t)=54,    curvature-hitting supports=1,
     consistent=1, accepted=1, planted support/state match=yes

t=2: V/E/F=20/54/36, curvature defects=4,
     C(E,t)=1431,  curvature-hitting supports=1,
     consistent=1, accepted=1, planted support/state match=yes

t=3: V/E/F=20/54/36, curvature defects=6,
     C(E,t)=24804, curvature-hitting supports=1,
     consistent=1, accepted=1, planted support/state match=yes
```

All fixed nonidentity face holonomies are 3-cycles. The largest fixed support space therefore collapses from 24,804 candidates to exactly one using only public curvature incidence before any group-state propagation.

## Eight-seed sweep

The official sweep contains `F=24,30,36` × eight seeds × three noise weights = **72** public instances.

Measured Python 3.12 result:

- **72/72** planted supports satisfy the public curvature-hitting constraints;
- **64/72** instances have exactly **one** size-`t` curvature-hitting support;
- the remaining **8/72** have only **2, 5, or 7** curvature-hitting supports;
- the maximum measured candidate family after curvature filtering is **7**;
- deterministic clean-subgraph propagation leaves exactly **one** connected/path-consistent accepted state on **72/72** instances;
- the first accepted inferred support matches the planted support on **72/72** after public success;
- the first accepted normalized `A5` state matches the planted normalized state on **72/72** after public success;
- no accepted-state cap is hit.

The eight non-unique curvature-support cases are preserved rather than hidden; propagation resolves each of them without reference data.

## Interpretation

NAT3 demonstrates that removing easy abelian quotients is insufficient. The noise model is still structurally exposed because an isolated corrupted edge creates nontrivial curvature on adjacent public faces. Sparse supports are therefore localized by a public hypergraph hitting constraint before the nonabelian synchronization problem is meaningfully engaged.

This is not a claim that generic noisy `A5` synchronization is easy. It is a rejection of this generated noise relation/distribution.

Increasing only carrier size or replacing `A5` by a larger perfect group is not a justified repair while local face curvature continues to reveal corruption locations.

## Successor gate

NAT4 must make local face curvature intentionally uninformative about individual corruption support—for example through coupled locally-flat gauge deformations or edge/face noise satisfying zero local curvature—then immediately face:

- global synchronization and quotient/representation attacks;
- message passing / belief propagation;
- sparse recovery and matching/flow reductions where applicable;
- generic SAT / ILP / CP-SAT;
- equivalent-state enumeration;
- explicit noise-scaling and generated-distribution tests.

No trapdoor primitive, KEM, one-wayness, post-quantum, IND-CPA/CCA, or production-security claim exists.
