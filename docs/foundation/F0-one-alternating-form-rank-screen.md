# MORPH-F0: one alternating form is publicly invertible; rank is sufficient for ideal planted-vs-null detection

**Date:** 2026-10-16. **Status:** analytical attack-first screen of an **existing** planted totally-isotropic (TI) relation, not a MORPH assumption. **GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.** Unnumbered research pass; no N1/F0-K reservation, trials, test cases, source draws, code or candidate/OWF/PQ/PKE/KEM/trapdoor claims.

## 1. Original full any-witness verifier (any honest source)

Fix a public effectively represented finite field \(K=\mathbb F_q\), \(n\ge1\), \(1\le d\le n\), and **one** public \(n\times n\) alternating matrix \(A\). "Alternating" means \(v^TAv=0\) for all vectors, including *zero diagonal* in characteristic two; merely assuming \(A^T=-A\) is insufficient in characteristic two. The original verifier accepts precisely

\[
E(A,d)=\{Y\in K^{n\times d}:\operatorname{rank}Y=d,\quad Y^TAY=0\}.
\]

Any basis for any \(d\)-dimensional totally isotropic space wins; the planted space need not be found. This is the **single-slice** \(m=1\) limit of the independently developed [Liu–Qiao–Tang–Zhang planted tensor problem (2026)](https://arxiv.org/abs/2609.31256). The earlier [universal small-d algorithm for *m* slices](https://github.com/StanleyLl0yd/morph-kem/issues/208#issuecomment-6214371503) only guaranteed \(d\le\lceil n/(m+1)\rceil\). The following exact single-slice algorithm works at **every feasible d**, including degenerate matrices with \(d>\lceil n/2\rceil\).

## 2. Pointwise deterministic polynomial any-witness inversion for every feasible d

Write \(\operatorname{rank} A=2r\) (even over characteristic two), and \(k=n-2r=\dim\operatorname{rad}A\). By public alternating Gram-Schmidt / symplectic elimination, find an invertible basis change giving an orthogonal direct sum of \(r\) hyperbolic pairs and a \(k\)-dimensional radical. More concretely, whenever the remaining form is nonzero, select public \(u,v\) with \(u^TAv\ne0\), normalize \(u^TAv=1\), orthogonalize the remaining vectors against \(u,v\), and recurse on their orthogonal complement. This consists of polynomially many field operations and works in **all** characteristics.

The radical basis \(z_1,\ldots,z_k\) together with one vector \(e_i\) from each hyperbolic pair \(e_i,f_i\) span a totally isotropic space of dimension \(k+r=n-r\). Output **any d** of these linearly independent basis vectors as the \(n\times d\) matrix \(Y\), provided \(d\le k+r\); verify \(\operatorname{rank}Y=d\) and \(Y^TAY=0\) with the **full original verifier**.

The bound is **exact**: for any TI subspace \(W\), the quotient image of \(W\) in the nondegenerate symplectic space \(K^n/\operatorname{rad}A\) has dimension at most \(r\), and \(\dim(W\cap\operatorname{rad}A)\le k\), so \(\dim W\le r+k\). Consequently

\[
E(A,d)\ne\varnothing \iff d\le n-\tfrac12\operatorname{rank}(A).
\]

On **every** honestly generated single-slice planted YES instance, this public algorithm succeeds with probability exactly one, regardless of the source's hidden-subspace distribution, radical size or solution multiplicity. The algorithm does not recover the planted basis or infer any security property.

## 3. Exact rank-only likelihood for the *ideal uniform planted law*

This section is **distribution-specific**, unlike §2. It analyzes a mathematically exact ideal law; it must not be conflated with a strictly worst-case-bounded exact-uniform sampler.

Let \(N=\binom n2\), \(c=\binom d2\), \(G={n\brack d}_q\) (Gaussian binomial). Define \(Q_0\) by taking \(A\) uniformly from the \(q^N\) alternating matrices. Define \(Q_{\rm pl}\) by first choosing \(V\) **uniformly** from \(\mathrm{Gr}(d,n;K)\), then \(A\) uniformly from the \(q^{N-c}\) alternating forms with \(A|_{V\times V}=0\). The condition imposes exactly \(c\) independent linear equations for each \(V\). Both are full, explicitly defined public probability laws; the verifier is still the one in §1.

Let \(I_d(A)\) be the **number of TI d-subspaces** for \(A\). Bayes/counting gives the exact per-matrix likelihood ratio:

\[
Q_{\rm pl}(A)=\frac{I_d(A)}{{n\brack d}_q\,q^{N-c}},\quad
Q_0(A)=q^{-N},\qquad
\frac{Q_{\rm pl}(A)}{Q_0(A)}
  =q^c\frac{I_d(A)}{{n\brack d}_q}.
\]

The posterior on \(V\), conditioned on the public \(A\), is uniform **among the \(I_d(A)\) compatible subspaces** whenever \(I_d(A)>0\). This identity is a rank-specific refinement of the previously recorded general planted-TI posterior count, **not** independent hardness evidence.

### 3.1 Explicit polynomial-time count from the public rank

For \(\operatorname{rank}A=2r\) and \(k=n-2r\), all alternating matrices with this rank are congruent over every finite field, including characteristic two. Hence \(I_d(A)\) depends **only** on \(r\) and \(k\). An explicit count is

\[
I_d(k,r)=
 \sum_{\substack{a+b=d\\0\le a\le k\\0\le b\le r}}
  {k\brack a}_q\ q^{\,b(k-a)}\ J_q(r,b),
\qquad
J_q(r,b)=
 \prod_{j=0}^{b-1}
 \frac{q^{2r-j}-q^{j}}{q^{b}-q^{j}}
\]

(with the empty product \(J_q(r,0)=1\)). Here \(a=\dim(W\cap\operatorname{rad}A)\), \(b=\dim\pi(W)\) in the symplectic quotient. Choose the radical intersection in \({k\brack a}_q\) ways, the isotropic quotient \(b\)-space in \(J_q(r,b)\) ways, and a graph lift \(\pi(W)\to\operatorname{rad}A/(W\cap\operatorname{rad}A)\) in \(q^{b(k-a)}\) ways.

For completeness, the product for \(J_q\) counts ordered mutually orthogonal independent \(b\)-frames in the nondegenerate \(2r\)-space: after \(j\) vectors, the orthogonal complement has \(q^{2r-j}\) elements and the already chosen span has \(q^j\). Divide by the number \(\prod_{j=0}^{b-1}(q^b-q^j)\) of ordered bases of a \(b\)-space. All products and sums use integers of polynomial bitlength \(O(n^2\log q)\) and polynomially many arithmetic operations. No enumeration of the Grassmannian is required.

### 3.2 Exact optimal detector and total-variation formula

The exact number of public alternating matrices of rank \(2r\) is

\[
M_q(n,2r)={n\brack n-2r}_q\,
\frac{|\operatorname{GL}_{2r}(q)|}{|\operatorname{Sp}_{2r}(q)|},
\quad
|\operatorname{Sp}_{2r}(q)|=q^{r^2}\prod_{i=1}^r(q^{2i}-1),
\quad
|\operatorname{GL}_{s}(q)|=\prod_{j=0}^{s-1}(q^s-q^j).
\]

For rank zero the group quotient is \(1\). First choose the radical, then a nondegenerate alternating form on its quotient. Therefore **the conditional public law given rank is identical under \(Q_{\rm pl}\) and \(Q_0\)**; every likelihood-ratio or optimal (equal-prior) hypothesis test can use public rank alone. An exact polynomial-time optimal detector compares \(q^c I_d(k,r)\) with \(G\). Its full-distribution total-variation advantage is exactly

\[
\operatorname{TV}(Q_{\rm pl},Q_0)
 =\frac12\sum_{r=0}^{\lfloor n/2\rfloor}
   \frac{M_q(n,2r)}{q^N}
   \left|q^c\frac{I_d(n-2r,r)}{{n\brack d}_q}-1\right|.
\]

This is an **exact identity**, not a numerical estimate, security bound, or claim that the TV is large for every asymptotic parameter regime. In particular \(d=1\) gives \(I_1(A)={n\brack1}_q\), \(c=0\), and **\(Q_{\rm pl}=Q_0\) exactly**, even though any nonzero vector is an accepted witness. For \(d>n-\operatorname{rank}(A)/2\), \(I_d(A)=0\), and that rank cannot occur in the planted law.

## 4. Honest-generation caveat and decision

The exact \(Q_{\rm pl}\) calculations above use an **ideal uniform Grassmannian source**. If an exact-uniform implementation uses variable-time rejection, one must not advertise a strict worst-case polynomial sampler without proof. An earlier [strict time-bounded near-uniform \(\mathbb F_2\) sampler](https://github.com/StanleyLl0yd/morph-kem/issues/208#issuecomment-6214371503) provides a TV-controlled substitute under its exact stated parameters, but then the rank-only likelihood formula applies **exactly to the ideal law** and to the bounded substitute only up to its proved TV error, not by silent substitution. The **pointwise inverter in §2 remains exact for every planted YES sample from either source**.

Classical background (not claims of independent mathematical novelty): [finite-field symplectic form and radical conventions (GAP Forms)](https://cage.ugent.be/geometry/software/forms/chap3.html); [symplectic polar-space TI subspace counts](https://www.mdpi.com/2075-1680/14/8/614); [rank classification and counting for finite-field alternating matrices](https://mathoverflow.net/questions/238834/number-of-skew-symmetric-matrices-of-fixed-rank).

**Decision:** the *single alternating-slice* planted TI search relation is **ANALYTIC EASY / POINTWISE REJECT** at every feasible \(d\). Ideal-source detection has an exact rank-sufficient likelihood; this does **not** solve multi-slice tensor/TI, arbitrary tensor isomorphism, or H-A as a whole. **GLOBAL NO NOMINATION**, H-A/H-B/H-C HOLD, N1-60 unallocated, 80/20 strategy, HEPMR #195 BENCHMARK ONLY through AP103, #199 source ZIP blocker and historical PARTIAL/HOLD unchanged.
