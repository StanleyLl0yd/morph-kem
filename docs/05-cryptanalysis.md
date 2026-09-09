# 05 — Cryptanalysis ledger

This file is intentionally a ledger of attacks, including attacks that succeed.

## Current attack surface

| ID | Attack family | Current assessment | Status |
|---|---|---|---|
| A-001 | Greedy / heuristic Morse reduction | High risk | Not implemented |
| A-002 | Joint recovery from public (G_i) | Critical risk | Not implemented |
| A-003 | Canonical labeling / isomorphism recovery | High risk | Not implemented |
| A-004 | SAT reconstruction | High risk | Not implemented |
| A-005 | MILP reconstruction | High risk | Not implemented |
| A-006 | Treewidth / separator methods | High risk | Not implemented |
| A-007 | Spectral / invariant distinguisher | High risk | Not implemented |
| A-008 | Meet-in-the-middle on coordinate path | High risk | Not implemented |
| A-009 | Learned gadget recognition | Unknown/high | Not implemented |
| A-010 | Invalid-ciphertext / oracle leakage | Critical for KEM | Not implemented |
| A-011 | Generic quantum search | Expected baseline | Analytical only |
| A-012 | Quantum walk / structure exploitation | Unknown | Not analyzed |

## Fatal-flaw candidate #1: shared hidden structure

If

[
G_i=Phi T_iPhi^{-1}
]

for many (i), an attacker receives many related public objects sharing the same hidden (Phi).

The attacker may be able to recover (Phi), an equivalent coordinate system, or enough common structure to invert ciphertexts without solving a generic Morse problem.

This attack must be tested before investing in large parameters.

## Fatal-flaw candidate #2: planted-instance leakage

KeyGen starts from a deliberately easy hidden instance and disguises it. Generated instances may therefore occupy a statistically recognizable subset of all complexes.

Experiments must compare generated instances with suitable controls and search for cheap distinguishers.

## Fatal-flaw candidate #3: decomposition

If coordinates or gadgets can be isolated, seed recovery may decompose into many small independent problems. Local invariants, separators, graph embeddings, or message-passing models may reveal this.

## Reporting template

For every attack:

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
