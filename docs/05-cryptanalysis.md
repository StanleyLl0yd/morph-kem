# 05 — Cryptanalysis ledger

This file preserves attacks including successful breaks.

| ID | Attack | Assessment | Status |
|---|---|---|---|
| A-000 | Direct public coordinate recovery | **Fatal to M0** | Implemented |
| A-001 | Greedy Morse reduction/matching | Persistent risk | Implemented |
| A-002 | Shared hidden-structure recovery | Critical risk | Pending generic attack |
| A-003 | Canonical labeling/isomorphism | High risk | M1 weakness documented |
| A-004 | Exact SAT/CNF reconstruction | **Fatal to H2-H fixed generated instance** | Implemented (MiniSat) |
| A-005 | MILP reconstruction | High risk | Pending |
| A-006 | Treewidth/separator methods | High risk | Pending |
| A-007 | Statistical/invariant distinguisher | High risk | Pending |
| A-008 | Meet-in-the-middle path recovery | **Fatal to M1** | Implemented |
| A-009 | Learned gadget recognition | Unknown/high | Pending |
| A-010 | Invalid-ciphertext/oracle leakage | Future KEM risk | Initial tests only |
| A-011 | Generic quantum search | Baseline | Analytical only |
| A-012 | Quantum walk/structure exploitation | Unknown | Pending |
| A-013 | Bounded public collapse DFS | Effective on small M2 | Implemented |
| A-014 | 3-regular hidden-core reconstruction | **Fatal to M2** | Implemented |
| A-015 | Alternative irreducible residuals | Structural result | Observed |
| A-016 | Collapse + spanning-tree witness | **Fatal to M3** | Implemented |
| A-017 | Generic greedy acyclic Hasse matching | Strong M3 baseline | Implemented |
| A-018 | Primal/dual tree-cotree witness | **Fatal to M4** | Implemented |
| A-019 | Tree-plus-extension equivalent Morse witness | **Fatal to M5 fixed generated baseline** | Implemented |
| A-020 | Independent Q8 boundary-fiber lifting | **Fatal to K2.2** | Implemented |
| A-021 | GF(2) kernel-coherence elimination | **Fatal to K2.3 relation family** | Implemented |
| A-022 | Short equivalent Pachner path + bidirectional recovery | **Fatal to T0 generator** | Implemented |
| A-023 | Exact-distance bidirectional Pachner recovery | **Fatal to T1 generated distribution** | Implemented |
| A-024 | Dual-graph canonical gluing recovery | **Fatal to G0 by design** | Implemented |

## M0–M3 summary

M0 leaks coordinate-local choices directly (A-000). M1's public reversible path is vulnerable to balanced meet-in-the-middle (A-008). M2 creates real collapse branching but leaks a simpler 3-regular core reconstruction problem (A-014), while A-015 shows the planted residual is not a privileged witness. M3 fixes equivalent-witness semantics, but graph-expanded complexes are constructively easy: collapse to any graph residual and complete a spanning-tree matching (A-016).

## A-018 — primal/dual tree-cotree equivalent witness

### Target

M4 closed triangulated torus family.

### Why M4 differs from M3

Every tested M4 edge has exactly two incident triangles and every tested target has zero free collapse pairs. The M3 collapse-to-graph attack is therefore unavailable.

### Attack

A-018 builds a primal spanning tree, matches non-root vertices with its edges, then builds a spanning tree in the triangle dual graph using primal edges outside the primal tree, and matches those edges with non-root triangles.

The combined witness is checked by the exact equivalent-witness validator.

For torus-4x4:

~~~text
V/E/F: 16/48/32
free collapse pairs: 0
critical target: (1,2,1)
primal/dual tree edges: 15/31
critical edges: 2
accepted: yes
randomized: 16/16 accepted, 16 unique
~~~

Fixed-seed sweep:

| Set | Simplices | Free pairs | Deterministic | Random | Unique |
|---|---:|---:|---:|---:|---:|
| torus-3x3 | 54 | 0 | yes | 32/32 | 32 |
| torus-4x4 | 96 | 0 | yes | 32/32 | 32 |
| torus-5x5 | 150 | 0 | yes | 32/32 | 32 |
| torus-6x6 | 216 | 0 | yes | 32/32 | 32 |
| torus-7x7 | 294 | 0 | yes | 32/32 | 32 |

Generic greedy matching on the torus-4x4 baseline hit the target 0/4 times, with best total critical count 6. Thus A-018 is a stronger structure-aware break.

**Result:** M4 rejected.

**Lesson:** genuine 2D structure and absence of free collapses do not imply equivalent-witness hardness; a simple global decomposition can still construct a witness.

