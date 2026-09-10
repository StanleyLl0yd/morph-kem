# G8 — public phase-extraction topology-to-CSP collapse audit

Status: **calibration in progress**.

G8 tests a cross-cutting failure mode suggested by G3–G7. It does not introduce a new cryptographic predicate. Instead it asks whether, after public enumeration of each local gadget's accepted decompositions, the remaining HGES relation is exactly an ordinary finite-domain CSP.

## A-035 public reduction

For G4–G7, A-035 performs two public stages:

```text
PhaseExtract(topological public instance) -> finite-domain CSP
Lift(domain assignment) -> topological witness
```

Every local `g3-3` gadget is attacked by the existing public matching enumerator. Its two accepted decompositions are canonically ordered and become domain values `0` and `1`.

The compiler then discards local simplicial data from the solver representation. `CompiledPhaseCSP` contains only:

- a family label;
- integer domain sizes;
- relation scopes over variable indices;
- explicit allowed tuples of domain indices.

Tetrahedra, faces, vertices, local simplicial labels, and planted/reference roles do not appear in the compiled solver object or its deterministic JSON serialization. A separate public lift table retains the already-enumerated local witnesses only so a solved domain assignment can later be submitted to the original HGES verifier.

## Compiled relations

- **G4:** each public parity coupling becomes a binary table containing the two `(a,b)` pairs satisfying `a XOR b = parity`.
- **G5/G6:** each signed exact-one clause becomes a ternary relation containing its three accepted local tuples.
- **G7:** each signed 3-OR clause becomes a ternary relation containing its seven accepted local tuples.

No family-specific topology is needed after compilation.

## Generic solver

The G8 solver sees only `CompiledPhaseCSP`. It applies generalized arc consistency by deleting domain values unsupported by any compatible allowed tuple, then branches by minimum remaining domain size with a deterministic high-incidence tie break. It enumerates solutions up to an explicit cap and records nodes, decisions, value prunes, conflicts, and backtracks.

Every recovered assignment is lifted through the public domain table and checked by the original family verifier. Reference phases are used only after public acceptance to classify non-reference witnesses.

## Exact semantic-equivalence gate

The important G8 condition is stronger than recovering the planted witness. For the smallest public instances, A-035 exhaustively checks every phase assignment and requires

```text
CompiledPhaseCSP accepts assignment
    iff
original HGES verifier accepts Lift(assignment).
```

The fixed exhaustive spaces are:

- G4 `g4-4`: 16 assignments;
- G5 `g5-12`: 4096 assignments;
- G6 `g6-12`: 4096 assignments;
- G7 `g7-12`: 4096 assignments.

Any mismatch falsifies the claimed reduction.

## Rejection gate

If the exhaustive semantic audit has zero mismatches and the generic topology-free CSP solver routinely yields assignments that mechanically lift to accepted original witnesses, record A-035 as a structural break of the G4–G7 design line.

The interpretation would be narrow but important: adding a different CSP predicate on top of the same independently enumerable two-phase topological gadgets is not additional topological hardness. It merely selects another ordinary CSP after cheap public preprocessing.

A successor must therefore break the premise of independent cheap `PhaseExtract`, not merely scale or replace the compiled predicate.

No trapdoor primitive, KEM, one-wayness, average-case hardness, post-quantum, IND-CPA/CCA, or production-security claim exists.
