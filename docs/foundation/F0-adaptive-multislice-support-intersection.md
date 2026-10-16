# MORPH-F0: adaptive support-intersection inversion and exact full-source law

**Date:** 2026-10-16. **Status:** analytical attack-first no-go for a specified high-d planted source. **GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.** This is not a new F0-K/N1 number, measured experiment, sampled protocol, independent mathematical assumption, cryptographic nomination, code, OWF/PQ/PKE/KEM or trapdoor.

This extends the [two-slice public image-support attack](F0-two-slice-public-row-support-intersection.md) from \(d\ge2c\) to **all \(d>c\)**, allowing arbitrary polynomially many independently generated alternating slices and **not discarding the honest instance** just because some individual slices have rank deficiency. It derives an **exact, explicitly computable success probability** via classical Gaussian-binomial Möbius inversion and an elementary high-probability lower bound. It does not solve arbitrary planted-tensor distributions.

## 1. Honest source and full verifier

Let \(K=\mathbb F_q\) be an effectively represented finite field, \(n=c+d\), \(1\le c<d\), \(m\ge1\) polynomial in the public input size. An **unconditional polynomial-time honest source** samples *any* \(d\)-space \(H\le V=K^n\) by its explicitly stated generator, then, **independently conditional on H**, samples \(m\) uniform alternating forms \(A_i\) with \(A_i|_{H\times H}=0\). Every generated tuple has a full-verifier accepted planted basis, without filtering or rejection based on slice ranks.

The original verifier accepts **any** matrix \(Y\in K^{n\times d}\) for which
\[
\operatorname{rank}Y=d
\quad\text{and}\quad
Y^\top A_iY=0\qquad\text{for ALL }i=1,\dots,m.
\]
No requirement to recover the original hidden H is imposed on the attacker.

For proof only, write \(V=Q\oplus H\), \(\dim Q=c\), and let \(L=H^\circ\subset V^*\). Conditional on H, each public matrix has the exact block law
\[
 A_i=\begin{pmatrix}C_i&B_i\\-B_i^\top&0\end{pmatrix},
 \quad C_i\gets\mathrm{Uniform}(\operatorname{Alt}_c(K)),\quad
 B_i\gets\mathrm{Uniform}(K^{c\times d}),
\]
with all distinct blocks/slices independent. These coordinates are **not given to the attacker**. The form must have zero diagonal even in characteristic two.

## 2. Public algorithm: select good supports without source postselection

