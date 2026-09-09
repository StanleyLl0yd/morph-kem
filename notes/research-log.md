# Research log

## 2026-09-09 — project initialization

Selected combinatorial topology and discrete Morse reductions as the initial research family.

Provisional research labels:

- HMCP — Hidden Morse Coordinate Problem
- HMRP — Hidden Morse Reduction Path Problem
- HMCR — Hidden Morse Conjugacy Recovery

The project starts with no security claim. Negative results and successful breaks are first-class outputs.

## 2026-09-09 — M0 executable relation

Implemented canonical finite simplicial complexes, deterministic toy generation, planted elementary-collapse certificates, exact forward/accept/invert functions, and exhaustive baselines.

A-000 directly recovers every M0 seed from public coordinate-local triangle recipes.

**Result:** M0 rejected as a security candidate.

## 2026-09-09 — M1 non-local branching path

Replaced local M0 markers with globally supported public vertex permutations on one shared 2D scaffold.

A-008 meet-in-the-middle recovery joins forward prefix states and inverse suffix states in roughly 2^(ell/2) state enumeration.

M1 also preserves the complete simplicial isomorphism class because every step is only a relabeling.

**Result:** M1 rejected as a security candidate.

**Lesson:** global support is not inversion asymmetry.

## 2026-09-09 — M2 collapse maze

### Construction

Implemented:

- generic elementary expansion as the exact inverse of collapse;
- deterministic hidden connected 3-regular 1D core;
- overlapping edge/triangle elementary expansions;
- secret final vertex relabeling;
- public target + domain-separated core digest;
- trapdoor core + exact reverse-collapse certificate;
- greedy reduction attacks;
- deterministic random-greedy surveys;
- bounded public collapse DFS;
- structural 3-regular core recovery;
- fixed-seed attack scaling sweep.

### Branching result

Deterministic maze-6:

~~~text
target simplices:        42
core simplices:          30
planted steps:            6
initial free pairs:      18
mean free pairs on planted path: 10.50
~~~

Lexicographic and reverse greedy both reach 30-simplex residuals that are not the planted core.

Sixteen deterministic random-greedy trials produce sixteen distinct 30-simplex residuals and zero planted-core hits.

This confirms genuine path dependence.

### A-013 collapse search

Bounded DFS recovers the exact maze-6 core in 1095 explored nodes.

### A-014 structural core recovery

The stronger attack uses a generator invariant:

- every non-core edge is added together with a filled triangle;
- zero-triangle-incidence target edges are therefore forced hidden-core edges;
- the hidden core is publicly known to be 3-regular.

Backtracking over only compatible 3-regular spanning subgraphs plus public digest verification recovers the fixed-seed baseline:

~~~text
maze-4:  nodes 13
maze-6:  nodes 59
maze-8:  nodes 520
maze-10: nodes 51
maze-12: nodes 441
~~~

All five tested cores are recovered.

**Result:** M2 rejected as a security candidate.

### Main lesson

A difficult-looking reduction maze is irrelevant if the **generator leaks an easier reconstruction problem**.

Secret vertex relabeling does not hide degree/incidence semantics.

### Next milestone

Do not scale M2.

Design the next generated distribution around these constraints:

- no fixed low-complexity regular core family;
- incidence-balanced core/non-core cells;
- no obvious graph-factor/matching recovery formulation;
- explicit equivalent-witness semantics;
- structural-recovery attacks implemented before parameter scaling;
- no KEM wrapper until a primitive survives those attacks.