## Persistent fatal-flaw classes

- generated/planted distribution leakage;
- local or global decomposition;
- equivalent-witness multiplicity;
- easy recognizable homotopy/structural class;
- shared hidden structure;
- low-width or solver-friendly Hasse structure.

Every future attack record should include the exact parameter set, seeds, work metric, outcome, and interpretation.

## H-series attacks

### H-A01 — Z2 spanning-tree / cycle-space recovery

H1-Z2 publishes a connected graph, edge bits, and a fundamental-cycle target.

Fixing one root gauge and propagating over a public spanning tree recovers an accepted equivalent witness in linear graph work. Non-tree labels are exactly the fundamental-cycle coordinates.

**Result:** H1-Z2 rejected as designed.

### H-A03 — S3 verifier factors through sign

H1-S3 accepts a candidate frame assignment when every normalized edge transition is a transposition.

In S3, the odd permutations are exactly the three transpositions. Therefore:

~~~text
normalized transition is a transposition
    iff
sign(normalized transition) = 1
~~~

and every edge constraint factors through the public homomorphism:

~~~text
S3 --sign--> Z2.
~~~

Solving the resulting Z2 graph equations recovers one parity per vertex up to a global flip. Choosing any fixed even S3 representative for parity 0 and any fixed transposition for parity 1 gives an accepted full S3 witness.

The implementation `recover_s3_via_abelianization` performs this construction.

Fixed-seed H1 sweep:

| Set | V | E | Cycle rank | Z2 recovered | S3 direct recovered | Direct edge checks | CSP nodes | CSP backtracks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| h1-8 | 8 | 12 | 5 | yes | yes | 36 | 16 | 0 |
| h1-10 | 10 | 15 | 6 | yes | yes | 45 | 18 | 0 |
| h1-12 | 12 | 18 | 7 | yes | yes | 54 | 20 | 0 |
| h1-16 | 16 | 24 | 9 | yes | yes | 72 | 24 | 0 |
| h1-20 | 20 | 30 | 11 | yes | yes | 90 | 28 | 0 |

The CSP column uses solution cap 8. It is included only as a calibration: H-A03 is strictly stronger and already gives a direct linear construction.

For the h1-12 CI baseline with CSP solution cap 64:

~~~text
V/E/cycle rank: 12/18/7
direct S3 recovery: accepted
direct edge checks: 54
CSP solutions found: 64
CSP nodes/backtracks: 104/0
CSP elapsed: ~0.017 s on the CI runner
~~~

Wall-clock time is environment-dependent and is not a complexity claim.

**Result:** H1-S3 structurally broken.

**Lesson:** choosing a non-commutative group does not help when the verifier accepts an entire fiber of a cheap quotient homomorphism.

### H-E01 — fundamental-cycle obstruction extraction

H2-E1 assigns a relative height increment in Z/7Z to every public edge. Fixing a public spanning tree determines vertex potentials. Every non-tree edge then exposes one fundamental-cycle syndrome.

For the abelian height model, these cycle gains are a complete test for global consistency: the atlas is balanced iff all fundamental-cycle syndromes vanish.

**Result:** exact structural reduction confirmed.

Fixed-seed H2-E1 shows non-zero fundamental-cycle syndromes immediately expose the complete no-seam obstruction.

### H-E02 — unbalanced-cycle seam branching

H2-E1 accepts any seam set of size at most the public budget whose removal leaves a globally integrable height atlas.

The exact public attack repeatedly:

1. propagates vertex potentials on the current non-seam graph;
2. extracts one inconsistent cycle when propagation conflicts;
3. observes that every valid repair must remove at least one edge of that cycle;
4. branches on those cycle edges and memoizes deleted-edge sets.

This is equivalent in spirit to balancing-set / Group Feedback Edge Set attacks on gain/group-labelled graphs.

**Result:** fatal to H2-E1 as a new hardness direction.

Fixed-seed Python 3.12 CI sweep:

| Set | V | E | Cycle rank | Budget | Non-zero syndromes | Minimum seams | Search nodes | Backtracks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| escher-8 | 8 | 12 | 5 | 1 | 4 | 1 | 4 | 2 |
| escher-10 | 10 | 15 | 6 | 2 | 2 | 2 | 27 | 24 |
| escher-12 | 12 | 18 | 7 | 2 | 5 | 2 | 27 | 24 |
| escher-16 | 16 | 24 | 9 | 3 | 6 | 3 | 43 | 39 |
| escher-20 | 20 | 30 | 11 | 4 | 4 | 3 | 164 | 160 |

