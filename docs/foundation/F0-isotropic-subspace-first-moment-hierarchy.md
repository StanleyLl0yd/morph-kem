# MORPH-F0: exact first moments for all isotropic subspace dimensions

**2026-10-19. Analytical source-first counting boundary, not an implemented attack or a new candidate.** GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD. This note extends the previously merged [rank-two dual-bivector moments](F0-dual-bivector-kernel-exact-source-moments.md), without reproducing their exact covariance/variance result. It does not allocate N1-60, claim independent cryptographic novelty, solve any-witness inversion, or give a polynomial-time subspace counter.

**Source and earlier priority.** The planted alternating-tensor setting is Liu, Qiao, Tang and Zhang, *The planted tensor problem over finite fields: algorithms and cryptography*, [arXiv:2609.31256v1](https://arxiv.org/abs/2609.31256). The previously established exact planted size-bias, d-dimensional null first-moment/uniqueness and search-to-detection discussion is [#208, comment 6215551334](https://github.com/StanleyLl0yd/morph-kem/issues/208#issuecomment-6215551334). The genuinely *scoped addition here* is the entire intermediate-r first-moment hierarchy plus a quantitative relative-mean suppression bound; all ingredients are elementary standard finite-geometry counting, not a new hard mathematical assumption.

## 1. Full original public relation and source

Work over any finite field F_q, including characteristic two. Let V=F_q^n, 2<=d<n, c=n-d, m>=1. Sample a planted d-plane H from **any unconditional** H-distribution and then independent **uniform** alternating bilinear forms A_1,...,A_m conditioned on A_i|_(H x H)=0. The null source has m independent unrestricted uniform alternating forms. No conditioning or discarding of published samples is permitted. The original full verifier accepts *any* n-by-d rank-d matrix Y if Y^T A_i Y=0 for **every** i. The subspace count below is a mathematical statistic, not an additional verifier restriction.

For each 1<=r<=d define Z_r(A) as the number of labelled-by-their-position (not ordered-basis) r-dimensional subspaces J<=V such that A_i|_(J x J)=0 for all i. Let b_r=binom(r,2) and G_r=[n choose r]_q, using Gaussian-binomial coefficients.

## 2. Exact full-source means

**Theorem.** For all 1<=r<=d:
\[
  \boxed{E_0 Z_r = {n\brack r}_q q^{-m\binom r2}.}
\]
Under the planted source, conditional on **each fixed H**, and therefore also under any unconditional choice of H,
\[
\boxed{
 E_{\rm pl} Z_r =
 \sum_{t=\max(0,r-c)}^{r}
 {d\brack t}_q{c\brack r-t}_q
 q^{(d-t)(r-t)}
 q^{-m(\binom r2-\binom t2)}.}
\]
Terms with invalid Gaussian-binomial indices are zero. The formula applies unchanged to binary fields, since alternating forms are zero-diagonal even in characteristic two.

**Proof.** A fixed J imposes exactly b_r independent linear constraints on an unrestricted uniform alternating form, so its m-slice survival probability under null is q^(-m b_r). For planted H, let t=dim(J intersect H). The exterior-square intersection identity
\[
  \Lambda^2 J\cap\Lambda^2 H=\Lambda^2(J\cap H)
\]
gives exactly b_r-b_t independent constraints on a form uniformly drawn from the annihilator of Lambda^2 H. Its m-slice survival probability is q^(-m(b_r-b_t)). The exact number of r-planes J with intersection dimension t with fixed H is
\[
 {d\brack t}_q {c\brack r-t}_q q^{(d-t)(r-t)}.
\]
Indeed, select J intersect H as a t-plane of H, select its (r-t)-dimensional image in V/H, then choose its graph in H/(J intersect H), of which there are q^((d-t)(r-t)). Summing proves the theorem. The intersection counts also sum to [n choose r]_q. They depend only on dimensions, so averaging over **any** honest H-prior does not alter the result.

For r=1, both sources have deterministic Z_1=[n choose1]_q. For r=2, the formula reduces exactly to the mean from [PR #231](../foundation/F0-dual-bivector-kernel-exact-source-moments.md), namely S+(G_2-S)q^(-m), S=[d choose2]_q. No higher-dimensional variance or TV assertion is smuggled into this first-moment identity.

## 3. A quantitative low-r relative-mean blind window

Define R_r=E_pl Z_r/E_0 Z_r and let T=dim(J intersect H), for uniform J in Gr(r,V) with any fixed H. Cancelling the common q^(-m b_r) gives the **exact** expression
\[
 R_r-1=\sum_{t=2}^r \Pr[T=t]\big(q^{m\binom t2}-1\big)\ge0.
\]
The missing t=0,1 contributions are exactly zero, **not** neglected asymptotically. By a union bound over t-planes inside J,
\[
 \Pr[T\ge t]\le {r\brack t}_q {d\brack t}_q/{n\brack t}_q.
\]
For q>=2, [r choose t]_q<=4q^{t(r-t)}<=4q^{tr} and
\[
 {d\brack t}_q/{n\brack t}_q
 =\prod_{j=0}^{t-1}\frac{q^d-q^j}{q^n-q^j}
 \le 2^tq^{-ct}.
\]
Thus, for 2<=r<=d, putting
\[
 \sigma=c-r-\tfrac m2(r-1),
\]
we obtain whenever 2q^(-sigma)<1,
\[
\boxed{0\le R_r-1
 \le 4\sum_{t=2}^r (2q^{-\sigma})^t
 \le \frac{16q^{-2\sigma}}{1-2q^{-\sigma}}.}
\]
This is a finite-n explicit relative-**expectation** inequality, not a bound on the TV distance of Z_r, nor a variance or detection bound.

For **fixed q**, m=ceil(n/log n), d=ceil(n/C) with any constant C>=3 (using natural log as in the parameter scaling), c=n-d, and fixed 0<epsilon<2, uniformly over integers 2<=r<=min(d,(2-epsilon)c/m), we have sigma=Omega(n). Consequently R_r=1+q^(-Omega(n)). This includes every fixed r, and a growing r=Theta(log n) window, even though the planted source always has a valid dimension-d witness. A difference in first moments outside this window also does not imply an efficient distinguisher.

## 4. What this does and does not resolve

The **full** d-dimensional accepted-witness problem remains the target. The prior exact estimate E_0 Z_d=[n choose d]_q q^(-m binom(d,2)) can make null d-plane existence overwhelmingly unlikely; this is already established in [#208](https://github.com/StanleyLl0yd/morph-kem/issues/208#issuecomment-6215551334) and is not a new detector. Conversely, for small r the expected count is almost the same under planted and null, but expectations do **not** control distributional TV or rule out nonlinear, higher-moment, optimized MinRank, algebraic-geometric or original-verifier search attacks.

Z_r is a combinatorial count over generally exponentially many r-planes. The formulas neither compute Z_r in polynomial time nor recover a hidden (or any accepted) d-plane; source-relative mean proximity is not cryptographic security. The separate proven sparse individual-rank/minrank null controls remain [here](F0-sparse-planted-ti-rank-profile-minrank-screen.md), and the previous universal small-d public inverse remains [#208, comment 6214371503](https://github.com/StanleyLl0yd/morph-kem/issues/208#issuecomment-6214371503).

**Disposition:** exactly derived intermediate-r source-moment hierarchy, **ANALYTIC NEGATIVE CONTROL ONLY**. GLOBAL NO NOMINATION, H-A/H-B/H-C HOLD; no generated cases, tests, new experiment, implementation, candidate, N1 number, PQ/OWF/PKE/KEM/trapdoor claim. HEPMR #195 BENCHMARK ONLY, #199 evidence blocker and historical partial stages unchanged.
