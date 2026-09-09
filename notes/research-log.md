# Research log

## 2026-09-09

### M0
Canonical toy relation implemented; A-000 directly recovers coordinates. **Rejected.**

### M1
Global reversible path implemented; A-008 meet-in-the-middle recovers paths. **Rejected.**

### M2
Genuine collapse maze implemented; A-014 reconstructs the 3-regular planted core from generator invariants; A-015 shows many alternative residuals. **Rejected.**

### M3
Equivalent-witness relation formalized: any valid acyclic Hasse matching with public target vector is accepted. A-016 collapses graph-expanded instances to arbitrary graph residuals and completes a spanning-tree witness; A-017 generic greedy matching also succeeds frequently. **Rejected.**

### M4 — closed surface

M4 uses periodic triangulated tori to remove M3's free-collapse-to-graph shortcut.

For all fixed-seed tested sets, every edge has two incident triangles and free collapse pair count is zero.

A-018 constructs a public primal/dual tree-cotree Morse matching.

Baseline torus-4x4:

~~~text
V/E/F: 16/48/32
free pairs: 0
target: (1,2,1)
primal/dual tree edges: 15/31
critical edges: 2
tree-cotree accepted: yes
randomized survey: 16/16 accepted, 16 unique
generic greedy: 0/4 target hits, best total critical 6
~~~

Scaling:

~~~text
torus-3x3: accepted, random 32/32, unique 32
torus-4x4: accepted, random 32/32, unique 32
torus-5x5: accepted, random 32/32, unique 32
torus-6x6: accepted, random 32/32, unique 32
torus-7x7: accepted, random 32/32, unique 32
~~~

**M4 rejected.**

Main lesson: genuine 2D structure and absence of free collapses do not create hardness if the public family has a simple global witness decomposition.

### Next

M5: irregular non-manifold 2-complexes with planted acyclic matching; add exact/solver attacks before scaling.


### H0 — Hyperbolic / non-orientable side track

Opened a separate H-series for the Möbius / Escher / Lobachevsky direction.

Working label: **Hyperbolic Frustrated MORPH (HFM)**.

Literature scan immediately rules out several naive hardness stories:

- ordinary word/conjugacy problems in standard hyperbolic groups are often algorithmically efficient;
- hyperbolic tessellations and finite quotients are established mathematical machinery;
- non-orientability by itself is a simple topological invariant;
- canonical/Delaunay tiling machinery creates a direct normalization/canonicalization attack surface.

H0 therefore separates geometry, topology, transition/holonomy, and witness layers.

The first H1 ladder will deliberately begin with:

1. Z2 orientation holonomy — expected to collapse to GF(2) linear algebra;
2. S3 non-abelian frame holonomy — attacked by gauge fixing, abelianization, cycle basis, exact CSP, canonicalization, and local statistics.

No H-series security claim exists.