The escher-20 attack found an accepted equivalent repair using only 3 seams even though the generator planted 4. This reinforces the repository rule that attacker success is any accepted witness, not recovery of generation history.

For escher-12 the exact attack required 27 search nodes, 24 backtracks and 469 public edge checks.

H2-E1 is therefore rejected. The relation is an instance of known gain/group-labelled graph balancing/cycle-hitting structure; increasing graph size does not repair the conceptual issue.

### H-E03 — exact higher-order NAE atlas repair

H2-E2 moves from edge gains to 3-variable local charts. Every chart uses a signed Not-All-Equal relation on three Boolean variables.

The public verifier accepts any global assignment plus any chart-seam set within budget such that every retained chart is satisfied.

Attack H-E03 minimizes the number of violated charts over global assignments using exact branch-and-bound:

- global complement symmetry fixes one variable;
- variables are ordered by chart incidence;
- partial assignments use an admissible lower bound from already violated charts and conflicting one-variable NAE requirements;
- the leaf violation set is itself an accepted equivalent seam set.

This is a standard CSP/Max-CSP style attack, not a novel cryptanalytic algorithm.

**Result:** fatal to H2-E2 as a candidate direction.

Fixed-seed Python 3.12 CI sweep:

| Set | Variables | Charts | Budget | Pairwise compatible | Minimum seams | Nodes | Backtracks | Planted seam signatures also seen among normal |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| atlas-8 | 8 | 18 | 1 | yes | 1 | 43 | 21 | 1/1 |
| atlas-10 | 10 | 24 | 1 | yes | 1 | 41 | 20 | 0/1 |
| atlas-12 | 12 | 30 | 2 | yes | 1 | 37 | 18 | 0/2 |
| atlas-14 | 14 | 36 | 2 | yes | 1 | 73 | 36 | 0/2 |
| atlas-16 | 16 | 42 | 3 | yes | 1 | 281 | 138 | 1/3 |

For atlas-12 all 435 chart pairs are jointly satisfiable, but an accepted equivalent global repair needs only one seam chart and is proven minimum in 37 search nodes.

Two independent failures are visible:

1. the equivalent-witness optimization is extremely easy on this planted distribution;
2. the simple public signature (negation count + variable incidence degrees) uniquely separates every planted seam in atlas-10, atlas-12 and atlas-14.

**H2-E2 rejected.**

Worst-case NAE-3SAT hardness does not rescue a generated distribution that is both solver-friendly and statistically role-leaking.

### H-E04 — local-function flattening

Target: any proposed all-charts Escher construction.

Test whether the public evaluator can be written as:

[
y_j=P_j(x|_{S_j})
]

with bounded (|S_j|) and one hidden global state (x).

If yes, the proposal is classified as a structured random/local function and planted CSP rather than a new MORPH hardness family.

**Result for naive H2-E3:** complete flattening.

The proposed "all charts remain" construction maps directly to Goldreich's local-function skeleton. Geometry changes the neighborhood distribution, but not the inversion relation.

**Disposition:** naive H2-E3 rejected before code.

Mandatory successor gate: any H3-E construction must demonstrate a public operation/witness relation that cannot be flattened to independent bounded-local predicates of one hidden vector.

### H-E05 — public spanning-tree gauge normalization

Target: H3-E0 lifted-atlas calibration.

Suppose a k-sheet cover over a connected public base graph is described by public edge permutations T_uv in S_k. A secret fiber relabeling is a vertex gauge phi_v.

If enough T_uv are public for an untrusted sender to lift arbitrary public paths, an attacker can choose any public spanning tree and compute vertex gauges h_v so every tree transition becomes identity.

For a tree-normalized hidden cover rho and public disguise:

~~~text
T_uv = phi_v * rho_uv * phi_u^-1
~~~

the public normalization gives:

~~~text
T'_uv = h_v * T_uv * h_u^-1
      = phi_root * rho_uv * phi_root^-1.
~~~

Thus the entire hidden per-vertex gauge collapses to one global sheet conjugation.

A global sheet relabeling is an equivalent covering representation, not a useful trapdoor under equivalent-witness semantics.

Complexity is linear in the public base graph size times the sheet permutation size.

**Result:** fatal to hidden fiber labels as an H3-E trapdoor.

Fixed-seed Python 3.12 CI baseline:

~~~text
parameter: lift-12x5
base V/E/cycle rank: 12/18/7
sheets: 5
tree transitions normalized: 11/11
public chord monodromies retained: 7
point-operation estimate: 380
equal to hidden canonical cover up to one global conjugation: yes
path-lift equivariance preserved: yes
residual root relabelings: 120 = 5!
~~~

