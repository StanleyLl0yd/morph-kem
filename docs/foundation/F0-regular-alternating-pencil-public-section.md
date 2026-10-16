# MORPH-F0: regular alternating matrix pencils have a deterministic common-TI public section

**Date:** 2026-10-16. **Status:** scoped attack-first analytical screen / classical symplectic matrix-pencil machinery. **GLOBAL NO NOMINATION**, H-A/H-B/H-C HOLD, no new N1/F0-K stage, code, generated test cases, empirical success, cryptographic assumption, trapdoor, OWF, PKE or KEM.

## 1. Original any-witness relation and public regular-pencil certificate

Let \(K=\mathbb F_q\) be an effectively represented finite field, \(n=2h>0\), and \(A_1,\ldots,A_m\in K^{n\times n}\) be public **alternating** matrices: \(x^TA_ix=0\) for all \(x\), requiring zero diagonal also in characteristic two. The public rank-\(d\) verifier (for \(1\le d\le h\)) accepts exactly

\[
E(A_1,\ldots,A_m;d)
 =\{Y\in K^{n\times d}:\operatorname{rank}Y=d,\quad
                 Y^TA_iY=0\ \text{for ALL }i\}.
\]

The attacker wins with **any** accepted \(Y\), not the planted subspace. Suppose the **public span** of the matrices has dimension at most two and contains a **nondegenerate** alternating matrix \(C\). A basis \(A,B\) of this public span is computed by Gaussian elimination on the matrix entries. The condition is equivalent to the finite-field projective pencil \(\{\alpha A+\beta B:[\alpha:\beta]\in\mathbf P^1(K)\}\) containing a nonsingular member. It is a **sufficient publicly verifiable gate**, not asserted for all pairs.

To find such a member in polynomial time, check \(B\) and \(A+tB\). The polynomial \(f(t)=\det(A+tB)\) has degree at most \(n\). If any original-field combination is invertible, either \(B\) is invertible or \(f\not\equiv0\). For \(q\le n\), enumerate all \(q\) field elements; for \(q>n\), evaluate at any \(n+1\) distinct effectively enumerable elements, more than the number of roots of a nonzero degree-\(\le n\) polynomial. **This checks and finds regularity deterministically in polynomial time in \(n,\log q\)**, without enumerating an exponentially large field or passing to extension fields.

If the public span has dimension one and its generator is degenerate, the independent [single-form theorem](F0-one-alternating-form-rank-screen.md) handles **all feasible d**; span zero is trivially invertible. Hereafter suppose a nonsingular pencil member \(C\) has been found.

## 2. Constructive common Lagrangian for any two alternating forms with C nonsingular

Choose a second public alternating generator \(B\) so that \(A,B\) span the same space as \(C,B\). (If the span has dimension one, simply use \(B=0\).) On \(V=K^n\), let \(\omega(x,y)=x^TCy\) be the nondegenerate alternating form and define \(T=C^{-1}B\). Then

\[
 B(x,y)=\omega(x,Ty),\qquad
 \omega(Tx,y)=\omega(x,Ty).
\]

Thus \(T\) is \(\omega\)-self-adjoint. We additionally use the crucial fact \(B(x,x)=\omega(x,Tx)=0\), which is **not automatic from self-adjointness alone in characteristic two**.

**Cyclic isotropy lemma (all characteristics).** For any nonzero \(v\in V\), the cyclic \(T\)-stable subspace
\[
U_v=\operatorname{span}\{v,Tv,T^2v,\ldots\}
\]
is totally isotropic for **both** \(\omega\) and \(B\).

**Proof.** Self-adjointness moves powers between the arguments:
\(\omega(T^iv,T^jv)=\omega(v,T^{i+j}v)\).
If \(i+j=2a\) is even, this equals \(\omega(T^av,T^av)=0\) by alternation. If \(i+j=2a+1\) is odd, it equals \(\omega(T^av,T^{a+1}v)=B(T^av,T^av)=0\), again by alternation. Therefore \(\omega|_{U_v}=0\). Since \(TU_v\subseteq U_v\), \(B(x,y)=\omega(x,Ty)=0\) also for all \(x,y\in U_v\). No division by two, eigenvalue extraction or field-factorization is used.

