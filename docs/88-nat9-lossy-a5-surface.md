# 88 — NAT9 lossy A5 surface-representation control

## Status

**NAT9 is a falsification experiment in progress.** NAT7/NAT8 close exact public edge-connections: after deterministic tree normalization, exact edge labels expose the residual global representation itself. NAT9 therefore changes the publication model and hides the exact residual generator images.

This experiment does not make a hardness or security claim.

## Hidden object

Use a genus-two surface-group presentation

```text
<a,b,c,d | [a,b][c,d] = 1>
```

and a hidden representation into `A5` specified by the four exact generator images

```text
rho(a), rho(b), rho(c), rho(d) in A5.
```

Generation deterministically samples nonidentity `A5` quadruples until the public surface relator holds exactly.

The planted exact quadruple is reference-only.

## Lossy public observable

The public object does **not** contain the four exact `A5` elements. It contains only their permutation cycle types plus a fixed subset of product cycle types.

Important terminology: this is intentionally **coarser than an A5 conjugacy class observable**. In particular, `A5` splits the five-cycles into two conjugacy classes, while permutation cycle type merges them. The experiment therefore calls these values **cycle-type classes**.

Three fixed public levels are tested:

```text
nat9-C4: four generator cycle types only
nat9-P2: generator types + types of ab and cd
nat9-X4: generator types + types of ab, cd, ac and bd
```

No level is selected after seeing attack output.

## Verification semantics

A recovered quadruple is accepted if:

1. all four values are nonidentity `A5` elements;
2. all four generator cycle types equal the public values;
3. `[a,b][c,d] = 1` exactly;
4. every published product cycle type matches.

**Any accepted quadruple is attacker success.** Equality with the planted representation is checked only after public success and has no role in verification.

This semantic point is central: a lossy observable may hide the planted representation while simultaneously creating many verifier-equivalent representations for the attacker.

## NAT-A011 public CSP

The attack receives only the public observable.

1. Enumerate the `A5` elements matching each public generator cycle type.
2. Enumerate `(a,b)` pairs, pruning by the public `ab` product type when present, and compute `[a,b]`.
3. Enumerate `(c,d)` pairs, pruning by `cd` when present, and bucket them by `[c,d]`.
4. Join left/right pairs requiring

```text
[c,d] = [a,b]^-1.
```

5. Apply `ac`/`bd` product-type filters when present.
6. Run the exact public verifier on every remaining candidate.
7. Record the total number of accepted representations rather than stopping at the planted one.

The implementation records class-candidate sizes, pair counts, relator joins, verifier tests, accepted multiplicity, and reference equality only after success.

## Declared measurement

Run a deterministic eight-seed sweep for all three public levels:

```text
C4 / P2 / X4 × 8 seeds
```

The gate asks:

- whether public recovery succeeds;
- how many verifier-equivalent representations remain;
- whether additional coarse product observables materially reduce CSP work;
- how often the first accepted representation happens to equal the planted one.

## Rejection gate

Reject this NAT9 family if the public pair-join CSP routinely finds a verifier-accepted representation with small explicit work, regardless of whether it recovers the planted quadruple.

Do not repair such a failure by changing the verifier to demand planted equality: that would require publishing information that identifies the secret and would contradict the intended equivalent-representation semantics.

## Survival gate

Only if the fixed lossy observable leaves measurable residual uncertainty **and** the declared public CSP fails under an explicit work bound should a successor add controlled noise or larger targets. Survival would still be toy evidence only.

No trapdoor primitive, KEM, one-wayness, post-quantum, IND-CPA/CCA, or production-security claim exists.