The 120 residual choices are a single global relabeling of the five sheets. They describe equivalent coverings and therefore do not constitute a trapdoor.

**H3-E0 rejected.**

### H-E06 — composite-cover public-key interface collapse

Target: naive adaptation of Negami-style composite graph-cover cryptography.

Four variants were checked:

1. publish the base/tree used for common-key decoding -> attacker receives the same decoding structure;
2. keep base/tree secret -> original sender algorithm is no longer public;
3. include the planted outer covering projection in ciphertext -> attacker receives sender recovery data;
4. omit the projection -> receiver and attacker face the public search relation "find any H -> G covering projection", and no trapdoor recovery algorithm from a hidden lower factorization has been defined.

**Result:** naive H3-E1 rejected before code.

This is an interface failure, not a proof that every cover-based public-key primitive is impossible.

Mandatory successor gate: define an efficient TrapdoorRecover algorithm on an exact generated positive cover distribution before claiming a cover-based one-way relation.

### H-H01 — exact A5 frame CSP on Klein quartic

Target: H2-H exact {3,7} Klein-quartic scaffold.

The public surface is not a graph-only hyperbolic analogy. It is built combinatorially from the order-168 (2,3,7) quotient using cosets of the cyclic subgroups of orders 7, 2, and 3.

The transition group is A5. Its 3-cycle conjugacy class has 20 elements and A5 is perfect, so H1's cheap abelian sign quotient is absent.

The public relation remains pairwise:

~~~text
x_v * T_uv * x_u^-1 in C3(A5)
~~~

for every public edge.

Attack H-H01 uses exact finite-domain CSP with:
- one global gauge representative fixed;
- exact edge compatibility tables;
- repeated arc consistency;
- MRV + public incidence degree tie-breaking;
- equivalent-witness enumeration.

**Assessment:** implemented; the bounded exact baseline does not recover a witness on the fixed instance.

Fixed-seed result with the full current attack pipeline:

~~~text
spectral violations:             49
belief-propagation violations:   17
min-conflicts best:               3
weighted breakout best:           1
pair repair best:                 1
tree-coordinate best:             1

Hamming repair radius 0..6:
  accepted: no
  nodes/backtracks: 1767/1774

neighborhood repair:
  radius 2 mutable vertices: 24/24
  5000-node cap, no witness

exact CSP:
  1000 nodes / 996 backtracks
  300 singleton probes
  0 singleton values removed
  no witness
~~~

The Hamming-ball searches through radius 6 exhausted below their per-radius node cap. Therefore no accepted solution exists in those tested Hamming balls around the one-violation public heuristic assignment, assuming correctness of the exact validator/search implementation.

This is a bounded exact result on one generated instance, not a hardness proof.

### H-H02 — coordinated heuristic synchronization attacks

To avoid mistaking weakness of one solver for hardness, H2-H also includes several structurally different public attacks:

- natural 5-point spectral synchronization;
- sum-product belief propagation;
- min-conflicts over A5 vertex frames;
- weighted breakout on violated edges;
- exhaustive two-vertex repair near violated edges;
- spanning-tree transition coordinates where 23 tree constraints are satisfied by construction and only 61 chord constraints remain.

The strongest fixed-seed heuristic reaches one violated edge but does not cross the final barrier.

**Assessment:** no accepted witness under the measured bounded settings.

### H-H03 — generated-instance mini-sweep

A deterministic four-instance sweep uses lighter attack budgets to test whether the fixed baseline is anomalously difficult.

| Instance | BP | Local | Breakout | Tree-coordinate | Hamming hit | CSP hit | Best violations |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0 | 17 | 4 | 4 | 4 | no | no | 4 |
| 1 | 23 | 3 | 3 | 3 | no | no | 3 |
| 2 | 30 | 3 | 2 | 2 | no | no | 2 |
| 3 | 16 | 3 | 3 | 3 | no | no | 3 |

Each mini-sweep CSP is capped at 250 search nodes and 50 singleton probes. No singleton probe removes a value on these four instances.

**Assessment:** H2-H remains unresolved rather than broken under these bounded Python attacks. Four samples and bounded attacks are far below the evidence required for a cryptographic assumption.

### H-H04 — exact MiniSat recovery

Target: the H2-H Klein-quartic/A5 generated relation.

The exact public relation was encoded to CNF with one Boolean variable for every vertex/A5-frame value. One global gauge representative is fixed at the root. Exactly-one constraints enforce one frame per vertex, and edge clauses encode the exact A5 3-cycle compatibility relation. The decoded solver model is checked again with the repository's exact verifier.

