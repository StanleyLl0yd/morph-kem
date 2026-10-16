# MORPH-F0: fixed-codimension wedge-kernel public sections

**Date:** 2026-10-16. **Research status:** paper-only analytical no-go boundary. **GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.** This is not a new numbered F0-K/N1 stage, a candidate, a tested implementation, an empirical measurement, a security claim, or a KEM/PKE/trapdoor/OWF/PQ construction.

This note extends the [codimension-one full verifier attack](F0-multislice-isotropic-hyperplane-linearization.md) to two *carefully scoped* subclasses with **fixed** codimension \(c\): (i) pointwise inputs whose public wedge kernel is one-dimensional, and (ii) unconditional planted sources with sufficiently many independent forms to span the full vanishing-form space. It does **not** claim polynomial inversion of arbitrary higher-codimension planted tensors.

## 1. Original full verifier and polynomial-size linearization

Work over an effectively encoded finite field \(K=\mathbb F_q\), including characteristic two. Let \(n=c+d\), **fixed** \(c\ge1\), \(d\ge2\), and \(m\) polynomial in \(n,\log q\). An \(n\times n\) alternating matrix has zero diagonal even in characteristic two; identify it with an element of \(\Lambda^2 V^*\), \(V=K^n\). The entire original accepted relation is

\[
E(P)=\{Y\in K^{n\times d}:\operatorname{rank}Y=d,\
     Y^\top A_iY=0\text{ for every }1\le i\le m\},
\quad P=(A_1,\ldots,A_m).
\]

Any accepted \(Y\) wins, not necessarily the planted \(Y_0\) or even the same subspace. For an annihilator \(L=H^\circ\le V^*\) of a candidate \(d\)-space \(H\), take a nonzero decomposable \(\xi=\ell_1\wedge\cdots\wedge\ell_c\in\Lambda^c V^*\), with \(\ell_i\) a basis of \(L\). Elementary exterior-coordinate expansion gives the **exact** equivalence

\[
 A_i|_{H\times H}=0\quad\Longleftrightarrow\quad
 \xi\wedge A_i=0.
\]

The public linear map
\[
T_P:\Lambda^c V^*\longrightarrow(\Lambda^{c+2}V^*)^m,\qquad
\xi\longmapsto(\xi\wedge A_1,\ldots,\xi\wedge A_m)
\]
has \(\binom nc=O(n^c)\) input coordinates and \(m\binom n{c+2}=O(mn^{c+2})\) output coordinates for fixed \(c\). Gaussian elimination on its matrix is polynomial in the **full input bitlength**. **Warning:** when \(c\ge2\), an arbitrary nonzero vector of \(\ker T_P\) may be **nondecomposable**. A nonzero linear kernel alone is not a public section.

## 2. Pointwise theorem: one-dimensional wedge kernel suffices

**Theorem 1.** Suppose \(P\) is a YES instance of the exact original verifier and \(\dim\ker T_P=1\). Then a deterministic polynomial-time public algorithm outputs an element of \(E(P)\), for every finite field and fixed \(c\).

**Constructive algorithm.** Compute the unique nonzero kernel direction \(\xi\) by linear algebra. Because a YES witness exists, \(\ker T_P\) already contains the nonzero **decomposable** \(\xi_0\) of its annihilator, so \(\xi\) is proportional to \(\xi_0\) and is decomposable automatically. Recover
\[
L_\xi=\{\ell\in V^*: \ell\wedge\xi=0\}
\]
by a **second public linear solve**; for a nonzero decomposable \(c\)-vector, \(L_\xi\) has dimension exactly \(c\) and equals its unique represented \(c\)-space. Set \(H=L_\xi^\circ\), compute any ordered basis \(Y\) for \(H\), and run **all original rank and alternating-slice verifier equations**. The algorithm is exact and has success one on **every YES instance with wedge-nullity one**. On inputs without a guaranteed witness, reject if \(\ker T_P=0\), its dimension is not one, the recovered \(L_\xi\) has wrong dimension, or the original verifier fails; no general decision algorithm is claimed when nullity exceeds one.

