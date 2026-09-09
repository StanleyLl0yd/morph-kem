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


### H1 — signed holonomy calibration

Implemented Z2 and S3 vertex-frame/edge-transition experiments on deterministic cycle-rich graph scaffolds.

H1-Z2 behaves as expected: a public spanning tree fixes a gauge representative and exposes the fundamental-cycle bits with linear work.

H1-S3 failed even more strongly than expected.

The verifier accepts an edge exactly when its normalized S3 element is a transposition. Since the three transpositions are exactly the odd elements of S3, this condition is equivalent to one sign/parity equation per edge.

Thus the whole S3 relation factors through:

~~~text
S3 --sign--> Z2
~~~

and a public Z2 solution can be lifted using arbitrary fixed even/odd S3 representatives.

The direct attack `recover_s3_via_abelianization` therefore constructs an accepted equivalent witness in linear graph work.

**H1 rejected.**

Lesson: non-commutativity is irrelevant when the verifier accepts an entire fiber of a simple quotient homomorphism.


H1 measured baseline (fixed seed):

~~~text
h1-12:
  V/E/cycle rank = 12/18/7
  Z2 spanning-tree recovery = accepted
  S3 direct sign-lift recovery = accepted
  S3 direct edge checks = 54
  CSP cap 64: 64 solutions, 104 nodes, 0 backtracks

sweep:
  h1-8  -> direct accepted, 36 checks
  h1-10 -> direct accepted, 45 checks
  h1-12 -> direct accepted, 54 checks
  h1-16 -> direct accepted, 72 checks
  h1-20 -> direct accepted, 90 checks
~~~

The algebraic proof is stronger than the measurements: H1-S3's verifier is exactly its Z2 sign quotient.


### H2-E — Escher frustrated atlas started

Opened a separate Escher/Penrose branch rather than replacing the pending hyperbolic Klein-quartic branch.

The first H2-E1 calibration models relative height as edge increments in Z/7Z:

- every individual edge is locally satisfiable;
- contradictions appear only around cycles;
- the generator injects a bounded set of hidden defect/seam edges;
- the public verifier accepts any seam set within budget and any compatible height assignment.

This directly implements the "locally plausible, globally impossible" staircase intuition.

Prior-art review shows the local-to-global obstruction viewpoint is already formalized through sheaves/cohomology, network torsors, impossible-object geometry processing, and gain/group-labelled graphs. H2-E therefore makes no novelty claim for the intuition itself.

Implemented attacks:

- fundamental-cycle syndrome extraction;
- exact unbalanced-cycle branching for any equivalent seam repair.

Measured fixed-seed CI results confirm the expected break.

~~~text
escher-8:  min repair 1, nodes 4
escher-10: min repair 2, nodes 27
escher-12: min repair 2, nodes 27
escher-16: min repair 3, nodes 43
escher-20: min repair 3, nodes 164
~~~

For escher-20 the solver found a smaller equivalent repair than the planted four-edge seam set.

**H2-E1 rejected.**

The Escher intuition itself remains useful, but edge-relative height data is too low-order: its obstruction is completely captured by cycle gains/cohomology and seam repair is a known gain-graph balancing problem.

Next Escher experiment, if continued: overlapping multi-variable charts/higher-order constraints that cannot be flattened to one group label per graph edge.


### H2-E2 — higher-order Escher atlas started

H2-E1 showed that a one-dimensional relative-height field is only a gain graph.

H2-E2 raises the local data from edges to 3-variable charts.

Each chart is a signed NAE-3 relation. Two key properties are enforced:

1. every chart is individually satisfiable;
2. every pair of charts has a compatible joint local assignment.

The generator conditions normal charts on a hidden assignment until that assignment (up to global complement symmetry) is the unique normal-atlas global section. It then injects seam charts that reject that section, making the full public atlas globally inconsistent.

The public verifier accepts any equivalent repair: any seam-chart set within budget plus any satisfying global assignment.

The primary attack is exact minimum-violation NAE-CSP branch-and-bound.

No novelty/security claim is made. NAE-3SAT is a standard Boolean CSP family and the local/global-section viewpoint is established prior art.

Fixed-seed CI measurements:

