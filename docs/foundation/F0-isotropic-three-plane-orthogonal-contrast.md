# MORPH-F0: an exact Z3-vs-Z2 null-orthogonal contrast for planted alternating forms

**2026-10-19. Purely analytical attack-first statistics screen.** GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD. This note follows the [all-r moments](F0-isotropic-subspace-second-moment-boundaries.md) and [joint cross-dimensional covariance theorem](F0-isotropic-subspace-mixed-covariance-rank-one.md) without repeating them as novel mathematical foundations. No new numbered research stage, assumption, efficient counter, implementation, OWF/PKE/KEM/trapdoor or security claim.

**External source and priority.** Liu, Qiao, Tang and Zhang, *The planted tensor problem over finite fields: algorithms and cryptography*, [arXiv:2609.31256v1](https://arxiv.org/abs/2609.31256); previous exact planted size-bias and full-d null-witness rarity are credited to [#208 comment 6215551334](https://github.com/StanleyLl0yd/morph-kem/issues/208#issuecomment-6215551334). The new scoped derivation is the **exact residual mean/variance** after removing the full null linear projection of Z3 onto Z2. Classical incidence counting is not a new hardness assumption.

## 1. Unmodified original tensor source

Let V=F_q^n, q any prime power (also characteristic two), 3<=d<n, m>=1. The null public tuple contains m iid unrestricted uniform alternating bilinear forms A_i; the planted tuple first chooses an arbitrary unconditional d-plane H-distribution and then iid **uniform** alternating forms satisfying A_i|_(H x H)=0. No sample filtering. The complete original verifier accepts **any** rank-d matrix Y satisfying Y^T A_i Y=0 for every slice.

For each r, Z_r is the mathematical number of common isotropic r-planes. This does not supply a polynomial public algorithm evaluating Z_r. Put

\[
L=[n\choose2]_q,\quad G=[n\choose3]_q,\quad
M=[n-2\choose1]_q,\quad
a=[3\choose2]_q=q^2+q+1,\quad p=q^{-m},
\]
\[
B=M p^2,\qquad D_3=Z_3-B Z_2,\qquad
F(p)=(1-p)(1-qp)(1+(q+1)p).
\]

The rational-valued D_3 is a **formal statistic**, not a replacement original verifier, a public witness, or a promised efficient distinguisher.

## 2. Exact null projection, variance and planted mean shift

**Theorem 1 (all finite parameters and every unconditional planted H-prior).**

\[
\boxed{
\operatorname{Cov}_0(Z_3,Z_2)=LMp^3(1-p),\quad
\operatorname{Var}_0(Z_2)=Lp(1-p),\quad
\operatorname{Cov}_0(D_3,Z_2)=0.
}
\]

In particular B is the **exact** null least-squares linear-projection coefficient, not just an asymptotic approximation. Moreover,

\[
\boxed{\operatorname{Var}_0(D_3)=Gp^3 F(p),\qquad
\mathbb E_{\rm pl}D_3-\mathbb E_0D_3=[d\choose3]_q F(p).}
\]

For m=1, F(q^{-1})=0, while for every m>=2, F(q^{-m})>0. When m>=2 the exact standardized planted mean shift relative to the **null** standard deviation is

\[
\boxed{
\frac{\mathbb E_{\rm pl}D_3-\mathbb E_0D_3}
{\sqrt{\operatorname{Var}_0(D_3)}}
=\frac{[d\choose3]_q}{\sqrt{[n\choose3]_q}}\,
 q^{3m/2}\sqrt{F(q^{-m})}.
}
\]

**Proof of null identities.** Every 3-plane contains a=[3 choose2]_q 2-planes; every 2-plane belongs to M=[n-2 choose1]_q 3-planes. Hence the incidence identity Ga=LM. Applying the [exact cross-dimensional covariance theorem](F0-isotropic-subspace-mixed-covariance-rank-one.md#2-exact-cross-dimensional-null-covariance) with (r,k)=(3,2) gives Cov_0(Z3,Z2)=Ga(p^3-p^4)=LMp^3(1-p); the already proved 2-plane variance is Lp(1-p). Thus B=Cov(Z3,Z2)/Var(Z2)=Mp^2 and the residual is null-orthogonal to Z2.

The [all-r variance formula](F0-isotropic-subspace-second-moment-boundaries.md#2-null-law-exact-variance-in-all-dimensions) for r=3 gives, with N_{3,2}=a q[n-3 choose1]_q,

\[
\operatorname{Var}_0(Z_3)=
G N_{3,2}\,p^5(1-p)+Gp^3(1-p^3).
\]

Double-count triples (common isotropic status is irrelevant for the incidence): select an isotropic-*unrestricted* abstract 2-plane L and two 3-planes J,K containing it. This gives the combinatorial identity

\[
LM^2=G(N_{3,2}+a),
\]

because J cap K has dimension 2 or 3, and a pair equal at a 3-plane is counted a times. Subtract B^2 Var_0(Z2) from Var_0(Z3), obtaining

\[
\operatorname{Var}_0(D_3)
=G[p^3(1-p^3)-a p^5(1-p)]
=Gp^3(1-p)(1-qp)(1+(q+1)p).
\]

**Proof of planted shift.** The already proved all-r first moments give Delta_2=[d choose2]_q(1-p). Let C_t be the number of 3-planes J with dim(J cap H)=t. For t=2,3,

\[
\Delta_3=\mathbb E_{\rm pl}Z_3-\mathbb E_0 Z_3
=p^3\left[C_2(p^{-1}-1)+[d\choose3]_q(p^{-3}-1)\right].
\]

Count the incidences (L,J) with L a 2-plane of H and J a 3-plane containing L: [d choose2]_q M=C_2+a[d choose3]_q. Subtract B Delta_2: the **entire t=2 planted contribution cancels identically**, leaving

\[
\Delta_{D_3}
=[d\choose3]_q p^3\big[(p^{-3}-1)-a(p^{-1}-1)\big].
\]

Using a=q^2+q+1, the bracket factors as
\((p^{-1}-1)(p^{-1}-q)(p^{-1}+q+1)\), whose product with p^3 is exactly F(p). This proves both identities. The formula depends only on dim H=d, so averaging over any unconditional H-prior changes nothing.

## 3. Single-slice pointwise collapse, not merely zero variance

**Theorem 2 (every alternating form, no probability).** When the entire public slice span has dimension at most one, including m=1, the following identity holds *on every public tuple*:

\[
\boxed{M Z_2=(q+1)G+q^2Z_3.}
\]

**Proof.** Count (J,L), where J is any 3-plane and L is an isotropic 2-plane contained in J. Each isotropic L has exactly M containing 3-planes, so the total is M Z_2. If the single underlying alternating form restricts to zero on J, all a=q^2+q+1 constituent 2-planes are isotropic. If it restricts nontrivially, an alternating form on a 3-space has rank two and a one-dimensional radical; exactly q+1 of its 2-planes contain that radical and are isotropic. Summing over the Z_3 zero-restriction planes and G-Z_3 other 3-planes yields MZ_2=a Z_3+(q+1)(G-Z_3)=(q+1)G+q^2Z_3.

Consequently for m=1, B=M/q^2 and D_3 is the **pointwise constant** -(q+1)G/q^2, agreeing with F(1/q)=0. This is compatible with the [previous full-verifier public section for one alternating slice](F0-one-alternating-form-rank-screen.md), and is *not* a new attack against the multislice d<c source.

## 4. Sparse-regime comparison and independent finite check

Assume q is fixed, d/n -> alpha with 0<alpha<1/2, and 2<=m=o(n). Since F(q^{-m}) is uniformly bounded above and **away from zero** for m>=2, the exact mean-to-null-noise formula gives

\[
\frac{\Delta_{D_3}}{\sqrt{\operatorname{Var}_0(D_3)}}
=\Theta_q(q^{3d-\frac32 n+\frac32m})=q^{-\Omega(n)}.
\]

Thus the concrete null-orthogonal projection suppresses the common r=2 noise but **also exactly removes the t=2 planted mean contribution**; its remaining first-moment signal is exponentially small relative to null standard deviation when d<n/2 by a fixed fraction. This is a statement about **one predeclared abstract linear count contrast**, not a proof that arbitrary optimized statistics fail.

For a separate tiny arithmetic cross-check, at q=2,n=4,d=3,m=2, fully enumerating the 4,096 ordered unrestricted pairs of alternating forms and 64 ordered planted pairs for a fixed 3-plane H gives

\[
\operatorname{Var}_0(D_3)=315/2048,\qquad
\mathbb E_{\rm pl}D_3-\mathbb E_0D_3=21/32,
\]

matching the formulas exactly. This scratch enumeration is **not** a committed benchmark or measured cryptanalytic attack. In particular, there is no claimed public Z_2/Z_3 counter in the sparse high-dimensional regime.

## 5. Strict boundaries

- The fixed-r null covariance theorem and this exact r=3 contrast do not imply TV indistinguishability of planted and unrestricted tensor distributions.
- The statistic D_3 may be exponentially expensive to compute from published tensors for multiple independent slices. No feasible distinguisher or full-original-verifier inversion follows.
- A nonlinear statistic, a higher-dimensional count, residual contrasts of several dimensions, higher moments, adaptive MinRank or matrix-pencil invariants may behave differently.
- The new pointwise one-slice identity is a **public easy-subclass screen** and inherits an established public section; it is not a positive independently novel MORPH-R0 Field-15 basis.

**Disposition:** ANALYTIC STATISTICS NEGATIVE CONTROL, **NO NOMINATION**, H-A/H-B/H-C HOLD, N1-60 unallocated, HEPMR BENCHMARK ONLY, no code/README/stage-registry changes.
