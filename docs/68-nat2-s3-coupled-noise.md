# 68 — NAT2 S3-coupled noisy synchronization control

## Status

**NAT2 is rejected by NAT-A003.** The relation is genuinely nonabelian at the full `S3` layer, but its public sign quotient routinely reveals the exact sparse noise support. Once those quotient-identified edges are removed, exact `S3` vertex states propagate uniquely over the remaining connected clean graph on 76/80 measured instances. The four quotient-ambiguous cases are still recovered by an independent bounded exact residual search.

NAT2 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Carrier and relation

NAT2 uses flip-mixed public spheres only as sparse factor graphs:

```text
nat2-F24: F=24, V/E=14/36, noise t in {1,2,3}
nat2-F30: F=30, V/E=17/45, noise t in {1,2,3}
nat2-F36: F=36, V/E=20/54, noise t in {1,2,3,4}
```

Each public vertex has a hidden `g_v in S3`, modulo a global left gauge fixed by setting public vertex 0 to the identity. For oriented edge `u < v`, the clean label is

```text
h_uv = g_u^-1 g_v.
```

Exactly `t` distinct public edges are right-multiplied by seeded transpositions. There is one noisy sample, no spacing/separation conditioning, and the verifier accepts any normalized state for which exactly `t` residual edges are transpositions and every other edge is exact.

## NAT-A003-Q — sign quotient and support propagation

The public homomorphism

```text
sign : S3 -> C2
```

maps every transposition noise factor to one flipped binary edge bit. The quotient therefore reproduces NAT1's public sphere-boundary syndrome:

1. take edge-label signs;
2. compute violated triangle parities;
3. solve the minimum dual-graph T-join;
4. interpret its edge support as the candidate noisy-edge set.

A second attack then removes those candidate noisy edges and uses all remaining observed `S3` constraints as exact clean equations. Starting from gauge-fixed vertex 0, labels propagate over the clean subgraph. Every repeated path is checked for consistency, and the final state is resubmitted to the exact NAT2 verifier.

This support-propagation attack uses no planted state/noise data. Reference equality is recorded only after public acceptance.

## NAT-A003-R — independent residual tree-CSP

The exact fallback attack does not assume that the minimum sign T-join recovered the planted support.

On a deterministic public spanning tree, once a parent label is known each tree edge has only four declared possibilities:

- one clean continuation;
- three noisy continuations, one for each transposition.

DFS enforces the public noise budget, then checks every non-tree edge exactly and resubmits completed states to the verifier. This is a bounded-noise residual search, not a polynomial-time claim; its growth with `t` is measured explicitly.

## Fixed Python 3.12 result

For fixed `nat2-F36`, generation recorded 183 rejected carrier flip proposals. The full curve is:

| `t` | sign defects | sign T-join | DP states | residual CSP nodes | CSP backtracks | accepted states | first state = planted |
|---:|---:|---:|---:|---:|---:|---:|:---:|
| 1 | 2 | 1 | 2 | 590 | 57 | 1 | yes |
| 2 | 4 | 2 | 5 | 10,850 | 1,596 | 1 | yes |
| 3 | 6 | 3 | 13 | 141,665 | 27,759 | 1 | yes |
| 4 | 8 | 4 | 34 | 1,397,489 | 341,715 | 1 | yes |

The fixed sign quotient exactly matches planted noise support and planted vertex parity at all four weights. The fallback search also recovers the exact planted normalized `S3` state at every weight.

The rapid CSP growth is retained as evidence against pretending that brute-force residual enumeration is itself a structural polynomial break. NAT2 is rejected for the much stronger quotient-collapse behavior measured across the full sweep.

## Deterministic sweep

Python 3.12 tested every declared weight over eight seeds:

- `nat2-F24`: 24 instances;
- `nat2-F30`: 24 instances;
- `nat2-F36`: 32 instances;
- total: **80 single-sample nonabelian noisy instances**.

### Sign quotient

The minimum public T-join equals the planted noise support on **76/80** instances, and the recovered normalized vertex parity equals the planted parity on those same 76/80 instances.

The four quotient-ambiguous cases are:

```text
nat2-F24 seed 3, t=3: planted 3 edges, minimum sign correction weight 2
nat2-F30 seed 7, t=3: planted 3 edges, minimum sign correction weight 2
nat2-F36 seed 1, t=4: alternative minimum correction of weight 4
nat2-F36 seed 5, t=3: planted 3 edges, minimum sign correction weight 2
```

These are preserved negative results for the quotient attack; reference mismatch does not invalidate the independent full-state attack.

### Quotient-support propagation

On **76/80** instances the sign-derived support leaves a connected, path-consistent clean subgraph, direct `S3` propagation reaches every public vertex, and the resulting state passes the exact verifier. All 76 accepted propagated states match the planted normalized state after public success.

The same four quotient-ambiguous instances fail the direct propagation verifier/connected-consistency gate, as expected. No reference data is used to decide success or failure.

Thus 95% of the official distribution collapses to:

```text
public C2 quotient -> minimum T-join support -> deterministic nonabelian propagation.
```

### Independent exact residual search

The fallback tree-CSP returns an accepted state on **80/80** instances. Its first accepted state equals the planted normalized `S3` state on **80/80**. Most instances expose one accepted state under the cap; two F36 cases expose two accepted normalized states, preserving equivalent-clean-state multiplicity.

Measured CSP work depends strongly on size and noise budget. At `F36,t=4` it reaches about **1.40 million nodes / 341k backtracks**, so no claim is made that this fallback has favorable asymptotic complexity.

Dedicated NAT2 CI passes on Python 3.11, 3.12 and 3.13.

## Result

**NAT2 is rejected by NAT-A003 because the generated distribution routinely collapses through a public abelian quotient.** A formally noncommutative full relation does not help when an informative quotient reveals the exact sparse corruption pattern on 95% of instances and the remaining clean group equations then propagate deterministically.

The fallback exact CSP closes the four quotient-ambiguous toy cases, but its growth is not used as the structural rejection argument.

Do not repair NAT2 merely by enlarging the sphere or increasing `t` while every allowed noise element has visible odd sign and the same quotient boundary code remains public.

## NAT3 gate

NAT3 must remove this quotient failure at the relation level. In particular, allowed noise should not project injectively to a cheap public quotient that exposes its support. A successor may use noise contained partly or wholly in a commutator/kernel subgroup, or couple several constraint types so quotient information leaves a nontrivial residual problem.

It must immediately face:

- all natural quotient chains, not only abelianization;
- propagation/message passing;
- matching/flow and sparse-recovery reductions;
- generic SAT/ILP/CP-SAT;
- equivalent-clean-state enumeration;
- generated-distribution leakage and matched controls where meaningful.

No security claim.
