# MORPH-F0: exact planted third central bivector-count moment by four quotient line types

**2026-10-19. Analytical-only source-first statistics theorem; GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.** This follows the [previous null third moment](F0-dual-bivector-null-third-central-moment.md) and the [planted exact quotient-line fibres](F0-dual-bivector-kernel-exact-source-moments.md). Their mean, variance, and null third moment retain their original priority. No candidate, attack ID, N1/F0-K stage, generated security experiment, implementation, OWF/PKE/KEM, trapdoor, or claim of mathematical cryptographic novelty.

**External problem.** Liu, Qiao, Tang and Zhang, *The planted tensor problem over finite fields: algorithms and cryptography*, [arXiv:2609.31256v1](https://arxiv.org/abs/2609.31256). The paper's conjectural sparse-m regime is not assumed hard merely because the exact moments below are computable symbolically.

## 1. Original unfiltered planted relation and quotient-fibre source

Let V=F_q^n for any prime power q>=2, 2<=d<n, c=n-d>=1 and m>=1. The original honest source first chooses any d-plane H via a specified unconditional distribution, and then samples m independent **uniform alternating** bilinear forms vanishing on H x H. Zero diagonals are mandatory in characteristic two. Null forms are m iid unrestricted uniform alternating forms. The original full verifier accepts any n-by-d rank-d Y satisfying Y^T A_i Y=0 for **every** public i. There is no postselection by rank, count, or geometry.

Let X=Z_2 be the count of isotropic 2-planes surviving the full tuple. Work conditionally on each H, put U=Lambda^2 H and Q=(Lambda^2 V)/U. The [previous rank-two note](F0-dual-bivector-kernel-exact-source-moments.md#3-planted-law-exact-expectation-and-the-entire-covariance-structure) proved that X has the exact representation

\[
X=[d\choose2]_q+\sum_{\ell\in\mathcal S}f_\ell I_\ell,
\]

where every I_ell says that m independent uniform linear forms on Q annihilate the projective line ell; each has probability p=q^{-m}. The support S and weights f are **exactly**:

- Type A: projective rank-one tensors [h tensor c] in H tensor C (for a proof-only splitting V=H direct-sum C), one for every ([h],[c]) in P(H) times P(C); the number of directions is a=[d choose1]_q[c choose1]_q, and **every** such direction has weight w=q^(d-1).
- Type B: graph 2-planes projecting injectively onto a 2-plane P<=C; there are b=q^(2d)[c choose2]_q quotient directions, **each of weight 1**. Such directions have nonzero Lambda^2 C component and are disjoint from Type A.

The I_ell for distinct ell are pairwise independent, but not generally three-wise independent. The conditional law of X depends on H only through its dimension d, so centered conditional and unconditional moments coincide for **every** unconditional H-prior. These weights and directions come from the **entire** original honest law, without discarded draws.

## 2. Four types of projective support lines

Define the numbers of distinct projective lines L<=P(Q) with the indicated support:

\[
\begin{aligned}
L_{\rm I}&=[d\choose1]_q[c\choose2]_q+[c\choose1]_q[d\choose2]_q,\\
L_{\rm II}&=[c\choose2]_q\,q^{2d-1}[d\choose1]_q[2\choose1]_q,\\
L_{\rm III}&=[c\choose2]_q\,q^{2d-1}
  \big([2d\choose1]_q-[d\choose1]_q[2\choose1]_q\big),\\
L_{\rm IV}&=[c\choose1]_q[c-1\choose2]_q\,q^{3d}.
\end{aligned}
\]

All Gaussian binomials with out-of-range indices are interpreted as zero. The four families are **disjoint**, with exactly the following supported points on every line:

| Family | Supported directions on the line | Number of such lines |
|---|---|---|
| I: Segre line | q+1 type-A points, each weight w | L_I |
| II: same transverse 2-plane, rank-one affine direction | one type-A point of weight w and q type-B points of weight 1 | L_II |
| III: same transverse 2-plane, rank-two affine direction | q type-B points of weight 1; point at infinity is unsupported | L_III |
| IV: coherent varying transverse 2-plane | q+1 type-B points of weight 1 | L_IV |

**Exhaustiveness proof.** Project Q further to Lambda^2 C. The projective image of a line has linear rank 0, 1, or 2.

1. If rank 0, the line lies in P(H tensor C). Three distinct supported type-A points force all 2x2 Segre minors, homogeneous quadratics restricted to the projective line, to vanish identically (three distinct projective zeros suffice even over GF(2)). Thus it is a Segre line: fix [h] and vary [c] in a 2-plane, or fix [c] and vary [h] in a 2-plane. This counts L_I.
2. If rank 1, there is a unique point at infinity with vanishing Lambda^2 C component, and q points over the same fixed transverse P<=C. Choose an affine graph f:P->H and a nonzero projective direction delta in Hom(P,H), a 2d-dimensional vector space. Every affine coset of the one-dimensional subspace <delta> supplies q B-points. The infinity point is type A **if and only if delta has matrix rank one**. Such projective directions number [d choose1]_q[2 choose1]_q; the remaining [2d choose1]_q minus this are rank two. For every fixed P and delta, there are q^(2d-1) cosets. This gives exactly L_II and L_III.
3. If rank 2, there is no type-A point. Three supported B-points force their Lambda^2 C projections onto a projective line in the Plücker Grassmannian Gr(2,C). Its quadratic Plücker equations have three distinct zeros and hence vanish identically, so the transverse 2-planes sweep the pencil containing a fixed 1-plane R inside a fixed 3-plane W<=C. Two graph lifts agree on R **if and only if** a third point of their projective line is type B; once they agree, they glue uniquely to a linear graph f:W->H and **all q+1 points** are type B. Conversely every flag R<W in C and every f:W->H yields exactly one such supported line. Their number is [c choose1]_q[c-1 choose2]_q q^(3d)=L_IV.

These cases include q=2: a rank-two affine line in family III has only q=2 supported points and therefore contributes **no** distinct supported triple. No unsupported direction is ever counted as a surviving isotropic 2-plane.

## 3. Exact planted third centered moment

Let

\[
\begin{aligned}
C_{\rm pl}={}&(q+1)q(q-1)w^3 L_{\rm I}\\
&+q(q-1)\big((q-2)+3w\big)L_{\rm II}\\
&+q(q-1)(q-2)L_{\rm III}\\
&+(q+1)q(q-1)L_{\rm IV}.
\end{aligned}
\]

This is the exact **weighted count of ordered triples of distinct supported quotient directions on one projective line**. Family II has 3q(q-1) ordered triples with one A and two Bs, plus q(q-1)(q-2) triples containing only Bs; all other terms follow from the uniform type weights.

**Theorem (exact for all finite q,n,d,m above).**

\[
\boxed{
\mathbb E_{\rm pl}[(X-\mathbb E_{\rm pl}X)^3]
=p(1-p)(1-2p)(aw^3+b)+p^2(1-p) C_{\rm pl}.
}
\]

**Proof.** Expand the centered cube of the exact weighted quotient-direction representation in Section 1. For a single line ell, the Bernoulli third centered moment is p(1-p)(1-2p), weighted by f_ell^3. Triples containing exactly two equal directions contribute zero by pairwise independence. A triple of three distinct quotient directions contributes zero when their vectors are linearly independent, while three distinct collinear directions have joint survival probability p^2 and centered triple contribution p^2(1-p), weighted by the product of their three fibre sizes. The exhaustive four-line classification counts their weighted ordered occurrences as C_pl. The conditional mean depends only on n,d,q,m, so averaging the conditional centered moment over any unconditional H-source introduces no extra term. This proves the formula. It is a finite symbolic moment theorem, **not** an efficient evaluation of X from public data.

## 4. Leading sparse asymptotic: null and planted third moments agree relatively

Let q be fixed, n->infinity, d/n->alpha with 0<alpha<1/2, c=n-d, and 1<=m=o(n). The just-merged [exact null result](F0-dual-bivector-null-third-central-moment.md) has

\[
\mu_{3,0}
=Tp(1-p)(1-2p)+[n\choose1]_q[n-1\choose2]_q
(q+1)q(q-1)p^2(1-p),\quad T=[n\choose2]_q.
\]

In this scaling, the family-IV contribution dominates the **planted** weighted collinear-triple count; the dominant null count is the full Grassmann flag count. Specifically,

\[
\frac{q^{3d}[c\choose1]_q[c-1\choose2]_q}
     {[n\choose1]_q[n-1\choose2]_q}
=1+O_q(q^{-c})
\]

and all other weighted planted line contributions are smaller than the family-IV contribution by O_q(q^{-(n-2d)}). The single-point diagonal terms are smaller than the leading line terms by O_q(q^{-n+m}). Hence

\[
\boxed{\frac{\mu_{3,\rm pl}}{\mu_{3,0}}
 =1+O_q(q^{-c}+q^{-(n-2d)}+q^{-n+m})
 =1+q^{-\Omega(n)}.}
\]

Both third moments are nonnegative, and positive for the stated n,d,m (which eventually satisfies c>=3). Along with the previously established exact null and planted **means and variances**, this supplies a third-moment-scale negative control for the fixed-q, d<c sparse source. It is **not** full-moment convergence, a TV bound, concentration, Gaussianity, a polynomial-time counter, a detector impossibility theorem or evidence for independent cryptographic hardness.

## 5. Independent small-field arithmetic checks (not repository benchmarks)

The exact theorem was checked by independent, exhaustive scratch enumeration of compatible alternating forms on small fixed-H spaces:

| q | n | d | m | Exact planted centered third moment |
|---|---|---|---|---|
| 2 | 4 | 2 | 1 | 144 |
| 2 | 4 | 2 | 2 | 249/4 |
| 2 | 5 | 2 | 1 | 1260 |
| 2 | 5 | 3 | 1 | 3360 |
| 3 | 4 | 2 | 1 | 2630 |

For example GF(2),n=5,d=2,m=1 involves 2^9=512 compatible forms and tests the nonempty family-IV contribution. GF(3),n=4,d=2,m=1 tests the rank-two affine family III, absent from weighted triples over GF(2). These are **scratch consistency checks** of an analytic identity, not code committed to the repository, measured original-verifier attack success, or new generated candidate evidence.

**Disposition:** EXACT PLANTED THIRD-MOMENT SOURCE CONTROL, **GLOBAL NO NOMINATION**, H-A/H-B/H-C HOLD. No N1-60 reservation. HEPMR BENCHMARK ONLY. Root README and stage registry unchanged.
