# 65 — HGA3 simultaneous matrix-tuple conjugation negative control

## Status

**HGA3 is rejected by HGA-A004.** Simultaneous matrix conjugacy looks nonlinear through `X^-1`, but the public endpoint relation linearizes exactly to an intertwiner nullspace problem.

HGA3 is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Public action

Over a toy prime field `F_p`, generation samples a tuple of matrices

```text
A = (A1, A2, ..., Ak)
```

and a hidden invertible matrix `S`. The public target tuple is

```text
B_i = S A_i S^-1.
```

The verifier accepts any invertible matrix `X` satisfying all simultaneous conjugacy equations. It never compares `X` against planted `S`.

Toy sets:

```text
hga3-p5-n3:  p=5,  n=3, k=3
hga3-p7-n4:  p=7,  n=4, k=3
hga3-p11-n5: p=11, n=5, k=3
```

## HGA-A004 — public intertwiner-space recovery

The endpoint relation is equivalent to

```text
X A_i = B_i X,
```

which gives `k n^2` homogeneous linear equations in the `n^2` unknown entries of `X`.

The attack performs exact modular RREF, extracts the public nullspace, tests deterministic linear combinations for invertibility, and verifies simultaneous conjugacy directly. A scalar multiple or any other valid conjugator is attacker success.

## Fixed Python 3.12 result

For `hga3-p11-n5`:

```text
prime / n / tuple length:          11 / 5 / 3
linear variables / equations:      25 / 75
system rank / nullity:             24 / 1
RREF row eliminations:             1399
invertible combinations tested:    1
recovered rank / determinant:      5 / 10
endpoint verified:                 yes
scalar-equivalent to planted S:    yes
exactly equals planted S:          no
trace fingerprint:                 (8,1,9,3,10)
```

The one-dimensional public intertwiner space already contains an invertible basis vector, so no meaningful combinatorial search remains.

## Deterministic sweep

Python 3.12 tested all three toy sets over eight deterministic seeds each:

- **24/24** systems have nullity exactly `1`;
- **24/24** recover an invertible public intertwiner on the **first** tested nullspace vector;
- **24/24** recovered matrices pass exact simultaneous-conjugacy verification;
- **24/24** are scalar-equivalent to the planted conjugator;
- only **5/24** equal the planted matrix literally, while **19/24** are different nonzero scalar representatives;
- RREF ranks are exactly `8/15/24` for dimensions `3/4/5`, leaving the expected one-dimensional intertwiner line;
- measured row-elimination work ranges from roughly 119 to 1496 operations across the toy sets.

Source and target trace-word fingerprints agree on every instance. Dedicated HGA3 CI passes on Python 3.11, 3.12 and 3.13.

## Result

**HGA3 is rejected by HGA-A004.** The action family is not repaired by lacking a finite orbit or Euclidean endpoint normal form: public inversion is simply linear algebra in `n^2` variables.

The measured scalar multiplicity is also semantically important. Recovering planted `S` exactly is unnecessary; any invertible point on the public intertwiner line gives the same conjugation action and is attacker success.

Increasing only `n` is not a justified repair while the same homogeneous intertwiner system exists.

## HGA4 gate

HGA4 may proceed only to an action whose endpoint inversion does not immediately linearize to an intertwiner/kernel problem. It must still face finite-dimensional and finite-quotient representations, invariant theory, stabilizers/equivalent actions, canonical forms, bounded-ball MITM, generated-distribution leakage and quantum hidden-shift/subgroup screening.

No security claim.