The attacker computes each **public covector image** \(S_i=\mathrm{im}(A_i:V\to V^*)\) and marks it *eligible* exactly when \(\operatorname{rank}A_i=2c\). On any honest sample, this condition is equivalent to \(\operatorname{rank}B_i=c\), and [the two-slice block lemma](F0-two-slice-public-row-support-intersection.md#2-pointwise-public-row-support-certificate) proves
\[
S_i=L\oplus R_i,\qquad R_i\le H^*,\quad \dim R_i=c
\]
for every eligible slice. The public \(\operatorname{im}A_i\) is computed without knowing that proof decomposition.

Intersect **only** the eligible \(S_i\); if none are eligible, the intersection is defined to be all of \(V^*\). If the public intersection has dimension exactly c, it **must equal** \(L\) on every honest YES input. Construct its annihilator \(H'\), output any basis Y, and check **all** original verifier equations, **including every ineligible public slice**. The original honest H makes the final check pass. If the intersection is not c-dimensional or verification fails, report failure. This public algorithm is deterministic polynomial for *any* c, m and q and never selects/rejects generator samples. It is an attack on the **actual original-verifier any-witness target**.

On the honest source, each eligible B has uniform row space among the \({d\brack c}_q\) c-spaces of \(H^*\); eligible selections are independent across slices. Ineligible slices are **ignored only by the reconstruction step**, not removed from the public instance or final verifier. Define \(X=\bigcap_{\mathrm{eligible}\ i}R_i\subset H^*\), with the empty intersection \(H^*\). Since every eligible support is \(L\oplus R_i\), the public attack succeeds **if and only if \(X=0\)** under the exact honest source.

## 3. Exact full-source success probability (every q, every H-source)

Write
\[
p_B=\Pr[\operatorname{rank}B_i=c]
=\prod_{a=0}^{c-1}(1-q^{a-d})>0,
\]
and let \({u\brack v}_q\) denote the Gaussian binomial coefficient. For each \(j=0,\ldots,d\) define
\[
a_j=\begin{cases}
\dfrac{{d-j\brack c-j}_q}{{d\brack c}_q},&0\le j\le c,\\
0,&j>c.
\end{cases}
\qquad
\theta_j=1-p_B+p_B a_j.
\]
Here \(a_j\) is the **conditional** probability that one uniformly random c-space contains one fixed j-space J. For every fixed J, an individual slice does **not** exclude J from X precisely if it is *ineligible* (probability \(1-p_B\)) or eligible and its row space contains J (probability \(p_B a_j\)). Independence of the m conditional uniform forms therefore gives
\[
\Pr[J\le X\mid H]=\theta_j^m,
\qquad j=\dim J.
\]

**Exact theorem (subspace-lattice Möbius inversion).** For any \(1\le c<d\), any m, any finite field and **any honest H-distribution** in the specified conditional-uniform model, the exact unconditioned attack-success probability is
\[
\boxed{\quad
p_{\rm attack}(c,d,m,q)=
\sum_{j=0}^{d}
 (-1)^j q^{\binom j2}{d\brack j}_q\,
      \bigl(1-p_B+p_B a_j\bigr)^m.
\quad}
\]

**Proof.** For a subspace J of dimension j, the Möbius coefficient from zero to J in the finite-field subspace lattice is \(\mu(0,J)=(-1)^j q^{\binom j2}\). For any X, \(\mathbf1[X=0]=\sum_{J\le X}\mu(0,J)\). Take expectations and group the J by dimension using \({d\brack j}_q\) possibilities and the exact \(\theta_j^m\). The identity is equivalent to the Gaussian q-binomial theorem, which gives \(\sum_{J\le X}\mu(0,J)=0\) for every nonzero X. The expression is **the exact attack probability conditional on every fixed H**, so averaging over the original unconditional H-source leaves it unchanged. No independence assumption across projective lines is needed.

All \({d\brack j}_q\), p_B and powers can be calculated using polynomially many finite products and integer/rational arithmetic of **polynomial bitlength in \(n,m,\log q\)**. The exact formula is **not an empirical measurement**, not an unbounded enumerate-all-subspaces attack and not a claim of an optimal adversary. Its value is zero in some small-m regimes; success tends to one for \(d>c\) as the number of independent slices increases. [Classical source for subspace Möbius function](https://www.sfu.ca/~mdevos/notes/comb_struct/mobius.pdf) and [Stanley, *Enumerative Combinatorics*, the q-binomial theorem](https://math.mit.edu/~rstan/ec/ec1.pdf).

## 4. A universal simple high-probability bound for d>c

For a fixed nonzero **projective line** \(\ell\le H^*\), its chance to survive all eligible supports is \(\theta_1^m\), where
\[
a_1=\frac{q^c-1}{q^d-1},\qquad
\theta_1=1-p_B(1-a_1).
\]
If \(X\neq0\), it contains at least one such line. A **union bound**, with no false independence assumption among lines, yields
\[
\Pr[X\neq0]\le
\frac{q^d-1}{q-1}
 \left[1-p_B\left(1-\frac{q^c-1}{q^d-1}\right)\right]^m.
\]

For **every** finite field \(q\ge2\) and every \(d\ge c+1\), the full-row-rank probability satisfies
\[
p_B=\prod_{s=d-c+1}^{d}(1-q^{-s})
 \ge \prod_{s=2}^{\infty}(1-2^{-s})\ge\tfrac12,
\]
and \(a_1<q^{c-d}\le1/2\). Hence \(\theta_1\le3/4\), giving the elementary **unconditional source attack** guarantee
\[
\boxed{\quad
p_{\rm attack}\ge
\max\!\left(0,\;
1-\frac{q^d-1}{q-1}\,(3/4)^m
\right).\quad}
\]
For any desired \(\delta>0\), \(m\ge(\ln((q^d-1)/(q-1))+\ln(1/\delta))/\ln(4/3)\) suffices to make success at least \(1-\delta\). If \(\log q\) and the demanded \(\log(1/\delta)\) are polynomial in n, this uses **polynomially many public slices**, even if c grows linearly with n. At **d=c** every eligible row space is all of \(H^*\), so the support-intersection attack **does not** recover L by this method; the strict inequality \(d>c\) is essential.

### Connection with the exact two-slice result

For \(m=2,d\ge2c\), the only way the selected row-space intersection vanishes is for both \(B_i\) to have full row rank and disjoint c-row spaces, equivalently \(\operatorname{rank}\begin{psmallmatrix}B_1\\B_2\end{psmallmatrix}=2c\). The exact expression in §3 therefore specializes to the earlier [two-slice product](F0-two-slice-public-row-support-intersection.md#3-exact-original-source-probability-with-two-slices),
\(\prod_{j=0}^{2c-1}(1-q^{j-d})\). When \(c<d<2c\), this **two-slice** event is impossible, but larger m can make \(X=0\); this is a genuine extension with a different observation count, **not** a retroactive claim about the earlier two-slice theorem.

## 5. Unconditional strict-generator and scope limits

For \(q=2^e\) with an effective binary polynomial-basis representation, instantiate the [bounded honest generator with fixed full-rank fallback](F0-two-slice-public-row-support-intersection.md#a-strictly-worst-case-polynomial-exact-binary-field-honest-generator) and sample all m alternating slices independently through uniformly chosen B_i and C_i coefficients. Every sample **always** contains a planted H; conditional independence and uniformity hold even on fallback. Therefore both the exact Möbius formula and the bound above apply to the **actual unconditional strictly worst-case-polynomial binary-field source**, not only a filtered idealization. For other q, the uniform source formulas are ideal unless a concrete finite-field sampler's strict time/TV properties are explicitly proved; public inversion remains deterministic polynomial for all q.

**Outside scope:** arbitrary nonuniform conditional slice laws, unsynchronized/hidden slice correspondences, added witness restrictions not in V, or the external planted-TI conjectural \(d\approx n/C\) with \(C\ge3\) (so \(d<c\), violating this theorem). The [Liu–Qiao–Tang–Zhang 2026 work](https://arxiv.org/abs/2609.31256) already studies polynomial algorithms for other high-d regimes and **does not become a MORPH independent foundation**. The present result is an elementary high-rank image-space recovery and a classical Möbius counting application, not a novelty claim. Failure of the public sufficient certificate never implies general hardness or Field 15.

**Disposition:** **ANALYTIC EASY / SOURCE-DISTRIBUTION FAILURE** for the precisely conditioned uniform planted model with \(d>c\), m satisfying the source bound, with a deterministic attack that verifies the complete original tuple. **GLOBAL NO NOMINATION**, H-A/H-B/H-C HOLD, N1-60 unallocated, HEPMR #195 BENCHMARK ONLY through AP103, #199 ZIP blocker and historical N1-19/N1-23 PARTIAL, N1-26 HOLD unchanged.