Fixed generated instance:

~~~text
Klein vertices / edges / faces: 24 / 84 / 56
A5 domain size:                 60
SAT variables:                 1,440
SAT clauses:                  47,545

MiniSat:
  result:                       SAT
  decoded accepted witness:     yes
  conflicts:              2,810,606
  decisions:              6,909,361
  propagations:         172,452,978
~~~

Recorded CPU time varies by CI runner; the exact SAT witness is the result that matters.

The attack uses only public instance data. Any accepted equivalent frame assignment is attacker success; the planted reference frames are not used by the solver.

**Result:** H2-H is rejected for this generated relation/instance. The previous bounded Python attacks stopping at one violated edge were only a limitation of those attack implementations.

This does not prove a polynomial-time attack or characterize asymptotic complexity. It is nevertheless enough to falsify the current generated instance as a cryptographic hardness candidate under the repository's attack-first rules.

**Lesson:** removing abelianization and moving to an exact hyperbolic surface can make naive search much harder without creating a usable one-way relation. Industrial exact solvers must be part of the gate before interpreting bounded heuristic failure.

### K-A01 — Klein-bottle orientation gauge recovery

Target: K0 non-orientable orientation-atlas control.

For every dual edge between faces f and g, the public scaffold determines a canonical orientation-transition bit b_fg. Generation hides it only by face gauge bits:

~~~text
T_fg = b_fg XOR phi_f XOR phi_g.
~~~

Therefore:

~~~text
T_fg XOR b_fg = phi_f XOR phi_g.
~~~

A public dual spanning tree recovers all face gauges relative to one root bit. Equivalently, tree-gauge normalization removes every secret per-face label and leaves exactly the canonical cycle-obstruction data.

The non-tree normalized bits are the fundamental-cycle orientation syndromes. Their non-zero values certify that the local orientation equations cannot be made globally consistent, but they are public linear data rather than a trapdoor.

Fixed-seed K0 CI sweep:

| Set | V | E | F | Dual cycle rank | Non-zero syndromes | Gauge recovered | Edge checks |
|---|---:|---:|---:|---:|---:|---:|---:|
| klein-bottle-4x4 | 16 | 48 | 32 | 17 | 6 | yes | 48 |
| klein-bottle-5x4 | 20 | 60 | 40 | 21 | 7 | yes | 60 |
| klein-bottle-6x4 | 24 | 72 | 48 | 25 | 8 | yes | 72 |

For the baseline klein-bottle-5x4 instance, public normalization exactly equals canonical normalization and every hidden face gauge is recovered relative to the root face. The only ambiguity is the expected common global XOR bit.

**Result:** K0 rejected exactly as designed.

**Lesson:** a genuine non-orientable surface and non-zero global orientation obstruction do not imply cryptographic hardness. If the hidden information is only local orientation gauge, the public relation is linear Z2 synchronization.

### K-A02 — public orientation-double-cover reconstruction

Target: K1 exact non-orientable hyperbolic regular-map control.

The base map is N4:{6,4}_3 with V/E/F = 6/12/4, Euler characteristic -2 and regular type {6,4}. The public face-orientation transitions define a two-sheet orientation cover directly.

For every dual edge f--g with public transition T_fg, the attack glues local sheet copies by:

~~~text
(f, s) <-> (g, s XOR T_fg).
~~~

This requires no hidden reference face gauge.

The same public transition data also gives the K0-style linear recovery:

~~~text
T_fg XOR b_fg = phi_f XOR phi_g.
~~~

Thus the hidden face gauges collapse to one global bit, while the public cover exposes the orientable lift.

Fixed-seed K1 CI result:

~~~text
map: N4:{6,4}_3
base V/E/F:                         6/12/4
base vertex degree:                 4
base face size:                     6
base edge-face degree:              2
base Euler characteristic:         -2
base dual cycle rank:               9
regular type hyperbolic:            yes
base orientable:                    no
non-zero orientation syndromes:     6/9
public normalization = canonical:   yes
hidden face gauges recovered:       yes, up to one global bit
public gauge edge checks:           12

orientation cover V/E/F:            12/24/8
orientation cover chi:              -4
orientation cover orientable:       yes
orientation cover genus:            3
reconstructed from public data:     yes
~~~

**Result:** K1 rejected exactly as designed.

**Lesson:** passing from the Klein bottle to a genuine non-orientable hyperbolic regular map does not create asymmetry when the protected object still factors through the orientation character. The orientation double cover is a public construction from the same transition data.

### K-A03 — semidirect-product completion of twisted A5

Target: K2.0 orientation-twisted A5 local system.

