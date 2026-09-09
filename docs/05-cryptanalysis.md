# 05 — Cryptanalysis ledger

This file is intentionally a ledger of attacks, including attacks that succeed.

## Current attack surface

| ID | Attack family | Current assessment | Status |
|---|---|---|---|
| A-000 | Direct public recipe recovery against M0 | **Fatal to M0** | Implemented |
| A-001 | Greedy / heuristic Morse reduction | Persistent high risk | Implemented in M2/M3 forms |
| A-002 | Joint recovery from public transformations | Critical risk | Not implemented generically |
| A-003 | Canonical labeling / isomorphism recovery | High risk | M1 weakness documented |
| A-004 | SAT reconstruction | High risk | Not implemented |
| A-005 | MILP reconstruction | High risk | Not implemented |
| A-006 | Treewidth / separator methods | High risk | Not implemented |
| A-007 | Spectral / invariant distinguisher | High risk | Not implemented |
| A-008 | Generic meet-in-the-middle path recovery | **Fatal to M1** | Implemented |
| A-009 | Learned gadget recognition | Unknown/high | Not implemented |
| A-010 | Invalid-ciphertext / oracle leakage | Critical for a future KEM | Initial malformed-input tests only |
| A-011 | Generic quantum search | Expected baseline | Analytical only |
| A-012 | Quantum walk / structure exploitation | Unknown | Not analyzed |
| A-013 | Bounded public collapse DFS against M2 | Effective on small M2 | Implemented |
| A-014 | 3-regular hidden-core reconstruction | **Fatal to M2** | Implemented |
| A-015 | Alternative irreducible residual ambiguity | Structural result | Observed in M2 |
| A-016 | Free-collapse + spanning-tree equivalent witness | **Fatal to M3** | Implemented |
| A-017 | Generic greedy acyclic Hasse matching | Strong empirical attack on M3 | Implemented |

## A-000 — direct public recipe recovery

M0 publishes two candidate triangles per coordinate and the ciphertext contains exactly one.

**Result:** complete break of M0.

**Lesson:** selected hidden coordinates must not remain locally recognizable.

## A-008 — generic meet-in-the-middle path recovery

M1 replaces local markers with global vertex permutations, but every layer still exposes two efficiently invertible public choices.

For a balanced split of an ell-layer path:

~~~text
forward states  ~ 2^(ell/2)
reverse states  ~ 2^(ell/2)
memory          ~ 2^(ell/2)
~~~

**Result:** M1 rejected.

**Lesson:** global support is not inversion asymmetry.

## A-013 — bounded collapse DFS

M2 creates genuine non-invertible collapse branching.

For deterministic maze-6:

~~~text
target simplices: 42
initial free collapse pairs: 18

bounded DFS:
  planted core found: yes
  nodes: 1095
  visited states: 1150
  maximum frontier: 58
~~~

A-014 is the stronger break.

## A-014 — structural 3-regular core recovery

Every M2 non-core edge is introduced with a filled triangle, while the planted hidden core is always a spanning 3-regular graph.

Therefore a target edge with triangle incidence zero is a forced hidden-core edge.

The attack completes those forced edges to a 3-regular spanning subgraph and checks candidates against the public planted-core digest.

| Set | Nodes | Digest-tested candidates | Forced edges |
|---|---:|---:|---:|
| maze-4 | 13 | 1 | 7 |
| maze-6 | 59 | 4 | 6 |
| maze-8 | 520 | 14 | 2 |
| maze-10 | 51 | 1 | 5 |
| maze-12 | 441 | 5 | 2 |

**Result:** M2 rejected.

**Lesson:** the generator can leak a much easier reconstruction problem than the nominal reduction problem.

## A-015 — alternative irreducible residual ambiguity

For deterministic maze-6, lexicographic, reverse, and sixteen deterministic random greedy collapse paths all reach a 30-simplex residual, but none reaches the planted core. The sixteen random trials produce sixteen different residuals.

**Lesson:** a planted residual is not automatically a mathematically privileged witness.

## A-016 — free-collapse plus spanning-tree equivalent witness

M3 fixes the verifier problem: **any** acyclic Morse matching with the public target critical vector is accepted.

The generated family is a variable-degree connected graph plus elementary 2D expansions.

The attack:

1. greedily collapses free edge/triangle pairs until a graph residual is reached;
2. constructs a public spanning tree of that residual;
3. matches every non-root tree vertex with its tree edge;
4. combines graph pairs with the chosen collapse pairs.

No planted core, planted path, or secret relabeling is recovered.

For every tested M3 parameter set:

- lex collapse produces an accepted witness;
- reverse collapse produces an accepted witness;
- all 32/32 deterministic random collapse trials produce accepted witnesses;
- all 32 random trials reach different graph residuals.

**Result:** M3 rejected.

**Lesson:** equivalent-witness semantics are necessary, but a graph-expanded generated family makes the honest equivalent-witness relation constructively easy.

## A-017 — generic greedy acyclic Hasse matching

A-017 randomizes Hasse incidences and greedily adds any unused pair that preserves acyclicity.

Fixed-seed target-hit rates:

~~~text
morse-6:  8/8
morse-8:  5/8
morse-10: 3/8
morse-12: 3/8
morse-16: 4/8
~~~

The best critical count equals the public target count in every tested set.

This is secondary evidence that M3 instances contain many easy high-quality Morse matchings.

## Persistent fatal-flaw classes

### Shared hidden structure

Repeated public objects derived from one hidden representation may reveal an equivalent coordinate system or matching.

### Planted-instance leakage

The generator can expose an easier recognition or reconstruction problem than the nominal hard problem.

### Decomposition

Local gadgets or low-width structure may split the global problem into small independent constraints.

### Equivalent witnesses

The attacker must be credited for any witness satisfying the public relation. M3 formalizes this rule.

### Easy homotopy class

If the generated family publicly reduces to a class with an elementary optimal matching construction, the target Morse relation may be easy even when the planted history is hidden. A-016 is the concrete graph-expanded example.

## Reporting template

For every attack record:

- attack ID;
- commit / implementation version;
- parameter set;
- sample count;
- random seeds;
- hardware/software environment;
- success probability;
- median / tail runtime;
- memory use;
- recovered information;
- interpretation;
- whether the result falsifies a claim or parameter set.
