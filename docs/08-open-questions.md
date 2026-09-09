# 08 — Open questions

## Mathematical

- What class of complexes gives controllable trapdoor reductions without a cheaply recognizable planted core?
- Should the construction move from simplicial complexes to regular CW complexes?
- Can a useful hidden reduction certificate be compact while equivalent certificates remain difficult to find?
- Can generated instances be sampled from a distribution close to a natural public ensemble rather than "easy object + visible decoration"?
- Can core and non-core cells be made locally incidence-indistinguishable?
- What invariants necessarily survive elementary expansion/collapse and therefore cannot carry secret information?
- Is there a family where a planted global Morse matching is useful but no simpler graph-factor, matching, canonicalization, or CSP reconstruction problem is exposed?

## Complexity

- What is the right average-case problem after M0/M1/M2?
- Is any credible worst-case-to-average-case connection available?
- Which graph-width or Hasse-diagram width parameters make matching/reduction easy?
- Can hidden-Morse recovery be reformulated as matching, f-factor, CSP, SAT, tensor, or isomorphism on the generated family?
- What is the best attack when many terminal residuals are equivalent or same-sized?
- Can reverse/predecessor branching be made large without introducing a simpler planted-substructure problem?

## Generator design after A-014

M2 demonstrates that hiding labels is insufficient when the generator preserves a simple semantic invariant.

A successor must answer:

1. What public property characterizes the hidden core family?
2. Can an attacker search that family directly without following collapse paths?
3. Which cells are provably core/non-core from local incidence?
4. Does the public verifier reduce core recovery to a standard constrained-subgraph problem?
5. Are generated instances statistically distinguishable from suitable control complexes?

These questions must be attacked **before** increasing dimension or parameter size.

## Cryptographic

- What is the actual one-way relation: recover the original trapdoor, any valid reduction certificate, a canonical residual, or only a derived secret?
- How are equivalent witnesses handled in the security game?
- Can public verification avoid privileging an arbitrary planted residual without opening a direct reconstruction oracle?
- Can forward evaluation be public without revealing the decomposition used for inversion?
- Is there a natural key-indistinguishability game at all for this mathematical direction?
- If a KEM wrapper is eventually attempted, can decapsulation validation be deterministic, non-malleable, and oracle-safe?

## Quantum

- Can quantum walks exploit the free-collapse or predecessor graph?
- Can amplitude amplification accelerate constrained core/certificate recovery?
- Does a reformulation expose hidden-shift/subgroup structure?
- What is the correct quantum query model for public evaluation and public verification?

## Engineering

- The standard-library simplicial representation is intentionally simple, not optimized. When does it become the attack bottleneck?
- Which canonical-labeling and graph/CSP libraries should be introduced for research attacks?
- How should experiment manifests record generator seed, attack seed, node budget, interpreter, and hardware?
- Which attack metrics should become CI regression baselines?

## Lessons established

- **M0:** independent public coordinate recipes are fatal.
- **M1:** global but publicly invertible transformations are still vulnerable to generic bidirectional search.
- **M2:** genuine non-invertible branching is not enough when the planted generator exposes a simpler structural reconstruction problem.
- **M2/A-015:** many same-sized irreducible residuals exist, so "the planted core" is not automatically a mathematically privileged witness.

The next model must improve the **generated distribution**, not merely make the collapse maze larger.