Let the public orientation bit act on A5 through the non-trivial outer automorphism induced by conjugation with a fixed odd permutation r in S5.

Then the twisted transport law is:

~~~text
(a,b)(c,d) = (a alpha^b(c), b XOR d).
~~~

The map:

~~~text
Phi(a,b) = a r^b
~~~

is tested exhaustively against S5 multiplication.

If Phi is bijective and homomorphic, every orientation-twisted pairwise A5 transport is exactly one ordinary S5 transport. The public orientation bit is simply the permutation parity.

K2.0 additionally checks every endpoint-frame pair on every N4:{6,4}_3 dual edge to ensure that the twisted verifier and flattened S5 verifier agree exactly.

Fixed-seed K2.0 CI result:

~~~text
semidirect elements:                  120
S5 image elements:                    120
bijective:                             yes
homomorphic:                           yes
multiplication checks:              14,400
orientation/parity checks:             120
orientation component = S5 parity:    yes

N4:{6,4}_3:
  V/E/F = 6/12/4
  orientable = no
  non-zero orientation syndromes = 6/9

twisted relation:
  public dual edges = 12
  endpoint assignments checked = 43,200
  relation mismatches = 0
  public edge parity matches orientation = 12/12
  planted twisted witness accepted = yes
  same witness under S5 flattening = yes
~~~

**Result:** K2.0 rejected algebraically.

The failure is exact, not a solver timeout or small-parameter observation. Every tested pairwise orientation-twisted A5 edge predicate is the same predicate written inside S5 after semidirect completion.

**Lesson:** outer twisting by the orientation character does not evade ordinary finite-group transport. A successor must add genuinely 2-dimensional data rather than a more complicated one-group-per-edge notation.

### K-A04 — crossed-module kernel/cokernel and gauge projection

Target: any proposed K2.1/K2.2 finite crossed-module construction.

For a crossed module partial:E->G:

~~~text
pi1 ~= coker(partial)
pi2 ~= ker(partial)
~~~

with ker(partial) abelian and im(partial) normal.

This gives an immediate structural attack hierarchy:

- partial injective -> pi2 vanishes; reduce first to ordinary quotient/group structure;
- partial surjective -> pi1 vanishes; the remaining higher homotopy layer is abelian;
- partial an isomorphism -> represented 2-type is trivial;
- general case -> expose ker, coker, the induced action and the Postnikov/cohomological layer before treating the presentation as a new hard problem.

A hidden 1-gauge/2-gauge representative is not accepted as a trapdoor because equivalent gauges are attacker success.

**Result:** naive K2.1 "hide a crossed-module gauge" rejected before code.

Sources and details are recorded in `docs/25-k2-crossed-module-frontier.md`.

## A-019 — M5 public tree-plus-extension equivalent witness

Target: M5 irregular non-manifold triangular 2-core.

M5 deliberately removes both the M3 free-collapse shortcut and the M4 closed-manifold structure. On the fixed baseline:

~~~text
V/E/F:                         8/27/29
edge triangle incidence:       2..6
free collapse pairs:           0
critical target:               (1,0,9)
~~~

A public multi-start tree/triangle greedy already finds two distinct accepted target matchings in 32 trials. More decisively, `bounded_tree_extension_search` fixes a public spanning-tree vertex/edge matching and exactly branches over remaining edge/triangle matching choices.

Measured Python 3.12 CI:

~~~text
accepted equivalent witness:   yes
search nodes:                   30
spanning-tree trials:           1
search exhausted:               no
~~~

No planted reference information is used.

**Result:** M5 rejected on the fixed generated baseline.

This is a generated-distribution falsification, not an asymptotic theorem. It is enough to reject parameter inflation as a repair.

## A-020 / K-A05 — Q8 independent public face lifting

Target: K2.2 automorphism crossed module `partial: Q8 -> Aut(Q8)`.

The exact crossed-module audit gives:

~~~text
|Q8| = 8
|Aut(Q8)| = 24
|ker(partial)| = 2
|im(partial)| = 4
|coker(partial)| = 6
~~~

On exact `N4:{6,4}_3`, every public face holonomy lies in `im(partial)`. Each such boundary has exactly two Q8 preimages, a coset of `ker(partial) ~= C2`.

The public attack computes every face holonomy and independently chooses any preimage. For four faces:

~~~text
fiber sizes:                    (2,2,2,2)
equivalent witnesses:           16
edge compositions:              24
Q8 preimage checks:             32
accepted equivalent witness:    yes
same as planted representative: no
~~~

**Result:** K2.2 rejected exactly for fake-flatness alone.

