# 93 — TDC3c Lee–Brickell order-2 matched-control gate

## Status

**TDC3c rejects the current TDC2g-derived ensemble under its predeclared gate.**

The aggregate mandatory `n10 × 32` curves are mixed rather than uniformly topology-easier, and the strongest fixed attack actually succeeds slightly more often on matched controls. However, the gate was fixed before measurement at the **same error weight and fixed `(max_order,budget)` checkpoint** level. A clear topology-easier early-budget window appears inside that declared grid. Averaging over weights after observing it would weaken the gate post hoc, so the current ensemble does not advance.

This result is deliberately narrow: it does **not** establish a universal weakness of topology-derived codes, Lee–Brickell decoding, or sparse codes. It says only that this exact TDC2g-derived generator/distribution failed its own predeclared matched-control falsification rule.

No decoding-hardness or security claim exists.

## Fixed ensemble

TDC3c reuses exactly:

- `tdc3-n8`, `tdc3-n9`, `tdc3-n10`;
- topology-derived and matched-random matrices from the merged TDC2g line;
- common planted support indices;
- public error weights `1..6`.

Any syndrome-equivalent error of weight at most the declared bound is attacker success. Planted equality is measured only after public success.

No generator parameter was tuned after observing TDC3c output.

## TDC-A012 — bounded Lee–Brickell-style ISD

For a full-row-rank public parity-check matrix `H` and public target syndrome `s`, each information-set trial:

1. selects `r = rank(H)` columns using the existing public TDC3b information-set derivation;
2. rejects the trial if those columns are rank-deficient;
3. otherwise computes one public GF(2) coordinate map for the selected basis;
4. maps `s` and all nonbasis columns into basis coordinates;
5. enumerates nonbasis error subsets in deterministic order for exact outside orders `0`, `1`, and `2`;
6. linearly computes the unique basis completion for each outside subset;
7. forms the full error candidate;
8. checks the public weight bound and exact syndrome verifier.

Order zero is the Prange special case. Orders one and two strictly enlarge the public attack search.

An exact outside order larger than the public weight bound is skipped because no accepted candidate can contain that many outside errors. This optimization was made before reading the final measurement run and avoids inflating attack work with publicly impossible subsets.

## Fixed checkpoints

Before measurement, cumulative information-set budgets were fixed at

```text
1
4
16
```

and cumulative outside orders were fixed at

```text
0
1
2.
```

The implementation evaluates the same sixteen public information sets once and records success for all nine `(max_order,budget)` checkpoints. Work snapshots at `1/4/16` are fixed-budget exhaustion costs, independent of early success. A separate snapshot records work accumulated to the first strongest-attack accepted candidate.

No trial budget or outside order was increased after measurement.

## Exact GF(2) coordinate map

For selected basis matrix `M`, Gauss–Jordan elimination runs on

```text
[M | I]
```

to obtain

```text
[I | M^-1].
```

The right block maps any public syndrome to selected-column coordinates. Linearity then allows every outside subset to be compensated without repeating elimination.

Unit tests reconstruct public unit syndromes and verify them through the same exact syndrome function used by the attack verifier.

## Declared measurement

The larger `n10` validation was mandatory from the start:

```text
n8  ×  8 seeds × weights 1..6
n9  ×  8 seeds × weights 1..6
n10 × 32 seeds × weights 1..6
```

Thus the mandatory `n10` comparison contains 192 paired weight-cases per family. The `n10×32` distribution was not activated in response to an observed signal.

## Mandatory n10 × 32 aggregate picture

Across all six weights, the nine fixed checkpoints are:

```text
max order   budget    topology   control   delta
    0          1         12         12        0
    0          4         50         49       +1
    0         16        120        116       +4

    1          1         38         33       +5
    1          4        107        104       +3
    1         16        172        176       -4

    2          1         49         46       +3
    2          4        135        136       -1
    2         16        187        191       -4
```

The sign changes with attack budget. In particular, the strongest declared attack succeeds on

```text
topology: 187 / 192
control:  191 / 192
```

so there is no family-wide claim that topology is generally easier under this attack.

