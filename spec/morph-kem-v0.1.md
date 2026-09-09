# MORPH-KEM v0.1 — research draft

**Status:** incomplete, non-normative, research only.

M0–M4 are rejected attack experiments, not deployable cryptography:

- M0 broken by A-000;
- M1 broken by A-008;
- M2 broken by A-014;
- M3 broken by A-016;
- M4 broken by A-018.

## Equivalent-witness rule

Any future relation must count every mathematically accepted equivalent witness as attacker success. Recovery of one arbitrary planted history is not a security objective.

## Generated distribution gate

A future distribution must be tested against local-role leakage, reversible or low-dimensional decomposition, planted substructure, primal/dual tree-like constructions, generic greedy matching, SAT/CSP, low-width structure, canonicalization/statistical distinguishers, and eventually quantum attacks.

## Future algorithms

Only after a primitive survives those gates would it make sense to define:

~~~text
(pk, sk) <- KeyGen(1^lambda)
(ct, K) <- Encaps(pk)
K' <- Decaps(sk, ct)
~~~

No such construction is currently justified.

No one-wayness, IND-CPA, IND-CCA, post-quantum, concrete-bit-security, or production parameter claim exists.
