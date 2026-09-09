# MORPH-KEM v0.1 — research draft

**Status:** incomplete, non-normative, research only.

## 1. Purpose

This is the specification skeleton for a possible future MORPH-KEM construction. It is not a deployable cryptographic standard.

The repository currently contains four **rejected attack experiments**:

- M0 — coordinate-local toy relation, broken by A-000;
- M1 — reversible global branching path, broken by A-008;
- M2 — non-invertible collapse maze, broken by A-014;
- M3 — honest equivalent-witness Morse relation on graph-expanded complexes, broken by A-016.

None is the future KEM described by this skeleton.

## 2. Algorithms

A future version would have to define exactly:

~~~text
(pk, sk) <- KeyGen(1^lambda)
(ct, K) <- Encaps(pk)
K' <- Decaps(sk, ct)
~~~

and a complete public success relation.

## 3. Equivalent-witness semantics

A future relation must never require recovery of one arbitrary planted generator history if other mathematically equivalent witnesses exist.

Any witness satisfying the public relation is an attacker success.

M3 is the repository reference implementation of this rule for acyclic Morse matchings.

## 4. Domain separation

Every hash/KDF invocation must use fixed domain-separation labels containing the protocol name and major version.

Hashes used inside deterministic research generators are not future KEM-suite decisions.

## 5. Encoding

The research code defines canonical bytes for finite simplicial complexes.

Any future specification must additionally define canonical encodings for public keys, witness/trapdoor objects, ciphertexts, parameter identifiers, and extension fields.

Malformed, duplicate, non-closed, overflowing, trailing, or alternate encodings must be rejected.

## 6. Generated distribution

TBD.

This remains the central gate after A-014 and A-016.

A future generated distribution must not expose a simpler solver through degree/incidence profiles, graph factors or spanning trees, collapse to an easy lower-dimensional class, canonicalization, low-width decomposition, local gadget recognition, planted-substructure tests, or generic greedy matching.

## 7. Forward evaluation

TBD.

A future public forward operation must not reproduce M0's recognizable local choices, M1's reversible path, M2's recognizable planted core, or M3's graph-plus-collapsible-decoration relation.

## 8. Trapdoor inversion

TBD.

The exact role of a hidden discrete-Morse certificate and equivalent certificates must be formalized before any KEM wrapper.

A future trapdoor is useful only if producing any accepted public witness remains hard without it.

## 9. Correctness

No correctness theorem is stated for a future KEM.

M0-M3 provide correctness only for rejected research experiments.

## 10. Security

No one-wayness, IND-CPA, IND-CCA, post-quantum, or concrete-bit-security claim exists.

The next acceptable milestone is a generated equivalent-witness primitive that survives repository-local constructive and structural cryptanalysis.

## 11. Parameters

No security parameter sets exist.

Only toy or experimental names may be used until an explicit security model, generated distribution, and attack analysis justify candidate parameters.
