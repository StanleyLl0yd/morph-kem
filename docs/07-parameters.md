# 07 — Parameters

No security parameter set exists yet.

## Labels

Parameter sets must use only these maturity labels:

- **toy** — designed for exhaustive analysis and debugging;
- **experimental** — designed for empirical cryptanalysis;
- **candidate** — considered only after substantial evidence and review.

Do not label a parameter set "secure."

## Initial toy ladder

The first implementation should intentionally remain tiny:

| Set | Seed bits | Purpose |
|---|---:|---|
| toy-8 | 8 | exhaustive enumeration and correctness |
| toy-12 | 12 | attack harness debugging |
| toy-16 | 16 | canonicalization / SAT / MILP comparison |
| toy-24 | 24 | scaling experiments |
| toy-32 | 32 | upper end of early exhaustive/structured testing |

Other dimensions — complex dimension, gadget size, decoy count, treewidth targets, transformation depth, and encoding size — remain undefined.

## Acceptance criteria for scaling

Do not increase parameters simply because brute force becomes expensive. Scaling is justified only after measuring whether structural attacks grow at the intended rate.
