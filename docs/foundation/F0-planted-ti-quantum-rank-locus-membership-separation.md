# MORPH-F0: quantum membership-oracle lower bound and dense public rank-locus search

**2026-10-20. Source-first quantum attack/strictly weaker oracle negative control; GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD.** This continues the [exact full-public dense contraction-rank locus](F0-planted-ti-dense-rank-locus.md) and [reversible full-public quantum greedy-flag analysis](F0-planted-ti-quantum-greedy-flags.md). It gives (i) a **tight quantum query lower bound in an explicitly restricted oracle-only model**, and (ii) a **valid quantum original-verifier any-witness attack using the actual complete published tuple** when a separate dense-source event makes that rank oracle correct. The first claim MUST NOT be transferred to the full-public attacker.

**Priority.** The planted-TI source, original problem and generic classical upper bound are due to Liu, Qiao, Tang and Zhang, [*The planted tensor problem over finite fields: algorithms and cryptography*](https://arxiv.org/abs/2609.31256) (2026). The quantum lower-bound proof uses the classical **hybrid argument** associated with Bennett, Bernstein, Brassard and Vazirani, [*Strengths and Weaknesses of Quantum Computing*](https://arxiv.org/abs/quant-ph/9701001) (1997); the upper bound uses **known** Grover/fixed-point amplitude amplification, including Yoder, Low and Chuang, [*Fixed-point quantum search with an optimal number of queries*](https://doi.org/10.1103/PhysRevLett.113.210501) (2014). Neither search technique is presented as a novel quantum algorithm or quantum hardness assumption.

## 1. Strict oracle-only experiment: no public matrices

Let `V=F_q^n` and `H` be a **uniform** d-plane with `1<=d<n`, `c=n-d`. The algorithm receives only `q,n,d` and may coherently query the **idealized hidden point-membership oracle**
\[
O_H:\ |v,b\rangle\ \longmapsto\
 |v,b\oplus [v\ne0\ \land\ v\in H]\rangle.
\]
Any answer about the universally known zero vector can be simulated locally, hence the nonzero convention loses no hidden-H information. There is **no public alternating tensor**, matrix coefficient, planted generating basis, quantum example state or coset label. The goal is to output **one nonzero v in H**. Ancillas, arbitrary unitary computations between queries, arbitrary coherent inputs and final measurement are permitted.

Each fixed nonzero v belongs to a uniform H with the same probability
\[
\boxed{p=\frac{q^d-1}{q^n-1}<q^{-c}.}
\]

**Theorem 1 (distributional quantum black-box lower bound).** Any quantum algorithm using at most Q membership queries, then proposing one nonzero vector, has averaged success probability at most
\[
\boxed{\Pr_{H,\mathrm{algorithm}}[\mathrm{output}\in H\setminus\{0\}]
 \ \le\ \min(1,p+2Q\sqrt p).}
\]
Therefore constant (e.g. at least 2/3) success requires
\[
\boxed{Q\ge\frac{2/3-p}{2\sqrt p}=\Omega_q(q^{c/2})}
\]
when `c\to\infty` (with the displayed inequality meaningful when `p<2/3`).

**Proof (full source-aware hybrid).** Purify all random bits and postponed measurements. Compare the true `O_H` run with an *all-zero-membership* oracle (identity on the answer register). Let `|\psi_k^0\rangle` be the pre-query state in the all-zero run at call k; crucially, it is independent of H. Let `\Pi_H` project onto nonzero query-register inputs in H. For either the standard bit oracle or its phase-equivalent form,
\[
\|(O_H-I)|\psi_k^0\rangle\|
\le2\|\Pi_H|\psi_k^0\rangle\|.
\]
Averaging over uniform H yields
\[
\mathbb E_H\|\Pi_H|\psi_k^0\rangle\|^2\le p
\quad\Longrightarrow\quad
\mathbb E_H\|\Pi_H|\psi_k^0\rangle\|\le\sqrt p.
\]
The usual Q-step telescoping/hybrid triangle inequality gives
\[
\mathbb E_H\|\,|\psi_Q^H\rangle-|\psi_Q^0\rangle\,\|\le2Q\sqrt p.
\]
For every H, the total variation of any final measurement is at most the pure-state trace distance, itself bounded by this state-vector norm. In the all-zero oracle run the proposed output distribution is independent of H, hence its average chance to land in nonzero H is **at most p**. Combining gives the boxed result. QED.

This is a **distributional lower bound for an oracle with one bit per tested vector**. It says absolutely nothing negative about a quantum attacker that receives all the actual public tensor coefficients in its initial input state or classical program.

## 2. Matching standard quantum oracle-only upper bound

For `q=2^e` with an effective public field representation, prepare a uniform superposition over all `q^n` vectors, using exactly `en` Hadamard gates; exclude zero inside the membership marking predicate. The marked fraction is precisely `(q^d-1)/q^n`. Standard amplitude amplification therefore returns one nonzero vector in H with constant success after
\[
\boxed{O\!\left(\sqrt{\frac{q^n}{q^d-1}}\right)=O_q(q^{c/2})}
\]
membership queries. Fixed-point amplification permits arbitrary prescribed failure parameter with an additional logarithmic factor. The oracle-query complexity is thus **Theta(q^{c/2}) in this restricted uniform-H model** (constants/polynomial gate overhead suppressed). This is the familiar quadratic Grover speedup over the classical membership-only `Omega(q^c)` screen of [the dense rank-locus note](F0-planted-ti-dense-rank-locus.md); it is **not** a full-tensor quantum hardness lower bound.

## 3. Concrete full-public quantum attack at the sufficiently dense rank threshold

Now return to the **original, entirely different information experiment**: sample H from **any prior**, independently sample m uniform alternating public forms annihilating `H x H`, and publish **all matrix entries**. The original verifier accepts any d-plane L on which all m forms vanish. Set `c=n-d`, require `m>c`, and define the explicitly **public**
\[
f_A(v)=[v\ne0\ \land\ \operatorname{rank}C_A(v)\le c],
\qquad
C_A(v)=\begin{bmatrix}A_1(v,-)\\\vdots\\A_m(v,-)\end{bmatrix}.
\]
Every f_A evaluation is polynomial via Gaussian elimination, and its reversible evaluation is polynomial over a fixed effective binary field.

The previously proven [full-tensor rank-locus theorem](F0-planted-ti-dense-rank-locus.md) supplies, **for every fixed H**, a no-postselection honest-source failure probability
\[
\boxed{
\varepsilon_{n,d,m,q}
=\min\!\left\{1,
\left({n\brack1}_q-{d\brack1}_q\right)
C_q q^{-(m-c)(d-1)}
\right\},
\quad C_q=\prod_{j\ge1}(1-q^{-j})^{-1}<4,}
\]
such that on the complementary source event
\[
\boxed{f_A(v)=1\quad\Longleftrightarrow\quad v\in H\setminus\{0\}}
\]
**simultaneously for all v**. This is far stronger than assigning the fixed-point contraction law to tensor-adaptive points.

**Theorem 2 (verified dense full-public quantum inversion upper bound).** Take `q=2^e`, with a fixed effective field and `0<\eta<1`. There is an explicit quantum algorithm reading **all actual public matrices** that uses at most
\[
\boxed{
O\!\left(d\,q^{c/2}\log(d/\eta)\right)
}
\]
coherent evaluations of the public f_A rank circuit and its inverse (and polynomial reversible overhead per evaluation), outputs a classical **original-verifier accepted** d-plane whenever it reports success, and on the unfiltered honest source succeeds with probability at least
\[
\boxed{1-\varepsilon_{n,d,m,q}-\eta.}
\]

**Algorithm and proof.** On the good source event f_A is exactly membership in the unknown H. Build a list of independent recovered vectors `v_1,...,v_k` beginning with k=0. Mark public vectors v when `f_A(v)=1` and `v\notin\operatorname{span}(v_1,...,v_k)`, each predicate computed reversibly and publicly. If all already obtained vectors belong to H, the exact marked fraction in the **uniform q^n superposition** is
\[
p_k=(q^d-q^k)/q^n\ge(1-1/q)q^{-c},\qquad0\le k<d.
\]
Apply known fixed-point amplitude amplification using this explicit lower bound, then measure and classically check the newly recovered vector's public predicate and linear independence. Repeat with a fresh success budget `\eta/d` until k=d. The d-stage total failure chance on the good tensor event is at most `\eta`; each stage needs `O(q^{c/2}\log(d/\eta))` coherent public-rank tests. The resulting span equals H. **Before output**, run the entire unchanged original public verifier; abort on any failure. Even on bad source tensors, this final verifier forbids false declared witnesses. Average the good event over any prior on H to obtain the stated lower success bound. QED.

For fixed q, `d/n\to\alpha\in(0,1)`, and `m=c+h` with fixed h satisfying `h\alpha>1`, the first-moment bound gives `\varepsilon=q^{-\Omega(n)}`. Thus this is a high-probability **full-public** quantum search bound already at `m=c+O(1)=\Theta(n)`, below the previously known `m=\Theta(n^2)` polynomial full-span inversion boundary. The **displayed sufficient work budget** scales as q^{Theta(n)} when c is linear, not polynomial; this is **not** a lower bound on the best full-public attacker. Furthermore the classical/quantum seeded completion results already give a t=1 attack of the same broad `q^{c/2}` quantum order when m>=c; no independent speedup or new complexity-class claim is made.

## 4. Exact binary size sanity and strict nonclaims

For `q=2,n=6,d=2,c=4`, the uniform-H membership probability for a fixed nonzero candidate is `p=(2^2-1)/(2^6-1)=1/21`. With one previously recovered genuine independent vector, the uniform all-vector marked fraction is `p_1=(2^2-2)/2^6=1/32`, exactly the generic lower fraction `(1-1/2)2^{-4}`. These are simple exact counts, **not quantum-circuit tests, measured amplitudes or generated-tensor attack cases**.

Critical boundaries:

- The **quantum lower bound** is **ONLY for a hidden-H membership bit oracle** and uniform H. It is *not* a full-tensor computational or quantum-hardness claim.
- The **quantum upper bound** genuinely uses the complete public tuple but assumes the **source-good dense rank-locus identity**, not a hidden H oracle. The attack's final answer passes the unchanged **any-witness** public verifier.
- If `m<=c` (including the external sparse conjectural `m\asymp n/\log n,d/n<1/2`), the public predicate `rank C_A(v)<=c` is **vacuous on every nonzero v**, so the full-public dense algorithm above provides **no attack** on those parameters.
- No quantum program, QPU run, QRAM, physical gate budget, empirical source samples, KEM/PKE/trapdoor/OWF construction, independent Field 15, A-ID, F0-K or N1 reservation. README and research-stage registry unchanged.

**Disposition:** TIGHT QUANTUM MEMBERSHIP-ONLY QUERY SCREEN / DENSE FULL-PUBLIC ORIGINAL-VERIFIER QUANTUM UPPER BOUND. GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD; HEPMR BENCHMARK ONLY; N1-60 free.
