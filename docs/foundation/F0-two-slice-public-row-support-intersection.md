# MORPH-F0: two public alternating slices reveal a high-dimensional planted TI space by row-support intersection

**Date:** 2026-10-16. **Scope:** paper-only, source-first analytical no-go; **GLOBAL NO NOMINATION**, H-A/H-B/H-C HOLD. No new F0-K/N1 number, external source cases, code, measurements, conjectured hardness, primitive, OWF/PQ/PKE/KEM/trapdoor or implementation authorization.

This result substantially strengthens the [fixed-codimension full-span exterior-kernel gate](F0-fixed-codimension-wedge-kernel-section.md): on a **specified** high-dimensional planted distribution, **two** alternating slices suffice with constant-to-overwhelming *unconditioned* attack success. Unlike that earlier exterior-coordinate proof, its algorithm is plain public linear algebra **even if codimension grows linearly with n**.

## 1. Exact full any-witness relation and conditioned honest source

Let \(K=\mathbb F_q\) be an effectively represented finite field, including characteristic two. Choose positive integers \(c,d\), \(n=c+d\), and target \(\operatorname{rank}Y=d\). The public tuple consists of \(m\ge2\) **alternating** forms \(A_i\in\operatorname{Alt}_n(K)\). The **complete original verifier** checks
\[
V(P,Y)=[\operatorname{rank}Y=d\ \wedge\
          Y^\top A_iY=0\text{ for every }i=1,\ldots,m].
\]
Every accepted \(Y\) succeeds, regardless of the source's planted basis.

The *explicit* honest law first samples **any** \(d\)-dimensional \(H\subseteq K^n\) using a stated polynomial-time sampler (not assumed uniform), then independently samples \(A_1,A_2\) **uniformly** from the full space \(W_H\) of alternating forms vanishing on \(H\times H\). Any further public forms may be independently sampled from \(W_H\), or otherwise chosen as long as they vanish on H and their production is polynomial. The planted H always passes V, with no sample rejection or output conditioning. Uniformity is required for the claimed probability, not for the pointwise public acceptance certificate.

Select, for *proof only*, a decomposition \(V=Q\oplus H\), \(\dim Q=c\), \(\dim H=d\), with \(H^\circ=L\subset V^*\), \(\dim L=c\). Each conditional-uniform alternating form has matrix
\[
A_i=\begin{pmatrix} C_i&B_i\\-B_i^\top&0\end{pmatrix},
\quad
C_i\in\operatorname{Alt}_c(K),\qquad B_i\in K^{c\times d},
\]
with all independent parameters in \(C_i\)'s strict upper triangle and in \(B_i\) uniform. Over characteristic two the lower left is \(+B_i^\top\), **but the alternating diagonal remains zero**. The proof coordinates and hidden B matrices are **not given to the attacker**.

## 2. Pointwise public row-support certificate

Treat each matrix \(A_i\) as an alternating linear map \(V\to V^*\), and denote its **public image/covector support** by \(S_i=\operatorname{im}A_i\le V^*\). We can compute each S_i and its intersection in polynomial time by Gaussian elimination directly on **the original public matrices**, without knowing H or the above decomposition.

**Lemma.** If \(B_i\) has full row rank c, then \(\operatorname{rank}A_i=2c\) and
\[
S_i=L\oplus R_i,
\]
where \(R_i\le H^*\) is the c-dimensional row space of \(B_i\) under the proof-only splitting \(V^*=L\oplus H^*\).

**Proof.** The block equation \(A_i(x,y)=0\) gives \(B_i^\top x=0\), hence \(x=0\) because B_i has full row rank; then \(B_i y=0\). The radical has dimension \(d-c\), so rank A_i is \(2c\). The images of vectors \((0,y)\) are all of L since \(B_i:K^d\to K^c\) is onto, while the image modulo L from vectors \((x,0)\) is exactly the row space \(R_i\). This proves the decomposition. Conversely, \(\operatorname{rank}A_i=2c\) forces \(\operatorname{rank} B_i=c\) for a form in \(W_H\).

**Pointwise attack certificate.** Compute S_1,S_2 and check the public conditions
\[
\operatorname{rank}A_1=\operatorname{rank}A_2=2c,
\qquad\dim(S_1\cap S_2)=c.
\]
Whenever an honestly planted H exists and these checks pass, both supports contain L; their c-dimensional intersection is therefore **exactly L**. Reconstruct \(H=(S_1\cap S_2)^\circ\), output an arbitrary basis \(Y\) of dimension d, and **verify every original public alternating slice**, including additional \(A_3,\ldots,A_m\). An honest input meeting the public certificate is inverted **with certainty**. On arbitrary inputs without a planted guarantee, the final full verifier prevents false positive accepted witnesses; no claim is made that this certificate characterizes all YES inputs.

