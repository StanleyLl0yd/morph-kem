# MORPH-F0: rank-sensitive TV bounds for adaptive linear bivector probes

**2026-10-19. Strict oracle-only information-theoretic negative control; GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.** This strengthens the previously proved [adaptive pair-evaluation carrier bound](F0-planted-ti-adaptive-oracle-span-tv.md), **not** the fully public matrix inversion problem. No new N1/F0-K/A-ID, candidate, assumption, source experiment, algorithmic KEM/PKE/OWF/trapdoor, security or average-case-hardness claim.

**External source / priority.** The alternating-form planted TI problem is studied by Liu, Qiao, Tang and Zhang, *The planted tensor problem over finite fields: algorithms and cryptography*, [arXiv:2609.31256v1](https://arxiv.org/abs/2609.31256). The support of a bivector, Grassmann containment probabilities and delayed linear-oracle sampling below are standard finite-dimensional algebra. They do not establish an independently new Field-15 hardness basis.

## 1. Full honest law and a *stronger*, but still restricted, oracle

Let V=F_q^n for any prime power q>=2, 2<=d<n, c=n-d and m>=1. Under null, m independent uniform alternating forms are sampled on V. Under planted, choose an unconditional d-plane H (with arbitrary prior pi unless otherwise stated), then m independent **uniform** alternating forms annihilating H x H. Alternating forms have zero diagonal in characteristic two. No sample selection or rank filtering is used. The actual *full-public-tensor* original verifier accepts **any** rank-d Y with Y^T A_i Y=0 for every i.

Put E=Lambda^2V. Here a **linear-bivector oracle** receives an arbitrary vector x in E, **not necessarily decomposable**, and returns the m field scalars

\[
O(x)=(\langle A_1,x\rangle,\ldots,\langle A_m,x\rangle)\in F_q^m.
\]

A randomized observer may choose each new x and its stopping time adaptively using **only** its own independent coins and previous oracle queries/answers. The full transcript records these choices. Let L_0<=E be the linear span of *all queried bivectors in its null-oracle run*, of random dimension ell_0; assume finitely many queries. The observer does **not** receive the full alternating matrices, their public kernels/ranks, or tensor-dependent side information before or during oracle access. This last distinction is mandatory: a genuinely published tensor already contains Θ(n^2) field coefficients per slice and does not satisfy this narrow information-access model.

## 2. Source-first adaptive transcript coupling

**Theorem 1 (any honest H-prior, finite exact source).** For every (possibly unbounded-computation) adaptive linear-bivector oracle observer,

\[
\boxed{\operatorname{TV}(Transcript_{\rm pl},Transcript_0)
 \le \Pr_{H\sim\pi,\; \text{independent null run}}\!
       [L_0\cap\Lambda^2H\ne\{0\}].}
\]

**Proof.** Fix H and set U=Lambda^2H. Each null slice is a uniform linear functional E->F_q; a planted slice is a uniform linear functional on E/U. For a common previous query span L and a proposed new query x, whenever (L+<x>) cap U=0, the quotient E->E/U is injective on the enlarged query span. Thus the exact linear dependence relations and the conditional distribution of the next m answers, given identical past answers, agree between the sources: a dependent query repeats a forced linear combination, while an independent query returns an independent uniform F_q^m vector. Couple each next answer identically until the first query enlarging L to intersect U. After that use any coupling. A first transcript discrepancy is possible only at or after that event, and the matching prefix forces the null-run L_0 to intersect U as well. The coupling inequality gives the theorem. Although the planted query span is selected from planted answers, **the bad event is evaluated on an independent null run**; it is not assumed that a tensor-dependent planted span is independent of H.

For a *fixed nonadaptive* linear query subspace L, conditioned on a fixed H, the exact TV of the complete restrictions to L is \(1-q^{-m\dim(L\cap U)}\), as a direct quotient-linear-map calculation. Do not equate this nonadaptive conditional identity with the **adaptive** transcript TV; the stopping-time theorem above uses only the rigorous intersection-probability upper bound.

## 3. Exact support-rank geometry

For a nonzero bivector x in E, define its **support** \(W_x\le V\) to be the image of the contraction map \(V^*\to V,\ \alpha\mapsto \iota_\alpha x\). Its dimension s(x) is the (even) rank of the associated alternating coefficient matrix, so s(x)>=2, including over fields of characteristic two. A direct block decomposition relative to V=H+complement shows

\[
\boxed{x\in\Lambda^2H\ \Longleftrightarrow\ W_x\subseteq H.}
\]

Indeed membership in Lambda^2H makes all contractions land in H; conversely if every contraction lies in H, the mixed H/complement and complement/complement matrix blocks vanish, so x lies in Lambda^2H. For H uniform on Gr(d,V), the probability of including a fixed s-dimensional W_x is

\[
\boxed{\eta_s=\Pr_H(x\in\Lambda^2H)
=\begin{cases}
[d\choose s]_q/[n\choose s]_q,&s\le d,\\
0,&s>d,
\end{cases}
\quad\le q^{-cs}.}
\]

The last inequality follows termwise from
\((q^{d-j}-1)/(q^{n-j}-1)\le q^{-c}\) for 0<=j<s<=d. In particular the **highest** containment probability over nonzero bivectors is attained at rank two and is at most q^{-2c}; higher-rank bivectors have strictly smaller probability or exactly zero.

**Exact one-query public law (any prior).** For any fixed public nonzero query x and any unconditional H-prior, put \(w_x=\Pr_\pi(W_x\le H)\). Null O(x) is uniform F_q^m; planted O(x) is a mixture of a zero vector with weight w_x and a uniform vector with weight 1-w_x. Hence

\[
\boxed{\operatorname{TV}(O_{\rm pl}(x),O_0(x))
=(1-q^{-m})w_x.}
\]

Under uniform H, w_x=eta_{s(x)}. This proves an exact rank-sensitive *one-query* statement, not an algorithm for constructing an accepted d-plane.

## 4. Rank-sensitive adaptive union bound and linear-query lower bound

**Theorem 2 (uniform H).** Conditional on the random null span L_0, the hidden uniform H is still independent of L_0. Union-bound the event of Theorem 1 over distinct projective one-dimensional directions of L_0. For any nonzero query-space L define

\[
B(L)=\sum_{[x]\in\mathbf P(L)}
\frac{[d\choose s(x)]_q}{[n\choose s(x)]_q},
\]

where terms with s(x)>d are zero. Then

\[
\boxed{
\operatorname{TV}(Transcript_{\rm pl},Transcript_0)
\le \mathbb E_0[\min(1,B(L_0))]
\le \mathbb E_0\left[\min\left(1,
 \frac{q^{\ell_0}-1}{q-1}\frac{[d\choose2]_q}{[n\choose2]_q}
\right)\right].}
\]

If at most Q bivectors are queried on **every** transcript, ell_0<=Q, so the universal finite-field simplification is

\[
\boxed{
\operatorname{TV}(Transcript_{\rm pl},Transcript_0)
\le \min\left(1,\frac{q^Q-1}{q-1}\frac{[d\choose2]_q}{[n\choose2]_q}\right)
\le \min(1,q^{Q-2c}).}
\]

This bound is independent of m, the algorithm's computational running time, the queries' ranks, and whether query directions are selected adaptively from earlier answers. More exactly, their ranks can only improve the first rank-sensitive sum.

**Query complexity corollary.** Any oracle-only adaptive algorithm with distinguishing advantage at least a constant delta>0 must use

\[
\boxed{Q\ge 2c-\log_q(1/\delta)}
\]

queries in the worst-case transcript, whenever this right-hand side is positive. In the externally conjectural regime d=ceil(n/C) for C>=3, c=Theta(n), every Q<=2c-epsilon*n has exponentially small TV <=q^{-epsilon*n} for any fixed epsilon>0. This is an *information-theoretic query bound in a restricted oracle model*, not a polynomial-time hardness or security statement about the full m published n-by-n matrices. The [earlier pair-carrier TV theorem](F0-planted-ti-adaptive-oracle-span-tv.md) can be stronger when many pair queries stay inside a small vector carrier, while this theorem can be stronger for a budget on the number of independent global bivector queries.

**Optional nonuniform prior:** the uniform-H conclusion also holds for any fixed H-prior when the null query span L_0, conditional on its dimension, has a GL(V)-invariant distribution under the induced exterior-square action. The event probability for fixed H is then the same as after uniformly randomizing H by transitivity. Without such symmetry, only Theorem 1 holds for arbitrary pi.

## 5. Tiny exact GF(2) arithmetic controls (scratch, not committed experiments)

Set q=2, n=4, d=2 and m=1; E has dimension 6 and there are [4 choose2]_2=35 equally likely planted 2-planes H. Enumerating all 64 null forms and the 32 uniform compatible forms for each of the 35 H yields:

- One decomposable rank-two query x=e1 wedge e2: exact planted/null TV = (1-1/2)/35 = **1/70**.
- One nondecomposable rank-four query y=e1 wedge e2 + e3 wedge e4: support(y)=V, which cannot lie in any 2-plane H; exact planted/null TV = **0**.
- Two fixed rank-two queries x1=e1 wedge e2 and x2=e3 wedge e4: exact joint TV = **1/70**. Their three projective span directions have ranks 2,2,4, so B(span{x1,x2})=2/35 (not the looser 3/35 unranked bound).

These are deliberately tiny exhaustive **formula checks** performed separately, not a full-tensor attack benchmark, source experiments committed to the repository, new tests, or evidence for a cryptographic candidate.

## 6. Exact limits and falsification priority

The proof never samples accepted-only public tensors, alters their verifier, or hides equivalent witnesses in the definition. Still, it **does not** model the original attacker who receives the entire public tuple. An algorithm allowed to read a global alternating matrix, compute its nullspaces, select minimum-rank linear combinations, or choose a clever L based on all its entries need not generate L through the restricted oracle and is not subject to this theorem. Full-public-tensor planted/null TV can be close to one even when a bounded-query transcript is statistically quiet. Results for arbitrary full-data algebraic recovery, q-growing regimes with costly arithmetic, average-case planted TI inversion, and independently novel Field-15 foundation remain open.

**Disposition:** RANK-SENSITIVE ADAPTIVE LINEAR-ORACLE NEGATIVE CONTROL ONLY. GLOBAL NO NOMINATION, H-A/H-B/H-C HOLD; N1-60 unallocated; HEPMR BENCHMARK ONLY; README, code, and stage registry unchanged.
