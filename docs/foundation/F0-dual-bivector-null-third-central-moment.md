# MORPH-F0: exact null third central moment of decomposable-bivector survival counts

**Planted-source follow-up:** [exact third central moment using four projective quotient-line types](F0-dual-bivector-planted-third-central-moment.md), including the sparse-regime relative comparison. No efficient tensor counter, TV or security claim follows.

**2026-10-19. Paper-only, attack-first statistics screen; GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.** Extends the [previous exact first/second bivector moments](F0-dual-bivector-kernel-exact-source-moments.md) and the [all-r variance hierarchy](F0-isotropic-subspace-second-moment-boundaries.md) without claiming a new independent cryptographic foundation. No N1/F0-K/A-ID, source experiments, executable counter, PKE/KEM/trapdoor or security theorem.

**Origin and credit.** The external planted alternating-tensor problem is Liu, Qiao, Tang and Zhang, *The planted tensor problem over finite fields: algorithms and cryptography*, [arXiv:2609.31256v1](https://arxiv.org/abs/2609.31256). The earlier r=2 null expectation/variance and planted second moments are already documented in the linked notes and PR #231. This scoped addition derives the **exact null third central moment** and classifies the only source of third-order dependence through classical projective lines on the Grassmannian. It is elementary finite geometry, not a novel hardness assumption.

## 1. The unchanged public law and mathematical statistic

Let V=F_q^n for any prime power q>=2 (including characteristic two), n>=3, and m>=1. Under the **null** law, publish m independent unrestricted uniform alternating bilinear forms A_i on V; use zero-diagonal matrices in characteristic two. Under the **planted** law, the original honest sampler first chooses a d-plane H by any specified unconditional distribution and samples independent uniform forms annihilating Lambda^2H. No conditioning on a convenient observed rank or accepted witness is permitted. The original full verifier continues to accept any rank-d Y satisfying Y^T A_i Y=0 for **every** i.

Let X=Z_2 be the number of **projective decomposable bivector lines** in the common public annihilator, or equivalently the number of 2-planes J on which all m forms vanish. Put

\[
T=[n\choose2]_q,\quad p=q^{-m},\quad
F=[n\choose1]_q[n-1\choose2]_q.
\]

Here F is the number of **flags** (U,W) with U a 1-plane and W a 3-plane containing U. The previously proved exact null results are E_0X=Tp and Var_0(X)=Tp(1-p), because all **distinct projective decomposable lines** produce pairwise independent survival events.

## 2. Exact third central moment under the unrestricted null law

**Theorem 1 (finite and exact for all q,n,m as above).**

\[
\boxed{\mathbb E_0[(X-\mathbb E_0 X)^3]
=Tp(1-p)(1-2p)
+F(q+1)q(q-1)\,p^2(1-p).}
\]

The second term is strictly positive and comes **only** from ordered triples of distinct projective decomposable lines that are linearly dependent in Lambda^2V. Consequently a binomial(T,p) model for X is in general false even though all distinct survival indicators are pairwise independent.

**Proof.** Write X=sum_{J in Gr(2,V)} I_J, with I_J the common-isotropy indicator. Uniform alternating slices are uniform independent linear functionals on Lambda^2V. Therefore any k projective bivector representatives of linear span dimension s survive jointly with probability q^{-ms}=p^s.

Expand E[(sum_J(I_J-p))^3] over ordered triples (J,K,L):

1. If J=K=L, its contribution is E[(I_J-p)^3]=p(1-p)(1-2p); there are T such triples.
2. If exactly two indices coincide, the term is zero: (I_J-p)^2=(1-2p)I_J+p^2, and distinct I_J,I_K are pairwise independent.
3. If the three indices are distinct and their bivectors are linearly independent, their indicators are mutually independent, and the centered triple contribution vanishes.
4. If three **distinct** projective decomposable bivectors have span dimension two, their pairwise survival events remain independent but the triple survival probability is p^2 (rather than p^3). Its centered contribution is p^2-p^3=p^2(1-p).

To count case (4), recall/prove the elementary Plücker-line criterion: for two distinct 2-planes J,K, a nontrivial linear combination of their decomposable exterior-square representatives is itself decomposable **if and only if** dim(J cap K)=1. Indeed, with a common vector h, both bivectors factor as h wedge v and h wedge w, so all points of their projective line are decomposable. Conversely, if J cap K=0, their four spanning vectors are independent, and every nonzero combination with both coefficients nonzero has exterior rank four, including in characteristic two, so cannot be a wedge of two vectors. Thus each projective line entirely in the Grassmannian corresponds **uniquely** to a flag U=J cap K inside W=J+K of dimensions (1,3).

There are exactly F such flags. Every corresponding projective line has q+1 distinct points. The number of **ordered triples of distinct** points on it is (q+1)q(q-1). A dependent ordered triple with distinct points determines a unique projective line, so there is no overcount. Summing all contributions gives Theorem 1.

## 3. Exact normalized skewness and the sparse regime

Since Var_0(X)=Tp(1-p), the standardized null skewness is exactly

\[
\boxed{
\gamma_{1,0}=
\frac{Tp(1-p)(1-2p)+F(q+1)q(q-1)p^2(1-p)}
{[Tp(1-p)]^{3/2}}.
}
\]

For **fixed q**, n->infinity and 1<=m=o(n), Gaussian-binomial growth yields T=Theta_q(q^{2n-4}) and F=Theta_q(q^{3n-7}); the flag contribution dominates the single-variable Bernoulli contribution by a factor Theta_q(q^{n-m}). Consequently

\[
\boxed{\gamma_{1,0}=\Theta_q(q^{-m/2})}
\]

where constants depend on q but are uniform for any integer m>=1 with m=o(n). Thus in the externally discussed m=ceil(n/log n) range the null standardized third moment tends to zero. This is **one moment statement**, not a central limit theorem, Gaussian tail bound, concentration at rare events, total-variation comparison, computational lower bound or hardness evidence. For bounded m it generally converges to a nonzero positive constant.

## 4. Independent finite arithmetic checks (not committed attack experiments)

For q=2,n=4 there are T=[4 choose2]_2=35 projective 2-planes and F=[4 choose1]_2[3 choose2]_2=15*7=105 projective Grassmann lines. The underlying alternating-form space has dimension binom(4,2)=6 over GF(2).

- For m=1 (all 64 null forms exhaustively enumerated in a separate scratch calculation), E[X]=35/2, Var(X)=35/4 and E[(X-E X)^3]=315/4. Theorem 1 gives the identical rational 315/4.
- For m=2 (all 64^2=4096 ordered unrestricted pairs enumerated separately), E[X]=35/4 and E[(X-E X)^3]=525/16; again the exact formula agrees.

These are finite **formula checks**, not published source benchmarks, new CI tests or measured attacker success. They do not change the original honest generation distribution.

## 5. Cryptanalytic interpretation and unresolved work

Pairwise independence does **not** extend to higher moments because the Plücker-embedded Grassmannian contains projective lines. Classical rank-two null variance alone loses the contribution of such incidence-dependent triples. However, in the fixed-q sparse m=o(n) scaling the standardized null skew vanishes; this still cannot rule out a strong nonlinear or tail-based detector. The planted **third central moment is not evaluated here**; the earlier [exact planted quotient-line variance](F0-dual-bivector-kernel-exact-source-moments.md#3-planted-law-exact-expectation-and-the-entire-covariance-structure) has nontrivial same-fibre dependence and cannot be replaced by the null expression.

No polynomial-time method to evaluate X on arbitrary published m-slice tensors is obtained; it is generally a combinatorial count across exponentially many 2-planes. No original-verifier accepted d-plane is recovered. Full planted/null TV, planted skew, tail likelihood, optimized public MinRank, and all-r source-level search remain separate problems; the external tensor relation does not clear the MORPH-R0 originality gate.

**Disposition:** EXACT NULL HIGHER-MOMENT NEGATIVE CONTROL, **GLOBAL NO NOMINATION**, H-A/H-B/H-C HOLD. N1-60 unallocated. HEPMR BENCHMARK ONLY. README and stage registry unchanged.
