# MORPH-F0: full multislice hyperplane inversion is public linear algebra

**Date:** 2026-10-16. **State:** analytically proved, source-first **no-go** for the codimension-one alternating-form inverse relation. **GLOBAL NO NOMINATION**, H-A/H-B/H-C HOLD. This is **unnumbered**: not F0-K10 or N1-60, not an independently novel mathematical construction, implementation, empirical test, sample count, security assumption, trapdoor, PKE or KEM.

## 1. Exact original any-witness target, for arbitrarily many slices

Let \(n\ge2\), \(m\ge1\), and \(K=\mathbb F_q\) be an effectively represented finite field. The public input \(P=(A_1,\ldots,A_m)\) is an arbitrary tuple of alternating \(n\times n\) matrices, with \(v^TA_iv=0\) for every \(v\) (including **zero diagonal** in characteristic two). The **complete original** rank-\((n-1)\) verifier accepts

\[
E(P)=\{Y\in K^{n\times(n-1)}:
 \operatorname{rank}Y=n-1,\quad Y^TA_iY=0\;\text{for ALL }1\le i\le m\}.
\]

Any accepted matrix, not the planted hyperplane or its basis, wins. The statement is **pointwise on every YES input**, independently of the distribution that produced \(P\) or of the number \(m\) of public slices.

## 2. A universal deterministic linear public section (every field, every m)

Identify each alternating bilinear form with an element \(A_i\in\Lambda^2 V^*\), where \(V=K^n\), without dividing by two. The annihilator of a candidate hyperplane \(H\subset V\) is a one-dimensional space of covectors \(\alpha\ne0\) with \(H=\ker\alpha\).

**Exact exterior-algebra equivalence:**
\[
A_i|_{H\times H}=0
\iff A_i=\alpha\wedge\beta_i\ \text{for some }\beta_i\in V^*
\iff \alpha\wedge A_i=0\quad\text{in }\Lambda^3 V^*.
\]

**Proof:** extend the nonzero \(\alpha\) to a dual basis beginning with \(e^1=\alpha\). Every 2-form decomposes uniquely into \(A_i=e^1\wedge\beta_i+C_i\), where \(C_i\in\Lambda^2\operatorname{span}(e^2,\ldots,e^n)\). Its restriction to \(H=\ker e^1\) is exactly \(C_i\). Likewise \(e^1\wedge A_i=e^1\wedge C_i\), which vanishes **if and only if** \(C_i=0\), because the indicated exterior basis elements are independent. This works over every characteristic, including two.

Most importantly, **for public fixed \(A_i\), the equation \(\alpha\wedge A_i=0\) is LINEAR in the n unknown coordinates of \(\alpha\)**. Explicitly, for every slice \(s\) and triple \(j<k<\ell\), impose
\[
\alpha_j(A_s)_{k\ell}
-\alpha_k(A_s)_{j\ell}
+\alpha_\ell(A_s)_{jk}=0.
\]
The minus sign is interpreted in \(K\); in characteristic two it equals plus, and the equivalence remains exact. Let \(L_P:V^*\to(\Lambda^3V^*)^m\) be the public matrix of this linear map.

**Full-inverter algorithm:** compute \(K_P=\ker L_P\) by Gaussian elimination. If \(K_P=0\), report NO. Otherwise choose **any nonzero** \(\alpha\in K_P\), compute a basis \(Y\) of its ordinary hyperplane \(\ker\alpha\), and check the **entire original verifier** (all m matrices and rank). The exterior equivalence guarantees acceptance. Conversely any accepted Y provides a nonzero hyperplane annihilator \(\alpha\in K_P\). Thus
\[
E(P)\ne\varnothing\quad\Longleftrightarrow\quad \dim K_P>0.
\]

This is a polynomial-time **decision-and-search algorithm even on adversarial NO inputs**, not merely an honest-distribution attack. It has at most \(m\binom n3\) public linear equations in n unknowns, plus a polynomial verifier. There is no Grassmannian enumeration, field-size enumeration, secret conditioning, factorization, randomized success event, or assumption that the matrix pencil is regular. When \(n=2\), \(\Lambda^3V^*=0\) and the statement correctly reduces to the fact that every nonzero vector spans an isotropic hyperplane.

