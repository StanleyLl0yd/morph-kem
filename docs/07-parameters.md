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

All M2 sets share the fatal A-014 generator invariant.

## M3 equivalent-witness ladder

| Set | Vertices | Extra graph edges | 2D expansions | Public critical target |
|---|---:|---:|---:|---|
| morse-6 | 12 | 4 | 6 | (1,5,0) |
| morse-8 | 14 | 5 | 8 | (1,6,0) |
| morse-10 | 16 | 6 | 10 | (1,7,0) |
| morse-12 | 18 | 7 | 12 | (1,8,0) |
| morse-16 | 22 | 9 | 16 | (1,10,0) |

The hidden M3 core is a connected variable-degree graph and the public relation contains no core digest.

This removes A-014's exact 3-regular reconstruction target but exposes the more fundamental A-016 equivalent-witness attack.

### A-016 fixed-seed results

| Set | Lex accepted | Reverse accepted | Random accepted | Unique graph residuals |
|---|---:|---:|---:|---:|
| morse-6 | yes | yes | 32/32 | 32 |
| morse-8 | yes | yes | 32/32 | 32 |
| morse-10 | yes | yes | 32/32 | 32 |
| morse-12 | yes | yes | 32/32 | 32 |
| morse-16 | yes | yes | 32/32 | 32 |

### A-017 fixed-seed results

| Set | Target hits | Best total critical cells |
|---|---:|---:|
| morse-6 | 8/8 | 6 |
| morse-8 | 5/8 | 7 |
| morse-10 | 3/8 | 8 |
| morse-12 | 3/8 | 9 |
| morse-16 | 4/8 | 11 |

The best critical-cell total equals the public target total in every tested set.

These are reproducible fixed-seed observations, not asymptotic complexity estimates.

## Security interpretation

Parameter inflation is never a response to a structural break.

A model may scale only after its distribution is precise, equivalent-witness semantics are explicit, easy homotopy reductions are excluded, cheapest classical attacks have measured growth, and the quantum attack model is at least formulated.

M0, M1, M2, and M3 all fail before this gate.

## Future dimensions

A successor to M3 should measure:

- ambient dimension;
- target critical vector;
- natural versus planted distribution distinguishability;
- local incidence histograms by cell role;
- Hasse-graph degree distribution;
- matching overlap and dependency depth;
- automorphism/canonicalization profile;
- separator/treewidth profile;
- greedy-matching success;
- SAT/CSP attack cost;
- public description size;
- witness/trapdoor size.

## Acceptance criterion for scaling

Do not scale until the generated distribution survives its cheapest structural and constructive equivalent-witness attacks.

"Brute force is expensive" is not a parameter-selection argument.
