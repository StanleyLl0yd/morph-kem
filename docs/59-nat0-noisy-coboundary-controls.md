# 59 — NAT0 noisy coboundary negative controls

## Status

**NAT0 is an attack-harness calibration in progress.** Both controls deliberately add noise but are designed to remain publicly recoverable. They must fail before any stronger noisy-topology candidate is interpreted.

NAT0 is not a KEM, one-way function, post-quantum assumption, or production-security construction.

## Control A — one noisy edge in a public coboundary

A hidden public-vertex bit assignment `s` induces a clean edge coboundary

```text
c(u,v) = s(u) XOR s(v).
```

One public edge bit is then flipped to produce the observed edge vector `y`.

For every public triangle, the clean coboundary has zero boundary parity. A one-edge error therefore makes exactly the two incident public triangles odd. On the closed triangulated torus, that violated-triangle pair identifies the noisy public edge uniquely.

The attack is:

1. compute all triangle parities of `y`;
2. find the two violated triangles;
3. locate their unique common public edge;
4. flip that edge back;
5. propagate the recovered clean coboundary from one public root vertex.

The hidden vertex assignment is recovered up to the unavoidable global complement gauge. Reference data is consulted only after public success.

## Control B — repeated noisy coboundaries

The same clean coboundary is published through an odd number of noisy samples. Each sample flips a public fixed number of edges. The calibration generator deliberately schedules distinct noisy edges across samples, so every public edge is corrupted in at most one sample.

A per-edge majority vote therefore recovers the clean coboundary exactly. Public propagation then recovers the hidden vertex assignment up to global complement.

Toy sets:

- `nat0-4x4`: 7 samples, weight 2 noise per sample;
- `nat0-6x6`: 7 samples, weight 3;
- `nat0-8x8`: 7 samples, weight 4.

This control validates the multi-sample correlation attack before any stronger noise model is considered.

## NAT-A001 calibration gate

Across deterministic public relabeling seeds require:

- the one-edge control always exposes exactly two violated public triangles;
- their pair always identifies one public edge;
- clean coboundary recovery always verifies;
- repeated-sample majority always returns a valid public coboundary;
- recovered clean data differs from every repeated sample by exactly the public noise weight;
- normalized hidden vertex data matches reference only after public success.

If either weak noisy construction survives this harness, NAT0 is not ready for stronger candidates.

## Next NAT gate

NAT1 must use a noise distribution that is not removable by a local syndrome locator or repeated-sample majority. It must immediately face quotient leakage, sparse recovery, syndrome decoding, belief propagation, spectral diagnostics, multi-sample correlation and matched-random controls.

No security claim.
