# 99 — BPT-R1 Pachner corpus reconciliation and re-entry decision

## Status

**NO NOMINATION.**

BPT-R1 finds no bounded-Pachner-transport distribution that currently clears the MORPH-R0 re-entry gate. No successor implementation is justified yet.

This is a research/rejection memo. It does not claim one-wayness, average-case hardness, post-quantum hardness, a trapdoor, KEM, IND-CPA/CCA security, or production suitability.

The immediate reason is twofold:

1. the repository has already falsified the obvious generated `2-3 / 3-2` Pachner-search families in T0 and T1; and
2. the 2026 worst-case NP-hardness construction of Tillmann–Tsvietkova uses a more general topological-triangulation representation and obtains hardness by a Karp reduction from a modified planar Hamiltonian-path problem. Directly implementing that reduction family would therefore not supply a new MORPH hardness source.

BPT-W0 remains useful: it validates that the new BPT verifier/attack harness rejects an intentionally simplifiable family. It does not reopen T0/T1 or convert worst-case NP-hardness into cryptographic evidence.

## 1. Prior Pachner corpus is inherited, not superseded

### T0 / A-022

`docs/30-t0-bounded-pachner-spec.md` already defines the central relation that an obvious BPT successor would otherwise recreate:

```text
Public:  (R0, R1, L)
Moves:   legal 2-3 / 3-2 Pachner moves
Success: any path of length <= L ending at a state isomorphic to R1
State:   quotient-canonical under vertex relabeling
```

The exact measured T0 result in `docs/33-t0-pachner-results.md` is fatal to that generator. In the fixed `t0-8` case, generation plants a non-self-repeating eight-move path but the true public quotient distance is four. Bidirectional recovery expands only 13 states.

Therefore planted path length is already known not to be a useful hardness parameter for this family.

### T1 / A-023

T1 repairs the immediate T0 generator defect by constructing exact quotient BFS shells and selecting targets with certified shortest distance. That still does not create meaningful measured resistance.

The fixed `t1-3` target is genuinely at distance three, has one measured shortest path and is deliberately weakly predicted by tetrahedron-count difference. Nevertheless bidirectional recovery expands only five quotient states.

The declared T1 rejection gate therefore fired. `t1-4` was intentionally not added merely to inflate the work factor.

### BPT consequence

The following are now permanent inherited attacks/controls for every BPT proposal:

- exact canonical quotienting;
- BFS on toy move graphs;
- bidirectional BFS;
- admissible A*/IDA* where a valid lower bound exists;
- path multiplicity / predecessor counting;
- state-collision accounting;
- move-interaction / commuting-region analysis;
- shorter-path search independent of the planted history.

A BPT proposal that is only “T0/T1 at larger depth” is rejected before code by the no-parameter-rescue rule.

## 2. BPT-W0 calibration result

BPT-W0 uses stacked `S^3` triangulations generated only by `1-4` moves. The public attack greedily applies legal `4-1` moves to both endpoints and splices the resulting paths through a recovered public isomorphism between the simplified roots.

The first implementation exposed a useful harness bug: greedy simplification can legally remove an original root vertex, so the two five-tetrahedron roots need not have identical labels. Requiring literal root equality contradicted the public verifier, which accepts target equality only up to combinatorial isomorphism.

After correcting the attack to transport the inverse target path through an exact public root isomorphism, the declared weak control is rejected on 24/24 instances. The fixed depth-three baseline has at least 96 accepted simplification/splice paths, and the recovered path differs from the planted path.

This establishes only that the BPT harness respects equivalent-witness and isomorphism semantics. It is a calibration success through candidate failure.

See `docs/98-bpt0-stacked-s3-weak-control.md`.

## 3. The 2026 theorem is about a broader representation

Tillmann and Tsvietkova define a closed 3-manifold triangulation from a disjoint union of Euclidean tetrahedra together with affine face pairings, followed by taking the quotient. The resulting vertices, edges, faces and tetrahedra can have self-identifications along their boundaries.

Reference:

- S. Tillmann, A. Tsvietkova, *Moving between 3-manifold triangulations is NP-hard*, arXiv:2606.14413 (2026), especially Sections 1–3: https://arxiv.org/abs/2606.14413

This is materially more general than MORPH's current `SimplicialComplex` representation.

`src/morph_kem/complex.py` stores each simplex as a sorted tuple of distinct global vertex identifiers, rejects repeated vertices inside a simplex, rejects duplicate simplices, and represents the complex by its downward-closed set of vertex subsets. Consequently, for example:

- there is at most one abstract edge for a given unordered pair of vertices;
- a tetrahedron cannot identify two of its own vertices;
- two distinct tetrahedra cannot be represented as separate cells if they have exactly the same global vertex set;
- general face-pairing self-identifications are outside the model.

Those restrictions are useful for the old MORPH toy experiments, but they mean the current BPT/T0/T1 code is **not a faithful implementation of the theorem's topological-triangulation category**.

This is not a request to add a more general representation now. Representation work is justified only after a candidate relation clears the re-entry screen.

## 4. Exact sparse degree-two collapse semantics

The theorem does not use arbitrary edge collapse.

For a candidate edge `e` in a topological 3-manifold triangulation, the paper's sparse degree-two collapse requires, in substance:

1. `e` has degree exactly two;
2. exactly two tetrahedra `Delta1, Delta2` contain `e`;
3. their union is an embedded 3-ball in the manifold;
4. the relevant opposite edges `f1` in `Delta1` and `f2` in `Delta2` are distinct; and
5. both opposite edges have degree at least three.

The collapse identifies the endpoints of `e` and flattens the two incident tetrahedra. Its inverse expands the corresponding embedded two-face disc. The move reduces the complexity pair `(tetrahedra, vertices)` by `(2,1)`; the inverse increases it by `(2,1)`.

These conditions must be checked in the quotient topological triangulation, not inferred from the abstract vertex sets of the current `SimplicialComplex` class.

The paper explicitly describes this move as **more restrictive** than the general edge collapses used by Regina.

Reference:

- Tillmann–Tsvietkova, Section 2.3: https://arxiv.org/abs/2606.14413

### Not the same as Regina `collapseEdge()`

Regina's 3-dimensional `collapseEdge()` checks a broader topology-preserving edge-collapse operation and flattens all tetrahedra incident to the edge. Its legality conditions are deliberately more general than the sparse theorem move.

Reference:

- Regina `Triangulation<3>` API: https://regina-normal.github.io/engine-docs/classregina_1_1Triangulation_3_013_01_4.html

### Not just a `2-0` edge move

The theorem's sparse collapse also must not be silently renamed as the standard `2-0` edge move. Any theorem-aligned implementation would need the paper's exact local quotient conditions and inverse, with separate regression tests against broader or different simplification moves.

## 5. Mature-assumption screen: the theorem hard family

The paper proves NP-hardness by Karp reduction from a modified planar Hamiltonian-path problem.

At a high level, an embedded planar graph `Gamma` is transformed into a 3-sphere triangulation. Deleting suitable non-cut graph edges corresponds to sparse degree-two edge collapses. The target is reached in the prescribed number of collapses exactly when the original graph contains the required Hamiltonian path. The paper further proves that allowing bistellar moves does not create a shorter mixed route on these reduction instances.

Reference:

- Tillmann–Tsvietkova, Sections 3.3–3.4 and Theorem 1: https://arxiv.org/abs/2606.14413

For MORPH this is valuable complexity evidence about the move problem, but it creates a strong re-entry warning:

```text
sample reduction graph
-> encode graph as theorem triangulation
-> ask for bounded move path
```

would be a triangulated presentation of the Hamiltonian-path reduction family. It would not explain a new average-case distribution, a new trapdoor asymmetry, or a new post-quantum assumption.

Therefore the theorem reduction family is suitable as a **negative/control corpus** for a future generalized-triangulation harness, but it is not nominated as a MORPH cryptographic candidate.

Worst-case NP-hardness alone remains explicitly insufficient under `AGENTS.md` and MORPH-R0.

## 6. Standard public navigation/simplification attack surface

Any future candidate operating on genuine 3-manifold triangulations must treat mature topology software as attacker capability.

Regina currently exposes, among other operations:

- legal Pachner moves in dimension three;
- topology-preserving edge collapse;
- greedy simplification;
- exhaustive bounded-height simplification through the `2-3 / 3-2` Pachner graph;
- isomorphism signatures (`isoSig`) that identify triangulations up to combinatorial isomorphism.

References:

- Regina `Triangulation<3>` API: https://regina-normal.github.io/engine-docs/classregina_1_1Triangulation_3_013_01_4.html
- Regina documentation: https://regina-normal.github.io/docs/tri-modification.html

These capabilities enlarge, rather than replace, the inherited T0/T1 attack suite.

A future BPT attack plan must therefore include at minimum:

