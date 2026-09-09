# 08 — Open questions

## Mathematical

- What exact class of complexes gives controllable trapdoor reductions without cheap canonical recovery?
- Should the construction use simplicial complexes or regular CW complexes?
- Can the hidden reduction certificate be represented compactly?
- Can equivalent witnesses be characterized cleanly?
- Can generated instances be sampled without obvious planted structure?
- What invariants remain after masking transformations?
- Can a family be constructed where a secret global Morse matching gives efficient reduction but arbitrary predecessor search has high branching?

## Complexity

- What is the right average-case assumption?
- Is there any credible worst-case-to-average-case connection?
- Which graph-width parameters make the problem easy?
- What is the best known exact/parameterized algorithm on the generated family?
- Does HMCR reduce to a known isomorphism, conjugacy, CSP, or tensor problem?
- What reverse-search complexity can be established for a non-invertible reduction system?
- Can meet-in-the-middle or bidirectional search be prevented by construction rather than by parameter inflation?

## Cryptographic

- Can forward evaluation be public without leaking inversion structure?
- What source of **asymmetry** remains after ruling out M0 local leakage and M1 reversible-path hiding?
- Is the primitive one-way on its generated distribution?
- Can a key-indistinguishability game be defined naturally?
- Is an FO-style transform applicable without circular assumptions?
- Can decapsulation validation be deterministic and non-malleable?
- How large are public keys and ciphertexts?

## Quantum

- Is there hidden algebraic structure exploitable by quantum algorithms?
- Can quantum walks exploit the reduction/predecessor graph?
- What is the correct quantum query model for public evaluation?
- Would a high-branching predecessor graph still admit a useful quantum-walk speedup?

## Engineering

- Can canonical complex operations be made fast enough for large attack sweeps?
- Which exact libraries should represent complexes once the standard-library model becomes a bottleneck?
- How will experiment manifests guarantee reproducibility?
- Which attack metrics should CI enforce as invariant research baselines?

## Lessons already established

- **M0:** independent public coordinate recipes are fatal.
- **M1:** replacing local recipes with globally supported but publicly invertible branch transforms is still fatal to path hiding because of generic meet-in-the-middle recovery.

The next model must add a qualitatively different source of inversion asymmetry.
