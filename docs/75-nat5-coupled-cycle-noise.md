# 75 — NAT5 coupled non-flat A5 cycle-noise control

## Status

**NAT5 is a falsification experiment in progress.** NAT3 failed because isolated edge noise was locally visible through face curvature. NAT4 failed because enforcing exact local flatness turned the deformation into a removable vertex gauge. NAT5 tests a middle case: noise is coupled along one simple primal circuit rather than independent per edge or freely reparameterizable per vertex.

NAT5 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Construction

Reuse the flip-mixed triangulated-sphere carrier and normalized hidden `A5` vertex state from NAT3.

For each declared parameter set, choose one deterministic simple primal cycle of public even length:

```text
nat5-F24: length 4
nat5-F30: length 6
nat5-F36: length 6
```

Select one seeded 3-cycle `r in A5`. Along the oriented circuit, alternate residual factors

```text
r, r^-1, r, r^-1, ...
```

and compose them on the right of the clean directed edge transport. Outside the circuit, observations are clean.

The verifier accepts any normalized `A5` vertex state, any simple cycle of the declared public length, and any 3-cycle value `r` that exactly reproduces every public edge observation. It never compares to the planted cycle, value or state.

## NAT-A006 — public circuit-decomposition attack

1. Enumerate every public simple primal cycle of the declared length, canonicalizing rotations and reversal.
2. Compute exact nonabelian public face holonomies.
3. Keep only cycle supports that intersect every face with nonidentity holonomy; a clean face cannot be a public defect.
4. For every surviving cycle and each of the 20 public `A5` 3-cycles, algebraically remove the alternating residual pattern from the observations.
5. Integrate the resulting candidate clean edge field from the normalized root.
6. Reject path-inconsistent candidates and submit every consistent candidate to the exact verifier.
7. Any accepted decomposition is attacker success; planted equality is checked only after public success.

This attack is deliberately simple. If it fails to localize the planted circuit, equivalent accepted circuit decompositions still count as a break.

## Measurements

Record:

- V/E/F and declared circuit length;
- total enumerated public simple cycles;
- nonidentity face-holonomy count;
- cycles surviving the public curvature-hitting filter;
- cycle/value pairs tested;
- path-consistent candidate pairs;
- accepted witnesses and cap status;
- first verifier acceptance;
- post-success cycle/value/state equality with the reference;
- deterministic all-size/multi-seed curve.

## Gate

Reject NAT5 if public curvature plus short-cycle enumeration reduces the coupled support to a small family and deterministic correction/integration routinely produces a verifier-accepted decomposition. Also reject if many non-planted decompositions are accepted: equivalent-witness multiplicity is attacker success, not ambiguity in our favor.

If this first gate survives, NAT5 must still face graph-flow/exact-cover formulations, message passing, representation quotients and generic SAT/ILP/CP-SAT before any advancement.

No security claim.
