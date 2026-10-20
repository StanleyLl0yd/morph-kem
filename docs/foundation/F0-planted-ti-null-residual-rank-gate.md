# MORPH-F0: exact null quotient law and short-seed residual rank gate

**2026-10-20. Attack-first analytical follow-up to the shorter-seed public residual-support algorithm. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.** The result is an exact planted-true-seed versus *unrestricted-null* source calculation, including an explicit finite expected number of public low-rank seed candidates and a conservative high-probability null-exclusion regime. It gives a superpolynomial public **distinguisher** after enumeration, **not** a polynomial planted witness extractor, a new cryptographic assumption, or a statement about false seed distributions inside the planted model.

**Priority and scope.** The planted totally-isotropic (TI) source and generic finite-field tensor algorithms are due to Liu–Qiao–Tang–Zhang, [*The planted tensor problem over finite fields: algorithms and cryptography*](https://arxiv.org/abs/2609.31256) (2026). This result combines the repository's [public residual planted inverter](F0-planted-ti-seeded-residual-support-attack.md) with its [exact uniform alternating rank law](F0-sparse-planted-ti-rank-profile-minrank-screen.md); no independent mathematical novelty or best-known-algorithm improvement is claimed.

## 1. The two **unfiltered** distributions and a completely public gate

Let q be any prime power, V=F_q^n, 2<=d<n, c=n-d, m>=1, and 1<=t<d. The **honest planted source** draws H from any prior independently of the forms, and then publishes m independent uniform alternating forms A_i vanishing on H x H. The **null source** publishes m unrestricted independent uniform alternating forms on V. No rank filter or rejection is applied to either generator.

Choose parameters in the **full-row gate** range

\[
0<mt<c,\qquad \ell=c-mt,\qquad u=d-t,\qquad 0<\ell<u,
\quad D=u+\ell=n-t-mt,\quad h=u-\ell>0.
\]

For every public t-plane T, use only the fully published forms and exact linear algebra:

1. Check T is simultaneously isotropic, so T is contained in its public simultaneous orthogonal space S_A(T). Reject otherwise.
2. Check that the public contraction matrix from T to V/T has **row rank mt**. Equivalently, S_A(T) has dimension n-mt. Reject otherwise.
3. Restrict every public A_i to the canonical quotient W_T=S_A(T)/T of dimension D. Accept the **rank gate** only when the rank of **each** induced alternating form is at most 2\ell.

Let G_t(A) count all t-planes that pass these three tests. This is a deterministic, public, finite observable; it does **not** consult or require H and does **not** assume the original any-witness verifier accepts any d-plane. Each seed test is polynomial in n,m,log q, but computing G_t by enumerating every seed can take \(\operatorname{poly}\,{n\brack t}_q\) field operations.

The seeded residual *witness* procedure of the preceding note can additionally apply its support-intersection recovery to gate-passing seeds, lift a candidate and invoke the **entire original verifier**. The gate alone is **not** a verifier and is **not** evidence that an arbitrary gate-passing T is genuine.

## 2. Exact null residual law conditional on a fixed public seed

**Theorem 1 (unrestricted-null quotient law, every finite characteristic).** Fix any t-plane T **before** sampling the null forms. The probability T is simultaneously isotropic is exactly

\[
p_{\rm iso}=q^{-m{t\choose2}}.
\]

Conditional on this event, the joint cross-contraction map from T to a chosen complement V/T is a **uniform mt-by-(n-t) matrix** M, independent of all complementary alternating blocks. Hence for mt<=n-t its full-row probability is

\[
p_{\rm cross}=\prod_{j=0}^{mt-1}(1-q^{j-(n-t)}).
\]

Conditional on both events, put K=ker M in the complement. Then S_A(T)=T\oplus K and W_T is identified with K of dimension D=n-t-mt. Given even the **entire value** of M, the m quotient forms on W_T are mutually independent, unrestricted **uniform alternating forms on F_q^D**.

**Proof.** Write each unrestricted alternating form relative to T plus a fixed complement as the block matrix with top-left t-by-t alternating block E_i, uniform cross block B_i, and bottom-right unrestricted alternating block C_i. In the null distribution all free coefficients of E_i, B_i and C_i are independent uniform, also across i. Imposing isotropy forces E_i=0 and leaves B_i,C_i independent uniform. Stacking all B_i gives M. On its full-row event, K=ker M, and every A_i(T,T\oplus K) vanishes; the quotient restriction is precisely C_i|_{K\times K}. For every **fixed K**, restriction Alt(complement) -> Alt(K) is a surjective linear map. Uniform independent C_i therefore give independent unrestricted uniform forms, conditional even on M. This proof uses no hidden H and remains valid in characteristic two with zero diagonal. QED.

**Important disjointness of models.** For a precommitted **genuine T<=H** under the planted source, the earlier [residual theorem](F0-planted-ti-seeded-residual-support-attack.md) gives a residual **planted** u-plane and rank of each quotient form at most 2\ell, whenever its T-to-complementary-H cross map has rank mt. Theorem 1 instead applies to a fixed T under **unrestricted null**. It is *not* the law of a planted-sample T chosen outside H, nor the law of a public tensor-adaptive T; such transfers would be invalid.

## 3. Exact null expected count and genuine-true-seed count

Let \(R_{D,q}\) be the rank of one uniformly random D-by-D alternating form. For integer \(\ell\ge0\), define the exact **unrestricted-null** rank tail

\[
\tau_{D,\ell,q}=\Pr[R_{D,q}\le 2\ell]
= q^{-{D\choose2}}
 \sum_{k=0}^{\min(\ell,\lfloor D/2\rfloor)}
 {D\brack 2k}_q\, q^{k(k-1)}
 \prod_{j=1}^{k}(q^{2j-1}-1).
\]

The empty product is 1. The summand chooses the radical of dimension D-2k and then a nondegenerate alternating form on its 2k-dimensional quotient. The nondegenerate count is \(|GL_{2k}(q)|/|Sp_{2k}(q)|\), valid in all finite characteristics.

**Theorem 2 (exact fixed-seed null event, exact expected public count).**

\[
\boxed{\Pr_0[T\text{ passes the public gate}]
 = q^{-m{t\choose2}}\,p_{\rm cross}\,\tau_{D,\ell,q}^{\,m}.}
\]

In particular, with no independence claim between distinct candidate T,

\[
\boxed{\mathbb E_0 G_t(A)
 ={n\brack t}_q
 q^{-m{t\choose2}}\,
 \left[\prod_{j=0}^{mt-1}(1-q^{j-(n-t)})\right]
 \tau_{D,\ell,q}^{\,m}.}
\]

**Proof.** Apply Theorem 1 to the three public gate predicates. The m induced quotient rank events are independent only **conditional on the fixed seed and its cross block**, which suffices for the product \(\tau^m\). Every t-plane has the same null probability by GL(V) symmetry; linearity of expectation gives the count. No false independence between different t-planes is used. QED.

For the planted source, define \(X_t(A,H)\) as the number of **genuine** t-planes T<=H whose own cross-contraction has full row rank mt. Then

\[
\boxed{\mathbb E_{\rm pl}[X_t\mid H]
 ={d\brack t}_q\,p_{\rm row},\qquad
 p_{\rm row}=\prod_{j=0}^{mt-1}(1-q^{j-c}).}
\]

Every such genuine T passes all three public tests: T is isotropic, S_A(T)/T contains an isotropic u-plane H/T, so each induced alternating form has rank <=2\ell. The earlier seeded support method further recovers the planted H on some, but **not necessarily every**, gate-passing true seed. For any fixed precommitted genuine T, its full-row gate probability is exactly p_row, with

\[
1-p_{\rm row}<\frac{q^{-\ell}}{q-1}.
\]

The mean count of true seeds is a proof-only statistic, **not** computable from the public tensor without knowing H.

## 4. A finite public null-exclusion bound and an explicit asymptotic distinguisher

For h=D-2\ell=u-\ell>=2, the previously recorded exact alternating corank tail satisfies

\[
\tau_{D,\ell,q}=\Pr[\operatorname{corank}R_{D,q}\ge h]
\le 3q^{-{h\choose2}}.
\]

(The bound may exceed 1 at tiny h but remains a valid upper bound; it follows by summing the exact alternating corank masses, each at most \(2q^{-{v\choose2}}\) for v>=h.) With \(C_q=\prod_{j\ge1}(1-q^{-j})^{-1}<4\) and \(p_{\rm cross}\le1\),

\[
\boxed{
\Pr_0[G_t>0]\le\mathbb E_0G_t
\le C_q q^{t(n-t)-m{t\choose2}-m{h\choose2}}\,3^m.
}
\]

The first inequality is Markov/union bound, not independence of the seed events.

**Theorem 3 (short-seed exhaustive public distinguisher, still superpolynomial).** Fix q, \(d/n\to\alpha\in(0,1/2)\), and \(m\asymp n/\log n\); write \(\beta=1-2\alpha>0\). Choose

\[
t=\left\lceil\frac{c-d+n/m}{m-1}\right\rceil.
\]

Eventually the full-row gate hypotheses hold, \(t=\beta n/m+O(1)=\Theta(\log n)\), \(\ell=\Theta(n)\), and \(h=(m-1)t-(c-d)\ge n/m\). Thus

\[
\log_q\mathbb E_0G_t
\le \left(\beta-\frac{\beta^2}{2}-\frac12+o(1)\right)
\frac{n^2}{m}
=\boxed{-(2\alpha^2+o(1))\frac{n^2}{m}}.
\]

**Actual public deterministic test:** enumerate **all** t-planes using their public reduced-row-echelon representations, and output "planted" iff at least one public seed passes the rank gate. For every planted H prior independently chosen before the original tensor:

\[
\boxed{
\Pr_{\rm pl}[\text{test says planted}]\ge p_{\rm row}
 =1-q^{-\Omega(n)},\quad
\Pr_0[\text{test says planted}]
 \le q^{-(2\alpha^2+o(1))n^2/m}.
}
\]

The test uses \(q^{\beta n^2/m+o(n^2/m)}=q^{O(n\log n)}\) worst-case public work. There is **no** claim of a polynomial-time detector. A rank-gate success is not necessarily a valid original witness; the separate [public support-inversion attack](F0-planted-ti-seeded-residual-support-attack.md) has its own original-verifier success and runtime theorems.

**Proof.** The t-plane count is bounded by \(C_qq^{t(n-t)}\). Since \(t=\beta n/m+O(1)\), \(h\ge n/m\), and \(m\asymp n/\log n\), the preceding exact-count upper bound has leading exponent \((\beta-\beta^2/2-1/2)n^2/m\); terms of size \(O(n+m+n^2/m^2)\) are lower order. As \(\beta=1-2\alpha\), its coefficient is \(-2\alpha^2\). The planted test accepts whenever one **precommitted** true seed (fixed only in this proof) has full row rank, with probability p_row, and \(\ell=\Theta(n)\) ensures its failure is \(q^{-\Omega(n)}\). No adaptive-source substitution is used. QED.

This changes neither the known \(q^{O(n\log n)}\) generic attack class nor the sharper randomized/quantum upper work exponents of the preceding note. No computational security lower bound, polynomial inversion, source sampling claim, postselection, code execution on cryptographic parameters, or independent Field-15 evidence follows.

## 5. Independent tiny exact arithmetic controls (scratch only)

Over GF(2), independently enumerate the \(2^{D(D-1)/2}\) alternating matrices (zero diagonal), then compare their rank histograms with the quotient-law tail formula:

- D=4: rank 0/2/4 counts = 1/35/28 out of 64; \(\tau_{4,1,2}=36/64=9/16\).
- D=5: rank 0/2/4 counts = 1/155/868 out of 1024; \(\tau_{5,1,2}=156/1024=39/256\).
- As a separate **whole-null-tensor** check of Theorem 1, exhaust all 64 alternating 4-by-4 GF(2) matrices for a fixed T=span(e1), m=1. Of the 56 cases with full cross-row rank, the two-dimensional quotient has exactly 28 zero and 28 nonzero alternating forms. Thus conditioning on the cross block leaves the quotient uniform, including the fully summed complement-block multiplicities.
- Finite rank-gate parameters \(q=2,n=11,d=5,c=6,m=5,t=1\) give \(\ell=1,u=4,h=3,D=5\), \(p_{\rm row}=615195/1048576\), \(p_{\rm cross}=1066549422015/1099511627776\), and exact \(\mathbb E_0G_1=196979877253307849996295/1208925819614629174706176\approx0.162938\). This is an exact block-law calculation, **not** an exhaustive 11-dimensional full-tensor run or an empirical attack success estimate.

These are scratch integer/rational cross-checks only; no new repository test suite, public benchmark, sampled cryptographic instance or executable attack has been added.

## 6. Limits and next falsification target

1. The residual gate is a superpolynomial **enumerated** distinguisher and an early-rejection check for the existing superpolynomial witness attack, not a polynomial way to **locate** a genuine T.
2. The exact false-positive probability is for **unrestricted null**. Inside a *planted* tensor, a wrong T may be statistically dependent on the planted H, and an adaptively selected T may be correlated with the entire tensor. Neither population is assigned the null law.
3. This rank gate is **necessary** for the planted-true-seed residual source but insufficient for original-verifier acceptance; no output bypasses all m original bilinear equations.
4. A meaningful next attack-first objective is a **polynomial public search for a passing low-rank seed** with proved planted-original-source success, rather than enumeration, and an independent comparison to the existing external planted-tensor algorithms. A certificate that null instances rarely have a seed is *not* a source-hardness theorem.
5. No N1-60 allocation, F0-K/A-ID, new candidate, KEM/PKE/OWF, quantum implementation, README enlargement or stage-registry change.

**Disposition:** EXACT NULL QUOTIENT / PUBLIC RESIDUAL RANK-GATE SOURCE COUNT / SUPERPOLYNOMIAL DISTINGUISHER. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD; HEPMR BENCHMARK ONLY.
