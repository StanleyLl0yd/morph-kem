# MORPH-F0: exact public inversion of iterated univariate permutation polynomials

**2026-10-22. Independent arithmetic-dynamics attack-first screen, ANALYTIC REJECT for the specified permutation-polynomial family.** This is classical finite-field algebra, not independent mathematical novelty, a candidate KEM, an average-case hardness result, or a cryptographic primitive. **GLOBAL NO NOMINATION**; H-A/H-B/H-C HOLD; D0 HOLD/DEFER; planted-TI FROZEN comparator; N1-60 unallocated.

## 1. Full original source and accepted-witness verifier

Let \(\mathbb F_q\) have an explicit effective representation and polynomial-time field arithmetic, and \(\log q\) be polynomial in the security parameter. An *unconditional polynomial-time honest generator* outputs an explicitly dense coefficient list for \(f(X)\in\mathbb F_q[X]\), of polynomial degree \(1\le d\le\mathrm{poly}(\lambda)\), and a public iteration count \(1\le T\le\mathrm{poly}(\lambda)\). Its declared support **consists entirely of polynomials that induce permutations of \(\mathbb F_q\)**; there is no secret-dependent sampling filter or after-the-fact rank conditioning. It then selects \(s\in\mathbb F_q\) from any specified polynomial-time conditional source and publishes
\[
P=(q,f,T,b),\qquad b=f^{\circ T}(s).
\]
The **complete original verifier** accepts any \(y\in\mathbb F_q\) with \(f^{\circ T}(y)=b\). The attacker sees all coefficients of f, q, T and b, **not** s. Evaluation is T times the public polynomial and is polynomial time; there is no exponentially expanded coefficient list for \(f^{\circ T}\).

There are concrete unconditional source families meeting the promise: for q=2^r, the public polynomial \(f(X)=X^2+a\) for any sampled \(a\in\mathbb F_q\) permutes the field because Frobenius squaring does; choose a and s with their explicit unbiased r-bit representation and choose a polynomially bounded T. This is an easy source to **attack**, not evidence of a hard family.

## 2. Deterministic public inverse without expanding f composed T times

**Theorem (full-public iterated-permutation section).** For **every** public image of the above generator and **every** source prior on s, the following deterministic algorithm outputs the **unique** originally accepted y in time polynomial in \(T,d,\log q\) and the field representation. Its success on the unfiltered honest source is exactly one.

Given a target \(z\in\mathbb F_q\), form the public polynomial
\[
p_z(X)=f(X)-z.
\]
In the quotient ring \(\mathbb F_q[X]/(p_z)\), compute \(u_z(X)=X^q\bmod p_z\) by binary modular exponentiation, using only \(O(\log q)\) modular polynomial multiplications (when d=1, the same formula works). Compute the **monic** public gcd
\[
\boxed{g_z(X)=\gcd(p_z(X),u_z(X)-X)
             =\gcd(p_z(X),X^q-X).}
\]
Since \(X^q-X=\prod_{\alpha\in\mathbb F_q}(X-\alpha)\) has every field element as a **simple** root and f permutes \(\mathbb F_q\), there is *exactly one* \(\alpha_z\in\mathbb F_q\) satisfying \(f(\alpha_z)=z\). Thus
\[
\boxed{g_z(X)=X-\alpha_z.}
\]
Read \(\alpha_z\) as the negative constant coefficient. This is a public **deterministic** inverse-step solver, no discrete logarithms, exponential polynomial expansion, random factoring, oracle access or planted-secret membership test.

Start at \(z_T=b\). For j=T,T-1,...,1 set \(z_{j-1}=\alpha_{z_j}\). Return \(y=z_0\) after evaluating the **entire original verifier** \(f^{\circ T}(y)=b\).

**Proof.** The polynomial gcd identity holds because reduction modulo p_z does not change its gcd with p_z. Finite fields split \(X^q-X\) into exactly the q distinct linear factors. The permutation promise makes the gcd precisely one linear factor, even if p_z has repeated roots in an algebraic closure or deg f is larger than q. Repeated squaring computes \(X^q\bmod p_z\) using time polynomial in degree d and \(\log q\); Euclid's gcd algorithm is polynomial in d and field arithmetic. Exactly T successive public inversions give a unique field preimage under \(f^{\circ T}\), and the full verifier passes. QED.

