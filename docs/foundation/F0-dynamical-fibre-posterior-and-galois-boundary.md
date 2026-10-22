# MORPH-F0: exact iterated-map fibre posterior, null TV and finite-field Galois boundary

**2026-10-22. Source-first analytic D1 boundary, not an inversion algorithm for arbitrary nonpermutation maps or a new cryptographic assumption.** Builds on the [public permutation-iteration no-go](F0-iterated-permutation-polynomial-public-section.md). GLOBAL NO NOMINATION; H-A/H-B/H-C HOLD; D0 HOLD/DEFER; TI FROZEN comparator; D1 nonpermutation HOLD, **not** a candidate. No new N1/F0-K/A-ID, code, performance measurements, source experiment campaign or security parameters.

## 1. Honest distribution and full original any-witness problem

Fix an effective finite field \(\mathbb F_q\), an explicit public polynomial \(f\in\mathbb F_q[X]\) of polynomial degree, and a public polynomially bounded positive iteration count T. The unconditional polynomial honest generator selects **uniform** \(s\in\mathbb F_q\) and publishes \(P=(q,f,T,b)\) with
\[
 b=\Phi(s),\qquad \Phi=f^{\circ T}.
\]
Every honest sample passes the **complete original verifier** on s:
\[
\operatorname{Equivalent}(P)=\{y\in\mathbb F_q:\Phi(y)=b\}.
\]
The attacker needs **any y in this entire set**, not the sampled s; f need **not** be injective. Although \(\deg\Phi\) may be exponential in T, the forward map and original verification evaluate T copies of the explicitly represented low-degree f in polynomial time. All the following distributional statements are **conditional on exact public (q,f,T)**. If these are randomized by another polynomial-time source, use the same distribution in both planted and null worlds before averaging.

Define exact pointwise fibre counts and image size
\[
 N_z=\#\{x\in\mathbb F_q:\Phi(x)=z\},\qquad
 M=|\operatorname{im}\Phi|=\#\{z:N_z>0\}.
\]
The definitions describe a finite mathematical distribution; **computing M or all N_z by enumerating q elements can require exponential time in \(\log q\)**. No efficient public preimage enumeration, polynomial image-membership test or output sampler is assumed.

## 2. Exact posterior and optimal unbounded planted-secret recovery

**Theorem 1 (honest uniform-source size bias):** for every z in \(\mathbb F_q\),
\[
\boxed{\Pr_{\rm honest}[b=z\mid q,f,T]=N_z/q.}
\]
For \(N_z>0\), the conditional posterior on the **sampled** s is uniform over the full original accepted fibre:
\[
\boxed{\Pr[s=x\mid b=z,q,f,T]=
       \mathbf1_{\{\Phi(x)=z\}}/N_z.}
\]
Consequently the Shannon posterior entropy and Bayes-optimal *unbounded* probability of recovering the **particular sampled s** are
\[
\boxed{H(s\mid b,q,f,T)=\frac1q\sum_{z:N_z>0}N_z\log_2 N_z},
\qquad
\boxed{P_{\rm Bayes,\ sampled\ s}=M/q.}
\]

**Proof:** For uniform s every x contributes probability 1/q; collecting preimages produces the pushforward probability N_z/q. Conditional normalization gives the fibre-uniform posterior. For each reachable z, entropy is log_2 N_z. The Bayes-optimal guessed sampled s succeeds conditional on z with probability 1/N_z; weighting by N_z/q and summing over M nonempty fibres yields M/q. QED.

**Critically different target:** the unbounded probability of producing **any** original-verifier accepted y is **one on every honest instance**, regardless of N_z. The Bayes \(M/q\) formula is *not* a computational attack bound and is *not* the original MORPH success condition. Any computational hardness conjecture must be about **finding an accepted y under this exact honest distribution**, not identifying which member was sampled.

## 3. Exact public planted/null statistical divergence

Let the *comparison null* draw the identical public (q,f,T) and then select \(b\) **independently uniformly** from all \(\mathbb F_q\). Its mass is 1/q for each z. Then
\[
\begin{aligned}
\operatorname{TV}(D_{\rm honest},D_{\rm null}\mid q,f,T)
 &=\tfrac12\sum_z |N_z/q-1/q|\\
 &=\tfrac1{2q}\sum_z|N_z-1|\\
 &={q-M\over q}.
\end{aligned}
\]
Thus
\[
\boxed{\operatorname{TV}=1-M/q.}
\]
**Proof of the last equality:** \(\sum_zN_z=q\), and for each nonempty fibre \(N_z\ge1\). The sum of \(N_z-1\) over the M occupied outputs is \(q-M\), and exactly \(q-M\) outputs have N_z=0 and contribute one each. Divide the total \(2(q-M)\) by \(2q\). QED.