### Exact accepted-fibre count

Let \(\kappa(P)=\dim K_P\). Every nonzero \(\alpha\in K_P\) specifies an accepted hyperplane \(\ker\alpha\), and two such covectors define the same hyperplane **exactly when they are nonzero scalar multiples**. Hence the exact number of **distinct accepted hyperplanes** is
\[
S(P)=\frac{q^{\kappa(P)}-1}{q-1}.
\]
Every hyperplane has precisely \(\lvert\operatorname{GL}_{n-1}(q)\rvert
=\prod_{j=0}^{n-2}(q^{n-1}-q^j)\) ordered bases. Consequently
\[
\lvert E(P)\rvert
=S(P)\,\lvert\operatorname{GL}_{n-1}(q)\rvert.
\]
Both counts are exactly computable in polynomial bit complexity from a single public Gaussian elimination. A large fibre is not a security indicator: the deterministic section exists for **every** nonempty fibre.

## 3. Ideal uniform planted law: exact posterior, likelihood ratio and optimal detection

The search theorem above needs **no** source model. For a separate source-specific result, let \(N=\binom n2\), \(c=\binom{n-1}2\), and \(G=\lvert\mathrm{Gr}(n-1,n;K)\rvert=(q^n-1)/(q-1)\).

- **Ideal planted \(Q_{\rm pl}\):** choose a hyperplane \(H\) uniformly among these G hyperplanes; conditional on H, sample \(A_1,\ldots,A_m\) **independently uniformly** among forms vanishing on \(H\times H\). Each allowable slice space is precisely \(\alpha\wedge V^*\), of dimension \(n-1=N-c\), for any nonzero annihilator \(\alpha\) of H.
- **Null \(Q_0\):** choose all m public alternating forms independently uniformly in \(\Lambda^2V^*\), a vector space of dimension N. This null distribution has NO guaranteed common isotropic hyperplane.

For any particular public tuple P, exact counting gives
\[
Q_{\rm pl}(P)=\frac{S(P)}{G\,q^{m(n-1)}},
\qquad Q_0(P)=q^{-mN},
\]
and therefore
\[
\boxed{\frac{Q_{\rm pl}(P)}{Q_0(P)}
 =q^{mc}\,\frac{q^{\kappa(P)}-1}{q^n-1}.}
\]

The posterior on planted H given P is **uniform over the S(P) accepted hyperplanes**, provided \(S(P)>0\). Hence the single public integer \(\kappa(P)\), computed in polynomial time, is an **exact sufficient statistic for the planted-vs-null likelihood-ratio test**. In particular the optimal equal-prior detector can compare \(q^{mc}(q^\kappa-1)\) with \(q^n-1\), with polynomial-bit integer arithmetic. The total-variation distance has the **exact identity**
\[
\operatorname{TV}(Q_{\rm pl},Q_0)
=\tfrac12\,\mathbb E_{P\leftarrow Q_0}
 \left|q^{mc}\,\frac{q^{\kappa(P)}-1}{q^n-1}-1\right|.
\]
This is an identity, **not** a claim that computing its whole expectation is polynomial or that the two laws have the same conditional distribution as other source models.

### A simple explicit polynomial distinguisher on the unconditioned laws

Even the binary test \(D(P)=[\kappa(P)>0]\) has **true-positive probability exactly one** under \(Q_{\rm pl}\). Under \(Q_0\), each fixed H satisfies all m slice restrictions with probability \(q^{-mc}\). A **union bound over all G hyperplanes**, with no independence assumption across H, gives
\[
\Pr_{Q_0}[D(P)=1]
 \le\min\{1,Gq^{-mc}\}
 =\min\left\{1,\frac{q^n-1}{q-1}\,
             q^{-m\binom{n-1}{2}}\right\}.
\]
Consequently this **polynomial-time** original-public-input distinguisher has true-positive minus false-positive advantage at least \(1-\min\{1,Gq^{-mc}\}\). For fixed q, any \(m\ge1\) and increasing n, the false-positive upper bound is \(q^{-\Omega(mn^2)}\) (up to the lower-order \(O(n)\) projective count); this is a **near-perfect detection break** of this *specific high-d ideal planted source*, not a statement about the independently studied planted-TI regime \(d\approx n/C\) with \(C\ge3\). It is vital that the existence test here is publicly polynomial by §2; a generic Grassmannian existence test at lower d is not thereby solved.

