# MORPH-F0: public rank-gate probing, quenched selection, and a restricted uniform-seed search lower bound

**2026-10-21. Attack-first algorithmic boundary; GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.** This note separates the exact **single independently uniform seed** posterior of [the all-overlap rank-gate theorem](F0-planted-ti-overlap-rank-gate-posterior.md) from rejection sampling on a *single fixed public tensor*. It also gives a rigorous sampling lower bound for algorithms that probe uniform public seed planes and can only return a verified d-plane containing a probed seed. This is **not** a lower bound for unrestricted, tensor-adaptive, greedy-flag, or coherent quantum algorithms, nor a new hard foundation. The underlying planted-TI task and a generic superpolynomial attack class were published by [Liu–Qiao–Tang–Zhang](https://arxiv.org/abs/2609.31256) (2026).

## 1. Source and explicit attack class

Use the original *unfiltered* distribution from the preceding foundation documents: a hidden d-plane H in V=F_q^n, c=n-d, and m independent conditional-uniform alternating forms vanishing on H×H; all matrices are public. The original **any-witness verifier** accepts every d-plane L on which every original form vanishes. No generator rank postselection and no H-membership oracle are allowed.

Fix 1<=t<d, 0<mt<c, residual codimension ell=c-mt, u=d-t, and h=u-ell>0. For any public t-plane T let **Gate(A,T)** be the *public* simultaneous-isotropy, full-row contraction, and induced residual-rank<=2ell test of the all-overlap rank-gate note. Passing Gate does not certify a witness.

Write
\[
N={n\brack t}_q,\qquad M={d\brack t}_q.
\]
For each fixed (A,H), define:
\[
\begin{aligned}
G(A)&=\#\{T\le V:\dim T=t,\ \mathrm{Gate}(A,T)\},\\
X(A,H)&=\#\{T\le H:\dim T=t,\ \text{full-row residual support solver at }T\text{ outputs }H\}.
\end{aligned}
\]
The support solver *always* checks the complete original verifier before returning anything. The preceding genuine-seed theorem implies that every T counted in X passes Gate: hence
\[
0\le X(A,H)\le \min(G(A),M),\quad 0\le G(A)\le N.
\]
Let
\[
\mu_G=\mathbb E_{\rm planted}G=\sum_{j=0}^tN_jP_j,\quad
\mu_X=\mathbb E_{\rm planted}X=M\,p_{\rm row}\,p_{\rm supp}(u,\ell,m).
\]
Both are finite **first moments**, already exactly evaluable from previous source laws, for **any independent H-prior**. They are NOT values of G(A) or X(A,H) on a given input. We analyze two carefully distinguished algorithms.

**First-gate-stop:** for at most K attempts, draw a *fresh independent uniform* t-plane T from all N public planes (with replacement), test Gate; stop upon the first Gate success, run the seeded support solver once, and check the full verifier. A failed seeded solver does not trigger another probe. This deliberately simple policy quantifies the precise effect of public gate postselection.

**Gate-and-continue:** sample K independent uniform t-planes; skip seeds failing Gate, run the original-verifier-gated residual solver on every passing seed, and stop on the first accepted output. The first accepted L need not equal H. The probability of detecting *at least one sampled seed whose solver would output H*, disregarding any earlier accepted different witness, is a convenient auxiliary event, **not** an assertion that the real output equals H.

Neither algorithm can steer its next seed based on earlier rank values other than stopping; such a tensor-adaptive selection policy is outside the scope of the uniform-seed bound.

## 2. Exact fixed-tensor stopping law and the annealed/quenched distinction

**Theorem 1 (exact first-gate-stop H-recovery).** On a **fixed** public (A,H), if G>0 the probability that First-gate-stop returns the original sampled H within K probes is exactly
\[
\boxed{p_H^{\rm first}(K\mid A,H)
={X\over G}\left(1-\left(1-{G\over N}\right)^K\right).}
\]
If G=0 it is zero (then necessarily X=0). Thus the full-source probability is the **expectation of this nonlinear ratio**, not a ratio of first moments:
\[
\boxed{P_H^{\rm first}(K)
=\mathbb E_{\rm planted}\left[
{X\over G}\left(1-\left(1-{G\over N}\right)^K\right)
\,\mathbf1_{\{G>0\}}\right].}
\]
For unlimited probes, its eventual H-recovery probability is
\(\mathbb E[(X/G)\mathbf1_{\{G>0\}}]\);
if G>0, the expected number of raw public probes until the first gate hit is **N/G**, and if G=0 it never hits. No unconditional finite expectation of that waiting time follows just from a positive \(\mu_G\).

**Proof.** For fixed A every fresh trial hits any passing seed with probability G/N and a seed in X with probability X/N. The disjoint event that the first gate hit occurs at attempt s+1 and is H-recovering has probability \((1-G/N)^s X/N\). Sum s=0,...,K-1, with the G=0 convention. Stopping on a wrong passing seed can still produce an *other* verifier-accepted witness, but never the sampled H, because every lifted witness contains its seed. QED.

**Theorem 2 (what the old first moment really says).** Draw **one** independently uniform T before inspecting A, and reveal only the gate bit. If that bit is 1, then
\[
\boxed{\Pr[\text{its support solver returns }H\mid\mathrm{Gate}]=
{\mu_X\over\mu_G},\quad \mu_G>0.}
\]
This is a marginal probability for the **single sampled seed**; it is not the probability of H recovery from repeated first-gate-stop on one fixed A. The same ratio applies to independent new (H,A,T) instances conditioned on gate passage, but *not* to repeated T probes that reuse a fixed A.

**Proof.** For uniform T independent of A and H, the joint probability of its belonging to X is \(\mathbb E[X/N]=\mu_X/N\), while the gate probability is \(\mu_G/N\). Divide. QED.

**Counterexample showing why the moments are insufficient.** Consider hypothetical gate/true-solver configurations with N=4, M=1 (these are abstract probability-space examples, not asserted to arise from the planted source). Ensemble A has (G,X)=(2,1) always. Ensemble B has (G,X)=(1,1) half the time and (3,1) half the time. Both have \(\mu_G=2,\mu_X=1\) and the *same independent-one-seed* conditional H recovery 1/2. But unlimited first-gate-stop succeeds with probabilities 1/2 and 2/3, respectively; with K=3 probes the exact values are 7/16 and 29/64. Thus \(\mu_X/\mu_G\) cannot replace \(\mathbb E[X/G]\).

**General finite-moment bounds, requiring no false independence.** Let
\[
f_K(g)={1\over N}\sum_{s=0}^{K-1}(1-g/N)^s,
\]
which is nonincreasing for 0<=g<=N. Then \(P_H^{\rm first}(K)=\mathbb E[Xf_K(G)]\), and for any real 0<B<=N, since X<=M and Markov gives \(\Pr[G>B]\le\mu_G/B\),
\[
\boxed{P_H^{\rm first}(K)
\ \ge\ f_K(B)\bigl(\mu_X-M\mu_G/B\bigr)_+.}
\]
The bound can be weak or zero; it is a genuine *source-valid* lower bound, rather than an unjustified self-averaging assumption. For the chance of hitting **some** gate in K trials, Jensen's inequality instead yields the upper bound
\[
\Pr[\text{gate hit by }K]
=\mathbb E[1-(1-G/N)^K]
\ \le\ 1-(1-\mu_G/N)^K,\quad K\ge 1.
\]
Consequently the expected public passing count is **not** a high-probability existence or efficient-sampling theorem.

## 3. Restricted uniform-probe query lower bound, including the any-witness target

Let \(M/N\) denote the exact probability that an independent uniform public t-plane is genuinely contained in H. This quantity is independent of the original tensor and of the H-prior.

**Theorem 3 (uniform-seed-only no-acceleration statement).** Consider **any** algorithm which makes at most K independent uniform public t-plane draws with replacement, may compute arbitrary polynomial-time public gates/quotients for those planes, and whose only accepted output is a lifted d-plane **containing at least one of the sampled planes** and passing the *full original verifier*. The algorithm may stop early and may choose which of its sampled seeds to complete based on the entire published tensor, but its proposed t-planes must be independently uniform rather than tensor-adaptively biased. Then
\[
\boxed{\begin{aligned}
\Pr[\text{algorithm returns the sampled }H]
&\le 1-(1-M/N)^K\le KM/N,\\
\Pr[\text{algorithm returns any verifier-accepted }L]
&\le \min\{1,\ 1-(1-M/N)^K+\beta\}.
\end{aligned}}
\]
Here \(\beta=\mathbb E_{\rm planted}\#\{L\ne H:\dim L=d,\ L\text{ satisfies the original verifier}\}\) is the exact nonnegative wrong-witness first moment from [the preceding any-witness calibration](F0-planted-ti-any-witness-success-calibration.md); the bound is valid for any independent H-prior. Thus if \(\beta=o(1)\), attaining fixed positive **original any-witness** probability \(\epsilon>0\) through this restricted uniform-seed-only procedure requires
\[
\boxed{K\ \ge\ (\epsilon-\beta)_+\,{N\over M}.}
\]
This is only a **sampling/query lower bound for the explicitly restricted algorithm class**. It is not a computational lower bound for tensor-adaptive seeds, public greedy flags, global polynomial-system solvers, or any quantum adversary.

**Proof.** If the algorithm outputs H by lifting a sampled T, at least one probed T must lie inside H. Conditional on every H, all K pre-generated candidate planes are independent uniform, so the exact probability that any lies in H is \(1-(1-M/N)^K\). This event does not become more likely by applying a public rank gate *after choosing* those uniform planes. If the algorithm instead outputs L≠H, the honestly generated A must admit some other verifier-accepted d-plane; this source event is at most \(\beta\) by Markov's inequality, independent of how the attacker searches. Combine by union bound; use \(1-(1-x)^K\le Kx\). QED.

**Sparse scaling.** For fixed q and \(d/n\to\alpha\in(0,1/2)\), \(m\asymp n/\log n\), and the shorter residual-seed choice \(t=(c-d)/m+O(1)\), Gaussian-product counting yields
\[
\log_q(N/M)=ct+o(n^2/m)
={c(c-d)\over m}+o(n^2/m).
\]
Hence this **restricted nonadaptive-uniform-plane strategy** requires \(q^{c(c-d)/m+o(n^2/m)}\) raw public plane probes to have constant any-witness success when \(\beta=o(1)\). At \(\alpha=1/3\), its leading q-exponent coefficient is **2/9** of \(n^2/m\), versus the prior **1/6** upper exponent for the actual tensor-dependent public greedy-flag+residual attack. This gap is precisely why a polynomial public gate does not automatically reduce the expensive *seed generation* exponent; the greedy algorithm already exploits public isotropy to bias how seeds are generated. No general lower bound for that greedy algorithm follows.

## 4. Rank-gate vacuity at the minimal residual boundary

**Lemma (parity barrier).** Since every alternating form on a D-dimensional vector space has even rank at most \(2\lfloor D/2\rfloor\), the residual test \(\operatorname{rank}(\bar A_i)\le2\ell\) is **automatically true for every quotient form** whenever \(D=u+\ell\le2\ell+1\), equivalently \(h=u-\ell\le1\). In the applicable inversion regime \(h>0\), the boundary case \(h=1\) therefore makes **the entire residual-rank gate vacuous beyond isotropy and full-row contraction**.

For \(h\ge2\) the residual-rank gate can genuinely exclude public false seeds, but it remains only a **necessary** condition for the original seeded support reconstruction, not an accepting-witness certificate. This elementary parity observation holds in characteristic two too (alternating means zero diagonal).

## 5. Exact GF(2) check, not an attack benchmark

Re-use the independent finite counting control from PR #257: q=2, n=10, d=c=5, m=2, t=2, so \(N=174251,M=155,\ell=1,u=3,h=2\). The previous exact gate count is
\[
\mu_G={3898666485\over262144}\approx14872.23238.
\]
For **one precommitted genuine T**, the full-row event occurs with \(p_{\rm row}=9765/16384\). Each of the two independent residual 1-by-3 rows must be nonzero and have distinct projective directions to make the support intersection zero: 7*6 of 8*8 pairs, so \(p_{\rm supp}=21/32\). Hence
\[
\boxed{\begin{aligned}
\mu_X&=155\cdot{9765\over16384}\cdot{21\over32}
={31785075\over524288}\approx60.62522,\\
\Pr[\text{one uniform seed returns }H]
&={\mu_X\over174251}
={146475\over421003264}\approx0.00034792,\\
\Pr[\text{solver returns }H\mid\text{one uniform seed passes gate}]
&={\mu_X\over\mu_G}={35\over8586}\approx0.00407640.
\end{aligned}}
\]
The 0.4076% conditional solver-H rate is **not** the earlier 0.6212% conditional true-seed probability \(80/12879\): a true seed can fail the residual support-intersection certificate. Neither conditional number determines success after many probes on one fixed tensor.

These are exact rational **scratch calculations**, not full honest-tensor enumeration, committed execution tests, independent experimental security rates, source concentration, new A-ID, or demonstrated runtime gains.

## 6. Decision and next research gate

**Negative finding:** filtering *independently uniform already-probed seeds* cannot beat the \(N/M\) raw-probe scale for the restricted lifted-witness search when wrong accepted witnesses are rare. Rank-gate first moments do not justify substituting an annealed posterior for fixed-key gate-selected seeds; near the \(h=1\) threshold, the residual rank gate has no discriminating content at all.

**Constructive opening:** the existing greedy public isotropic-flag algorithm is outside this lower-bound class and already enjoys a better leading upper exponent. A genuinely new speedup must change the publicly generated seed **distribution** toward accepting-witness-containing planes at lower total cost, or derive credible per-tensor counts/concentration using joint seed statistics—not merely add a post-hoc gate to independent uniform proposals. Any such algorithm must continue using the entire original source, all published slices, and the unchanged any-witness verifier.

No N1-60/F0-K/A-ID allocation, security assumption, PQ/KEM/PKE/OWF, experiment, README growth, or stage-registry change. **GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD; HEPMR BENCHMARK ONLY.**
