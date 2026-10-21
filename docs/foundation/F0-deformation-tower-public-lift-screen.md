# F0: finite-local-ring lifting gate for public any-witness inversion

**2026-10-21. Analytic kill gate; not a candidate or novelty claim.** Track the [independent-mathematics pivot](F0-independent-foundation-pivot-2026-10-21.md). **GLOBAL NO NOMINATION**; H-A/H-B/H-C HOLD; no new N1/F0-K/A-ID and no implementation, measured sample, crypto security or OWF assertion.

## 1. Exact public problem, including the source

Let \(\mathbb F_q\) be a finite field in an effective polynomial-size representation, and let \(R=\mathbb F_q[\epsilon]/(\epsilon^k)\), \(k\ge2\). Assume that \(q,k,v,w\), the bit representations and field arithmetic have polynomial cost in the security parameter. A *public*, uniform polynomial-size arithmetic circuit \(F:R^v\to R^w\) may use additions, scalar constants and products; scalar coordinate extraction over \(\mathbb F_q\) converts matrix-valued/noncommuting word circuits to the same finite-dimensional statement, **if** all ambient-domain and verifier conditions are preserved.

The honest generator selects \(s\) by any specified polynomial-time distribution independent of the attack, publishes \(P=(F,F(s))\), and the **complete original verifier** accepts *any* \(y\in R^v\) with \(F(y)=F(s)\). There is no requirement that \(y=s\). This theorem concerns the entire affine-domain relation. For invertible-matrix or subgroup domains, additional domain tests and a proof of lift closure are necessary; merely verifying equations is not sufficient.

Write \(\bar F:\mathbb F_q^v\to\mathbb F_q^w\) for reduction modulo \(\epsilon\), and \(b=F(s)\). The hypothesis of the attack is a *public polynomial-time residue section* \(x_0=\sigma(\bar F,\bar b)\) such that \(\bar F(x_0)=\bar b\). This is a substantive assumption: no method for finding \(\sigma\) for an arbitrary polynomial map is asserted. Let \(J=D\bar F(x_0)\) be its \(w\times v\) formal Jacobian over \(\mathbb F_q\).

## 2. The public lifting theorem and exact fibre count

**Theorem (smooth-residue any-witness section).** If \(\operatorname{rank}_{\mathbb F_q}J=w\), then a deterministic polynomial-time public algorithm produces \(y\in R^v\) with \(F(y)=b\), starting solely from \((F,b,x_0)\). Exactly \(q^{(v-w)(k-1)}\) accepted lifts have residue \(x_0\). No assumption about the planted secret, its rank, its distribution beyond a valid public output, or uniqueness of the witness is needed.

**Construction.** Lift \(x_0\) to the constant-coefficient vector \(y_1\in R^v\). For \(j=1,\ldots,k-1\), maintain \(F(y_j)=b\bmod\epsilon^j\). Compute the public discrepancy
\[
 e_j=[\epsilon^j](b-F(y_j))\in\mathbb F_q^w.
\]
Solve the **public linear system**
\[
 J\Delta_j=e_j,\qquad \Delta_j\in\mathbb F_q^v,
\]
and set \(y_{j+1}=y_j+\epsilon^j\Delta_j\). At the end, run the **full original verifier** \(F(y_k)=b\) and output \(y_k\) only if it accepts.

**Proof.** For any polynomial circuit, including products of noncommuting matrices after vectorization, the square-zero quotient \((\epsilon^j)/(\epsilon^{j+1})\) gives the exact first-order identity
\[
 F(y_j+\epsilon^j\Delta)=F(y_j)+\epsilon^jJ\Delta
 \pmod{\epsilon^{j+1}}.
\]
All terms containing at least two perturbation factors vanish because \(2j\ge j+1\) for \(j\ge1\); coefficients of the derivative reduce to those of \(\bar F\) at \(x_0\). Full row rank makes every right-hand side solvable. Induction produces a full lift, which passes the original verifier. Each stage has exactly \(q^{v-w}\) different linear solutions, and distinct sequences of coefficient choices yield distinct final vectors, proving the exact fibre count. Circuit evaluation, differentiation (or finite-difference linearization of each product gate), coefficient arithmetic and Gaussian elimination are polynomial in circuit size, \(k,v,w,\log q\). QED.

