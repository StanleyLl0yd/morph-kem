# 07 — Parameters

No security parameter set exists yet.

## Labels

Parameter sets must use only these maturity labels:

- **toy** — designed for exhaustive analysis and debugging;
- **experimental** — designed for empirical cryptanalysis;
- **candidate** — considered only after substantial evidence and review.

Do not label a parameter set "secure."

## M0 toy ladder

| Set | Seed bits | Purpose |
|---|---:|---|
| toy-8 | 8 | exhaustive enumeration, full round-trip tests, CI baseline |
| toy-12 | 12 | attack-harness scaling |
| toy-16 | 16 | canonicalization / solver experiments |
| toy-24 | 24 | structured-attack scaling only |
| toy-32 | 32 | upper M0 API bound; never intended for exhaustive CI |

M0 uses exactly five hidden vertices per coordinate before relabeling.

All M0 sets are broken by A-000 and have no security meaning.

## M1 experimental path ladder

| Set | Layers | Vertices | Minimum branch/relative support |
|---|---:|---:|---:|
| path-12 | 12 | 20 | 75% |
| path-16 | 16 | 24 | 75% |
| path-20 | 20 | 28 | 75% |
| path-24 | 24 | 32 | 75% |

M1 uses one common 2D simplicial scaffold and two global public vertex permutations per layer.

These are **experiment-size labels only**.

For balanced meet-in-the-middle recovery, the generic state counts are approximately:

| Set | Exhaustive paths | MITM forward states | MITM reverse states |
|---|---:|---:|---:|
| path-12 | 4096 | 64 | 64 |
| path-16 | 65536 | 256 | 256 |
| path-20 | 1048576 | 1024 | 1024 |
| path-24 | 16777216 | 4096 | 4096 |

Representation costs are omitted from this table.

A-008 therefore breaks the intended path-hiding idea independently of the configured 75% global support.

## Security interpretation

Neither M0 nor M1 defines a security level.

Increasing seed/path length is not evidence of security when a structural attack changes the effective exponent.

Parameter growth must follow attack measurements, not precede them.

## Future dimensions

A post-M1 generated distribution will likely need independent parameters for:

- complex dimension;
- base/core size;
- reduction/expansion depth;
- number of admissible local reductions;
- overlap between candidate reductions;
- decoy density;
- predecessor branching;
- separator/treewidth targets;
- public description size;
- trapdoor size;
- ciphertext size.

## Acceptance criterion for scaling

Do not scale merely until exhaustive search becomes expensive.

A model should be scaled only after the cheapest known structural attacks have been implemented and their growth is understood.