1. cheap greedy simplification independently on both endpoints;
2. splicing through any common simplified/isomorphic state;
3. exact or bounded-height bidirectional navigation on toy instances;
4. canonical `isoSig`-style state hashing;
5. general legal edge-collapse probes, even if the verifier only accepts the narrower sparse move;
6. recovery of any graph, spine, dual graph, normal surface, or other control object used by generation;
7. comparison against the already measured T0/T1 work factors.

If a public simplifier constructs an accepted route, it does not matter whether that route resembles the planted generation history.

## 7. Equivalent-witness discipline

For all BPT variants, define

```text
Equivalent(T0,T1,L) = {
    legal move paths p :
    len(p) <= L and Apply(T0,p) ~= T1
}
```

where `~=` is the verifier's public combinatorial-isomorphism relation.

The attacker wins with any member of this set.

This is not bookkeeping. BPT-W0 already demonstrates multiple accepted routes; T0 demonstrates that a much shorter equivalent route can exist than the planted walk; and T1 shows that even a unique measured shortest route at a tiny distance can remain publicly cheap to recover.

Any future generator must report route multiplicity or a justified bound/estimator where exact counting is infeasible.

## 8. Matched-control requirements

The following controls are inherited and mandatory:

### Weak simplification control

BPT-W0 stacked `1-4 / 4-1` instances. The harness must continue to reject them under label-invariant verifier semantics.

### Ordinary Pachner navigation controls

T0 and T1 provide two distinct controls:

- T0 catches planted-history/true-distance mismatch;
- T1 catches tiny public navigation work even after exact-distance conditioning.

A stronger distribution cannot claim progress merely because its planted paths are self-avoiding or exact-distance certified.

### New matched comparison

Before measuring a future distribution, fix a control with the same public representation class, size range, move alphabet, endpoint canonicalization, public move bound, and generator work budget. The comparison statistic and validation horizon must be declared before seeing attack outcomes.

## 9. Quantum screen

No BPT-specific quantum algorithm was identified in this screening pass. That statement is deliberately weak and is **not** evidence of post-quantum hardness.

The relation is still a search/navigation problem on a public state graph. Generic quantum search and quantum-walk techniques can provide square-root-type advantages over corresponding unstructured or random-walk search costs in broad settings.

References:

- S. Apers, S. Chakraborty, L. Novo, J. Roland, *Quadratic speedup for spatial search by continuous-time quantum walk*, arXiv:2112.12746: https://arxiv.org/abs/2112.12746
- A. Ambainis, A. Gilyén, S. Jeffery, M. Kokainis, *Quadratic speedup for finding marked vertices by quantum walks*, arXiv:1903.07493: https://arxiv.org/abs/1903.07493

For any future candidate, classical work factors must therefore not be reported as quantum work factors. A separate analysis would be required for state preparation, adjacency oracles, reversibility, memory, marked-state checking, and any exploitable algebraic/isomorphism structure.

## 10. What would be materially new enough to reconsider BPT

BPT can re-enter implementation only if a concrete generated relation is proposed that simultaneously satisfies all of the following before code:

- it is not the old T0/T1 `S^3` path distribution with larger parameters;
- it is not a direct or lightly disguised sample from the theorem's Hamiltonian-path reduction family;
- its representation is explicit enough that move legality and verifier equivalence are exact;
- any generalized face-pairing representation is justified by the candidate, not built speculatively;
- the generator does not filter on attacker output;
- a public simplification/navigation route is not already apparent from construction history;
- the accepted-witness quotient is explicitly defined;
- matched controls and mandatory validation are predeclared;
- a reason is given for why public `isoSig`/Regina-style simplification does not simply manufacture connectors;
- the quantum screen is stated without translating classical NP-hardness into PQ security.

A candidate could, in principle, use a different fixed manifold, a different distribution over genuine face-pairing triangulations, or a different bounded relation. But “different geometry” alone is insufficient; the computational relation and generated distribution must differ in a way that directly addresses the inherited failures.

## 11. Re-entry decision

No currently specified BPT distribution meets that bar.

Building a generalized Regina-like triangulation layer now would be infrastructure-first rather than hypothesis-first. Implementing the theorem reduction family would test a known NP-hard reduction but would fail MORPH-R0's “not a renamed mature assumption” requirement. Returning to plain `2-3 / 3-2` `S^3` search would repeat the already rejected T0/T1 corpus.

Therefore:

**NO NOMINATION.**

Do not implement BPT-R2, a theorem-reduction generator, a generalized face-pairing engine, a trapdoor, PKE or KEM from the current BPT state. Re-open BPT only when a concrete relation/distribution materially distinct from both T0/T1 and the Hamiltonian-path reduction family can pass the full MORPH-R0 specification on paper first.

No security claim.
