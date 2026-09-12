# 68 — NAT2 S3-coupled noisy synchronization control

## Status

**NAT2 is a falsification experiment in progress.** It removes NAT1's purely binary public-boundary relation by using hidden nonabelian `S3` vertex states and a single sample of group-valued noisy edge constraints.

NAT2 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Carrier

NAT2 uses the already-audited flip-mixed sphere carrier machinery only as a public sparse factor graph. Toy sets are:

```text
nat2-F24: F=24, 240 successful flips, noise t in {1,2,3}
nat2-F30: F=30, 300 successful flips, noise t in {1,2,3}
nat2-F36: F=36, 360 successful flips, noise t in {1,2,3,4}
```

The sphere is globally relabelled before hidden states/noise are sampled.

## Hidden state and public relation

Each public vertex has a hidden group element `g_v in S3`. A global left action is gauge and is normalized by fixing public vertex 0 to the identity.

For every oriented public edge `u < v`, the clean constraint is

```text
h_uv = g_u^-1 g_v.
```

Generation chooses exactly `t` distinct public edges without spacing/separation conditioning. Each selected edge is right-multiplied by one uniformly seeded transposition:

```text
observed_uv = h_uv * tau_uv.
```

Only one observed edge-label tuple and the public value `t` are published.

The verifier accepts **any** normalized vertex-state assignment for which exactly `t` public edges differ by a transposition and every other edge is exact. It never compares with the planted hidden state.

## NAT-A003 attack 1 — sign quotient

The abelianization/sign map

```text
sign : S3 -> C2
```

turns every transposition noise factor into one flipped binary edge bit. Therefore the public sign layer falls directly back to NAT1's sphere-boundary problem:

1. take the parity/sign of every observed edge label;
2. compute violated triangle parities;
3. solve the minimum public T-join on the dual graph;
4. remove that correction;
5. recover a normalized public vertex-parity assignment.

The attack records whether this minimum sign correction equals the planted noise support only **after** public success. An alternative sign correction is not a failure of the attack.

## NAT-A003 attack 2 — exact nonabelian residual search

The full `S3` relation is attacked independently; the exact state search does not assume that the minimum sign T-join recovered the planted support.

Choose a deterministic public spanning tree. Once a parent label is known, each tree edge has only four legal possibilities under the declared noise model:

- clean edge: one uniquely determined child label;
- noisy edge: three uniquely determined child labels, one for each transposition.

The DFS therefore branches on noise placement/transposition choices rather than over all `6^V` hidden states. It enforces the public noise budget during tree propagation, then checks every non-tree edge exactly. Every completed state is resubmitted to the repository verifier.

The search enumerates accepted normalized clean states up to a public cap. Any accepted non-planted state is attacker success and is recorded as equivalent-clean-state multiplicity.

## Measurements

Record at least:

- public `V/E/F`;
- public noise weight `t`;
- sign-syndrome defect count;
- minimum sign T-join weight, DP states and pair tests;
- post-success equality of sign correction with planted support;
- post-success equality of recovered vertex parity with planted normalized parity;
- exact residual CSP nodes/backtracks;
- accepted normalized clean states up to the cap;
- whether the cap is hit;
- exact verifier acceptance of the first state;
- inferred noise support for the first state;
- post-success equality of the first state with planted normalized `S3` state;
- deterministic all-size / multi-seed sweep.

## Rejection gate

Reject NAT2 if the nonabelian-looking relation routinely collapses to:

1. an easy public abelian quotient; plus
2. a small exact residual search that returns an accepted clean state.

A recovered state or noise assignment need not match the planted reference. Equivalent accepted states are attacker successes.

Do not repair by increasing only the number of vertices while the sign quotient and bounded-noise tree propagation remain the same attack architecture.

## Advancement gate

If NAT2 fails, NAT3 must use a noisy relation whose informative quotient does not reduce most of the problem to an ordinary boundary code and whose residual state is not fixed by bounded local branching. It must immediately face quotient chains, BP/message passing, flow/matching reductions, generic SAT/ILP/CP-SAT, equivalent-clean-state enumeration and generated-distribution attacks.

No security claim.
