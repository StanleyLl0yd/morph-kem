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

**Assessment:** H2-H remains unresolved rather than broken. Four samples and bounded Python attacks are far below the evidence required for a cryptographic assumption.

Next mandatory attacks include industrial SAT/SMT/CP-SAT, subgroup/coset projections, representation-theoretic relaxations, automorphism/canonicalization exploitation, and substantially larger generated-distribution studies.


### H-H02 — exact MiniSat recovery

Target: the H2-H Klein-quartic/A5 generated relation.

The exact public relation was encoded to CNF with one Boolean variable for every vertex/A5-frame value. One global gauge representative is fixed at the root. Exactly-one constraints enforce one frame per vertex, and edge clauses encode the exact A5 3-cycle compatibility relation. The decoded solver model is checked again with the repository's exact verifier, so a SAT result is not accepted merely on the CNF encoder's word.

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
  CPU time:                 115.099 s
~~~

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

**Expected result:** fatal to K0 by construction.

K0 exists to verify that non-orientability and Möbius/Klein-bottle intuition do not become cryptographic hardness when the protected quantity is only an orientation character or face gauge.
