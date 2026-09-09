# 07 — Parameters

No security parameter set exists.

All current names describe experiment sizes only.

## Labels

Allowed maturity labels:

- **toy** — exhaustive analysis/debugging;
- **experimental** — empirical cryptanalysis;
- **candidate** — only after substantial evidence and review.

Do not label a parameter set "secure."

## M0 toy ladder

| Set | Seed bits | Purpose |
|---|---:|---|
| toy-8 | 8 | exhaustive CI baseline |
| toy-12 | 12 | attack-harness scaling |
| toy-16 | 16 | solver experiments |
| toy-24 | 24 | structured-attack scaling |
| toy-32 | 32 | upper M0 API bound |

All M0 sets are broken by A-000.

## M1 path ladder

| Set | Layers | Vertices | Minimum branch/relative support |
|---|---:|---:|---:|
| path-12 | 12 | 20 | 75% |
| path-16 | 16 | 24 | 75% |
| path-20 | 20 | 28 | 75% |
| path-24 | 24 | 32 | 75% |

Balanced A-008 meet-in-the-middle state counts:

| Set | Exhaustive paths | Forward half | Reverse half |
|---|---:|---:|---:|
| path-12 | 4096 | 64 | 64 |
| path-16 | 65536 | 256 | 256 |
| path-20 | 1048576 | 1024 | 1024 |
| path-24 | 16777216 | 4096 | 4096 |

All M1 sets are structurally subject to A-008.

## M2 collapse-maze ladder

| Set | Vertices | Planted expansions | Hidden core |
|---|---:|---:|---|
| maze-4 | 10 | 4 | 3-regular spanning graph |
| maze-6 | 12 | 6 | 3-regular spanning graph |
| maze-8 | 12 | 8 | 3-regular spanning graph |
| maze-10 | 16 | 10 | 3-regular spanning graph |
| maze-12 | 16 | 12 | 3-regular spanning graph |
| maze-16 | 20 | 16 | 3-regular spanning graph |

Every M2 expansion adds one missing edge and one filled triangle. A final secret vertex permutation hides the generator's original labels, and only a digest of the hidden core is public.

This does **not** hide the generator family.

### A-014 fixed-seed results

| Set | Recovery nodes | Digest-tested candidates | Forced zero-triangle edges |
|---|---:|---:|---:|
| maze-4 | 13 | 1 | 7 |
| maze-6 | 59 | 4 | 6 |
| maze-8 | 520 | 14 | 2 |
| maze-10 | 51 | 1 | 5 |
| maze-12 | 441 | 5 | 2 |

The values are reproducible observations for the repository's fixed experiment seed. They are not complexity estimates.

All M2 sets share the same fatal structural invariant: the hidden core is 3-regular and non-core edges necessarily have positive filled-triangle incidence.

## Security interpretation

Parameter inflation is never a response to a structural break.

A model is allowed to scale only after:

1. its generated distribution is precisely specified;
2. obvious generator invariants have dedicated attacks;
3. equivalent-witness semantics are defined;
4. the cheapest known classical attacks have measured growth;
5. the quantum attack model has at least been formulated.

M0, M1, and M2 all fail before this gate.

## Future dimensions

A successor to M2 should avoid a single low-complexity core family and should measure at least:

- ambient complex dimension;
- hidden core distribution entropy;
- dimension-dependent incidence histograms;
- reduction/expansion depth;
- number of admissible local reductions;
- overlap between candidate reductions;
- predecessor branching;
- automorphism/canonicalization profile;
- separator/treewidth profile;
- public description size;
- trapdoor size;
- ciphertext size.

## Acceptance criterion for scaling

Do not scale until the generated distribution survives its own cheapest structural-recovery attacks.

"Brute force is expensive" is not a parameter-selection argument.
