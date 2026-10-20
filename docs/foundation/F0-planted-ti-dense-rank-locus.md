# MORPH-F0: dense public point-contraction rank locus and black-box membership boundary

**2026-10-20. Full-public-tensor source-first geometry; GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.** This pass continues the [exact point-contraction rank laws](F0-planted-ti-point-contraction-rank-trap.md) on the **opposite, dense m>c boundary**. It shows that a polynomial public *point-membership predicate* can characterize the hidden plane with high probability, without claiming polynomial **search** for a member, an accepted d-plane, or a new cryptographic primitive.

**Prior art and positioning.** The planted totally-isotropic problem and a generic `q^{O(n log n)}` algorithm are external work by Liu, Qiao, Tang and Zhang, [*The planted tensor problem over finite fields: algorithms and cryptography*](https://arxiv.org/abs/2609.31256) (2026). The much denser `m>=M=\binom n2-\binom d2=\Theta(n^2)` **polynomial full-span public inverter** was already derived in [issue #208 comment 6215130941](https://github.com/StanleyLl0yd/morph-kem/issues/208#issuecomment-6215130941); this note does not re-claim it. The rank-locus observation below holds at `m=c+O(1)=\Theta(n)` for linear-size d, but does **not** bridge the extraction gap.

## 1. Unfiltered honest source, original any-witness verifier

Take an arbitrary prime power `q`, `V=F_q^n`, `2<=d<n`, `c=n-d`, `m>=1`. Choose hidden `H` of dimension d using **any prior**, independently of the forms. Conditional on H, publish the **full tuple** of m independent uniform alternating forms annihilating `H x H`. No restriction to a query oracle, no rejection sampling or rank postselection.

An attacker succeeds if it outputs **any** full-dimensional `d`-plane L with `A_i|_{L x L}=0` for every i, verified using the unchanged original public relation. Recovering the sampled H is not separately required. For a nonzero public vector v, the `m\times n` contraction `C_A(v)` has row i equal to `A_i(v,-)`.

Define the publicly decidable projective rank locus
\[
\mathcal R_c(A)=\{[v]\in\mathbf P(V)(F_q):
        \operatorname{rank}C_A(v)\le c\}.
\]
Each individual rank test uses only Gaussian elimination and is polynomial in public bitlength. **Computing the entire locus, or finding a point on it, is not asserted polynomial.**

## 2. Exact rank-locus first moment and conditional recovery theorem

**Theorem 1 (finite, arbitrary H prior).**

1. **Containment for every honest tuple:** `\mathbf P(H)(F_q)\subseteq\mathcal R_c(A)`. Every true contraction annihilates H, so its rows occupy the c-dimensional `H^\perp`.
2. **If m<=c, the predicate is vacuous:** `\mathcal R_c(A)=\mathbf P(V)(F_q)`, on *every* input, because a matrix with m rows has rank at most m.
3. **If m>c:** set `N=n-1` and
   \[
   p_{\le c}(q;m,N)
   =q^{-mN}\sum_{k=0}^c
       {N\brack k}_q\prod_{j=0}^{k-1}(q^m-q^j).
   \]
   Then, conditional on every fixed H,
   \[
   \boxed{\mathbb E[|\mathcal R_c(A)\setminus\mathbf P(H)|\mid H]
   =\left({n\brack1}_q-{d\brack1}_q\right)p_{\le c}(q;m,n-1).}
   \]
   In particular, with `C_q=\prod_{j\ge1}(1-q^{-j})^{-1}<4`,
   \[
   \boxed{
   \Pr[\mathcal R_c(A)\ne\mathbf P(H)\mid H]
   \le \min\left(1,\left({n\brack1}_q-{d\brack1}_q\right)
      C_q q^{-(m-c)(d-1)}\right).}
   \]
   The same bounds hold after averaging over **any** hidden-H prior.

**Proof.** The first two parts are pointwise rank bounds. For every fixed outside point `v\notin H`, independently of the sampled forms, the [two-population contraction theorem](F0-planted-ti-point-contraction-rank-trap.md) gives a public contraction with the exact rank distribution of a uniform `m\times(n-1)` matrix. Summing the finite rank probabilities through c and counting the `{n\brack1}_q-{d\brack1}_q` outside points proves the first moment; correlations between different v are irrelevant.

For the tail, put `N=n-1>c` and `u=\min(m,N)-c\ge1`. The uniform rectangular matrix kernel-plane union bound gives
\[
\Pr[\operatorname{rank}M\le c]
\le C_q q^{-u(|m-N|+u)}.
\]
If `m<=N`, then `u=m-c` and `|m-N|+u=N-c=d-1`; if `m>=N`, then `u=N-c=d-1` and `|m-N|+u=m-c`. In **both** cases the exponent is exactly `(m-c)(d-1)`. Union-bound the outside points to show that none remain, and average over the H prior. QED.

**Consequently**, on the high-probability event in Theorem 1(3), the *entire public set* of projective points passing the low-rank test is **exactly** the sampled `\mathbf P(H)`. This is an **identifiability** statement about an algebraic rank predicate, *not* an efficient procedure to find a satisfying point.

## 3. Sharp enough asymptotic screen, explicitly outside the conjectural sparse source

Fix q and suppose `d/n\to\alpha\in(0,1)`, `m=c+h` for a fixed positive integer h. The union bound exponent is
\[
\boxed{
\log_q \Pr[\mathcal R_c(A)\ne\mathbf P(H)]
\le (1-h\alpha)n+o(n)
}
\]
when the probability bound is nontrivial. Thus **if `h\alpha>1`**, `\mathcal R_c(A)=\mathbf P(H)` with source probability `1-q^{-\Omega(n)}`. For `\alpha=1/3`, `h=4` suffices for this asymptotic conclusion. We do **not** claim a converse or precise sharp threshold when `h\alpha<=1`.

This happens already at `m=c+O(1)=\Theta(n)`, far below the known `\Theta(n^2)` full-span polynomial inversion boundary. However the externally conjectural sparse regime is `d=\lceil n/C\rceil`, `C>=3`, `m=\lceil n/\log n\rceil`, where `m<c` for large n and **the same low-rank predicate is identically true for every nonzero public vector**. It is therefore **not** a polynomial attack on the conjectural source.

## 4. Even an exact point-membership oracle does not automatically provide a point

To separate identifiability from recovery, consider a *strictly weaker oracle-only experiment*: H is now **uniform** on `Gr(d,V)`. The algorithm sees only q,n,d and may adaptively query whether a **nonzero** chosen v lies in H; it does **not** see the published tensor, structural algebraic equations, or samples of vectors in H.

**Theorem 2 (membership-only lower bound).** Any randomized algorithm making at most Q membership queries, then proposing one nonzero vector `v_*`, finds a nonzero element of H with probability at most
\[
\boxed{
(Q+1)\frac{{d\brack1}_q}{{n\brack1}_q}
=(Q+1)\frac{q^d-1}{q^n-1}
<(Q+1)q^{-c}.
}
\]

**Proof.** Fix the algorithm's internal random tape. Follow its unique **all-NO response path**, giving a precommitted list of at most Q nonzero query vectors and its final nonzero output. If the real execution ever gets a first YES, that YES must occur at the same position on the fixed all-NO path, so H contains one of these listed query vectors. If all answers are NO and the final output succeeds, H contains the listed final vector. Every fixed nonzero vector belongs to a uniformly drawn d-plane with probability `(q^d-1)/(q^n-1)`. A simple union bound over at most Q+1 fixed vectors proves the claim. Average over random tapes. QED.

Hence constant membership-only success needs `Q=\Omega(q^c)` queries, but **this lower bound does not apply to a full-public-matrix attacker**. Full tensors may expose additional algebraic structure not captured by a YES/NO point-membership oracle. No claim that polynomial public inversion is impossible follows.

## 5. Independent finite arithmetic control (scratch only)

Evaluate the exact finite rank sum (not a source simulation) over GF(2) for `n=30`, `d=10`, `c=20`, `N=29`:

| m | Extra rows h=m-c | Exact expected number of false rank-locus points (decimal) | Conservative union bound using C_q<4 |
|---:|---:|---:|---:|
| 24 | 4 | approximately 0.05069761 | <0.0625 |
| 25 | 5 | approximately 0.00010221 | <0.00012208 |
| 26 | 6 | approximately 0.00000020279 | <0.00000023842 |

These are exact-rational finite Gaussian-binomial evaluations displayed as decimals, **not** observed experiments, generated planted tensors, implementation benchmarks or security-bit estimates. They illustrate why a finite-n claim must use the actual bound, not only the asymptotic `h>1/\alpha` slogan.

**Quantum boundary update (2026-10-20):** the separate [membership-only quantum hybrid theorem and dense full-public rank-locus quantum attack](F0-planted-ti-quantum-rank-locus-membership-separation.md) prove Ω(q^(c/2)) **only** for idealized hidden-H membership queries (uniform H), matched by standard Grover search. When this note's good rank-locus event holds, a reversible public rank predicate yields an original-verifier-accepted d-plane with O(poly*d*q^(c/2)*log(d/eta)) quantum work and unconditional honest-source probability at least 1-epsilon-eta. This is not polynomial for linear c, not novel amplitude amplification, and does **not** apply in the sparse m<=c regime where the predicate is vacuous.

## 6. Cryptanalytic meaning and next legitimate step

- **New publicly decidable geometric fingerprint:** with sufficiently dense publication, the rational points of the rank-<=c determinantal locus are precisely those of H with high honest-source probability.
- **Not a polynomial search algorithm:** the public rank oracle is polynomial **per supplied point**, but searching its exponentially sparse zero-locus might still be expensive. Writing down all relevant determinantal minors explicitly may itself require exponentially many generators; no claim that their ideal has been computed or solved efficiently.
- **No black-box extrapolation to the full tensor:** the membership-only lower bound restricts a strictly weaker information model, not real cryptanalysis of all matrix entries.
- **Sparse target untouched:** when `m<c` this particular low-rank predicate is vacuous and no newly hard distribution, trapdoor, quantum bound or public inverter emerges.
- **Next attack-first question:** for `m=c+h` and h large enough, does a **polynomial public algorithm** reconstruct the linear space H from the implicit determinantal linear-matrix-space description, despite the black-box membership barrier? Such an algorithm must be explicitly given, costed, and verified on the original unfiltered source and full any-witness verifier before classification.
- No N1-60 allocation, A-ID/F0-K, implementation, source sample, KEM/PKE/OWF, HEPMR expansion, or positive Field-15 claim.

**Disposition:** DENSE PUBLIC RANK-LOCUS IDENTIFIABILITY / MEMBERSHIP-ONLY LOWER-BOUND SEPARATION. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD; HEPMR BENCHMARK ONLY; N1-60 remains free.
