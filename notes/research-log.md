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

M0 is therefore not a security candidate.

### Verification

- Python 3.11/3.12/3.13 CI passed;
- all 256 toy-8 seeds passed forward/trapdoor/direct-attack checks;
- exhaustive toy-8 recovery is part of CI.

## 2026-09-09 — M1 non-local branching-path experiment

### Question

Does replacing coordinate-local public markers with globally supported transformations make the hidden path plausibly difficult to recover?

### Implemented

- one shared 2D simplicial scaffold;
- deterministic two-way public branching program;
- both branches at each layer are global vertex permutations;
- minimum support threshold for each branch and for the relative branch transform;
- exact public path-forward relation;
- exhaustive small-path recovery;
- meet-in-the-middle path recovery;
- collision profiling;
- path-12, path-16, path-20, path-24 experiment presets.

### Cryptanalytic result

A-000 no longer applies directly because a selected bit is not represented by an independent public triangle.

However, A-008 recovers the branch path generically by meeting forward prefix states with reverse suffix states.

For ell layers, balanced recovery enumerates approximately:

~~~text
2^(ell/2) forward states
+
2^(ell/2) reverse states
~~~

rather than 2^ell complete paths.

This works because every public branch is efficiently invertible and both inverse choices remain valid at every reverse layer.

### Initial development observations

- path-16 target 0xB6D3 recovered from 256 forward + 256 reverse states;
- path-20 target 0xB6D3A recovered from 1024 forward + 1024 reverse states;
- tested path-12 instance: 4096 seeds, 4096 unique outputs, no output collision;
- branch and relative supports remained high in the tested instances, so the result is not explained by branch locality.

### Interpretation

M1 is not a security candidate.

The negative result is useful: **global support is not inversion asymmetry**. A future construction cannot be only a secret word in public efficiently invertible transformations.

### Next milestone

M2 should test a genuinely asymmetric state transition, preferably tied back to discrete Morse reductions: public forward generation should remain efficient while naive reverse search encounters many admissible predecessors, and a hidden global reduction certificate should select a useful path.

M2 must be attacked before any KEM wrapper is added.
