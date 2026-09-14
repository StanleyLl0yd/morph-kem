# 83 — HGA4f adaptive finite-representation ensemble attack

## Status

**HGA4f is rejected by HGA-A010 on the measured toy distribution.** HGA4e showed that conditioning endpoint generation against two known finite quotients merely overfits those maps. HGA4f returns to the unconditioned exact-distance HGA4c distribution and instead strengthens the attacker with a fixed endpoint-independent library of small public representations.

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

A quotient state is never accepted as a witness. Quotient collisions can only weaken pruning. Ordinary balanced MITM is measured on the same endpoint as an independent exact baseline.

## Fixed Python 3.12 result

For `hga4f-D8`:

```text
exact distance:                         8
generator ball / shell:             2589 / 1356
generator transitions:                 4932
ordinary MITM states / transitions:    230 / 376
representation library size:             8

best single:                         A5-d
best single exact states:              98

best product:                    A5-d + A5-a
best product exact states:             53
best product / generator ball:  0.020471224
best product / MITM states:     0.230434783
exact endpoint verified:              yes
```

The best product therefore keeps only 53 exact states from a 2589-state generator ball while preserving a verifier-correct length-eight connector.

## Deterministic sweep

Python 3.12 tested `D=4/6/8 × 8` deterministic seeds: **24 public exact-distance endpoints**.

- exact endpoint recovery succeeds on **24/24**;
- best product retains <20% of the generator ball on **24/24**;
- best product retains fewer exact states than ordinary balanced MITM on **24/24**;
- retained fraction of generator ball is `0.012131716 .. 0.092182891`, mean `0.034809637`;
- D4 retained fraction: `0.043478261 .. 0.073529412`, mean `0.047234655`;
- D6 retained fraction: `0.012131716 .. 0.028662420`, mean `0.020263912`;
- D8 retained fraction: `0.012746234 .. 0.092182891`, mean `0.036930346`.

The selected-single frequency is dominated by the four independent `A5` maps, but the public rule is representation-agnostic and the generator never sees any member of the library.

## Result

**HGA4f is rejected by HGA-A010.** A modest fixed public representation library, evaluated only after endpoint publication and combined by a deterministic public rule, systematically produces a much smaller exact admissible set than both the full generator ball and ordinary MITM state count while preserving exact endpoint recovery.

This strengthens HGA4d/HGA4e. The measured leakage is not tied to one hand-picked quotient and cannot be repaired by training generation against a finite list of known maps without repeating the overfitting loop already exposed by HGA4e.

This result does **not** prove that the infinite Hurwitz action is asymptotically easy. It rejects the current exact-distance endpoint family and its finite-quotient-conditioning repair strategy on the measured distribution.

## Successor gate

A successor HGA action/distribution must not merely add the current library to a generation objective. It should change the relation so independently chosen finite representations do not routinely leave a tiny admissible subset. Any successor must still face:

- a held-out library of finite representations fixed before measurement;
- adaptive products of independently chosen public maps;
- ordinary balanced MITM;
- stabilizer/equivalent-action analysis;
- canonical and linear representations;
- quantum hidden-shift/subgroup screening where applicable.

No security claim.