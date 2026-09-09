# 07 — Parameters

No security parameter set exists yet.

## Labels

Parameter sets must use only these maturity labels:

- **toy** — designed for exhaustive analysis and debugging;
- **experimental** — designed for empirical cryptanalysis;
- **candidate** — considered only after substantial evidence and review.

Do not label a parameter set "secure."

## Implemented M0 toy ladder

| Set | Seed bits | M0 purpose |
|---|---:|---|
| toy-8 | 8 | exhaustive enumeration, full round-trip tests, CI baseline |
| toy-12 | 12 | attack-harness scaling |
| toy-16 | 16 | canonicalization / solver experiments |
| toy-24 | 24 | structured-attack scaling only |
| toy-32 | 32 | upper M0 API bound; never intended for exhaustive CI |

M0 uses exactly five hidden vertices per coordinate before relabeling. This is an implementation property of the toy harness, not a proposed cryptographic parameter formula.

## Security interpretation

None of the M0 sets has any security meaning. A-000 recovers their seeds directly from public recipes.

Increasing from toy-8 to toy-32 therefore does not increase security in a meaningful sense; it only changes experiment size.

## Future dimensions

A post-M0 generated distribution will need independent parameters for at least:

- complex dimension;
- base/core size;
- transformation depth;
- decoy density;
- overlap between hidden coordinates;
- separator/treewidth targets;
- public description size;
- trapdoor size;
- ciphertext size.

## Acceptance criterion for scaling

Do not increase parameters simply because brute force becomes expensive. Scaling is justified only after measuring whether structural attacks grow at the intended rate and after eliminating trivial local distinguishers.
