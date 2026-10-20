# MORPH-F0: full-tensor seeded linear completion and exhaustive short-seed attack

**2026-10-20. Full-public-tensor constructive negative-control attack; GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.** This pass follows [exact global incidence and tangent rigidity](F0-planted-ti-global-incidence-and-tangent-rigidity.md). The algorithm reads **all published alternating forms**, constructs an accepted **any-witness** by public linear algebra when it finds a suitable seed, and verifies the *original* relation. It does not assert polynomial unseeded inversion in the conjectural d<c regime, any independent Field-15 novelty, a KEM/OWF/trapdoor, or an experimental success.

**External priority.** Liu, Qiao, Tang and Zhang, [*The planted tensor problem over finite fields: algorithms and cryptography*](https://arxiv.org/abs/2609.31256) (2026) already establish a generic q^{O(n log n)} planted-TI algorithm and describe polynomial algorithms on a different d>=n/2 boundary. We make **no claim** to have invented the generic subexponential attack complexity. The scoped addition below is a self-contained original-verifier algorithm with *exact conditional rank distribution and success probability* and a precise conditional-seed interface, for transparent audit against that literature.

## 1. Honest law, verifier and public contraction

Let V=F_q^n, 2<=d<n, c=n-d, m>=1, and q any prime power. Draw an arbitrary-prior d-plane H independently of the forms. Given H, sample each of m independent **uniform** alternating forms A_i vanishing on H x H; no acceptance-only filtering, rank postselection or oracle restriction. The full public tensor is (A_1,...,A_m), and

\[
\operatorname{Verify}(A,L)=
 [\dim L=d\ \wedge\ A_i|_{L\times L}=0\;\forall i].
\]

Every accepted L wins, whether or not L equals the actual H. An attacker knows A and the public parameter d, **not H**.

For a *publicly supplied* t-plane T<=V, 1<=t<=d, define its simultaneously orthogonal public completion space

\[
S_A(T)=\{v\in V:\ A_i(u,v)=0
\text{ for every }u\in T,\ 1\le i\le m\}.
\]

Given a basis of T, S_A(T) is the kernel of an explicit mt-by-n matrix of public linear equations. Both constructing S_A(T) and checking Verify(A,S_A(T)) (if dim S_A(T)=d) cost polynomially many finite-field operations. The procedure may reject a bad seed; it never declares success without the full original verifier.

## 2. Exact known-seed rank theorem

**Theorem 1 (conditional fixed-seed completion).** Fix any honest H and any fixed t-plane T<=H independently of the conditional sampling of A. With V=H plus a complement C of dimension c, the restriction of S_A(T) to C is the kernel of a **uniform mt-by-c matrix** M_T. Thus

\[
\boxed{S_A(T)=H\oplus\ker M_T,\qquad
\dim S_A(T)=d+c-\operatorname{rank}M_T.}
\]

The direct sum is in the chosen (private analysis) splitting; the public computation of S_A(T) requires no such splitting. For 0<=k<=min(mt,c), with [a choose b]_q denoting the Gaussian binomial,

\[
\boxed{\Pr(\operatorname{rank}M_T=k\mid H,T)
=q^{-mtc}\left[{c\atop k}\right]_q
\prod_{j=0}^{k-1}(q^{mt}-q^j).}
\]

In particular, for mt>=c,

\[
\boxed{p_{\rm complete}(q,c,m,t)
=\Pr[S_A(T)=H\mid H,T]
=\prod_{j=0}^{c-1}(1-q^{j-mt}).}
\]

For mt<c, exact completion S_A(T)=H is impossible. If mt>=c+s with integer s>=0, the failure probability obeys

\[
\boxed{1-p_{\rm complete}
\le\frac{q^c-1}{q-1}\,q^{-mt}
<\frac{q^{-s}}{q-1}.}
\]

**Proof.** Fix an H-adapted basis, write A_i in blocks [0,B_i; -B_i^T,D_i], and choose a basis of T inside H. The t rows recording pairings A_i(u,-) vanish on H and give t *independent uniform* rows on C because B_i is a uniform d-by-c matrix. All m slices are independent. Hence M_T is uniform mt-by-c and H is always contained in S_A(T). The exact number of rank-k mt-by-c matrices is [c choose k]_q times the number of surjective maps F_q^{mt}->F_q^k, namely prod_{j<k}(q^{mt}-q^j). Full rank gives the product. Finally union-bound over projective nonzero x in F_q^c to estimate Pr(M_T x=0). QED.

**Independence caveat.** The *exact conditional rank law* above applies when T is fixed conditional on H **without inspecting the sampled forms**. A tensor-adaptive algorithm may choose an exceptional T correlated with A; do **not** apply the same conditional probability to such postselected seeds. However for any observed public T, computing S_A(T), checking its dimension and checking the **full verifier** are deterministic and always valid.

## 3. Actual attack: enumerate short seeds and verify complete witnesses

**Exhaustive public seed-completion algorithm (mathematical pseudocode):**

1. Enumerate every t-dimensional subspace T of the public V, canonically (for example by reduced-row-echelon matrices). No H-membership test or secret-dependent enumeration is used.
2. Compute the full public simultaneous orthogonal complement S_A(T) by Gaussian elimination.
3. If dim S_A(T)=d, run the *original full* Verify(A,S_A(T)); return an accepted basis only when it passes. Otherwise continue.
4. Return "not found" if no seed gives an accepted candidate; no claim of deciding nonexistence on arbitrary inputs.

**Theorem 2 (unconditional honest-source success).** Assume 1<=t<=d and mt>=c. The above deterministic algorithm, given only the full public tuple, outputs **some accepted d-plane** on the original unfiltered honest distribution with probability **at least**

\[
\boxed{\Pr_{\rm honest}[\text{public accepted witness found}]
\ \ge\ p_{\rm complete}(q,c,m,t)
=\prod_{j=0}^{c-1}(1-q^{j-mt}).}
\]

The lower bound holds for **any prior on H**. Every success is full-original-verifier certified. The number of candidate t-planes is exactly [n choose t]_q; for C_q=prod_{j>=1}(1-q^{-j})^{-1}<4,

\[
\boxed{\text{field-operation work}\le
\operatorname{poly}(n,m,t,\log q)\,[n\choose t]_q
\le\operatorname{poly}(n,m,t,\log q)\,C_q q^{t(n-t)}.}
\]

**Proof.** For each fixed H, select *one* t-plane T_*(H)<=H by a deterministic rule depending only on H (not on sampled A). This seed appears in the public exhaustive enumeration, although the algorithm does not know which enumerated seed it is. By Theorem 1, with probability p_complete the public orthogonal completion of this fixed seed equals H, and its full verifier then passes. The real algorithm might also succeed on other seeds, so this is a lower bound. Average over any H-prior. The enumeration bound is Gaussian-binomial counting; all per-seed operations are linear algebra plus verification. QED.

For the externally conjectural fixed-q scale d=ceil(n/C), C>=3, m=ceil(n/log n), choose t=ceil((c+s)/m) (eventually t<=d). When s=Omega(n) is a fixed linear slack, t=Theta(log n), the honest-source failure bound is q^(-Omega(n)), and exhaustive field work is q^{O(n log n)} times a polynomial. This matches the **order of the pre-existing generic upper bound**, not a polynomial-time public break. No hardness *lower* bound or cryptographic security follows.

## 4. Exact binary small-field formula control (scratch only)

Let q=2, n=6, d=3, c=3, m=2, t=2, and a **fixed precommitted** T<=H. Here mt=4 and the public completion uses a uniform 4-by-3 binary matrix. There are 2^12=4096 such matrices, of which

\[
(2^4-1)(2^4-2)(2^4-2^2)=15\cdot14\cdot12=2520
\]

have column rank three. Thus p_complete=2520/4096=**315/512**, matching the product (1-2^-4)(1-2^-3)(1-2^-2). The full public enumeration would search [6 choose 2]_2=651 subspaces. This is finite exact arithmetic, not a committed attack implementation, measured source recovery, CI benchmark, or cryptographic parameter validation.

## 5. Honest boundaries and next genuinely new challenge

- **The seed may not be publicly available.** Theorem 1 is a *known-partial-witness* reduction; Theorem 2 turns it into a genuine **unseeded, but q^{O(n log n)}-time full-data attack** by exhaustive enumeration. It does *not* obtain the desired polynomial-time inversion in d<c.
- **Any accepted witness, not necessarily H.** Every output passes the original public verifier. The prior [global incidence note](F0-planted-ti-global-incidence-and-tangent-rigidity.md) separately shows that in sparse d~alpha*n<m? (specifically d/n->alpha<1/2 and m~n/log n) H is typically the only F_q-rational accepted d-plane, but the algorithm does not rely on this uniqueness.
- **Tensor-derived seed selection is the real attack bottleneck.** A future result that can efficiently find an appropriate small T from the entire public tensor, or can use weaker certified partial structure, may improve the attack. Every such proposal must record how T was selected, the source distribution, its cost and full-verifier outcome. The fixed-T exact probability must never be transferred automatically to an adaptively postselected T.
- **Not a new independent basis.** The external planted-TI problem and known q^{O(n log n)} bound predate this pass; no Field-15 novelty is claimed. No positive security claim, exact polynomial-time inverter, quantum-hardness conclusion, new source samples, A-ID, N1 number, KEM/PKE/trapdoor or candidate admission.

**Disposition:** FULL-PUBLIC EXHAUSTIVE SEED-COMPLETION ATTACK / EXACT CONDITIONAL SOURCE LAW. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD; HEPMR BENCHMARK ONLY; N1-60 remains free.
