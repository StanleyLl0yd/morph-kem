# 65 — HGA3 simultaneous matrix-tuple conjugation negative control

## Status

**HGA3 is a falsification experiment in progress.** It removes HGA1's small finite-orbit failure and HGA2's Euclidean endpoint normal form, then tests whether the action itself linearizes.

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

Although simultaneous conjugacy looks nonlinear when written with `X^-1`, the endpoint relation is equivalent to

```text
X A_i = B_i X.
```

For fixed public `A_i,B_i`, these are homogeneous linear equations in the `n^2` unknown entries of `X`.

The attack:

1. constructs all `k n^2` public linear equations over `F_p`;
2. performs exact modular RREF;
3. extracts a basis for the public nullspace/intertwiner space;
4. deterministically enumerates sparse linear combinations of basis vectors;
5. stops at the first full-rank/invertible matrix;
6. verifies all simultaneous conjugacy equations directly;
7. compares with planted `S` only after public success.

A recovered conjugator that differs from `S` is attacker success. Scalar multiples or other centralizer-induced alternatives are explicitly expected and measured.

## Independent invariant cross-check

Conjugacy preserves traces. The implementation records traces of every tuple component plus short trace-word fingerprints such as `tr(A1 A2)` and `tr(A1 A2 A3)` on both public endpoints. These are diagnostics, not the inversion attack.

## Measurements

Record at least:

- prime `p`, matrix dimension `n`, tuple length `k`;
- public variable/equation counts;
- RREF rank/nullity and row-elimination work;
- nullspace dimension;
- invertible linear-combination candidates tested;
- recovered matrix rank/determinant;
- exact public endpoint verification;
- post-success scalar equivalence and exact equality to planted `S`;
- source/target trace fingerprints;
- deterministic all-size / multi-seed sweep.

## Rejection gate

Reject HGA3 if public linear algebra routinely yields an invertible intertwiner with small work. Do not repair by increasing only `n`: the relation remains a public `n^2`-variable homogeneous linear system.

## Advancement gate

HGA4 may proceed only to an action whose endpoint inversion does not immediately linearize to an intertwiner/kernel problem. It must still face finite-dimensional representations, quotient actions, invariant theory, stabilizers/equivalent actions, canonical forms, bounded-ball MITM and quantum hidden-shift/subgroup screening.

No security claim.
