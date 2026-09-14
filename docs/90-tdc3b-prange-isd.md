# 90 — TDC3b bounded Prange / ISD control

## Status

**TDC3b survives TDC-A011 on the declared toy distribution.** The initial `n10 × 8` slice showed an apparent topology-easier work signal, but the already-predeclared `n10 × 32` validation extension reversed that signal. The larger validation does not show topology-derived instances being easier than matched controls under the fixed Prange budgets.

This is survival of one bounded toy decoder-work gate only. It is not evidence of asymptotic decoding hardness, one-wayness, post-quantum security, or KEM suitability.

## Fixed ensemble

TDC3b reuses the exact TDC2g-derived paired ensemble already measured in TDC3:

- topology-derived parity-check matrix;
- matched-random control with identical public dimensions, rank, rate and planted support indices;
- planted weights `1..6`;
- `n8/n9/n10 × 8` deterministic seeds.

No generation parameter is conditioned on decoder output.

The public decoder receives only the parity-check matrix, target syndrome and public weight bound. The planted support is reference-only. **Any syndrome-equivalent accepted error is attacker success.**

The implementation also checks explicitly that the fixed public matrices are full-row-rank, so the Prange information-set size is the actual public rank `r`, not an implicit row-count approximation.

## TDC-A011 — bounded deterministic Prange / ISD

For a public rank-`r` parity-check matrix `H` and target syndrome `s`, each trial:

1. derives a deterministic public permutation of the `n` columns from a domain-separated hash of the public matrix, target syndrome and trial index;
2. takes the first `r` columns as the candidate information/parity set;
3. rejects the trial if the resulting `r × r` GF(2) matrix is rank-deficient;
4. otherwise solves the square system for the unique error supported on those `r` positions whose syndrome is `s`;
5. maps the solution back to public column coordinates;
6. accepts only if the candidate verifies publicly and has Hamming weight at most the declared bound.

The implementation records exact public work rather than wall-clock timing.

## Predeclared budgets

Before measurement, cumulative trial checkpoints were fixed at

```text
8
32
128
```

No extra trial budget was introduced after looking at the sweep.

## Work accounting

The measured counters include:

- information sets attempted;
- rank-deficient sets rejected;
- full-rank candidate systems solved;
- pivot scans;
- pivot swaps;
- GF(2) row-XOR operations;
- accepted candidate weight;
- verifier-correct success by each cumulative checkpoint.

## Primary `n8/n9/n10 × 8` sweep

At the largest `n10 × 8` slice, aggregate work initially appeared topology-easier:

```text
                    topology      control      delta
information sets        965          1303       -338
rank-deficient          685           944       -259
full-rank solved        280           359        -79
row XORs             778739       1052548    -273809
pivot scans           77950        105096     -27146
row swaps             19150         25820      -6670
```

At the same time, the smaller sizes did **not** preserve that sign:

```text
n8 attempts: 399 topology vs 355 control
n9 attempts: 898 topology vs 674 control
```

and both `n8` and `n9` used more row-XOR work on topology than on controls. Therefore the `n10 × 8` observation was treated as a possible signal, not as a conclusion.

Per the rule written before those results, this automatically activated the predeclared `n10 × 32` validation extension with the same generator, decoder, weights and `8/32/128` budgets.

## Predeclared `n10 × 32` validation

Across `32 seeds × weights 1..6 = 192` paired targets, cumulative public success is:

```text
budget          topology    control    delta
8 trials           75          78        -3
32 trials         146         154        -8
128 trials        182         184        -2
```

Per-weight success is mixed rather than consistently topology-favorable:

```text
weight   @8 top/control   @32 top/control   @128 top/control
1            29 / 27          32 / 32           32 / 32
2            17 / 19          32 / 32           32 / 32
3            12 / 10          30 / 29           32 / 32
4             8 / 14          24 / 26           32 / 32
5             6 /  5          17 / 20           31 / 30
6             3 /  3          11 / 15           23 / 26
```

Aggregate work on the validation extension is:

```text
                         topology      control      delta
information sets            4951          4531       +420
rank-deficient              3481          3247       +234
full-rank solved            1470          1284       +186
row XORs                 3994444       3662118    +332326
pivot scans               402158        364874     +37284
row swaps                  98810         89582      +9228
```

Thus the larger validation reverses the initial `n10 × 8` work signal: topology requires about 9% more information-set attempts and GF(2) row-XOR work, while its success counts are slightly lower overall at all three fixed budgets.

The initial topology-easier observation therefore **does not reproduce** and is retained as a sampling fluctuation rather than discarded.

## Verdict

TDC-A011 does not falsify the current TDC2g-derived ensemble under this bounded deterministic Prange experiment. The topology/control ordering changes with sample and size, and the predeclared largest validation does not favor the attacker on topology.

This result justifies a stronger successor attack only; it does not justify changing the generator, scaling parameters, defining a trapdoor, or making a security claim. A successor should keep the same paired ensemble and test a stronger bounded ISD/OSD family with attack parameters declared before measurement.

No trapdoor primitive, KEM, one-wayness, post-quantum, IND-CPA/CCA, or production-security claim exists.
