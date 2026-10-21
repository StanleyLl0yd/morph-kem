# MORPH-F0: exact full-row greedy one-shot H recovery and same-tensor success concentration

**2026-10-21. Original-source, full-public, unchanged-verifier attack analysis. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.** This exploits equality in the prior [all-input greedy terminal-seed density cap](F0-planted-ti-greedy-flag-terminal-density-cap.md) when a **genuine** terminal seed has full contraction-row rank. It supplies an exact source-average one-shot hidden-H recovery formula, a **pointwise same-public-tensor success identity**, and a source-good repetition theorem without the previous prefix-rank slack overhead. The original *any accepted d-plane* verifier remains the attack's only success criterion; the hidden-H rate is used only as an exact lower benchmark for original any-witness success. This does not establish polynomial extraction, a cryptographic foundation or an unrestricted attack lower bound. The planted-TI source and a generic \(q^{O(n\log n)}\) attack are already in [Liu–Qiao–Tang–Zhang (2026), §3.3](https://arxiv.org/abs/2609.31256).

## 1. Fixed original source, algorithm and quantities

Let q be any prime power, V=F_q^n, 2<=d<n, c=n-d, m>=2. The original honest source draws **any independently chosen prior** on a hidden d-plane H and, conditional on H, independent uniform alternating A_i annihilating H×H, with no rank conditioning or rejection. All coefficients of all m forms are public. The original accepted set comprises **every** d-plane L annihilated by all A_i, irrespective of its equality with H.

Choose \(1\le t<d\), \(0<mt<c\), \(\ell=c-mt>0\), \(u=d-t>\ell\). Use the **previously specified actual public zero-abort greedy algorithm**: at level k, choose one uniform vector from the public quotient \(S_A(U_k)/U_k\), abort on zero, otherwise extend by its line; continue to t. At terminal T, apply the [full-row-only residual image-support-intersection reconstruction](F0-planted-ti-seeded-residual-support-attack.md): require public contraction rank mt, recover the residual u-plane from all m public quotient slice images, lift an L containing T, and output L **only after checking the full original any-witness verifier**. On a failed seed, abort that one trial. The algorithm never receives H or checks T<=H.

Let
\[
\begin{gathered}
N={n\brack t}_q,\quad M={d\brack t}_q,\quad
C_{q,t}=\prod_{i=1}^t(1-q^{-i}),\\
E_t=ct-m{t\choose2},\quad
a_{d,t}=\prod_{i=0}^{t-1}(1-q^{i-d}),\\
p_{\rm row}=\prod_{j=0}^{mt-1}(1-q^{j-c}),\quad
p_{\rm supp}=p_{\rm supp}(u,\ell,m),\quad
p_{\rm seed}=p_{\rm row}p_{\rm supp},\quad
\varepsilon=1-p_{\rm seed}.
\end{gathered}
\]
The exact p_supp is the earlier finite Gaussian-Möbius intersection formula, not a postulated independent-slice empirical rate; conditional on a fixed precommitted true T and full rank, the original honest residual forms obey precisely the uniform planted quotient law. Set
\[
C=C_{q,t}\,q^{-t(n-t)+m{t\choose2}},
\quad MC=a_{d,t}q^{-E_t}.
\]

## 2. Pointwise equality at each full-row genuine seed

**Lemma 1 (maximal greedy proposal mass, pointwise).** Fix any honest (A,H) and a genuine t-plane T<=H for which the **public** T contraction has rank mt. Then
\[
\boxed{Q_A(T)=\Pr_{\rm public\ zero\!-\!abort\ greedy\ coins}[U_t=T\mid A]=C.}
\]
This is **equality**, not merely the all-input upper cap from the preceding theorem, and requires no source averaging.

