# 83 — HGA4f adaptive finite-representation ensemble attack

## Status

**HGA4f is a falsification experiment in progress.** HGA4e shows that conditioning endpoint generation against two known finite quotients overfits those maps. HGA4f returns to the unconditioned exact-distance HGA4c distribution and instead strengthens the attacker: a fixed public library of independent small representations is evaluated after the endpoint is published.

HGA4f is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Instance distribution

Use HGA4c exact-distance generation at `D=4,6,8`. The generator constructs the exact ball/shell and selects its target by the original HGA4c public rule. It does **not** inspect any HGA4f quotient map or attack metric.

Every selected endpoint therefore retains its exact-distance certificate in the original free-group Hurwitz action.

## Fixed representation library

Before the deterministic sweep, fix eight public homomorphisms of `F(a,b)`:

```text
2 x S3
2 x S4
4 x A5
```

with different generator pairs. Because the source group is free, each permutation-generator pair defines a homomorphism; unit tests additionally require every map to commute exactly with each public Hurwitz generator on the measured action states.

No representation is created or modified after seeing a sweep result.

## HGA-A010 adaptive attack

For every public endpoint:

1. run quotient-admissible exact recovery under all eight single maps;
2. rank singles by exact states retained, then exact transitions, then public label;
3. select the best three singles by that fixed deterministic rule;
4. evaluate all three pair-products among those selected maps;
5. choose the best product by the same public rule;
6. accept only if the recovered braid connector reproduces the original exact free-group endpoint.

A quotient state is never accepted as a witness. Quotient collisions can only weaken pruning.

The attack also records ordinary balanced MITM on the same endpoint.

## Measurements

Record:

- exact generator ball/shell and generation transitions;
- ordinary MITM states/transitions;
- library size;
- every single-map retained state count/fraction;
- selected top-three labels;
- all three product retained state counts/fractions;
- best-single and best-product results;
- exact connector length/verification;
- frequency with which the best product retains <20% of the generator ball;
- frequency with which it retains fewer exact states than ordinary MITM;
- deterministic `D=4/6/8 x 8` sweep and per-distance summaries.

## Gate

Reject the current HGA4c endpoint family more broadly if this modest fixed public library routinely yields a very small exact admissible set while preserving verifier-correct recovery, especially if adaptive products retain fewer exact states than ordinary MITM on most endpoints.

If the library is weak, record that result without adding more maps post hoc. Larger representations, stabilizers, canonical forms and generic search remain separate gates.

Do not repair a failure by conditioning generation against this library: HGA4e already demonstrates that finite training sets lead to a representation-overfitting loop.

No security claim.