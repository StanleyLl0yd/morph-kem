# 59 — NAT0 noisy coboundary negative controls

## Status

**NAT0 calibration succeeds by rejecting both deliberately weak noisy constructions.** A single noisy edge is removed by public triangle syndrome localization, while repeated sparse noise is removed exactly by public majority. This validates the first NAT denoising gates; it is not evidence that a stronger noisy relation is hard.

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

## Measured NAT-A001 calibration

Exact Python 3.12 fixed `nat0-8x8`:

```text
public V/E/F:                              64/192/128
single violated triangles:                (17,113)
single recovered noise edge:              182
single accepted:                          yes
single matches reference after success:   yes
repeated samples:                         7
public repeated noise weight:             4
repeated sample distances:                (4,4,4,4,4,4,4)
majority edge votes:                      1344
repeated accepted:                        yes
repeated matches reference after success: yes
```

Python 3.12 sweep over all three sets × eight deterministic seeds gives:

- single-noise control: **24/24** runs expose exactly two violated triangles, recover the unique noisy edge, reconstruct a valid clean coboundary and match normalized reference only after public success;
- repeated-noise control: **24/24** runs recover the clean coboundary exactly by majority;
- `nat0-4x4`: 7 samples, noise weight 2, `336` majority edge votes;
- `nat0-6x6`: 7 samples, noise weight 3, `756` votes;
- `nat0-8x8`: 7 samples, noise weight 4, `1344` votes;
- every recovered clean vector lies at exactly the configured public noise weight from each corresponding noisy sample.

The dedicated NAT0 workflow passes on Python 3.11, 3.12 and 3.13.

## Result

**Both NAT0 controls are rejected as intended.** Adding noise alone does not repair the exact-witness failure modes. Noise that produces a local public syndrome locator is removable, and repeated samples sharing one clean object can make denoising easier through correlation.

Future NAT candidates must therefore make two properties explicit: a non-local noise distribution with meaningful entropy, and a publication model that does not hand the attacker many correlated samples unless that exposure is part of the intended assumption.

## Next NAT gate

NAT1 must use a noise distribution that is not removable by a local syndrome locator or repeated-sample majority. It must immediately face quotient leakage, sparse recovery, syndrome decoding, belief propagation, spectral diagnostics, multi-sample correlation and matched-random controls.

A suitable next control should publish one sample per hidden object, use multiple nonadjacent errors drawn without an exposed local locator, and measure recovery curves as noise weight increases rather than selecting one favorable point.

No security claim.
