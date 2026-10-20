# MORPH-F0: exact honest-source greedy-flag recovery by a finite rank dynamic program

**2026-10-20. Constructive attack accounting / independent exact source-law theorem; GLOBAL NO NOMINATION, H-A/H-B/H-C HOLD.** This derives a polynomial-arithmetic-time *analysis* of the one-trial recovery probability for the previously specified [public randomized greedy-flag algorithm](F0-planted-ti-randomized-flag-search.md). It does **not** give the attacker a polynomial inversion algorithm. The target is the unfiltered planted totally-isotropic source; all outputs of the actual attacker still require the unchanged original **any-witness verifier**.

**External context.** The planted-TI relation and generic `q^{O(n log n)}` upper bound are due to Liu, Qiao, Tang and Zhang, [*The planted tensor problem over finite fields: algorithms and cryptography*](https://arxiv.org/abs/2609.31256) (2026). The present note makes no claim of an independent Field-15 problem, priority over standard flag-counting methods, or new security evidence.

## 1. Honest source and the precisely specified one-shot algorithm

Over any prime-power field `F_q`, take `2<=d<n`, `c=n-d`, `m>=1`, and a target `1<=t<=d`. Sample a hidden d-plane `H` from **any prior independently of the forms**; conditional on H, publish m independent uniform alternating forms `A_i` annihilating `H x H`, without rank postselection.

The public greedy algorithm starts with `U_0=0`, and at each `k<t` computes
\[
S_A(U_k)=\{v\in V:A_i(u,v)=0\ \forall u\in U_k,\ 1\le i\le m\}.
\]
It chooses **one uniform vector** from the represented quotient `S_A(U_k)/U_k`. If the vector is zero, **the trial aborts**; otherwise it extends the flag by its projective line. At depth t it outputs `S_A(U_t)` *only* when its dimension equals d and the entire original public verifier accepts. This is the **zero-abort, not resample-until-nonzero**, algorithm of the prior note.

Define `P_H` as the unconditional probability that one trial actually outputs the **sampled H**. The probability `P_{\rm any}` of returning *any* originally accepted d-plane satisfies `P_{\rm any}\ge P_H`, with possible strict inequality; the distinction is essential for the MORPH any-witness gate.

## 2. The fixed-true-flag rank Markov chain

Fix H only in the analysis and choose any complete true flag
\[
0=T_0<T_1<\cdots<T_t\subseteq H,\qquad \dim T_k=k,
\]
**before** independently drawing the public matrices. Each public contraction on `T_k` vanishes on H, leaving a uniform `mk\times c` quotient matrix `M_k`. In an H-adapted basis of the complete flag, adding `T_{k+1}/T_k` exposes precisely `m` fresh independent uniform rows of length c. Hence the nested ranks
\[
R_k=\operatorname{rank}M_k,\quad R_0=0
\]
form a finite Markov chain (for a fixed precommitted true flag):

\[
\boxed{
\Pr[R_{k+1}=r+z\mid R_k=r]
=\pi_{m,c-r}(z),}
\]
where `\pi_{a,b}(z)` is the exact rank-z probability of a uniform `a\times b` matrix,
\[
\boxed{
\pi_{a,b}(z)=q^{-ab}{b\brack z}_q
 \prod_{j=0}^{z-1}(q^a-q^j),\qquad
0\le z\le\min(a,b).
}
\]

This chain is an **analyst's distribution** for every fixed true flag, *not* a public rank oracle revealing H or an assertion about the form distribution conditional on the attacker's tensor-adaptive chosen flag.

For a given genuine prefix `T_k`, the quotient `S_A(T_k)/T_k` has dimension
\[
D_k=n-k-R_k.
\]
The one-shot uniform quotient-vector algorithm hits the **specified nonzero projective child** `T_{k+1}/T_k` with probability exactly
\[
\boxed{(q-1)q^{-D_k}.}
\]
Unlike the conditional-nonzero-projective-line algorithm, it can abort on the zero quotient vector. The completion `S_A(T_t)=H` holds **if and only if** `R_t=c`.

## 3. Exact finite source success and polynomial rational recurrence

The number of complete true flags of length t in H is
\[
N_H={d\brack t}_q\prod_{i=1}^t{i\brack1}_q.
\]
All such flags have the **same joint source law** of their rank chains; their path events under one trial are disjoint. Therefore

**Theorem 1 (exact one-shot planted-H recovery, every H prior).**
\[
\boxed{
P_H=N_H(q-1)^t q^{-tn+t(t-1)/2}
\,\mathbb E\!\left[
q^{R_0+\cdots+R_{t-1}}\mathbf 1_{\{R_t=c\}}
\right].}
\]

This remains valid when `mt<c`, in which case the expectation and `P_H` both vanish. In particular,
\[
\boxed{P_{\rm any}\ge P_H,}
\]
but no equality of these two success probabilities is claimed.

**Proof.** For each fixed public tensor A, if the algorithm ends with `S_A(U_t)=H` then `U_t\subseteq H`, and all intermediate flag nodes lie inside H. Conversely each genuine complete flag with `R_t=c` gives one path that outputs H and passes the original verifier. Conditional on A, the probability of that path is
\[
\prod_{k=0}^{t-1}(q-1)q^{-(n-k-R_k)}
=(q-1)^t q^{-tn+t(t-1)/2}q^{\sum_{k<t}R_k}.
\]
These path events are disjoint. Sum over all true flags, average over the **unfiltered** forms and then over any H prior; by symmetry each fixed true flag has the same nested uniform-block rank law described above. QED.

The expectation is computable by the finite weighted dynamic program

\[
\boxed{
v_0(0)=1,\qquad
v_{k+1}(r')=\sum_{r=0}^{c}
v_k(r)\,q^r\,\pi_{m,c-r}(r'-r),
\qquad
P_H=N_H(q-1)^t q^{-tn+t(t-1)/2}v_t(c),
}
\]
where out-of-range `\pi` values and absent states are zero. There are at most `t(c+1)` states and `O(tc\min(m,c))` possible transitions. Gaussian binomials and the exact rational arithmetic have polynomial bit length in `n,m,t,\log q`. The recurrence is therefore polynomial in the stated parameters **as an exact mathematical probability evaluator**, not as a search for an accepted public d-plane.

## 4. Independent finite-field checks and an important sample-definition distinction

For `GF(2),n=4,d=2,c=2,m=2,t=2`, with H fixed to the first two coordinate axes:

- The recurrence gives `v_2(c)=303/128` (a **weighted moment**, allowed to exceed 1), `N_H=3`, and `P_H=909/16384`.
- Independently exhaust all `2^{2(dc+\binom c2)}=1024` honest ordered full alternating-form pairs, calculate true-prefix ranks, and sum exact one-shot path probabilities: again `909/16384`.
- Independently enumerate only all `2^{mdc}=256` ordered public cross-block patterns: the same exact source average follows after the irrelevant complement blocks are summed out.
- For the distinct **resample-until-nonzero** rule, each prescribed child has probability `1/{D_k\brack1}_q`, not `(q-1)q^{-D_k}`. The corresponding tiny-event probability is **93/896**, so these two numbers must never be substituted for one another.

For a separate small check, `GF(2),n=5,d=2,c=3,m=2,t=2` yields `P_H=1701/131072` both from the recurrence and by independent exhaustive enumeration of all `2^{mdc}=4096` cross-block tuples. These are **scratch exact arithmetic controls**, not committed runnable attack code, measured runtime tests, an honest-source benchmark dataset or evidence of cryptographic security.

**Historical reconciliation:** The current [randomized flag document](F0-planted-ti-randomized-flag-search.md) on main *already* reports `909/16384` for the one-shot zero-abort variant. This note adds the general recurrence and second independent small parameter control; it does **not** reopen or silently overwrite an already corrected experiment.

## 5. Asymptotic interpretation and limits

The rank-chain law permits finite, source-faithful calculation of one-trial **hidden-H recovery** without sampling whole planted matrices, but this exact **average** cannot be substituted for a per-public-tensor success guarantee. In particular, applying quantum fixed-point amplification using only an **average** value of `P_H` as a certified success lower bound for each A would be invalid. The independent [source-good flag fraction theorem](F0-planted-ti-randomized-flag-search.md) supplies the necessary concentration screen, as used in the [quantum amplification note](F0-planted-ti-quantum-greedy-flags.md).

This pass **does not improve** the proven classical `q^{c^2/(2m)+o(n^2/m)}` or quantum `q^{c^2/(4m)+o(n^2/m)}` sparse-family *upper work exponents*, and does not show polynomial extraction in `d<c`. Exact probability evaluation is not inversion. Further progress requires a public algorithm using the entire tensor to bias flag choices toward genuine prefixes while preserving the original verifier and unconditional source.

No new primitive, hardness assumption, security claim, N1/F0-K/A-ID allocation, sampler, committed attack test, implementation, README expansion or stage-registry edit.

**Disposition:** EXACT FINITE-RANK DYNAMIC PROGRAM / FULL-PUBLIC GREEDY-FLAG HONEST-SOURCE H-RECOVERY PROBABILITY. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD; HEPMR BENCHMARK ONLY; N1-60 unallocated.
