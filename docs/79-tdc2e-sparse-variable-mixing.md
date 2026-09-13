# 79 — TDC2e sparse invertible variable-mixing control

## Status

**TDC2e is rejected by TDC-A007.** The sparse invertible variable transform removes many of the direct low-weight words that killed TDC2d, but it cannot alter the binary rank of the public matrix. The TDC2b topology family and its degree-matched random control already have different rank/dimension profiles, so the mixed public instances remain perfectly distinguishable by a cheaper invariant before any sparse-factorization attack is needed.

TDC2e is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Construction

Start from each TDC2b topology sparse-face matrix and its degree-matched random control.

Apply two complete rounds of elementary invertible column additions. In every round every public variable coordinate is targeted exactly once, in seeded deterministic order. For each target choose the first seeded source producing a nonzero column distinct from every other current column:

```text
column[target] <- column[target] XOR column[source].
```

Every accepted step is an elementary invertible binary change of variable coordinates. A rejected candidate is rejected only for the local malformed conditions zero/duplicate; generation never queries low-weight search, Tanner statistics or decoder output.

After mixing, globally relabel rows and columns. Topology and matched-random matrices use independent histories but identical declared mixing budgets.

## TDC-A007 — public rank/rate invariant

The first public profile gate is already fatal. Elementary column additions are multiplication by an invertible matrix on the variable side, and public row/column relabeling is also invertible. Therefore neither operation can change matrix rank.

On the declared deterministic sweep the topology and matched-random families separate exactly:

```text
parameter   topology rank   random rank
n8                  21            28
n9                  28            36
n10                 36            45
```

Those ranks are seed-invariant across all eight seeds at each size. Thus all **24/24 topology** instances and **24/24 matched-random** controls are classified by the public rank alone. No quotient, hidden mixing history, low-weight search, or topology labels are required.

This is structural leakage preserved by every invertible variable-coordinate transform. Adding more invertible mixing rounds cannot repair it.

## Secondary direct low-weight result

The mixing does suppress much of the TDC2d bounded-weight signal, but not all of it. Exact public kernel search through weight six finds a relation on:

- `n8`: **6/8** topology instances;
- `n9`: **1/8** topology instances;
- `n10`: **1/8** topology instances;
- matched-random controls: **0/24**.

So weight-six-or-lower relations remain an additional topology-specific distinguisher on **8/24** mixed topology instances, even though the rank invariant has already rejected the family.

The fixed Python 3.12 `tdc2e-n10` baseline itself has no kernel word through weight six in either family, but already exposes the fatal rank split:

```text
topology rows / columns:        45 / 67
topology rank / dimension:      36 / 31
random rows / columns:          45 / 67
random rank / dimension:        45 / 22
mixing operations:             134 / 134
rejected mixing candidates:      0 / 0
```

## Tanner and sparse-atom calibration

The experiment also records row/column weight histograms, exact Tanner 4-cycle counts, surviving public weight-three columns, and pair-XOR-derived weight-three vectors. These quantities are retained as calibration evidence, but they are not needed for the rejection verdict because rank is cheaper, exact, and universal on the declared sweep.

In the fixed `n10` baseline, for example, topology has zero public weight-three columns and zero pair-derived weight-three atoms, while the random control has one singleton and two pair-derived atoms. Sparse-atom recovery therefore does **not** explain the topology rejection here.

## Measurements

Across `n8/n9/n10 × 8` seeds:

- every topology/random pair preserves its base rank under two full mixing rounds;
- the rank split is perfect at every declared size;
- mixing candidate rejections are zero throughout the measured sweep;
- bounded public kernel words through weight six remain on 8/24 topology instances and 0/24 controls;
- pair/triple syndrome collisions, Tanner 4-cycles and low-order atom counts are recorded for secondary analysis.

## Interpretation

TDC2e demonstrates that changing only the variable basis cannot hide a basis-invariant topological signature. The correct successor must change the public relation in a way that equalizes obvious algebraic invariants such as rank/rate **by construction**, with independently generated matched controls, before any decoding-hardness question is meaningful.

Do not repair TDC2e by increasing the number of invertible mixing rounds or making the mixing denser. Rank survives every invertible basis change exactly.

No security claim.