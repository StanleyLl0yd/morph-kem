# MORPH-F0: randomized public isotropic-flag search with source-aware success bound

**2026-10-20. Constructive randomized full-public-tensor attack. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.** This pass strengthens the [deterministic flag-enumeration bound](F0-planted-ti-isotropic-flag-search.md) and [fixed-seed completion theorem](F0-planted-ti-public-seed-completion.md). It studies the same **unfiltered planted source** and unchanged **any-witness verifier**, not an oracle-restricted problem. No KEM, OWF, trapdoor, security conclusion, Field-15 nomination, sample campaign or experimental attack implementation follows.

**Priority:** The planted totally-isotropic tensor relation, its conjectural sparse regime and a generic `q^{O(n log n)}` upper bound are from Liu–Qiao–Tang–Zhang, [*The planted tensor problem over finite fields: algorithms and cryptography*](https://arxiv.org/abs/2609.31256) (2026). This note derives a *self-contained leading-exponent upper bound for one elementary randomized greedy flag algorithm*; it does **not** assert that the method or exponent is new relative to all variants of their generic algorithm.

## 1. Original honest source, original output condition

Let `q` be any prime power, `V=F_q^n`, `2<=d<n`, `c=n-d`, and `m>=1`. Draw a hidden `d`-plane `H` from any prior independently of the public forms. Conditional on `H`, draw independent uniform alternating `A_1,...,A_m` annihilating `H x H`. **No postselection or conditioning on tensor rank** is allowed. All `m` matrices are public.

The only accepted output is any public `d`-plane `L` satisfying `A_i|_{L x L}=0` for every `i`, checked by the complete original verifier; an algorithm need not identify the sampled `H`.

For any public isotropic `k`-plane `U`, its common orthogonal space
\[
S_A(U)=\{v\in V:A_i(u,v)=0\ \forall u\in U,\ i=1,\ldots,m\}
\]
is computed by Gaussian elimination, and `U\subseteq S_A(U)`. Given a fixed `U\subseteq H` independently of the tensor draws, its public pairing matrix has rank equal to that of a **uniform `mk`-by-`c` matrix** (the previous [fixed-seed theorem](F0-planted-ti-public-seed-completion.md)). Only the proof knows `H`; the attacker never does.

## 2. Actual public randomized algorithm

For an integer `1<=t<=d`:

1. Start with `U_0=0`.
2. At depth `k<t`, compute `S_A(U_k)`. If `S_A(U_k)=U_k`, fail this trial. Otherwise choose a **uniform projective line** in the explicitly represented public quotient `S_A(U_k)/U_k` and let `U_{k+1}` be its preimage extension.
3. At depth `t`, compute `S_A(U_t)`. Output its basis **only if** its dimension is exactly `d` and the **full original verifier** accepts it. Otherwise fail this trial.
4. For amplification, repeat independent trials **on the same original public tensor**, each using fresh algorithmic randomness, until a verified witness is found or the fixed repetition budget ends.

Every generated flag is simultaneously isotropic, since every quotient extension is orthogonal to the current plane and all forms are alternating. Sampling a uniform projective line from a known quotient basis uses expected polynomial field operations (one may sample a uniform nonzero quotient vector and normalize).

## 3. Uniform finite rank-tail lemma for fixed genuine prefixes

For a uniform `a`-by-`c` matrix `M`, set `h=\min(a,c)`. For any positive integer `u`,

\[
\boxed{\Pr[\operatorname{rank}M\le h-u]
 \le C_q q^{-u(|a-c|+u)},\quad
 C_q=\prod_{j\ge1}(1-q^{-j})^{-1}<4.}
\]

**Proof.** If `a<=c`, rank deficiency `u` supplies a `u`-plane in the **left** kernel. There are at most `C_q q^{u(a-u)}` such planes, and each prescribed plane annihilates `M` with probability `q^{-uc}`. If `c<a`, use `u`-planes in the right kernel, giving `C_q q^{u(c-u)}q^{-ua}`. If `u>h` the event is impossible. Union bounds suffice; no independence between kernel planes is claimed. QED.

Fix `H` and a **precommitted complete flag** `0=T_0<T_1<...<T_t\subseteq H`, independent of the sampled `A`. For each `k<t`, write `R_k=\operatorname{rank}(M_{T_k})`, `a_k=\min(mk,c)`. For a nonnegative integer `r`, declare this flag *good* when:

- every prefix has `R_k>=a_k-r`; and
- the terminal pairing matrix `M_{T_t}` has full column rank `c`, so `S_A(T_t)=H`.

Assume `mt>=c+s` for an integer `s>=0`. By the rank-tail lemma and the exact [terminal completion bound](F0-planted-ti-public-seed-completion.md), **each fixed genuine flag**, under the unchanged conditional honest source, is bad with probability at most

\[
\boxed{\delta=t C_q q^{-(r+1)^2}
 +\frac{q^{-s}}{q-1}.}
\]

This uses a union bound over the `t` prefixes and terminal event, not an invalid independence assumption. It does not transfer a fixed-seed law to a tensor-adaptive terminal flag.

## 4. Source-level success for the randomized public search

Let `\mathcal F_t(H)` denote all complete flags of length `t` in `H`; its size is exactly

\[
N_H={d\brack t}_q F_t(q),\qquad
F_t(q)=\prod_{i=1}^t{i\brack1}_q.
\]

For a fixed sampled tensor and `H`, let `G(A,H)` be the fraction of these `N_H` flags that are *good*. Although `G` is not public and is never computed by the attack, the fixed-flag lemma gives

\[
\mathbb E[G(A,H)\mid H]\ge1-\delta.
\]

Let
\[
\boxed{E_t=\sum_{k=0}^{t-1}(c-mk)_+.}
\]

**Theorem 1 (finite conditional one-trial lower bound).** For every fixed `A,H`, the public randomized greedy algorithm satisfies

\[
\boxed{\Pr_{\rm algorithm}[\hbox{verified witness}\mid A,H]
\ \ge\ G(A,H)\,q^{-E_t-(r+1)t}.}
\]

**Proof.** Along any *good genuine flag* the rank condition gives
\[
\dim S_A(T_k)-k
=n-R_k-k
\le d-k+(c-mk)_++r.
\]
The algorithm's uniform next-line choice assigns this prescribed child probability
\[
1/{\dim S_A(T_k)-k\brack1}_q
\ge(q-1)q^{-d+k-(c-mk)_+-r}.
\]
The probability of the complete prescribed flag is at least the product over `k=0,...,t-1`. The terminal full-rank condition forces `S_A(T_t)=H`, and the **original verifier accepts**. Distinct complete flags are disjoint path events, so sum the lower bound over `G N_H` good genuine flags. Finally `[d choose t]_q>=q^{t(d-t)}`, `F_t(q)>=q^{t(t-1)/2}`, and `(q-1)^t>=1`; exponents cancel to `-E_t-(r+1)t`. Other successful paths only improve the bound. QED.

**Theorem 2 (amplified honest-source attack, every `H` prior).** If `0<\delta<1`, then conditional on any fixed `H`, with probability at least `1-\sqrt\delta` over the *honestly sampled* tensor, the conditional per-trial success probability is at least
\[
(1-\sqrt\delta)\,q^{-E_t-(r+1)t}.
\]
Therefore for any `0<\eta<1`, after
\[
\boxed{
R=\left\lceil
\frac{q^{E_t+(r+1)t}\ln(1/\eta)}
     {1-\sqrt\delta}\right\rceil
}
\]
independent public trials, success on the unconditional planted distribution is **at least** `1-\sqrt\delta-\eta` for every prior on `H`. Work is bounded by `R` times a fixed polynomial in the public representation size, `t`, and `\log q`. No runtime or security statement is made on adversarially selected nonhonest tensors.

**Proof.** Markov's inequality on the fraction `1-G(A,H)`, whose conditional expectation is at most `\delta`, shows that the event `G<1-\sqrt\delta` has conditional probability at most `\sqrt\delta`. Apply Theorem 1 on the complementary event. Fresh trials are independent **given the same fixed public tensor**; failure after `R` trials is at most `\exp[-R(1-\sqrt\delta)q^{-E_t-(r+1)t}]\le\eta`. Average over any prior on `H`. QED.

## 5. Sparse conjectural regime: stronger leading upper exponent

Fix `q` and assume `d/n\to\alpha\in(0,1/2)`, `m\asymp n/\log n`, `c=n-d`. Choose, for example,
\[
s=\lceil\sqrt n\rceil,\quad
t=\lceil(c+s)/m\rceil,\quad
r=\lceil\sqrt{3\log_q n}\rceil,
\]
eventually `1<=t<=d`, `s=o(m)`, `t=\Theta(\log n)`, and `\delta=o(1)`. Choose `\eta=o(1)` with `\log(1/\eta)=O(\log n)`. Then
\[
E_t={c^2\over2m}+O(c+m),\qquad
(r+1)t=o(n^2/m),
\]
and the deterministic work bound of Theorem 2 becomes

\[
\boxed{\log_q(\text{bounded randomized full-verifier work})
\le\frac{c^2}{2m}+o(n^2/m).}
\]

This is a strictly smaller **leading attack upper exponent** than the deterministic all-plane bound `cn/m` and the deterministic flag enumeration bound `(cn-c^2/2)/m` for the stated regime. All are still `q^{O(n\log n)}` (superpolynomial; not `q^{o(n)}`). Relative to public input length they have a different interpretation; **do not call them subexponential in `n`**.

At `\alpha=1/3`, the respective coefficients of `n^2/m` are `2/3`, `4/9`, and **`2/9`**. No claim is made that these constants beat the best existing specialized algorithm: that requires independent paper-level comparison.

## 6. Tiny independent exhaustive arithmetic control (not a benchmark)

For `q=2,n=4,d=2,c=2,m=2,t=2`, fix `H=\langle e_1,e_2\rangle`, enumerate **all 1024** conditioned full alternating-form pairs, and exactly sum the random quotient-line transition probabilities over the 15 initial projective points and their isotropic extensions. The source-average probability that a **single trial reaches `H` and its public completion equals `H`** is

\[
\boxed{93/896\approx0.103794642857.}
\]

Independent enumeration of just the uniformly drawn cross-blocks, with irrelevant complement blocks summed out, gives the same rational result. This is a **scratch exact control of a toy event**, not a committed runnable attack, counted cryptographic sample, original-verifier attack benchmark, or empirical large-parameter result. Other accepted `d`-planes could increase the algorithm's success beyond this particular `H`-recovery event.

## 7. Boundary and immediate next work

- **The extractor is not polynomial.** One greedy trial is polynomial, but the necessary repeated trials retain a `q^{\Theta(n\log n)}` bound in the sparse parameter family. No average-case hardness lower bound or crypto candidate is established.
- The proof explicitly handles adaptive public flag selection **without transferring** a fixed-seed rank law to the adaptively selected terminal plane: it counts all precommitted genuine flags and their independently valid prefix rank events, then sums exact algorithmic path probabilities.
- **Next target:** a genuinely polynomial public method to *bias* the greedy choices toward planted flags beyond this source-counting advantage; test point-contraction rank-defect and public radicals as negative controls before proposing min-rank extraction. Keep any-witness verification and full honest source.
- No new `N1`, `F0-K`, `A-ID`, source corpus, sampler/implementation, security parameter, README text or stage-registry reservation is authorized.

**Disposition:** SOURCE-AWARE RANDOMIZED FULL-TENSOR GREEDY-FLAG ATTACK / FINITE HONEST-SOURCE SUCCESS LOWER BOUND. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD; HEPMR BENCHMARK ONLY; N1-60 free.
