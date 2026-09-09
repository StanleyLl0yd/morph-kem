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

The public forward transformations may share enough hidden structure to recover the secret representation. This is currently treated as the highest-priority attack, not as a secondary optimization.

### Research discipline

The project begins with no security claim. Negative results, distinguishers, and successful breaks are first-class outcomes.

### Next milestone

Formalize a tiny deterministic instance generator and exact acceptance relation before implementing a KEM wrapper.