**Invariant symplectic reduction.** Given a nonzero \(U=U_v\), compute \(U^{\perp_\omega}\) by linear equations. Since \(U\) is \(\omega\)-isotropic, \(U\subseteq U^\perp\). Self-adjointness and \(TU\subseteq U\) imply \(T(U^\perp)\subseteq U^\perp\); hence the quotient \(W=U^\perp/U\) inherits a **nondegenerate alternating** form and a well-defined self-adjoint operator \(T_W\). The descended pairing \(\omega_W(x,T_Wy)\) is alternating because it comes from the alternating \(B\) on \(U^\perp\). Its dimension is \(n-2\dim U<n\).

Repeat the cyclic construction recursively on \(W\), then lift the resulting invariant isotropic subspace back to its full preimage inside \(U^\perp\), adjoining \(U\). If the quotient is zero, stop. At every step the dimension drops by at least two; all quotients, cyclic spans and lifts are obtained by **polynomial-time finite-field linear algebra**. The final \(L\subseteq V\) is \(T\)-invariant, isotropic for both \(C,B\), and has dimension \(n/2=h\). This gives a **deterministic construction of a common Lagrangian**, including **characteristic two**, with no random choices or polynomial factorization.

Since every original slice \(A_i\) is a public linear combination of \(C,B\), every original restriction \(A_i|_{L\times L}\) vanishes. Output any \(d\le h\) linearly independent columns spanning a subspace of \(L\). Run the **entire original verifier** (rank, all m matrices) before returning. It always accepts whenever the public regular-pencil condition holds.

**Theorem (pointwise).** Every honest rank-\(d\), \(d\le n/2\), alternating tuple with public matrix-span dimension \(\le2\) and a **regular pencil over its original \(\mathbb F_q\)** has a **deterministic polynomial any-witness inverter**, irrespective of its planted basis, multiplicity of solutions, source distribution or number of syntactically repeated/linearly dependent observations.

## 3. Exact honest-source success probability for two independent planted forms

A separate stronger **source-dependent** statement gives an unconditional lower bound on the success probability of the preceding inverter for **two** slices, without conditioning the generator on the easy event.

Let \(n\) be even and \(1\le d\le n/2\). An honest source samples a full-rank planted \(d\)-space \(S\) in **any** way and, **conditionally on S**, samples \(A_1,A_2\) *independently and uniformly* from all alternating forms whose restrictions to \(S\) vanish. In a basis where \(S=K^d\oplus0\), each slice is

\[
 A=\begin{pmatrix}0&B\\-B^T&D\end{pmatrix},
 \quad B\gets\operatorname{Uniform}(K^{d\times(n-d)}),\quad
 D\gets\operatorname{Uniform}(\operatorname{Alt}_{n-d}(K)).
\]

The entries of \(B\) and of the strict upper triangle of \(D\) are independent and uniform. This source **never rejects based on matrix rank**, and every outcome has the planted full-original-verifier witness. Its exact conditional success calculations are invariant under any choice or distribution of \(S\).

Set \(k=n-d\), \(t=n-2d\) (even). The matrix \(A\) is invertible only if \(B\) has full row rank \(d\); otherwise a nonzero vector in \(\ker B^T\) lies in its radical. Conditional on full row rank, let \(H=\ker B\) have dimension \(t\). The block equations show
\[
 A\ \text{invertible}\ \Longleftrightarrow\
  D|_{H\times H}\ \text{is nondegenerate}.
\]
The restriction is **uniform** over alternating forms on \(H\), independently of \(B\), because restriction is a surjective linear map from the uniform full alternating-form space. Therefore the exact single-slice invertibility probability, for **every fixed planted S**, is

\[
p_{n,d,q}=
 \underbrace{\prod_{j=0}^{d-1}(1-q^{j-(n-d)})}_{\Pr[\operatorname{rank} B=d]}
 \ \underbrace{\prod_{i=1}^{(n-2d)/2}(1-q^{1-2i})}_{\Pr[D|_H\text{ symplectic}]}.
\]

Both products are \(1\) when their index sets are empty. The second is the classical exact fraction of nondegenerate alternating matrices in even dimension \(t\).

For any \(q\ge2\), each finite product is bounded below by its corresponding infinite positive product. Explicit **elementary constants**, independent of \(n,d,q\), are