This is ordinary Grassmann/Plücker reconstruction, not an independently novel complexity theorem. Background: [Plücker coordinates and decomposable-subspace reconstruction](https://link.springer.com/article/10.1007/s10231-022-01233-7); [finite-field linear sections of Grassmannians](https://doi.org/10.1016/j.ffa.2008.08.001).

## 3. Exact full-span rigidity, proved without random assumptions

Fix **any** \(d\)-space \(H\) (not necessarily uniformly distributed). Define its \(c\)-dimensional annihilator \(L=H^\circ\) and the full space of compatible public forms
\[
W_H=\{A\in\Lambda^2V^*: A|_{H\times H}=0\}
     =\Lambda^2L\oplus(L\wedge U),
\]
for **any** complementary subspace \(V^*=L\oplus U\), \(\dim U=d\). Its dimension is
\[
D=\binom c2+cd=\binom n2-\binom d2.
\]

**Theorem 2 (full-span rigidity).** For every \(d\ge2\), over **every** field,
\[
\bigcap_{A\in W_H}\ker(\xi\mapsto\xi\wedge A)
  =\Lambda^cL,
\]
which is a **one-dimensional** subspace of \(\Lambda^cV^*\).

**Self-contained coefficient proof.** Choose basis covectors \(\ell_1,\ldots,\ell_c\) for \(L\) and \(u_1,\ldots,u_d\) for \(U\). Expand \(\xi\) as a linear combination of distinct exterior basis monomials \(\ell_I\wedge u_J\) with \(|I|+|J|=c\), and classify monomials by \(t=|J|\).

- For any monomial with \(t\ge2\), at least two indices \(a,b\) of \(L\) are missing from \(I\). Wedging \(\xi\) with the **public allowable** form \(\ell_a\wedge\ell_b\in\Lambda^2L\subset W_H\) exposes its coefficient in the unique output basis monomial \(\ell_{I\cup\{a,b\}}\wedge u_J\). No different input monomial can contribute to that **same output monomial for this fixed multiplier**, so the coefficient must be zero.
- For any monomial with \(t=1\), at least one index \(a\) of \(L\) is missing from \(I\). Since \(d\ge2\), choose \(u_b\) different from the unique \(u\)-factor of this monomial. Wedging with \(\ell_a\wedge u_b\in L\wedge U\subset W_H\) similarly exposes its coefficient uniquely. The term must vanish. This argument does not require division by two and is valid even in characteristic two.
- The sole remaining \(t=0\) exterior monomial is \(\ell_1\wedge\cdots\wedge\ell_c\), and its wedge with **every** form in \(W_H\) is zero, because each such form contains at least one \(L\)-factor.

Therefore the common wedge-annihilator is precisely the line \(\Lambda^cL\). The hypothesis \(d\ge2\) matters: the \(t=1\) step needs another \(U\)-index. No pointwise statement for arbitrary *proper* subsets of \(W_H\) follows from this lemma.

**Corollary.** If the publicly observed \(A_1,\ldots,A_m\) span the whole \(W_H\), then \(\dim\ker T_P=1\), and Theorem 1 reconstructs \(H\) exactly as a subspace. It is the **unique** d-dimensional common totally-isotropic subspace on that public input: every other candidate supplies a decomposable line in the same one-dimensional kernel, hence has annihilator \(L\) and equals \(H\). Accepted matrices still differ by an arbitrary \(\mathrm{GL}_d(K)\) basis change.

## 4. Full unconditional planted-source probability and strict bounded generation

**Specified honest source.** Sample any \(d\)-subspace \(H\) by an explicitly given polynomial-time procedure, with no constraint on its distribution. Conditioned on \(H\), sample \(m\) **independent uniform elements of the entire** \(D\)-dimensional linear space \(W_H\). Publish all their complete matrices; the private planted basis always passes the exact verifier. The conditional sampling of \(W_H\) is part of this model; it is **not** automatic for arbitrary planted generators.

For every fixed \(H\), the coefficient matrix of the \(m\) uniform forms in a basis of \(W_H\) is a uniform \(m\times D\) matrix. Thus, if \(m\ge D\),
\[
\Pr[\operatorname{span}(A_1,\ldots,A_m)=W_H\mid H]
 =\prod_{j=0}^{D-1}(1-q^{j-m})=:p_{m,D,q}.
\]
This probability does **not** depend on \(H\), so it remains **exact** after averaging over the original unconditional honest \(H\)-source. The publicly computable rank test \(\dim\operatorname{span}(A_i)=D\), followed by Theorem 1 and the **full original verifier**, is a strict polynomial attacker with **success exactly** \(p_{m,D,q}\) if defined to return failure whenever the rank test is not full. A variant that also tries wedge-nullity-one cases when public form rank is lower can only improve its success.

The exact product gives a uniform lower bound at \(m=D\):
\[
p_{D,D,q}=\prod_{s=1}^{D}(1-q^{-s})
\ge\prod_{s\ge1}(1-2^{-s})\ge\tfrac14.
\]
For \(m=D+t\), integer \(t\ge1\), a union bound for uniform matrix row rank gives
\[
1-p_{m,D,q}
  \le\sum_{j=0}^{D-1}q^{j-m}
  <\frac{q^{D-m}}{q-1}
  =\frac{q^{-t}}{q-1}.
\]
Thus \(p_{m,D,q}>1-q^{-t}/(q-1)\). Since \(c\) is fixed,
\(D=cn-\tfrac{c(c+1)}2=O(n)\), and **\(m=D+t\)** is a polynomial-size public tuple. No source draws, simulation, run counts, parameter tuning or rejection on "easy" instances are needed for these exact probabilities.

### Strict worst-case polynomial realization for binary extension fields

For \(q=2^e\) with an effective polynomial-basis representation, every uniform field element is exactly e random unbiased bits. Produce a full-row-rank \(c\times n\) annihilator matrix \(M\) by choosing its entries independently uniformly; if \(\operatorname{rank} M<c\), replace the whole \(M\) by the fixed \([I_c\ 0]\). Set \(H=\ker M\). This is **always polynomial**, the fallback is part of the original honest law, and every sampled H has the correct dimension. Find by Gaussian elimination a complementary public-working basis \(U\) of \(V^*\) to the row span \(L\) of M. Independently fill **every** coefficient of the basis \(\Lambda^2L\oplus(L\wedge U)\) with a uniform field element for each of the m forms. This gives the **exact conditional-uniform** source assumed above, with no field arithmetic rejection.

Conditioned on \(\operatorname{rank}M=c\), its row space is uniform over the Grassmannian of c-spaces. The fallback probability
\[
\varepsilon=1-\prod_{j=0}^{c-1}(1-q^{j-n})
   <\frac{q^{c-n}}{q-1}
   =\frac{q^{-d}}{q-1}.
\]
Therefore the resulting **public-tuple distribution** differs in TV by at most \(\varepsilon\) from the ideal uniform planted-H law; no claim of exact uniformity is made for the bounded fallback mixture. More strongly, the actual unconditional bounded-source **search success remains exactly \(p_{m,D,q}\)**, including the fallback, because the conditional uniform-form spanning probability is the same for *every* H.

For other prime-power fields, the exact formulas describe their specified ideal uniform conditional source; a concrete strict-PPT sampler requires separate unbiased-field-element generation/TV control. None of these qualifications affect the **pointwise** full-span/no-nullity reconstruction over any field.

## 5. Limits, known mathematics and research decision

- **Fixed c is essential** for the \(\binom nc\)-coordinate exterior lift to remain polynomial. This is no proof of a general efficient algorithm with \(c=\Theta(n)\).
- The exact \(m\ge D=\Theta(cn)\) **full-span gate** is a large-public-observation regime. It does **not** resolve the Liu–Qiao–Tang–Zhang [2026 planted-TI conjectural parameters](https://arxiv.org/abs/2609.31256), where \(m=\lceil n/\log n\rceil\), \(d\approx n/C\) and neither \(c\) nor the number of observed forms satisfies these hypotheses. Nor does failure of the full-span event prove hardness.
- If wedge-nullity is greater than one, an arbitrary kernel vector need not be decomposable; Plücker equations remain and this method does **not** decide the existence of any \(d\)-subspace. An input with only a nonzero wedge kernel is **not** automatically a YES instance.
- The full-span event may allow **other simpler public reconstruction attacks**. No independent cryptographic novelty is suggested by the exterior lift, its dimension count or the distributional proof.
- Established mathematical background: [Plücker embedding and reconstructing a represented subspace](https://link.springer.com/article/10.1007/s10231-022-01233-7); [linear sections of the Grassmannian over finite fields](https://doi.org/10.1016/j.ffa.2008.08.001). Our result is a scoped explicit elementary no-go gate, not a novelty assertion.

**Disposition:** **ANALYTIC EASY** for (1) all honest fixed-c YES inputs with one-dimensional public wedge kernel, and (2) any honest source with *conditionally independent uniform full-vanishing-space forms* and \(m\ge D\), with exact full-source success probability \(p_{m,D,q}\). The full original verifier is always checked. **GLOBAL NO NOMINATION**, H-A/H-B/H-C HOLD, N1-60 unallocated, HEPMR #195 BENCHMARK ONLY through AP103, #199 source ZIP blocker, historical N1-19/N1-23 PARTIAL and N1-26 HOLD unchanged.
