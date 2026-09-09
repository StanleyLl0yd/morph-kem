# MORPH-KEM v0.1 — research draft

**Status:** incomplete, non-normative, research only.

## 1. Purpose

This document is the evolving specification skeleton for MORPH-KEM. It must not be treated as a deployable cryptographic standard.

## 2. Algorithms

A future version will define exactly:

[
(pk,sk)leftarrowoperatorname{KeyGen}(1^lambda)
]

[
(ct,K)leftarrowoperatorname{Encaps}(pk)
]

[
K'leftarrowoperatorname{Decaps}(sk,ct)
]

and the valid-ciphertext relation.

## 3. Domain separation

Every hash/KDF invocation will use fixed ASCII domain-separation labels containing the protocol name and major version.

No concrete hash or XOF is selected by this draft yet.

## 4. Encoding

The final specification must define a canonical byte encoding for every public object and reject:

- duplicate simplices;
- non-canonical vertex order;
- out-of-range dimensions;
- inconsistent face closure;
- integer overflow;
- trailing data;
- ambiguous alternate encodings.

## 5. Key generation

TBD after formal definition of the generated instance distribution.

## 6. Encapsulation

TBD after formal definition of public forward evaluation.

## 7. Decapsulation

TBD after formal definition of trapdoor inversion and a constant-shape invalid-ciphertext strategy.

## 8. Correctness

No correctness theorem is stated yet.

## 9. Security

No IND-CPA, IND-CCA, post-quantum, or concrete-bit-security claim is stated by this draft.

## 10. Parameter sets

Only toy parameter sets are permitted at this stage.
