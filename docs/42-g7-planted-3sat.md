# G7 — planted signed 3-SAT phase-CSP negative control

Status: **calibration in progress**.

G7 is the first HGES phase-coupling calibration in this line whose local clause predicate has no non-trivial affine GF(2) implication. It is a falsification experiment, not a security claim.

## Construction

Each public variable is an independently relabelled `g3-3` gadget. Public canonical ordering of its two accepted perfect-match decompositions defines a phase bit `0` or `1`.

For `g in {12,18,24}`, G7 publishes `4g` signed 3-OR clauses on the fixed circulant scopes

```text
(i, i+1, i+3)
(i, i+2, i+5)
(i, i+4, i+9)
(i, i+5, i+11)
```

modulo `g`, with each scope canonicalized. Clause signs are generated deterministically from a hidden reference assignment so every public clause is satisfied. The hidden assignment and selected local decompositions are reference evidence only.

Each variable has public degree 12 and the factor graph is connected. The toy sets are `g7-12`, `g7-18`, and `g7-24`; these are not security parameters.

## Quotient check

Unsigned 3-OR accepts seven of the eight Boolean triples. Exhaustive enumeration of all non-zero affine masks over GF(2) finds **zero** non-trivial affine equations satisfied by all accepted tuples. Literal negation only translates the relation, so signed clauses inherit the same property.

This removes the direct per-clause parity shortcuts that rejected G4–G6. It does not imply hardness.

## A-034 — public DPLL / equivalent-witness recovery

The public attack:

1. reconstructs and canonically orders the two accepted G3 matchings for every gadget;
2. performs unit propagation on the public signed 3-SAT clauses;
3. branches deterministically on the unassigned variable with maximum incidence in currently unresolved clauses;
4. enumerates solutions up to an explicit cap;
5. lifts recovered phase assignments back to local G3 matching witnesses;
6. submits every candidate to the exact public G7 verifier;
7. counts non-reference accepted witnesses only after public success.

The dedicated Python 3.12 workflow additionally emits a standard DIMACS CNF, invokes MiniSat independently, parses its model, lifts it to local matching witnesses, and rechecks that model with the repository verifier.

## Rejection gate

If public DPLL routinely finds accepted witnesses with small search, or if equivalent non-reference witnesses are readily available, reject G7. MiniSat is an independent cross-check, not a hardness oracle.

Worst-case NP-completeness of 3-SAT is not evidence for average-case hardness of this deterministic planted distribution.

## Measurements to record

- gadget / tetrahedron / clause counts;
- variable-degree histogram and factor components/cycle rank;
- exact local affine-implication count;
- local G3 matching nodes/backtracks;
- DPLL nodes, decisions, propagations, conflicts/backtracks;
- solution count / cap / cap-hit;
- exact verifier work and accepted witnesses;
- accepted non-reference witnesses;
- deterministic all-size × multi-seed sweep;
- independent MiniSat model acceptance on the fixed baseline.

No trapdoor primitive, KEM, one-wayness, average-case hardness, post-quantum, IND-CPA/CCA, or production-security claim exists.
