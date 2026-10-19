# MORPH-F0: adaptive pair-evaluation oracle transcripts and span-limited total variation

**Follow-up, distinct resource bound:** [adaptive *linear-bivector* probe TV](F0-planted-ti-adaptive-linear-bivector-probe-tv.md) extends the oracle-only interface beyond decomposable pair queries and bounds total **query-space dimension** (rather than vector-carrier dimension). Both notes expressly exclude attackers given the full published matrices.

**2026-10-19. Attack-first, analytic-only restricted-oracle theorem. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.** This follows the [precommitted random restriction](F0-planted-ti-random-restriction-exact-tv.md) and [precommitted joint-view span](F0-planted-ti-precommitted-multiview-span-tv.md) results, **without** claiming those results already covered adaptive selection. The new scope is a rigorously restricted *adaptive query oracle*, not the real full-public-tensor attacker. No candidate, new N1/F0-K/A-ID, executable inversion, cryptographic assumption, OWF/PKE/KEM/trapdoor or security claim.

**Source and external priority.** Planted alternating-tensor problem: Liu, Qiao, Tang and Zhang, *The planted tensor problem over finite fields: algorithms and cryptography*, [arXiv:2609.31256v1](https://arxiv.org/abs/2609.31256). Gaussian-binomial subspace counting and deferred random-linear-map exposure are standard elementary methods, not a new mathematical hard relation.

## 1. Unchanged full source, but a strictly bounded observation interface

Fix any prime power q>=2, V=F_q^n, 2<=d<n, c=n-d, and m>=1. Under null Q_0 the m alternating forms A_i are iid unrestricted uniform, and under planted Q_pl an unconditional d-plane H is sampled from prior pi and m iid uniform alternating forms conditioned on A_i|_(H x H)=0. Characteristic two is covered by zero-diagonal alternating forms. No conditioning or postselection of published samples occurs. The **original** public relation still accepts *any* full-rank n-by-d Y with Y^T A_i Y=0 for all i.

The **separate observation model in this note** is an oracle queried on an ordered vector pair (v,w) in V^2, returning the full vector of m field evaluations

\[
 O(v,w)=(A_1(v,w),\ldots,A_m(v,w))\in F_q^m.
\]

A randomized algorithm may choose each next pair and its stopping rule **adaptively using only previous queried pairs, answers and independent coins**. Include both all queries and all answers in the transcript. Its final carrier S_0 is the linear span of *every* vector appearing in its **null-oracle** queries. Assume finitely many queries almost surely; a worst-case polynomial query bound is sufficient but not necessary for the information-theoretic claim. The algorithm is **not** initially given the matrices A_i, their ranks, a nullspace, the planted H, or any global tensor-derived preprocessing. Allowing those full-data inputs changes the experiment and invalidates this narrow conclusion.

## 2. Adaptive coupling theorem for an arbitrary honest H-prior

**Theorem 1 (finite exact-source TV upper bound).** For every such possibly randomized and adaptive oracle algorithm Q and **every** unconditional prior pi over d-planes,

\[
\boxed{
\operatorname{TV}(\operatorname{Law}(Transcript_{\rm pl}),
                      \operatorname{Law}(Transcript_0))
\le
\Pr_{\substack{H\leftarrow\pi,\ A\leftarrow Q_0\\\text{independent coins}}}
\left[\dim(S_0(A,\text{coins})\cap H)\ge2\right].
}
\]

The probability on the right samples H **independently of the entire null run**, even though S_0 may depend arbitrarily on the null answers. This is an upper bound, not an equality or the actual full-public-tensor TV distance. It remains valid for arbitrary subsequent randomized postprocessing of the transcript.

**Proof.** Set E=Lambda^2 V and U=Lambda^2 H. Each null alternating slice is a uniform linear functional on E; each planted slice is a uniform functional on E/U. Fix an H and synchronize the algorithm's independent coins. At a given identical history, let L<=E be the linear span of all bivector queries v wedge w so far. For a proposed next query x=v wedge w, write L'=L+<x>. If L' cap U=0, then the quotient map E -> E/U is injective on L'. Hence *all linear relations among the exposed queries* are exactly the same under the null and planted source. Conditional on the matched previous answers, the next m-vector has precisely the same law in both experiments: it is already determined if x belongs to L, and otherwise it is an independent uniform F_q^m vector. The two responses can thus be coupled identically for this step.

Let S' be the span of all vectors in queries up to and including (v,w). Since L'<=Lambda^2 S', the elementary identity

\[
\Lambda^2 S'\cap\Lambda^2 H=\Lambda^2(S'\cap H)
\]

