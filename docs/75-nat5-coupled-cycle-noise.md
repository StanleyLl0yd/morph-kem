# 75 — NAT5 coupled non-flat A5 cycle-noise control

## Status

**NAT5 is rejected by NAT-A006.** Coupling the nonabelian residual along one simple primal circuit avoids NAT4's free vertex-gauge collapse, but public face curvature still localizes the entire circuit to a tiny candidate family. Exact correction and integration then recover one verifier-accepted decomposition on every measured instance.

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

## Fixed Python 3.12 result

For `nat5-F36`:

```text
V/E/F:                         20 / 54 / 36
cycle length:                             6
enumerated public cycles:               703
nonidentity face holonomies:             10
curvature-hitting cycles:                 1
cycle/value pairs tested:                20
path-consistent pairs:                    1
accepted witnesses:                       1
accepted cap hit:                         no
first accepted cycle/value/state:   planted
```

Thus public curvature collapses 703 possible six-cycles to one support before any group-value search. Trying the 20 legal 3-cycle values leaves one path-consistent verifier-accepted witness.

## Eight-seed sweep

Across F24/F30/F36 × eight deterministic seeds (**24 public instances**):

- all **24/24** attacks recover a verifier-accepted decomposition;
- all **24/24** have exactly one path-consistent cycle/value pair and exactly one accepted witness;
- the first accepted cycle, `A5` noise value and normalized clean state match the planted reference on **24/24**, checked only after public success;
- no accepted-witness cap is hit.

Public cycle counts and curvature filtering are:

```text
F24, length 4: 59..72 public cycles  -> 1..3 curvature-hitting cycles
F30, length 6: 521..642 public cycles -> 1..5 curvature-hitting cycles
F36, length 6: 612..922 public cycles -> 1..2 curvature-hitting cycles
```

The attack therefore tests only 20..100 cycle/value pairs per instance despite hundreds of legal public circuit supports.

## Interpretation

NAT5 demonstrates that merely correlating isolated edge noise into a short nonabelian circuit does not remove NAT3's structural leakage. The face-curvature pattern acts as a strong public fingerprint for the whole circuit even though no individual edge is published as an independent error variable.

This is not a generic theorem about all coupled nonabelian noise. It rejects this short-cycle distribution. Increasing only the carrier size while keeping bounded public circuit length is not a justified repair.

A successor must prevent local curvature from determining a bounded support object **and** avoid NAT4's complete gauge factorization. Plausible next controls require overlapping/multiple long-range circuits or a genuinely global constraint whose local defect pattern has many public preimages. Those controls must immediately face flow/exact-cover, representation quotients, message passing and generic SAT/ILP/CP-SAT.

No one-wayness, post-quantum, IND-CPA/CCA, or production-security claim exists.