**Honest-source corollary.** If a public residue section with full-row Jacobian exists on a set of complete honestly generated public instances of measure at least \(1-\delta\), the public original-verifier adversary succeeds with probability at least \(1-\delta\) over the *unfiltered* honest distribution. If it exists on every valid output, inversion succeeds on every output. A high-entropy planted secret or many higher \(\epsilon\)-coefficients **cannot** rescue this specified relation. These are upper-attack results, not hardness claims.

**Noncommutative scope.** For matrix-word observations \(F:(M_a(R))^v\to(M_a(R))^w\), vectorize matrix entries, replace \(v,w\) above by \(va^2,wa^2\), and use the Frechet linearization of ordered products. The argument does **not** commute matrix factors. If the witness is constrained to invertible matrices, an invertible residue remains invertible under nilpotent lifting, but *other* promised restrictions require a separate proof.

## 3. Why dropping the rank hypothesis is invalid

Over \(R=\mathbb F_2[\epsilon]/(\epsilon^2)\), take the ordinary scalar map \(F(x)=x^2(x-1)\) and the *honestly reachable* target \(b=\epsilon=F(1+\epsilon)\). Both \(x_0=0\) and \(x_0=1\) solve \(\bar F(x_0)=0\). At \(x_0=0\), \(D\bar F(0)=0\), and **no** lift \(x=\epsilon a\) satisfies \(F(x)=\epsilon\) (indeed its image is zero). At \(x_0=1\), \(D\bar F(1)=1\), and \(x=1+\epsilon\) is a lift. Thus a public field-level section returning an *arbitrary* root need not lift even when an honest full-ring secret exists. A singular Jacobian is **not evidence of hardness**: a different residue section, branching, or a public normal form may still find another witness.

## 4. Established mathematics and boundary of contribution

This lifting calculation is an elementary instance of **multivariate Hensel lifting/formal smoothness**, not a newly discovered cryptographic assumption. Sources: [Grochow, *Multivariate Hensel Lifting Without Assuming as Many Variables as Equations* (2025)](https://doi.org/10.1080/00029890.2024.2440297); [Stacks Project, formal smoothness and infinitesimal lifting](https://stacks.math.columbia.edu/tag/02GZ); [Kamche–Kalachi, systems of equations over finite commutative rings (2024/2025)](https://link.springer.com/article/10.1007/s00200-024-00652-8). The separate [Grochow preprint](https://home.cs.colorado.edu/~jgrochow/hensel-notes.pdf) explicitly treats rectangular Jacobians. No priority is claimed for the theorem, proof technique or extension to coordinatewise polynomial maps.

This screen **does not** prove easy inversion when the residue problem is hard, when the public section cannot be found, when the selected root is singular, for arbitrary noncommutative rings with no effective coefficient filtration, for compressed implicit circuits with infeasible evaluation, or for a domain not preserved by the correction steps. Failure of this sufficient attack test is not positive Field-15 evidence.

## 5. First independent-basis research gate (not an admitted proposal)

**Working question D0, HOLD:** Can an explicitly specified, source-faithful, *singular* finite-algebra deformation or obstruction relation (rather than a smooth nilpotent tower) satisfy the complete public any-witness interface without collapsing to a known polynomial system, tensor/algebra isomorphism, gauge quotient, group synchronization, polynomial ring Hensel section, or classical average-case assumption?

Before implementation or a new stage: write a concrete unconditional polynomial sampler and full original verifier; audit **every** residue root, not merely the planted one; identify public normal forms and fibre multiplicity; determine whether the obstruction is an independently established mathematical object or a repackaging of mature deformation/CSP theory; and provide **positive** literature evidence for Field 15. If any public full-verifier section survives, **REJECT**, preserving the result. If the interface or novelty remains undefined, **HOLD**, not READY or a cryptographic primitive.

**Disposition:** exact public-smooth-lift **NO-GO** under specified hypotheses; singular-obstruction exploration **HOLD**. Zero new experiments or CI attack tests, no code, no new canonical stage; legacy TI kept as frozen comparator only.
