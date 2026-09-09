# 05 — Cryptanalysis ledger

This file preserves attacks including successful breaks.

| ID | Attack | Assessment | Status |
|---|---|---|---|
| A-000 | Direct public coordinate recovery | **Fatal to M0** | Implemented |
| A-001 | Greedy Morse reduction/matching | Persistent risk | Implemented |
| A-002 | Shared hidden-structure recovery | Critical risk | Pending generic attack |
| A-003 | Canonical labeling/isomorphism | High risk | M1 weakness documented |
| A-004 | SAT reconstruction | High risk | Pending |
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
