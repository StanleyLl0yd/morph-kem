# MORPH-F0: mixed-dimensional isotropic-count covariance and rank-one null fluctuations

**Follow-up screen:** [exact Z3 minus null-projection Z2 contrast](F0-isotropic-three-plane-orthogonal-contrast.md) evaluates a residual direction rather than assuming leading null-correlation alone rules it out.

**2026-10-19. Analytical-only source moment boundary.** GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD. Follows the [all-r first moments](F0-isotropic-subspace-first-moment-hierarchy.md) and [same-dimensional second moments](F0-isotropic-subspace-second-moment-boundaries.md); neither earlier result is re-announced as an independent new foundation. No source modification, implemented public attack, experimental artifact, cryptographic security claim, or new N1/F0-K number.

**External problem and priority:** Liu, Qiao, Tang and Zhang, *The planted tensor problem over finite fields: algorithms and cryptography*, [arXiv:2609.31256v1](https://arxiv.org/abs/2609.31256). Earlier exact planted size-bias and full-d null-witness rarity are [#208 comment 6215551334](https://github.com/StanleyLl0yd/morph-kem/issues/208#issuecomment-6215551334). The precise scoped addition here is the **joint second-moment matrix across distinct r,k**, with an asymptotic leading-rank-one identity under *null*. It does not purport to invent the underlying Grassmann incidence counting.

## 1. The unchanged full relation and source

Let V=F_q^n, q any prime power including 2, 2<=d<n, m>=1. Null publishes m independent uniform alternating forms on V. Planted first draws a d-plane H from any **unconditional** distribution, then publishes independent uniform alternating forms constrained to vanish on H x H, without filtering. Alternating forms have zero diagonal even in characteristic two.

For a dimension j with 1<=j<=d, let Z_j count all j-dimensional subspaces isotropic under **every** public form; put b_j=binom(j,2). The actual equivalent-witness verifier still accepts **any** rank-d matrix Y with Y^T A_i Y=0 for all i. Nothing in this count grants an oracle evaluating Z_j efficiently from the public tuple.

## 2. Exact cross-dimensional null covariance

Fix 1<=r,k<=d. Given an r-plane J, the number of k-planes K with s=dim(J cap K) is

\[
N_{r,k,s}=[r\choose s]_q[n-r\choose k-s]_q q^{(r-s)(k-s)}
\]

for max(0,r+k-n)<=s<=min(r,k), and zero otherwise.

**Theorem 1 (all finite n,q,m,r,k).**

\[
\boxed{\operatorname{Cov}_0(Z_r,Z_k)
=[n\choose r]_q
\sum_{s=2}^{\min(r,k)}
N_{r,k,s}\,
q^{-m(b_r+b_k)}(q^{m b_s}-1).}
\]

If min(r,k)=1 this sum is empty, consistently with the deterministic isotropic line count. Taking k=r recovers precisely the [previous all-r variance](F0-isotropic-subspace-second-moment-boundaries.md#2-null-law-exact-variance-in-all-dimensions). Every entry of the null covariance matrix is nonnegative.

**Proof.** The independent unrestricted alternating slices jointly annihilate Lambda^2J+Lambda^2K, whose dimension is b_r+b_k-b_s because Lambda^2J cap Lambda^2K=Lambda^2(J cap K). Hence the joint event has probability q^{-m(b_r+b_k-b_s)}, versus the marginal product q^{-m(b_r+b_k)}. Count ordered pairs (J,K) by choosing J and then its intersection s, the image of K in V/J and a graph to J/(J cap K); the graph factor is q^{(r-s)(k-s)}. For s=0,1, b_s=0 and covariance is zero. No independence between three or more indicators is claimed.

**Exact arithmetic check (independent scratch enumeration; no committed benchmark):** q=2,n=4,m=1, r=2, k=3. Exhaustively traversing all 2^6 null alternating forms gives E_0 Z_2=35/2, E_0 Z_3=15/8 and Cov_0(Z_2,Z_3)=105/16, as the formula predicts. The same enumeration matched both previously derived diagonal variances, 35/4 and 315/64.

## 3. Exact planted cross-dimensional kernel

For fixed H put U=Lambda^2H and, for each j-plane J, set W_J=(Lambda^2J+U)/U. Let a_J=dim W_J=b_j-b_dim(J cap H). For any r-plane J and k-plane K set rho(J,K)=dim(W_J+W_K).

**Theorem 2 (all finite parameters, fixed H).**

\[
\boxed{\operatorname{Cov}_{\rm pl}(Z_r,Z_k\mid H)
=\sum_{J\in\operatorname{Gr}(r,V)}
 \sum_{K\in\operatorname{Gr}(k,V)}
 \left(q^{-m\rho(J,K)}-q^{-m(a_J+a_K)}\right).}
\]

Each summand is nonnegative. The mean of Z_j conditional on H depends only on its dimension d, not H itself, so the *unconditional* planted covariance equals the displayed value under **any** unconditional H-prior.

**Proof.** The conditional planted forms induce m independent uniform linear functionals on (Lambda^2V)/U. Their simultaneous annihilation of W_J+W_K has probability q^{-m rho(J,K)}. Multiplying the individual probabilities gives q^{-m(a_J+a_K)}. GL(V) transitivity makes both conditional means independent of H, so the total-covariance correction from varying H vanishes. This exact expression is generally an exponentially large incidence sum, not a compact closed Gaussian-binomial formula or a public counting algorithm. The quotient images can have nontrivial intersections not deducible solely from dim(J cap K) and dim(J cap K cap H).

## 4. Sparse fixed-dimensional null fluctuations collapse to one leading direction

Let q>=2 be fixed, r,k>=2 be **fixed** integers, n grow, and 1<=m=o(n). Introduce

\[
L=[n\choose2]_q,\qquad
M_j=[n-2\choose j-2]_q,\qquad
B_j=M_j\,q^{-m(b_j-1)}.
\]

Here M_j is exactly the number of j-planes containing a fixed 2-plane, and B_2=1.

**Theorem 3 (asymptotically rank-one covariance).**

\[
\boxed{
\operatorname{Cov}_0(Z_r,Z_k)
=(1+o(1))\,L M_r M_k\,
q^{-m(b_r+b_k-1)}(1-q^{-m})
=(1+o(1))\,B_rB_k\operatorname{Var}_0(Z_2).
}
\]

The approximation applies simultaneously to any **fixed finite** collection of dimensions. In particular

\[
\operatorname{Corr}_0(Z_r,Z_k)\longrightarrow1,
\qquad
\frac{\mathbb E_0[((Z_r-\mathbb E_0Z_r)-B_r(Z_2-\mathbb E_0Z_2))^2]}
{\operatorname{Var}_0(Z_r)}\longrightarrow0.
\]

**Proof.** The s=2 summand of Theorem 1 counts ordered pairs whose intersection is exactly a 2-plane. Alternatively, choose a common 2-plane L (there are [n choose2]_q), then choose J and K containing L independently (M_r M_k choices). This *double counts* a pair meeting in a larger s by [s choose2]_q, but for fixed r,k and large n the share with s>=3 is O_{q,r,k}(q^{-n}) of the s=2 share. The weighted contributions with s>=3 gain at most q^{m(b_s-1)}, which cannot overcome their q^{-(s-2)n+O_{q,r,k}(1)} incidence suppression when m=o(n). Thus the s=2 covariance contribution is asymptotic to L M_r M_k q^{-m(b_r+b_k-1)}(1-q^{-m}). Taking r=k and separately r=2,k=j yields the normalized-correlation and L^2-projection conclusions by the identity Var_0(Z_2)=L q^{-m}(1-q^{-m}).

The same-dimensional [mean-to-null-noise exponent](F0-isotropic-subspace-second-moment-boundaries.md#4-fixed-r-sparse-asymptotic-all-dimensions-share-the-rank-two-noise-exponent) q^{2d-n+m/2}, for fixed r and d/n<1/2, therefore cannot be treated as a collection of *independent* leading-order signals merely by counting different fixed dimensions. **However**, lower-order linear contrasts may suppress this common noise and amplify otherwise hidden information: the rank-one limit does **not** establish such contrasts are harmless.

## 5. What is not established

- This is a property of **null** second moments and a formal planted covariance kernel. It does **not** prove the planted covariance matrix has the same rank-one asymptotics.
- Fixed dimensions must not be silently replaced by r growing with n (especially r=Theta(log n)); contributions with s>=3 can change the dominant saddle point.
- Neither the exact counts Z_j nor their optimal linear contrasts are established polynomial-time computable from a public tensor.
- Correlation converging to one, L^2 coupling and an exponentially small standardized *mean* shift say **nothing on their own** about planted-vs-null TV, distinguishability by nonlinear statistics, computational inversion, post-quantum security, or the novelty of a hard relation.

**Disposition:** ANALYTICAL NULL-COVARIANCE STRUCTURE, no candidate and no empirical attack. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD. N1-60 remains unallocated; HEPMR remains BENCHMARK ONLY. README and stage registry unchanged.