**Proof.** Fix a basis of T. The full mt independent contraction rows imply, after any change of T basis, that the m*k rows corresponding to **every** k-plane U_k inside T are independent for each 0<=k<t. Thus every prefix of every complete flag ending at T has public rank R_k=mk. Since the true T is simultaneously isotropic, all its complete flags are valid public greedy paths. The earlier exact zero-abort path law assigns **each** such flag probability
\[
(q-1)^t q^{-tn+t(t-1)/2+m{t\choose2}}.
\]
There are exactly \(F_t(q)=\prod_{i=1}^t{i\brack1}_q\) complete flags ending in T, their path events are disjoint, and \((q-1)^tF_t(q)=q^{t(t+1)/2}C_{q,t}\). Summing gives precisely C. The form distribution is not used. QED.

Let X(A,H) be the **number of pre-existing genuine t-planes T<=H** on which the public full-row-only seeded terminal procedure would output **the sampled H**, i.e. the full-row and residual support certificate pass, followed by the entire original verifier. \(0\le X\le M\). The test defining X is conceptual for the analyst; the attacker NEVER enumerates true seeds or sees hidden membership.

**Theorem 1 (exact same-tensor one-shot H-recovery identity).** For **every honest** (A,H), the actual public one-shot greedy+full-row-residual algorithm satisfies
\[
\boxed{p_H(A,H)=\Pr_{\rm algorithm\ coins}[\mathrm{output\ sampled}\ H\mid A,H]
=C\,X(A,H)
=a_{d,t}q^{-E_t}\,{X(A,H)\over M}.}
\]
The actual probability of an **original-verifier accepted output** is at least p_H and may exceed it on false seeds yielding another accepted L.

**Proof.** The only terminal seeds that can produce H are contained in H, because every lifted candidate L includes its terminal T. For every genuine terminal T counted in X, full row rank holds, so Lemma 1 assigns probability exactly C to the corresponding complete disjoint terminal event, and the deterministic residual solver returns H. All other terminal T cannot return H. Sum over the X terminal events. QED.

## 3. Exact unconditional one-shot source probability and finite rank-defect sandwich

For any **fixed** precommitted genuine T, the earlier honest-law theorem proves
\[
\Pr_{A|H}[\text{full-row residual seeded solver returns H from T}]
=p_{\rm row}p_{\rm supp}=p_{\rm seed},
\]
identically for all H and true T, with no requirement that the public greedy process had selected T. Therefore by linearity of expectation,
\[
\mathbb E[X\mid H]=M p_{\rm seed}.
\]

**Theorem 2 (closed-form exact one-shot sampled-H recovery).** Averaging Theorem 1 over the **original unfiltered** honest tensor, for every H-prior,
\[
\boxed{
P_{H,\rm fullrow}^{(1)}
=q^{-E_t}\,a_{d,t}\,p_{\rm row}\,p_{\rm supp}(u,\ell,m).
}
\]
No weighted finite rank-state DP is needed **for this full-row-only terminal variant**. The earlier weighted DP is still correct and required for the **different rank-deficiency-tolerant** terminal variant.

**Rank-deficient correction.** Let \(P_{H,\rm adaptive}^{(1)}\) denote the rank-adaptive terminal support solver from PR #254, run after the *same* public greedy proposal. On full-row true seeds, it coincides with the full-row-only solver; any extra H success must come from true seeds whose T contraction rank is below mt. Since the previous pointwise density theorem bounds \(Q_A(T)\le C\) even on deficient seeds, and each fixed genuine T has deficient probability \(1-p_{\rm row}\),
\[
\boxed{
0\le P_{H,\rm adaptive}^{(1)}-P_{H,\rm fullrow}^{(1)}
\le a_{d,t}q^{-E_t}(1-p_{\rm row}).
}
\]
This **finite sandwich** does not assert an independent rank-defect terminal probability, nor equate the full-row and rank-adaptive finite algorithms.

## 4. Sharp same-public-tensor high-probability concentration

