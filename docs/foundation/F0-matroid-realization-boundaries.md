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

## 7. Decision and limits

| Public subclass | Original any-witness inverse | Research decision |
| --- | --- | --- |
| Rank ≤2, full labelled rank pattern | Pointwise polynomial, with effective field enumeration | **ANALYTIC EASY** |
| Simple rank 3 with frame-generated two-line closure | Pointwise polynomial; verify all ranks | **ANALYTIC EASY under closure hypothesis** |
| Simple rank 3 with no four-point frame (near-pencil) | Pointwise polynomial for every finite field | **ANALYTIC EASY** |
| Simple rank 3 with a core-anchored closure, `q>n²` | Pointwise polynomial by deterministic line/conic avoidance | **ANALYTIC EASY under checkable certificate** |
| Uniform independent affine rank-three source, `q≥n⁴` | Unconditional success `1-O(1/n)` | **SOURCE-DISTRIBUTION FAILURE** |
| Uniform full-vector fixed-rank `r` source, `q≥n^(r+1)` | Unconditional success `1-O(1/n)` | **SOURCE-DISTRIBUTION FAILURE** |
| Arbitrary finite-field rank-three realization | No general inverter supplied here | **UNRESOLVED, NOT NOVELTY EVIDENCE** |

No measured runs, parameter trials, fresh numbered source cases or Q-hardness claims. Passing no existing screen is insufficient for Field 15. **GLOBAL NO NOMINATION**; #195 BENCHMARK ONLY through AP103, #199 missing ZIP bytes, N1-19/23 PARTIAL, N1-26 HOLD and N1-60 unallocated remain unchanged.
