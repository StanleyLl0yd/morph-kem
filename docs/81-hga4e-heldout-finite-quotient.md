# 81 — HGA4e held-out finite-quotient generalization control

## Status

**HGA4e is rejected by HGA-A009 on the measured generated distribution.** Conditioning exact-distance endpoint selection against the known `S3/A5` quotient filters does not generalize: independent held-out finite representations and their products still prune the exact free-group state space strongly while preserving verifier-correct recovery.

HGA4e is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Exact-distance generator

Reuse the HGA4c exact-distance shell construction at `D=4,6,8`. Enumerate the full exact ball and shell.

Target selection is allowed to inspect only two declared **training** representations, identical to HGA4d:

- `S3-train`;
- `A5-train`.

For every shell target and every training quotient:

1. build the quotient reverse-distance table through `D`;
2. inspect the already-generated exact ball;
3. count exact states whose quotient could still reach the quotient target within the remaining exact depth.

Select the target lexicographically to maximize the worse training retention, then total training retention, target free-word length, and an independent deterministic hash tie-break. Held-out representations are never consulted during selection.

## Held-out HGA-A009 attacks

After the target is fixed, test independent public representations:

- `A4-heldout` from two fixed 3-cycles;
- `S4-heldout` from a transposition and 4-cycle;
- `A5-heldout` from a fixed 5-cycle and 3-cycle distinct from the training generator pair;
- product admissibility `A4-heldout x S4-heldout`;
- product admissibility `S4-heldout x A5-heldout`.

For every attack, the finite quotient is only a necessary admissibility filter. Exact free-group tuples remain authoritative. A candidate succeeds only if the recovered braid connector maps the original public source to the original public target exactly.

## Fixed Python 3.12 `hga4e-D8`

```text
exact distance:                         8
generator ball / shell:          2589 / 1356
ordinary balanced MITM:          230 states / 376 transitions

training S3 retained:                   1078  (41.64% of ball)
training A5 retained:                    227   (8.77% of ball)

held-out A4:                             445  (17.19% of ball)
held-out S4:                             571  (22.05% of ball)
held-out A5-alt:                         300  (11.59% of ball)
held-out A4 x S4:                        238   (9.19% of ball)
held-out S4 x A5-alt:                    181   (6.99% of ball)

all recovered connectors: length 8, exact endpoint verified
```

The generator therefore succeeds only against the representations it was explicitly allowed to optimize. A held-out product already keeps fewer exact states than the ordinary balanced MITM on this fixed endpoint.

## Deterministic `D=4/6/8 x 8` sweep

Every held-out attack recovers the exact public endpoint on **24/24** instances. Aggregate public-state retention is:

| held-out filter | accepted | <20% of full ball | fewer states than MITM | min fraction | max fraction | mean fraction |
|---|---:|---:|---:|---:|---:|---:|
| `A4` | 24/24 | 11/24 | 9/24 | 0.147826 | 0.438475 | 0.238370 |
| `S4` | 24/24 | 15/24 | 10/24 | 0.112012 | 0.568946 | 0.236306 |
| `A5-alt` | 24/24 | 19/24 | 18/24 | 0.016827 | 0.285962 | 0.124609 |
| `A4 x S4` | 24/24 | 22/24 | 19/24 | 0.074519 | 0.329545 | 0.130451 |
| `S4 x A5-alt` | 24/24 | **22/24** | **24/24** | **0.016827** | 0.234783 | **0.086906** |

The strongest held-out product is especially stable at the largest declared distance:

```text
S4 x A5-alt at D=8, eight seeds:
  accepted:                  8/8
  <20% of generator ball:    8/8
  fewer states than MITM:    8/8
  retained fraction range:   0.043260 .. 0.094402
  mean retained fraction:    0.069742
```

Thus the HGA4d leakage was not an accident of one training `A5` map. Conditioning against finitely many known quotient maps overfits those maps while other small public representations continue to expose strong admissibility filters.

## Interpretation

**HGA4e rejects the current exact-distance Hurwitz endpoint family as generically finite-representation-leaky on the measured toy distribution.** The result is stronger than HGA4d because held-out maps were never used during generation.

This is still not a claim that quotient-pruned one-sided BFS is the asymptotically best solver for the action. The important result is structural: small independent finite representations repeatedly preserve enough endpoint information to discard most exact states without creating false positives.

Do not repair this by adding the five held-out maps to the generator's training set. That would simply repeat the same overfitting loop. A successor needs an action/distribution for which an independently chosen finite representation does not routinely retain a tiny fraction of the exact search space.

No trapdoor primitive, KEM, one-wayness, post-quantum, IND-CPA/CCA, or production-security claim exists.