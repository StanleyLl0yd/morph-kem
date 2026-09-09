# 00 — Overview

## Objective

MORPH-KEM investigates a possible trapdoor-cryptography direction based on hidden discrete-Morse reduction structure in finite combinatorial-topological objects.

The central research question is not "can we encode a secret in a complicated complex?" It is:

> Can we define a generated-instance distribution for which forward evaluation and inversion with a compact trapdoor are efficient, while inversion or trapdoor recovery without that trapdoor resists all known classical and quantum attacks?

## Research status

The project begins at the lowest maturity level:

- no average-case hardness result;
- no reduction from a standard hard problem;
- no quantum-security proof;
- no IND-CPA or IND-CCA proof;
- no production parameters;
- no independent cryptanalysis.

Accordingly, every security-relevant statement should be read as a hypothesis until proved.

## Candidate architecture

The provisional architecture has four layers:

1. a family of finite complexes with hidden reduction structure;
2. a secret acyclic discrete-Morse matching / reduction certificate;
3. public forward transformations that obscure simple hidden coordinates;
4. a KEM wrapper that derives a shared secret from a recovered hidden seed and transcript binding.

The cryptographic value of the entire direction depends on whether the public structure leaks the hidden reduction certificate.

## Primary falsification targets

The first experiments should try to show the idea is broken by:

- greedy or heuristic Morse reduction;
- canonical labeling / isomorphism recovery;
- common-structure recovery across public transformations;
- SAT or MILP reconstruction;
- low-treewidth or separator algorithms;
- statistical invariants;
- meet-in-the-middle decomposition;
- graph-neural or other learned gadget recognition;
- malformed-ciphertext or decapsulation leakage;
- quantum search or quantum-walk improvements.

A fast break is a useful result.
