# 71 — NAT3 A5 perfect-group noisy synchronization

## Status

**NAT3 is a falsification/calibration experiment in progress.** NAT2 failed because the public sign quotient `S3 -> C2` exposed sparse corruption support on 76/80 measured instances. NAT3 removes that specific quotient by moving hidden states and sparse noise into the perfect simple group `A5`.

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

This does not imply hardness. NAT3 immediately attacks the full nonabelian local relation.

## NAT-A004 — curvature-support attack

For every oriented public triangle `a<b<c`, compute exact nonabelian face holonomy

```text
H_abc = observed_ab * observed_bc * observed_ac^-1.
```

If all three boundary edges are clean, `H_abc = 1`. Therefore every public face with nonidentity holonomy must contain at least one noisy edge.

The attack then:

1. enumerates all public size-`t` edge supports;
2. keeps only supports hitting every nonidentity-curvature face;
3. deletes each candidate support;
4. propagates normalized `A5` labels deterministically through the remaining clean subgraph;
5. rejects disconnected or path-inconsistent candidates;
6. submits every completed state to the exact verifier.

This attack uses no planted data. Post-success support/state equality is reference-only.

## Interpretation rule

Exact fixed-`t` support enumeration is only a toy/FPT baseline and is **not** by itself a structural rejection. The measured question is whether public nonabelian curvature shrinks the support space to a tiny or unique family routinely.

If curvature leaves many candidates and work scales essentially like generic `E^t`, NAT3 survives this specific gate only. If curvature almost directly localizes sparse corruption and clean-subgraph propagation finishes recovery, reject the generated noise distribution.

## Measurements

Record at least:

- public `V/E/F` and noise weight;
- nonidentity face-curvature count and nonidentity conjugacy/cycle-type histogram;
- total `C(E,t)` support combinations;
- support count after exact curvature hitting constraints;
- propagated and connected/consistent support counts;
- accepted normalized states and cap;
- first exact verifier acceptance;
- post-success planted support/state equality;
- whether planted support necessarily hits every public defect face;
- deterministic all-size/multi-seed curve.

## Advancement gate

A surviving NAT3 must next face message passing, sparse synchronization algorithms, generic SAT/ILP/CP-SAT, equivalent-state enumeration and explicit noise-scaling experiments. A rejected NAT3 must change the noise relation so local curvature no longer reveals corruption locations.

No security claim.