**Representation caveat:** d denotes **the degree of the public dense f**, not the degree of the expanded iterated polynomial \(f^{\circ T}\), which may be exponential in T. The theorem does not claim that an arbitrary exponentially large/succinctly represented single-step polynomial, an arbitrary **multivariate** polynomial permutation, or a rational map with partial-domain poles can be inverted by this one-variable gcd trick.

## 3. Exact equality to an unrestricted-uniform target law despite easy inversion

Suppose conditional on public (q,f,T) the honest s is **uniform in all \(\mathbb F_q\)**. Since \(f^{\circ T}\) permutes the finite field, b is also exactly uniform in \(\mathbb F_q\), *regardless of T*. Against a null distribution selecting the **same** public (q,f,T) and an independent uniform target b, the entire observable public-instance distributions coincide:
\[
\boxed{\operatorname{TV}(D_{\rm honest},D_{\rm null})=0.}
\]
Nevertheless the above public inverter wins with probability **one**; and for the uniform source the conditional entropy \(H(s\mid q,f,T,b)=0\), since s is uniquely determined. This is a decisive contrast to [the cochain gate](F0-cochain-public-section-null-distinction.md), where an exact planted-image membership test can have large statistical advantage. **Neither large nor zero planted/null statistical divergence implies original any-witness computational hardness.**

For a nonuniform conditional s-distribution the pointwise inversion theorem still holds, but the uniform-output/TV=0 corollary is **not asserted**.

## 4. Exact small-field checks and the nonpermutation failure boundary

Over \(\mathbb F_7\), \(f(X)=X^5+2\) is a permutation because \(x\mapsto x^5\) is an automorphism of the multiplicative group of order 6 (gcd(5,6)=1) and adding 2 translates the field. Its values on x=0,...,6 are (2,3,6,0,4,5,1). With T=3 and honest s=3, the public forward path is
\[
3\longmapsto0\longmapsto2\longmapsto6=b.
\]
The public polynomial gcd inverse steps from target 6 recover 2, then 0, then 3. The full verifier passes. This finite arithmetic check is **scratch only**, not a sampled crypto benchmark or committed code test.

**Essential nonpermutation counterexample:** Over \(\mathbb F_7\), let \(f(X)=X^2\), T=2, s=1, b=1. The honest original verifier is satisfiable. But from target 1 the first inverse step has **two** roots, 1 and 6. If an attacker chooses 6, there is **no** field square root of 6, so the next inverse step fails even though s=1 works. Therefore the permutation result does **not** imply that factoring each degree-d equation and choosing an arbitrary backward root suffices for nonbijective iterates. A branching/liveness analysis tied to the **actual honest source**, not a different random-mapping surrogate, is mandatory.

## 5. Established mathematical prior art and D1 decision

Finite-field root extraction by gcd with \(X^q-X\) and modular exponentiation is standard [Lidl–Niederreiter, *Finite Fields*, polynomial factorization chapter](https://doi.org/10.1017/CBO9780511525926.006) and [Stanford PBC finite-field polynomial root notes](https://crypto.stanford.edu/pbc/notes/ep/root.html). Polynomial dynamics/functional graphs over finite fields are a substantial mature research area: [Oliveira–Brochero Martínez, *Dynamics of polynomial maps over finite fields* (2022)](https://arxiv.org/abs/2201.00954); [Matera, *Inverting bijective polynomial maps over finite fields* (2006)](https://bicyt.conicet.gov.ar/fichas/produccion/en/2813900). Broader nonlinear/chaos-based cryptographic dynamics have well-documented caveats: [*On the use of dynamical systems in cryptography* (2024)](https://doi.org/10.1016/j.chaos.2024.114952). None of this yields a new independent MORPH foundation.

**D1 permutation-polynomial family: ANALYTIC REJECT.** The nonpermutation **arithmetic-dynamics** problem is *not automatically rejected*: source distributions, preimage branch viability, functional graphs, polynomial-system attack algorithms, parameter representation costs and quantum screens would require independent mathematics and positive Field-15 distinctness before any experiment. Label this *unselected* frontier **HOLD**, not a new cryptographic assumption. Do not respond to the no-go by merely increasing T or hiding polynomial coefficients. No new N1/F0-K/A-ID, primitive design, security level or numerical experiment campaign.
