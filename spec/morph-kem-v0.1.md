# MORPH-KEM v0.1 — research draft

**Status:** incomplete, non-normative, research only.

## 1. Purpose

This document is the evolving specification skeleton for MORPH-KEM. It must not be treated as a deployable cryptographic standard.

The executable M0 relation is specified separately in docs/09-toy-model.md. M0 is deliberately broken and is not the cryptographic construction described by future versions of this document.

## 2. Algorithms

A future version will define exactly:

~~~text
(pk, sk) <- KeyGen(1^lambda)
(ct, K) <- Encaps(pk)
K' <- Decaps(sk, ct)
~~~

and the valid-ciphertext relation.

## 3. Domain separation

Every hash/KDF invocation will use fixed ASCII domain-separation labels containing the protocol name and major version.

No concrete hash or XOF is selected by this draft yet.

M0 uses domain-separated SHA-256 only for deterministic research generation and key binding; that choice is not a future KEM-suite decision.

## 4. Encoding

The final specification must define a canonical byte encoding for every public object and reject:

- duplicate simplices;
- non-canonical vertex order;
- out-of-range dimensions;
- inconsistent face closure;
- integer overflow;
- trailing data;
- ambiguous alternate encodings.

M0 has an executable canonical complex encoding with magic/version MKSC || 0x01; see docs/09-toy-model.md.

## 5. Key generation

TBD after formal definition of a generated instance distribution that does not have M0's trivial public-coordinate leakage.

## 6. Encapsulation

TBD after formal definition of public forward evaluation.

## 7. Decapsulation

TBD after formal definition of trapdoor inversion and a constant-shape invalid-ciphertext strategy.

## 8. Correctness

No correctness theorem is stated for the future KEM.

The separate M0 executable relation has deterministic round-trip tests for all toy-8 seeds.

## 9. Security

No IND-CPA, IND-CCA, post-quantum, or concrete-bit-security claim is stated by this draft.

## 10. Parameter sets

Only toy parameter sets are permitted at this stage.
