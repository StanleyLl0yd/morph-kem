# 79 — TDC2e sparse invertible variable-mixing control

## Status

**TDC2e is a falsification experiment in progress.** TDC2d removes the exact 1-WL fiber shortcut of a regular cover, but direct public quotient-free search still finds weight-six kernel words on 14/24 topology expansions and none of the paired matched-random controls. TDC2e changes the variable coordinates of the code instead of adding another hiding layer around the same columns.

TDC2e is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Construction

Start from each TDC2b topology sparse-face matrix and its degree-matched random control.

Apply two complete rounds of elementary invertible column additions. In every round every public variable coordinate is targeted exactly once, in seeded deterministic order. For each target choose the first seeded source producing a nonzero column distinct from every other current column:

```text
column[target] <- column[target] XOR column[source].
```

Every accepted step is an elementary invertible binary change of variable coordinates. A rejected candidate is rejected only for the local malformed conditions zero/duplicate; generation never queries low-weight search, Tanner statistics or decoder output.

After mixing, globally relabel rows and columns. Topology and matched-random matrices use independent histories but identical declared mixing budgets.

## TDC-A007 first gates

### Direct quotient-free kernel search

Run the exact public kernel search through weight six directly on the mixed public columns. Record the first weight, multiplicity and pair/triple syndrome-collision buckets. Every discovered support is a public binary relation; no base quotient or mixing history is needed.

If weight six is absent routinely, extend the next gate to weight eight rather than treating absence as hardness evidence.

### Tanner profile

Record row/column weight histograms and exact Tanner 4-cycle count. Compare topology and matched-random mixed controls at the same base parameter sizes.

### Sparse atom screen

Because the hidden transform is deliberately sparse, test whether it leaves a cheap inverse signature. Count:

- public columns that still have Hamming weight three;
- pairs of public columns whose XOR has weight three;
- distinct weight-three vectors produced by those pairs.

These are public candidate `face-like` atoms. A large or topology-specific population means sparse mixing may be exposing a dictionary/basis-recovery route even when direct kernel words move to higher weight.

## Measurements

Record:

- rows/columns, rank/dimension/rate;
- successful operations and local rejected candidates;
- base and public column-weight histograms;
- public row-weight histogram;
- minimum kernel weight through six and multiplicity;
- pair/triple syndrome collision buckets;
- Tanner 4-cycles;
- singleton and pair-derived weight-three atom counts;
- identical matched-random measurements;
- deterministic n8/n9/n10 × multi-seed curves.

## Gate

Reject TDC2e if bounded public kernel words remain common or distinguishing, or if the sparse transform leaves an obvious low-order weight-three atom reconstruction channel. If both first gates survive, the next required work is exact weight-eight search plus explicit sparse-basis recovery and generic OSD/ISD/MITM/BP controls.

Removing one bounded-weight relation is not evidence of one-wayness, asymptotic hardness or post-quantum security.

No security claim.