**Lesson:** placing independent witness variables on faces does not create higher-order asymmetry when verification factorizes into independent boundary-preimage tests.

## A-021 / K-A06 — affine GF(2) kernel-coherence collapse

Target: K2.3 three-dimensional successor to K2.2.

After selecting one public canonical lift `h_f^0` in each two-element Q8 boundary fiber, any other valid lift is uniquely

~~~text
h_f = (-1)^z_f h_f^0,
z_f in GF(2).
~~~

The implemented tetrahedral coherence predicate multiplies these central kernel choices around each 3-cell. Consequently the entire residual witness relation is exactly

~~~text
A z = b  over GF(2).
~~~

The public attack row-reduces this system and lifts any solution back to Q8.

Fixed-seed Python 3.12 CI on the boundary of a 4-simplex:

~~~text
V/E/F/T:                        5/10/10/5
boundary fiber sizes:           ten copies of 2
equations / variables:          5 / 10
rank / nullity:                 4 / 6
dependent equations:            1
row XOR operations:             7
equivalent witnesses:           64
public attack accepted:         yes
same as planted representative: no
elapsed:                        0.000111 s
~~~

The row dependency is structural: every triangular face belongs to two tetrahedra, so the XOR of all five tetrahedral incidence rows is zero.

**Result:** K2.3 rejected exactly for this relation family.

This is stronger than a toy-runtime result. For any larger instance that keeps the same semantics — public two-element central-kernel fibers plus coherence given by products of their `C2` choices — witness recovery remains affine binary linear algebra. Increasing the complex size only increases the public linear system.

This does **not** show that every higher-topological cryptosystem is linear or impossible. It shows that the next hard component, if one exists, cannot live solely in the abelian `pi2`/kernel cochain. A successor must expose a genuinely coupled unknown `pi1`/`pi2` or other trapdoor distribution and still survive cohomology, finite-module, gauge, group-synchronization, canonicalization and CSP/SAT attacks.

## A-022 — short equivalent Pachner path and bidirectional recovery

Target: T0 Bounded Topological Transformation Search calibration.

T0 removes several earlier artificial weaknesses: the legal move set is state-dependent, the branching factor is not fixed, vertex labels are quotiented by exact toy canonicalization, and attacker success is any path within the public bound.

Nevertheless the generated challenge walk does not control true distance in the quotient reconfiguration graph.

Fixed-seed Python 3.12 exact-head CI:

| Set | Planted | BFS distance | BFS visited | BFS expanded | Bidir distance | Bidir F/R visited | Bidir expanded | Mean unique branching | Commuting fraction |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| t0-4 | 4 | 4 | 154 | 47 | 4 | 40/55 | 13 | 15.250 | 0.028319 |
| t0-6 | 6 | 6 | 588 | 316 | 6 | 149/187 | 75 | 18.667 | 0.019201 |
| t0-8 | 8 | **4** | 170 | 51 | **4** | 40/65 | 13 | 20.000 | 0.009336 |

Detailed `t0-8` baseline:

~~~text
start vertices/tetrahedra:      9/17
target vertices/tetrahedra:     9/21
planted length/public bound:    8/8
planted moves 2-3 / 3-2:        6/2
branching initial/min/mean/max: 12/12/21.12/28
neighbor collisions:            9
commuting move pairs:           17/1821
BFS shortest path:              4
bidirectional shortest path:    4
bidirectional expansions:       13
recovered witness valid:        yes
~~~

**Result:** T0 generator rejected.

This is not a theorem that bounded Pachner search is easy in general. It is a generated-distribution falsification: an eight-step planted challenge has a four-step public equivalent witness, and bidirectional search recovers it after expanding only 13 quotient states.

The low commuting fraction also matters: the break is not explained by a trivial decomposition into mostly independent commuting moves. The more basic defect is that random non-self-repeating walks can return close to the start or target through alternate quotient paths.

**Lesson:** planted walk length is not a hardness parameter. A successor must control or measure actual quotient distance, short-path multiplicity, and bidirectional frontier growth before any path length is interpreted as security evidence.

## A-023 — exact-distance bidirectional Pachner recovery

Target: T1 exact-distance-conditioned BTTS/Pachner calibration.

T1 removes T0's endpoint-distance defect. It constructs complete canonical quotient BFS shells and samples a target from the exact shell `S_D`. Within that shell, generation first maximizes slack against the public tetrahedron-count lower bound and then minimizes capped shortest-path multiplicity, so the calibration does not deliberately choose an obviously easy target.

Fixed-seed Python 3.12 exact-head CI:

