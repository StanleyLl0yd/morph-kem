# 95 — TDC-R0 freeze of the current TDC2g-derived ensemble

## Status

**Cryptographic progression of the current TDC2g-derived ensemble is frozen.**

The freeze follows TDC3c, which violated a predeclared same-weight matched-control checkpoint under bounded Lee–Brickell-style decoding. This is deliberately narrower than claiming that topology-derived sparse codes are generically weak.

No decoding-hardness, one-wayness, post-quantum, KEM, IND-CPA/CCA or production-security claim exists.

## Why the family stops here

TDC3b had survived a bounded deterministic Prange/ISD gate after its initially suspicious `n10 × 8` signal reversed on the predeclared `n10 × 32` validation set.

TDC3c therefore strengthened the attack without changing the generator:

```text
trial budgets:  1 / 4 / 16
outside orders: 0 / 1 / 2
n8  ×  8 seeds × weights 1..6
n9  ×  8 seeds × weights 1..6
n10 × 32 seeds × weights 1..6
```

The all-weight `n10 × 32` aggregate is mixed. At the strongest declared checkpoint (`order<=2`, `budget=16`), matched controls are actually solved slightly more often:

```text
topology: 187 / 192
control:  191 / 192
```

Therefore TDC3c does **not** justify a family-wide statement that topology makes Lee–Brickell decoding easier.

However, the rejection rule was written before measurement at the same error weight and fixed `(max_order,budget)` checkpoint level. That rule fails reproducibly.

## Mandatory failed checkpoint

At `n10`, planted/public weight `2`, one information-set trial:

```text
                         topology   control
order <= 0                  5          1
order <= 1                 13          5
order <= 2                 14          5
```

At `(weight=2, order<=2, budget=1)`, paired outcomes over 32 seeds are:

```text
topology-only: 10
control-only:   1
both:           4
neither:       17
```

A second topology-easier window appears at weight `4`, `order<=2`, budget `4`:

```text
topology success: 26 / 32
control success:  20 / 32

topology-only: 11
control-only:   5
both:          15
neither:        1
```

Reverse windows also exist. That is why the result is a **freeze of this exact ensemble under its declared gate**, not a theorem about topology-derived codes.

## Why the gate is not redefined after measurement

It would be easy to rescue the family post hoc by saying only the all-weight aggregate matters. That was not the rule written before the experiment.

Changing the success criterion after seeing the local matched failure would invalidate the falsification discipline that preserved earlier negative results such as:

- the false topology-easier signal in TDC3b `n10 × 8`;
- its reversal on mandatory `n10 × 32` validation;
- the TDC2f/TDC2g low-weight control comparisons;
- earlier quotient and role-recovery failures.

The correct response is therefore to stop the current ensemble, preserve the mixed data, and redesign.

## Frozen changes

Do **not** continue the exact current family by merely changing:

- number of random overlay parity rows;
- mesh/lift size while preserving the same construction;
- planted error weights;
- seed filtering;
- matched-control generation after observing decoder output;
- Prange/Lee–Brickell trial budgets;
- degree/rank/rate parameters chosen to erase the failed checkpoint.

Those are parameter rescue, not a new construction.

## Preserved TDC corpus

Keep the whole lineage as calibration evidence:

- **TDC0** — public incidence/triangle structure gives weight-three codewords and direct syndrome recovery;
- **TDC1** — graph lifts remain graphic, keep `d_min=3`, admit T-join decoding and leak the base quotient;
- **TDC2** — non-graphic `∂2` moves the forced local word to tetrahedron boundaries of weight four;
- **TDC2b** — tetrahedron suppression moves the leakage to weight six rather than eliminating it;
- **TDC2c** — regular lifts leak exact fibres/base through public color refinement;
- **TDC2d** — irregular expansion removes the 1-WL fibre shortcut but retains topology-specific weight-six words;
- **TDC2e/TDC2f** — coordinate mixing and rank matching expose new distribution-level effects;
- **TDC2g** — common random overlays finally pass the declared low-weight search through weight eight on `n10×32`;
- **TDC3** — greedy/reliability and exact bounded decoding show no stable topology-easier signal;
- **TDC3b** — bounded Prange survives after the mandatory larger validation reverses the initial small-sample signal;
- **TDC3c** — low-order Lee–Brickell matched checkpoints finally falsify the exact current ensemble.

Do not rewrite a survival result as hardness and do not rewrite a local rejection as a universal weakness theorem.

## Re-entry requirements for a future TDC redesign

A materially new TDC ensemble must define **before implementation**:

1. public matrix/complex generation;
2. what topological structure remains public/recoverable;
3. matched-control generation fixed independently of attack output;
4. exact matching requirements for dimensions, rank, rate and public degree profiles;
5. public error/noise distribution;
6. attacker success as any syndrome-equivalent verifier-accepted error;
7. low-weight search and quotient/base-role recovery;
8. greedy/BP-style decoder baseline;
9. bounded Prange checkpoints;
10. low-order Lee–Brickell checkpoints from the first experiment, not added later;
11. a mandatory larger validation slice;
12. an explicit multiple-checkpoint rule that cannot be averaged away after measurement.

Only after such a redesigned ensemble survives those gates should stronger Stern/BJMM-style toy attacks be worth implementing.

## Research consequence

TDC is not abandoned as mathematics. The **current** TDC2g-derived cryptographic family is abandoned as a progression target.

A future return must change the ensemble structurally enough that TDC3c is no longer merely being re-run with tuned parameters.

No security claim.
