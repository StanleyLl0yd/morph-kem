# MORPH-F0: calibrated any-witness inversion, planted-H recovery and null detection

**2026-10-20. Full-public source-first cryptanalytic calibration; GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.** This result combines the previously established [exact global wrong-witness incidence profile](F0-planted-ti-global-incidence-and-tangent-rigidity.md), [exact honest-source greedy-flag H-recovery rank DP](F0-planted-ti-greedy-flag-exact-rank-dp.md), and [no-terminal-slack source concentration](F0-planted-ti-genuine-seed-second-moment.md). It establishes **an explicit finite error bar** on the distinction between *recovering the sampled H* and *finding any accepted witness*, without ever replacing the original full public verifier. The fundamental planted-TI problem and generic classical `q^{O(n log n)}` attack class originate with Liu, Qiao, Tang and Zhang, [*The planted tensor problem over finite fields: algorithms and cryptography*](https://arxiv.org/abs/2609.31256) (2026). No independent mathematical hardness basis, cryptographic security or algorithmic priority is claimed.

## 1. Honest source, null source and original verifier

Let `q` be any prime power, `V=F_q^n`, `2<=d<n`, `c=n-d`, `m>=1`. Under the **original unfiltered planted distribution**, choose a hidden d-plane H from *any prior* independent of the forms; conditional on H, draw m independent uniform alternating forms A_i annihilating `H x H`. Under the **null distribution**, the m public alternating forms are independent unrestricted uniform.

The original, unchanged public accepted set is
\[
\mathcal E(A)=\{L\in\operatorname{Gr}(d,V):
 A_i|_{L\times L}=0\text{ for all }i\}.
\]
**Every L in this set wins** the original search relation; it need not be the sampled H. Let `B` be any randomized or deterministic attacker, possibly quantum, given the complete public tuple A and public parameters but **not** H. Assume only that a reported output is a candidate d-plane (and the verifier decides whether it is accepted). No time bound is required for the finite claims.

Define over honest `(H,A)` and the attacker's own coins
\[
P_{\rm any}(B)=\Pr[B(A)\in\mathcal E(A)],
\qquad
P_H(B)=\Pr[B(A)=H].
\]
A failure symbol counts as neither event; if an attacker emits an unverified d-plane it is still scored using the **original** verifier. Since H is always in `\mathcal E(A)`, `P_H<=P_{\rm any}` even for an arbitrary attacker.

## 2. Exact finite uniqueness first moment and universal success sandwich

For `1<=r<=\min(d,c)` put
\[
k_r={r(2d-r-1)\over2},\qquad
M_r={d\brack r}_q{c\brack r}_q q^{r^2},
\qquad
\boxed{\beta=\sum_{r=1}^{\min(d,c)}M_rq^{-mk_r}.}
\]
The [previous exact incidence theorem](F0-planted-ti-global-incidence-and-tangent-rigidity.md) shows, conditional on **every fixed H**,
\[
\mathbb E_{\rm honest}[|\mathcal E(A)|-1\mid H]=\beta.
\]
Consequently `\Pr_{\rm honest}[|\mathcal E(A)|>1]\le\min(1,\beta)`, without assuming independence of competing witnesses.

**Theorem 1 (algorithm-universal any-witness calibration).** For **every** algorithm B using the *actual full public tensor*, under **every prior on H**,
\[
\boxed{
0\le P_{\rm any}(B)-P_H(B)
\le \Pr_{\rm honest}[|\mathcal E(A)|>1]
\le\min(1,\beta).
}
\]

**Proof.** The only outcome counted by `P_{\rm any}` but not `P_H` is a verifier-accepted d-plane different from H. Its existence implies `|\mathcal E(A)|>1`. Inclusion of events and the exact first-moment Markov bound prove the statement. No information restriction, fixed-seed assumption, coupling to the null source, or average-case hardness claim is used. QED.

This holds *equally* for exhaustive algorithms, tensor-adaptive randomized flags, algorithms with internal quantum circuits and an arbitrarily powerful unbounded attacker. It gives an additive distributional success comparison, **not** an algorithm for extracting H and **not** a worst-case uniqueness claim on all inputs.

## 3. Exact finite one-shot greedy source bounds and null detection

For the existing public **one-shot zero-abort greedy-flag algorithm**, let `t` be its fixed terminal seed dimension. The [exact nested-rank dynamic program](F0-planted-ti-greedy-flag-exact-rank-dp.md) gives the honest-source H-recovery probability exactly:
\[
\boxed{
P_H^{\rm greedy}
={d\brack t}_q\left(\prod_{i=1}^{t}{i\brack1}_q\right)
(q-1)^t q^{-tn+t(t-1)/2}v_t(c),
}
\]
where `v_0(0)=1` and
\[
v_{k+1}(r')=\sum_r v_k(r)\,q^r\,\pi_{m,c-r}(r'-r),
\]
with `\pi_{a,b}` the uniform rectangular-matrix rank law. This is a **polynomial-size rational analysis** of an attack that uses all public forms; evaluating `v_t` is **not** a public method to find a witness.

By Theorem 1, for the **actual original verifier**,
\[
\boxed{
P_H^{\rm greedy}\le P_{\rm any}^{\rm greedy}
\le\min(1,P_H^{\rm greedy}+\beta).
}
\]
This gives a genuinely finite, source-faithful error bar around the exact greedy source average even when multiple different verifier-accepted d-planes exist.

Under the unrestricted-null source, a precommitted d-plane has probability `q^{-m{d\choose2}}` of passing all alternating forms. Therefore the expected number of accepted null d-planes is exactly
\[
\boxed{
\nu={n\brack d}_q q^{-m{d\choose2}},
\qquad
\Pr_{\rm null}[\mathcal E(A)\ne\varnothing]\le\min(1,\nu).
}
\]

**Theorem 2 (real full-public search-to-detection upper screen).** Run any public algorithm B, then output a binary detector value 1 **only if** B produced an originally verifier-accepted d-plane; otherwise output 0. Its actual planted-vs-null acceptance gap obeys
\[
\boxed{
\Pr_{\rm planted}[D_B=1]-\Pr_{\rm null}[D_B=1]
\ge P_H(B)-\min(1,\nu).
}
\]
The planted true-positive rate is `P_{\rm any}(B)` and the null false-positive rate is at most `\min(1,\nu)`. Thus the explicit exact greedy DP gives the lower gap `P_H^{\rm greedy}-\min(1,\nu)`, clipped at zero if only a nonnegative bound is desired.

**Proof.** Any accepted candidate under null proves that the null tuple has at least one accepted d-plane, so the false-positive event is contained in `\{\mathcal E(A)\ne\varnothing\}`. The null union bound controls it, while the planted accepted-output rate is at least the true-H recovery rate. QED.

**Scope caveat:** the detector inherits its **actual runtime** from B, which in the externally conjectural sparse regime remains superpolynomial for the current greedy search and its amplified variants. A mathematical search-to-detection transformation is **not** a polynomial-time planted/null distinguisher without a polynomial-time search algorithm.

### Exact null-support TV under a **uniform** hidden-H prior

The general honest-prior results above do not require H to be uniform. For the following additional exact statistical identity only, assume **H uniform** over all `N={n\brack d}_q` d-planes. Let `Z(A)=|\mathcal E(A)|` and `\nu=N q^{-m{d\choose2}}`, as above.

**Theorem 3 (exact size-biased source law and optimal *unbounded* detector).**
\[
\boxed{\frac{\Pr_{\rm planted}[A]}{\Pr_{\rm null}[A]}
=\frac{Z(A)}{\nu}.}
\]
When `0<\nu\le1`, it follows *exactly* that
\[
\boxed{
\operatorname{TV}(P_{\rm planted},P_{\rm null})
=1-\Pr_{\rm null}[Z(A)>0]
=1-\nu\,\mathbb E_{\rm planted}\!\left[{1\over Z(A)}\right].
}
\]
The convention on `1/Z` is harmless: under the planted source `Z>=1` always. In particular,
\[
\boxed{
\nu\max(0,1-\beta)
\le \Pr_{\rm null}[Z>0]\le\nu,
}
\qquad
\boxed{
1-\nu\le \operatorname{TV}(P_{\rm planted},P_{\rm null})
\le 1-\nu\max(0,1-\beta).
}
\]
For `\nu\le1`, the **optimal information-theoretic likelihood-ratio test** distinguishes by the event `Z(A)>0`; this is an unbounded existence test and is **not** an efficient detector in the sparse setting.

**Proof.** For every fixed H, conditioning m independent unrestricted uniform alternating forms to annihilate `H\times H` multiplies their null point mass by `q^{m{d\choose2}}` if H is accepted, and gives zero otherwise. Averaging uniformly over N possible H yields the displayed Radon–Nikodym ratio `q^{m{d\choose2}}Z/N=Z/\nu`. For `\nu\le1`, the likelihood ratio vanishes on `Z=0` and is at least one on `Z>=1`. The minimum common probability measure is therefore exactly the null mass on `Z>0`, proving the first TV equality. The size-bias identity implies
\[
\Pr_{\rm null}[Z>0]
=\sum_{A:Z(A)>0}\Pr_{\rm planted}[A]\,{\nu\over Z(A)}
=\nu\,\mathbb E_{\rm planted}[1/Z].
\]
Since `0<=1-1/Z<=(Z-1)` for positive integer Z, the prior exact first moment `\mathbb E_{\rm planted}(Z-1)=\beta` yields `1-\beta<=\mathbb E_{\rm planted}[1/Z]<=1`. Clip the lower bound at zero and multiply by `\nu`. QED.

**Priority and limitation:** the underlying planted size-bias/posterior phenomenon was already analyzed in [issue #208's earlier uniqueness/size-bias checkpoint](https://github.com/StanleyLl0yd/morph-kem/issues/208#issuecomment-6215551334). This is a **scoped finite TV and null-support calibration consequence**, not a claim to a newly discovered general size-bias theorem. For nonuniform H priors, the likelihood is instead `q^{m{d\choose2}}\sum_H\pi(H)\mathbf 1_{\{H\in\mathcal E(A)\}}`, and neither the displayed uniform-H ratio nor the exact TV simplification follows automatically.

An independent tiny exact GF(2) arithmetic control uses `n=3,d=2,m=4`, where `N=7`, `\nu=7/16`. Exhausting all `2^{m{n\choose2}}=4096` unrestricted full tuples gives the histogram `Z=0,1,3,7` with respective counts `2520,1470,105,1`. Thus
\[
\Pr_{\rm null}[Z>0]=\frac{197}{512},\quad
\operatorname{TV}(P_{\rm planted},P_{\rm null})=\frac{315}{512},\quad
\beta=\frac38,
\]
and the exact bounds `35/128 <= 197/512 <= 7/16` hold. This is **scratch arithmetic only**: no committed source data, benchmark, executable test or cryptographic security parameter.

## 4. Sparse d<c regime: asymptotic equivalence of actual success events

Fix q and let `d/n\to\alpha\in(0,1/2)`, `m\asymp n/\log n`, `c=n-d`. Set `\Delta=m(d-1)/2-(n-1)`. The established finite incidence estimate gives, for `\Delta>0`,
\[
\boxed{
\beta\le C_q^2{q^{-\Delta}\over1-q^{-\Delta}}
=q^{-\Omega(n^2/\log n)}.
}
\]
For unrestricted null,
\[
\log_q\nu \le dc-m{d\choose2}+O_q(1)
=-\Theta(n^3/\log n).
\]
Both are *analytic source probability bounds*, not measured running times.

Set `t=\lceil c/m\rceil=\Theta(\log n)` and `r=\lceil\sqrt{3\log_q n}\rceil`. The [previous genuine-seed second-moment theorem](F0-planted-ti-genuine-seed-second-moment.md) establishes a source-good event of probability `1-o(1)` on which the **same publicly evaluable, one-shot zero-abort greedy algorithm** has conditional H-recovery chance at least
\[
{p\over4}q^{-E_t-(r+1)t},
\quad
p=\prod_{j=0}^{c-1}(1-q^{j-mt})\ge C_q^{-1},
\quad
E_t=\sum_{k=0}^{t-1}(c-mk)_+
={c^2\over2m}+O(c+m).
\]
Averaging over A yields `P_H^{\rm greedy}\ge q^{-O(n\log n)}`, explicitly a bound on its **one-trial probability**, not on a polynomial-time inversion rate.

Together these give
\[
\boxed{
0\le {P_{\rm any}^{\rm greedy}\over P_H^{\rm greedy}}-1
\le {\beta\over P_H^{\rm greedy}}
=q^{-\Omega(n^2/\log n)}.
}
\]
Similarly `\nu/P_H^{\rm greedy}=q^{-\Omega(n^3/\log n)}`, so the detector constructed from this **actual full-public** greedy attack has detection gap
\[
P_{\rm any}^{\rm greedy}-\Pr_{\rm null}[D=1]
=P_H^{\rm greedy}\bigl(1+o(1)\bigr).
\]
In words: although the original cryptographic game accepts **any** witness, this particular attack's unfiltered honest-source *single-run* success is asymptotically equivalent to recovering sampled H; null false positives are still smaller. **None of this is a hardness lower bound, a novel primitive, or a polynomial-time attack**.

For an arbitrary B without a quantitative lower bound on `P_H(B)`, Theorem 1 gives **only the additive** `\beta` comparison, not the multiplicative conclusion.

## 5. Independent exact binary arithmetic control (scratch only)

Let `GF(2)`, `n=7,d=3,c=4,m=8,t=1`. The true-seed single-line completion probability is
\[
p=\prod_{j=0}^{3}(1-2^{j-8})
=\frac{63247905}{67108864}.
\]
The one-shot zero-abort greedy public algorithm first draws one uniform full-vector quotient element, and hence exactly
\[
\boxed{P_H^{\rm greedy}
=\frac{2^d-1}{2^n}\,p
=\frac{442735335}{8589934592}.}
\]
An independent Gaussian-incidence sum has `M_1=210,k_1=2`, `M_2=3920,k_2=3`, and `M_3=7680,k_3=3`; therefore
\[
\boxed{
\beta={210\over2^{16}}
+{3920\over2^{24}}+{7680\over2^{24}}
={4085\over1048576}.
}
\]
The unrestricted-null original-verifier first moment is
\[
\boxed{\nu={7\brack3}_2\,2^{-24}
={11811\over16777216}.}
\]
Consequently the genuine original-verifier single-shot success is bracketed by
\[
P_H^{\rm greedy}
\le P_{\rm any}^{\rm greedy}
\le P_H^{\rm greedy}+\beta<1,
\]
and the associated binary detector has planted-minus-null gap at least
\[
\boxed{
P_H^{\rm greedy}-\nu
={436688103\over8589934592}>0.
}
\]
These are **exact finite rational formula evaluations**, not an enumeration of all 2^{m*(binom(n,2)-binom(d,2))} honest public tensors, committed tests, empirical attack runs or a security calibration for a real parameter set.

## 6. Boundaries and research priority

- The accepted-witness error bar is explicitly about the **real original verifier**; no hidden-H acceptance check replaces it. Almost-sure source uniqueness is statistical, not an efficient public extraction technique.
- The null detector is efficiently *verifiable* once a witness is produced, but the present sparse **search work is q^{O(n log n)}**, not polynomial or a proof of post-quantum hardness.
- The exact first moments `\beta,\nu` and rank DP can be evaluated as mathematics without a public section. No claim of new Field-15 originality is made for combining previously proved bounds.
- **Next real attack bottleneck:** design a polynomial-time global tensor-dependent seed bias or a direct public solver whose original-verifier success can be demonstrated under the unfiltered source. A better probability calibration, marginal moment or restricted-oracle indistinguishability alone does not meet this gate.
- No N1-60 allocation, F0-K/A-ID, KEM/PKE/OWF/trapdoor, new sampler/corpus, executable attack, quantum measurement, README expansion or stage-registry change.

**Disposition:** FINITE ANY-WITNESS/TRUE-H SUCCESS SANDWICH AND NULL-VERIFIER DETECTION GAP, NOT A NEW INVERTER. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD; HEPMR BENCHMARK ONLY; N1-60 remains free.