Paired all-weight discordance says the same thing. For `(max_order=2,budget=16)`:

```text
topology-only:   1
control-only:    5
both:          186
neither:         0
```

while at `(max_order=1,budget=1)` it is

```text
topology-only:  30
control-only:   25
both:            8
neither:       129
```

The aggregate signal is therefore mixed rather than monotone.

## The predeclared local gate that fails

The rejection rule was not defined only on the all-weight aggregate. It explicitly compared matched families at the same dimensions/rank/rate/**error weight** and any fixed `(max_order,budget)` checkpoint.

At `n10`, weight `2`, one public information-set trial gives:

```text
                         topology   control
order <= 0                  5          1
order <= 1                 13          5
order <= 2                 14          5
```

For the strongest of those one-trial checkpoints, the paired decomposition is:

```text
weight=2, order<=2, budget=1

topology-only:  10
control-only:    1
both:            4
neither:        17
```

This is not an artifact of comparing independent counts: ten paired seeds are solved only on the topology instance while one is solved only on its matched control.

A second topology-easier window appears at weight `4`, `order<=2`, budget `4`:

```text
success:         26 / 32 topology
                 20 / 32 control
paired:
  topology-only: 11
  control-only:   5
  both:          15
  neither:        1
```

There are also reverse windows where controls are easier, notably weight `5`, `order<=1`, budget `4` (`11/32` vs `17/32`) and weight `6`, `order<=2`, budget `4` (`17/32` vs `21/32`). This is why the result is **not** generalized into a theorem that topology makes decoding easier.

Nevertheless, the experiment's rule was deliberately conservative: a reproducible topology-easier checkpoint at matched public parameters is enough to stop cryptographic progression of the current ensemble. Redefining the rule now to require a favorable all-weight average would be post-measurement rescue.

## Smaller-size context

The smaller declared slices also fluctuate rather than establishing a clean scaling law.

For example, at weight `3`, `order<=1`, budget `1`:

```text
n8:   topology 3/8   control 1/8
n9:   topology 4/8   control 0/8
n10:  topology 9/32  control 6/32
```

while other checkpoints reverse sign. These observations are retained as diagnostics, not promoted into an asymptotic claim.

## Exact public work at n10 × 32

At the full 16-information-set budget, summed over all 192 weight-cases:

```text
                              topology      control
information sets                3072         3072
rank-deficient sets             2151         2208
full-rank maps                   921          864
GF(2) row XORs               2473924      2486692
pivot scans                   252066       247918
row swaps                      61666        61019
candidate weight tests        261343       246808
verifier calls                   783          742
```

Gaussian-elimination work is extremely close. Topology produces more full-rank information sets, so it also performs more outside-subset/candidate work. These totals do not rescue or independently condemn the ensemble; the rejection is driven by the predeclared matched checkpoint criterion above.

Work to first strongest-attack success is likewise mixed by weight:

```text
weight   top success/control   top trials   ctl trials   top XORs   ctl XORs
  1          31 / 32              94          115         76071      92812
  2          31 / 32              78          103         62889      82957
  3          32 / 32             116          114         93911      92702
  4          32 / 32             108          127         86467     103069
  5          31 / 32             122          117         97980      94516
  6          30 / 31             166          151        133598     122396
```

Again, no single global work ordering is claimed.

## Verdict

Under the rule written before measurement, **TDC3c fails the current TDC2g-derived ensemble**.

The scientifically conservative consequence is:

1. do not call TDC3c a survival;
2. do not average away the failed same-weight checkpoint after seeing it;
3. do not tune overlay rows, error weights, seeds, trial budgets or the same generator to recover a pass;
4. freeze cryptographic progression of this exact TDC2g-derived family;
5. preserve TDC0–TDC3c as a matched-control/negative-calibration corpus;
6. if TDC research continues, redesign the ensemble and make low-order ISD checkpoints part of the gate from the beginning.

This rejection does **not** prove a structural decoding attack on all topology-derived codes. It only prevents this measured toy family from being promoted past its own falsification standard.

No trapdoor primitive, KEM, one-wayness, post-quantum, IND-CPA/CCA or production-security claim exists.