~~~text
atlas-8:  min seam 1, nodes 43,  backtracks 21
atlas-10: min seam 1, nodes 41,  backtracks 20
atlas-12: min seam 1, nodes 37,  backtracks 18
atlas-14: min seam 1, nodes 73,  backtracks 36
atlas-16: min seam 1, nodes 281, backtracks 138
~~~

All tested chart pairs were locally compatible.

For atlas-12:

~~~text
pairwise compatibility: 435/435
planted budget: 2
minimum equivalent repair: 1
proven minimum: yes
nodes/backtracks: 37/18
~~~

The public role-signature audit also exposed planted roles: no planted seam signature occurred among normal charts in atlas-10, atlas-12, or atlas-14.

**H2-E2 rejected.**

This is a stronger lesson than "SAT is easy at small n." The generated distribution itself has a one-seam escape and visible planted-role correlations. Scaling would only hide the defect rather than fix it.

A future H2-E3 must change the verifier relation and generator, not increase NAE instance size.


### H2-E3 — all-charts frontier review

The natural next Escher construction was intentionally stopped before code.

Naive formulation:

~~~text
hidden global state x
+
many overlapping constant-size public chart neighborhoods Sj
+
bounded-local predicate/output on x|Sj
+
inversion = recover any globally compatible x'
~~~

This is essentially Goldreich's random local-function / planted-CSP paradigm.

Key prior-art findings:

- Goldreich proposed overlapping small input subsets selected by combinatorial/expander structure with one fixed local predicate as a candidate OWF in 2000.
- Planted-CSP theory directly studies recovery of a planted assignment from such local constraints.
- Concrete Goldreich-PRG cryptanalysis includes guess-and-determine, algebraic, guess-and-decode, and correlation attacks.
- ECCC TR25-139 (2025, revised 2026) gives a search-to-decision reduction for random local functions for any constant-arity predicate.
- CSP global-section and cohomological local-to-global methods are established prior art.

**Decision: naive H2-E3 rejected before implementation.**

Changing visualization, using a hyperbolic tiling, larger finite alphabet, non-abelian local state, or another constant-arity predicate would not by itself create a new mathematical cryptosystem.

Proposed next frontier: H3-E Lifted Atlas, but only if hidden covering/lifting data changes the computational relation itself and survives canonicalization, graph-cover, monodromy, fundamental-group, homology, group-action, and local-function-flattening attacks.


### H3-E0 — lifted-atlas public-evaluation calibration started

The H2-E3 frontier suggested that a meaningful successor must change the computational relation, not merely the local predicate.

The first candidate is a hidden k-sheet graph cover.

Prior-art review found a direct cryptographic precedent:

- Seiya Negami, *Composite coverings of graphs and cryptography*, Yokohama Mathematical Journal 70 (2024; repository publication 2025), proposes a prototype **common-key** cryptosystem based on composite graph coverings.

This does not provide the public-key asymmetry MORPH needs, but it means "graph covering as cryptography" is itself established prior art.

H3-E0 formalizes a stronger public-key question.

A hidden canonical cover uses permutation voltages rho_e. Secret per-fiber labels phi_v disguise them as public transitions:

~~~text
T_uv = phi_v * rho_uv * phi_u^-1.
~~~

These public transitions are sufficient for anyone to lift a public path.

Attack H-E05 chooses a public spanning tree and gauge-fixes every tree transition to identity. Algebraically the resulting public normal form equals the hidden canonical cover up to a **single global conjugation by phi_root**.

Therefore the per-vertex fiber labels are not a trapdoor; they are gauge.

An executable calibration now checks:

- deterministic connected cover generation;
- full public tree normalization;
- equality to the hidden canonical cover up to one global conjugation;
- path-lift equivariance before/after the attack.

Fixed-seed CI confirmed the exact algebraic prediction:

~~~text
lift-12x5
  base V/E/cycle rank = 12/18/7
  sheets = 5
  tree transitions normalized = 11/11
  chord monodromies retained = 7
  point-operation estimate = 380
  canonical-cover equivalence up to root conjugation = yes
  path-lift equivariance = yes
  residual global sheet relabelings = 120 = 5!
~~~

**H3-E0 rejected.**

The secret per-fiber coordinate system is pure gauge. Once public transitions allow path lifting, the attacker obtains the same cover behavior in a public canonical gauge.

The only remaining ambiguity is one global sheet name permutation, which is irrelevant under equivalent-cover semantics.

A successor cannot use "hidden sheet labels" as the trapdoor.
