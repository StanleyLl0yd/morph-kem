# G7 — planted signed 3-SAT phase-CSP negative control

Status: **rejected by A-034**.

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

This removes the direct per-clause parity shortcuts that rejected G4–G6. It does **not** create hardness: generic public SAT search remains fatal on the generated distribution.

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

## Fixed Python 3.12 baseline

For `g7-24` and master seed `76120450aabbccddeeff001122334455`:

```text
gadgets:                                24
total public tetrahedra:               144
clauses:                                96
variable degree histogram:             ((12,24),)
factor components / cycle rank:        1/169
local nontrivial affine implications:  0
local matching nodes / backtracks:     168/0
DPLL solutions / cap:                  16/16
DPLL cap hit:                           yes
DPLL nodes / decisions:                40/22
DPLL propagations / conflicts:         34/2
DPLL backtracks:                       2
exact verifier clause checks:          1536
accepted DPLL solutions:               16
accepted non-reference solutions:      16
first DPLL solution = reference:       no
reference witness accepted:            yes
```

Thus A-034 does not recover merely the planted assignment: the first capped batch already consists entirely of accepted equivalent non-reference witnesses.

The fixed baseline's independent MiniSat run reports SAT with 3 conflicts, 13 decisions, and 41 propagations. The decoded MiniSat model passes all 96 clauses in the repository's exact G7 verifier. Solver timing is not treated as a stable metric; the discrete search counts and verifier acceptance are the evidence.

## Multi-seed sweep

Python 3.12 covers `g7-12`, `g7-18`, and `g7-24` across eight deterministic seeds each.

All **24/24** instances yield at least one accepted public DPLL witness and at least one accepted non-reference witness. Across the measured sweep:

- local affine-implication count is always zero;
- local G3 matching recovery has zero backtracking;
- DPLL node counts range from 23 to 86;
- every `g7-18`/`g7-24` instance except one `g7-18` seed reaches the 16-solution cap, while the smaller `g7-12` instances expose between 3 and 16 solutions within the same cap;
- the largest measured DPLL work is still only 86 nodes on `g7-24`;
- non-reference accepted witnesses appear in every instance.

The fixed master-seed per-size controls are:

```text
g7-12: 48 clauses, 10 solutions, 37 nodes, 18 decisions,
       82 propagations, 9 conflicts, 10 backtracks, 9 non-reference

g7-18: 72 clauses, 16/16 solutions, 36 nodes, 20 decisions,
       14 propagations, 0 conflicts, 0 backtracks, 15 non-reference

g7-24: 96 clauses, 16/16 solutions, 40 nodes, 22 decisions,
       34 propagations, 2 conflicts, 2 backtracks, 16 non-reference
```

## Result

**G7 is rejected by A-034.**

Removing the cheap affine quotient was necessary but not sufficient. The deterministic planted 3-SAT distribution is still solver-friendly, and equivalent-witness multiplicity is itself fatal under the project attack model. Scaling the same generated family is not a repair.

This is a generated-distribution result, not a theorem that arbitrary 3-SAT or general HGES is easy. Worst-case NP-completeness of 3-SAT is not evidence for average-case cryptographic hardness of this planted distribution.

## Successor gate

G8 must change the generated relation rather than only increase clause/variable counts. Before any positive interpretation it should test whether topology contributes anything beyond an ordinary planted CSP. A successor must face at least:

- generic exact CSP/SAT on the public relation;
- equivalent-witness multiplicity and solution-space connectivity;
- unit/local-consistency and belief-propagation-style leakage;
- variable/role/sign distribution leakage;
- low-width/decomposition attacks;
- quotient/normalization/automorphism attacks;
- independent solver cross-checks.

No trapdoor primitive, KEM, one-wayness, average-case hardness, post-quantum, IND-CPA/CCA, or production-security claim exists.
