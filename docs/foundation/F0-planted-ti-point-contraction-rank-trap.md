# MORPH-F0: exact public point-contraction ranks and a false-seed trap

**2026-10-20. Full-public source-first mathematical negative control; GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.** This independently tests a natural proposed public polynomial seed extractor after the [randomized isotropic-flag attack](F0-planted-ti-randomized-flag-search.md). It is **not** an extractor or hardness proof, new assumption, benchmark, security claim, A-ID, F0-K or N1 stage. External planted-TI priority remains with Liu–Qiao–Tang–Zhang, [*The planted tensor problem over finite fields: algorithms and cryptography*](https://arxiv.org/abs/2609.31256) (2026).

## 1. Exact honest distribution and public contraction

Let `q` be any prime power, `V=F_q^n`, `2<=d<n`, `c=n-d`, `m>=1`. Draw a hidden `d`-plane `H` from **any prior**, independently of the tuple. Conditional on `H`, draw `m` independent **uniform alternating** forms `A_i` satisfying `A_i|_{H x H}=0`; no rank conditioning, rejection sampler, public-oracle restriction or source filtering. The attacker observes all coefficients. The *original* verifier accepts **any** `d`-plane `L` with `A_i|_{L x L}=0` for all `i`.

For any nonzero publicly chosen `v`, define the public `m`-by-`n` contraction matrix
\[
C_A(v)=\begin{bmatrix}A_1(v,-)\\ \vdots\\ A_m(v,-)\end{bmatrix},
\]
and its projectively well-defined rank `\rho_A([v])=\operatorname{rank} C_A(v)`. Every row annihilates `v`, so `\rho_A([v])<=\min(m,n-1)`. The proposed shortcut “pick a projective point of rank <m, extend it into a planted seed” is **not valid** in the hard sparse regime.

## 2. Exact two-population rank law (fixed points only)

**Theorem 1.** Fix any `H`, and a nonzero point `[v]`, chosen **independently** of the sampled forms. The conditional public contraction rank has exactly the rank law of a uniform rectangular random matrix as follows:

\[
\boxed{\begin{array}{ll}
v\in H:& \rho_A([v])\stackrel{d}{=}\operatorname{rank}\bigl(\mathrm{Unif}(F_q^{m\times c})\bigr),\\
v\notin H:& \rho_A([v])\stackrel{d}{=}\operatorname{rank}\bigl(\mathrm{Unif}(F_q^{m\times(n-1)})\bigr).
\end{array}}
\]

For `N=c` or `N=n-1`, the complete finite distribution is
\[
\boxed{
\Pr[\rho=k\mid N]
=q^{-mN}{N\brack k}_q\prod_{j=0}^{k-1}(q^m-q^j),
\quad 0\le k\le\min(m,N).
}
\]

**Proof.** First fix `H` and choose an adapted decomposition `V=H\oplus C`. A sampled alternating matrix has blocks `\begin{psmallmatrix}0&B\\-B^\top&D\end{psmallmatrix}`, where every `B` is uniform `d\times c`, every `D` is independent uniform alternating `c\times c`, and slices are independent. If `v\in H`, choose it as the first `H` basis vector; the contraction vanishes on `H` and its `c` remaining coefficients form one uniform row of `B`. If `v\notin H`, take `v` as the first complement basis vector: its pairing coefficients on `H` are a uniform column of `B`; those on a complement to `\langle v\rangle` inside `C` are an independent uniform row of `D`, giving exactly `n-1` independent uniform coordinates in the annihilator `v^\perp`. The map is surjective even in characteristic two. Each `A_i` is sampled independently. The displayed finite rank distribution counts rank-`k` matrices. The adapted coordinates exist only in this proof: the real attacker uses the public contraction. QED.

**Selection warning:** The law is for **fixed v independent of A**. Publicly selecting `v` from a radical or minimum-rank search is tensor-adaptive and must **not** be assigned this fixed-point probability.

## 3. Exact defect count and absence of hidden low-rank points

Assume `1<=m<=c` and define
\[
b_N(q,m)
=1-\prod_{j=0}^{m-1}(1-q^{j-N})
\]
for `m<=N`. This is the exact probability a uniform `m\times N` matrix lacks full row rank; it is **monotone decreasing** in `N`.

Let `Z_{\rm def}(A)` count **all public projective points** `[v]` with `\rho_A([v])<m`. By Theorem 1 and linearity of expectation, conditional on every `H`,

\[
\boxed{
\mathbb E_{\rm honest} Z_{\rm def}
={d\brack1}_q b_c(q,m)
+\bigl({n\brack1}_q-{d\brack1}_q\bigr)b_{n-1}(q,m).}
\]

Under `m` independent **null unrestricted** alternating forms, every fixed nonzero `v` has independent rows uniform on `v^\perp`, so

\[
\boxed{\mathbb E_{\rm null}Z_{\rm def}
={n\brack1}_q b_{n-1}(q,m).}
\]

The exact planted-minus-null expected count is `[d choose 1]_q(b_c-b_{n-1})>=0`. **This is a first moment only**, not a polynomial-time counting algorithm, a feasible distinguisher, concentration result or any-witness inverter.

For every fixed genuine `v\in H`, rank deficiency implies a nonzero left-kernel **line** of the public `m\times c` contraction. Union-bounding all left-kernel lines gives
\[
b_c(q,m)\le {m\brack1}_q q^{-c},
\]
and therefore, again conditional on every fixed `H`,
\[
\boxed{
\Pr_{\rm honest}[\exists\,0\ne v\in H:\rho_A([v])<m]
\le {d\brack1}_q{m\brack1}_q q^{-c}.
}
\]

In fixed-`q` sparse scaling `d/n\to\alpha\in(0,1/2)` and `m\asymp n/\log n`, the bound is `q^{-(1-2\alpha)n+o(n)}`, i.e. negligible. **With overwhelming probability every genuine seed point has rank exactly m.** The implication “low contraction rank reveals H” is therefore backwards: **every rank-deficient point is outside H** on that high-probability event.

## 4. An efficiently constructible, provably false deficient point when n is odd

For **odd `n`**, any alternating bilinear form has even matrix rank and hence a nonzero radical, over every finite characteristic, including two. Given the entire published tuple, Gaussian elimination on `A_1` finds a nonzero `v\in\ker A_1` in polynomial time. Its first contraction row vanishes, so `\rho_A([v])<m` for every `m>=1`.

Combine this **deterministic public construction** with the preceding high-probability absence theorem: whenever the latter event holds, *every* such public radical vector lies **outside H**. Thus, for odd `n` and sparse `d<c`, the proposal “get a seed by taking a deficient contraction point” has a concrete counterexample on virtually every honestly drawn public tuple.

This does **not** rule out all algorithms using detailed contraction data, nor does it claim that an `m`-full-rank contraction point is a genuine seed. Most outside points also have full rank for `m\ll n`, by Theorem 1. A public radical vector need not lie in any accepted `d`-plane, and it is not automatically a verified witness; the unchanged full verifier remains mandatory.

## 5. Independent exact binary scratch controls (not an attack corpus)

Fix `GF(2)`, `n=5`, `d=2`, `c=3`, `m=2`, and `H=\langle e_1,e_2\rangle`. One conditioned alternating slice has `2^{dc+\binom c2}=2^9=512` equally likely matrices. Exhaustively enumerating these `512` slices shows:

- For fixed `v=e_1\in H`, all `2^3` possible contraction rows occur **64 times** each.
- For fixed `v=e_3\notin H`, all `2^4` possible contraction rows occur **32 times** each.
- Over two independent slices, exact rank-defect probabilities are `b_3(2,2)=11/32` (true point) and `b_4(2,2)=23/128` (fixed outside point).
- Hence `\mathbb E_{\rm honest}Z_{\rm def}=3(11/32)+28(23/128)=97/16`, versus `\mathbb E_{\rm null}Z_{\rm def}=31(23/128)=713/128`. The exact shift is `63/128`.
- Independently enumerating all `2^{m d c}=4096` pairs of binary `2\times3` cross-block matrices shows **1092/4096=273/1024** have `\rho_A([v])=2` for *all three* true projective points, so the true-point union-bound result was **not claimed as exact** on this deliberately small instance.

All are finite exact scratch arithmetic, **not** committed executable code, measured attack trials, frozen sampler corpus or extrapolated numerical security levels.

## 6. Exact one-random-point **rank-only** observation TV

To avoid confusing an exceptional **tensor-adaptively selected** public radical with an informative **precommitted** test, draw a uniform public projective point `P=[v]` *independently* of both the planted/null form tuple and H. Publish only `(P,\rho_A(P))`, **not** all public matrices or complete contraction rows. Let `\mu_N` denote the explicit rank law in Theorem 1 for a uniform `m\times N` matrix.

**Theorem 2 (exact real-observation TV for every H prior).**
\[
\boxed{
\operatorname{TV}\bigl(\mathcal L_{\rm planted}(P,\rho_A(P)),
                         \mathcal L_{\rm null}(P,\rho_A(P))\bigr)
={ {d\brack1}_q\over {n\brack1}_q}
\,\operatorname{TV}(\mu_c,\mu_{n-1})
<q^{-c}.
}
\]
The inner distance is an exact finite sum `\frac12\sum_{k=0}^{\min(m,n-1)}|\mu_c(k)-\mu_{n-1}(k)|`, interpreting out-of-range ranks as zero.

**Proof.** Let `p_P=\Pr_H[P\subseteq H]` for the arbitrary hidden-H prior. Theorem 1, with no uniform-H assumption, gives `\mathcal L_{\rm planted}(\rho\mid P)=p_P\mu_c+(1-p_P)\mu_{n-1}` and `\mathcal L_{\rm null}(\rho\mid P)=\mu_{n-1}`. The same nonnegative scalar `p_P` multiplies their rank-law difference at each P. Therefore joint TV equals `(\sum_P p_P/{n\brack1}_q)\operatorname{TV}(\mu_c,\mu_{n-1})`. For every actual H, exactly `{d\brack1}_q` public projective points lie in H; averaging over any prior fixes the sum. Finally `{d\brack1}_q/{n\brack1}_q=(q^d-1)/(q^n-1)<q^{-c}`. QED.

For the binary scratch control of Section 5, `\mu_3=(1,21,42)/64` and `\mu_4=(1,45,210)/256` at ranks `0,1,2`; the inner TV is `21/128`, so the exact **joint rank-only** observation TV is `(3/31)(21/128)=63/3968`. This is a pencil-and-paper finite arithmetic consequence, not a measured distinguishing run.

**Scope:** the theorem covers a *single independent uniform point and its rank*. It does **not** bound total variation of the complete published tensor, multiple adaptive point queries, selection of an observable radical, full contraction vectors, or the accepted-witness search task.

### Uniform-H refinement: full single-point contraction leaks no more than its rank

For the **special case that H itself is uniform on Gr(d,V)**, suppose the local observation is enlarged from `(P,\rho_A(P))` to `(P,C_A(v))`, with a fixed deterministic representative `v\ne0` chosen for each independent uniform projective point `P`. Then

\[
\boxed{
\operatorname{TV}\bigl(\mathcal L_{\rm planted}(P,C_A(v)),
                         \mathcal L_{\rm null}(P,C_A(v))\bigr)
={ {d\brack1}_q\over {n\brack1}_q}
\,\operatorname{TV}(\mu_c,\mu_{n-1}).
}
\]

**Proof.** Fix `P=[v]` and write `N=n-1`. Conditional on `P\subseteq H`, the annihilator `W=H^\perp` is a **uniform c-plane** of `v^\perp\simeq F_q^N`. The observed ordered m-tuple `X=C_A(v)` is uniform on `W^m`. If its row-span dimension is `k`, its planted conditional probability divided by the unrestricted-null probability equals
\[
q^{m(N-c)}
\frac{{N-k\brack c-k}_q}{{N\brack c}_q},
\]
with the numerator interpreted as zero if `k>c`. This likelihood ratio depends **only** on the publicly computed row rank `k`, not on the orientation or other coefficients of `X`. Conditional on any fixed rank, the planted-inside and null row-tuple distributions therefore coincide. Their full-vector TV equals `\operatorname{TV}(\mu_c,\mu_N)`. Outside `H`, the point contraction is exactly null-distributed by Theorem 1. Under uniform `H`, the membership probability of any fixed `P` is `{d\brack1}_q/{n\brack1}_q`. Averaging gives the displayed exact joint TV. QED.

**Scope:** this enlarged-observation equality **requires uniform H**. For an arbitrary H prior, the preceding *rank-only* equality holds, but the orientation of full contraction rows can carry additional information. Neither result addresses the **entire public tensor** or a tensor-adaptively chosen point.

## 7. Disposition and falsification priority

- The rank-defect point selector is a **failed route to an authentic hidden seed** in the sparse regime. It is not an attack improvement, public inversion, or positive hard-distribution evidence.
- Its pointwise rank laws are **not valid after tensor-adaptive selection**. The stronger “no genuine deficient points” event is a uniform-over-all-H-points source theorem and **does** apply to every adaptively chosen public deficient point.
- A future public biased-greedy algorithm must demonstrate a substantive advantage at selecting *fully ranked* genuine prefixes and must pass the **original any-witness verifier**; it may not rely on hidden charts or promote single-point rank disparities to a polynomial recovery claim.
- No new N1 number (N1-60 remains unallocated), F0-K, A-ID, parameter set, code, KEM/PKE/OWF, independent Field-15 basis or status change.

**Disposition:** EXACT FIXED-POINT CONTRACTION RANK SOURCE LAW / PUBLIC RANK-DEFECT FALSE-SEED NEGATIVE CONTROL. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD; HEPMR BENCHMARK ONLY.
