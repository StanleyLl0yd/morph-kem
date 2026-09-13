# 77 — HGA4d finite free-group quotient pruning

## Status

**HGA4d is rejected by HGA-A008 as a quotient-leaky endpoint family.** Exact-distance HGA4c endpoints remain verifier-correct and generic balanced MITM is still the strongest uniform end-to-end attack measured here, but a tiny public `A5` quotient systematically eliminates most exact free-group states while preserving exact recovery on every measured endpoint.

This is not a canonical inversion of the infinite Hurwitz action, and the quotient-pruned one-sided search does not uniformly beat balanced MITM in wall-clock work or transition count. The rejection is specifically that the tested endpoint distribution leaks a strong public finite-representation admissibility filter.

HGA4d is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Instance distribution

Reuse the HGA4c exact-distance shell construction at public distances `D=4,6,8`. The endpoint is certified to have exact action distance `D`, so a shorter exact connector would be a calibration error.

The HGA4d parameter names derive independent deterministic source samples, but the generator method is the same exact-shell method as HGA4c.

## Finite quotients

Each free-group component is mapped homomorphically into two fixed public permutation groups:

- `S3`: `a=(0 1)`, `b=(1 2)`;
- `A5`: `a=(0 1 2)`, `b=(0 3 4)`.

The Hurwitz action commutes with these homomorphisms. For each public target, HGA4d builds a reverse-distance table in the finite quotient action through the full public bound.

## HGA-A008 — quotient-admissible exact recovery

The quotient is used only as a necessary pruning condition; it is never an authoritative witness space.

Starting from the public exact source:

1. enumerate exact free-group tuple states by increasing depth;
2. for a candidate at depth `d`, compute its finite quotient state;
3. consult the public quotient reverse-distance table;
4. discard the exact candidate if its quotient cannot reach the quotient target within the remaining `D-d` moves;
5. otherwise retain the exact free-group tuple and continue;
6. recover the exact public target and verify the resulting braid word against the original free-group action.

Finite-quotient collisions therefore cannot create a false positive. They can only weaken pruning.

The experiment also runs the ordinary HGA4 balanced MITM attack as an independent exact-state baseline.

## Fixed Python 3.12 result

For `hga4d-D8`:

```text
exact distance:                         8
generator ball / shell:             2589 / 1356
ordinary balanced MITM states:           230
ordinary balanced MITM transitions:      376
ordinary connector / verified:         8 / yes

S3 reverse states / transitions:        8 / 32
S3 quotient distance / exact gap:       0 / 8
S3 exact states kept:                     961
S3 exact transitions tested:             3156
S3 state fraction of generator ball: 0.371186
S3 connector / verified:               8 / yes

A5 reverse states / transitions:      233 / 868
A5 quotient distance / exact gap:       6 / 2
A5 exact states kept:                     163
A5 exact transitions tested:              604
A5 candidate prunes:                       220
A5 distinct quotient states seen:           75
A5 max exact states per quotient:            16
A5 state fraction of generator ball: 0.062959
A5 connector / verified:               8 / yes
```

The A5 filter keeps fewer exact states than ordinary MITM in this fixed case, but the one-sided pruned BFS performs more transitions. This is why the result is classified as representation leakage, not as a uniformly superior solver.

## Eight-seed / multi-distance sweep

Across `D=4,6,8` × eight seeds, both quotient attacks recover the exact target at the certified distance on **24/24** instances.

`S3` is weak and inconsistent. Depending on the source/target quotient collision, it retains between about 20% and 100% of the full exact generator ball and sometimes gives essentially no pruning.

`A5` is materially stronger:

- exact recovery succeeds on **24/24**;
- retained exact-state fraction ranges from **0.003476 to 0.351820** of the generator ball;
- **20/24** measured endpoints retain less than 20% of the generator ball;
- all eight `D=8` endpoints retain at most about 19.1%;
- the strongest measured `D=8` case keeps only **9 exact states out of 2589** (`0.3476%`) and still recovers the exact length-eight connector;
- quotient-only distances can be strictly smaller than exact distance, so the quotient does not itself solve the original word problem; it acts as an admissibility filter.

The A5 finite orbit/reverse table remains tiny on these controls (at most a few hundred quotient states) while exact free-group words and target component lengths can be much larger.

## Interpretation

HGA4d provides a structural negative result distinct from HGA4b/c:

- HGA4b showed that greedy self-avoiding planted histories remain non-geodesic;
- HGA4c removed that artifact but exposed the generic full-BFS-generation versus balanced-MITM asymmetry;
- HGA4d shows that even those exact-distance endpoints carry substantial public information in a very small finite representation.

The `A5` quotient is not a complete invariant and does not uniformly beat balanced MITM. Nevertheless, a distribution for which a fixed tiny public quotient routinely deletes 65–99.6% of the exact generator state space cannot be treated as representation-opaque.

A successor must therefore avoid selecting endpoints whose small finite representations are unusually restrictive, and must immediately face multiple independent finite/matrix quotients. Conditioning generation on attack output is not an acceptable repair.

No security claim.
