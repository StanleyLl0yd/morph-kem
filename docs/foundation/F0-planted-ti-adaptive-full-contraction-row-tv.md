# MORPH-F0: adaptive full-row contraction oracle coupling and its one-intersection boundary

**2026-10-20. Full-source mathematical information screen for a strictly restricted observer; GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.** This strengthens the oracle model of the [adaptive pair evaluations](F0-planted-ti-adaptive-oracle-span-tv.md) and [adaptive bivector probes](F0-planted-ti-adaptive-linear-bivector-probe-tv.md): a query now returns **all n pairing coefficients in every public slice**, not just the pairing of selected vectors. It does **not** model an adversary receiving the complete published matrices at the start. The original full any-witness verifier and unfiltered planted source are unchanged.

**External problem priority.** The planted totally-isotropic tensor relation, including the generic q^{O(n log n)} upper attack class, is from Liu, Qiao, Tang and Zhang, [*The planted tensor problem over finite fields: algorithms and cryptography*](https://arxiv.org/abs/2609.31256) (2026). Exterior algebra and Gaussian-intersection counting below are established mathematics; neither a new hardness assumption, quantum lower bound, nor positive Field-15 basis is claimed.

## 1. Exact honest source and full-row observation model

Let `V=F_q^n`, q any prime power (including characteristic two), `2<=d<n`, `c=n-d`, `m>=1`. Under the **null source**, all m alternating bilinear forms `A_i` are independent and uniform. Under the **unfiltered planted source**, choose a hidden d-plane `H` from a specified prior independently of the forms, and condition each of the independent uniform forms to satisfy `A_i|_{H x H}=0`. No rank postselection, rejection on observed data or substitute sampler is permitted.

The published object in the *real attack problem* is the **entire** tuple A, and its original full verifier accepts any d-plane L with `A_i|_{L x L}=0` for every i. This paper instead analyzes an explicitly **weaker oracle-only experiment**. A classical randomized observer is not handed A, but may adaptively query a vector `u\in V` and receive the ordered `m` full covector rows
\[
\mathcal O_A(u)=\bigl(A_1(u,e_1),\ldots,A_1(u,e_n);\ \ldots;\ A_m(u,e_1),\ldots,A_m(u,e_n)\bigr),
\]
in a fixed public basis `e_1,\ldots,e_n`. Every query reveals up to `mn` field elements. Later choices may depend arbitrarily on every earlier row, public parameters and private coins; the hidden H is **not** supplied. The full transcript records queries and replies.

An attacker can acquire all public matrices by querying n basis vectors, so no nontrivial security consequence should be expected when the query carrier approaches all of V.

## 2. Fixed-carrier exact distribution: one hidden intersection suffices

For any fixed k-plane `T\subseteq V`, let `\rho_T(A)` be the ordered full-row restriction of each `A_i` to `T\times V`. Put `S=T\cap H`, `j=\dim S`, and
\[
\boxed{\kappa_j=\dim(S\wedge H)
=j(d-j)+{j\choose2}=jd-\frac{j(j+1)}2.}
\]

**Theorem 1 (exact augmented-H total variation for fixed T,H).** Under the conditional-uniform original source,
\[
\boxed{
\operatorname{TV}\bigl(
\mathcal L_{\rm planted}(\rho_T(A)\mid H),
\mathcal L_{\rm null}(\rho_T(A))
\bigr)
=1-q^{-m\kappa_j}.}
\]

**Proof.** Write `E=\Lambda^2V`. An alternating form is a linear functional on E. The full rows on T correspond to restricting this functional to `K_T=T\wedge V\subseteq E`. The source condition requires annihilating `E_H=\Lambda^2H`. The exterior quotient `E\to\Lambda^2(V/T)` has kernel `K_T`, and the image of H in V/T has dimension d-j. Thus
\[
E_H\cap K_T=S\wedge H,
\]
of dimension `\kappa_j`. Under null, the row restriction is uniform over the complete dual `K_T^*`. Under the conditioned planted source, it is uniform on the subspace of `K_T^*` that vanishes on `E_H\cap K_T`, of codimension `\kappa_j`; surjectivity of restriction follows by extending a functional linearly from `K_T+E_H` to E. With m independent slices the codimension is `m\kappa_j`, and TV of uniform measure on a subspace of relative size `q^{-m\kappa_j}` against the ambient uniform measure is exactly `1-q^{-m\kappa_j}`. No restriction on characteristic. QED.

**Immediate distinction:** If `T\cap H=\{0\}`, the entire **vector-valued full-row observation** has *exactly identical* planted and null distributions even for a known fixed H. A single intersection point already introduces `d-1` scalar constraints per slice; this is **not** the two-intersection threshold governing queries restricted to pair evaluations *within T*.

## 3. Fully adaptive full-row transcript coupling

For a deterministic oracle observer (fix its random tape), let `T_{\mathrm{null}}` be the linear span of all vectors it would query along its actual run against an independent **unrestricted null tensor**. This carrier is a random subspace determined by the null tensor and the observer, but is **independent of a separately sampled hidden H**. Repeated/dependent queries count toward the query budget but do not increase its dimension.

**Theorem 2 (adaptive full-row carrier bound, any H prior).** For any classical randomized observer making at most Q full-row queries,
\[
\boxed{
\operatorname{TV}\bigl(
\mathcal L_{\rm planted}(\mathrm{transcript}),
\mathcal L_{\rm null}(\mathrm{transcript})
\bigr)
\le
\Pr_{H\sim\pi,\ A_0\sim\mathrm{null},\ \mathrm{coins}}
[T_{\mathrm{null}}\cap H\ne\{0\}].}
\]

**Proof (adaptive transcript rather than invalid postselection).** Fix the observer's coins and H. A complete consistent transcript fixes both the queried vectors and every corresponding full row. Its event is the affine linear event `\rho_T(A)=y` for its final carrier T: adaptivity does not impose additional constraints because the selected query sequence is a deterministic function of earlier recorded rows. If `T\cap H=0`, Theorem 1 says the affine restriction `\rho_T(A)=y` has **exactly the same probability** under the planted conditional source and null, for every consistent y. Thus the planted and null probabilities agree *pointwise on the set of safe transcripts*. The total masses of the unsafe complements then agree; outside the safe set their L1 difference is at most twice their common mass. The conditional TV is therefore at most the null probability of unsafe transcripts. Average over the observer's random tape and the independently chosen H, then discard H from the observed transcript by data processing. QED.

**No illicit fixed-T argument:** the theorem does **not** assume that the attacker's adaptive T is statistically independent of the null or planted matrices. Rather, it compares probabilities of complete transcript cylinders, using their actual final linear constraints. Independence of `T_{\mathrm{null}}` and H is asserted only because the **null** response source does not sample or depend on H.

### Exact adaptive transcript likelihood and hidden-H posterior

The preceding safe-cylinder proof admits a useful, stronger **pointwise likelihood identity** for **every** adaptive transcript, including carriers that intersect H. Fix the observer's coins, and let `τ` be any algebraically consistent, fully recorded transcript with carrier `T=T(τ)`. Write `K_T=T\wedge V`, `j_H=\dim(T\cap H)`, `\kappa_H=j_Hd-j_H(j_H+1)/2`. Let `\mathrm{Compat}_H(τ)=1` exactly when every observed full-row functional, regarded as an element of `K_T^*`, annihilates `\Lambda^2H\cap K_T`; otherwise it is zero.

**Theorem 3 (exact finite transcript likelihood, any prior).**
\[
\boxed{
\frac{\Pr_{\rm planted}[\tau\mid H,\mathrm{coins}]}
     {\Pr_{\rm null}[\tau\mid\mathrm{coins}]}
=q^{m\kappa_H}\,\mathrm{Compat}_H(\tau).
}
\]
Consequently for any discrete prior `\pi` on `Gr(d,V)`, the precise posterior in the oracle-only experiment is
\[
\boxed{
\pi(H\mid\tau,\mathrm{coins})
=
\frac{\pi(H)\,q^{m\kappa_H}\,\mathrm{Compat}_H(\tau)}
{\sum_{H'}\pi(H')\,q^{m\kappa_{H'}}\,\mathrm{Compat}_{H'}(\tau)}
}
\]
whenever the denominator is positive.

**Proof.** Consistency of `τ` forces a prescribed restriction of every alternating functional to K_T, a linear affine fibre; it also forces the adaptive query path, since future queries are already determined by the recorded previous rows. Under null this fibre has probability `q^{-m\dim K_T}`. Under the planted conditional-uniform source the fibre is empty unless all row constraints agree on the common subspace `\Lambda^2H\cap K_T`; if compatible, its probability is `q^{-m(\dim K_T-\kappa_H)}`. Their ratio is the displayed likelihood. Bayes' rule proves the posterior formula. QED.

The posterior is an **analyst's exact identity**, not a polynomial algorithm to enumerate H or an information bound on an attacker holding the complete public tuple. In particular, `T\cap H=0` gives factor exactly one; **tensor-adaptively chosen** unsafe carriers may have likelihood factors above one and must never be treated as independent probes. The previous *whole-transcript* TV bound remains valid without computing the posterior.

## 4. Sharp Gaussian intersection bound under uniform H

For this section only let H be **uniform** on `Gr(d,V)`. Conditional on any fixed `k`-plane T independent of H,
\[
\Pr_H[T\cap H=0]
=\frac{{c\brack k}_q q^{dk}}{{n\brack k}_q},\qquad
0\le k\le c.
\]
The exact intersection-dimension distribution is
\[
\Pr_H[\dim(T\cap H)=j]
=\frac{{d\brack j}_q{c\brack k-j}_q q^{(d-j)(k-j)}}{{n\brack k}_q}.
\]
Consequently, for every adaptive algorithm with carrier dimension at most `Q\le c`, Theorem 2 gives the **honest/unrestricted transcript TV bound**
\[
\boxed{
\operatorname{TV}(\mathcal L_{\rm planted}\mathrm{Tr},
\mathcal L_{\rm null}\mathrm{Tr})
\le 1-\frac{{c\brack Q}_q q^{dQ}}{{n\brack Q}_q}
\le \min\!\left(1,\frac{{d\brack1}_q{Q\brack1}_q}{{n\brack1}_q}\right).}
\]
For `Q>c` the displayed bound is replaced by the trivial 1.

**Proof.** Under the null run, the random carrier T is independent of uniform H, even though T was selected using all previous null tensor rows. Conditional on the realized carrier dimension k, its intersection probability depends only on k by GL-invariance, is monotone in k, and is at most the stated k=Q probability. For the elementary union bound, if `T\cap H\ne0` some projective line in T lies in H. Each of `{Q\brack1}_q` lines belongs to uniform H with probability `{d\brack1}_q/{n\brack1}_q`. QED.

For fixed q, `d/n\to\alpha\in(0,1/2)`, `c=\Theta(n)`, and `Q=O(\log n)`, the bound is `q^{-\Omega(n)}`. This is a **strong full-covector-row restricted-transcript indistinguishability statement**, but **not** an information-theoretic or quantum lower bound for someone who sees the **whole public matrix tuple**. The attacker can simply read n independent full rows when it has complete public inputs, and the intersection bound then ceases to be small.

### An exact augmented-H fixed-carrier control

If a **uniform k-plane** T is precommitted independently of H and A (not tensor-adapted) and the observer is *also* given the true H as an auxiliary analysis variable, the exact joint TV is
\[
\boxed{
\operatorname{TV}\bigl(
\mathcal L_{\rm planted}(H,T,\rho_T(A)),
\mathcal L_{\rm null}(H,T,\rho_T(A))
\bigr)
=\sum_j
\frac{{d\brack j}_q{c\brack k-j}_q q^{(d-j)(k-j)}}{{n\brack k}_q}
(1-q^{-m\kappa_j}).}
\]
The real observation `(T,\rho_T(A))` has TV **at most** this auxiliary-information TV. Do **not** confuse this exact augmented-H formula with exact real TV or with the adaptive result of Theorem 2.

## 5. Independent exact binary scratch controls (not an attack benchmark)

Fix GF(2), n=5, d=3, m=1, and H spanned by the first three coordinate vectors. Exhaust all `2^{\binom52}=1024` alternating full matrices; in the planted subset the three H-internal coefficients are zero. Count the distinct full contraction views (including row overlaps):

| Precommitted basis vectors of T | `j=\dim(T\cap H)` | Null view count | Planted view count | Exact TV |
|---|---:|---:|---:|---:|
| `e_4` | 0 | 16 | 16 | 0 |
| `e_1` | 1 | 16 | 4 | 3/4 |
| `e_1,e_4` | 1 | 128 | 32 | 3/4 |
| `e_4,e_5` | 0 | 128 | 128 | 0 |
| `e_1,e_2,e_5` | 2 | 512 | 64 | 7/8 |

An independent toy **adaptive** check over GF(2), n=4, d=2, m=1: query e1 first; inspect its full row, then query e2 if `A(e_1,e_2)=0`, else query e3. Enumerate all 35 hidden 2-planes and 64 unrestricted null full tensors, and all 1120 equally weighted planted pairs. The exact **real transcript TV** is `29/560`, while the null-run carrier-intersection upper bound is `19/35`; the inequality holds with slack, not claimed tight. These are pencil-and-paper/exhaustive **scratch controls**, not a committed executable attack, frozen source corpus, measured runtime or a claim of programmatic cryptanalysis.

## 6. Nonclaims and next falsification target

- **The full-row oracle is still weaker than publication of every coefficient.** Nothing proves computational hardness, information-theoretic closeness, polynomial inversion impossibility or quantum security for the original full-tensor search problem.
- **Nonuniform hidden-H priors** retain Theorem 2 with its explicit null-carrier intersection probability. The uniform-H Gaussian formula is **not** transferred to arbitrary priors that might reveal preferred directions.
- Neither the oracle transcript nor the augmented-H TV theorem is a public algorithm outputting a full-verifier accepted d-plane. No KEM/PKE/OWF/trapdoor, security level, source sampler, parameter nomination, new N1, F0-K, A-ID or positive Field 15 is introduced.
- The remaining attack-first problem is tensor-adaptive **global** algebraic extraction of an accepted witness using **all published rows**, without confusing the strict Q-row oracle coupling with a polynomial full-tensor inverse.

**Disposition:** EXACT FULL-ROW CARRIER LAW / ADAPTIVE RESTRICTED-ORACLE TV UPPER BOUND. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD; HEPMR BENCHMARK ONLY; N1-60 unallocated.
