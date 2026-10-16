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

## 6. Decision and limits

| Public subclass | Original any-witness inverse | Research decision |
| --- | --- | --- |
| Rank ≤2, full labelled rank pattern | Pointwise polynomial, with effective field enumeration | **ANALYTIC EASY** |
| Simple rank 3 with frame-generated two-line closure | Pointwise polynomial; verify all ranks | **ANALYTIC EASY under closure hypothesis** |
| Uniform independent affine rank-three source, `q≥n⁴` | Unconditional success `1-O(1/n)` | **SOURCE-DISTRIBUTION FAILURE** |
| Uniform full-vector fixed-rank `r` source, `q≥n^(r+1)` | Unconditional success `1-O(1/n)` | **SOURCE-DISTRIBUTION FAILURE** |
| Arbitrary finite-field rank-three realization | No general inverter supplied here | **UNRESOLVED, NOT NOVELTY EVIDENCE** |

No measured runs, parameter trials, fresh numbered source cases or Q-hardness claims. Passing no existing screen is insufficient for Field 15. **GLOBAL NO NOMINATION**; #195 BENCHMARK ONLY through AP103, #199 missing ZIP bytes, N1-19/23 PARTIAL, N1-26 HOLD and N1-60 unallocated remain unchanged.
