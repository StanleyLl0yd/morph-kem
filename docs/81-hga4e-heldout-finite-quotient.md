# 81 — HGA4e held-out finite-quotient generalization control

## Status

**HGA4e is a falsification experiment in progress.** HGA4d showed that exact-distance Hurwitz endpoints are strongly filtered by a tiny public `A5` representation. HGA4e asks whether conditioning target selection against the known `S3/A5` leaks merely overfits those two maps.

HGA4e is not a trapdoor primitive, KEM, one-way function, post-quantum assumption, or production-security construction.

## Exact-distance generator

Reuse the HGA4c exact-distance shell construction at `D=4,6,8`. Enumerate the full exact ball and shell.

Target selection is allowed to inspect only two declared **training** representations, identical to HGA4d:

- `S3-train`;
- `A5-train`.

For every shell target and every training quotient:

1. build the quotient reverse-distance table through `D`;
2. inspect the already-generated exact ball;
3. count exact states whose quotient could still reach the quotient target within the remaining exact depth.

This count is a generation-time retention proxy. Select the target lexicographically to maximize:

1. the worse of the two training retentions;
2. total training retention;
3. target free-word length;
4. an independent deterministic hash tie-break.

Thus the generator intentionally chooses an endpoint that is difficult for the **known** quotient filters. It never consults held-out representations.

## Held-out HGA-A009 attacks

After the target is fixed, test independent public representations:

- `A4-heldout` from two fixed 3-cycles;
- `S4-heldout` from a transposition and 4-cycle;
- `A5-heldout` from a fixed 5-cycle and 3-cycle distinct from the training generator pair;
- product admissibility `A4 x S4`;
- product admissibility `S4 x A5-heldout`.

For every attack, the finite quotient is only a necessary admissibility filter. Exact free-group tuples remain the authoritative state. A candidate succeeds only if the recovered braid connector maps the original public source to the original public target exactly.

## Measurements

Record:

- exact generator ball/shell and generation transitions;
- selected training retention proxy and fraction;
- number of shell targets with lower retention than the selected target;
- actual post-selection training-quotient search work;
- ordinary balanced MITM states/transitions;
- held-out reverse-table sizes/distances;
- exact states/transitions after held-out pruning;
- retained fractions relative to generator ball and ordinary MITM state count;
- quotient collision multiplicity;
- recovered exact connector length and endpoint verification;
- deterministic `D=4/6/8 x 8` sweep.

## Gate

Reject HGA4e if held-out representations or their products recover strong exact-state pruning routinely despite training-quotient conditioning. This would indicate generic finite-representation leakage rather than one unlucky `A5` map.

If the held-out screen is weak, continue with stabilizers, Nielsen/Hurwitz normal forms, larger representations and independent generic exact solvers. Survival of these specific tests is not evidence of one-wayness.

Do not repair a failure by merely increasing `D` while retaining the same public action.

No security claim.
