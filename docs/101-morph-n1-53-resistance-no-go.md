# N1-53 - exact effective-resistance inverse (analytic no-go)

**Date:** 2026-10-14. **Disposition:** REJECT before code, no new empirical cases. **Global:** NO NOMINATION.

This is an immutable, referenced research note transcribed from [issue #196, comment 6169028746](https://github.com/StanleyLl0yd/morph-kem/issues/196#issuecomment-6169028746), not a new experiment. It includes all 15 MORPH-R0 fields, the polynomial reconstruction identity, the precise labeled/positive/simple-graph scope, and prior-art citations. The public inverter is mathematical, **not repository implementation**.


**Scope and distinction.** Unlike the previously rejected *shortest-path/tropical metric* constructions N1-25/27/28, this is an independently specified *electrical-flow/effective-resistance* relation. Its exact inverse, however, is already classical. This gate therefore ends **BEFORE code or source sampling**. No experiment is claimed.

### MORPH-R0 fields (specified together, before any experimental data)

1. **PublicInstance:** a labeled vertex set `V={0,...,n-1}`, `n>=3`, and the **complete exact rational matrix** `R=(r_ij)` of all-pairs effective resistance on one connected positive-conductance undirected simple graph.
2. **Secret/Witness:** its hidden (but not security-relevant) simple weighted edge set. Witness `Y` is any connected graph on the **same labeled V** whose allowed positive integer conductances (1 or 2) yield the same exact `R`; an absent edge has weight zero.
3. **Generation distribution:** guarantee connectivity by including every star edge `(0,i)`, each independently conductance 1 or 2. For all nonstar unordered pairs independently sample `w_ij in {0,1,2}` with probabilities `(1/2,1/4,1/4)`. No rejection, no conditioning, all coins public-distribution-defined. Complete `R` is computed by rational Laplacian linear algebra; both generation and exact output bitlength are polynomial in n (conductances <=2; determinant-size/Hadamard bounds).
4. **Public verifier:** reconstruct candidate Laplacian `L_Y`, compute `R(Y)` by exact rational inverse on the rank-`n-1` subspace (or `L_Y+11^T/n`), and accept iff `R(Y)=R` and the candidate obeys connected/star/edge-weight domain. Polynomial-time in the **bit model**, not floating-point tolerance.
5. **Attacker-success equivalence:** `Equivalent(P)={Y: Verify(P,Y)}`; **any** accepted Y wins, irrespective of planted edge-generation coins.
6. **Stabilizer/kernel/fibre:** for the specified labeled simple positive-integer graph domain, complete `R` determines its Laplacian and every off-diagonal conductance, so **the exact accepted fibre is a singleton**. If parallel edges were permitted, splitting the same total conductance would instead yield equivalent witnesses; no security may be inferred from either case.
7. **Known quotients/representations:** weighted Laplacian `L`, Moore-Penrose pseudoinverse `L^+`, Euclidean squared-distance Gram matrix `L^+`; a standard electrical-network inversion problem, not a new algebraic assumption.
8. **Canonicalization / public section:** let `J=I-11^T/n`. From `r_ij=L^+_ii+L^+_jj-2L^+_ij` and `L^+1=0`, we have **`B=-1/2 J R J=L^+`** exactly. Then **`L=(B+11^T/n)^{-1}-11^T/n`**. Return each `w_ij=-L_ij` for `i!=j`. This uses only P, two rational matrix products and one nonsingular rational inverse; exact original verifier accepts the returned Y on every honestly generated instance.
9. **Local / low-weight:** the attack does not need motif leakage. Each edge weight is exposed as an off-diagonal entry of reconstructed `L`; local-statistic or planted-star camouflage cannot repair the structural section.
10. **Noise-to-optimization:** no noise is present. Rounding/truncation would change the relation to a classical inverse-network estimation problem requiring a fresh exact definition, not rescue this one.
11. **Cover/base/fibre:** none; vertices are labeled and fully observed. Partial terminal observations belong to the established Kron-reduction/Schur-complement response-network problem and are NOT covered by the uniqueness statement above.
12. **Matched weak control:** on the **same** generated graph, the one-vertex effective-resistance star `(r_0i)` is a lower-information comparator (not assumed invertible). The full `R` attacker above is mandatory and deterministically succeeds. No measured control comparison is claimed or needed for analytical rejection.
13. **Mandatory validation:** ZERO empirical slices pre-registered or run, because Fields 7,8,15 already fail. A future independent implementation can unit-check the displayed identity with rational arithmetic but must never be counted as a hardness experiment or used to resuscitate N1-53.
14. **Quantum screen:** the described full-matrix inversion has a classical polynomial exact public algorithm. Quantum HSP/hidden-shift, generic Grover and quantum-walk studies do not create hardness in its presence; no quantum claim.
15. **Why-not-mature / novelty:** **FAIL, with explicit affirmative counterevidence.** The relation is a classical effective-resistance-to-Laplacian inversion / Euclidean-distance centering identity. It shares neither the shortest-path operation of N1-25 nor any new cryptographic hardness. Sources: [electrical networks/algebraic graph theory, Proposition 5.2](https://www.control.utoronto.ca/~jwsimpson/papers/2017k/), [effective resistance and Laplacian pseudoinverse, Phys. Rev. E 2017](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.96.032311), and [resistance distance / Schur complement, Linear Algebra Appl. 2022](https://www.sciencedirect.com/science/article/abs/pii/S0024379522000039).

### Proof and decision

Write `d=diag(L^+)` and `1` for the all-ones column. The defining identity is `R=d1^T+1d^T-2L^+`. Multiply by `J` on both sides; `J1=0` kills the two rank-one summands and `JL^+J=L^+`, giving `-JRJ/2=L^+`. On `1^perp`, `B=L^+` has eigenvalues reciprocal to the positive eigenvalues of `L`; adding `11^T/n` supplies eigenvalue one along span(1). The inverse-minus-projector formula recovers `L` exactly and therefore all original simple-graph conductances. Rational Gaussian elimination on polynomial-bitlength data gives a polynomial public any-witness section.

**Disposition: N1-53 REJECT (analytic, not experimental); GLOBAL NO NOMINATION.** No trapdoor, KEM/PKE, OWF/PQ claim, implementation branch, parameter rescue or additional HEPMR AP scans. The genuinely new mathematical Field-15 search must continue **beyond** electrical resistance, Kron reduction and full matrix normal forms.

## Repository integrity

No new `src/`, `scripts/`, `tests/`, raw experimental ZIP or corpus is asserted or added by this documentation sync. N1-52 cumulative numerical values are unchanged and frozen in [the prior snapshot](100-morph-n1-status-2026-10-14.md). The next independent positive-Field-15 search is N1-54, not a numerical repair of N1-53.
