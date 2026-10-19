# MORPH-F0: two-dimensional public Plücker kernels have an exact polynomial section over binary finite fields

**Date:** 2026-10-16. **State:** paper-only analytic no-go / classical Grassmannian geometry. **GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.** Not an F0-K/N1 numbered stage, new candidate, experiment, proof of security, OWF/PQ/PKE/KEM/trapdoor or source benchmark.

This strengthens the [fixed-codimension one-dimensional wedge-kernel public inverter](F0-fixed-codimension-wedge-kernel-section.md). Its domain is **public wedge-nullity exactly two**. Unlike a general high-nullity Plücker intersection, a *projective line* intersects the Grassmannian in **at most two points or lies entirely inside it**, because its defining equations are quadratic. Over \(\mathbb F_{2^e}\), the associated roots can be found by deterministic binary linear algebra even when q is exponentially large.

## 1. Complete original any-witness relation and finite-field interface

Let \(V=K^n\), \(K=\mathbb F_{2^e}\) explicitly represented by a polynomial basis with public irreducible modulus and polynomial field operations. Fix \(1\le c<n\) as a **constant independent of n**, \(d=n-c\ge2\), and polynomial m. For arbitrary public alternating \(A_1,\ldots,A_m\in\Lambda^2 V^*\), including zero-diagonal characteristic-two matrices, the **full original verifier** is
\[
\mathrm{Verify}(P,Y)=
[\operatorname{rank}Y=d\ \wedge\
 Y^\top A_iY=0\text{ for every }i=1,\ldots,m].
\]
Any accepted \(d\)-basis wins, regardless of planted coordinates. Denote by
\[
T_P:\Lambda^cV^*\to(\Lambda^{c+2}V^*)^m,\quad
 \xi\mapsto(\xi\wedge A_i)_i
\]
the public linear wedge map; its \(\binom nc=O(n^c)\) columns can be constructed explicitly and Gaussian-eliminated in polynomial \((n,m,e)\) time.

