# MORPH-F0: exact joint completion of genuine seeds and no-slack public flag attack

**2026-10-20. Full-public, source-first, constructive attack strengthening; GLOBAL NO NOMINATION, H-A/H-B/H-C HOLD.** The result sharpens the [fixed-seed full-tensor completion theorem](F0-planted-ti-public-seed-completion.md), [exhaustive isotropic-flag work bound](F0-planted-ti-isotropic-flag-search.md), [classical randomized greedy flags](F0-planted-ti-randomized-flag-search.md), and [quantum amplitude amplification](F0-planted-ti-quantum-greedy-flags.md). It **does not** give polynomial public seed extraction, a new hard mathematical assumption, a security parameter, an executable attack or Field-15 novelty.

**External priority:** the planted totally-isotropic tensor relation and a generic `q^{O(n\log n)}` classical attack are due to Liu, Qiao, Tang and Zhang, [*The planted tensor problem over finite fields: algorithms and cryptography*](https://arxiv.org/abs/2609.31256) (2026). The mathematics below is scoped to an exact conditional-uniform source law and original verifier; no competing algorithm priority or new complexity-class claim is made.

## 1. Original source, original successful witness

Let `V=F_q^n`, `2<=d<n`, `c=n-d`, `m>=1`, and `1<=t<=d`, over any finite prime-power field. Sample a hidden d-plane H from **any prior independently** of the forms. Conditional on H, the complete public tuple comprises m independent **uniform alternating** bilinear forms `A_i` annihilating `H x H`, with no rank conditioning, special acceptance filter or restricted oracle.

The unchanged public verifier accepts **any** d-plane L with `A_i|_{L x L}=0` for all i. Finding the sampled H is merely one sufficient route to passing that verifier.

For each true t-plane `T\subseteq H`, compute its fully **public** simultaneous orthogonal space
\[
S_A(T)=\{v\in V:A_i(u,v)=0\;\forall u\in T,\ 1\le i\le m\}.
\]
Call T *completing* if `S_A(T)=H`. This is equivalent to full column rank c of the `mt\times c` cross-pairing matrix `M_T` in an H-adapted **proof-only** quotient chart. The algorithm itself never receives that chart or tests hidden membership.

Assume `mt>=c`, and set
\[
L_t={d\brack t}_q,\qquad
p=p_{m,t,c}=\prod_{j=0}^{c-1}(1-q^{j-mt})\ge C_q^{-1}>0,\qquad
C_q=\prod_{j\ge1}(1-q^{-j})^{-1}<4.
\]
Let `X_t(A,H)` count all **genuine** t-planes `T\subseteq H` satisfying `S_A(T)=H`. This is an **analytical hidden-source count**, not a publicly computable statistic or a hidden-H oracle supplied to an attacker.

## 2. Exact two-seed law by intersection rank

Fix two distinct or coinciding true t-planes `T,T'\subseteq H`, **independently of the sampled forms**, and let `j=\dim(T\cap T')`. Put
\[
\pi_{a,b}(r)=q^{-ab}{b\brack r}_q\prod_{\ell=0}^{r-1}(q^a-q^\ell),
\]
the exact finite rank-r law of a uniform `a\times b` matrix, and
\[
f_{a,b}=\begin{cases}
\prod_{\ell=0}^{b-1}(1-q^{\ell-a}),&a\ge b,\\
0,&a<b,
\end{cases}
\quad f_{a,0}=1.
\]

**Theorem 1 (exact joint completion, every H prior).**
\[
\boxed{
\Pr[S_A(T)=H\ \land\ S_A(T')=H\mid H,T,T']
=p_j:=\sum_{r=0}^{\min(mj,c)}
\pi_{mj,c}(r)\; f_{m(t-j),c-r}^{\,2}.}
\]
Moreover,
\[
\boxed{p_j-p^2
=\operatorname{Var}_{R\sim\pi_{mj,c}}
\left[f_{m(t-j),c-R}\right]\ge0.}
\]
Thus **disjoint** true seeds (j=0) have independent completion events `p_0=p^2`, even though all forms are globally shared; coinciding seeds (j=t) have `p_t=p`.

**Proof.** In the hidden chart choose a basis beginning with j coordinates spanning `T\cap T'`, then t-j additional coordinates for each of T and T'. Conditional-uniform cross-block rows are independent for these linearly independent basis coordinates. The two `mt\times c` completion matrices share exactly the `mj\times c` uniform rows associated with the intersection, and their other `m(t-j)` rows are mutually independent uniform rows. Conditional on rank R=r of the shared block, each set of new rows must span a remaining quotient of dimension c-r; the two independent success probabilities are both `f_{m(t-j),c-r}`. Average their product over the exact shared-rank law. Marginally, completing either fixed t-plane has probability `p=\mathbb E_R[f_{m(t-j),c-R}]`. Subtracting `p^2` gives the variance identity. Characteristic two and all other finite characteristics are covered. QED.

## 3. Exact second moment and sharp source concentration

For a fixed true t-plane T, the number of true t-planes T' with intersection dimension j is exactly
\[
\boxed{
M_j={t\brack j}_q{d-t\brack t-j}_q\,q^{(t-j)^2},
\qquad \max(0,2t-d)\le j\le t.
}
\]
Consequently

**Theorem 2 (finite conditional second moment, every H prior).**
\[
\boxed{
\mathbb E[X_t\mid H]=L_t p,\qquad
\mathbb E[X_t^2\mid H]=L_t\sum_j M_jp_j,\qquad
\operatorname{Var}(X_t\mid H)=L_t\sum_j M_j(p_j-p^2).}
\]

**Proof.** Expand `X_t=\sum_{T\in Gr(t,H)}1_{\{S_A(T)=H\}}`. The mean is the fixed-seed probability summed over all L_t true planes. For the second moment, first choose T (L_t choices), then choose T' by its dimension-j intersection. Count the latter using the intersection `T\cap T'`, the quotient image in H/T, and the graph map of dimension `(t-j)^2`; multiply by the exact joint probability from Theorem 1. All formulas hold conditional on **each** H, hence under every H prior. No independence outside j=0 is assumed. QED.

Let
\[
\gamma=\min\left(1,\frac{{t\brack1}_q^2}{{d\brack1}_q}\right).
\]
For two independent uniform t-planes in H, a union bound over projective lines in the first plane gives
\[
\Pr[T\cap T'\ne0]\le\gamma.
\]
Since `0\le f_{m(t-j),c-R}\le1` has mean p, its variance is at most `p(1-p)`; moreover the covariance vanishes at j=0. Therefore
\[
\boxed{
\frac{\operatorname{Var}(X_t\mid H)}{(L_t p)^2}
\le\frac{1-p}{p}\,\gamma,\qquad
\Pr\left[\left|\frac{X_t}{L_t p}-1\right|\ge\varepsilon\mid H\right]
\le\frac{1-p}{p\varepsilon^2}\,\gamma.
}
\]
These are bounds under the original **unfiltered source**, with no independence assumption between intersecting seeds.

For fixed q, `d=\Theta(n)`, `t=O(\log n)`, and `mt>=c`, `p>=C_q^{-1}` and
\[
\gamma\le q^{-d+2t+O_q(1)}=q^{-\Omega(n)}.
\]
Thus **the fraction of genuine t-seeds completing to H concentrates exponentially strongly** even at the exact threshold `mt=c`. In particular, the prior exhaustive public all-t-plane completion algorithm (which enumerates every T without knowing H and runs the original verifier) now has unconditional honest-source success at least
\[
\boxed{
1-\min\left(1,\frac{1-p}{p}\gamma\right)
}
\]
because `X_t=0` implies a relative deficit of at least 1. **No artificial positive completion slack `mt-c` is necessary for overwhelming honest-source success** in the stated sparse asymptotics. Its work is still bounded by `poly*[n choose t]_q`, not polynomial.

## 4. Strengthened actual randomized public-flag search, with no terminal slack

The public greedy algorithm of the [previous theorem](F0-planted-ti-randomized-flag-search.md) chooses **one** uniform quotient vector at each step, **aborts on zero**, and returns a completed public d-plane only if the **entire original verifier** accepts. It never tests membership in H.

Fix `r>=0` and define
\[
E_t=\sum_{k=0}^{t-1}(c-mk)_+,\quad
\delta=t\,C_q q^{-(r+1)^2}.
\]
For a **precommitted true complete t-flag**, the uniform prefix rank-tail lemma bounds the probability that *some* prefix k<t has rank below `min(mk,c)-r` by `\delta`. Let `B_{\rm prefix}(A,H)` be the fraction of all true complete flags that violate this prefix condition. The original uniform source and Markov's inequality give
\[
\Pr[B_{\rm prefix}>\sqrt\delta\mid H]\le\sqrt\delta.
\]
Each true terminal t-plane has precisely `F_t(q)=\prod_{i=1}^t{i\brack1}_q` complete true flags inside it. The **fraction** of true complete flags whose terminal seed completes to H is therefore exactly `X_t/L_t`; it is at least `p/2` except with probability at most `4(1-p)\gamma/p` by Theorem 2.

**Theorem 3 (finite no-slack any-witness attack).** Suppose `mt>=c`, `0<\delta<1`, and `\sqrt\delta\le p/4`. On a source event of probability at least
\[
\boxed{
1-\sqrt\delta-\frac{4(1-p)}{p}\gamma
}
\]
every fixed public tensor A has one-trial (fresh public random coins) probability of returning a **fully verified accepted d-plane** at least
\[
\boxed{\frac p4 q^{-E_t-(r+1)t}.}
\]
Hence for any `0<\eta<1`, running the same publicly evaluable trial on the same public A at most
\[
\boxed{
R=\left\lceil\frac4p q^{E_t+(r+1)t}\ln(1/\eta)\right\rceil
}
\]
times yields honest-source success at least
\[
\boxed{
1-\sqrt\delta-\frac{4(1-p)}p\gamma-\eta
}
\]
(clipped below by zero), using at most `poly(n,m,t,\log q)*R` field operations. **This includes exact terminal equality `mt=c` and uses the original full any-witness verifier**.

**Proof.** Intersect the prefix-good event with the terminal fraction event. At least `p/2-\sqrt\delta\ge p/4` of all true complete flags have both good prefixes and a full-rank terminal completion. The exact public path-probability counting in the [previous greedy-flag theorem](F0-planted-ti-randomized-flag-search.md) gives per-trial acceptance probability at least `G(A,H)q^{-E_t-(r+1)t}` for any good-flag fraction G, regardless of adaptivity. All such paths end at H and pass the original verifier. Repeating independent coins on the same public A yields conditional failure at most `e^{-R(p/4)q^{-E_t-(r+1)t}}\le\eta`. Union-bound the two source-bad events. QED.

For fixed q, `d/n\to\alpha\in(0,1/2)`, `m\asymp n/\log n`, choose **the minimal** `t=\lceil c/m\rceil=\Theta(\log n)` and `r=\lceil\sqrt{3\log_q n}\rceil`. Eventually `t<=d`, `\delta=o(1)`, `\sqrt\delta\le p/4`, `\gamma=q^{-\Omega(n)}`; the above no-slack attack succeeds with probability `1-o(1)` using work with leading upper q-exponent
\[
\boxed{\log_q W_{\rm classical}
\le c^2/(2m)+o(n^2/m).}
\]
This retains the earlier **known generic q^{O(n\log n)} class** and does **not** produce polynomial inversion.

For `q=2^e`, the same **per-public-tensor source-good bound** may be used with the standard reversible greedy-trial circuit and Yoder–Low–Chuang fixed-point amplitude amplification, requiring `O(poly*q^{(E_t+(r+1)t)/2}\log(1/\eta))` quantum work up to p-dependent constants. Thus the previously derived leading **quantum upper** exponent `c^2/(4m)` also holds with no positive completion slack. **This is a standard quantum square-root acceleration**, not a quantum-hardness result or a new quantum algorithm.

## 5. Independent GF(2) exact controls (scratch only)

**Nontrivial intersecting t-planes:** take `q=2,d=3,c=2,m=1,t=2`. Then `L_t=[3 choose2]_2=7`, `p=3/8`; distinct true 2-planes intersect in a line, `j=1`, and the joint completion law gives `p_1=3/16` (different from `p^2=9/64`). Thus
\[
\boxed{\mathbb E X_t=21/8,\qquad \operatorname{Var}X_t=231/64.}
\]
Independently exhaust all `2^{dc}=64` binary 3-by-2 cross-blocks. Exactly **22** blocks have `X_t=0` and **42** have `X_t=4`, yielding precisely these two rational moments. Complement alternating blocks only multiply each cross-block's occurrence uniformly and do not change the conditional law.

**Disjoint one-dimensional seeds:** take `q=2,d=2,c=2,m=2,t=1`. Then `L_t=3`, `p=3/8`, and distinct true projective points have **independent** completions. Hence `EX_t=9/8` and `\operatorname{Var}X_t=45/64`. All `2^{mdc}=256` ordered binary 2-by-2 cross-block pairs have exact histogram `X=0,1,2,3` with counts `64,108,72,12`, matching those moments. These three indicator events are **not asserted mutually independent**.

**Both disjoint and intersecting 2-plane pairs:** take `q=2,d=4,c=2,m=1,t=2`. Here `L_t=[4 choose2]_2=35`, `p=3/8`; for a fixed T, there are exactly `M_0=16` disjoint T', `M_1=18` meeting T in a line, and `M_2=1` identical T. The joint probabilities are `p_0=9/64`, `p_1=3/16`, `p_2=3/8`, giving `EX_t=105/8` and `Var X_t=2415/64`. Independently enumerating all `2^(dc)=256` binary 4-by-2 cross-blocks yields exactly **46** with `X_t=0` and **210** with `X_t=16`; both rational moments agree. This third control directly exercises **all three intersection classes**, not just the marginal or intersecting-pair specialization.

These are independent finite arithmetic controls, **not** a committed attack executable, generated source dataset, measured runtime, CI evidence or cryptographic parameter validation.

## 6. Scope and falsification priority

- The source moment and concentration results concern **true hidden-H seeds**, not a polynomial public test that identifies them. The real algorithms enumerate or randomly construct public flags and use only the **unchanged original full verifier**.
- A source-average success probability is never assumed to hold for an **adaptively tensor-selected single seed**; the no-slack randomized and quantum claims instead derive an explicit **per-public-tensor good event**.
- No terminal completion slack improves the finite attack guarantee and selection of t, **not** the established leading classical/quantum work exponents or independent algorithmic priority.
- A genuinely new attack would bias public flag extension probabilities toward true hidden structure by polynomial-time use of the **complete** tensor, rather than counting hidden seeds. No such polynomial extractor is provided.
- No N1-60 reservation, F0-K/A-ID, source benchmark, implementation, KEM/PKE/OWF, positive Field 15, security claim, README expansion or stage-registry change.

**Disposition:** EXACT GENUINE-SEED JOINT SOURCE LAW / SECOND MOMENT / NO-TERMINAL-SLACK PUBLIC GREEDY-FLAG ATTACK. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD; HEPMR BENCHMARK ONLY; N1-60 free.
