# F0: published MESS exact multiplicative source - character projection and quantum-log gate

**22 October 2026. Independent analytic screening of a special subclass of an already published problem. Not a claim that Trey Li's full parameter families or security proofs are broken, no original cryptographic foundation and no benchmark.** GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD; planted-TI FROZEN; no new A-ID/N1/Field15/implementation.

## 1. Original-source fidelity / evidence limits

Trey Li, [*Multivariate exponential equations with unknown coefficients*, Advances in Mathematics of Communications 22 (2026), pp. 75-105, DOI 10.3934/amc.2026001](https://doi.org/10.3934/amc.2026001), published online 27 November 2025. The publisher's accessible abstract claims MESS hardness, reductions and applications. An indexed public author-paper excerpt (ResearchGate mirror, not an independently verified official full proof) includes section 4.1's *Search-MESS/Decision-MESS* oracle source, Theorem 4.5, Lemmas 4.6-4.7. These excerpts are **not** a complete independent audit of the author's stated hardness proofs, parameter restrictions or concrete constructions.

For the explicit **integer prime-modulus subclass**, let q be an odd prime, G=F_q^* (multiplicative group), public L an **explicitly enumerated polynomial-size set** of nonzero coefficient residues in G, and x drawn once from an explicitly chosen domain Z^n. One independent original-source oracle sample is

    a=(a_1,...,a_n) uniform G^n,
    xi sampled from public L according to its stipulated law,
    b=xi * product_{i=1}^n a_i^(x_i) mod q.

The SAME hidden x is used for m independent oracle samples. Decision-MESS compares this source to uniform independent (a,b) in G^n x G. **Do not** replace multiple-oracle samples by a single equation, choose arbitrary xi outside L, or assume L's distribution induces uniform discrete-log noise if collisions occur. For the conditional theorem below specialize Z={0,1}, a domain explicitly used in the paper's search-to-decision discussion. Honest-source generation and verification use modular exponentiation and membership in public L, assuming the required q and all members of L are explicitly presented with polynomial total encoding length. The cost of generating qualified parameters remains a separate gate.

The paper's native Search-MESS requests x. A source-preserving MORPH **full public** verifier for m transcripts can check any proposed x' in Z^n by calculating the implied coefficient xi'_j=b_j*(product_i a_(j,i)^(x'_i))^(-1) in G and checking xi'_j belongs to public L for every j. This is a verifier of the actual published sample equations, not a changed approximate/noise-truncated relation. It accepts the original planted x on every honest sample.

## 2. Exact character-projection polynomial special-case attack

Let chi:G->{+1,-1} be the quadratic character chi(u)=u^((q-1)/2) mod q (interpreted as +/-1). It is publicly computable in polynomial time by modular exponentiation.

**Precondition P (checkable from q,L):** every possible xi in the ORIGINAL coefficient support L has **the same** quadratic character gamma in {+1,-1}. This is a *restricted parameter subset*, not a claim that the paper's concrete qualified samplers satisfy P. Nonzero xi mod q is required.

Put bit(+1)=0 and bit(-1)=1. For each original transcript row j, compute

    M_(j,i) = bit(chi(a_(j,i))) in F2,
    y_j = bit(chi(b_j)/gamma) in F2.

By multiplicativity and P, **for every planted x**:

    y_j = sum_i M_(j,i) * (x_i mod 2)  (mod 2).

Because the a_(j,i) are independent uniform in G, M has independent uniform F2 entries. With m=n+lambda original independent oracle samples and Gaussian elimination:

- **Original search for Boolean x:** rank(M)=n except with probability at most 2^(n-m)=2^(-lambda), since for any fixed nonzero v, Pr[Mv=0]=2^(-m), and a union bound covers fewer than 2^n nonzero v. When full rank, solve exactly for x in F2^n; because x_i in {0,1}, this recovers the ORIGINAL secret, then the full m-equation verifier above accepts.
- **Original decision:** test whether Mx=y is consistent. It is ALWAYS consistent on the honest source (even without full rank). Under the unchanged uniform null, y is independent uniform in F2^m given M; probability that some x solves the projected system is at most 2^(n-m)=2^(-lambda), by a union bound over all 2^n candidate Boolean x. Therefore the test has one-sided false-positive bound 2^(-lambda), pointwise for every public q,L satisfying P.

All operations (Legendre symbols, Gaussian elimination and native witness checks) are **classical polynomial time in sample count and log(q)**. **No quantum discrete logarithms are required** for this specific character-collapse attack. It is a standard public-character projection, not new mathematics or a conclusion about the broad MESS framework. It **analytically rejects only** original Boolean-secret, finite-prime-modulus MESS subclasses meeting P. If P fails, the projected equations have coefficient-dependent binary noise; this proof does NOT remove it or imply a break.

## 3. Cyclic-group discrete-log comparator, not an unconditional break

For G=F_q^*, |G|=s=q-1, choose a generator g. Write alpha_i=log_g(a_i), beta=log_g(b) and eta=log_g(xi), all modulo s. Then the ORIGINAL MESS oracle equation becomes exactly

    beta = sum_i alpha_i*x_i + eta  (mod s),

where eta follows the *push-forward* of the original public xi distribution on L. The null b gives uniform independent beta. Thus finite cyclic MESS converts to a specifically distributed **noisy additive linear problem** (LWE-like) whenever logs are available. Its reverse map (alpha,beta)->(g^alpha,g^beta) is computable with modular exponentiation. Shor-type quantum discrete logarithms make the forward direction efficient in a standard finite cyclic group with suitable explicit representation and order. This observation and the corresponding conditional MESS/LWE reductions are already discussed by Li, Theorem 4.5; **do not present them as MORPH novelty**.

Crucially, the induced eta need not resemble *standard small-error* LWE. Neither the group identity nor efficient quantum logs solves the resulting noisy linear problem. An assertion that arbitrary published MESS is broken, or that generic LWE hardness transfers to an arbitrary chosen L, would be unjustified. A full security review still needs the precise coefficient and secret distributions, sample limits, group representation, original qualified-domain hypotheses, parameter-generation complexity and best classical/quantum algorithms.

## 4. Disposition

**P-subclass:** conditional, source-faithful classical POLYNOMIAL NO-GO for Boolean x, with explicit checkable public hypothesis and m=n+lambda samples. **All other parameter domains:** HOLD for independent full source/proof/quantifier review. The externally published MESS framework is *not* an independent new MORPH Field-15 mathematical foundation merely by adopting it. No launch of a cryptographic construction, no N1-60, no A-ID or empirical attack campaign.
