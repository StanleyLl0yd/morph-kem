# 18 — H2-E3 frontier review: Escher all-charts vs local OWF / planted CSP

## Status

**Decision: reject the naive H2-E3 construction before implementation.**

The intended Escher idea remains interesting:

> every public local chart remains present; each chart is locally simple; the attacker must find a globally coherent interpretation.

But once formalized as a hidden global state observed through many overlapping bounded-local predicates, the naive construction is not a new mathematical family. It is essentially a random/local-function or planted-CSP construction.

No cryptographic novelty or security claim is made.

## 1. Naive Escher all-charts notation

Let the hidden global state be

[
x=(x_1,ldots,x_n)in A^n
]

over a finite alphabet (A).

Let the public atlas contain (m) local neighborhoods

[
S_1,ldots,S_msubseteq[n],
qquad |S_j|=d=O(1).
]

Each chart publishes a bounded-local observation

[
y_j=P_j(x|_{S_j})
]

or, equivalently, a local relation

[
R_j(x|_{S_j},y_j)=1.
]

Inversion asks for any

[
x'
]

such that every public chart accepts:

[
R_j(x'|_{S_j},y_j)=1
quad	ext{for all }j.
]

That is the strongest "all charts remain" version considered after H2-E2.

## 2. Direct correspondence to Goldreich local functions

Goldreich's candidate one-way function uses:

- (n) hidden input bits;
- (m) public overlapping (d)-subsets / hyperedges;
- a fixed bounded-local predicate (P:{0,1}^d	o{0,1});
- output bits

[
y_j=P(x|_{S_j}).
]

This is exactly the same computational skeleton.

Reference:

- Oded Goldreich, *Candidate One-Way Functions Based on Expander Graphs*, ECCC TR00-090:
  https://eccc.weizmann.ac.il/eccc-reports/2000/TR00-090/index.html

Goldreich explicitly proposed overlapping small projections of the input, selected using combinatorial/expander structure, followed by a fixed local predicate.

Therefore the following change is **not** a novelty delta:

> replace random hyperedges by neighborhoods coming from an Escher drawing, hyperbolic tiling, Möbius complex, or other geometric embedding.

If evaluation is still a list of independent constant-local predicates on one hidden state, it remains a structured local-function instance.

## 3. Direct correspondence to planted CSP

Given the public outputs (y_j), inversion can be written as a CSP:

[
P_j(x|_{S_j})=y_j
]

for all (j).

The hidden (x) is a planted satisfying assignment.

This is precisely the planted-CSP viewpoint used in the literature on Goldreich functions.

Relevant prior art:

- Feldman, Perkins, Vempala, *On the Complexity of Random Satisfiability Problems with Planted Solutions*, SIAM J. Comput. 47(4), 2018:
  https://epubs.siam.org/doi/10.1137/16M1078471

That work gives statistical-query lower bounds for planted CSP distributions and explicitly discusses consequences for Goldreich's one-way-function candidate when the predicate has sufficiently high distribution complexity.

Important research discipline:

> worst-case NP-hardness of the local CSP is not enough, and even lower bounds against a broad algorithmic family do not prove one-wayness.

## 4. The field is active, not historical

A 2025/2026 result strengthens the connection between inversion and distinguishing for random local functions.

- Kel Zin Tan, Prashant Nalini Vasudevan, *Improved Search-to-Decision Reduction for Random Local Functions*, ECCC TR25-139, revised 2026:
  https://eccc.weizmann.ac.il/report/2025/139/

The reduction applies to random local functions defined by any constant-arity predicate, including noisy variants in part of the result.

Consequence for MORPH:

> "choose a more exotic bounded-local predicate" is not a sufficient research delta.

## 5. Concrete cryptanalysis that H2-E3 would inherit

Goldreich-style local generators have substantial dedicated cryptanalysis.

### Guess-and-determine / algebraic attacks

- Couteau, Dupin, Méaux, Rossi, Rotella, *On the Concrete Security of Goldreich's Pseudorandom Generator*, ASIACRYPT 2018 / ePrint 2018/1162:
  https://eprint.iacr.org/2018/1162

The work develops concrete guess-and-determine and algebraic attacks and studies predicate properties such as resiliency and algebraic immunity.

### Guess-and-decode

- Yang, Guo, Johansson, Lentmaier, *Revisiting the Concrete Security of Goldreich's Pseudorandom Generator*, IEEE Trans. Inf. Theory 2021:
  https://arxiv.org/abs/2103.02668

The paper substantially improves earlier attacks for several proposed predicates/parameter sets and introduces guess-and-decode methods exploiting sparse structure.

### Correlation attacks

More recent work continues to attack local predicates through correlation structure:

- *Bit-fixing Correlation Attacks on Goldreich's ...*, IACR ePrint 2024/1594:
  https://eprint.iacr.org/2024/1594

The exact predicate matters greatly. A geometric interpretation of the hypergraph does not remove these attack classes.

## 6. CSP / sheaf local-to-global viewpoint is also established

The Escher language "locally compatible charts, globally coherent section" is mathematically natural, but not new by itself.

Relevant work:

- Abramsky and Brandenburger, *The Sheaf-Theoretic Structure of Non-Locality and Contextuality*:
  https://arxiv.org/abs/1102.0264
- Adam Ó Conghaile, *Cohomology in Constraint Satisfaction and Structure Isomorphism*:
  https://arxiv.org/abs/2206.15253

The latter explicitly treats CSP as global-section existence and extends local (k)-consistency with cohomological obstruction methods.

Therefore:

> "our charts are locally consistent but globally difficult" is a research motivation, not a new hardness assumption.

## 7. Formal equivalence map

### Escher all-charts

~~~text
global hidden interpretation x
        |
        +--> chart S1 --> local observation y1
        +--> chart S2 --> local observation y2
        +--> ...
        +--> chart Sm --> local observation ym
~~~

### Goldreich/local function

~~~text
input x
        |
        +--> hyperedge S1 --> P(x|S1)
        +--> hyperedge S2 --> P(x|S2)
        +--> ...
        +--> hyperedge Sm --> P(x|Sm)
~~~

### Planted CSP inversion

~~~text
find x' such that
P_j(x'|Sj) = yj
for every j
~~~

Unless an H-series successor changes this computational skeleton, it belongs in the existing local-function/planted-CSP research landscape.

## 8. Changes that do NOT create meaningful novelty

The following alone are insufficient:

1. drawing the interaction hypergraph in hyperbolic geometry;
2. using a Möbius/non-orientable embedding;
3. replacing Boolean variables with a larger fixed alphabet;
4. replacing NAE with a different constant-arity predicate;
5. using a finite non-abelian group as the local alphabet;
6. increasing predicate locality by a small constant;
7. selecting neighborhoods from a ({p,q}) tiling rather than a random hypergraph;
8. adding a visual "impossible staircase" interpretation;
9. increasing parameters until SAT becomes slow;
10. calling the global assignment a "section", "lift", or "chart interpretation" while the verifier remains a bounded-local CSP.

These may produce interesting structured instances, but they do not by themselves define a new cryptographic foundation.

## 9. What would count as a meaningful H3-E delta

A successor should change at least one **computational** layer, not merely the representation.

### Delta A — topology-dependent trapdoor relation

Key generation creates public instances together with hidden topological/covering data such that:

- public forward evaluation remains efficient;
- the secret enables an operation not representable as merely evaluating local predicates on a hidden vector;
- equivalent witnesses remain accepted;
- recovering any useful equivalent secret is the attack problem.

The trapdoor must have a role stronger than "this is the planted satisfying assignment."

### Delta B — non-local evaluation semantics

At least some public output must depend on a genuinely global operation, for example:

- path lifting through a hidden cover;
- reduction to a canonical object using secret covering coordinates;
- composition of transition data along nontrivial homotopy classes;
- a global quotient/lift certificate.

If the output can be rewritten as (m) independent (O(1))-local predicates of (x), it fails this gate.

### Delta C — geometry changes the inversion problem

Hyperbolic/non-orientable geometry must alter the computational relation, not only the interaction graph.

A valid claim would need an explicit statement of the form:

> removing the geometric/covering structure changes algorithm X from polynomial / low-width to problem Y.

Without such an effect, geometry is decoration.

### Delta D — no small exceptional role class

H2-E1/E2 used defects/seams.

H3-E should avoid a small planted subset whose public statistics may reveal its role.

The public distribution should be role-symmetric enough that there is no obvious "these are the bad cells" attack.

## 10. Immediate H3-E attack surface

Any topology/covering based successor must be attacked first by:

1. canonical labeling / automorphism recovery;
2. graph-cover recognition and monodromy recovery;
3. fundamental-group / subgroup representation;
4. homology/cohomology linearization;
5. spanning-tree gauge fixing;
6. local-function flattening test;
7. CSP/SAT extraction;
8. bounded treewidth/separator decomposition;
9. deck-transformation/group-action recovery;
10. equivalent-cover / equivalent-witness search.

A secret cover is not assumed hidden merely because the public complex is large.

## 11. H2-E3 decision

**Naive H2-E3 is rejected before code.**

That is a successful research outcome.

The Escher idea has now taught three distinct lessons:

- **H2-E1:** one-dimensional local inconsistency becomes gain/cohomology cycle data.
- **H2-E2:** higher-order local charts plus deletable seams become a planted deletion-CSP.
- **H2-E3 naive:** all bounded-local charts with a hidden global state are already the Goldreich/local-function + planted-CSP paradigm.

The next experiment should not be another predicate search.

## 12. Proposed next track: H3-E Lifted Atlas

Working research question:

> Can a hidden finite covering/lifting structure provide a real trapdoor-like asymmetry that cannot be flattened to bounded-local predicates or recovered by standard covering/group algorithms?

This question is sufficiently different to justify a separate frontier milestone.

It must be literature/attack-model work before implementation.

## Security status

No one-wayness, post-quantum, IND-CPA, IND-CCA, or concrete-security claim exists.