Every accepted H has a nonzero **decomposable** annihilator vector \(\xi_H=\ell_1\wedge\cdots\wedge\ell_c\in\ker T_P\). Conversely, for **any** nonzero decomposable \(\xi\in\ker T_P\), recover \(L=\{\ell\in V^*:\ell\wedge\xi=0\}\), which has dimension c, set \(H=L^\circ\), and check all original verifier equations. The equivalence \(\xi\wedge A_i=0\Leftrightarrow A_i|_{H\times H}=0\) is the prior [exterior coordinate proof](F0-multislice-isotropic-hyperplane-linearization.md#5-why-the-easy-boundary-stops-at-codimension-one). For c≥2, **not every kernel vector is decomposable**: extra Plücker equations cannot be skipped.

## 2. The exact public kernel-plane theorem

**Theorem (pointwise deterministic decision and search).** For fixed c over **every** binary extension field \(\mathbb F_{2^e}\), there is a deterministic algorithm polynomial in n, m and e that **decides and constructs a full-original-verifier witness on every public input with \(\dim\ker T_P\le2\)**. It does not require a planted instance distribution, uniform sampling or source postselection.

If nullity is zero, no accepted annihilator exists and the instance is NO. If nullity is one, test the kernel's unique nonzero projective direction for decomposability, reconstruct H and run the original verifier; this is the earlier pointwise theorem. For **nullity two**, choose public basis \(\xi_0,\xi_1\) of \(\ker T_P\). A projective point \([s:t]\in\mathbf P^1(K)\) represents \(\xi(s,t)=s\xi_0+t\xi_1\neq0\). It corresponds to an accepted subspace **if and only if** all defining quadratic Grassmann–Plücker relations vanish there (and the full original verifier is checked).

There is an explicit polynomially bounded generating family of homogeneous quadratic relations \(R_{I,J}(p)=0\) for the Plücker embedding \(\mathrm{Gr}(c,n)\hookrightarrow\mathbf P(\Lambda^cV^*)\), with \(|I|=c-1\), \(|J|=c+1\):
\[
 R_{I,J}(p)=\sum_{\nu=1}^{c+1}
 (-1)^{\nu-1}\,p_{I\cup\{j_\nu\}}\,
 p_{J\setminus\{j_\nu\}},
\]
where repeated indices contribute zero, and exterior-index order determines the signs. In characteristic two the signs reduce to plus, but **the same quadratic defining relations remain valid**. These equations collectively vanish on a nonzero c-vector **if and only if it is decomposable**. They can be explicitly enumerated in \(O(n^{2c})\) many relations at fixed c; evaluating each requires polynomial work. Classical sources: [Grassmannians and Plücker equations](https://link.springer.com/article/10.1007/s10231-022-01233-7) and [finite-field linear sections of Grassmann varieties](https://doi.org/10.1016/j.ffa.2008.08.001).

On the public two-dimensional kernel, each \(R_{I,J}\) restricts to a **homogeneous binary quadratic**
\[
 Q_{I,J}(s,t)=a s^2+b s t+z t^2.
\]
Its coefficients are extracted from \(R(\xi_0)\), \(R(\xi_1)\) and \(R(\xi_0+\xi_1)\), so **no polynomial factorization in n variables** is needed.

**Case A: every restricted Q is identically zero as a polynomial.** Then **every one of the q+1** projective points of the public kernel line represents a distinct decomposable c-vector and hence a distinct accepted d-space. Choose \(\xi_0\), reconstruct H, check the complete verifier and return its basis. This case does not require enumerating q field elements.

**Case B: some restricted Q is nonzero.** A nonzero homogeneous quadratic has **at most two** distinct zeros on \(\mathbf P^1(K)\). Solve this single quadratic exactly, producing all its rational projective roots (zero, one or two). For each root \([s:t]\), test **all the other Plücker quadrics**, reconstruct L and H, and run the **full original verifier**. Output the first accepted candidate; if none pass, the input is NO. Any actual accepted H must be among these at-most-two projective roots, so both soundness and completeness are exact.

### Deterministic quadratic roots in characteristic two, without enumerating K

For \(Q(s,t)=a s^2+b s t+z t^2\), test the projective point \([1:0]\) exactly when a=0. For the affine chart t=1, solve \(a x^2+b x+z=0\):

- If a=0, solve the linear equation \(b x+z=0\), or recognize identically zero/no solutions in the affine chart.
- If a≠0 and b=0, solve \(x^2=z/a\) by the deterministic inverse Frobenius map \(x=(z/a)^{2^{e-1}}\).
- If a≠0 and b≠0, set \(y=(a/b)x\), so \(y^2+y=a z/b^2\). The map \(y\mapsto y^2+y\) is **\(\mathbb F_2\)-linear** on the e-dimensional binary vector space K. Write its e×e matrix in the public polynomial basis and solve with ordinary binary Gaussian elimination. If solvable, its kernel is \(\{0,1\}\), so list **both** solutions; otherwise list none.

The nonzero-Q case cannot contain an identically zero entire projective line; the above process yields **at most two distinct roots** including infinity. Every step is polynomial in e and the public description length. This is classical Artin–Schreier/Frobenius arithmetic, not a special cryptographic assumption; see [quadratic equations over \(\mathrm{GF}(2^e)\) and trace](https://olegfomenko.dev/2025/08/30/solve_gf2.html).

### Exact witness multiplicity in this nullity-two subclass

Projectively distinct decomposable c-vectors define distinct annihilator c-spaces and distinct accepted d-spaces. Thus on a public nullity-two instance, the **number of accepted d-dimensional subspaces** is **exactly one of** \(0,1,2,q+1\), and is determined by the above polynomial algorithm. The number of accepted matrices/bases is this number multiplied by
\[
|\operatorname{GL}_d(q)|=\prod_{j=0}^{d-1}(q^d-q^j).
\]
This is not a statement that these cases are equally likely or that the planted H is unique in general. For nullity one the count is 0 or 1, depending on decomposability and the full verifier; for nullity zero it is 0.

## 3. Complexity, restrictions and source-first interpretation

The public exterior-coordinate dimension \(\binom nc\), Plücker equation family and all linear systems remain polynomial **because c is fixed**. This is a **pointwise attack**: for *any* honest source whose **actual public output** has wedge-nullity at most two, its original any-witness inversion succeeds with certainty. We make **no** assertion that an interesting planted distribution places non-negligible probability on that event unless that probability is separately derived from the **unconditional honest generator**.

For general odd-characteristic finite fields, a degree-two root finder may be randomized/expected polynomial; **this note only claims unconditional deterministic polynomial inversion for \(q=2^e\)**. For large unknown nullity, solving all simultaneous quadratic Plücker restrictions is not reduced to a single quadratic, and neither universal decision nor search has been established by this argument. It also says nothing about the external [Liu–Qiao–Tang–Zhang 2026 low-d planted-TI conjectural regime](https://arxiv.org/abs/2609.31256) where codimension grows and \(\dim\ker T_P\) need not be ≤2. No source sampling, code, new N1/F0-K numbered record, field-size brute force or asserted cryptographic hardness.

**Decision:** **ANALYTIC EASY** for full-original-verifier fixed-c binary-field tuples with public wedge-nullity \(\le2\), with exact accepted-fibre count when it equals two. **GLOBAL NO NOMINATION**, H-A/H-B/H-C HOLD, N1-60 unallocated, HEPMR #195 BENCHMARK ONLY through AP103, #199 missing source ZIP and historical N1-19/N1-23 PARTIAL, N1-26 HOLD unchanged.
