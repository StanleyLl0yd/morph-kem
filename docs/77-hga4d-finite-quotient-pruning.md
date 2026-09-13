# 77 — HGA4d finite free-group quotient pruning

## Status

**HGA4d is a falsification/calibration experiment in progress.** HGA4c removes planted-history non-geodesicity by selecting exact-distance endpoints, but its generator constructs a full BFS shell while public balanced MITM is already cheaper. HGA4d asks whether tiny public finite quotients expose an additional structural pruning shortcut.

HGA4d is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Instance distribution

Reuse the HGA4c exact-distance shell construction at public distances `D=4,6,8`. Target selection is unchanged in spirit: the endpoint is certified to have exact action distance `D`, so any shorter exact connector would be a calibration error.

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

## Measurements

For `S3` and `A5`, record:

- quotient reverse-table states/transitions;
- quotient-only shortest distance and its gap to exact `D`;
- exact states kept after pruning;
- exact transitions tested;
- candidate prunes and duplicate skips;
- number of distinct quotient states represented by retained exact states;
- maximum exact-state multiplicity per quotient state;
- retained exact states as a fraction of the full HGA4c generator ball;
- recovered connector length and exact endpoint verification;
- ordinary balanced MITM states/transitions;
- deterministic multi-seed curves.

## Gate

Reject the measured endpoint family as quotient-leaky if a tiny public finite quotient routinely removes a large fraction of the exact search while preserving exact recovery, especially if the effect strengthens with distance.

If quotient pruning is weak, record only that these two finite quotients do not add a strong shortcut on the measured toy endpoints. That would not be evidence of one-wayness: larger representations, stabilizers, canonical forms and ordinary generic search remain unresolved.

No security claim.
