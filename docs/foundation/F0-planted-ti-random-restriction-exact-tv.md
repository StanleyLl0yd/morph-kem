# MORPH-F0: exact TV bound for precommitted random subspace restrictions of planted TI forms

**2026-10-19. Narrow local-observation information-theoretic negative control.** GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD. This is **not** a full planted-vs-null tensor TV theorem, not an efficient public full-verifier inverse, not an independent cryptographic assumption, and not a KEM/OWF/PKE/trapdoor. It differs from the [all-r source moment counts](F0-isotropic-subspace-first-moment-hierarchy.md): the result is an actual exact conditional distribution and a quantitative TV bound for **one randomly preselected restricted observation**.

**External problem and priority:** Liu, Qiao, Tang and Zhang, *The planted tensor problem over finite fields: algorithms and cryptography*, [arXiv:2609.31256v1](https://arxiv.org/abs/2609.31256). Standard Gaussian-binomial intersection counting, not a claimed novel foundation, supplies the probability.

## 1. Unchanged full public source and deliberately narrower view

Let V=F_q^n for any prime power q>=2 (including characteristic two), 2<=d<n, c=n-d, and m>=1. Under null, publish m iid unrestricted uniform **alternating** bilinear forms A_i on V. Under planted, choose an honest d-plane H from **any specified unconditional H-prior**, then publish m independent uniform alternating forms satisfying A_i|_(H x H)=0. Every alternating matrix has zero diagonal in characteristic two. The actual full original any-witness verifier accepts a rank-d matrix Y iff Y^T A_i Y=0 for **every** public slice i.

**Narrow observation protocol:** independently of the public tensor and H, choose a uniformly random t-plane T<=V, 1<=t<=n, and reveal T together with the **complete restricted m-tuple** (A_i|_(T x T))_{i=1}^m. Any chosen public basis of T may encode each restriction as an alternating t-by-t matrix. This protocol is a mathematical projection of the existing public tuple, **not** replacement honest generation, sample selection, or a restricted success verifier. Choosing T adaptively based on the public A_i is expressly outside scope.

Write j=dim(T cap H), b_j=binom(j,2), and Alt(T) for all alternating forms on T (dimension binom(t,2)).

## 2. Exact conditional laws for every fixed H,T

**Lemma (extension of restricted alternating forms).** Conditional on any H,T with intersection dimension j, the null restriction A_i|_T is uniform on Alt(T), whereas the planted restriction is uniform on the codimension-b_j subspace

\[
\{B\in\operatorname{Alt}(T):B|_{(T\cap H)\times(T\cap H)}=0\}.
\]

These restrictions remain independent across i. **Proof.** Alternating forms on V are the dual of Lambda^2V, and the planted single-slice space is the annihilator of Lambda^2H. Restriction to T is the dual of the embedding Lambda^2T -> Lambda^2V followed by quotient modulo Lambda^2H. The elementary exterior-intersection identity

\[
\Lambda^2T\cap\Lambda^2H=\Lambda^2(T\cap H)
\]

shows that its image consists **exactly** of the forms annihilating Lambda^2(T cap H). A surjective linear map carries a uniform vector of its domain to uniform measure on its image. Repeat independently for all m forms. No assumption on how H was sampled is needed.

**Consequently**, conditional on each fixed H,T, the TV distance between the two **complete restricted m-tuple laws** is exactly

\[
\boxed{\operatorname{TV}(\mathcal L_{\rm pl}(A|_T\mid H,T),
\mathcal L_0(A|_T\mid H,T))=1-q^{-m\binom j2}.}
\]

Indeed the planted support is a linear subset having null probability q^{-m b_j}, and planted is null conditioned uniformly on that subset. For j=0 or 1, the **entire restricted tuple is identically distributed**, not merely its rank or expected isotropic count. This applies to arbitrary postprocessing of all m restricted matrices, even unbounded postprocessing.

## 3. Exact augmented-source TV and public-view upper bound

For fixed H and uniformly independent random T, classical Gaussian-binomial intersection counting gives

\[
\Pr(\dim(T\cap H)=j)
=\frac{[d\choose j]_q[c\choose t-j]_q
 q^{(d-j)(t-j)}}{[n\choose t]_q},
\]

with invalid indices contributing zero and max(0,t-c)<=j<=min(d,t). The distribution depends on the H-prior **only through its dimension**.

To upper-bound the actual public view, create an **analytical coupling** in which the null experiment also draws an independent auxiliary H from the same prior, and reveal this auxiliary H in **both** experiments. It is not included in the real observation. The joint (H,T,restricted tuple) TV can be computed **exactly** by averaging conditional TV:

\[
\boxed{
\Delta_{\rm aug}(n,d,t,m,q)=
\sum_j\frac{[d\choose j]_q[c\choose t-j]_q
q^{(d-j)(t-j)}}{[n\choose t]_q}
(1-q^{-m\binom j2}).
}
\]

For the actual observable restricted tuple, hiding H is a stochastic postprocessing step, hence by TV data processing

\[
\boxed{0\le\Delta_{\rm public}
=\operatorname{TV}(\mathcal L_{\rm pl}(T,A|_T),
                  \mathcal L_0(T,A|_T))
\le\Delta_{\rm aug}\le\Pr(j\ge2).}
\]

The first inequality may be strict: mixture over unknown H can reduce distinguishability. **Never state that the displayed augmented TV is automatically the full public-view TV or the original full-tensor TV.**

## 4. Exponentially quiet range for a random preselected view

For t>=2, a union bound over all 2-planes L<=H gives

\[
\Pr(j\ge2)\le
[d\choose2]_q\,\frac{[t\choose2]_q}{[n\choose2]_q}.
\]

A fixed 2-plane L belongs to a uniform t-plane with probability [t choose2]_q/[n choose2]_q. If t<=c=n-d, standard finite-field Gaussian-binomial inequalities

\[
[a\choose2]_q
\le\frac{q^{2(a-2)}}{(1-q^{-1})(1-q^{-2})},
\qquad
[n\choose2]_q\ge q^{2(n-2)}
\]

give the simple universal estimate (terms with t<2 vanish)

\[
\boxed{
\Delta_{\rm public}\le\Delta_{\rm aug}
\le \frac{4}{9}\,q^{-2(c-t)}
\quad\text{when }t\le c,\ q\ge2.
}
\]

The factor 4/9 is a **loose** upper constant, from the worst case q=2 in q^-4/((1-q^-1)^2(1-q^-2)^2). For t<=c-s it yields a <=(4/9)q^(-2s) bound **independent of m**. In the external d~n/C, C>=3 sparse regime, a random t-plane with t<=c-epsilon*n has exponentially small total-variation signal **even if the observer gets the entire tuple of restricted alternating matrices and computes on it arbitrarily**.

This makes no assertion for random t close above c, adaptive t-planes, jointly dependent multiple probes, or the original published full n-dimensional tensor. In particular the full public data may contain a rare but distinguishable dimension-d isotropic witness even when these random local views are statistically quiet.

## 5. Exact t=2 public-view TV and a feasible but exponentially weak local test

The public upper bound is **tight as an identity** when t=2, for **every unconditional H-prior**, because T cap H has dimension at least two iff T<=H. Conditional on any given public T, the planted m-dimensional evaluation vector (A_i(v,w))_i, for a chosen basis (v,w) of T, is the mixture of

- a point mass at zero, with mixing weight Pr_H(T<=H), and
- the same uniform F_q^m law as null, with the remaining weight.

Averaging the conditional TV over uniform T gives the **exact public-view formula**

\[
\boxed{
\Delta_{\rm public}(t=2)=
\left(1-q^{-m}\right)\frac{[d\choose2]_q}{[n\choose2]_q}.
}
\]

The elementary public polynomial-time local test **“are all m values on this randomly selected 2-plane zero?”** achieves this TV for the single-view experiment; its advantage is exactly the displayed value. In the sparse d<c high-codimension regime that advantage is exponentially small. This is an **explicit observation protocol**, not an efficient detector on the original full tensor with meaningful non-negligible advantage, and not evidence of computational hardness.

For example q=2,n=4,d=2,m=2 gives exactly (1-1/4)/[4 choose2]_2=3/140. The formula is elementary and does not imply success amplification for many potentially dependent queries.

## 6. Decision and scope

The distinguishing statement is information-theoretic and applies to all postprocessing of **one random precommitted T** independent of the forms; it is not an analysis of an adversary selecting T from public tensor invariants, Plücker kernels, minimum rank or recovered witnesses. Local weak signal cannot certify original full-data hardness: the original tensor is available in full to a genuine attacker, and the relation accepts **any** common totally-isotropic d-space. The result is a narrow attack-first statistical null control and is already within classical finite-field linear/subspace geometry, not a positive independent MORPH-R0 Field-15 proposal.

**Disposition: EXACT RESTRICTED-VIEW TV / ANALYTIC NEGATIVE CONTROL ONLY. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.** N1-60 unallocated. HEPMR BENCHMARK ONLY. No code, generated datasets, root README or stage-registry edits.
