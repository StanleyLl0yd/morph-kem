# 76 — TDC2d irregular role-mixed Tanner expansion

## Status

**TDC2d is rejected by TDC-A006.** Irregular role-mixed expansion successfully removes the exact 1-WL fiber-recovery shortcut that killed TDC2c, but the resulting public topology codes still exhibit bounded weight-six kernel words at a rate sharply separated from matched-random irregular controls.

TDC2d is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Construction

Start from each tetrahedron-free TDC2b base matrix and its degree-matched random control.

For every base check row, choose a deterministic seeded multiplicity in `{2,3}`. Every base variable receives exactly two clones. For each base incidence and each variable clone, connect it to exactly one clone of the corresponding base check using a seeded modular shift.

Consequences:

- there is no single public lift degree;
- check fibers have mixed sizes 2 and 3;
- each public variable column still has weight exactly 3;
- paired variable clones select different check clones, so duplicate public columns are forbidden;
- all public check and variable labels are globally relabeled.

The same check-multiplicity profile is used for the topology and matched-random bases; incidence shifts are generated independently.

## TDC-A006 gate 1 — public 1-WL / equitable signatures

Run ordinary bipartite role+degree color refinement to stabilization. Record public class-size statistics. For calibration only, compare stabilized classes with planted row/column fibers **after** public refinement.

The TDC2c failure mode is removed on the measured TDC2d family:

- exact planted row fibers recovered by one color class: **0 on every measured instance**;
- exact planted column fibers recovered by one color class: **0 on every measured instance**;
- most public vertices stabilize as singleton colors;
- the largest residual color classes have size only 1–3 on the measured sweep.

This is a successful repair of the specific TDC2c 1-WL shortcut only. It is not hardness evidence.

## TDC-A006 gate 2 — quotient-free low-weight search

Run the exact binary kernel search through weight six directly on the expanded public matrices, without recovering a quotient:

- zero / duplicate columns;
- pair-syndrome weight 3/4 search;
- pair/triple collisions for weight 5;
- disjoint triple collisions for weight 6.

The identical search runs on matched-random irregular expansions with the same public size/check-multiplicity profile.

## Fixed Python 3.12 result

For `tdc2d-n10`:

```text
topology rows / columns:          120 / 132
check multiplicities:              15x2 + 30x3
column weights:                     all 3
1-WL rounds:                        5
color classes:                      249 singleton + one size-3
exact row fibers by color:          0 / 45
exact column fibers by color:       0 / 66
minimum public kernel weight <=6:   6
minimum-weight multiplicity:        1
triple-collision buckets:           10

matched random rows / columns:      120 / 132
exact row fibers by color:          0 / 45
exact column fibers by color:       0 / 66
minimum public kernel weight <=6:   none
```

The fixed topology expansion contains three zero-degree public check clones. These are redundant zero rows and can be deleted publicly without changing the binary kernel or removing the measured weight-six codeword; they are therefore a construction-quality defect but not the cause of the rejection.

## Eight-seed / multi-size sweep

Across `tdc2d-n8`, `tdc2d-n9`, `tdc2d-n10` × eight seeds:

- the old exact-fiber 1-WL shortcut is absent on **24/24 topology** and **24/24 matched-random** expansions;
- exact row-fiber recovery by a stabilized color class is 0 throughout;
- exact column-fiber recovery by a stabilized color class is 0 throughout;
- public quotient-free search finds a weight-six kernel word on **14/24 topology expansions**;
- the same search finds **0/24** such words on matched-random irregular controls;
- topology incidence by size is:

```text
tdc2d-n8:   3 / 8
tdc2d-n9:   5 / 8
tdc2d-n10:  6 / 8
```

Thus the incidence of bounded public kernel words rises rather than disappears over the declared size ladder, while the paired random controls remain clean through weight six.

The measured topology words arise from disjoint triple-syndrome collisions. They are found directly in the public expanded matrix; no fiber labels, quotient recovery or planted reference are required.

## Interpretation

TDC2d demonstrates a useful negative distinction:

1. irregular expansion **does** defeat the specific regular-cover/fiber-recovery failure of TDC2c;
2. nevertheless, the topology-derived code remains publicly distinguishable from a degree/profile-matched random control by bounded low-weight kernel structure.

This is stronger evidence against the current topology-code lineage than merely recovering a hidden quotient: even after the quotient shortcut is removed, a quotient-free exact attack still sees the inherited combinatorial structure.

Increasing only the expansion size or making fibers harder to recognize is not a repair while weight-six public relations remain common and increasingly frequent relative to matched random controls.

## Successor gate

A TDC successor must change the relation itself rather than only obfuscate base roles. Before any advancement it must face:

- direct minimum-distance / low-weight collision search without quotient assumptions;
- Tanner girth and trapping-set measurements;
- BP / bit-flipping;
- OSD / ISD / MITM;
- matched-random controls with the same public degree distribution;
- quotient / WL / automorphism attacks only as secondary structure diagnostics.

No security claim.
