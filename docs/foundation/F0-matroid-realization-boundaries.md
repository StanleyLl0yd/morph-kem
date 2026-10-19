# F0 source-first boundary: finite-field matroid realization (2026-10-16)

**Status:** independent mathematical literature screened; specific polynomial public sections proved below. **Research-only, GLOBAL NO NOMINATION, H-A/H-B/H-C HOLD.** This is an *unnumbered* analytical continuation of [#208, comment 6216134094](https://github.com/StanleyLl0yd/morph-kem/issues/208#issuecomment-6216134094). It is **not** F0-K10 or N1-60, a candidate, an experiment, an implementation, or new empirical evidence.

## 1. Public inverse relation and polynomial interface

For a fixed rank `r` and a publicly represented finite field `F_q`, an unconditional polynomial-time generator samples an `r × n` matrix `X`, then publishes the exact rank `rk(X_S)` of **every** labelled subset `S ⊆ [n]` with `|S| ≤ r`. The full public verifier takes **any** `r × n` candidate `Y` and accepts only when **all** those ranks agree. The attack target is the entire fibre `Equivalent(P)`, not the planted columns or their coordinate gauges. For fixed `r`, the public rank table and verifier have `O(n^r)` entries and polynomial running time; nothing here authorizes this explicit interface for unbounded `r`.

The underlying *matroid representation* problem is established mathematics. Kim, de Mesmay and Miltzow prove that **real-field** representability is `∃R`-complete even for rank three, in [DMTCS 26:2 (2024)](https://doi.org/10.46298/dmtcs.10810). This is a **worst-case real-field decision** theorem, not an average-case finite-field inversion or PQ-hardness result. Uniform matroids and their Vandermonde / Reed-Solomon realizations are also classical; see [MDS characterization](https://ecc-iiith.vlabs.ac.in/exp/reed-solomon-codes/theory.html).

## 2. Rank two: universal deterministic section

From singleton ranks, find all zero (loop) columns. From pair ranks, partition nonzero labelled columns into classes of parallel directions. Every honest `F_q²` input has at most `q+1` classes. Using the **public polynomial-basis field representation** (or another explicitly guaranteed polynomial-time procedure to list as many distinct elements as needed), assign each class a different projective direction from `(1,t)`, `t∈F_q`, plus `(0,1)` when required. Give every member of a class the same nonzero representative; loops receive `(0,0)`.

All published singleton/pair ranks are now reproduced **exactly**; the original full verifier accepts. The procedure is polynomial in `n` and `log q` under the stated effective element-enumeration interface, not exponential enumeration of all of `F_q`. Even rank-zero and rank-one honest patterns are handled. No planted coordinates are reconstructed. **This entire exact rank-two subclass is analytically invertible on every honest instance.**

## 3. Rank three: deterministic two-line closure from a projective frame

Assume a **simple rank-three configuration** over `F_q` and a frame `(a,b,c,d)` whose every triple is independent. Normalize these four projective points to `[1:0:0]`, `[0:1:0]`, `[0:0:1]`, `[1:1:1]`. Such a unique frame normalization exists over every finite field, including characteristic two.

Build a closure of placed labelled points: for an unplaced `z`, find **two distinct** lines `uv` and `st` through already placed distinct points, whose collinearities with `z` are certified by the **original** public rank table. Compute the unique intersection of the two already reconstructed lines, place `z` there, and repeat. Try all `O(n⁴)` frames; for any full closure, check **all** original public rank tests before returning `Y`. Distinctness of the two source lines is itself publicly certified by a rank-three test on one source point against the other source pair.

**Scoped theorem.** If some frame produces a closure that places *every* column, all placed points equal the planted realization after a common projective normalization: induction holds because a pair of distinct projective lines has exactly one intersection. Thus the candidate always passes the original verifier; the same argument shows accepted representations in this frame-generated subclass are unique **up to common projectivity and independent nonzero column scalings**. The algorithm is polynomial for fixed rank three.

**Not proved:** closure for arbitrary rank-three matroids. A point constrained only to one placed line, or a configuration with no fully generating frame, is outside the theorem. Four noncollinear points alone are **insufficient**.

## 4. Unconditional honest-law failure: affine rank three

Sample independently and uniformly `(a_i,b_i) ∈ F_q²`, and set `x_i=(1,a_i,b_i)` for each `i=1,...,n`. Publish the full rank-≤3 pattern **without rejection or conditioning**. Each fixed triple is dependent with exact probability

```text
q^(-2) + (1 - q^(-2)) / q = q^(-1) + q^(-2) - q^(-3).
```

Indeed the first two points coincide with probability `q^(-2)`; otherwise their affine line contains exactly `q` of the `q²` equally possible third points. A union bound gives, on the original unconditional distribution,

```text
Pr[all triples independent] >=
  1 - binom(n,3) * (q^(-1) + q^(-2) - q^(-3)).
```

When `q ≥ n`, choose `n` distinct public elements `t_i` efficiently in the fixed field representation and output `y_i=(1,t_i,t_i²)` **if** the entire rank table reports all triples independent. Every three-column determinant is a nonzero Vandermonde product, so all singleton/pair/triple ranks agree and the full original verifier accepts. This is an any-witness inverter with unconditional success at least the bound above; for `q ≥ n⁴`, its success tends to one as `1-O(1/n)`. It never attempts to infer the sampled affine points.

## 5. Fixed-rank generalization: uniform matroid section

For **fixed** `r≥2`, sample `n` columns independently uniformly in `F_q^r`, without rejection; publish all ranks on subsets of size ≤r. Each `r × r` sampled submatrix has independent columns with exact probability

```text
prod(j=1..r) (1 - q^(-j)).
```

The union bound on the **original unconditional law** yields

```text
Pr[every r-subset independent] >=
  1 - binom(n,r) * (1 - prod(j=1..r) (1-q^(-j)))
>= 1 - binom(n,r) * sum(j=1..r) q^(-j).
```

On this event every subset of size ≤r is independent, so the honest published rank table is exactly `U_(r,n)`. If `q≥n`, `r × n` Vandermonde columns `y_i=(1,t_i,...,t_i^(r-1))` on distinct public field elements reproduce **every rank**, giving a deterministic accepted witness. For `q≥n^(r+1)`, fixed `r`, the unconditional success bound is `1-O(1/n)`. This is the classic uniform-matroid / MDS / Reed-Solomon section, **not an original MORPH hardness relation**. If `r` grows, the complete rank-table interface may cease to be polynomial; no such extension is claimed.

## 6. Rank-three extension: frame-free near-pencil and core-anchored lines

This section strengthens the scoped frame-closure result using **deterministic public any-witness construction**; it does **not** establish generic rank-three representability/inversion. The full rank-≤3 table, simplicity (no zero/parallel columns), rank exactly three, and an effectively encoded finite field remain essential.

### 6.1 No projective frame implies a near-pencil (all field sizes)

A *projective frame* is four labelled points with every triple independent. Suppose a simple rank-three honest configuration has **no** frame. Choose any independent triple \(a,b,c\). Every remaining point must lie on one of the three lines \(ab,ac,bc\), otherwise \(a,b,c,z\) is a frame. A remaining point lies on only one such side because the sides meet only in the existing vertices. If points \(z,w\) existed on *different* sides, for example \(z\in ab\setminus\{a,b\}\), \(w\in ac\setminus\{a,c\}\), then \((b,c,z,w)\) would have every triple independent, contradicting frame-freeness. By symmetry all additional points lie on **one** triangle side. Thus all but one of the \(n\) labelled points lie on one projective line: a **near-pencil** (including the three-point case).

Find the maximal \((n-1)\)-point line from the public rank table, place its distinct labels on distinct points of \(\mathbf P^1(\mathbb F_q)\) inside the plane, and place the remaining label off that line. The honest source guarantees \(n-1\le q+1\); an effective polynomial-time listing of \(n-2\) finite-field elements and, if needed, the point at infinity suffices even if \(q\) is enormous. Verify every original singleton, pair and triple rank before return. **Pointwise deterministic polynomial inversion for the frame-free simple rank-three subclass, for every finite \(q\).**

### 6.2 Maximal two-line closure and the public core-anchoring certificate

If there is a frame, enumerate frames and reconstruct the maximal core \(C\) by the sound two-line closure in §3. Its coordinates are projectively equivalent to the planted core on every honest input. Let \(R=[n]\setminus C\) be the unresolved labels. A *core line* is a rank-two flat generated by two distinct points of \(C\), computable from the public rank table. By maximality, every \(z\in R\) belongs to **at most one** distinct core line; otherwise two distinct core lines determine \(z\) and closure would have placed it.

Define an exact **publicly checkable core-anchoring condition**: every dependent triple containing **at least two labels of \(R\)** lies wholly on some core line (i.e. for a pair \(u,v\in C\) all three triple labels are publicly collinear with \(u,v\)). Triples containing zero unresolved labels are already represented by \(C\), and any dependent triple with just one unresolved label and two core labels is automatically on a core line. Therefore, under the condition, **every dependent triple is either entirely within \(C\) or supported on a core line**. The condition is decidable by polynomially many public rank lookups; it never examines the secret planted coordinates.

This condition permits arbitrarily many unresolved points on the *same* core line and free points on no core line. It excludes unsupported collinearities among unresolved points, such as an independent residual line generated by two unresolved points and one other point. It is sufficient, not asserted necessary.

### 6.3 Deterministic greedy public section when \(q>n^2\)

**Theorem.** For an honest simple rank-three full-rank-pattern instance with \(n\) labels, if \(q>n^2\) and **some** public frame/closure core \(C\) passes the preceding anchoring test, a deterministic algorithm polynomial in \(n\) and \(\log q\) constructs a matrix satisfying **every original rank test**. No recovery of the planted matrix, uniqueness or source distribution estimate is required.

**Construction.** Enumerate and normalize a frame, close \(C\), test anchoring, and consider the unresolved labels in any order. Previously placed projective points are pairwise distinct and realize their induced rank pattern. For a new \(z\):

- If \(z\) is on **no** core line, its public rank pattern requires independence from every pair of previously placed points. Try \([1:t:t^2]\) for successive distinct publicly enumerable \(t\in\mathbb F_q\). For any existing pair, its projective line rules out **at most two** values of \(t\), since substituting the conic coordinates gives a nonzero polynomial of degree at most two. An existing point rules out at most one value. With \(k<n\) previously placed points, at most \(2\binom{k}{2}+k\le n^2\) trial values are forbidden.
- If \(z\) lies on its **unique** core line \(L\), choose two linearly independent public core representatives \(u,v\) spanning \(L\). Try the projective points \([u+t v]\). Pairs of previously placed points whose line is exactly \(L\) are allowed to be collinear with \(z\). Each **other** pair-line meets \(L\) in at most one point, excluding at most one parameter \(t\), and each existing point excludes at most one parameter. Thus at most \(\binom{k}{2}+k\le n^2\) values are forbidden. An \(L\)-intersection with another known line is excluded unless that line is \(L\).

Because \(q>n^2\), inspect the first \(n^2+1\) **distinct** field elements in a polynomial-time effective encoding, selecting the first permitted value. No enumeration of all \(q\) elements and no hidden rejection-sampling step is needed. All chosen projective representatives are nonzero; avoid equality with already placed points explicitly.

**Inductive proof of correctness.** For a free \(z\), by the core-anchoring condition and its lack of a core line there is **no** published dependent triple of \(z\) with two previously placed labels. Avoiding every existing pair-line reproduces exactly these required triple ranks. For \(z\) attached to \(L\), any published dependent triple with previous labels must be on a core line, hence (by uniqueness) on \(L\); conversely, any previous pair already on \(L\) must form a dependent triple with \(z\) in the honest source. Keeping \(z\) on \(L\) and avoiding every other existing pair-line reproduces precisely these dependencies. Explicit point-avoidance preserves simplicity. Inductively every new triple, pair and singleton rank is correct; all previous ranks remain unchanged. After the last label, **the entire original verifier** accepts. Trying all \(O(n^4)\) frames and their polynomial closures and anchoring tests is still polynomial.

**No-frame input:** apply §6.1 instead, with no large-field assumption. **Frame with no passing anchored core:** this theorem supplies **no** inverter; failing the anchoring certificate is not evidence of hardness. The theorem is a scoped deterministic extension of classical projective coordinatization / generic point avoidance, not a claim of new matroid theory or Field-15 distinctness. Background: [Oxley, *Matroid Theory*, representability and projective construction](https://doi.org/10.1093/acprof:oso/9780198566946.003.0007); related modern hyperplane-avoidance literature [Jafari (2026)](https://arxiv.org/abs/2608.23647), which is **not** cited as proving this exact algorithm.

**Honest-source corollary (no conditioning):** for any unconditional polynomial sampler of simple rank-three representations over fields with \(q>n^2\), running this public algorithm and declaring failure otherwise succeeds with probability **at least** the probability that its honestly generated rank pattern has a frame/closure passing the public anchoring condition, plus the probability of its frame-free case. This is a taut exact-event lower bound, **not** a non-negligible-success claim without separately bounding the event for that source.

## 7. All fixed-field, fixed-rank labelled matroids: finite projective-point enumeration

This is a **pointwise complete** finite-domain no-go, with a more limited asymptotic interface than the large-field rank-three and Vandermonde screens above. It is a classical finite-projective-geometry algorithm, **not** a new matroid representation theory result or a novel hardness candidate.

### Exact public interface and source

Let the public input be the **complete labelled rank table** of every subset of at most r columns of an honestly generated \(r\times n\) matrix over an explicitly represented \(\mathbb F_q\), with **q and r fixed constants**. The **entire original verifier** accepts any \(r\times n\) output whose ranks agree on **all** published subsets, not necessarily the planted matrix or its field-coordinate gauges. Sampling can use **any unconditional polynomial-time honest source** producing this table; no uniformity, uniqueness, planted-vector reconstruction or rank-conditioned rejection is assumed.

For an arbitrary public table, its claimed maximum rank is \(\rho\le r\); on honest tables this equals the rank of the planted matrix. If \(\rho=0\), return all-zero columns. If \(\rho=1\), return 1 for every publicly nonloop column and zero for loops, embedding in r rows. For \(\rho\ge2\), perform these deterministic steps:

1. Read singleton ranks: rank zero iff the column is a **loop** (zero). Among nonloops, the public pair rank-one relation identifies equal **projective directions**. On honest data it is an equivalence relation and partitions the labels into t publicly known **parallel classes**, regardless of class sizes.
2. Every nonzero direction of a rank-\(\rho\) representation lies in the finite projective space \(\mathrm{PG}(\rho-1,q)\), which contains exactly
\[
M(q,\rho)=\frac{q^\rho-1}{q-1}
\]
one-dimensional subspaces. Hence every honest source has **t≤M(q,\rho)**. Enumerate the M normalized projective vectors, e.g. by scaling each nonzero vector until its first nonzero coordinate is 1.
3. Enumerate **every injection** from the t public parallel classes into these M projective directions. Assign its chosen normalized vector to all labels in a class and zero to the loops; pad extra zero rows up to r. For each resulting public candidate Y, check **every original singleton/pair/.../r-subset rank**. Output the first that passes, or reject if all fail.

### Proof of pointwise completeness and complexity

Every honest representation has exactly the given loops and parallel classes. Its nonzero columns, normalized projectively and after selecting coordinates for their \(\rho\)-dimensional span, realize an **injective assignment** of those t classes to \(\mathrm{PG}(\rho-1,q)\). That exact injection is among the public algorithm's trials. Independently scaling nonzero columns or changing their common basis never changes any subset rank. Thus at least one trial passes the **full original verifier**, with certainty and without trying to recover the planted coordinate matrix. Conversely no rejected candidate is output as accepted: every successful trial is checked against the entire original table.

There are at most
\[
M(M-1)\cdots(M-t+1)\le M!
\]
candidate injections. Let L be the **actual explicit bitlength** of the full published rank table. Testing one candidate costs \(\mathrm{poly}(L,n,r,\log q)\) field operations. Therefore runtime is
\[
M(q,\rho)!\cdot\mathrm{poly}(L,n,r,\log q).
\]
For **fixed q and r** this is polynomial in n and L, with success probability **one on every honest input**. More generally it is a **fixed-parameter algorithm in the numeric parameters (q,r)** relative to the *explicit table bitlength*, with a potentially astronomical parameter-dependent factor; it is **not** polynomial in growing q/r or in a succinct rank-oracle encoding. Rank agreement through size r automatically determines the rank of any larger labelled subset, since the whole represented matrix has row rank at most r.

**Concrete q=2, r=3 check:** there are exactly seven nonzero projective directions, including the classical Fano configuration. Any honest binary rank-three table, no matter how many repeated labelled columns it has, has at most seven nonloop parallel classes, so **at most \(7!=5040\)** trial assignments followed by polynomial full-rank-table checks. Neither an unknown projective frame nor a failed line-closure certificate is an obstruction for this **fixed-field** subclass.

### Precise limits

- The factor \(M!\) is **not** polynomial in \(\log q\) when q grows, nor in r when r grows. The previously unresolved **rank-three, growing-field** source remains unresolved outside its independently proved large-field/frame/anchoring subclasses. A public rank **oracle** rather than an explicit full table is a different interface.
- If r grows with the security parameter, the complete rank table itself may require superpolynomial public bitlength, so the parameterized bound **does not** establish a polynomial honest cryptographic generator.
- This is elementary labelled projective-point enumeration from classical matroid representation theory. Prior-art context: [Oxley, *Matroid Theory*, finite-field representability](https://doi.org/10.1093/acprof:oso/9780198566946.003.0007); [SageMath's binary Fano-matroid example](https://doc.sagemath.org/html/en/reference/matroids/sage/matroids/database_matroids.html). The 7-point Fano geometry is long known; no independent Field-15 novelty or crypto assumption follows.

**Research disposition:** **ANALYTIC EASY** for **every** honest fixed-q/fixed-rank full-labelled-rank-table instance, with exact pointwise full-verifier success. **GLOBAL NO NOMINATION**, H-A/H-B/H-C HOLD, N1-60 unallocated; no new measured cases, PR-independent experiment, implementation or security claim.

## 8. All honest binary matroids: exact public standard representation by basis exchanges

The fixed-field finite-projective enumeration in §7 is **unnecessary for \(q=2\)**. The field \(\mathbb F_2\) has only one nonzero scalar, so a replacement-basis rank query exposes each column coordinate **exactly**, not merely whether it is nonzero modulo a hidden scalar. This is the **classical unique standard binary representation** via fundamental circuits, not a new theorem. Relevant prior art: [Truemper, *Matroid Decomposition*, §3.3](https://www2.math.ethz.ch/EMIS/monographs/md/matroiddecompositionbook.pdf); [Binary Spaces and Cutting Planes, standard representation \([I\mid A]\)](https://ir.cwi.nl/pub/21445/21445A.pdf).

### Theorem: deterministic pointwise public reconstruction at arbitrary rank

Let \(P\) be **any honest GF(2)-representable labelled matroid**, given as (i) the exact rank table for all subsets of size at most a published row bound r, (ii) an **exact public rank-query oracle**, or (iii) an **exact public independence oracle** that decides whether a requested labelled subset is linearly independent. Let its actual matroid rank be \(\rho\le r\), possibly growing with n. An attacker can recover an accepted \(\rho\times n\) binary representation, padding it to r rows if the original output interface requires r rows, with **\(O(n\rho+n)\) exact public independence-or-rank queries** and polynomial binary arithmetic. **No fixed-rank or finite-projective-size assumption is required.**

**Algorithm and proof.** Use the public rank or independence predicate to greedily find a maximal independent labelled basis \(B=(b_1,\ldots,b_\rho)\). Since P is honest, this is a true basis; identifying it needs at most n incremental independence/rank queries. If \(\rho=0\), output all-zero columns. Normalize the unknown planted representation by the unique invertible row change that sends its columns indexed by B to the standard unit columns \(e_1,\ldots,e_\rho\). This change does **not** alter any subset rank.

For each *other* labelled column x and each basis index j, query the **independence** of the size-\(\rho\) set (equivalently ask whether its rank is \(\rho\))
\[
(B\setminus\{b_j\})\cup\{x\}.
\]
With the planted representation in the normalized basis, this set is independent **if and only if** the jth coordinate of the column x is **nonzero**: all other \(\rho-1\) basis coordinates are still spanned, so the rank rises exactly when x has a component in the missing \(e_j\) direction. Over **GF(2)**, "nonzero" means **exactly 1**. Set
\[
Y_{jx}=\begin{cases}
1,&\operatorname{rank}_P((B\setminus b_j)\cup x)=\rho,\\
0,&\text{otherwise}.
\end{cases}
\]
For the basis columns set \(Y_{b_j}=e_j\). Thus **every** output column agrees exactly with the planted representation after that single unknown global row normalization, even if loops or repeated parallel labels exist. The entire candidate is consequently rank-equivalent to the planted matrix on **all subsets**, including every original published rank test. The adversary never needs to know the original basis transformation and may run the complete original verifier as a final independent check.

The total count is at most n basis-extension rank calls and \(\rho(n-\rho)\) replacement-basis calls, all on sets of size ≤r.

A rank query on each replacement basis set can be replaced **one-for-one by the binary independence predicate** (independent exactly when its rank is rho); finding B itself also requires only incremental independence calls. Thus even the weaker public *independence-oracle* interface gives the same pointwise query bound. With an explicit rank table, the algorithm is polynomial in its **actual public table bitlength** and in n and r. With an exact rank **or independence** oracle, reconstruction needs only polynomially many queries **even when \(\rho\) grows**. An oracle by itself does **not** imply that the separate original all-subsets verifier is executable in polynomial time; the theorem establishes exact matroid equality mathematically and polynomial **reconstruction query complexity**, not an unjustified verifier-interface claim.

**Decision:** every honestly generated binary matroid in the stated rank-access interface is **ANALYTIC EASY / PUBLIC ANY-WITNESS INVERSION**, irrespective of rank, n, secret gauge, number of repeated labelled columns or honest source distribution. In particular, the previous 5040-case exhaustive bound for GF(2), r=3 is superseded by this **linear-in-nr query** construction.

### What changes for other fields

For \(\mathbb F_q\) with \(q>2\), replacement-basis rank still reveals the **zero/nonzero support** of each normalized column coordinate but **not its actual nonzero value** (nor independent column scalings). Thus this proof does **not** establish full representation recovery over GF(3) or growing q. The complete fixed-q/r projective enumeration (§7), frame/closure and source-distribution gates remain separately valid. No reduction from arbitrary rank-oracle representability **decision** to a polynomial algorithm on adversarial NO instances is claimed: the theorem requires an **honest representable YES input**.

**GLOBAL NO NOMINATION**, no samples, no implementation and no independent Field-15 novelty.

## 9. Decision and limits

| Public subclass | Original any-witness inverse | Research decision |
| --- | --- | --- |
| Rank ≤2, full labelled rank pattern | Pointwise polynomial, with effective field enumeration | **ANALYTIC EASY** |
| All honest binary (GF(2)) rank-access matroids, even growing rank | Pointwise polynomial public basis-exchange recovery, `O(nr)` rank/independence queries | **ANALYTIC EASY, no rank bound** |
| All exact labelled rank tables over fixed finite q and fixed r | Complete pointwise projective-class enumeration, at most `M(q,r)!` trials | **ANALYTIC EASY (parameter-limited)** |
| Simple rank 3 with frame-generated two-line closure | Pointwise polynomial; verify all ranks | **ANALYTIC EASY under closure hypothesis** |
| Simple rank 3 with no four-point frame (near-pencil) | Pointwise polynomial for every finite field | **ANALYTIC EASY** |
| Simple rank 3 with a core-anchored closure, `q>n²` | Pointwise polynomial by deterministic line/conic avoidance | **ANALYTIC EASY under checkable certificate** |
| Uniform independent affine rank-three source, `q≥n⁴` | Unconditional success `1-O(1/n)` | **SOURCE-DISTRIBUTION FAILURE** |
| Uniform full-vector fixed-rank `r` source, `q≥n^(r+1)` | Unconditional success `1-O(1/n)` | **SOURCE-DISTRIBUTION FAILURE** |
| Rank-three realization over growing/unbounded finite fields | No general polynomial-in-`log q` inverter supplied here | **UNRESOLVED, NOT NOVELTY EVIDENCE** |

No measured runs, parameter trials, fresh numbered source cases or Q-hardness claims. Passing no existing screen is insufficient for Field 15. **GLOBAL NO NOMINATION**; #195 BENCHMARK ONLY through AP103, #199 missing ZIP bytes, N1-19/23 PARTIAL, N1-26 HOLD and N1-60 unallocated remain unchanged.
