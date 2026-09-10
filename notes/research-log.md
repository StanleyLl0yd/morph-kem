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


### H3-E1 — composite-cover public-key adaptation frontier

Reviewed whether Negami-style composite graph-cover cryptography can be converted from a common-key mechanism into a public-key relation.

The obvious variants fail the public interface:

~~~text
publish common base/tree
    -> attacker gets decoder structure

hide common base/tree
    -> sender cannot run the original encoding

include H->G projection/voltage in ct
    -> attacker gets planted cover data

omit H->G projection
    -> both receiver and attacker face public cover-projection search
       and no secret-factorization trapdoor algorithm has been defined
~~~

Worst-case H-Cover NP-completeness does not fill this gap because cryptographic instances are generated positive instances and the required task is search, not arbitrary worst-case decision.

**H3-E1 rejected before code.**

Future cover-based work must begin with a complete trapdoor positive-distribution interface:

~~~text
(pk, td) <- CoverTrapdoorGen
(H, w)   <- SamplePositive(pk)
w'       <- TrapdoorRecover(td, pk, H)
~~~

with exact correctness and a public attack target.

Until TrapdoorRecover exists, there is no cover-based primitive to benchmark.


### H2-H — exact Klein quartic + A5 started

Returned to issue #17 after completing the Escher/covering frontier reviews.

This experiment finally uses an exact finite hyperbolic surface combinatorics rather than a cycle-rich graph surrogate.

Scaffold construction:

~~~text
GL(3,2) ~= PSL(2,7), order 168
(2,3,7) generators
vertex cosets: order-7 subgroup -> 24
edge cosets:   order-2 subgroup -> 84
face cosets:   order-3 subgroup -> 56
~~~

Required surface checks:
- 24 vertices;
- 84 edges;
- 56 triangular faces;
- degree 7 at every vertex;
- two faces at every edge;
- Euler characteristic -4;
- orientable genus 3;
- zero free collapse pairs.

The local state group is A5, order 60. The public accepted normalized edge subset is the 20-element conjugacy class of 3-cycles.

Unlike H1/S3, A5 has trivial abelianization; the implementation explicitly checks that the commutator subgroup is all 60 elements and that the 3-cycle class generates all A5.

This removes one known shortcut but does not imply hardness.

Attack H-H01 began as exact CSP with arc consistency and MRV, then expanded into a deliberately heterogeneous public attack stack.

Fixed-seed measured baseline:

~~~text
spectral:             49 violations
belief propagation:   17
min-conflicts:          3
weighted breakout:      1
pair repair:             1
tree-coordinate:         1

exact Hamming radius 0..6:
  no witness, search exhausted below per-radius cap

frozen neighborhood:
  radius 2 = all 24 vertices
  5000-node cap, no witness

exact CSP:
  1000-node cap
  300 singleton probes, 0 values removed
  no witness
~~~

A lighter deterministic four-instance generated-distribution sweep also found no accepted equivalent witness; best residual violations were 4, 3, 2, and 3.

**H2-H is unresolved, not rejected and not accepted as a security candidate.**

This is the first repository model where the implemented bounded public attacks fail to construct an accepted witness. The result is intentionally narrow: one strong fixed baseline plus four lighter samples.

Next work must attack the same relation with industrial SAT/SMT/CP-SAT, subgroup/coset projections, representation-theoretic methods, automorphism/canonicalization attacks, and broader generated-instance sampling. Parameter inflation is explicitly not the next step.


### H2.1 — industrial SAT break

The unresolved H2-H Klein-quartic/A5 relation was encoded exactly as CNF and attacked with MiniSat.

Fixed generated instance:

~~~text
variables = 1,440
clauses = 47,545
MiniSat result = SAT
decoded exact verifier = accepted
conflicts = 2,810,606
decisions = 6,909,361
propagations = 172,452,978
CPU time = 115.099 s
~~~

The solver used no planted reference witness. Any accepted equivalent A5 frame assignment counts as attacker success.

**H2-H rejected on the fixed generated instance.**

This is not an asymptotic hardness result; it is a concrete falsification of the current generated instance. The earlier bounded Python baseline was therefore attack-limited, not evidence of one-wayness.

Next H-series work must change the relation rather than inflate the Klein-quartic genus or the local finite group.


### K0 — Klein-bottle orientation control

Opened K0 as the first executable non-orientable calibration after the H2 Klein-quartic/A5 SAT break.

