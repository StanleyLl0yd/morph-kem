# 05 — Cryptanalysis ledger

This file is intentionally a ledger of attacks, including attacks that succeed.

## Current attack surface

| ID | Attack family | Current assessment | Status |
|---|---|---|---|
| A-000 | Direct public recipe recovery against M0 | **Fatal by design** | Implemented; breaks every M0 seed in linear time |
| A-001 | Greedy / heuristic Morse reduction | High risk | Not implemented |
| A-002 | Joint recovery from public transformations | Critical risk | Not implemented |
| A-003 | Canonical labeling / isomorphism recovery | High risk | Not implemented |
| A-004 | SAT reconstruction | High risk | Not implemented |
| A-005 | MILP reconstruction | High risk | Not implemented |
| A-006 | Treewidth / separator methods | High risk | Not implemented |
| A-007 | Spectral / invariant distinguisher | High risk | Not implemented |
| A-008 | Generic meet-in-the-middle path recovery | **Fatal to M1 as a security candidate** | Implemented |
| A-009 | Learned gadget recognition | Unknown/high | Not implemented |
| A-010 | Invalid-ciphertext / oracle leakage | Critical for KEM | Initial malformed-input tests only |
| A-011 | Generic quantum search | Expected baseline | Analytical only |
| A-012 | Quantum walk / structure exploitation | Unknown | Not analyzed |

## A-000 — direct public recipe recovery

### Target

M0 executable toy relation.

### Observation

For every coordinate, M0 publishes two candidate triangles and the ciphertext contains exactly one of them. An attacker can therefore recover each bit with two membership tests.

### Complexity

Ignoring representation lookup costs, the attack needs O(ell) coordinate tests and no secret information.

### Result

**Complete break of M0 by design.**

The implementation is direct_public_recover. Unit tests exercise it over all 256 toy-8 seeds.

### Interpretation

This does not falsify a claimed security property because M0 makes none. It established the first minimum bar: public evaluation cannot expose independent coordinate-local recipes whose selected outputs remain directly recognizable.

## A-008 — generic meet-in-the-middle path recovery

### Target

M1 non-local branching-path experiment.

### Observation

M1 removes M0's local triangle marker. Each selected branch instead relabels the complete shared simplicial scaffold using a large-support public permutation.

However, every layer still has two public efficiently invertible choices. An attacker can enumerate prefixes from the base and suffixes backwards from the target, then join equal middle states.

### Complexity

For ell layers and a balanced split:

~~~text
forward states  ~ 2^(ell/2)
reverse states  ~ 2^(ell/2)
memory          ~ 2^(ell/2)
~~~

plus representation and verification cost.

Both inverse branch choices are always syntactically valid, so reverse enumeration receives no structural pruning from the simplicial-complex validity relation.

### Initial result

The implementation mitm_path_recover recovered tested path-16 and path-20 targets without secret information.

A tested path-12 instance also had 4096 distinct final states for 4096 seeds, showing that the observed recovery was not relying on a collision in that instance.

### Interpretation

**M1 is unsuitable as a security candidate.**

This is a stronger lesson than A-000: removing local coordinate leakage is necessary but not sufficient. A public low-branching sequence of efficiently invertible transformations retains a generic bidirectional-search weakness even when every branch has global support.

A future model must introduce real forward/inverse asymmetry rather than merely hiding local coordinates behind global permutations.

## Fatal-flaw candidate #1: shared hidden structure

If many public transformations share one hidden representation, an attacker may recover that representation, an equivalent coordinate system, or enough common structure to invert ciphertexts without solving a generic Morse problem.

This attack remains relevant even if M2 removes A-008.

## Fatal-flaw candidate #2: planted-instance leakage

KeyGen starts from a deliberately easy hidden instance and disguises it. Generated instances may therefore occupy a statistically recognizable subset of all complexes.

Experiments must compare generated instances with suitable controls and search for cheap distinguishers.

## Fatal-flaw candidate #3: decomposition

If coordinates or gadgets can be isolated, seed recovery may decompose into many small independent problems. Local invariants, separators, graph embeddings, or message-passing models may reveal this.

M0 demonstrates the extreme local form through A-000. M1 demonstrates that merely replacing local gadgets with global reversible steps still leaves a generic path decomposition through A-008.

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
