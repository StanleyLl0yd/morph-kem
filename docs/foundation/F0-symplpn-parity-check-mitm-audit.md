# F0: exact sympLPN source, parity-check quotient, and paired MITM

**22 October 2026. Analytic attack-cost screen of existing literature, not a new cryptographic assumption, attack ID, KEM candidate or original security proof.** GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD; planted-TI FROZEN. No executable tests or parameter recommendations.

## Original problem and source provenance

Lu, Poremba, Quek and Ramkumar, [arXiv:2603.19110v2, 6 October 2026](https://arxiv.org/html/2603.19110v2), Definition 3.6: decision sympLPN(k,n,p), 1<=k<=n, samples a **uniform full-rank isotropic** A in F2^(2n by k), uniform x in F2^k and independent depolarizing Pauli-pair errors e with nonzero probability p per physical pair (p/3 per nonzero label), and asks to distinguish (A,Ax+e) from (A,u) for independent uniform u in F2^(2n). Its PKE hybrids explicitly encounter **k=n and k=n-1**. Search for arbitrary (x',e') satisfying Ax'+e'=z, without any error restriction, is trivially solved by (0,z) but is NOT the paper's decision problem.

The paper, sections 2.2 and 2.5-2.6, discusses standard and pair-aware information-set decoding (ISD). A 2^O(sqrt(n)) low-noise ISD estimate is discussed for classical LPN; the authors expect related tailored sympLPN attacks and describe generic bounds as 2^O-tilde(sqrt(n)). Consequently the 2^O(sqrt(n) log n) exhaustive-support gate in the preceding [intake](F0-external-symplectic-noise-exponential-intake.md) is mathematically valid but **not** a claim to best known generic complexity. The elementary MITM below is also NOT a novel or strongest attack.

## Public quotient: k=n is special

For ANY full-column-rank A (isotropic or not), public elimination gives Q of rank (2n-k), satisfying QA=0 and ker(Q)=im(A). For any z,e':

    (exists x': Ax'+e'=z) iff Qe'=Qz.

For isotropic **k=n**, with nondegenerate symplectic matrix J, Q=A^T J has rank n and ker(Q)=im(A). At **k=n-1**, A^T J has just n-1 rows, whereas a full parity check needs n+1 rows; the symplectic shortcut alone is INSUFFICIENT and may falsely accept error candidates. All bounds below use the **full** Q and hold for both paper PKE dimensions.

## Exact two-list syndrome search

Partition n physical error pairs (not individual binary coordinates) into L,R of sizes mL=floor(n/2), mR=ceil(n/2). Define B(m,t)=sum_{j=0}^{min(m,t)} binom(m,j)*3^j. For each Pauli error a supported on L of weight at most tL, store ONE a keyed by Q a. For each b supported on R of weight at most tR, check key Qz+Qb. On a hit, e'=a+b satisfies Qe'=Qz, and Gaussian elimination recovers x' with Ax'=z-e'. Retaining one representative per syndrome is enough: **any** collision is an accepted pair. Stop after the first hit.

For every fixed A,z, worst-case time <=(B(mL,tL)+B(mR,tR))*poly(n) and memory <=B(mL,tL)*poly(n), not the product-size all-pairs enumeration. This tests whether the original z admits an error within the **modified** left/right sparse witness thresholds. It also yields a distinguisher for the **unchanged original** structured-versus-uniform decision source.

**Honest acceptance lower bound:** the planted half-weights are independent Binomial(mL,p) and Binomial(mR,p), so

    Pr_structured[accept] >= BinCDF(mL,p,tL)*BinCDF(mR,p,tR).

Other accepted pairs can only increase success; equality is NOT asserted.

**Uniform-null false-positive upper bound:** Q u is uniform in F2^(2n-k), conditioned on EACH fixed full-rank A. A union bound over candidate pairs yields

    Pr_null[accept|A] <= min(1,B(mL,tL)*B(mR,tR)*2^(-(2n-k))).

No pairwise independence or disjoint-coset hypothesis is used.

At p=c/sqrt(n) (c>0 fixed), t_i=min(m_i,ceil(2*m_i*p)), and n sufficiently large, binomial Chernoff bounds yield honest acceptance >=(1-exp(-mL*p/3))*(1-exp(-mR*p/3))=1-exp(-Omega(sqrt(n))). Each list has log2 B(m_i,t_i)=O(sqrt(n)*log n); the total time remains 2^O(sqrt(n)*log n)*poly(n) and null bound is 2^(-(2n-k)+O(sqrt(n)*log n)). In the leading coarse support-count term, the two half-list sizes are smaller than enumeration of all errors of total weight tL+tR, at the cost of exponential memory; the big-O class remains unchanged. At k=n the leading null exponent is -n; at k=n-1 it is -(n+1). **There is no polynomial break, PKE contradiction or proof of post-quantum hardness.**

## External exponent-equation proof access gate

Trey Li, [*Multivariate exponential equations with unknown coefficients*, DOI 10.3934/amc.2026001](https://doi.org/10.3934/amc.2026001), does publish author claims concerning worst/average-case hardness, reductions and traps, but the publisher's HTML full-text link redirected to a login/access page during this checkpoint. No independent proof-level review or original bitlength/quantifier audit is claimed. Any exponent-equation source remains **EXTERNAL HOLD**.

**Disposition:** both are existing mathematical leads/comparators. No admitted independent MORPH Field 15, unconditional strict-polynomial honest search source with full any-witness verifier, candidate parameters, experiments or scheme. Research-only 80/20 continues.
