# MORPH-F0: full-public graph-cover reconstruction by color refinement

**2026-10-22. Independently sourced graph-covering search relation; attack-first ANALYTIC REJECT on the discrete-color base class, including an unfiltered dense random-base family.** This is an application of **established** graph-cover/Weisfeiler-Leman theory, **not** a new algorithmic priority claim, crypto hardness assumption or candidate. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD; D0 DEFER, D1 HOLD; planted-TI FROZEN. No N1-60, F0-K, A-ID, code, benchmark or security parameter.

## 1. Original full public source and any-cover verifier

Let H=(V,E) be an **explicit finite undirected simple graph** with n polynomially bounded vertices and edges. Choose a sheet count k=2. The honest source makes a 2-lift G of H: for each public undirected base edge {u,v}, choose independently a uniform bit \(\sigma_{uv}\), and connect (u,i) to (v,i⊕\sigma_{uv}) for i∈{0,1}. Optionally apply any polynomial-time randomized public-vertex relabeling process to the 2n lift vertices, while omitting the planted covering map \(\pi\). Publish P=(H,G) in ordinary uncolored graph encodings. **Do not publish sheets, \(\pi\), vertex-to-base hints, or edge-voltage bits**. The honest source is unconditional: every selected bit pattern and relabeling is accepted; neither H nor G is postselected by an attack test. A polynomial-time source can also choose H before this process.

The complete public original verifier accepts a map \(\rho:V(G)\to V(H)\) only if it is surjective and for **each vertex** x∈V(G), the restriction \(\rho:N_G(x)\to N_H(\rho(x))\) is a bijection, with edge preservation checked on the full public G (equivalently this is a covering projection for simple undirected graphs). All maps are polynomial-size. **Any** accepted covering map wins; the sampled \(\pi\) itself need not be recovered.

## 2. Exact public recovery theorem

Define ordinary unlabeled 1-dimensional Weisfeiler-Leman / color-refinement signatures on the **disjoint union** H ⊔ G, starting at \(c_0(v)=0\) for every vertex and iterating
\[
 c_{t+1}(v)=\operatorname{canonicalID}
 \big(c_t(v), \{\!\{c_t(w):w\in N(v)\}\!\}\big).
\]
CanonicalIDs are computed jointly, so equality means literally equal combinatorial signatures, **not separately enumerated arbitrary names**. Stabilize after polynomially many rounds (at most |V(H)|+|V(G)| strict partition refinements). The color of each G vertex is mapped to the color of its planted H-image by every iteration:

**Lemma (cover-equivariance of 1-WL).** For every covering projection \(\pi:G\to H\), every vertex x of G and all t,
\[
\boxed{c_t(x)=c_t(\pi(x)).}
\]

**Proof.** Equality holds at t=0. A covering locally bijects the neighbor multiset of x to the neighbor multiset of \(\pi(x)\). Assuming colors agree at depth t for each lift/base pair, those multisets agree with multiplicities and the old vertex colors agree. Joint canonical refinement therefore assigns equal new colors. Induct. This is classical covering-invariance of color refinement, not a newly discovered property. QED.

**Theorem (any-witness full public section).** Suppose that **the stable 1-WL colors on H are pairwise distinct**, a publicly checkable condition requiring no secret, for a published honest 2-lift G. For every lift vertex x, the matching base vertex h with \(c_*(h)=c_*(x)\) is unique. Output
\[
\boxed{\rho(x)=\text{the unique }h\in V(H)\text{ with }c_*(h)=c_*(x).}
\]
By the lemma, this map equals the sampled \(\pi\), satisfies **every part of the original covering verifier**, and is recovered by deterministic polynomial-time computation in the **entire** size of (H,G). The attacker does not receive the hidden sheet bits or \(\pi\), and does not rely on planted-label identification or a restricted oracle. Its success is pointwise for all honest lifts over any H satisfying the public color condition. Even a large covering degree, many voltage assignments, and long cycles are no barrier **in this class**.

