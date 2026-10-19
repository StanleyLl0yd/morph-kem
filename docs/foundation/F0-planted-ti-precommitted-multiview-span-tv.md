# MORPH-F0: joint TV bound for precommitted random local views with a bounded linear span

**2026-10-19. Analytical source-first follow-up to the [single random restricted tensor theorem](F0-planted-ti-random-restriction-exact-tv.md).** GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD. The new scoped result is a **joint observation** bound for multiple predetermined, GL-invariant local probes whose total linear span is small. The previously proved single-view exact conditional laws and t=2 exact TV retain priority. No novel hard relation, implemented attack, N1/F0-K stage, KEM/OWF/PKE/trapdoor or security claim.

**External planted tensor setting:** Liu, Qiao, Tang and Zhang, *The planted tensor problem over finite fields: algorithms and cryptography*, [arXiv:2609.31256v1](https://arxiv.org/abs/2609.31256). All dimensions and conditional distributions below refer to the **unchanged full honest source and unrestricted null source**, not a filtered source or substitute verifier.

## 1. Full original source and precommitted multi-view observation

Let V=F_q^n for any prime power q>=2, 2<=d<n, c=n-d, m>=1. Under null the m public alternating forms are independent and unrestricted uniform on V. Under planted choose **any unconditional** prior on a d-plane H and sample m independent uniform alternating forms annihilating H x H. Characteristic two uses zero-diagonal alternating forms. The complete original full-public-tuple verifier still accepts **any** rank-d Y with Y^T A_i Y=0 for every i.

Independently of H and of **all public alternating forms**, choose a finite tuple of t_i-dimensional subspaces

\[
\mathcal T=(T_1,\ldots,T_k)
\]

from any **GL(V)-invariant** joint distribution. The T_i may be correlated; the common case is independent uniform T_i. Define the public linear span S=T_1+\cdots+T_k, with random dimension u_S. The observed data consist of the tuple of subspaces and all restricted m-tuples (A_j|_(T_i x T_i)) for every i,j. The observation may be postprocessed arbitrarily, including by an unbounded algorithm. The selection of the T_i is **precommitted**: no T_i is selected based on observed public forms or their earlier restriction values.

## 2. Exact span-level augmented TV and real-view upper bound

The earlier [single-view lemma](F0-planted-ti-random-restriction-exact-tv.md#2-exact-conditional-laws-for-every-fixed-ht) states that for **any fixed** H,S the joint planted restriction A|_S is uniform among the alternating forms on S annihilating the subspace H cap S, while null A|_S is uniform unrestricted. If j=dim(S cap H), their exact m-slice TV is

\[
1-q^{-m\binom j2}.
\]

The tuple of individual restrictions is a deterministic function of the **entire** restriction to S and the public tuple (T_1,...,T_k). Couple null and planted by independently introducing an auxiliary H with the same prior into the null experiment. It is not observed by the real attacker.

**Theorem (joint precommitted observation).** Conditional on u_S=u, GL(V) invariance of the probe law ensures S is a **uniform u-plane**, independent of H and of the form tuple. Therefore, with the previously proved finite Gaussian intersection sum

\[
\Delta_{\rm aug}(n,d,u,m,q)
=\sum_j\frac{[d\choose j]_q[c\choose u-j]_q
 q^{(d-j)(u-j)}}{[n\choose u]_q}
 (1-q^{-m\binom j2}),
\]

the real public multi-view TV obeys

\[
\boxed{
\operatorname{TV}\big(\mathcal L_{\rm pl}(\mathcal T,(A|_{T_i})_i),
                      \mathcal L_0(\mathcal T,(A|_{T_i})_i)\big)
\le \mathbb E_{\mathcal T}[
   \Delta_{\rm aug}(n,d,u_S,m,q)].
}
\]

**Proof.** Condition on the public random tuple T and on the coupled auxiliary H. Both experiments have the same distribution of T,H (the probe tuple was sampled independently of the forms/H), and the full restriction on S has conditional TV exactly 1-q^{-m binom(dim(S cap H),2)} by the single-view lemma. Marginalizing the auxiliary H and discarding unobserved cross-evaluations between distinct T_i can only **decrease** TV (data processing). Condition on u_S=u: the distribution of S is uniform under the GL-invariant probe law. Average the already proved exact augmented bound over the classical Gaussian-binomial intersection distribution, then average over u_S. Nothing about the **full** tensor distribution is inferred.

If u_S<=u<=c=n-d **almost surely**, the elementary finite-field union bound from the single-view note applies at every possible span dimension and gives the simple uniform estimate

\[
\boxed{
\operatorname{TV}(\text{joint precommitted restricted views})
\le \frac49\,q^{-2(c-u)}.
}
\]

This holds for every unconditional planted H-prior and any number m of public forms. In particular for k independently uniform random 2-planes, u_S<=2k; if 2k<=c-s then even the **complete joint** collection of all their m scalar alternating evaluations has TV at most (4/9)q^(-2s). This is not an analysis of an adaptively selected sequence of arbitrary public subspaces.

## 3. Adaptive computations that stay inside one precommitted carrier

There is a separate safe corollary without requiring the **internal queries** to be nonadaptive. First draw one uniform u-plane S independently of H and of the tensor, with u<=c-s. Reveal S, and allow the observer to ask an arbitrary adaptive sequence of alternating-pair evaluations **using only vectors in S**, where later queries may depend on previously observed answers. Every response is a deterministic postprocessing of the complete restricted tuple A|_S, and the adaptive transcript is therefore also postprocessing of (S,A|_S) plus independent coins. Consequently the **same** (4/9)q^(-2s) TV bound holds for the entire adaptive **within-S** transcript.

This does **not** justify choosing or modifying S from public full-tensor invariants, or querying any vectors outside the initially independent S. “Adaptive within a predetermined random carrier” and “adaptive selection of the carrier using the tensor” are mathematically distinct observation models.

## 4. Why the invariance / independent-carrier requirement is essential

If H is itself uniformly distributed over all d-planes, then a fixed deterministic S selected independently of the published tensor has the same Gaussian intersection law; the single-S bound remains valid without randomizing S. **But this is not uniformly true for arbitrary planted H-priors.**

For example, with a known deterministic planted H=H_0, choose a **deterministic** S=H_0 of dimension d>=2. The planted restriction is identically zero, while null is uniform on the full alternating restriction space. Their exact restricted-view TV is

\[
1-q^{-m\binom d2},
\]

potentially nearly one **even when d<c**. The independent uniformly random S or GL-invariant multi-view sampling assumption prevents this public-prior alignment for an arbitrary H-prior. No claimed bound applies when an attacker discovers a correlated carrier from the published tensor.

## 5. Decision and interpretation

The only new scope beyond the single-view theorem is the rigorous **joint** TV control from a precommitted GL-invariant probe tuple with **bounded span**, plus its within-a-precommitted-carrier adaptive-query corollary. This is an information-theoretic limitation on a restricted local query model, **not** a statement that full tensors are indistinguishable, that optimally chosen Plücker kernels or public algebraic invariants fail, or that a full-original-verifier accepted d-plane is computationally hard to find. It is a finite-field linear-algebra fact rather than a new independent MORPH-R0 Field-15 foundation.

**Disposition: PRECOMMITTED MULTI-VIEW TV NEGATIVE CONTROL ONLY. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.** N1-60 unallocated, HEPMR BENCHMARK ONLY. No source code, datasets, README or stage-registry changes.
