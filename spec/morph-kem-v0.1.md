# MORPH-KEM v0.1 — research draft

**Status:** incomplete, non-normative, research only.

## 1. Purpose

This is the specification skeleton for a possible future MORPH-KEM construction. It is not a deployable cryptographic standard.

The repository currently contains three **rejected attack experiments**:

- M0 — coordinate-local toy relation, broken by A-000;
- M1 — reversible global branching path, broken by A-008;
- M2 — non-invertible collapse maze, broken by A-014 structural core recovery.

None of those experiments is the future KEM described by this skeleton.

## 2. Algorithms

A future version would have to define exactly:

~~~text
(pk, sk) <- KeyGen(1^lambda)
(ct, K) <- Encaps(pk)
K' <- Decaps(sk, ct)
~~~

and the complete valid-ciphertext/equivalent-witness relation.

## 3. Domain separation

Every hash/KDF invocation must use fixed domain-separation labels containing the protocol name and major version.

SHA-256 used inside M0/M1/M2 deterministic experiment generation or public experiment digests is not a future KEM-suite decision.

## 4. Encoding

The existing research code defines canonical bytes for finite simplicial complexes.

Any future specification must additionally define canonical encodings for public keys, trapdoor/certificate objects, ciphertexts, parameter identifiers, and extension fields.

Malformed, duplicate, non-closed, overflowing, trailing, or alternate encodings must be rejected.

## 5. Generated distribution

TBD.

This section is now a hard gate after A-014. It must specify not merely how to create an easy planted instance, but why the resulting public distribution does not expose a simpler reconstruction problem through:

- degree/incidence profiles;
- graph factors or matchings;
- canonicalization;
- low-width decomposition;
- local gadget recognition;
- simple planted-substructure tests.

## 6. Forward evaluation

TBD.

A future public forward operation must not reproduce M0's local recognizable choices, M1's publicly reversible low-branching path, or M2's easily recognizable planted core family.

## 7. Trapdoor inversion

TBD.

The exact role of a hidden discrete-Morse certificate and the treatment of equivalent certificates/residuals must be formalized before any KEM wrapper.

## 8. Correctness

No correctness theorem is stated for a future KEM.

M0/M1/M2 only provide correctness results for their respective rejected research models.

## 9. Security

No one-wayness, IND-CPA, IND-CCA, post-quantum, or concrete-bit-security claim exists.

The next acceptable milestone is a generated primitive that survives repository-local structural cryptanalysis, not a larger parameter set.

## 10. Parameters

No security parameter sets exist.

Only toy/experimental parameter names may be used until an explicit security model, generated distribution, and attack analysis justify candidate parameters.
