# 03 — Provisional construction

## Status

This document records the current construction sketch. It is intentionally non-normative until the objects and distributions are formalized.

## Hidden coordinates

Start with a simple hidden representation containing a sequence of binary coordinate gadgets

[
T_i^0,;T_i^1.
]

For seed

[
s=(s_1,dots,s_ell),
]

the hidden object is built by composing the selected transformations.

## Obfuscating representation

A secret structure-preserving transformation (Phi) maps the simple hidden representation into a complicated public representation.

Conceptually,

[
G_i^b=Phicirc T_i^bcircPhi^{-1}.
]

The public key exposes enough information to evaluate (G_i^b) but should not expose a useful description of (Phi^{-1}).

This requirement is speculative and is the main structural risk of the proposal.

## Key generation sketch

[
(pk,td)leftarrowoperatorname{KeyGen}(1^lambda)
]

where (td) contains a compact representation of a useful acyclic Morse flow, anchors, and any secret coordinate metadata needed for deterministic inversion.

The generator must avoid trivially distinguishable (0/1) gadgets and must treat every visible invariant as possible leakage.

## Encapsulation sketch

1. Sample a uniformly random seed (s).
2. Apply the public forward transformations selected by (s).
3. Canonically encode the resulting object as (ct).
4. Derive a shared secret from domain separation, (H(pk)), (s), and (H(ct)).

## Decapsulation sketch

1. Parse and validate the ciphertext canonically.
2. Use the trapdoor reduction flow to recover a candidate seed (s').
3. Recompute or otherwise verify the acceptance relation.
4. Derive the same shared secret on valid input.
5. Use constant-shape failure handling / implicit rejection in any future CCA-oriented construction.

## Correctness obligation

A formal construction must prove that honest encapsulation followed by decapsulation succeeds with probability 1 or with a precisely bounded negligible failure probability.

## Critical unresolved issue

The public maps share hidden structure. If an attacker can jointly analyze them to recover an equivalent hidden coordinate system, the construction fails regardless of the difficulty of generic Morse optimization.