implies L' cap U=0 whenever dim(S' cap H)<=1. Starting with identical empty transcripts, couple successive responses by their common conditional law until the first query that creates dim(S' cap H)>=2; from that point use any coupling. The two transcripts can differ **only** on such a stopping event. Along the common prefix, the selected query pairs are identical; in particular the stopping event entails that the final carrier S_0 of the complete null run meets H in dimension at least two (intersection dimension is monotone as queried vector spans increase). The null side of this coupling retains its exact null-oracle distribution independent of H, so the coupling inequality for TV gives the boxed bound. This argument does not pretend that an adaptively chosen S is independent of its observed tensor values.

## 3. Uniform H gives a closed adaptive-query bound

Assume now that H is **uniform** on Gr(d,V). Under the null source, the final adaptive S_0 depends on the null tensor and algorithmic coins but is independent of H. Therefore, conditional on the *actual* null-query carrier S_0 of dimension t, the chance of intersection dimension j is exactly the classical Gaussian-binomial law

\[
g_{n,d,t,q}(j)=
\frac{[d\choose j]_q[c\choose t-j]_q q^{(d-j)(t-j)}}{[n\choose t]_q}.
\]

Define \(\beta(t)=\sum_{j\ge2}g_{n,d,t,q}(j)\). Theorem 1 immediately yields

\[
\boxed{\operatorname{TV}(Transcript_{\rm pl},Transcript_0)
\le \mathbb E_0[\beta(\dim S_0)].}
\]

**Corollary (adaptive carrier cap).** If the algorithm enforces dim(S)<=u<=c on **every** possible query transcript, then the entire, potentially long **fully adaptive** query-answer transcript obeys

\[
\boxed{
\operatorname{TV}(Transcript_{\rm pl},Transcript_0)
\le [d\choose2]_q\frac{[u\choose2]_q}{[n\choose2]_q}
\le \frac49 q^{-2(c-u)} .
}
\]

The first inequality is the union bound over 2-planes L<=H, followed by monotonicity of the number of 2-planes contained in S_0. For u<2 the bound is zero. The second finite-field inequality and its uniform q>=2 constant are established in the [single-view note](F0-planted-ti-random-restriction-exact-tv.md#4-exponentially-quiet-range-for-a-random-preselected-view). Thus, when u<=c-s, the total-variation advantage is at most (4/9)q^(-2s), independent of m, query count and internal computation. For fixed q and s=Omega(n) it is exponentially small.

**Separate arbitrary-prior corollary.** If pi is nonuniform but the **null-run** carrier S_0 has a GL(V)-invariant law conditional on its dimension (for example because the algorithm first privately randomizes its whole coordinate frame), then the same average-\(\beta\) and carrier-cap bounds hold. Merely having an arbitrary H-prior does **not** imply the carrier invariance; without it use the prior-weighted upper bound of Theorem 1.

## 4. Explicit small adaptive example (finite formula check only)

Take GF(2), n=4, d=2, m=1 with H uniform over all [4 choose2]_2=35 2-planes. A deterministic observer first queries (e1,e2). If the response is zero it next queries (e1,e3); if it is one it next queries (e2,e3). The chosen second query **depends on the tensor response**, while every transcript has final vector carrier span(e1,e2,e3), of dimension u=3.

Enumerating the 2^6 unrestricted alternating forms, all 35 possible H, and the 2^5 forms compatible with each H gives the exact transcript distributions, with transcript recorded by the ordered pair of answers (the selected second query is determined by the first):

\[
P_0(00)=P_0(01)=P_0(10)=P_0(11)=\tfrac14,
\]

\[
P_{\rm pl}(00)=\tfrac{19}{70},\qquad
P_{\rm pl}(01)=P_{\rm pl}(10)=P_{\rm pl}(11)=\tfrac{17}{70}.
\]

Consequently \(\operatorname{TV}=3/140\), versus the safely loose Theorem 1 bad-carrier bound \(\Pr(H\subseteq S_0)=[3\choose2]_2/[4\choose2]_2=1/5\). This example lies **outside** the exponentially quiet u<=c parameter range (here u=3>c=2); it checks the finite adaptive coupling bound, not that sparse asymptotic. The enumeration was an independent scratch arithmetic check, **not** repository code, CI, published experimental data or cryptanalytic inversion.

## 5. Strict boundary and research consequence

- This adaptive theorem covers **only** observers obtaining information through their explicitly recorded pair-evaluation queries; their carrier is the span of *every vector ever queried*. It does **not** cover a genuine attacker who starts with the full n-by-n public matrices and chooses a small S after inspecting tensor-dependent ranks, kernels, MinRank combinations or other global invariants.
- Giving the full matrices to the algorithm effectively exposes the entire tensor regardless of how few additional pairs it later asks; declaring a small post-hoc query span does not meet the theorem's oracle-only hypothesis.
- The uniform-H assumption is material for arbitrary adaptive query policies. For a known deterministic H=H0, querying a basis of H0 makes the planted responses identically zero and can distinguish from null even when d<c.
- Even the **full restricted transcript** may be statistically quiet while a full-public-tensor dimension-d isotropic witness exists with overwhelming planted-vs-null distinguishing power. No efficient Z_r counter, original full-verifier accepted witness, average-case hardness, TV closeness of full sources, or new Field-15 foundation follows.
- This result is about linear evaluation access to already defined alternating tensors and finite-field sampling, not a claimed new cryptographic problem.

**Disposition:** ANALYTIC ADAPTIVE-ORACLE LOCAL-SPAN NEGATIVE CONTROL ONLY. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD; N1-60 remains unallocated; HEPMR BENCHMARK ONLY. README and stage registry unchanged.
