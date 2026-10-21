# MORPH-F0: sharp leading exponent of public greedy-flag seed selection

**2026-10-21. Exact deterministic terminal-proposal density bound + honest-source matching exponent. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.** This note combines the [public zero-abort greedy flag algorithm](F0-planted-ti-randomized-flag-search.md), its [exact nested-rank analysis](F0-planted-ti-greedy-flag-exact-rank-dp.md), the [shorter residual support completion theorem](F0-planted-ti-seeded-residual-support-attack.md), and the [uniform-proposal gate barrier](F0-planted-ti-public-gate-probe-complexity.md). It proves the previous greedy attack's leading \(q\)-work exponent is also **necessary for this precise public greedy terminal-proposal mechanism**, when wrong original-verifier witnesses are rare; no unrestricted or quantum hardness lower bound is asserted. The underlying planted TI problem and a generic \(q^{O(n\log n)}\) attack were already developed by [Liu–Qiao–Tang–Zhang, §3.3, Proposition 5](https://arxiv.org/abs/2609.31256) (2026). No independent priority claim.

## 1. Precisely scoped public proposal mechanism

Let \(q\) be any prime power, \(V=\mathbb F_q^n\), \(2\le d<n\), \(c=n-d\), and \(m,t\) positive integers with \(1\le t\le d\) and \(mt<c\). All \(m\) alternating forms \(A_i\) are public. For the source-dependent statements, the original unfiltered honest source has a hidden \(d\)-plane \(H\), drawn from any prior independently of \(A\), and independent conditional-uniform alternating forms annihilating \(H\times H\). The original verifier accepts **any** \(d\)-plane on which **all m** forms vanish.

For a public isotropic \(k\)-plane \(U_k\), let \(S_A(U_k)\) be the common simultaneous orthogonal space, and \(R_k=n-\dim S_A(U_k)\) the publicly computable contraction rank. The **same established zero-abort greedy algorithm** starts at \(U_0=0\) and, for each \(k<t\), samples **one uniform vector** in the represented quotient \(S_A(U_k)/U_k\): abort if it is zero, otherwise extend by its projective line. Do not condition on nonzero or introduce an alternative seed sampler. At terminal depth t, the previous residual solver (or another algorithm) can only output a verified lifted \(d\)-plane **containing the terminal \(U_t\)**. The upper bound below applies to terminal seed generation *before* completion.

For fixed A, write \(Q_A(T)=\Pr_{\rm coins}[U_t=T\mid A]\) for any public t-plane T. Since zero draws can abort, Q is a **subprobability distribution**: \(\sum_T Q_A(T)\le 1\). This definition does not condition on terminal survival or inspect H. Put
\[
N={n\brack t}_q,\quad M={d\brack t}_q,\qquad
C_{q,t}=\prod_{i=1}^{t}(1-q^{-i})\in(0,1).
\]

## 2. Exact deterministic pointwise density cap

**Theorem 1 (all public inputs; every terminal T).** For **every** tuple of public alternating forms, regardless of whether it was honestly sampled, and every t-plane T,
\[
\boxed{Q_A(T)\ \le\
C_{q,t}\ q^{-t(n-t)+m{t\choose2}}.}
\]
Consequently, relative to the uniform measure on all N public t-planes,
\[
\boxed{\Lambda_{\rm greedy}:=
N\,\max_T Q_A(T)
\ \le\ N C_{q,t}\,q^{-t(n-t)+m{t\choose2}}
\ \le\ C_q q^{m{t\choose2}},}
\]
where \(C_q=\prod_{i\ge1}(1-q^{-i})^{-1}<4\). The leftmost \(\Lambda_{\rm greedy}\) can be below 1 because zero-abort produces a subprobability law; the bound is an **unnormalized proposal mass cap**, not a pointwise posterior of H.

**Proof.** Any realized terminal T comes from one of exactly
\[
F_t(q)=\prod_{i=1}^t{i\brack1}_q
\]
complete projective flags \(0=T_0<T_1<\dots<T_t=T\) inside T. Along each prescribed feasible flag, the earlier exact zero-abort quotient-vector path formula is
\[
p_{\rm path}(A,T_\bullet)
=(q-1)^t q^{-tn+t(t-1)/2+\sum_{k=0}^{t-1}R_k}.
\]
Each rank satisfies the deterministic bound \(R_k\le mk\) since k vectors give exactly mk contraction rows. Hence
\[
p_{\rm path}\le(q-1)^t q^{-tn+(m+1){t\choose2}}.
\]
An infeasible flag has probability zero and respects the same bound. Sum these disjoint flag path probabilities over the \(F_t(q)\) candidate flags ending at T. Using the exact identity
\[
(q-1)^t F_t(q)=\prod_{i=1}^t(q^i-1)
=q^{t(t+1)/2}C_{q,t},
\]
obtain
\[
Q_A(T)\le
q^{-tn+(m+1)t(t-1)/2+t(t+1)/2}\,C_{q,t}
=q^{-t(n-t)+m{t\choose2}}\,C_{q,t}.
\]
Finally \(N={n\brack t}_q\le C_q q^{t(n-t)}\), so multiplication by N gives the displayed density cap. No true-seed conditioning, independence between flags, or average source distribution is used. QED.

