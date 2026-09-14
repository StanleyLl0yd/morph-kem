# 90 — TDC3b bounded Prange / ISD control

## Status

**TDC3b is a falsification experiment in progress.** TDC3 survives its measured matched greedy, exact-`<=6`, and public-reliability gates. TDC3b therefore moves to a stronger generic syndrome-decoding baseline while keeping the merged TDC2g generator and the TDC3 error schedule unchanged.

This is not a hardness or security claim.

## Fixed ensemble

TDC3b reuses the exact TDC2g-derived paired ensemble already measured in TDC3:

- topology-derived parity-check matrix;
- matched-random control with identical public dimensions, rank, rate and planted support indices;
- planted weights `1..6`;
- `n8/n9/n10 × 8` deterministic seeds.

No generation parameter is conditioned on decoder output.

The public decoder receives only the parity-check matrix, target syndrome and public weight bound. The planted support is reference-only. **Any syndrome-equivalent accepted error is attacker success.**

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

Before measurement, cumulative trial checkpoints are fixed at

```text
8
32
128
```

No extra trial budget may be introduced after looking at the sweep.

## Work accounting

Record per attack at least:

- information sets attempted;
- rank-deficient sets rejected;
- pivot scans;
- pivot swaps;
- GF(2) row-XOR operations;
- accepted candidate weight;
- verifier-correct success by each cumulative checkpoint.

Paired topology/control comparisons must report both success counts and work distributions.

## Declared measurement

Primary sweep:

```text
n8/n9/n10 × 8 seeds × weights 1..6
```

If and only if an apparent topology/control separation appears specifically at `n10`, validate that signal on the already-declared

```text
n10 × 32 seeds × weights 1..6
```

extension with the same `8/32/128` budgets and no generator changes.

## Rejection gate

Reject the current topology-derived ensemble if topology syndromes are routinely solved at smaller public trial budgets or with substantially less GF(2) elimination work than matched controls at the same dimensions/rank/rate/error weight.

## Survival gate

If topology/control success and work curves overlap under all fixed budgets, record only survival of this bounded Prange/ISD gate. Do not infer asymptotic hardness, decoding hardness at cryptographic scale, post-quantum security, or suitability for a KEM.

No trapdoor primitive, KEM, one-wayness, post-quantum, IND-CPA/CCA, or production-security claim exists.
