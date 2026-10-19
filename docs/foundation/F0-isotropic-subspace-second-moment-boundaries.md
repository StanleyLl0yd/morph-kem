# MORPH-F0: exact null variance and planted covariance of all-r isotropic-subspace counts

**Mixed-dimensional follow-up:** [cross-(r,k) covariance and rank-one null fluctuations](F0-isotropic-subspace-mixed-covariance-rank-one.md) refine the joint null moment picture; they do not change the full original verifier or planted law.

**2026-10-19. Source-first mathematical negative control; not a cryptographic construction.** GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD. This extends the [all-r first-moment hierarchy](F0-isotropic-subspace-first-moment-hierarchy.md) and is consistent with the [previous exact rank-two variance](F0-dual-bivector-kernel-exact-source-moments.md). No new N1/F0-K or attack ID, candidate, source experiments, OWF/PKE/KEM/trapdoor, or hardness claim.

**Credit and scope.** The external planted alternating-tensor problem is attributed to Liu, Qiao, Tang and Zhang, *The planted tensor problem over finite fields: algorithms and cryptography*, [arXiv:2609.31256v1](https://arxiv.org/abs/2609.31256). Exact planted size-bias and d-witness rarity were previously recorded in [#208 comment 6215551334](https://github.com/StanleyLl0yd/morph-kem/issues/208#issuecomment-6215551334); the rank-two moment result was merged in PR #231. These are not rediscovered or re-nominated here. The scoped addition is an explicit Gaussian-binomial **null variance for every r**, a general exact **conditional planted covariance kernel**, and a fixed-r sparse asymptotic mean-shift-to-null-noise comparison.

## 1. Full public source and statistic

Over F_q for any prime power q >= 2, let V=F_q^n, 2 <= d < n, c=n-d and m>=1. Let A_1,...,A_m be independent unrestricted uniform alternating bilinear forms under null. Under planted, choose a d-plane H from any specified **unconditional** honest distribution, then independently draw A_i uniformly from the alternating forms vanishing on H x H. This is the *entire* source, without rank filtering or acceptance postselection. Characteristic two uses zero-diagonal alternating forms.

For 1 <= r <= d let Z_r be the number of r-planes J <= V on which **all** public forms vanish. This is a mathematical count, not a polynomial-time oracle; the original any-witness verifier still asks for a full-rank n-by-d matrix Y satisfying Y^T A_i Y=0 for every i. Write b_k=binom(k,2), G_r=[n choose r]_q. The previously established means are

\[
\mu_0=E_0 Z_r=G_r q^{-m b_r},\qquad
\mu_{\rm pl}=E_{\rm pl} Z_r
=\sum_t [d\choose t]_q[c\choose r-t]_q
 q^{(d-t)(r-t)}q^{-m(b_r-b_t)}.
\]

Gaussian-binomial symbols are understood to vanish for invalid indices.

## 2. Null law: exact variance in all dimensions

For a fixed r-plane J, the exact number of r-planes K meeting J in dimension s is

\[
N_{r,s}=[r\choose s]_q[n-r\choose r-s]_q q^{(r-s)^2},
\quad \max(0,2r-n)\le s\le r.
\]

**Theorem 1.** For every q,n,m and r in the specified range,

\[
\boxed{\operatorname{Var}_0(Z_r)=
G_r\sum_{s=2}^{r}N_{r,s}
\left(q^{-m(2b_r-b_s)}-q^{-2m b_r}\right).}
\]

For r=1 the sum is empty and the statistic is deterministic. For r=2 this reduces **exactly** to the already merged result, G_2 q^{-m}(1-q^{-m}); the new cases are r>=3. Every summand is nonnegative.

**Proof.** For two r-planes J,K with intersection dimension s, the elementary exterior-square identity gives

\[
\Lambda^2J\cap\Lambda^2K=\Lambda^2(J\cap K),
\quad \dim(\Lambda^2J+\Lambda^2K)=2b_r-b_s.
\]

A uniform unrestricted alternating form has independent uniform evaluations on a basis of that sum. Therefore

\[
\Pr_0(J,K\text{ both isotropic for all }m)
=q^{-m(2b_r-b_s)}.
\]

Individually each event has probability q^{-m b_r}; subtract their product and sum over all ordered (J,K). To count K, first select S=J cap K as a s-plane in J, then select its image as an (r-s)-plane in V/J and a graph map into J/S; there are q^{(r-s)^2} graphs. For s=0 or 1, b_s=0 and covariance vanishes. This proves the formula. **Pairwise independence holds for r=2 only**, not for larger r.

**Exact small finite-field cross-check (not a repository benchmark):** at q=2,n=4,m=1, direct enumeration of all 2^6 unrestricted alternating forms yields for r=2: (E_0 Z_2,Var_0 Z_2)=(35/2,35/4), and for r=3: (E_0 Z_3,Var_0 Z_3)=(15/8,315/64). Both equal Theorem 1. The enumeration is an independent scratch arithmetic check, not a CI addition or attack success.

## 3. Planted law: exact covariance kernel, without a false independence shortcut

Fix the planted H. Put U=Lambda^2 H and let Q=(Lambda^2 V)/U. For an r-plane J define

\[
W_J=(\Lambda^2J+U)/U\le Q,\quad
a_J=\dim W_J=b_r-b_{\dim(J\cap H)}.
\]

For a pair J,K define \(\rho_{J,K}=\dim(W_J+W_K)\); this is computable *from the pair of subspaces and H* by a finite-field matrix rank calculation. It is **not** asserted efficiently available from the public tuple without H.

**Theorem 2 (exact fixed-H conditional covariance).**

\[
\boxed{\operatorname{Cov}_{\rm pl}(1_J,1_K\mid H)
=q^{-m\rho_{J,K}}-q^{-m(a_J+a_K)}\ge0.}
\]

Consequently,

\[
\boxed{\operatorname{Var}_{\rm pl}(Z_r\mid H)
=\sum_{J,K\in\operatorname{Gr}(r,V)}
\left(q^{-m\rho_{J,K}}-q^{-m(a_J+a_K)}\right).}
\]

**Proof.** A planted slice is a uniform linear functional on Q. The evaluations on W_J+W_K vanish together with probability q^{-rho_{J,K}} for one slice, and independently across m slices. The individual probabilities are q^{-a_J} and q^{-a_K} per slice. Since rho <= a_J+a_K, covariances are nonnegative. The joint rank is equivalently dim(Lambda^2J+Lambda^2K+U)-dim U. The conditional mean is independent of the specific d-plane H by the GL(V) action (indeed the previously derived Gaussian-binomial formula depends only on n,d,r,q,m); therefore the law of total variance adds **zero** between-H mean term. The displayed sum equals the unconditional planted variance for any unconditional H-prior.

This is an **exact exponential incidence sum**, not a closed Gaussian-binomial evaluation for arbitrary r and not an efficient public counter. In particular, simply replacing rho by a_J+a_K-b_s+b_dim(J cap K cap H) can fail: quotient images can overlap beyond the literal intersection of Lambda^2J and Lambda^2K. For r=2, quotient-line fibre classification collapses the formula to the *already established* explicit planted variance in the [rank-two note](F0-dual-bivector-kernel-exact-source-moments.md). For r>=3, further orbit/fibre classification would be required for a comparably compact planted expression.

## 4. Fixed-r sparse asymptotic: all dimensions share the rank-two noise exponent

Assume q fixed, integer r>=2 fixed, n goes to infinity, d/n -> alpha with 0<alpha<1/2, c=n-d, and 1<=m=o(n). The planted source is exactly the conditional-uniform source in Section 1. The symbols Theta below hide constants depending only on q and r (for fixed alpha), and do **not** refer to timing or feasible computation.

**Theorem 3.**

\[
\begin{aligned}
\mu_{\rm pl}-\mu_0
 &=\Theta_{q,r}(q^{r(n-r)-m b_r-2c+m}),\\
\operatorname{Var}_0(Z_r)
 &=\Theta_{q,r}(q^{(2r-2)n-m(2b_r-1)}),\\
\frac{\mu_{\rm pl}-\mu_0}{\sqrt{\operatorname{Var}_0(Z_r)}}
 &=\Theta_{q,r}(q^{2d-n+m/2})=q^{-\Omega(n)}.
\end{aligned}
\]

**Proof of the first line.** In the exact first-moment ratio, T=dim(J cap H) for a uniform r-plane obeys, for each fixed t with 2<=t<=r,

\[
\Pr(T=t)=\Theta_{q,r}(q^{-tc}) .
\]

The t-th difference contribution has exponent -tc+m b_t; since m=o(n) and c=Theta(n), t=2 uniquely dominates all t>2 by an exponentially vanishing relative factor. With m>=1, q^m-1=Theta(q^m), and G_r=Theta(q^{r(n-r)}), yielding line one.

**Proof of the second line.** In Theorem 1, the s=2 contribution has the positive factor 1-q^{-m}, bounded away from zero, and N_{r,2}=Theta(q^{(r-2)n}). Every s>2 contributes exponentially less: its ratio to the s=2 term has exponent -(s-2)n+m(b_s-1)+O_{q,r}(1)=-Omega(n). This includes r=2, where only the diagonal s=2 term exists. Taking a square root and simplifying exponents proves the last line.

For the externally discussed fixed-C sparse regime, d=ceil(n/C), C>=3, m=ceil(n/log n), this standardized **mean shift** vanishes exponentially for **every fixed r**, extending the previous r=2 calculation. Its leading exponent is independent of r because shared 2-dimensional intersections dominate null covariance at all fixed r>=2. It would be **incorrect** to infer the same conclusion for growing r=Theta(log n): the fixed-r asymptotic does not have uniform constants in r and needs separate treatment.

## 5. Attack-first interpretation and limits

- Theorem 1 is a closed exact **null second moment**. Theorem 2 is an exact **planted covariance kernel**, but its sum still ranges over exponentially many subspaces.
- Theorem 3 compares a *mean shift* with **null** standard deviation; it neither upper-bounds TV distance of the statistic's full distributions nor proves impossibility of distinguishing them. A large-tail or optimized statistic can evade a naive mean-based test.
- None of these moments makes Z_r polynomial-time computable from public alternating slices or recovers a valid d-plane. The original search task and the unresolved d<c region remain open to different attacks, especially growing-r dependencies, optimized public matrix-pencil invariants and full-verifier search.
- At r=d, the **previously known** d-witness null rarity / size-bias can yield an information-theoretic detector; fixed-r mean noise suppression is not a statement about all r.
- No direct evidence for a genuinely novel independent Field-15 hard relation has been obtained. The external tensor problem remains a maturity/novelty gate, not a nominated MORPH foundation.

**Disposition:** ANALYTIC NEGATIVE CONTROL ONLY. GLOBAL NO NOMINATION. H-A/H-B/H-C HOLD. Research strategy 80/20 unchanged; N1-60 unallocated; HEPMR remains BENCHMARK ONLY. README and stage registry need no change.
