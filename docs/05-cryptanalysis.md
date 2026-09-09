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
| A-008 | Meet-in-the-middle on coordinate path | High risk | Not implemented |
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

This does not falsify a claimed security property because M0 makes none. It establishes a minimum bar for M1: public evaluation cannot expose independent coordinate-local recipes whose selected outputs remain directly recognizable.

## Fatal-flaw candidate #1: shared hidden structure

If many public transformations share one hidden representation, an attacker may recover that representation, an equivalent coordinate system, or enough common structure to invert ciphertexts without solving a generic Morse problem.

This attack must be tested before investing in large parameters.

## Fatal-flaw candidate #2: planted-instance leakage

KeyGen starts from a deliberately easy hidden instance and disguises it. Generated instances may therefore occupy a statistically recognizable subset of all complexes.

Experiments must compare generated instances with suitable controls and search for cheap distinguishers.

## Fatal-flaw candidate #3: decomposition

If coordinates or gadgets can be isolated, seed recovery may decompose into many small independent problems. Local invariants, separators, graph embeddings, or message-passing models may reveal this.

M0 demonstrates the extreme case of this flaw through A-000.

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
