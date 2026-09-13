# 70 — HGA4b self-avoiding Hurwitz action-state generator

## Status

**HGA4b is a falsification/calibration experiment in progress.** HGA4 did not expose a new polynomial/canonical inversion of the infinite Hurwitz action, but its locally reduced planted-word generator was rejected because materially shorter equivalent connectors were routine.

HGA4b keeps the action, source distribution, verifier and attack unchanged. It changes only the planted-history generator.

HGA4b is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Generator

Reuse the HGA4 action of `B3` on triples of reduced words in `F(a,b)`. For requested lengths `L in {8,12,16,20}`:

1. sample exactly the same source-state distribution as the paired HGA4 control;
2. keep the exact action states already visited on the planted path;
3. at each step enumerate the four public Hurwitz generators in deterministic seeded order;
4. take the first successor not already on the current path;
5. if no successor exists, fail explicitly at that step; do not restart or inspect an attack result;
6. publish the endpoint after exactly `L` successful self-avoiding steps.

The generator does not query MITM distance, shortest connectors, canonical forms, quotient output, or any other attack result.

## Paired control

For every `(L,seed)`, construct both:

- the HGA4b self-avoiding endpoint;
- the original HGA4 locally reduced planted-word endpoint;

from the exact same public source state and the same requested length. Run the unchanged HGA4 public attack against both.

## HGA-A006

The attack remains:

- exact invariant total free-group product;
- free-abelianization quotient exposing the induced `S3` strand permutation;
- exact bidirectional BFS/MITM in reduced tuple states to the public word bound;
- shortest equivalent connector among public meet states;
- exact endpoint verification.

Planted-word equality is reference-only. Any equivalent connector is attacker success.

## Measurements

Record at least:

- requested/achieved path length;
- exact distinct generated path-state count;
- explicit generator dead-end count;
- target reduced-word size;
- forward/backward MITM states and transitions;
- meet-state count;
- shortest recovered connector length;
- whether the recovered connector is at least 25% shorter than the planted path;
- exact endpoint verification;
- post-success planted-word equality;
- paired locally reduced HGA4 values at the same source/length/seed;
- deterministic multi-seed curve including one longer `L=20` calibration.

## Gate

Reject HGA4b if substantial equivalent shortening remains routine. In that case simple self-avoidance removes literal path loops but does not make planted histories close to geodesic under braid/action relations.

If material shortening largely disappears while exact MITM state balls continue to grow with depth, record only survival of this generated-distribution gate on toy sizes. That is not evidence of one-wayness, asymptotic hardness, or post-quantum security.

No security claim.
