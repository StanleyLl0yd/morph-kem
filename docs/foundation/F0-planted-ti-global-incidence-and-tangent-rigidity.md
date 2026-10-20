# MORPH-F0: full-public-tensor incidence and tangent-rigidity screen

**2026-10-20. Analytical full-source geometry, not an inversion algorithm. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.** This studies the actual public alternating matrices, not the pair/linear-bivector oracle from the [adaptive span notes](F0-planted-ti-adaptive-linear-bivector-probe-tv.md). No new N1/F0-K/A-ID, implementation, generated source instances, candidate, hardness claim, KEM/PKE/OWF or trapdoor.

**Research provenance and priority.** The planted totally-isotropic (TI) tensor problem is an external relation discussed by Liu, Qiao, Tang and Zhang, [*The planted tensor problem over finite fields: algorithms and cryptography*](https://arxiv.org/abs/2609.31256). The [earlier #208 size-bias/uniqueness checkpoint](https://github.com/StanleyLl0yd/morph-kem/issues/208#issuecomment-6215551334) already discussed first-moment uniqueness; **this note does not re-claim that fact**. Its scoped additions are an exact rank-by-rank tangent-kernel profile, a matching finite-n wrong-witness incidence profile, their unexpected common exponent, and an explicit algebraic-geometry limitation on local linearization attacks. All formulas below are derived for the stated unconditional source, not borrowed hardness claims.

## 1. Exact source and original verifier

Let V=F_q^n, q any prime power, 2<=d<n, c=n-d, and m>=1. First draw H from an arbitrary prior on Gr(d,V), with no rejection of H. Conditional on H, draw independent **uniform** alternating bilinear forms A_1,...,A_m from the linear space of forms vanishing on H x H. The null distribution consists of independent uniform alternating forms on V. Characteristic two is included: alternating forms have zero diagonal.

A full-public-tensor attacker is handed **every entry of every A_i**. The original accepted set is

\[
\mathcal E(A)=\{L\in\operatorname{Gr}(d,V):A_i|_{L\times L}=0\text{ for all }i\}.
\]

**Any** L in E(A) is a successful search witness; identifying the sampled H is not separately required. The planted source guarantees H in E(A). It does not assume that the attacker knows H or is restricted to query an oracle.

Fix H only for *conditional probability analysis*. Choose V=H\oplus C, dim C=c, and bases. The planted matrices have block form

\[
A_i=\begin{pmatrix}0&B_i\\-B_i^T&D_i\end{pmatrix},
\quad B_i\in F_q^{d\times c}\text{ uniform},\quad
D_i\in\operatorname{Alt}_c(F_q)\text{ uniform}.
\]

Every B_i and D_i is independent over i (and independent within a slice). For a graph L_X={(h,Xh):h in H} of X in Hom(H,C), the **exact** public isotropy equations in this private analysis chart are

\[
F_i(X)=B_iX-X^TB_i^T+X^TD_iX=0,\qquad i=1,\ldots,m.
\]

They are homogeneous quadratic-plus-linear equations in dc unknown entries of X; their coefficients B_i,D_i refer to an **unknown** H and chart, so this representation is *not* an attacker-given inversion method.

## 2. Exact tangent-kernel rank profile

The differential of the full equations at the planted chart origin X=0 is

\[
J_H(X)=(B_iX-(B_iX)^T)_{i=1}^m
\in \operatorname{Alt}_d(F_q)^m .
\]

It is a linear map of the dc-dimensional tangent space Hom(H,V/H); the expression is basis-independent under the natural change of chart.

**Theorem 1 (rank-r tangent test).** For *every fixed* nonzero X:H->C of rank r, 1<=r<=min(d,c), under the unconditional honest source conditional on any fixed H,

\[
\boxed{\Pr[J_H(X)=0\mid H]=q^{-m k_r}},
\qquad
k_r=r(d-r)+\binom r2=\frac{r(2d-r-1)}2 .
\]

**Proof.** Choose a basis of H adapted to ker(X). The d-by-d product B_iX has r arbitrary columns and d-r zero columns, because B_i is uniform and composition with X surjects onto the full space of d-by-r first columns. For it to be symmetric (equivalently B_iX-(B_iX)^T=0, also in characteristic two), the lower-left (d-r)-by-r block must be zero, imposing r(d-r) independent scalar equations, and the r-by-r upper block must be symmetric, imposing binom(r,2) more. Therefore one slice passes with probability q^(-k_r); independence of m slices raises this to the m-th power. QED.

The number of **rank-r maps** H->C is exactly

\[
N_r=\left[{d\atop r}\right]_q\prod_{j=0}^{r-1}(q^c-q^j)
=\left[{d\atop r}\right]_q\left[{c\atop r}\right]_q|\mathrm{GL}_r(q)|.
\]

Therefore (linearity of expectation, no independence between different X assumed)

\[
\boxed{\mathbb E[\#\{X\ne0:J_H(X)=0\}\mid H]
 =\sum_{r=1}^{\min(d,c)}N_rq^{-mk_r}},
\]

and the same sum upper-bounds Pr(ker J_H !=0 | H) by the union bound. The tangent source law and formula are identical for every H; no uniform-H prior is needed.

## 3. Exact incidence profile of globally different witnesses

**Theorem 2 (wrong d-plane count).** For a fixed different d-plane L with dim(L cap H)=d-r,

\[
\boxed{\Pr[L\in\mathcal E(A)\mid H]=q^{-mk_r}}.
\]

Moreover, the number of such L for given H,r is

\[
M_r=\left[{d\atop r}\right]_q
     \left[{c\atop r}\right]_q q^{r^2}.
\]

Consequently the **exact conditional expected number of accepted L != H** and an upper bound on the probability of nonuniqueness are, respectively,

\[
\boxed{\mathbb E[|\mathcal E(A)|-1\mid H]
 =\sum_{r=1}^{\min(d,c)} M_r q^{-mk_r}},
\qquad
\Pr[|\mathcal E(A)|>1\mid H]\le\sum_r M_rq^{-mk_r}.
\]

**Proof.** The intersection of exterior-square subspaces is
Lambda^2 L cap Lambda^2 H = Lambda^2(L cap H). Conditional-uniform forms already annihilate Lambda^2 H, so vanishing also on L adds precisely binom(d,2)-binom(d-r,2)=k_r independent linear conditions per slice. To count L, choose T=L cap H (a (d-r)-plane of H), its r-dimensional image S in V/H (an r-plane in C), and the graph map S->H/T (r² independent scalar coordinates). The count is M_r. QED.

**Rank-profile link (the new cross-check).** For every r,

\[
\boxed{N_r=M_r\,|\mathrm{GL}_r(q)|/q^{r^2}},
\]

so tangent null-vector and wrong-witness expectations have *exactly the same field-exponential incidence penalty* q^(-m k_r), and differ by the explicit invertible-matrix density factor. This algebraic coincidence does **not** give a map from an unknown planted H or a tangent direction to an accepted public witness.

## 4. Explicit high-probability consequence

Set C_q=prod_{j>=1}(1-q^{-j})^{-1}; uniformly for q>=2, C_q<4. Standard finite Gaussian-binomial estimates yield

\[
N_r\le C_qq^{r(n-r)},\qquad M_r\le C_q^2q^{r(n-r)}.
\]

Define Δ=m(d-1)/2-(n-1). Since r<=d gives k_r>=r(d-1)/2 and r(n-r)<=r(n-1), for any Δ>0,

\[
\boxed{\Pr[\ker J_H\ne0\mid H]\le
 C_q\,\frac{q^{-\Delta}}{1-q^{-\Delta}}},
\]

\[
\boxed{\Pr[|\mathcal E(A)|>1\mid H]\le
 C_q^2\,\frac{q^{-\Delta}}{1-q^{-\Delta}}}.
\]

Bound each probability by 1 if the displayed expression exceeds 1. For fixed q and d/n->alpha with 0<alpha<1/2, m=Theta(n/log n), both error bounds are q^(-Omega(n²/log n)). Thus the **actual complete published tensor** has, overwhelmingly under this specific planted distribution, (a) a unique F_q-rational accepted d-plane and (b) an injective Jacobian at that planted point. The Jacobian has full column rank over F_q and hence over its algebraic closure: the planted point is isolated and reduced in its local common-isotropic scheme. This local conclusion does **not** rule out other non-rational geometric points elsewhere.

The exact finite-rank sums above are preferable to this deliberately coarse bound at the threshold or with small parameters. A necessary deterministic dimensional condition for Jacobian injectivity is m*binom(d,2)>=dc; this follows just from the Jacobian matrix dimensions and is not an algorithm.

## 5. Independent tiny arithmetic control (not a source benchmark)

For q=2, d=3, c=2, m=2, r=1,2:
- k_1=2, k_2=3; N_1=21 and N_2=42.
- Theorem 1 predicts expected rank-1 null directions =21/16 and rank-2 null directions =21/32.
- Exhausting all 2^(2dc)=4096 ordered pairs of binary 3-by-2 cross blocks B_i and all 2^(dc)=64 maps X confirms those two exact expectations.
- Theorem 2 gives M_1=42, M_2=112, hence expected extra witnesses 42/16+112/64=35/8 in this deliberately weak tiny setting; this last number is an exact formula evaluation, **not** a separately enumerated public-form corpus.

These are independent scratch finite-field formula checks, **not** committed attack tests, CI counts, honest-sampler outputs, or evidence for a parameter set.

## 6. Cryptanalytic interpretation and falsification priority

This pass studies the **global full-public quadratic constraints** and explicitly avoids the oracle-only assumption of PR #239-241. It resolves the finite-n geometry at the hidden solution, *not* the missing inversion complexity:

1. **Overdetermined does not mean efficiently solvable.** The tangent matrix J_H is trivial to compute only *after H is known*. One cannot use the hidden chart in a valid public attack. Local Newton/Hensel-style intuition does not provide a polynomial starting point for an unknown solution of an overdetermined finite-field quadratic system.
2. **Uniqueness is not hardness and not a public section.** On these honest parameters, a public accepted witness will usually coincide with H, but nothing above gives an efficient algorithm to output it. Conversely, unique-solution phenomena cannot serve as evidence of post-quantum inversion hardness.
3. **Search-to-detection is not an efficient detector.** An unbounded test for existence of a d-plane separates planted and null in this regime, but enumerating Gr(d,V) is not polynomial; no full-tensor polynomial distinguishability result is claimed here.
4. **Next genuine attack screen:** work with public coordinate-free algebraic invariants of the *whole* tuple (common exterior annihilator, determinantal/flattening ideals, tensor-derived adaptive subspaces, linearization ranks away from H) and require a demonstrated polynomial procedure returning any full-verifier accepted L, with the original unconditional distribution. The oracle-only TV bounds do not apply to tensor-dependent choices.

**Disposition:** EXACT GLOBAL INCIDENCE / PLANTED TANGENT RIGIDITY, ANALYTICAL NEGATIVE CONTROL ONLY. H-A HOLD, GLOBAL NO NOMINATION, H-B/H-C HOLD, HEPMR BENCHMARK ONLY; N1-60 still free. No README, stage registry, code, experiment, or crypto-status change.
