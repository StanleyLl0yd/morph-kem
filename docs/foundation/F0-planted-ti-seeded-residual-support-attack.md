# MORPH-F0: shorter public seeds through residual support-intersection inversion

**2026-10-20. Constructive full-public-tensor attack-first refinement; GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.** This combines the established [public simultaneous-orthogonal seeded completion](F0-planted-ti-public-seed-completion.md) with the [polynomial public multi-slice image-support intersection attack](F0-adaptive-multislice-support-intersection.md) on the **residual quotient** of a genuine short seed. The proof derives the exact conditional residual planted law and a rigorous **unseeded, original-any-witness public algorithm**, then a source-good randomized greedy-flag/standard-quantum amplification bound. It does **not** establish polynomial inversion in the sparse `d<c` source or a new Field-15 hard mathematical foundation.

**Priority.** The planted totally-isotropic (TI) source and a generic `q^{O(n log n)}` algorithm already appear in Liu, Qiao, Tang and Zhang, [*The planted tensor problem over finite fields: algorithms and cryptography*](https://arxiv.org/abs/2609.31256) (2026). The present *specific conditional quotient and sufficient-work exponent* are documented for reproducibility; **no claim of priority or improvement over all versions of the existing generic method** is made without a literature-level algorithm comparison. Both ingredients are previously documented MORPH-F0 elementary attacks.

## 1. Full original source, verifier, and public shortened-seed procedure

Let `q` be any prime power, `V=F_q^n`, `2<=d<n`, `c=n-d`, `m>=2`. Draw hidden d-plane H from **any prior independently of the forms**, then publish all coefficients of m independent **uniform alternating** forms A_i satisfying `A_i|_{H x H}=0`. No rejection of tensors, rank conditioning, oracle restriction, secret-dependent sample filter or secondary verifier is permitted.

The original accepted set is
\[
\mathcal E(A)=\{L\in\operatorname{Gr}(d,V):
  A_i|_{L\times L}=0\ \forall i\}.
\]
**Any L in E(A) wins**, whether or not it equals H.

For any public t-plane T, first check `T\subseteq S_A(T)`, where
\[
S_A(T)=\{v\in V:A_i(u,v)=0\text{ for all }u\in T,\ i=1,\ldots,m\}.
\]
If T is not simultaneously isotropic, reject it. Put `\ell_0=c-mt` and suppose `1<=t<=d`, `0<mt<c`, `0<\ell_0<d-t`. **Public deterministic completion from a supplied seed T:**

1. Construct `S=S_A(T)` by Gaussian elimination. Reject unless `\dim S=d+\ell_0`, which is a completely public rank check; verify `T\subseteq S`.
2. Construct the public quotient `W=S/T`, of dimension `u+\ell_0` with `u=d-t`. Each A_i descends to a well-defined alternating form `\bar A_i` on W because `A_i(T,S)=0`. **All m original slices** are carried to the quotient.
3. Compute public covector images `\operatorname{im}(\bar A_i:W\to W^*)`. Keep those of public rank `2\ell_0`; intersect their images, using all of W* when there are none. If the public intersection has dimension `\ell_0`, take its annihilator `\bar L\subset W` of dimension u. Otherwise reject T.
4. Lift `\bar L` back to a d-plane `L\subseteq S` containing T and run the **entire original verifier on L against every A_i**. Return L **only if it passes**; otherwise reject T.

Every step is polynomial in n,m,log q, on **every input**. On an arbitrary incorrect seed it may fail or occasionally find another accepted L; it never declares success without the original full verifier.

## 2. Exact residual conditional-uniform source theorem

Fix H and a t-plane `T\subseteq H` **independently of the form draws**, only for the conditional source proof. Write `V=H\oplus C`, `\dim C=c`, and select a basis H=T⊕H_0, `\dim H_0=u=d-t`. In each slice the cross-block `B_i\in F_q^{d\times c}` splits into `t` rows `B_i^T` from T and `u` rows `B_i^0` from H_0. All these rows, and the complementary alternating blocks `D_i`, are independent and uniform.

Stack the `B_i^T` into an `mt\times c` uniform matrix `M_T`. Suppose the **publicly checkable full-row-rank event**
\[
R_T=[\operatorname{rank} M_T=mt]
\]
occurs. Let `K=\ker M_T\subseteq C`, `\dim K=\ell_0=c-mt`. Then
\[
\boxed{S_A(T)=H\oplus K,\qquad S_A(T)/T\cong H_0\oplus K.}
\]

**Theorem 1 (exact residual conditional source; no hidden access for the algorithm).** Conditional on the entire tensor block `M_T` satisfying `R_T`, and hence on K, the induced tuple `(\bar A_i)` on `S_A(T)/T` is exactly m **independent uniform alternating forms annihilating `H_0\times H_0`**, with ambient dimension `u+\ell_0`, planted dimension `u`, and codimension `\ell_0`. No source postselection is performed by the honest generator; the event is used **only to calculate the attack's unconditional success**, and the actual public algorithm checks its dimension.

**Proof.** For any `h\in H` and `k\in K`, pairings with T vanish by construction of K. Thus T lies in the common radical of all restrictions A_i|_(S×S), so these restrictions descend to W. In the proof-only decomposition `H_0\oplus K`, the induced H_0×H_0 block vanishes. The `H_0\times K` cross block is `B_i^0|_K`: each `B_i^0` is independent uniform and independent of every `B_j^T`, so its restriction to the **fixed conditional K** is independent uniform on `F_q^{u\times\ell_0}`. Likewise the K×K alternating block is `D_i|_K`, independent uniform because restriction of alternating forms to K is a surjective linear map and each D_i is independent of all B blocks. Independence remains across all m slices. This is precisely the earlier multi-slice support-inversion honest law with `d'=u>c'=\ell_0`, without a secret-dependent input given to the public algorithm. QED.

The conditioned residual theorem applies **only** to precommitted genuine seeds T; assigning it automatically to the attacker-selected tensor-adaptive T would be invalid. The exhaustive and greedy attack proofs below avoid that error by fixing a hidden true seed or averaging over **all precommitted true flags** in the analysis.

## 3. Exact true-seed success probability and explicit tail

The probability that M_T has full row rank is
\[
\boxed{
p_{\rm row}=\prod_{j=0}^{mt-1}(1-q^{j-c}),\qquad
1-p_{\rm row}<\frac{q^{-\ell_0}}{q-1}.}
\]

Conditional on this event, invoke the previously proved [exact multi-slice support-intersection inversion formula](F0-adaptive-multislice-support-intersection.md) with `d'=u,c'=\ell_0`. Put
\[
p_B=\prod_{j=0}^{\ell_0-1}(1-q^{j-u}),\quad
a_j=\begin{cases}
{u-j\brack \ell_0-j}_q/{u\brack\ell_0}_q,&0\le j\le\ell_0,\\
0,&j>\ell_0,
\end{cases}\quad
\theta_j=1-p_B+p_B a_j.
\]
The exact conditional residual-inversion success is
\[
\boxed{
p_{\rm supp}=\sum_{j=0}^{u}(-1)^j q^{\binom j2}
  {u\brack j}_q\,\theta_j^m.}
\]

**Theorem 2 (exact fixed true-seed accepted-witness probability).** For every precommitted genuine `T\subseteq H`, the public seeded procedure of §1 outputs **the original sampled H** on the **unfiltered complete public tuple** with probability exactly
\[
\boxed{p_{\rm seed}=p_{\rm row}\,p_{\rm supp}.}
\]
Every reported output, also for incorrect public seeds, is certified by the entire original verifier.

**Proof.** On the honest law, the procedure first requires the full-row event R_T; it rejects if rank drops below mt. By Theorem 1, conditional on R_T and M_T, the public quotient is distributed exactly as the independent planted uniform-source input of the previously proved support attack. Its public certificate succeeds if and only if its selected eligible image supports have intersection dimension `\ell_0`; when it succeeds it reconstructs H_0, lifts to H and passes every original slice. The exact conditional probability is p_supp, independent of M_T subject to full-row rank. Multiply by p_row. QED.

Write `h=u-\ell_0=(m-1)t-(c-d)>0`. Then
\[
1-p_B<\frac{q^{-h}}{q-1},
\qquad a_1=\frac{q^{\ell_0}-1}{q^u-1}<q^{-h},
\qquad
\theta_1<\frac{q}{q-1}q^{-h}\le q^{1-h}.
\]
The prior union bound on a nonzero survivor in the intersection gives
\[
\boxed{
1-p_{\rm supp}\le
{u\brack1}_q\,\theta_1^m
\le {u\brack1}_q\,q^{-m(h-1)}.
}
\]
Thus
\[
\boxed{
p_{\rm seed}
\ge1-\frac{q^{-\ell_0}}{q-1}
-{u\brack1}_q q^{-m(h-1)},
}
\]
clipped below at zero if the RHS is negative. These are unconditional-source *attack probabilities*, not security estimates.

### Rank-deficiency-tolerant public completion: exact finite mixture

The full-row branch above is an intentionally simple certificate, **not a necessary condition for residual inversion**. A stronger variant uses the observed public dimension of `S_A(T)` to **adapt to every rank** of the seed contraction, while still rejecting and reporting nothing unless the original full verifier accepts.

Given any public isotropic t-plane T, compute `S=S_A(T)` and let `\ell=\dim S-d` and `u=d-t`. If `\ell<0` or `\ell\ge u`, reject this seed. If `\ell=0`, then verify and return S itself (when it is a d-plane). If `0<\ell<u`, descend all m original public forms to `W=S/T`, use the **same public eligible-image support-intersection solver** with observed codimension `\ell`, lift the recovered u-plane and verify all the original forms. This algorithm is polynomial for a supplied public T, with no hidden-H membership oracle and no precondition requiring `mt` independent seed rows.

**Theorem (exact conditional rank-defect tolerance).** Fix H and a genuine t-plane `T\subseteq H` before drawing the original honest tensor. For **every fixed value of the full public T-cross block** `M_T`, whether full-row rank or deficient, let `r=\operatorname{rank} M_T`, `K=\ker M_T`, and `\ell=c-r`. Then
\[
\boxed{S_A(T)=H\oplus K,\quad
S_A(T)/T\simeq (H/T)\oplus K}
\]
and the residual m alternating forms are still **independent uniform conditioned-planted forms on that quotient**, with planted dimension `u=d-t` and codimension `\ell=c-r`.

**Proof.** The proof of Theorem 1 never uses *surjectivity* of M_T to establish independence: all unused H/T×C rows of B_i and all alternating C×C blocks D_i are independent of the **entire value** of M_T. Restricting these unused uniform blocks to `K=\ker M_T`, for any K including those arising from deficient M_T, produces independent uniform H/T×K and Alt(K) coefficients by surjectivity of these linear restriction maps. All forms vanish on T×S by the definition of S, so the quotient law holds. The **only reason** §1 used full row rank was to set the predetermined residual codimension `c-mt`; the public observable dimension instead supplies the actual `c-r`. QED.

Let `\pi_{a,b}(r)` be the exact rank-r mass of a uniform a×b matrix from the [fixed-seed theorem](F0-planted-ti-public-seed-completion.md), and `p_{\rm supp}(u,\ell,m)` the earlier exact residual Gaussian Möbius success probability, with convention `p_{\rm supp}(u,0,m)=1` and `p_{\rm supp}(u,\ell,m)=0` if `\ell\ge u`. For the stronger publicly rank-adaptive variant its **exact precommitted true-seed probability** on the unfiltered honest source is
\[
\boxed{
p_{\rm mix}=\sum_{r=0}^{\min(mt,c)}
 \pi_{mt,c}(r)\,p_{\rm supp}(d-t,c-r,m).
}
\]
The events of different r are disjoint and the conditional residual law above supplies the exact conditional success. In the original §1 range `mt<c`, the original full-row-only probability `p_{\rm seed}=p_{\rm row}p_{\rm supp}(d-t,c-mt,m)` is one **nonnegative summand** in this formula, so `p_{\rm mix}\ge p_{\rm seed}`. Exhaustive public enumeration and greedy public-flag search remain genuine original-verifier algorithms when the new variant replaces the terminal procedure. Their **existing** source-success lower bounds and leading upper work exponents remain valid by monotonicity, without any postselected-seed assumption.

**Independent finite rank-mixture scratch check (GF(2)):** let `n=8,d=4,c=4,m=3,t=1`, so `u=3`. The rank-3 3×4 cross block occurs with probability `315/512`; its residual codimension 1 has `p_{\rm supp}(3,1,3)=231/256`, so the older gated probability is `72765/131072`. Deficient rank-2 occurs with probability `735/2048`, leaves `\ell=2<u=3` and has exact support-inversion probability `p_{\rm supp}(3,2,3)=567/4096`, verified independently by enumerating all `64^3=262144` ordered 2×3 binary cross-row triples: precisely **36288** pass the support-intersection criterion. (For `\ell=1`, exactly **462/512** ordered three 1×3 row triples pass.) Lower ranks give `\ell\ge u` and the variant rejects. Therefore
\[
\boxed{
p_{\rm mix}={5073705\over8388608}
={72765\over131072}+{416745\over8388608}
>{72765\over131072}.
}
\]
This is a finite scratch **conditional true-seed** validation, not a test of the unseeded public attack, a source dataset, committed executable, runtime benchmark or evidence of a new hard primitive.

## 4. Actual unseeded exhaustive public attack

**Algorithm:** Enumerate **all public t-planes** T canonically, run the §1 residual support procedure on each, and return the first candidate passing the *entire original verifier*. No hidden-membership test or private chart is used.

**Theorem 3 (honest-source unseeded success and work).** For `0<mt<c` and `0<\ell_0<d-t`, the deterministic all-public-seed procedure returns **some verifier-accepted d-plane** on the original unfiltered honest distribution with probability **at least** p_seed, for **every H prior**, using at most
\[
\boxed{\operatorname{poly}(n,m,t,\log q)\,{n\brack t}_q
\le\operatorname{poly}\,C_q q^{t(n-t)}}
\]
field operations (for `C_q=\prod_{j\ge1}(1-q^{-j})^{-1}<4`).

**Proof.** For each H, select a fixed t-plane `T_*(H)\subseteq H` using a rule depending only on H, not the sampled forms. That true seed appears in the **public enumeration**, although the algorithm has no idea which enumerated T it is. Its seeded public residual procedure recovers H with exact conditional probability p_seed. The real algorithm may succeed on other seeds earlier, so its success is at least that probability. All per-seed operations are polynomial and every accepted output passes the original verifier. QED.

## 5. Source-good public randomized greedy flags and standard quantum amplification

Use the **same actual one-shot zero-abort public greedy flag** algorithm from [PR #245](F0-planted-ti-randomized-flag-search.md), but replace its terminal direct kernel-equals-d acceptance step by the **public residual quotient support procedure** of §1. Every terminal output is still tested with the full original verifier. A single flag trial costs polynomially many field operations.

Fix an integer `r>=0` and put
\[
E_t=\sum_{k=0}^{t-1}(c-mk)_+
=ct-\frac{mt(t-1)}2
\quad(mt<c).
\]
For a precommitted genuine complete flag `0=T_0<\cdots<T_t\subset H`, the earlier independent prefix-rank union bound implies probability at most
\[
\delta_{\rm prefix}=t C_q q^{-(r+1)^2}
\]
that some prefix k<t has rank below mk−r. Theorem 2 gives a terminal *true-seed* failure at most
\[
\delta_{\rm end}=
\frac{q^{-\ell_0}}{q-1}
+{u\brack1}_q q^{-m(h-1)}.
\]
Set `\delta=\delta_{\rm prefix}+\delta_{\rm end}`.

**Theorem 4 (actual randomized public any-witness attack).** If `0<\delta<1`, then conditional on **every H**, for a set of original honest public tensors of probability at least `1-\sqrt\delta`, the public one-shot greedy + residual procedure has per-tensor success probability at least
\[
\boxed{
(1-\sqrt\delta)q^{-E_t-(r+1)t}.}
\]
After at most
\[
\boxed{
R=\left\lceil
\frac{q^{E_t+(r+1)t}\ln(1/\eta)}{1-\sqrt\delta}
\right\rceil
}
\]
independent public trials (same public A, fresh coins), the unconditional honest-source probability of a **fully original-verifier accepted d-plane** is at least `1-\sqrt\delta-\eta`, using at most `R\operatorname{poly}(n,m,t,\log q)` field operations.

**Proof.** Every precommitted genuine flag obeys the prefix and terminal failure bounds above; no independence between them is needed. Average their failure indicator over all genuine complete t-flags in H. Its conditional source expectation is at most δ. Markov gives that the fraction G(A,H) of entirely good true flags is at least `1-\sqrt\delta` on a source event of probability at least `1-\sqrt\delta`. The earlier public quotient-vector path-counting theorem shows that for a fixed A, the probability of following **some** good true flag is at least `G(A,H)q^{-E_t-(r+1)t}`. Every such terminal flag passes the public residual solver and produces H, which the unchanged verifier accepts. Repeating independent public random tapes on the **same A**, and then averaging over the source-good event, gives the displayed bound. This does not apply a fixed-T tensor law to an adaptive chosen seed. QED.

Over fixed effective binary extension fields `q=2^e`, the one-shot full-public greedy + residual + verifier predicate admits a polynomial reversible circuit with a fixed uniform random tape, exactly as in [the prior quantum pass](F0-planted-ti-quantum-greedy-flags.md). **Established fixed-point amplitude amplification** consequently gives an attack with the same source-good probability and coherent work upper-bounded by
\[
O\left(
\operatorname{poly}\,
q^{(E_t+(r+1)t)/2}
\frac{\ln(1/\eta)}{\sqrt{1-\sqrt\delta}}
\right),
\]
with ordinary polynomial precision overhead and a final classical original-verifier check. This is *known generic quantum square-root search*, not a new quantum algorithm or quantum-hardness statement. No quantum implementation or experiment is claimed.

## 6. Sparse source: shorter t and reduced **upper** work exponents

Take fixed q, `d/n\to\alpha\in(0,1/2)` and `m\asymp n/\log n`. Choose
\[
s=\left\lceil2d/m\right\rceil+3,\qquad
t=\left\lceil\frac{c-d+s}{m-1}\right\rceil,\qquad
r=\left\lceil\sqrt{3\log_q n}\right\rceil.
\]
For all sufficiently large n, `1<=t<=d`, `0<mt<c`, `\ell_0=c-mt=\Theta(n)`, and
\[
h=(m-1)t-(c-d)\ge s.
\]
It follows from §3 that `\delta_{\rm end}=q^{-\Omega(n)}`, while `\delta_{\rm prefix}=o(1)`. Thus the fixed true-seed, exhaustive public, and randomized public attacks all have the rigorously stated high source success bounds without any secret information.

The seed dimension is now
\[
\boxed{t=\frac{c-d}{m}+O(1)=
\frac{n-2d}{m}+O(1),}
\]
rather than approximately c/m for full linear orthogonal completion. The bounded-work **leading q-exponents** are
\[
\boxed{\begin{aligned}
\log_q W_{\rm exhaustive}&\le
\frac{n(c-d)}m+o(n^2/m),\\
\log_q W_{\rm randomized}&\le
\frac{c^2-d^2}{2m}+o(n^2/m)
=\frac{n(c-d)}{2m}+o(n^2/m),\\
\log_q W_{\rm quantum}&\le
\frac{c^2-d^2}{4m}+o(n^2/m).
\end{aligned}}
\]
The asymptotics are **sufficient upper-work budgets**, not tight work identities, hardness lower bounds, or claimed priority over every other published algorithm. All remain `q^{O(n\log n)}` in the stated sparse scaling: none is a polynomial inversion algorithm.

For `d/n\to1/3`, compare the prior full-linear-completion upper leading coefficients of `n^2/m` (exhaustive `2/3`, classical randomized `2/9`, standard quantum `1/9`) against this residual method (`1/3`, `1/6`, `1/12`). The **classical randomized leading exponent falls by one quarter**, and the exhaustive leading exponent by one half. They remain superpolynomial and do not establish any secure parameter set.

## 7. Independent tiny arithmetic controls (scratch, not a benchmark)

Take `n=7,d=3,c=4,m=3,t=1`, so `mt=3<c`, `\ell_0=1`, `u=2`, `h=1`, and the residual method is defined. For a **fixed genuine seed** T:

- Over GF(2), the `3\times4` seed cross-row block has full row rank for exactly `(16-1)(16-2)(16-4)=2520` of the `2^{12}=4096` possible matrices, so `p_{\rm row}=315/512`. Independently, the residual three `1\times2` cross rows have all `2^6=64` possibilities; exactly **42** have at least two distinct nonzero row directions, the support-intersection success condition. Hence `p_{\rm supp}=21/32`, and the **exact true-seed** public inversion probability is `6615/16384`.
- Over GF(3) at the same dimensions, the full-row probability is `p_{\rm row}=(1-3^{-4})(1-3^{-3})(1-3^{-2})=16640/19683`. The residual three `1\times2` rows yield `p_{\rm supp}=1-4(1/3)^3+3(1/9)^3=208/243`; their product is **3461120/4782969**.

These are independent finite field **block-count and Möbius formula controls**, not enumeration of entire `m\times n\times n` public alternating tensors, committed tests, calibrated runtime, random source samples or evidence for cryptographic parameters. The algorithm's possible successes on **incorrect** public seeds are additional and are always original-verifier gated.

## 8. Scope and next attack-first objective

- This is a **full-public constructive attack on the original any-witness relation**. The source theorem conditions only in the *proof* on a fixed hidden true seed; the actual attacks do not know H or test true membership.
- The residual conditional source is uniform **only after the specified genuine-seed and rank event**. Public tensor-adaptive seeds are treated by the enumeration of all seeds or by a source-good fraction of all precommitted true flags, never by pretending that their terminal conditional law is uniform.
- The technique **reuses** elementary public linear algebra and an earlier high-d support-intersection attack on a publicly computable quotient; it is not a newly proposed hard foundation, cryptographic primitive, trapdoor or independent Field-15 novelty.
- This improves a *specific sufficient-work exponent* while retaining the **known generic q^{O(n log n)} class**; the best existing external algorithm could be as good or better. A literature-level comparison remains necessary before any novelty assertion.
- The genuine open problem is **polynomial-time global tensor-adaptive extraction** in `d<c`, or a materially different original-verifier relation with positive Field-15 evidence. Neither follows from this work.
- No new N1-60 reservation, F0-K/A-ID, KEM/PKE/OWF, quantum implementation, public benchmark, source corpus, README expansion or stage-registry edit.

**Disposition:** SHORTER-SEED FULL-PUBLIC RESIDUAL SUPPORT-INVERSION ATTACK, STRICT SOURCE-LAW AND VERIFIER GATES. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD; HEPMR BENCHMARK ONLY; N1-60 free.
