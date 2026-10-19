# F0: sparse planted-TI rank-profile and high-corank MinRank negative controls

**Date:** 2026-10-19. **Scope:** exact, source-first, paper-only rank-diagnostic analysis. **GLOBAL NO NOMINATION**, H-A/H-B/H-C HOLD. No new N1/F0-K case, sample, implementation, cryptographic hardness claim or full-original-verifier inverter in the hard sparse regime.

This closes the **individual slice-rank** gap explicitly left in [#208's coefficient-rank and common-radical null-control proof](https://github.com/StanleyLl0yd/morph-kem/issues/208#issuecomment-6215891446). It also excludes only **exceptionally high-corank** combinations in sparse public spans. Established random-alternating-rank results: [Fulman–Goldstein, *Annals of Probability* 43 (2015)](https://doi.org/10.1214/13-AOP889); external independent planted-TI source: [Liu–Qiao–Tang–Zhang (2026)](https://arxiv.org/abs/2609.31256).

## 1. Exact laws and full original relation

Over a publicly effective \(\mathbb F_q\), \(q\ge2\), take \(n\ge2d\ge2\), \(s=n-2d\ge2\), \(m\ge1\). **Planted \(Q_{\rm pl}\):** sample any d-space H using an unconditional polynomial sampler, then independently uniform alternating \(n\times n\) forms \(A_i\) vanishing on \(H\times H\). **Null \(Q_0\):** take m independent unrestricted uniform alternating matrices. The original verifier accepts **any** rank-d Y satisfying \(Y^\top A_iY=0\) for **all** i. Every planted sample passes with its own H, with **no conditioning on rank or "hardness"**. Alternating requires zero diagonal, even in characteristic two.

Only for proof choose coordinates H first. Each planted slice has block matrix
\[
 A=\begin{pmatrix}0&B\\-B^\top&C\end{pmatrix},\quad
 B\sim\mathrm{Unif}(\mathbb F_q^{d\times k}),\
 C\sim\mathrm{Unif}(\operatorname{Alt}_{k}(\mathbb F_q)),\
 k=n-d,
\]
independent, and these coordinates are **not public to the attack**.

## 2. Exact unconditional one-slice corank distribution

If \(\operatorname{rank}B=t\), public-congruence algebra (as a proof device only) splits t hyperbolic pairs, d−t forced radical vectors and an independent uniform alternating block \(Z_{k-t}\). The cross terms can be eliminated without dividing by two, and uniformity of the residual follows from surjectivity of restriction:
\[
\operatorname{corank}(A)\mid(\operatorname{rank}B=t)
\ \stackrel d=\ d-t+\operatorname{corank}(Z_{k-t}).
\]
The elementary full-rank counting law for a uniform d×k matrix gives
\[
w_t=\frac{{d\brack t}_q{k\brack t}_q|\mathrm{GL}_t(q)|}{q^{dk}},
\quad 0\le t\le d.
\]
For \(\ell\ge0\), let \(G_j=\prod_{a=1}^j(1-q^{-a})\), \(S_j=\prod_{a=1}^j(1-q^{-2a})\). The **classical** exact corank law of a uniform alternating \(\ell\times\ell\) matrix is
\[
h_{\ell,q}(v)=
 q^{-\binom v2}\frac{G_\ell}{G_v S_{(\ell-v)/2}}
\]
when \(0\le v\le\ell\) and \(\ell-v\) even; otherwise it is zero. Proof: choose the radical v-space, then a nondegenerate alternating form on the quotient; use \(|GL_{2r}(q)|/|Sp_{2r}(q)|\) and divide by \(q^{\binom\ell2}\).

Hence the **exact** planted corank law is the polynomial-size mixture
\[
\boxed{\Pr_{Q_{\rm pl}}[\operatorname{corank}A=u]
=\sum_{t=0}^dw_t\,h_{k-t,q}(u-d+t),}
\]
while the null corank law is \(h_{n,q}(u)\). These rational distributions use polynomially many arithmetic operations with polynomial bitlength, with **no source samples or numerical trials**.

## 3. Negligible joint TV for every *individual slice rank* in the sparse-m regime

Write \(a_s=q^{-s}/(q-1)\). The probability B lacks full row rank is
\[
1-\prod_{j=0}^{d-1}(1-q^{j-k})\le a_s.
\]
On its complement, \(\operatorname{corank}A\stackrel d=\operatorname{corank}Z_s\). Thus the planted single-slice corank law has TV distance at most \(a_s\) from \(h_{s,q}\).

Since n and s have the same parity, for valid coranks \(v\le\lfloor s/2\rfloor\),
\[
\frac{h_{n,q}(v)}{h_{s,q}(v)}
=\frac{G_n}{G_s}\frac{S_{(s-v)/2}}{S_{(n-v)/2}}.
\]
The first ratio lies in \([1-a_s,1]\). Put
\[
b_s=\frac{q^{-(\lfloor s/2\rfloor+2)}}{1-q^{-2}}<\tfrac12,\qquad
u_s=\lfloor s/2\rfloor+1.
\]
The second ratio lies in \([1,(1-b_s)^{-1}]\). Thus the total low-corank \(\ell_1\) difference is at most \(a_s+2b_s\).

For the high-corank tails, the exact h-formula and \(S_r\ge1/2,\ G_\ell\le G_v\) give \(h_{\ell,q}(v)\le2q^{-\binom v2}\). Consequently, for every \(u\ge2\), the geometric bound on successive terms gives
\[
\Pr[\operatorname{corank} Z_\ell\ge u]\le3q^{-\binom u2}.
\]
Combining two tails, the low-corank ratio bound and the probability B is deficient yields the **conservative explicit source TV bound**
\[
\boxed{
\operatorname{TV}(\mu_{\rm pl},\mu_0)
\le\epsilon_{s,q}:=
2a_s+2b_s+6q^{-\binom {u_s}2}
}
\]
for the one-slice corank distributions.

Crucially, conditional on **every fixed H**, the m slice ranks are iid with the **same** law \(\mu_{\rm pl}\), independent of H by change-of-basis invariance. Thus averaging over any unconditional honest H sampler leaves their **joint** rank vector law exactly \(\mu_{\rm pl}^{\otimes m}\). Under Q0 it is \(\mu_0^{\otimes m}\). By product coupling,
\[
\boxed{
\operatorname{TV}\bigl(\mathcal L_{Q_{\rm pl}}((\operatorname{rank}A_i)_i),
\mathcal L_{Q_0}((\operatorname{rank}A_i)_i)\bigr)
\le\min(1,m\epsilon_{s,q}).
}
\]
For fixed q, \(m=\lceil n/\log n\rceil\), \(d=\lceil n/C\rceil\) with constant \(C\ge3\), one has \(s=\Omega(n)\), so \(m\epsilon_{s,q}=O(mq^{-s/2})=q^{-\Omega(n)}\), up to polynomial factors. Hence **the entire vector of individual slice ranks** has negligible planted-vs-null statistical distinguishing advantage. This is *not* a small-TV statement for the full public matrices, coupled invariants or adaptively selected combinations.

## 4. Public matrix-span MinRank: high-corank threshold events are absent on both laws

For any **fixed nonzero** coefficient vector \(\lambda\in\mathbb F_q^m\), the combination \(A(\lambda)=\sum_i\lambda_iA_i\) remains uniform on the conditioned compatible alternating-form space under \(Q_{\rm pl}\), and is unrestricted uniform alternating under Q0. Therefore, for any integer \(u\ge2\),
\[
\Pr_{Q_{\rm pl}}[\operatorname{corank}A(\lambda)\ge u]
\le a_s+3q^{-\binom u2},
\quad
\Pr_{Q_0}[\operatorname{corank}A(\lambda)\ge u]
\le3q^{-\binom u2}.
\]
Because scalar coefficient multiples yield the **same corank**, the union bound over **all** \((q^m-1)/(q-1)\) projective coefficient directions proves
\[
\boxed{
\Pr_{Q_{\rm pl}}[\exists[\lambda]:
\operatorname{corank}A(\lambda)\ge u]
\le\min\!\left(1,\frac{q^m-1}{q-1}
(a_s+3q^{-\binom u2})\right),
}
\]
and the same bound without \(a_s\) under Q0. **This covers even coefficients chosen adaptively after inspecting the matrices**: the bound concerns whether **any** such combination exists, not how it is searched.

In the fixed-q sparse-m regime above, let \(u=\lceil2\sqrt m\rceil+2\). Then \(\binom u2\ge2m\), and \(m=o(s)\), so
\[
\Pr_{Q_{\rm pl}}[\exists[\lambda]:\operatorname{corank}A(\lambda)\ge u]
\le O(q^{m-s}+q^{-m})=q^{-\Omega(n/\log n)},
\]
with \(O(q^{-m})\) under Q0. Thus **neither** public law typically contains an exceptionally-high-corank combination above this threshold. This does **not** rule out lower-threshold optimized MinRank, the distribution of the smallest attainable rank, joint row-space anomalies, nonlinear attacks or any-witness inversion. The public span can still contain useful structure at *smaller* rank defects.

## 5. Honest generation, prior art and limits

For q=2^e with a public polynomial-basis field, a worst-case polynomial sampler of a full-rank planted H may use a **fixed valid fallback** when a bounded candidate matrix is rank deficient, followed by independently exact uniform coefficients for every compatible alternating form. Every outcome, including fallback, has an accepted planted Y and **the same conditional rank laws above**. All probabilities are for the **actual unconditioned source**, not samples filtered for easy or difficult rank. For other q, the ideal uniform field-element source must be implemented with explicit strict-time/TV accounting before claiming the same statement for a bounded generator.

Random alternating rank counts are established (Fulman–Goldstein 2015, linked above); this proof applies them as a **negative control**, not a new hard problem, quantum hardness result or novel Field 15. It complements the earlier [#208 two-statistic null control](https://github.com/StanleyLl0yd/morph-kem/issues/208#issuecomment-6215891446). **GLOBAL NO NOMINATION**, H-A/H-B/H-C HOLD, N1-60 unallocated, HEPMR #195 BENCHMARK ONLY, #199 original source ZIP blocked and historical N1-19/23 PARTIAL, N1-26 HOLD remain unchanged.