| Set | D | Shell sizes | Ball | Target delta/slack | Shortest paths | Shortest predecessors | Bidir F/R visited | Bidir expanded | A* visited/expanded |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| t1-2 | 2 | 1/8/31 | 40 | 0/2 | 1 | 1 | 9/4 | **2** | 21/2 |
| t1-3 | 3 | 1/8/31/83 | 123 | 1/2 | 1 | 1 | 9/14 | **5** | 119/36 |

Detailed `t1-3` baseline:

~~~text
exact distance/public bound:        3/3
ball size/shell-build expanded:      123/40
raw moves/unique neighbors:         639/420
local neighbor collisions:          219
revisit hits:                       298
target tetrahedron delta/slack:     1/2
max-slack candidates:               14
min-path finalists:                 1
shortest paths/predecessors:        1/1
BFS visited/expanded:               119/36
bidirectional F/R visited:          9/14
bidirectional expanded:             5
tetrahedron A* visited/expanded:    119/36
recovered witness valid:            yes
~~~

The target is genuinely at distance 3, has a unique measured shortest path, and is deliberately poorly predicted by tetrahedron count: that lower bound is only 1 while the exact distance is 3. Nevertheless generic bidirectional search recovers the target after expanding only five quotient states.

**Result:** T1 generated distribution rejected.

This triggers the pre-declared T1 rejection condition that bidirectional search remains tiny at exact-distance-conditioned targets. Exact-distance conditioning fixes the specific T0 generator bug but does not provide evidence of generated-instance hardness.

Do not add `D=4` merely to inflate the work factor. This is not a theorem that bounded Pachner reconfiguration is easy and does not contradict worst-case NP-hardness for related move problems. It is a falsification of the current generated distribution as a cryptographic hardness direction.

Because a cheaper mandatory attack already triggers rejection, the heavier bounded SAT/CP-SAT/planning gate is not required to reject T1. It remains mandatory for any future BTTS distribution that first survives the cheap exact and bidirectional gates.

## A-024 — dual-graph canonical gluing recovery

Target: G0 HGES canonical-gluing negative control.

G0 publishes a quotient complex formed by gluing copies of one punctured-4-simplex 3-ball along a hidden tree. The planted piece partition, assembly tree, local boundary ports and local labels are not public.

Each piece contributes four tetrahedra whose internal tetrahedron-dual graph is `K4`. Every planted inter-piece shared triangular face contributes exactly one dual-graph edge. Because the assembly graph is a tree, those inter-piece dual edges are bridges, while no internal `K4` edge is a bridge.

A-024 uses only public tetrahedron incidence:

1. enumerate every triangular-face occurrence;
2. build the public tetrahedron dual graph;
3. compute all bridges with DFS low-link values;
4. remove those bridges;
5. return the resulting connected components as the candidate piece partition;
6. verify that partition with the exact public G0 verifier.

Fixed Python 3.12 exact-head baseline:

~~~text
parameter:                              g0-8
pieces:                                 8
public V/E/F/T:                         19/59/73/32
Euler characteristic:                  1
boundary faces / max face incidence:   18/2
dual graph vertices / edges:           32/55
dual bridges:                           7
bridge component sizes:                (4,4,4,4,4,4,4,4)
face occurrence checks:                 128
DFS edge scans:                         110
public bridge witness accepted:         yes
matches planted partition up to order: yes
~~~

The Python 3.12 sweep covers `g0-3`, `g0-5`, and `g0-8` over eight independently derived deterministic seeds each. All **24/24** public bridge recoveries are accepted and all **24/24** match the planted partition up to group order.

Per-size work counters are deterministic for the current family:

| Set | Pieces | Dual edges | Bridges | Face occurrences | DFS scans | Accepted/matched |
|---|---:|---:|---:|---:|---:|---:|
| g0-3 | 3 | 20 | 2 | 48 | 40 | 8/8 |
| g0-5 | 5 | 34 | 4 | 80 | 68 | 8/8 |
| g0-8 | 8 | 55 | 7 | 128 | 110 | 8/8 |

**Result:** G0 rejected as designed.

The attack is structural, not a small wall-clock accident. For the whole tree-of-`K4` family, every inter-piece gluing remains a dual-graph bridge, so ordinary linear-time bridge decomposition reconstructs the assembly blocks regardless of the hidden gluing permutations and global vertex relabeling.

This does not show that general HGES is easy. It validates the intended canonical-decomposition attack harness and establishes the minimum condition for G1: changing only the number of pieces is not a repair. A successor must eliminate the bridge separator structurally and then survive articulation/low-order separator, allowed-piece enumeration, automorphism normalization, boundary-signature and exact-cover/SAT/CP-SAT attacks.