**Corollary (fixed H, fully public A, true terminal hit).** For any d-plane H, whether known, planted or merely used for analysis,
\[
\boxed{\Pr_{\rm coins}[U_t\subseteq H\mid A]
\ \le M C_{q,t}\,q^{-t(n-t)+m{t\choose2}}
\ \le C_q q^{-E_t},}
\]
where in the specified \(mt<c\) regime
\[
E_t=\sum_{k=0}^{t-1}(c-mk)
=ct-m{t\choose2}.
\]
**Proof.** Sum the pointwise cap over the exactly M t-planes contained in H; use \(M\le C_q q^{t(d-t)}\). The cap is pointwise in A and H, and does not rely on the tensor's being planted. QED.

The corollary is an upper bound on *ever reaching any true terminal seed during one zero-abort greedy run*. It is **not** a claim that finding some other accepted witness is impossible, nor a claim that every true terminal seed can be completed.

## 3. Restricted attack lower bound and matching known source-good upper work

**Theorem 2 (one-shot and K-repetition ceiling).** Take the original unfiltered honest planted distribution, and repeat the **same zero-abort greedy terminal seed proposal** at most K times on the *same public A*, with fresh coins. Upon each terminal proposal, allow any additional public computation, including the previous polynomial residual quotient solver, but any returned witness must be a **lift containing that proposed T** and pass the **entire original any-witness verifier**. Then
\[
\begin{aligned}
\Pr[\mathrm{output\ sampled}\ H]
&\le \min(1,KC_q q^{-E_t}),\\
\boxed{
\Pr[\mathrm{output\ any\ accepted}\ L]
&\le \min(1,\beta+KC_q q^{-E_t}).}
\end{aligned}
\]
Here \(\beta=\mathbb E_{\rm planted}\#\{L\ne H:\dim L=d,\ \operatorname{Verify}(A,L)\}\) is the earlier original-verifier wrong-witness first moment, not a null-source probability or a hidden-membership oracle. This holds for **any independent H-prior**.

**Proof.** Returning H by lifting any terminal seed forces that terminal T to lie in H. For every fixed (A,H), the one-shot cap of Theorem 1 holds; the K-trial union bound costs at most K times this probability even if the completion computation can use all public coefficients. If the attacker instead returns any other L≠H, the full original tensor necessarily admits an accepted wrong d-plane; its probability under the original source is at most β by Markov's inequality. Sum the two events. QED.

In particular, whenever \(\beta=o(1)\), every **constant-success** attack in this fixed greedy-proposal/lifted-output class needs \(K=\Omega(q^{E_t})\) greedy trials (and therefore that many public seed probes, up to polynomial field operations), with no assumptions about independence of wrong seeds.

Conversely, the already-proved **source-good public greedy+residual theorem** constructs accepted-H completions with, on a set of honest (A,H) probability at least \(1-\sqrt\delta\),
\[
\boxed{\Pr_{\rm coins}[\mathrm{output}\ H\mid A,H]
\ \ge(1-\sqrt\delta)\,q^{-E_t-(r+1)t}}
\]
for parameters with \(0<\delta<1\), and it amplifies on the *same* A with at most
\[
R=\left\lceil q^{E_t+(r+1)t}\ln(1/\eta)/(1-\sqrt\delta)\right\rceil
\]
trials to unconditional original-verifier success at least \(1-\sqrt\delta-\eta\). This is a **previous theorem**, not a new inference from the present density upper bound.

**Matched leading exponent in the sparse short-seed family.** Choose the earlier valid \(d/n\to\alpha\in(0,1/2)\), fixed q, \(m\asymp n/\log n\), \(t=\lceil(c-d+s)/(m-1)\rceil\) with \(s=\lceil2d/m\rceil+3\), and \(r=\lceil\sqrt{3\log_q n}\rceil\). The prior source theorem gives \(\delta=o(1)\); the wrong-witness theorem gives \(\beta=o(1)\); and \((r+1)t=o(n^2/m)\). Thus on an honest-source set of probability \(1-o(1)\), where accepted wrong d-planes do not exist,
\[
\boxed{
q^{-E_t-o(n^2/m)}
\ \le\ P_{\rm any}^{\rm one\ greedy\ trial}(A)
\ \le\ C_q q^{-E_t}.}
\]
Therefore the previously published-in-repo *upper* repetition-work exponent \(E_t\) is **also the tight leading lower exponent for precisely this zero-abort greedy terminal-proposal+lifted-verifier mechanism**, not for full-tensor algorithms generally. If a new global tensor-adaptive proposal rule changes the seed law, this lower bound need not apply.

At \(d/n\to1/3\),
\[
E_t={c^2-d^2\over2m}+o(n^2/m)
={n^2\over6m}+o(n^2/m).
\]
Thus the matching **class-restricted classical** leading coefficient of \(n^2/m\) is **1/6**. Do not transfer this to standard quantum fixed-point amplification, arbitrary coherent proposals, or adversarially selected nonuniform seeds; those were not lower-bounded here.

## 4. The terminal maximum-density budget matches the exact exponent gap

Uniform public t-plane sampling from PR #258 has chance \(M/N=q^{-ct+o(n^2/m)}\) to land inside H. The new greedy proposal cap allows at most a relative pointwise density increase
\[
\log_q\Lambda_{\rm greedy}
\le m{t\choose2}+O(1)
={ (c-d)^2\over2m}+o(n^2/m).
\]
The difference between the uniform proposal hitting exponent \(ct\) and the greedy exponent \(E_t\) is **exactly**
\[
\boxed{ct-E_t=m{t\choose2}.}
\]
Consequently, the generic bounded-proposal-density necessary-bias argument recorded in issue #208 and the present *actual greedy pointwise cap* meet at the **same leading exponent**. This is an algebraic comparison of a necessary distributional bias and a provable cap, not a proof that a particular public flag has saturated the upper probability or an independent cryptographic foundation.

The precise research bottleneck is now **replacing** this greedy terminal seed law by an efficiently computable tensor-adaptive sampler with a lower total exponent, or exploiting correlations in the complete public tensor without relying on a sampled contained seed at all. A stronger rank gate applied only *after* the same terminal proposals cannot improve the probability of generating a genuine terminal seed.

## 5. Finite GF(2) deterministic arithmetic control

Set \(q=2,n=10,d=c=5,m=2,t=2\), so \(mt=4<c=5\), \(N={10\brack2}_2=174251\), \(M={5\brack2}_2=155\), \(E_t=ct-m{t\choose2}=8\), and \(C_{2,2}=(1-1/2)(1-1/4)=3/8\).

For **every** public pair of alternating forms, including non-planted pairs, the exact theorem gives
\[
\boxed{
Q_A(T)\le (3/8)\,2^{-2(10-2)+2}
={3\over131072}
}
\]
for each fixed terminal 2-plane T. Hence \(\Pr[U_2\subseteq H\mid A]\le 155\cdot3/131072=465/131072\) for any 5-plane H, and the relative uniform density cap is \(N\cdot3/131072=522753/131072\approx3.9883\). These are direct **deterministic combinatorial bounds**, not measured attack success, whole-tensor enumeration, performance benchmarks, or crypto parameters.

The original one-independent-seed gate+support value \(35/8586\) from PR #258 is a **different** conditional experiment and must not be compared as if it were the greedy one-trial success rate.

## 6. Scope and next gate

- Exact algorithm analyzed: one-uniform-quotient-vector-per-depth **zero-abort** greedy flags, full public forms, final verified *lift containing the terminal t-plane*. Any change to how the next seed is proposed changes the theorem's scope.
- Source-good lower bound is from the earlier complete-slice conditional-uniform planted theorem; pointwise density ceiling is deterministic for every input. Neither uses tensor-adaptive fixed-genuine-seed conditioning.
- Any-witness correction uses the actual global \(\beta\) wrong-accepted-plane first moment, never silently replacing acceptance by hidden-H recovery.
- Matching \(q\)-exponent is a **restricted-algorithm** result, not a complexity-theoretic lower bound on arbitrary public, quantum, or polynomial-time inversion methods; no Field-15 novelty or security evidence.
- The next meaningful direction is a **different** public seed distribution or full-tensor method, with exact original verifier success and quantitative conditional source law. An additional post-proposal rank filter alone cannot cross this proven gate.

No new N1-60, F0-K, A-ID, code, benchmark, field campaign, KEM/PKE/OWF, README expansion or stage-registry modification. **GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD; HEPMR BENCHMARK ONLY.**
