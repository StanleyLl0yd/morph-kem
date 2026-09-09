# MORPH-KEM

**MORPH-KEM** is exploratory post-quantum public-key cryptography research based on discrete Morse theory and combinatorial topology.

> **Research only. Not for production use. Not a security claim.**
>
> Do not use MORPH-KEM to protect real data, credentials, communications, or systems.

## Current status

**M0–M4 have all been implemented and rejected. No candidate primitive exists.**

- **M0** — broken by A-000 direct public coordinate recovery.
- **M1** — broken by A-008 meet-in-the-middle path recovery.
- **M2** — broken by A-014 structural hidden-core reconstruction.
- **M3** — honest equivalent-witness relation; broken by A-016 collapse plus spanning-tree construction.
- **M4** — closed triangulated tori with zero free collapses; broken by A-018 public primal/dual tree-cotree construction.

M4 matters because it removes the obvious M3 shortcut. Every tested edge has two incident triangles and every tested target has zero free collapse pairs, yet a label-invariant global algorithm still constructs an accepted (1,2,1) witness.

Fixed-seed M4 sweep:

~~~text
torus-3x3: free 0, deterministic accepted, random 32/32
torus-4x4: free 0, deterministic accepted, random 32/32
torus-5x5: free 0, deterministic accepted, random 32/32
torus-6x6: free 0, deterministic accepted, random 32/32
torus-7x7: free 0, deterministic accepted, random 32/32
~~~

## Research discipline

- Any equivalent accepted witness counts as attacker success.
- Generated distributions are part of the attack surface.
- Worst-case hardness is not average-case cryptographic hardness.
- Negative results are preserved.
- Structural breaks are redesigned, not repaired by larger parameters.
- No KEM wrapper until a primitive survives dedicated attacks.

## Key files

- src/morph_kem/ — constructions and attacks
- tests/ — exact validators and attack tests
- scripts/ — deterministic baselines and sweeps
- docs/05-cryptanalysis.md — attack ledger
- docs/13-m4-closed-surface.md — M4 result
- notes/research-log.md — chronological record
- spec/morph-kem-v0.1.md — future-spec skeleton

## Next direction

**M5:** irregular non-manifold 2-complexes generated around a planted acyclic Hasse matching, with greedy, branch-and-bound, SAT/CSP, incidence-statistical, canonicalization, and width attacks before scaling.

No security or post-quantum claim exists.

## Naming

MORPH-KEM is a working research name: Morse Obfuscated Reduction Path KEM.