K0 uses an exact finite Klein-bottle triangulation with:

- closed 2D incidence;
- Euler characteristic 0;
- two triangles at every edge;
- a public Z2 orientation-transition cocycle on the dual graph.

Generation disguises the canonical transition bits with one reference gauge bit per face.

The mandatory attack is public spanning-tree XOR normalization. It should recover every hidden face gauge up to one global bit and leave only the gauge-invariant fundamental-cycle orientation syndromes.

K0 is expected to fail. The purpose is to prove in executable form that genuine non-orientability can still reduce to cheap linear gauge data.


K0 measured result:

~~~text
klein-bottle-5x4:
  V/E/F = 20/60/40
  chi = 0
  dual cycle rank = 21
  orientable = no
  non-zero fundamental orientation syndromes = 7/21
  public normalization = canonical normalization
  hidden face gauges recovered up to one global bit = yes
  public edge checks = 60

sweep:
  4x4 -> 6/17 non-zero syndromes, gauge recovered in 48 checks
  5x4 -> 7/21 non-zero syndromes, gauge recovered in 60 checks
  6x4 -> 8/25 non-zero syndromes, gauge recovered in 72 checks
~~~

**K0 rejected as designed.**

The non-orientable obstruction is real but public; hiding local orientation labels adds only gauge. This confirms that the K-series must not treat the orientation character itself as a trapdoor.


### K1 — non-orientable hyperbolic regular-map control

After K0's exact Z2 gauge break, K1 moves to a genuine non-orientable regular map of hyperbolic type rather than increasing the Klein-bottle mesh.

The chosen scaffold is N4:{6,4}_3:

~~~text
V/E/F = 6/12/4
chi = -2
non-orientable genus = 4
vertex degree = 4
face size = 6
underlying graph = K_{2,2,2}
~~~

The implementation derives its four hexagonal faces as Petrie cycles of the octahedral skeleton.

K1 keeps the deliberately weak orientation-gauge relation so the mandatory public attack can test two things:

1. spanning-tree recovery of all face gauges up to one global bit;
2. explicit reconstruction of the orientable two-sheet cover from public transitions.

The referenced orientable cover S3:{6,4} has expected V/E/F = 12/24/8 and genus 3.

K1 is expected to fail if those properties are recovered directly.


K1 measured result:

~~~text
N4:{6,4}_3
  base V/E/F = 6/12/4
  chi = -2
  hyperbolic regular type = yes
  orientable = no
  non-zero fundamental syndromes = 6/9
  hidden face gauges recovered up to one global bit = yes
  public edge checks = 12

orientation double cover:
  V/E/F = 12/24/8
  chi = -4
  orientable = yes
  genus = 3
  reconstructed from public transitions = yes
~~~

**K1 rejected as designed.**

This confirms that genuine hyperbolicity does not help when the computational relation remains ordinary Z2 orientation gauge. The next K-series step must change the relation itself rather than scale the same regular-map/orientation construction.


### K2.0 — orientation-twisted A5 semidirect calibration

After K1 showed that the orientation character and orientation double cover are public, K2.0 tests the first obvious non-abelian twist.

Local state is A5. Orientation-reversing edges act by the non-trivial outer automorphism of A5.

Prior-art/group facts give:

~~~text
Aut(A5) ~= S5
Out(A5) ~= C2
A5 semidirect C2 ~= S5
~~~

The implementation does not accept those identities only as literature facts. It exhaustively checks all 120 semidirect elements and all 14,400 products under the explicit map Phi(a,b)=a r^b.

It then generates a twisted A5 transport relation on exact N4:{6,4}_3 and checks every 60x60 endpoint-frame pair on every public dual edge against the flattened S5 predicate.

Measured K2.0 result:

~~~text
A5 ⋊ C2 elements = 120
S5 image elements = 120
all 14,400 products agree
orientation bit = S5 parity on all 120 elements

N4 twisted transport:
  public edges = 12
  endpoint assignments checked = 43,200
  predicate mismatches = 0
  edge parity/orientation matches = 12/12
  planted witness accepted in both representations
~~~

**K2.0 rejected algebraically.**

The orientation twist is not a new relation: at the 1-dimensional transport level it is exactly ordinary S5 semidirect completion.

K2.1 is therefore a literature/interface gate for crossed-module / finite-2-group transport rather than another immediate implementation.
