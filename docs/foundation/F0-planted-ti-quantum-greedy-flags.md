# MORPH-F0: coherent amplification of randomized public isotropic flags

**2026-10-20. Quantum attack upper bound / mathematical screen; GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.** This pass applies **known** quantum amplitude amplification to the [proved full-public randomized greedy-flag attack](F0-planted-ti-randomized-flag-search.md), without inventing a new oracle, KEM, quantum hardness assumption, or quantum primitive. The *actual full published tensor* is available to the attacker, and **every reported classical output** passes the **original any-witness verifier**.

**External algorithmic priority.** The planted totally-isotropic source, original problem and a generic `q^{O(n log n)}` classical bound originate with Liu–Qiao–Tang–Zhang, [*The planted tensor problem over finite fields: algorithms and cryptography*](https://arxiv.org/abs/2609.31256) (2026). The **quantum speedup itself is not new**: fixed-point amplification with only a certified lower success bound is due to Yoder, Low and Chuang, [*Fixed-point quantum search with an optimal number of queries*](https://doi.org/10.1103/PhysRevLett.113.210501) (Phys. Rev. Lett. 113, 210501, 2014). This note derives only a **scoped combined upper exponent** for the explicit honest distribution and the original full-verifier attack, not a claim to priority over all competing quantum algorithms.

## 1. Original honest source and deliberate field/circuit scope

Take `V=F_q^n`, `2<=d<n`, `c=n-d`, and `m>=1`. H is sampled independently of the forms from **any prior** on d-planes. Conditional on H, publish m independent **uniform alternating forms** vanishing on `H x H` without rank filtering or postselection. All matrix coefficients are public classical input. The original accepted relation is
\[
\operatorname{Verify}(A,L)
=[\dim L=d\ \wedge\ A_i|_{L\times L}=0\ \forall i].
\]
**Any** accepted L wins, not only H.

For an explicit **exact uniform reversible coin circuit**, this quantum pass restricts to `q=2^e`, `e>=1`, with a polynomial-time effective representation of the field and fixed q in the stated asymptotics. Uniform field elements then require exactly e uniform computational-basis bits. The earlier **classical** rank theorems hold for *all* prime powers; this note does **not** silently assert the same exact gate model for an arbitrary odd characteristic. No fault tolerance, physical resource estimate, QRAM assumption or quantum simulation is claimed.

## 2. Polynomial reversible full-public trial oracle (not a hidden oracle)

Use the exact public algorithm of the [randomized flag note](F0-planted-ti-randomized-flag-search.md), with `1<=t<=d`. Starting at `U_0=0`, compute public simultaneous orthogonal spaces
\[
S_A(U_k)=\{v\in V:A_i(u,v)=0,\ u\in U_k,\ i=1,\ldots,m\}
\]
using a **fixed canonical RREF procedure**. For each depth k, choose one public basis of the quotient `S_A(U_k)/U_k`; let its dimension be `D_k\le n`.

For a fixed-length random tape
\[
R=(z_0,\ldots,z_{t-1}),\qquad
z_k\in F_q^n
\]
with all `tn` field coordinates uniformly independent, take the first `D_k` coordinates of `z_k` as the quotient-vector coefficients. If `D_k=0` or the selected quotient vector is zero, **abort that trial**; otherwise extend U by the selected line. The unused coefficients are ignored. Each nonzero quotient vector induces the same projective line with exactly q-1 choices, so this reproduces **precisely** the one-shot uniform quotient-vector-with-zero-abort experiment analyzed in [PR #245](F0-planted-ti-randomized-flag-search.md), even when `D_k` depends adaptively on previous public computations and coins.

At depth t compute `S_A(U_t)`, accept the tape if and only if its dimension is d **and the original verifier accepts the entire candidate**. Let `f_A(R)\in\{0,1\}` be this deterministic public predicate and, on acceptance, store the verified witness basis. One evaluation of f_A is **polynomial in the public bitlength**. Canonical Gaussian elimination with bounded loops, field arithmetic, branches, and verification admit a fixed-size **reversible quantum Boolean circuit** with polynomial overhead; the public coefficients A can be compiled as classical constants. The circuit computes f_A, can phase-mark success and uncompute its workspace. **No secret H, planted basis, sampled query oracle, or QRAM is supplied.**

Initial uniform superposition over all tapes R is prepared exactly by `etn` Hadamard gates (in any fixed binary coordinate encoding of the field). Measuring a uniform tape and running f_A reproduces the former classical single-trial probability
\[
p_A=\Pr_{R}[f_A(R)=1].
\]

## 3. Finite honest-source quantum search theorem

Re-use the finite parameters and **proved source statement** from the [classical greedy-flag analysis](F0-planted-ti-randomized-flag-search.md):
\[
t\le d,\qquad mt\ge c+s,\quad s\ge0,\qquad
r\ge0,\qquad
E_t=\sum_{k=0}^{t-1}(c-mk)_+,
\]
\[
\delta=t C_q q^{-(r+1)^2}+\frac{q^{-s}}{q-1},\qquad
C_q=\prod_{j\ge1}(1-q^{-j})^{-1}<4.
\]
Assume `0<\delta<1`. The **unfiltered planted-source theorem** from PR #245 says that conditional on **every H**, for at least `1-\sqrt\delta` of the sampled complete public tensors A,
\[
\boxed{p_A\ge p_0:=(1-\sqrt\delta)\,q^{-E_t-(r+1)t}.}
\]
This is a lower bound on an *actual publicly evaluable original-verifier predicate*, not a conditional probability illicitly assigned to an adaptively chosen seed.

**Theorem 1 (full-public quantum any-witness search upper bound).** Over `F_{2^e}`, for any `0<\eta<1`, a quantum attacker given all public matrices A can use established **fixed-point amplitude amplification** on the uniform random tape and reversible f_A to output a classically full-verifier-accepted d-plane, with unconditional honest-source probability at least
\[
\boxed{(1-\sqrt\delta)(1-\eta)\ge1-\sqrt\delta-\eta,}
\]
and at most
\[
\boxed{
O\left(
\operatorname{poly}(n,m,t,e,\log(1/\eta))
\frac{q^{(E_t+(r+1)t)/2}\log(1/\eta)}
     {\sqrt{1-\sqrt\delta}}
\right)
}
\]
reversible gate operations, up to the standard polynomial-precision overhead for the required controlled phase rotations. The number of coherent evaluations of the trial circuit and its inverse scales as `O(p_0^{-1/2}\log(1/\eta))`. A final classical full-verifier check is mandatory.

**Proof.** Condition on an H and on the source-good tensor event where `p_A\ge p_0`. The quantum circuit computes a success bit, performs its phase flip, and exactly uncomputes all trial state; uniform tape superposition therefore has marked squared amplitude `p_A`. The fixed-point amplification theorem of Yoder–Low–Chuang takes **a lower bound** `p_0`, not exact knowledge of `p_A`, and reaches measurement success at least `1-\eta` using `O(p_0^{-1/2}\log(1/\eta))` oracle calls. Each call costs polynomial reversible work; the measured successful tape yields an explicitly computed accepted candidate that is verified once again classically. Averaging the good event over every prior H gives the stated unconditional success probability. No quantum hardness theorem or cryptographic security follows. QED.

**Precision caveat.** In a discrete universal gate set, generic phase rotations can be approximated to an error polynomially smaller than the target aggregate failure budget using polynomial-in-`\log(1/\varepsilon)` synthesis per gate. The displayed complexity absorbs this overhead; it does **not** claim exact native synthesis of arbitrary fixed-point phases or a concrete fault-tolerant circuit count.

## 4. Asymptotic quantum attack cost in the sparse conjectural regime

Fix a binary field `q=2^e` with constant e and suppose `d/n\to\alpha\in(0,1/2)` and `m\asymp n/\log n`. Choose
\[
s=\lceil\sqrt n\rceil,\quad
t=\lceil(c+s)/m\rceil,\quad
r=\lceil\sqrt{3\log_q n}\rceil,
\]
and a target failure `\eta=o(1)` with `\log(1/\eta)=O(\log n)`. Then `t=\Theta(\log n)`, `\delta=o(1)`, and the prior finite classical analysis proves
\[
E_t=\frac{c^2}{2m}+O(c+m),\qquad
(r+1)t=o(n^2/m).
\]
Hence **the classical prior and quantum amplified upper bounds** are:
\[
\boxed{\begin{aligned}
\log_q W_{\rm classical}&\le {c^2\over2m}+o(n^2/m),\\
\log_q W_{\rm quantum}&\le {c^2\over4m}+o(n^2/m).
\end{aligned}}
\]

For `\alpha=1/3`, the corresponding leading coefficients of `n^2/m` are `2/9` classical and **`1/9` quantum**. This is a strict **upper bound on an actual search attack**, not a novel generic quantum speedup, lower bound, tight security estimate, or comparison against the best unrelated quantum tensor algorithm. Both **sufficient work budgets displayed above** scale as `q^{\Theta(n\log n)}` and are superpolynomial in n; this is **not** a lower bound on the best possible attack or on the actual work of an early-stopping implementation.

## 5. Explicit nonclaims and next attack-first work

- This quantum routine reads the **entire public tuple** via a reversible polynomial-time implementation; it is **not** an adaptive pair-oracle query lower bound or a use of any hidden-H coordinate chart.
- The quadratic speedup is standard quantum algorithmics; **no novel cryptographic hardness basis or positive MORPH-R0 Field 15** arises.
- The gate count is asymptotic, not a fault-tolerant resource report. No quantum program, generated public sample, hardware run, laboratory measurement, empirical speedup, A-ID or N1 stage is introduced.
- The earlier membership-only black-box bound in [dense rank-locus notes](F0-planted-ti-dense-rank-locus.md) was **classical** and does not apply to this coherent full-public algorithm.
- A genuine improvement would require **structure-aware quantum search** that uses the published coefficients to bias or directly reconstruct hidden witnesses beyond mere amplitude amplification; it must return an original-verifier accepted plane on the unfiltered source.
- README and the stage registry remain compact/unchanged; N1-60 is free. H-A/H-B/H-C stay HOLD, HEPMR BENCHMARK ONLY.

**Disposition:** QUANTUM AMPLIFICATION OF A PROVED PUBLIC ANY-WITNESS SEARCH UPPER BOUND, NOT A NEW QUANTUM ALGORITHM OR SECURITY RESULT. GLOBAL NO NOMINATION.
