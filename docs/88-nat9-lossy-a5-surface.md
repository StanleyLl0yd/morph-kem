# 88 — NAT9 lossy A5 surface-representation control

## Status

**NAT9 is rejected by NAT-A011 on the measured toy distribution.** Hiding the exact residual generator images behind coarse `A5` cycle-type observables does hide the planted quadruple, but it creates a large verifier-equivalent solution set that a small public pair-join CSP recovers on every declared instance.

This is a falsification result, not a claim about arbitrary noisy representation problems or cryptographic hardness.

NAT9 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Hidden object

Use a genus-two surface-group presentation

```text
<a,b,c,d | [a,b][c,d] = 1>
```

and a hidden representation into `A5` specified by four exact nonidentity generator images.

Generation deterministically samples quadruples until the surface relator holds. The planted exact quadruple is reference-only.

## Lossy public observable

The public object omits all four exact `A5` elements. It contains only their permutation cycle types plus a fixed subset of product cycle types.

This is intentionally **coarser than an A5 conjugacy-class observable**. In particular, `A5` splits five-cycles into two conjugacy classes, whereas permutation cycle type merges them. We therefore call the public values **cycle-type classes**.

Three levels were fixed before measurement:

```text
nat9-C4: four generator cycle types only
nat9-P2: generator types + types of ab and cd
nat9-X4: generator types + types of ab, cd, ac and bd
```

The generator never queries recovery output.

## Verification semantics

A recovered quadruple is accepted if:

1. all four values are nonidentity `A5` elements;
2. all four generator cycle types equal the public values;
3. `[a,b][c,d] = 1` exactly;
4. every published product cycle type matches.

**Any accepted quadruple is attacker success.** Equality with the planted representation is checked only after public success and has no role in verification.

This semantic rule is decisive here: lossiness hides the planted representation but simultaneously permits many alternative accepted representations.

## NAT-A011 public CSP

The attacker:

1. enumerates the `A5` elements matching each public generator cycle type;
2. enumerates `(a,b)` pairs, pruning by `ab` when available, and computes `[a,b]`;
3. enumerates `(c,d)` pairs, pruning by `cd` when available, and buckets them by `[c,d]`;
4. joins pairs requiring `[c,d] = [a,b]^-1`;
5. applies `ac`/`bd` filters when published;
6. runs the exact public verifier;
7. counts all accepted representations.

No reference witness is used by recovery.

## Fixed Python 3.12 `nat9-X4`

```text
generation attempts:                         17
generator cycle types:              3 / 5 / 5 / 5
candidate class sizes:              20 / 24 / 24 / 24
left pairs considered / retained:         480 / 240
right pairs considered / retained:        576 / 240
relator join candidates:                        1320
verifier candidates tested:                      480
accepted representations:                        480
public recovery accepted:                        yes
first recovered equals planted:                   no
```

Even the most informative fixed observable therefore leaves hundreds of verifier-equivalent solutions on the fixed instance.

## Declared `C4/P2/X4 × 8` sweep

Public recovery succeeds on **24/24** instances. The first deterministic accepted representation equals the planted quadruple on **0/24** instances.

Per observable level:

```text
level   recovered   planted-first   accepted representations / seed
C4        8/8           0/8          1740 .. 5280
P2        8/8           0/8           360 ..  960
X4        8/8           0/8           120 ..  480
```

Aggregate accepted-representation counts across eight seeds are:

```text
C4: 21165
P2:  5640
X4:  1800
```

The maximum explicit work observed was:

```text
C4: relator joins 5280, verifier tests 5280
P2: relator joins  960, verifier tests  960
X4: relator joins 5784, verifier tests  480
```

`X4` can have many relator-compatible joins before the cross-product filters, but its final verifier set remains tiny on an absolute scale and still contains at least 120 accepted representations on every measured seed.

## Interpretation

NAT9 demonstrates a specific failure mode distinct from NAT7/NAT8:

> **Making the public observable lossy can hide the planted secret while making the verifier-inversion objective easier, because equivalent accepted solutions proliferate.**

The planted quadruple is genuinely not recovered first on any declared instance, yet the attacker succeeds on every instance under the actual verifier semantics.

Demanding planted equality is not a valid repair: doing so would change the public verification problem and require enough identifying information to distinguish the planted representation from its current equivalence class.

Likewise, simply adding a few more exact cycle-type/product coordinates risks walking back toward the exact-publication failure already closed by NAT8.

## Successor direction

A meaningful NAT successor must introduce a noisy/probabilistic observable whose acceptance semantics do **not** collapse into a large cheap equivalence class. It must explicitly measure both:

- residual uncertainty about the hidden representation; and
- multiplicity/cost of verifier-accepted alternative representations.

Noise alone is not automatically helpful; the next gate must attack quotient/character information, relator propagation, CSP/SAT and equivalent-solution multiplicity before any scale-up.

No security claim.