**Theorem 3 (source-good per-tensor success without prefix slack).** Conditional on **every** H, the fraction \(B(A,H)=1-X(A,H)/M\) of bad genuine t-planes satisfies
\[
0\le B\le1,\qquad
\mathbb E_{A|H}B=1-p_{\rm seed}=\varepsilon.
\]
This exact first moment suffices. For any \(0<\tau<1\), Markov gives
\[
\boxed{\Pr_{A|H}[\,X/M<1-\tau\,]\le\varepsilon/\tau.}
\]
In particular, when \(0<\varepsilon<1\), choosing \(\tau=\sqrt\varepsilon\) shows that, on a source set of probability at least \(1-\sqrt\varepsilon\) conditional on **each** H,
\[
\boxed{(1-\sqrt\varepsilon)\,a_{d,t}q^{-E_t}
\le p_H(A,H)\le a_{d,t}q^{-E_t}.}
\]
For \(\varepsilon=0\), X=M almost surely and both endpoints equal. No independence, second-moment estimate, concentration of different false seeds, postselected original generator, or tensor-adaptive fixed-T law is invoked.

**Theorem 4 (same-A independent repetition for original any-witness target).** For any \(0<\eta<1\) and \(0\le\varepsilon<1\), repeat the **actual complete public greedy+full-row terminal solver and original verifier** at most
\[
\boxed{
R=\left\lceil
{q^{E_t}\ln(1/\eta)\over a_{d,t}(1-\sqrt\varepsilon)}
\right\rceil
}
\]
times on the **same public A**, with independent fresh algorithmic random tapes, stopping on the first originally accepted L. Then for every prior on H, the probability of returning **some original-verifier accepted d-plane** is at least \(1-\sqrt\varepsilon-\eta\).

**Proof.** On the guaranteed source-good event, each full public one-shot trial finds H with probability at least \(p_0=(1-\sqrt\varepsilon)a_{d,t}q^{-E_t}\), and it may also find another acceptable witness. Fresh random tapes are independent conditional on the fixed A. The probability of no **original-verifier success** in R trials is at most \((1-p_0)^R\le e^{-Rp_0}\le\eta\). Average over the source event of probability >=1-\sqrt\varepsilon, with failure elsewhere conservatively treated as certain. QED.

This strictly sharpens the older proof's sufficient \(q^{E_t+(r+1)t}\) trial budget **when p_seed is close to one**, because full mt terminal rank automatically makes *all* true prefix ranks maximal; no separately screened prefix rank-tail parameter r is needed. It does not eliminate the residual support success/slack conditions that make \(\varepsilon\to0\).

## 5. Sparse-family asymptotic and any-witness calibration

Use fixed q and the earlier valid sparse source \(d/n\to\alpha\in(0,1/2)\), \(m\asymp n/\log n\), and \(t=\lceil(c-d+s)/(m-1)\rceil\), with \(s=\lceil2d/m\rceil+3\), yielding \(0<mt<c\), \(\ell=\Theta(n)\) and support excess \(h=u-\ell\ge s\). The previous honest-source estimates imply:
\[
1-p_{\rm row}=q^{-\Omega(n)},\qquad
1-p_{\rm supp}=q^{-\Omega(n)},\qquad
1-a_{d,t}=q^{-\Omega(n)}.
\]
Therefore \(p_{\rm seed}=1-q^{-\Omega(n)}\), \(\varepsilon=q^{-\Omega(n)}\), and
\[
\boxed{
P_{H,\rm fullrow}^{(1)}=(1-o(1))q^{-E_t},\qquad
R=(1+o(1))q^{E_t}\ln(1/\eta)\ \text{(up to the ceiling)}.
}
\]
The **rank-adaptive** extra-H contribution is also \(o(q^{-E_t})\) by the finite sandwich. For the full **original any-witness** success, the earlier global wrong-accepted-witness first moment \(\beta=q^{-\Omega(n^2/\log n)}\) obeys \(\beta=o(q^{-E_t})\), since \(E_t=\Theta(n^2/m)=\Theta(n\log n)\). The preceding calibration gives
\[
\boxed{
P_{\rm any}^{(1)}
=P_{H,\rm fullrow}^{(1)}+O(\beta)
=(1-o(1))q^{-E_t},
}
\]
where the first equality is a bound on the difference, not an unjustified literal equality of recovery and any-witness events.