**No postselection:** every ideal planted sample contains its sampled H, so \(D(P)=1\) and the original full verifier's accepted fibre is nonempty with probability exactly one.

## 4. Strict worst-case polynomial binary-field source, without postselection

For \(q=2^e\), use an effective polynomial-basis field representation so that independent uniform field elements require exactly e unbiased bits. Sample \(\alpha\) uniformly from \(K^n\); if \(\alpha=0\), **replace it by the fixed \(e_1^*\)** instead of retrying. Independently sample each \(\beta_i\) uniformly from \(V^*\) and publish \(A_i=\alpha\wedge\beta_i\). The entire procedure is strictly worst-case polynomial and **always** has accepted hyperplane \(H=\ker\alpha\); fallback is part of its unconditional honest law.

Conditional on \(\alpha\ne0\), its projective class is exactly uniform among the G hyperplanes. For every nonzero \(\alpha\), \(\beta\mapsto\alpha\wedge\beta\) is a surjective linear map with kernel \(\operatorname{span}(\alpha)\), so each published \(A_i\) is exactly uniform on the allowed form space. Therefore the bounded generator's public law is **exactly a mixture**
\[
Q_{\rm bounded}=(1-q^{-n})Q_{\rm pl}+q^{-n}Q_{H_0},
\]
where \(Q_{H_0}\) is the fixed-hyperplane planted law. In particular \(\operatorname{TV}(Q_{\rm bounded},Q_{\rm pl})\le q^{-n}\); **no exact-uniform sampler claim** is made for the fixed-budget fallback law.

The deterministic public section §2 succeeds **on every bounded-source sample**, and the public detector D has true-positive probability exactly one on its *actual* unconditioned output law, including fallback. Its false-positive bound under the independent Q0 remains unchanged. The ideal-law posterior and likelihood ratio are **not** asserted verbatim for the bounded mixture; any event-level transfer must explicitly account for the \(q^{-n}\) TV gap.

## 5. Why the easy boundary stops at codimension one

For an arbitrary codimension-c subspace H, its annihilator \(L\subset V^*\) has dimension c. With any basis \(\alpha_1,\ldots,\alpha_c\) of L and decomposable \(\xi=\alpha_1\wedge\cdots\wedge\alpha_c\), the same coordinate argument gives
\[
A_i|_{H\times H}=0 \iff \xi\wedge A_i=0.
\]
These equations are **linear in the exterior coordinates of \(\xi\)**, but for \(c\ge2\) an arbitrary nonzero element of \(\Lambda^c V^*\) need **not** be decomposable. The public problem additionally requires the established **quadratic Plücker relations** (or equivalent Grassmannian constraints) and a rank-c annihilator. The fact that the enlarged linear wedge kernel is nonzero does not supply a valid original-verifier witness. In contrast, **every nonzero 1-vector is decomposable**, which is precisely why the codimension-one inverter is complete.

Established context: [Plücker embedding and defining relations, *Encyclopedia of Mathematics*](https://encyclopediaofmath.org/wiki/Pl%C3%BCcker_coordinates), [MathWorld exterior/Plücker relations](https://mathworld.wolfram.com/PlueckerRelations.html); the wedge-annihilator statement itself is the elementary exterior-algebra/Koszul identity proved in §2. This boundary neither solves general finite-field multilinear inversion nor nominates an independent MORPH foundation.

## 6. Decision

**ANALYTIC EASY, pointwise decision/search, all finite fields and any number of public alternating slices, strictly at target dimension \(d=n-1\).** The ideal uniformly planted hyperplane law is also polynomially and nearly perfectly distinguishable from unrestricted uniform alternating null for sufficiently large n; the binary-field strictly bounded generator is explicit and preserves an accepted witness on every run. These are exact scoped mathematical/source statements, not measurements, experiments or cryptographic security claims. **GLOBAL NO NOMINATION**, H-A/H-B/H-C HOLD, N1-60 unallocated, HEPMR #195 BENCHMARK ONLY through AP103, #199 missing ZIP and earlier N1 PARTIAL/HOLD unchanged.
