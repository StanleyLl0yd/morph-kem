# MORPH-F0: exact H-A residual core and F0-K9 acyclic-hypergraph no-go

**Date:** 2026-10-16. **State:** paper-only, **GLOBAL NO NOMINATION**. This is a quotient-first research clarification, not a new cryptographic primitive, new hardness theorem or general inversion algorithm. H-A/H-B/H-C HOLD. No code, source generation, empirical samples, N1-60 allocation, cryptographic security assertion or trapdoor/PKE/KEM design.

## 1. Inversion target and honest distribution

For finite efficiently encoded publicly recognizable X, public polynomial-time maps \(f:X\to A\), \(g:X\to B\), and an **unconditional polynomial-time source** \(x\leftarrow D_\lambda\), publish \(P=(a,b)=(f(x),g(x))\). The **original verifier** is

\[
V(P,y)=[y\in X\;\wedge\;f(y)=a\;\wedge\;g(y)=b],\qquad
E(P)=\{y:V(P,y)=1\}.
\]

The attacker needs **any** \(y\in E(P)\), not the planted x. The honest distribution of P is the *unconditioned push-forward* of \(D_\lambda\), not uniform over output pairs, or a source postselected for attack difficulty.

## 2. H-A: public full-fibre chart exposes an exactly equivalent residual inversion problem

**Lemma (change of variables, not an attack).** Suppose for every honestly reachable a there is a publicly computed polynomial-size chart with polynomial-time maps \(\Phi_a:T_a\to f^{-1}(a)\) and \(\Phi_a^{-1}\), inverse bijections, with efficiently recognizable T_a. Neither chart nor inverse may depend on the planted x or on unknown hidden witness information. The sets T_a need not be vector spaces or efficiently enumerable.

For each honest P, define the *residual* accepted relation

\[
R(P)=\{t\in T_a:h_a(t)=b\},\quad h_a=g\circ\Phi_a.
\]

Its honest hidden parameter is obtained by sampling x from the **same unconditional D**, then setting \(a=f(x)\), \(b=g(x)\), \(t=\Phi_a^{-1}(x)\). It is not necessary (or generally justified) to resample t uniformly in T_a.

**Proof of exact distribution-preserving interreduction.** On the **same public P**, a residual-inversion algorithm returning t is converted into a paired inverter by verifying \(t\in T_a\), \(h_a(t)=b\), and the **entire original verifier** of \(\Phi_a(t)\); output \(\Phi_a(t)\) on success and a distinguished failure otherwise. Conversely, a paired inverter returning y is converted to residual inversion by first checking the **entire original verifier** on y, then returning \(\Phi_a^{-1}(y)\) after residual membership/equality verification, or failure. Bijection onto the **entire** first-view fibre makes these checks equivalent. Thus \(E(P)\leftrightarrow R(P)\) bijectively and the wrapped algorithms have **exactly the same success probability** under the identical honest public-input distribution. All transformations are polynomial in explicit input length.

This lemma **does not** imply residual inversion is easy, or that charts exist in every H-A problem. If no public full-fibre chart is available, no reduction is asserted. Merely failing to identify one is not evidence of hardness.

**Field-15 research consequence:** isolate the residual mathematical family \(\{h_a\}\) and induced (a,t) law *before* claiming that marginal section incompatibility is independently new. F0-K8 proves an easy section if \(h_a\) is explicitly affine on a public vector-space chart. F0-K5 shows arbitrary pre-existing inversion can be repackaged as two trivially invertible views. Hence this lemma identifies the *place where novelty could reside*, without granting novelty.

[Original project proof in #208](https://github.com/StanleyLl0yd/morph-kem/issues/208#issuecomment-6210012660); [F0-K5/K8 context](F0-failure-mechanisms.md).

## 3. F0-K9: explicit acyclic hypergraph joins admit a polynomial public section

**Proposition (Yannakakis-type known result).** Let \(V\) be a public set of variables, and \(R_i\subseteq\prod_{v\in U_i}S_v\) be public **explicitly enumerated finite** relation tables on scopes \(U_i\subseteq V\). Their **total list bitlength N is polynomial**, regardless of the number of syntactically possible tuples. Suppose the public hypergraph of scopes has a public *join tree*: for every variable v, the set of scope-nodes containing v is connected in the join tree (the running-intersection property). An unconditional generator samples any global x first and publishes polynomial-length relation tables \(R_i\) containing \(x|_{U_i}\); other rows may be independently generated decoys. The **original joint verifier** accepts *any* global y with \(y|_{U_i}\in R_i\) for **all** i.

**Public attack.** Root the join tree. Bottom-up, for every parent-child pair discard a parent tuple if no surviving child tuple matches it on their common separator \(U_i\cap U_j\); process children after all their descendants. The planted x ensures a surviving root tuple. Select any surviving root tuple and propagate top-down, choosing for each child a surviving tuple compatible with its parent's separator. By the running-intersection property, values chosen in distinct subtrees never conflict on shared variables. They combine into a complete y satisfying **all original verifier tests**. The procedure uses only polynomially many table scans and tuple comparisons in the explicit input (e.g. a loose \(O(kN^2)\) comparison bound), without constructing the complete join-output table. It succeeds on **every honest** P and never needs the original x.

**High-width trap:** if \(U_1=V\), the primal constraint graph is the clique \(K_{|V|}\) (treewidth \(|V|-1\)); still, with a polynomial-size extensional allowed-tuple table, simply selecting one row supplies a full accepted witness. Therefore even *maximal primal treewidth* does not imply hard local-to-global reconstruction if the constraint **hypergraph** has a join tree.

**Mature prior art:** Mihalis Yannakakis, [*Algorithms for Acyclic Database Schemes*](https://www.vldb.org/dblp/db/conf/vldb/Yannakakis81.html), VLDB (1981), pp. 82–94; [*Database Theory in Action: Yannakakis' Algorithm*](https://drops.dagstuhl.de/storage/00lipics/lipics-vol365-icdt2026/html/LIPIcs.ICDT.2026.25/LIPIcs.ICDT.2026.25.html), ICDT 2026. This is the existence/one-witness form of classical acyclic conjunctive-query processing, **not a new cryptographic result**. [Original MORPH proof and scope](https://github.com/StanleyLl0yd/morph-kem/issues/208#issuecomment-6210050665).

**Not covered:** succinct predicate circuits without explicitly enumerable polynomial-size relation tables; cyclic hypergraphs lacking other tractability certificates; hidden/invalid join-tree data; deliberately inconsistent/noisy constraints; extra admissibility restrictions not represented by the full join. This theorem is *not* a generic polynomial algorithm for all hypergraph CSPs.

## 4. Disposition and next work

- **F0-K9: ANALYTIC REJECT** for H-B's exact acyclic-extensional-join subclass; separate from F0-K3's bounded-primal-width hypothesis. H-B as a whole **HOLD**, not universally disproved.
- **H-A residualization: exact conditional equivalence**, not an inverter or positive novelty claim. H-A **HOLD** until an independently defined specific \(h_a\) relation satisfies all 15 MORPH-R0 fields, demonstrates a positive independent Field-15 distinction, and admits a defensible unconditional distribution and attack study.
- H-C **HOLD / lower priority**. No KEM/PKE/trapdoor/OWF/PQ-security declaration. Do not allocate N1-60 based on a general reduction or mature database problem.
- Provenance unchanged: #199 actual ZIP archive bytes still missing; historical N1-19 19/30 and N1-23 9/12 remain PARTIAL, N1-26 HOLD/BENCHMARK; HEPMR #195 BENCHMARK ONLY through AP103. **Zero new case counts and no research source sampling.**