**Source-level consequence:** if any unconditional polynomial-time base graph distribution \(\mathcal D_n\) has \(\Pr_{H\sim\mathcal D_n}[\mathrm{1WL}(H)\text{ discrete}]\ge1-\delta_n\), then the above full-public accepted-witness algorithm succeeds with probability ≥\(1-\delta_n\) over the **entire unfiltered base + lift + relabeling source**, for every distribution of lifted edge permutations/relabelings conditional on H. No cross-edge independence is required for the attack; the exact specified honest 2-lift source merely demonstrates an efficiently sampleable concrete relation.

## 3. Truly unfiltered dense random-base rejection

Take H~G(n,1/2), sampled by n(n-1)/2 independent unbiased edge bits; then sample an independent uniformly random bit per base edge for the 2-lift and optionally relabel its vertices. The theorem by **Babai–Erdős–Selkow, *Random Graph Isomorphism*, SIAM J. Comput. (1980)** states that color refinement is discrete on H **with probability tending to one** as n grows. This specific statement is also recalled explicitly by **Verbitsky–Zhukovskii, *Canonical Labeling of Sparse Random Graphs*, STACS 2025**. Therefore the full original cover-verifier accepted-witness attack succeeds with probability **1-o(1)** on this unconditional honest dense random-base distribution. This is not the probability for arbitrary base distributions (such as regular or strongly regular graphs), and it is not a proof of an optimal graph-covering algorithm.

## 4. Independent finite arithmetic control (not a benchmark)

For a fixed seven-vertex simple base H with edges
\[
\{01,05,14,15,16,24,46,56\}
\]
the stable 1-WL coloring is discrete (seven distinct colors). Using the edge order displayed, choose 2-lift voltage bits \((1,0,1,0,0,1,0,0)\), construct fourteen lift vertices, and apply an arbitrary vertex permutation hiding the sheets. A direct tiny scratch computation of simultaneous color refinement produces exactly one distinct base color per H vertex and exactly two lift vertices of each base color. Assigning each lift vertex to its uniquely matching H-color reconstructs a covering map passing all local bijections. This checks only one **toy** pair and makes no claim about a large-source success frequency, a committed executable attack, calibrated runtime, or cryptographic parameter selection.

## 5. Prior art and the actual negative/positive gate

Graph covers are a classical **locally bijective graph homomorphism** problem, with longstanding complexity results for fixed and variable target H; see **Bok–Fiala–Jedličková–Kratochvíl–Seifrtová, *Computational Complexity of Covering Colored Mixed Multigraphs with Simple Degree Partitions* (2025 preprint; Discrete Applied Mathematics 2026)**, https://arxiv.org/abs/2502.20151. The **cover-invariance of color refinement** is stated explicitly in **Verbitsky–Zhukovskii (STACS 2025), §2.2**, https://doi.org/10.4230/LIPIcs.STACS.2025.75. The near-surely discrete-color dense random-base theorem is **Babai–Erdős–Selkow (1980)**, https://doi.org/10.1137/0209047. The graph-cover universal-cover connection and color-refinement/degree-matrix algorithms are established, e.g. **Fiala–Paulusma, *Comparing universal covers in polynomial time***, https://durham-repository.worktribe.com/output/1159609. These sources prevent any independent novelty assertion about coloring-invariant recovery.

The conclusion does **not** hold when base 1-WL colors are not all distinct, when only an unlabeled base graph *invariant* rather than the full public base H is published, for a compressed exponentially large graph, for vertex constraints inconsistent with this verifier, or for an adversarially selected nonhonest G. Failure of this particular sufficient attack condition is **not** hardness evidence: known graph covering algorithms, individualization-refinement, higher WL, group actions, isomorphism algorithms and source-specific cover tests remain available. Worst-case NP-hardness of some H-Cover families does not supply average-case one-wayness for the planted 2-lift source.

**Disposition:** graph-cover inversion with public 1-WL-discrete H **ANALYTIC REJECT**, in particular the completely unfiltered \(G(n,1/2)\) random-base plus random 2-lift family is inverted with probability 1-o(1) on its original accepted-witness relation. A **non-discrete base** is only a different *known graph-cover problem* requiring exact honest-source attack analysis and positive independent MORPH-R0 Field 15; no cryptographic candidate is nominated. Do **not** create another graph-cover parameter variant merely by making the base regular or increasing lift degree. Return to independent-object selection unless positive mathematical differentiation is supplied.