The **optimal unbounded** existence detector accepts iff \(b\in\operatorname{im}\Phi\), true-positive 1, null false-positive M/q, TV advantage \(1-M/q\). An *efficient* image-membership algorithm is **not** supplied. For any verifier-gated public attack with honest-source success p, using that attack as a detector gives null false-positive **at most** M/q (every emitted accepted witness forces b in the image), so its detection gap is **at least** \(p-M/q\), clipped at zero if used as a nonnegative bound. This does *not* make its success or runtime polynomial.

**Interpretation:** under a uniform source, a permutation map has M=q and TV=0 (the prior easy-inverter theorem); nonpermutation maps have M<q and a strictly positive *information-theoretic* detector gap, but **neither case establishes average-case one-wayness or efficient detection**. The image-size formula concerns exactly this unconditioned uniform source and this matching unrestricted-null b; it does not hold unchanged for nonuniform s or a null already conditioned to have a predecessor.

## 4. Exact toy control and wrong-branch caveat

Over \(\mathbb F_7\) take public \(f(X)=X^2\), T=2, hence \(\Phi(X)=X^4\). The public target counts \(N_z\), ordered z=0,1,...,6, are
\[
(N_0,\ldots,N_6)=(1,2,2,0,2,0,0),
\quad M=4,\quad \sum_z N_z=7.
\]
The honest b has support {0,1,2,4}; null is uniform on all seven values. Exact TV is \(1-4/7=3/7\), posterior entropy is \(6/7\) bits, and unbounded **sampled-s** recovery is \(4/7\). An honest target b=1 has two accepted full witnesses \(\{1,6\}\): either wins the *original full verifier* for \(f^{\circ2}(y)=1\), though only one was actually drawn. At the **intermediate** target of 1, a backward step choosing the root 6 of \(x^2=1\) cannot be extended another step because 6 is not a square in \(\mathbb F_7\). Thus naive arbitrary backward choices do not give an inversion proof for nonpermutation maps. These are finite scratch arithmetic statements, not a committed experiment or a cryptographic parameter study.

## 5. Finite-field arithmetic versus arboreal Galois arguments

The field-theoretic preimage tree of \(f^{\circ T}(X)-b\) over an algebraic closure is a genuine established object, studied in **arithmetic dynamics**; see [Jones, *Galois representations from pre-image trees: an arboreal survey*](https://arxiv.org/abs/1402.6018), [Kadets, *Large arboreal Galois representations* (2020)](https://doi.org/10.1016/j.jnt.2019.09.021), and [Oliveira–Brochero Martínez, polynomial dynamics over finite fields](https://arxiv.org/abs/2201.00954). A crucial base-field distinction must be preserved:

- Over a **fixed finite constant field** \(\mathbb F_q\), the absolute Galois group \(\mathrm{Gal}(\overline{\mathbb F}_q/\mathbb F_q)\cong\widehat{\mathbb Z}\) is **procyclic**, topologically generated by Frobenius \(\alpha\mapsto\alpha^q\). Therefore its induced image on **any** finite preimage level is **cyclic**. This does not resemble a generic full nonabelian automorphism group of a high-branching regular rooted tree.
- Over a **number field or a function field** such as \(\mathbb F_q(t)\), the absolute Galois group and arithmetic setting differ; the corresponding arboreal representation may be large and nonabelian, but a theorem over that field cannot simply be transferred to the fixed-\(b\), fixed-\(\mathbb F_q\), original full-public verifier without a new distribution-preserving reduction.
- Large formal tree width, complex global Galois monodromy and abundant extension-field roots **do not by themselves prove** average-case difficulty of finding an \(\mathbb F_q\)-rational accepted predecessor.

These are classical finite-field/Galois facts: [Lidl–Niederreiter, *Finite Fields*, structure chapter](https://www.cambridge.org/core/books/abs/introduction-to-finite-fields-and-their-applications/structure-of-finite-fields/E4A21903F3C53E179BA11282E8E16AD1) and the cited arboreal research. **No new full-Galois-group theorem or hardness claim** is made here. The conditional absolute-Galois observation is not an attack algorithm on nonpermutation f.

## 6. D1 stop/go gate

The [permutation polynomial public inverse](F0-iterated-permutation-polynomial-public-section.md) and this exact uniform-image/posterior analysis establish strong **known boundaries**, not independent Field-15 mathematics. D1 **nonpermutation** remains **HOLD / NOT ADMITTED**. Do not treat a large iterated degree, collision count, large tree or fixed-field Galois slogan as a novel cryptographic basis. An admissible future proposal would first require an independently motivated *specific* nonpermutation family with a strict polynomial honest generator and full any-witness verifier; a positive comparison against known finite-field root/functional-graph/resultant/Gröbner/generic search and quantum algorithms; and positive MORPH-R0 Field 15 evidence before code or samples.

No further routine D1 source counting passes are authorized without such a concrete independent object. Global status NO NOMINATION, original F0/N1 historical evidence and D0/TI decisions unchanged.
