# 80 — TDC2f rank-matched public-kernel control

## Status

**TDC2f is rejected by TDC-A008 on the measured generated distribution.** TDC2f successfully removes the fatal TDC2e rank/rate confounder: topology and independently generated random controls have identical public `(rows, columns, rank, dimension, rate)` by construction. After that repair, search through weight six no longer cleanly separates the families. However, exact meet-in-the-middle search through weight eight reveals a stable excess on the largest declared `n10` topology family: **8/32 topology instances** contain a public kernel word of weight at most eight, versus **0/32 rank-matched random controls**.

This is a generated-distribution falsification result, not an asymptotic theorem about random linear codes or topology-derived codes.

TDC2f is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Construction

For each TDC2b topology matrix with `n` columns and rank `r`:

1. compute a deterministic independent basis of its public row space, yielding an equivalent `r x n` parity-check matrix with the same kernel;
2. apply two rounds of invertible row additions to remove the canonical basis presentation;
3. apply two complete rounds of the TDC2e invertible variable-coordinate additions;
4. publicly relabel rows and columns.

The matched control is generated directly as an independent full-rank binary `r x n` matrix with nonzero distinct columns. It receives independent row scrambling, the same declared two-round variable-mixing budget, and public relabeling.

Consequently every topology/control pair has identical public:

- row count;
- column count;
- rank;
- dimension;
- rate.

Generation never queries low-weight search, Tanner statistics, or attack output.

## TDC-A008 — exact bounded-weight kernel search

### Rank/dimension regression

All measured topology/control pairs match exactly on `(rows, columns, rank, dimension, rate)`. The TDC2e rank distinguisher is therefore genuinely removed rather than masked.

### Search through weight six

The existing exact search checks zero/duplicate columns, pair/triple syndrome collisions, and disjoint supports through weight six.

On the original `n8/n9/n10 x 8` sweep:

- topology has a word of weight `<=6` on **6/24** instances;
- rank-matched random controls have one on **5/24**;
- the two distributions overlap strongly at this gate.

Thus the old TDC2d/TDC2e `<=6` signal is no longer a clean distinguisher once rank/dimension is fairly matched.

### Exact meet-in-the-middle extension through weight eight

Only when no word through weight six is present, index every public 3-subset by its XOR syndrome and scan public 4-subsets.

- equal `3+4` syndromes with disjoint supports give a weight-seven codeword;
- equal `4+4` syndromes with disjoint supports give a weight-eight codeword;
- every returned support is XOR-verified against the full public matrix before acceptance.

The implementation records the number of indexed triples, scanned four-subsets and syndrome-collision candidates. It does not hide exponential/combinatorial work.

## Fixed Python 3.12 `tdc2f-n10`

```text
target rank:                         36
rank profiles equal:                 yes
dimension profiles equal:            yes

topology rows / columns:          36 / 67
topology rank / dimension:        36 / 31
topology rate:                   0.462687
random rows / columns:            36 / 67
random rank / dimension:          36 / 31
random rate:                     0.462687

row-scramble operations:           72 / 72
column-mixing operations:        134 / 134
rejected mixing candidates:          0 / 0
minimum public kernel <=6:      none / none
minimum public kernel <=8:      none / none
triple subsets indexed:       47905 / 47905
four-subsets scanned:       766480 / 766480
```

The fixed baseline itself survives through weight eight in both families; the rejection comes from the deterministic distribution sweep, not a cherry-picked fixed instance.

## Original 8-seed all-size sweep

Presence of any public kernel word of weight `<=8`:

```text
size   topology   rank-matched random
n8        8/8            8/8
n9        7/8            7/8
n10       4/8            0/8
```

At n8 and n9, bounded low-weight words are common in both rank-matched families and therefore do not distinguish topology. At n10 the topology/control behavior separates sharply, motivating the pre-declared extended largest-size screen rather than an immediate verdict from only eight seeds.

## Extended `n10 x 32` screen

Without changing the generator, matrix dimensions, mixing budget, search bound, or attack logic, extend only the largest declared `n10` family from eight to 32 deterministic seeds.

Result:

```text
public kernel weight <=8:
  topology:             8 / 32
  rank-matched random:  0 / 32
```

The eight topology hits are seeds `2, 3, 4, 7, 13, 14, 16, 21` in the declared deterministic sweep. Two are weight seven (`13`, `21`); the remaining six are weight eight. Every witness passes the full public XOR check.

All 32 random controls complete the exact search through weight eight without a hit. Depending on public column count, a no-hit n10 search indexes roughly `43,680–52,394` triples and scans `677,040–864,501` four-subsets per matrix.

## Other public profiles

Exact Tanner 4-cycle counts and row/column weight histograms were retained as calibration measurements. Their direction is not stable enough across seeds to serve as the rejection argument. The rejection therefore does **not** depend on post-hoc selection of one noisy profile statistic.

## Interpretation

TDC2f is a useful repair experiment because it shows that the TDC lineage can remove the trivial rank leak without making the topology-specific kernel structure disappear. Once obvious algebraic dimensions are matched, the direct `<=6` signal mostly collapses into the random baseline, but extending the exact bounded search by only two weights exposes a topology-specific excess at the largest tested size.

This rejects the current rank-matched generated distribution. It does not prove an asymptotic distance gap, and it does not justify extrapolating from 32 toy instances to cryptographic parameters.

A successor must change the topology-derived relation itself rather than add another invertible basis disguise. Before any decoder-hardness claim, it must use matched controls for rank/rate **and** low-weight distance profile, then face OSD/ISD/MITM/BP and sparse-coordinate-recovery attacks.

No security claim.