# 08 — Open questions

## Mathematical

- What genuinely 2-dimensional family admits a compact planted Morse witness without making equivalent witnesses easy?
- Should the project continue with simplicial complexes or move to regular CW complexes?
- Can a generated distribution avoid being "easy lower-dimensional object + removable decoration"?
- Can planted and non-planted Hasse incidences be locally statistically indistinguishable?
- Can useful critical vectors live in a natural public ensemble rather than be encoded through a low-complexity core?
- Is there a family where finding any matching at the target vector remains difficult on average?

## Complexity

- What is the right average-case equivalent-witness problem after M3?
- Can it reduce to matching, matroid, graph-factor, CSP, SAT, tensor, or isomorphism on the generated family?
- Which Hasse-diagram width parameters make acyclic matching easy?
- How strong are greedy/local-search approximations on candidate distributions?
- Can a natural 2-complex ensemble be conditioned on a planted good matching without making the planting recognizable?
- What attack cost remains after quotienting out all equivalent witnesses?

## Generator design after M3

A successor must answer before scaling:

1. Can the target be solved by collapsing into an easy lower-dimensional class?
2. Does a standard spanning-tree, forest, or graph-matching construction meet the target?
3. Is the target critical vector implied by an easily exposed homotopy type?
4. Does a greedy acyclic Hasse matcher frequently hit the target?
5. Can SAT/CSP express the witness relation compactly enough to solve experimental sizes immediately?
6. Does the planted generator create role-dependent incidence statistics?

## Cryptographic

- What secret value would a future public-key primitive actually protect if many valid Morse witnesses exist?
- Can a derived secret be invariant across equivalent witnesses without becoming publicly computable?
- Can forward evaluation be public without publishing an easy witness-construction recipe?
- Is there a natural one-way relation rather than a verifier-selected planted object?
- Can future decapsulation avoid arbitrary witness privilege and oracle leakage?

## Quantum

- Can quantum walks exploit the Hasse matching state graph?
- Can amplitude amplification materially accelerate witness construction?
- Does a future formulation expose hidden-shift/subgroup structure?
- What is the right quantum query model for a public equivalent-witness relation?

## Engineering

- When does the simple standard-library representation become the attack bottleneck?
- Which SAT/CSP and canonical-labeling libraries should be introduced first?
- How should experiment manifests record generator seed, attack seed, solver version, node budget, interpreter, and hardware?
- Which fixed attack baselines should become CI regressions?

## Lessons established

- **M0:** independent public coordinate recipes are fatal.
- **M1:** global but publicly invertible transformations remain vulnerable to bidirectional search.
- **M2:** non-invertible branching is irrelevant if the generator exposes a simpler planted-substructure recovery problem.
- **M2/A-015:** a planted residual is not automatically a privileged mathematical witness.
- **M3:** equivalent-witness semantics are mandatory.
- **M3/A-016:** 2D expansions of a graph remain easy when public collapses recover any graph residual and a spanning tree completes the target matching.
- **M3/A-017:** generic greedy acyclic Hasse matching already reaches the target on a substantial fraction of tested instances.

The next model must be genuinely higher-dimensional in its useful witness structure, not just in its surface representation.
