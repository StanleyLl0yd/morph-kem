# Research log

## 2026-09-09 — project initialization

### Goal

Explore a new mathematical direction for post-quantum public-key cryptography without inventing new symmetric primitives.

### Initial direction

Selected combinatorial topology and discrete Morse reductions as the first research family.

The proposed trapdoor is a hidden globally consistent reduction certificate / acyclic Morse flow. The intended asymmetry is efficient inversion with the certificate versus difficult recovery of an equivalent useful reduction structure from public generated instances.

### Provisional problem names

- HMCP — Hidden Morse Coordinate Problem
- HMRP — Hidden Morse Reduction Path Problem
- HMCR — Hidden Morse Conjugacy Recovery

### Primary concern

The public forward transformations may share enough hidden structure to recover the secret representation. This is treated as the highest-priority attack, not as a secondary optimization.

### Research discipline

The project begins with no security claim. Negative results, distinguishers, and successful breaks are first-class outcomes.

## 2026-09-09 — M0 executable relation

### Implemented

- canonical finite simplicial-complex representation and binary encoding;
- deterministic toy KeyGen with a planted vertex permutation;
- one elementary-collapse gadget per hidden bit;
- public Forward and exact Accept relation;
- trapdoor inversion with collapse-to-base and exact re-encapsulation validation;
- toy-8 through toy-32 experiment presets;
- exhaustive seed-recovery baseline;
- malformed-input/canonicalization tests.

### Immediate cryptanalytic result

A-000 directly recovers every M0 seed because the public key exposes the two coordinate-local candidate triangles. The attack is linear in the number of coordinates and is implemented intentionally.

This is a successful falsification of M0 as a security candidate, but M0 was designed only as an executable harness. It establishes the baseline requirement that the next model must not leave selected hidden coordinates locally recognizable from public recipes.

### Local verification

On the initial implementation:

- Python byte-compilation passed;
- 15 unit tests passed;
- all 256 toy-8 seeds passed forward/trapdoor/direct-attack checks;
- exhaustive recovery of a toy-8 sample succeeded.

### Next milestone

Design M1 around overlapping/non-local public transformations and define the first generated distribution for which direct coordinate inspection is unavailable. Then attack that distribution before adding any KEM wrapper.