Combining with the prior deterministic [terminal-density cap](F0-planted-ti-greedy-flag-terminal-density-cap.md) shows that the one-shot exponent E_t is tight **for this specific zero-abort greedy terminal-proposal/lifted-verifier algorithm class**, not for arbitrary global tensor-adaptive or quantum algorithms. At \(d/n\to1/3\), \(E_t=(1/6)n^2/m+o(n^2/m)\), still superpolynomial and not an asserted hardness lower bound.

The original verifier-gated output may also act as a detector between honest planted and unrestricted null: its null false-positive probability is bounded by the earlier original-verifier first moment \(\nu=[n\choose d]_q q^{-m\binom d2}\), but **this detector still costs the same superpolynomial public greedy search**. No polynomial distinguisher follows.

## 6. Independent finite exact arithmetic controls (no crypto benchmark)

**GF(2), n=6, d=3, c=3, m=2, t=1:** \(\ell=1,u=2,E_t=3,a_{d,t}=7/8\). The 2x3 true-T stacked cross block has full-row probability 21/32. The two residual independent 1x2 cross rows give support success 3/8 (two nonzero distinct directions among four possibilities each), so \(p_{\rm seed}=63/256\). Independent brute-force scratch enumeration of **all 262144 ordered pairs of 3x3 binary cross blocks** found precisely **172032** full-row cases and **64512** full-row support-successful cases. Hence
\[
\boxed{
P_{H,\rm fullrow}^{(1)}
={1\over8}{7\over8}{63\over256}
={441\over16384}.
}
\]
This is an exhaustive finite **cross-block** control only; irrelevant alternating complement coefficients were not enumerated, and no real attack implementation, runtime benchmark or cryptographic performance was measured.

**GF(2), n=8, d=c=4, m=3, t=1:** the full-row-only source one-shot probability is
\[
{15\over256}\,{315\over512}\,{231\over256}
=\boxed{{1091475\over33554432}}.
\]
The earlier full rank-**adaptive** finite DP gave \(76105575/2147483648\); their exact difference is \(6251175/2147483648\), agreeing with the additional *rank-2* branch \((15/256)(735/2048)(567/4096)\). This is a cross-check of distinct terminal procedures, not a silent contradiction or replacement of prior results.

## 7. Interpretation and next attack-first gate

- The public algorithm **never knows H**; true-T source analysis is done over all independently precommitted genuine terminal t-planes, then its public disjoint path probabilities are summed **pointwise**. No tensor-adaptive fixed-T conditional law is assumed.
- This is an exact same-tensor success refinement of an existing superpolynomial full-public attack, retaining the original conditional-uniform generator, all public slices, zero-abort sampling, and original any-witness verification. It does not nominate a primitive, prove average-case hardness, or imply a cryptographic security level.
- The generic planted-TI \(q^{O(n\log n)}\) attack class is externally prior. The concrete work exponent and exact one-shot formula are preserved for reproducible comparison, with **no independent Field-15 novelty claim**.
- The new negative gate is precise: improving this *unchanged greedy terminal-seed generator* by a post-proposal rank filter cannot beat the matched exponent. Improving total attack work requires a **different tensor-dependent seed generator**, a global algorithm that does not lift a sampled seed, or a provably different mathematical foundation.

No N1-60, F0-K, A-ID, source experiment campaign, KEM/PKE/OWF, quantum implementation, README expansion, stage-registry modification or positive nomination. **GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD; HEPMR BENCHMARK ONLY.**
