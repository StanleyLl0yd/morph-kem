# 09 — M0 executable toy relation

## Status

The M0 toy relation is an executable research harness. It is **deliberately not a security candidate**.

Its purpose is to make the repository's objects, encodings, correctness checks, attack APIs, and experiment workflow concrete before attempting a harder planted distribution.

## Simplicial-complex representation

A complex is stored as the complete downward-closed set of non-empty simplices.

A simplex is a strictly increasing tuple of unsigned 32-bit vertex identifiers. Canonical order is increasing simplex arity and then lexicographic vertex order.

The binary encoding is:

~~~text
"MKSC" || 0x01
u32be simplex_count
repeat simplex_count times:
    u8 arity
    repeat arity times:
        u32be vertex
~~~

The decoder rejects non-canonical ordering, repeated vertices, missing faces, truncated fields, excessive arity/count, and trailing bytes.

## Hidden coordinate gadget

For coordinate i, hidden vertices are:

~~~text
a_i   = 5i
u_i0  = 5i + 1
v_i0  = 5i + 2
u_i1  = 5i + 3
v_i1  = 5i + 4
~~~

The base contains four arms:

~~~text
(a_i, u_i0)   (a_i, v_i0)
(a_i, u_i1)   (a_i, v_i1)
~~~

Bit b adds triangle (a_i, u_ib, v_ib), which also adds the missing edge (u_ib, v_ib). That edge is a free codimension-one face of the triangle. Removing the pair is an elementary collapse back to the base gadget.

## Deterministic key generation

For a parameter set and non-empty master_seed, KeyGen:

1. constructs the hidden base for all coordinates;
2. derives a deterministic Fisher-Yates vertex permutation using domain-separated SHA-256 blocks and rejection sampling;
3. relabels the base and both candidate triangles for every coordinate;
4. publishes the relabeled base and public forward recipes;
5. stores the hidden-to-public vertex permutation as the M0 trapdoor;
6. binds the secret key to SHA-256(domain || canonical_public_key).

The deterministic seed exists for reproducible experiments; it is not a production entropy design.

## Forward relation

For seed s in [0, 2^ell), bit i is interpreted little-endian:

~~~text
b_i = (s >> i) & 1
~~~

The public forward algorithm adds exactly one public triangle per coordinate.

The exact acceptance relation is:

~~~text
Accept(pk, s, C) := Forward(pk, s) == C
~~~

where equality is equality of canonical simplicial complexes.

## Trapdoor inversion

The M0 trapdoor inversion:

1. verifies public/secret key binding;
2. relabels the ciphertext back into hidden coordinates;
3. requires exactly one candidate triangle per coordinate;
4. reads the corresponding bit;
5. applies the planted elementary-collapse pair for every selected triangle;
6. requires the result to equal the canonical hidden base;
7. re-runs public forward evaluation and requires exact acceptance.

## Deliberate break: A-000

The public key contains both forward recipes for every coordinate. Consequently an attacker can inspect the ciphertext for the two public candidate triangles and recover every bit directly in linear time.

This attack is implemented as direct_public_recover.

The break is intentional. M0 tests the **research machinery**, not the hardness assumption. Any future model that still exposes such coordinate-local recipes has already failed.

## Exhaustive baseline

The repository also implements exhaustive_recover, which evaluates all 2^ell seeds and checks the exact acceptance relation.

toy-8 exhaustive recovery is part of CI. Larger toy sets exist for scaling experiments, not as security levels.

## What M0 establishes

M0 establishes:

- an exact finite object model;
- canonical bytes;
- deterministic instance generation;
- a planted elementary-collapse certificate;
- exact forward/accept/invert functions;
- malformed-input rejection;
- a reproducible attack interface;
- a known fatal public attack that proves negative results can be represented cleanly.

M0 does **not** establish one-wayness, average-case hardness, post-quantum hardness, IND-CPA security, IND-CCA security, or useful parameter sizes.

## Exit criterion

M0 is complete when deterministic/canonical/correctness tests and the exhaustive toy-8 baseline are green in CI and the A-000 break is documented.

The next research step must replace coordinate-local public recipes with a construction whose public evaluation does not trivially reveal selected hidden coordinates.
