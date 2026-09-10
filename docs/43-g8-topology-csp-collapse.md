# G8 — public phase-extraction topology-to-CSP collapse audit

Status: **rejected by A-035 / structural G4–G7 topology-to-CSP collapse confirmed**.

G8 is a cross-cutting falsification experiment. It does not introduce a new cryptographic predicate. It asks whether, after public enumeration of each local gadget's accepted decompositions, the remaining HGES relation is exactly an ordinary finite-domain CSP.

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

Tetrahedra, faces, vertices, local simplicial labels, and planted/reference roles do not appear in the compiled solver object or deterministic JSON serialization. A separate public lift table retains the already-enumerated local witnesses only so a solved domain assignment can later be submitted to the original HGES verifier.

## Compiled relations

- **G4:** each public parity coupling becomes a binary table containing the two `(a,b)` pairs satisfying `a XOR b = parity`.
- **G5/G6:** each signed exact-one clause becomes a ternary relation containing its three accepted local tuples.
- **G7:** each signed 3-OR clause becomes a ternary relation containing its seven accepted local tuples.

No family-specific topology is needed by the solver after compilation.

## Generic solver

The G8 solver sees only `CompiledPhaseCSP`. It applies generalized arc consistency by deleting domain values unsupported by any compatible allowed tuple, then branches by minimum remaining domain size with a deterministic high-incidence tie break. It enumerates solutions up to an explicit cap and records nodes, decisions, value prunes, conflicts, and backtracks.

Every recovered assignment is lifted through the public domain table and checked by the original family verifier. Reference phases are used only after public acceptance to classify non-reference witnesses.

## Fixed Python 3.12 large-family baseline

```text
family  vars/constraints  relation table      tets  extract n/b  JSON bytes  solutions/cap  solver n/d  prune/conf/back  lifted accepted  nonref
G4      12/18             arity2, allowed2     72    84/0         798         2/16           3/1         22/0/0          2                1
G5      24/48             arity3, allowed3    144   168/0        2772         1/16           3/1         31/1/1          1                0
G6      24/48             arity3, allowed3    144   168/0        2772         1/16           3/1         45/1/1          1                0
G7      24/96             arity3, allowed7    144   168/0        8520        16/16          38/22        39/0/0         16               16
```

For all four compiled representations the topology-token check is false: the serialized solver object contains no tetrahedron, face, vertex, simplicial, or witness-group representation. The separate lift table is not consulted by the generic solver.

## Exact semantic-equivalence result

The important G8 condition is stronger than recovering a planted witness. A-035 exhaustively checks every phase assignment in the smallest fixed instances and compares the compiled relation against the **original exact HGES verifier after Lift**:

```text
G4 g4-4:   checked 16    compiled accepts 2   original accepts 2   mismatches 0
G5 g5-12:  checked 4096  compiled accepts 1   original accepts 1   mismatches 0
G6 g6-12:  checked 4096  compiled accepts 1   original accepts 1   mismatches 0
G7 g7-12:  checked 4096  compiled accepts 10  original accepts 10  mismatches 0
```

Total: **12,304/12,304 assignments checked with zero semantic mismatches**.

Thus, for these measured families and domains,

```text
CompiledPhaseCSP accepts assignment
    iff
original HGES verifier accepts Lift(assignment).
```

The equivalence covers the entire measured accepted relation, not only planted/reference witnesses.

## Multi-seed regression

Python 3.12 tests the largest fixed representative of every family over four independently derived deterministic seeds: 16 compiled instances total.

All **16/16** generic topology-free solves produce public assignments that mechanically lift to accepted original HGES witnesses. Local phase extraction has zero backtracking throughout.

Measured solver work:

- G4: always 3 nodes / 1 decision, two accepted solutions, one non-reference;
- G5: always 3 nodes / 1 decision, one accepted solution;
- G6: always 3 nodes / 1 decision, one accepted solution;
- G7: 40–100 nodes, 23–53 decisions, all four runs hit the 16-solution cap; each has 15 or 16 accepted non-reference witnesses among the first 16.

The largest observed G7 generic-CSP run uses 100 nodes, 53 decisions, 316 value prunes, 31 conflicts and 52 backtracks.

## Result

**A-035 confirms a structural topology-to-CSP collapse for the G4–G7 design line.**

Once each local topological gadget exposes a small independently enumerable and canonically ordered witness domain, the global verifier factors exactly through an ordinary finite-domain CSP. The topological layer is cheap public preprocessing plus a mechanical post-solve lift; it contributes no additional inversion barrier in these measured constructions.

This does **not** prove that arbitrary HGES, topology, CSP, or SAT is easy. It rejects the specific architectural pattern used by G4–G7. Choosing a different or harder worst-case CSP predicate on top of the same independently enumerable local domains is not a topological cryptographic advance.

Scaling variables, clauses, or relation density is therefore not a repair.

## Successor gate

A G9 successor must break at least one premise of A-035. In particular, it must avoid exposing an efficiently enumerable, independently factored local witness domain that can be canonicalized before global solving.

The next useful negative control should entangle local topology across overlapping boundaries so that `PhaseExtract` itself becomes the object under attack. It must immediately face multiscale decomposition, separator/link/motif, normalization/automorphism, overlapping exact-cover/CSP/SAT, low-width, equivalent-witness, generated-role leakage, and public contraction/quotient attacks.

No trapdoor primitive, KEM, one-wayness, average-case hardness, post-quantum, IND-CPA/CCA, or production-security claim exists.