\[
 \prod_{s\ge1}(1-q^{-s})
 \ge\frac12\!\left(1-\sum_{s\ge2}2^{-s}\right)=\frac14,
\]
\[
 \prod_{i\ge1}(1-q^{1-2i})
 \ge\frac12\!\left(1-\sum_{i\ge2}2^{1-2i}\right)
 =\frac{5}{12},
 \qquad p_{n,d,q}\ge\frac5{48}.
\]

The product lower bounds use \(\prod(1-a_i)\ge1-\sum a_i\) for \(0\le a_i\le1\); no asymptotic or empirical estimates are required. Since \(A_1,A_2\) are conditionally independent with the same p for every S,

\[
 \Pr_{\rm honest}[A_1\text{ or }A_2\text{ nonsingular}]
 =1-(1-p_{n,d,q})^2
 \ \ge\ 1-(43/48)^2=\boxed{455/2304}.
\]

On that event, one public matrix itself is a regular pencil member, and the **deterministic** §2 inverter passes both original slice equations. Trying other pencil combinations can only improve its success. Thus this is an **unconditional honest-output lower bound**, not an experimental frequency, a postselected source, or a universal success-one guarantee for all pairs.

**Strict generator distinction:** for \(q=2^e\) in an effective polynomial-basis binary encoding, a uniform field element is exactly e unbiased bits; for **any** worst-case-polytime full-rank-S sampler, sampling all B,D entries above is strictly worst-case polynomial and exactly uniform. The bound \(455/2304\) therefore applies **without a source-runtime caveat** in this fully specified binary-field honest model. For arbitrary non-power-of-two \(q\), the displayed probabilities describe the **ideal exact conditional-uniform law**; an implementation using variable-time rejection or a bounded approximate sampler needs separate running-time/TV accounting. The pointwise §2 inverter itself works for all fields, regardless.

## 4. Boundaries and existing mathematical context

- **Not covered:** odd-dimensional spaces (no nonsingular alternating member), pencils with no invertible member **over the original base field**, public matrix spans of dimension \(\ge3\), extra nonlinear/witness restrictions, or unknown slice correspondence. A failed regular-pencil screen is **not** positive evidence of hardness.
- **No extension** to the established many-slice planted-TI conjectural regime \(m=\lceil n/\log n\rceil\), \(d\approx n/C\), or to arbitrary tensor-isomorphism problems. In particular, a high-rank *individual matrix* does not mean the full tensor tuple is handled when the matrix-span exceeds two.
- **Direct exact prior art:** Goldstein and Guralnick, [*Alternating forms and self-adjoint operators*, Journal of Algebra **308** (2007), 330–349](https://doi.org/10.1016/j.jalgebra.2006.06.009), **Lemma 2.5** (cyclic invariant subspaces are isotropic), **Corollary 2.13** (two alternating forms, one nondegenerate, have complementary common isotropic halves), explicitly **over arbitrary fields including characteristic two**. The paper itself cites earlier Kaplansky, Klyachko and Gow–Laffey proofs. Thus the *existence theorem and cyclic method are established mathematics*, **not new MORPH discoveries**. Our scoped contribution here is to spell out a deterministic full-original-verifier any-witness procedure and independently derive the exact *specified honest-law* nondegeneracy probability and unconditional success bound.
- Further background: [Sanabria Malagón (2017)](https://arxiv.org/abs/1710.00697), whose cited theorem is stated for characteristic not two and must **not** be substituted for the arbitrary-characteristic Goldstein–Guralnick result; [symplectic canonical forms](https://magma.maths.usyd.edu.au/magma/handbook/text/318); [external planted tensor source](https://arxiv.org/abs/2609.31256).

**Decision:** regular two-dimensional alternating matrix spaces at \(d\le n/2\): **ANALYTIC EASY / POINTWISE REJECT**. The two-independent-slice source additionally has **provable constant original-verifier inversion success** (at least \(455/2304\)) under the exact conditional-uniform model, with an exact strict-PPT binary-field realization. **GLOBAL NO NOMINATION**, H-A/H-B/H-C HOLD, N1-60 unallocated, HEPMR #195 BENCHMARK ONLY through AP103, #199 ZIP blocker and historical PARTIAL/HOLD unchanged.
