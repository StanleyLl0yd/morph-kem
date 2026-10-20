# MORPH-F0: exact planted-wrong disjoint-seed quotient and null-coupling boundary

**2026-10-20. Analytic source-law refinement; GLOBAL NO NOMINATION, H-A/H-B/H-C HOLD.** This answers a specific warning in the [null residual rank-gate theorem](F0-planted-ti-null-residual-rank-gate.md): an arbitrary false T inside a planted sample is **not** distributed like a null seed. For a **precommitted false T disjoint from H**, the quotient admits an exact planted-subspace law indexed by the rank of a hidden subblock. The result gives an exact finite rank-gate formula and a restricted local-observation TV bound. It is **not** a polynomial seed selector, any-witness inverter, full-tensor indistinguishability theorem, or new hard mathematical foundation.

**Original source:** fix any d-plane H<=V=F_q^n (or first draw H from any independent prior); then independently sample m uniform alternating forms A_i annihilating H x H, publishing all n-by-n coefficients. The original accepted relation remains **any** d-plane L with all A_i|_(L x L)=0. For comparison, unrestricted null samples independent uniform alternating forms without H. All statements concern these **unfiltered** sources, including characteristic two (alternating means zero diagonal). Earlier planted-TI work: [Liu–Qiao–Tang–Zhang (2026)](https://arxiv.org/abs/2609.31256); previous high-d alternating-rank law: [sparse rank-profile control](F0-sparse-planted-ti-rank-profile-minrank-screen.md).

## 1. Fixed H-disjoint T: a uniform public cross map, but a planted residual

Let 1<=t<=n-d=c, and fix a t-plane T with \(T\cap H=0\), **before** any A_i is drawn. Use a *proof-only* splitting

\[
V=T\oplus H\oplus C',\quad \dim C'=c-t=:b.
\]

Write \(E_i=A_i|_{T\times T}\), and \(B_i=A_i|_{T\times(H\oplus C')}\). The joint T-isotropy event \(I_T\) has exact probability \(q^{-m{t\choose2}}\), and conditional on \(I_T\),

- the stacked public T-contraction cross map \(M=(B_i)_i\) is **uniform** in \(F_q^{mt\times(n-t)}\);
- its H-column submatrix \(M_H\) is a uniform mt-by-d matrix (this hidden block is **not given to the attacker**);
- all remaining H-plus-C' alternating blocks \(D_i\) are mutually independent and uniform subject only to \(D_i|_{H\times H}=0\), also independent of **the entire value of M**.

**Proof.** In the chosen splitting every alternating coefficient except the H×H block is an independent uniformly sampled coordinate. T×T entries form E, T×(H+C') entries form B, and (H+C')×(H+C') entries form D. Disjoint free coordinates remain independent after conditioning on E_i=0. QED.

For any realized M define \(K=\ker M\le H\oplus C'\). Then

\[
S_A(T)=T\oplus K,\qquad W_T=S_A(T)/T\cong K,
\qquad F=K\cap H,\quad
\boxed{\dim F=d-\operatorname{rank}M_H.}
\]

This holds without requiring M to have full row rank.

**Theorem 1 (exact conditional residual planted law for a disjoint false seed).** Conditional on I_T and on the entire M, the induced m alternating forms on W_T are **independent uniform alternating forms vanishing on F×F**, with the fixed conditional planted subspace \(F=H\cap K\). In particular, when \(\dim F\le1\), the induced m forms are exactly **independent unrestricted uniform alternating forms** on W_T. For \(\dim F\ge2\), one cannot silently replace them by unrestricted-null forms.

**Proof.** Each quotient form is \(D_i|_{K\times K}\); the T pairings vanish on T⊕K by construction of M. The image of the restriction map

\[
\{D\in\operatorname{Alt}(H\oplus C'):D|_{H\times H}=0\}
\ \longrightarrow\operatorname{Alt}(K)
\]

is **exactly** \(\{E\in\operatorname{Alt}(K):E|_{F\times F}=0\}\). Necessity follows by F<=H. To prove surjectivity, extend a basis of F first to bases of H and K; their additional basis vectors are independent because H∩K=F. Prescribe any target form vanishing on F×F on K, zero on H×H, and arbitrary (say zero) values on remaining independent basis pairs; this extends to a compatible form on H+C'. Surjective linear maps send uniform finite-vector-space inputs to uniform outputs. Since the D_i are independent conditional on M, their restrictions remain independent. If dim F<=1, alternating bilinearity makes the constraint E|_F=0 vacuous. QED.

**Selection boundary.** T is fixed outside H and independently of the tensor; conditioning on its *public isotropy* is explicit in this calculation. This theorem is **not** an arbitrary planted-wrong seed law when T meets H nontrivially, nor a license to assign fixed-T distributions to the attacker's tensor-adaptive choice.

## 2. Exact false-seed rank gate by a finite matrix-rank mixture

Adopt the **public full-row residual gate** parameter range of the [null source theorem](F0-planted-ti-null-residual-rank-gate.md):

\[
0<mt<c,\quad 0<\ell=c-mt<u=d-t,\quad
D=u+\ell=n-t-mt.
\]

For any k<=D, define \(\Phi_{D,k,\ell,q}\) as the probability that a **single** uniform alternating form on an ambient D-space, conditioned to annihilate a prescribed k-plane on both inputs, has matrix rank <=2\ell. This is an exact rational number depending only on D,k,\ell,q (not the k-plane's orientation).

Use the exact rectangular rank mass

\[
\pi_{a,b}(z)=q^{-ab}{a\brack z}_q{b\brack z}_q
|\mathrm{GL}_z(q)|,\quad
|\mathrm{GL}_z(q)|=\prod_{j=0}^{z-1}(q^z-q^j).
\]

Let \(h_{s,q}(v)\) be the **exact** corank-v mass of a uniform s-by-s alternating matrix:

\[
h_{s,q}(v)=
\begin{cases}
q^{-{v\choose2}}\,G_s/(G_v S_{(s-v)/2}),
  &0\le v\le s,\;s-v\ \text{even},\\
0,&\text{otherwise},
\end{cases}
\]

where \(G_j=\prod_{a=1}^j(1-q^{-a})\), \(S_j=\prod_{a=1}^j(1-q^{-2a})\), and all products over empty index sets equal 1. The rank-profile document already proves this elementary symplectic counting formula. A planted k-plane decomposition has uniform k-by-(D-k) cross block of rank z; after splitting z hyperbolic pairs the full alternating corank is \(k-z+v\) where v is the corank of an independent uniform Alt(D-k-z). Therefore

\[
\boxed{
\Phi_{D,k,\ell,q}
=\sum_{z=0}^{\min(k,D-k)}\pi_{k,D-k}(z)
 \sum_{\substack{0\le v\le D-k-z\\k-z+v\ge D-2\ell}}
 h_{D-k-z,q}(v).
}
\]

This formula has polynomially many rational terms and no exponential seed enumeration. It is a **probability evaluator**, not an inverter. In particular

\[
\boxed{\Phi_{D,0,\ell,q}=\Phi_{D,1,\ell,q}
=\tau_{D,\ell,q}}
\]

for the unrestricted-null rank tail \(\tau\) in the previous note.

Define \(F_b(s)=\prod_{j=0}^{s-1}(1-q^{j-b})\) for \(0\le s\le b\), \(F_b(0)=1\), and \(F_b(s)=0\) when s>b or s<0. This is the probability b fresh uniform columns span an s-dimensional row quotient.

**Theorem 2 (exact finite fixed-disjoint-false-seed gate rate).** For any fixed H,T with T∩H=0, the honest planted source's probability that public T passes **all three** tests (T isotropic, full mt public contraction row rank, all m quotient alternating ranks <=2\ell) equals

\[
\boxed{
P_{\rm disjoint\ false}
=q^{-m{t\choose2}}
\sum_{r=0}^{\min(mt,d)}
\pi_{mt,d}(r)\,
F_{c-t}(mt-r)\,
\Phi_{D,d-r,\ell,q}^{\,m}.
}
\]

For the unrestricted-null source the corresponding exact fixed-T rate is

\[
\boxed{
P_{\rm null}
=q^{-m{t\choose2}}
F_{n-t}(mt)\,\tau_{D,\ell,q}^{\,m}.
}
\]

**Proof.** Conditional on T isotropic, the mt×d H-column matrix of M has rank r with probability \(\pi_{mt,d}(r)\). Independently append b=c-t uniform C' columns. They raise M to full row rank mt with probability \(F_b(mt-r)\). On that event K has fixed dimension D, F=K∩H has dimension d-r, and by Theorem 1 each induced form is an independent planted-(d-r) alternating source; its public rank-gate probability is \(\Phi_{D,d-r,\ell,q}\). Multiply m independent conditional residual probabilities and sum across disjoint rank-r events. The null formula is Theorem 2 of the previous note. No hidden rank r is used by the real public gate, and no independence across distinct public seeds is asserted. QED.

## 3. Strongest safe restricted null coupling when the hidden cross block is full rank

Conditional on I_T, the public M has exactly the same uniform distribution for a fixed H-disjoint planted seed and a fixed null seed. Given M, the public quotient forms have identical distributions whenever \(\operatorname{rank}M_H\ge d-1\), by Theorem 1 (then dim F<=1). Introduce the fixed H **only in the analysis** of the null experiment and couple the two quotient sources identically off the exceptional event.

**Theorem 3 (local observation TV; not full tensor TV).** Conditional on I_T, for the joint local observation \((M,(\bar A_i|_{W_T})_i)\), with W_T and its public basis calculated from M,

\[
\boxed{
\operatorname{TV}\bigl(
\mathcal L_{\rm planted}^{H,T}(\text{local data}\mid I_T),
\mathcal L_{\rm null}^{T}(\text{local data}\mid I_T)
\bigr)
\le \Pr[\operatorname{rank}(\mathrm{Unif}(F_q^{mt\times d}))\le d-2].
}
\]

If mt>=d, the previous rectangular-rank tail lemma gives

\[
\boxed{\operatorname{TV}(\text{these local observations})
\le \min(1,C_q q^{-2(mt-d+2)}),\qquad C_q<4.}
\]

This includes public rank-deficient cross maps M, because the proof does not need to condition on full row rank. The rank-gate event is deterministic postprocessing of this observation (and public T), so its **conditional-isotropy** planted-disjoint versus null event probability differs by no more than the same bound. The unconditional gate-rate difference is further multiplied by the common factor \(q^{-m{t\choose2}}\).

**Proof.** Conditional on T isotropy, M is uniform in both experiments. Couple it identically; when rank(M_H)>=d-1, F=H∩ker M has dimension <=1 and the conditional quotient law is exactly unrestricted uniform, so couple the m quotient forms identically too. The remaining exceptional M occur with the displayed uniform-matrix rank probability. Data processing gives the same bound for the gate. Apply the [uniform rectangular-rank tail](F0-planted-ti-randomized-flag-search.md#3-uniform-finite-rank-tail-lemma-for-fixed-genuine-prefixes) at a=mt>=b=d with rank deficit u=2. QED.

For fixed q, \(d/n\to\alpha\in(0,1/3)\), \(m\asymp n/\log n\), and the shorter-seed t from the previous null rank-gate theorem,

\[
mt-d=(1-3\alpha)n+o(n)>0,
\quad
\boxed{\operatorname{TV}(\text{fixed-disjoint-seed local observation})
\le q^{-2(1-3\alpha)n+o(n)}.}
\]

This is exponentially strong **for each precommitted H-disjoint false T** and the stated restricted local observation. It does **not** union bound over the \(q^{\Theta(n\log n)}\) public seeds, condition on an adaptively chosen T, or bound TV of the **complete published tensor**. At the boundary \(\alpha=1/3\), the sign of mt-d depends on lower-order parameter details; for \(\alpha>1/3\) a large residual H∩ker M remains typical, so the unrestricted-null approximation cannot be inferred from this bound.

## 4. Independent exact small-field controls (scratch, not sampling)

Take q=2, n=9,d=4,c=5,m=4,t=1. Then \(\ell=1,u=3,D=4\), and for a precommitted **false** line T disjoint from H, the residual planted-k rank<=2 probabilities computed using the finite rank mixture are

\[
\Phi_{4,k,1,2}=
\begin{cases}
9/16,&k=0,1,\\
5/8,&k=2,\\
1,&k=3,4.
\end{cases}
\]

Independently enumerate all compatible GF(2) alternating 4-by-4 matrices for each fixed k-plane, with zero k×k alternating block. Successful rank<=2 counts are respectively **36/64, 36/64, 20/32, 8/8, 1/1**, precisely matching the mixture rather than assuming an unrestricted rank distribution after false-seed conditioning.

Combining the **independent exact rectangular-rank mass** for M_H (4×4) with fresh c-t=4 cross columns gives

\[
\boxed{
P_{\rm disjoint\ false}
=\frac{1736641305}{17179869184}\approx0.101086,\qquad
P_{\rm null}
=\frac{414969504705}{4398046511104}\approx0.094353.
}
\]

They are **different**, as required by the scope warning of PR #255. Their difference is accounted for by the rank-defect cases with residual \(k\ge2\); the probability of that exceptional H-cross rank event is \(947/8192\), a valid (loose) coupling bound. These are block enumerations and rational-source calculations, **not** an exhaustive 9-dimensional m=4 full-tensor attack run, committed implementation, parameter validation or measured test.

## 5. Falsification boundary and next step

- The new finite mixture is an exact analysis of the **precommitted H-disjoint false T**, not a polynomial algorithm for finding T<=H, a false-seed sampler with a new distribution, or a claimed result for T intersecting H in an arbitrary positive dimension.
- The local TV result deliberately reveals only the precommitted T's cross map plus induced quotient forms. An attacker receiving the **entire tensor** is outside its scope; adding the unused blocks could destroy the TV bound.
- The [unrestricted-null enumeration theorem](F0-planted-ti-null-residual-rank-gate.md) remains correct as a null/planted distinguisher, but its expectation **must not** be quoted as an upper bound on the number of wrong gate-passing T inside planted instances.
- Genuine polynomial progress still requires tensor-adaptive public selection of promising true seeds with a proved unconditional original-source advantage and a full original-verifier witness. An explicit rank-gate predicate alone does not give that.
- No source corpus, KEM/PKE/OWF, A-ID, F0-K, N1-60 allocation, Field-15 novelty, README change, stage-registry edit, quantum implementation or attack benchmark is authorized.

**Disposition:** EXACT PLANTED-DISJOINT-FALSE-SEED RESIDUAL SOURCE / FINITE MIXTURE / RESTRICTED LOCAL NULL COUPLING. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD; HEPMR BENCHMARK ONLY.