**Uniqueness on the certified subclass.** If another \(d\)-space \(H'\) were accepted by both slices of rank \(2c\), its c-dimensional annihilator \(L'\) would be contained in each \(S_i\) by the same block lemma applied to \(H'\). Thus \(L'\subseteq S_1\cap S_2=L\) and \(H'=H\). The accepted *subspace* is unique, though every one of its \(\lvert\operatorname{GL}_d(q)\rvert\) ordered bases passes V. Secret-uniqueness is a **consequence of an easy public section**, not hardness evidence.

## 3. Exact original-source probability with TWO slices

Let \(d\ge2c\) (equivalently \(n\ge3c\)). Conditioned on **every fixed planted H**, stack the two independent uniformly sampled cross blocks
\[
B_{\rm stack}=\begin{pmatrix}B_1\\B_2\end{pmatrix}
\in K^{2c\times d}.
\]
It is a **uniform** \(2c\times d\) matrix. The event
\[
\mathcal G=[\operatorname{rank}B_{\rm stack}=2c]
\]
is exactly the event that both \(B_i\) have row rank c **and** their row spaces intersect trivially. By the lemma, this is **exactly the publicly checkable certificate** in §2, under the honest law.

The exact probability, for every fixed H, is the elementary full-row-rank formula
\[
p_{c,d,q}:=\Pr[\mathcal G\mid H]
 =\prod_{j=0}^{2c-1}(1-q^{j-d}).
\]
Since the right side is independent of H, averaging over the **unconditioned** polynomial-time honest H generator leaves the probability **exactly the same**. Define the public gated inverter to return failure unless the rank/intersection certificate passes, and to output its full-original-verifier-accepted Y otherwise. Its success probability under this **whole specified source** is **exactly** \(p_{c,d,q}\), not an estimate, postselected rate, or empirical count.

**Universal lower bounds.** For every \(q\ge2\), if \(d=2c\) then
\[
p_{c,2c,q}=\prod_{s=1}^{2c}(1-q^{-s})
 \ge\prod_{s\ge1}(1-2^{-s})\ge\frac14.
\]
For \(d=2c+t\), \(t\ge1\), a union bound yields
\[
1-p_{c,d,q}\le\sum_{j=0}^{2c-1}q^{j-d}
 <\frac{q^{2c-d}}{q-1}=\frac{q^{-t}}{q-1}.
\]
Thus the same **two-slice** inverter has success \(>1-q^{-t}/(q-1)\), rapidly approaching one with t even when c itself grows with n. Both matrices have full \(n^2\)-entry public encodings, and all work is polynomial in n and \(\log q\), **with no fixed-c restriction**.

For \(m>2\) conditionally uniform independently planted forms, this is a valid **lower bound** on success using just the first two slices. Additional slices must still pass the **original verifier**; they do on the honest source. One may inspect other pairs, but no compounded probability formula is asserted without analyzing their dependence.

### A strictly worst-case polynomial exact binary-field honest generator

For \(q=2^e\) in an effective polynomial-basis encoding, sample a uniform \(c\times n\) matrix M of covectors and set \(L=\operatorname{rowspan}M\) if full rank. If M is deficient, replace it by fixed \([I_c\ 0]\), with **no retries**; let H be the kernel. Choose a complementary dual basis to L by deterministic Gaussian elimination. Independently choose all coefficients of each \(C_i\) alternating and \(B_i\in K^{c\times d}\) uniformly via exactly e unbiased bits per field element, and construct A_i in the ambient public coordinates. The whole generator is unconditionally **worst-case polynomial**, every sample has a valid planted d-space, and every conditional public A_i law is **exactly uniform on \(W_H\)**, even on fallback. Therefore the actual full-source two-slice gated inverter still succeeds with **exactly** \(p_{c,d,q}\). No conditioned-experiment corpus or source filtering is introduced.

For arbitrary fields q, the same probability is an exact statement about an *ideal* conditional-uniform law; do not silently claim strict bounded-time exact random field-element generation if its implementation uses variable-time rejection. The public attack itself is deterministic polynomial over **all** finite fields.

## 4. Scope and why it does not nominate a cryptographic family

- The probability formula is conditional on **two independent uniform cross-blocks**, and the useful easy event \(d\ge2c\). If \(d<2c\), the stacked matrix cannot reach rank \(2c\); **this proof gives no probabilistic attack** in that regime. A failed certificate is not positive hardness evidence.
- For an arbitrary YES tuple that does not satisfy the public support-intersection certificate, no universal inversion claim follows, even if some other attack exists.
- For the separate [Liu–Qiao–Tang–Zhang planted-TI proposal (2026)](https://arxiv.org/abs/2609.31256), the conjectural \(d\simeq n/C\) with \(C\ge3\) has \(d\ll2(n-d)\), so this event cannot hold; the paper itself also has its own established polynomial algorithms in **other** large-d parameter regimes. This note is a **scoped attack boundary**, not a break of their stated conjectural parameters and not original Field-15 evidence.
- The technique is elementary low-rank image-support intersection and exact finite-field matrix-rank counting. No mathematical originality claim is made absent a comprehensive independent literature comparison. An apparent secret recovered **uniquely** is still easily public on the scoped distribution.
- The prior [fixed-c exterior-kernel full-span attack](F0-fixed-codimension-wedge-kernel-section.md) remains mathematically valid. This new sufficient condition can require only two slices and does not invoke expensive exterior coordinates, but has the different hypothesis \(d\ge2c\).

**Decision:** **SOURCE-DISTRIBUTION FAILURE / ANALYTIC EASY** for the indicated two-slice rank/support certificate and full conditioned-uniform planted source; exactly known unconditioned success. **GLOBAL NO NOMINATION**, H-A/H-B/H-C HOLD, no N1-60 reservation, HEPMR #195 BENCHMARK ONLY through AP103, #199 source ZIP blocker and historical N1-19/N1-23 PARTIAL and N1-26 HOLD unchanged.
