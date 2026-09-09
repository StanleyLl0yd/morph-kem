# 05 — Cryptanalysis ledger

This file is intentionally a ledger of attacks, including attacks that succeed.

## Current attack surface

| ID | Attack family | Current assessment | Status |
|---|---|---|---|
| A-000 | Direct public recipe recovery against M0 | **Fatal by design** | Implemented |
| A-001 | Greedy / heuristic Morse reduction | High risk | Implemented in basic form for M2 |
| A-002 | Joint recovery from public transformations | Critical risk | Not implemented generically |
| A-003 | Canonical labeling / isomorphism recovery | High risk | M1 weakness documented; dedicated attack pending |
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
| A-015 | Alternative irreducible residual ambiguity | Structural concern | Observed in M2 greedy surveys |

## A-000 — direct public recipe recovery

M0 publishes two candidate triangles per coordinate and the ciphertext contains exactly one. The implementation direct_public_recover therefore reads every seed bit directly.

**Result:** complete break of M0 by design.

**Lesson:** selected hidden coordinates must not remain locally recognizable in public output.

## A-008 — generic meet-in-the-middle path recovery

M1 replaces local markers with global vertex permutations, but every layer still exposes two efficiently invertible public choices.

For ell layers and a balanced split:

~~~text
forward states  ~ 2^(ell/2)
reverse states  ~ 2^(ell/2)
memory          ~ 2^(ell/2)
~~~

The implementation mitm_path_recover recovers tested path-16 and path-20 targets without secret information.

M1 also preserves the complete simplicial isomorphism class at every step because a branch is only a vertex relabeling.

**Result:** M1 is unsuitable as a security candidate.

**Lesson:** global support is not inversion asymmetry.

## A-013 — bounded collapse DFS

### Target

M2 collapse maze.

### Observation

M2 finally uses non-invertible elementary collapses. At the deterministic maze-6 target there are 18 free collapse pairs initially. Blind greedy choices do not recover the planted core.

The public core digest nevertheless gives an exact success oracle. A depth-first attacker can enumerate public free-collapse choices, deduplicate canonical intermediate states, and reject states that already contain fewer simplices than the known 3-regular core size.

### CI baseline

For maze-6:

~~~text
target simplices:            42
hidden core simplices:       30
planted expansion steps:      6
initial free collapse pairs: 18

bounded DFS:
  core found:          yes
  nodes:               1095
  visited states:      1150
  maximum frontier:      58
~~~

**Result:** the maze does create genuine branching, but the small baseline is still cheaply searchable.

This alone does not establish an asymptotic break; A-014 is substantially stronger.

## A-014 — structural 3-regular core recovery

### Target

M2 generated distribution.

### Generator leakage

M2's hidden core is always a spanning 3-regular graph.

Every expansion adds exactly:

~~~text
missing edge sigma
+
filled triangle tau
~~~

Therefore every non-core edge belongs to at least one filled triangle in the final target.

This gives a public implication:

~~~text
target edge with triangle-incidence 0
        =>
edge is certainly in the hidden core
~~~

These forced core edges combine with the public generator invariant:

~~~text
every vertex has hidden-core degree exactly 3
~~~

The attack enumerates only 3-regular spanning subgraphs of the public 1-skeleton consistent with the forced edges and checks candidates against the public core digest.

### Deterministic CI baseline

For maze-6:

~~~text
forced core edges:       6
optional target edges:  18
search nodes:           59
3-regular candidates:    4
hidden core recovered: yes
~~~

### Scaling sweep

Fixed master seed, node cap 2,000,000:

| Set | Found | Search nodes | Digest-tested 3-regular candidates | Forced edges | Optional edges |
|---|---:|---:|---:|---:|---:|
| maze-4 | yes | 13 | 1 | 7 | 12 |
| maze-6 | yes | 59 | 4 | 6 | 18 |
| maze-8 | yes | 520 | 14 | 2 | 24 |
| maze-10 | yes | 51 | 1 | 5 | 29 |
| maze-12 | yes | 441 | 5 | 2 | 34 |

These values are empirical results for one deterministic experiment seed, not asymptotic complexity claims.

### Interpretation

**M2 is structurally broken.**

The attack does not search the Morse/collapse maze at all. It recovers the planted target object from a much simpler invariant left by the generator.

This is exactly the planted-instance failure mode the project was created to detect.

Increasing expansion count or vertex count is not an acceptable repair for this model.

## A-015 — alternative irreducible residuals

For deterministic maze-6:

~~~text
lex greedy:
  6 collapses
  30-simplex residual
  planted-core hit: no

reverse greedy:
  6 collapses
  30-simplex residual
  planted-core hit: no

16 deterministic random greedy trials:
  planted-core hits: 0
  unique residuals: 16
  residual size: 30 simplices in all 16 trials
~~~

Thus the planted core is not the only irreducible residual of the same measured size reached by simple collapse paths.

A future security relation must explain why one particular residual/certificate is cryptographically privileged. A hash that merely declares one planted residual to be correct is a verifier mechanism, not evidence that the planted reduction is intrinsically difficult to recover.

## Persistent fatal-flaw classes

### Shared hidden structure

Repeated public objects derived from one hidden representation may reveal an equivalent coordinate system or matching.

### Planted-instance leakage

The generator can expose an easier recognition/reconstruction problem than the nominal hard problem. A-014 is the first concrete repository example.

### Decomposition

Local gadgets or low-width structure may split the global problem into small independent constraints.

### Equivalent witnesses

An attacker may not need the original trapdoor. Any equivalent witness accepted by the final relation must be included in the security model.

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
