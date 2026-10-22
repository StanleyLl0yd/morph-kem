# MORPH-F0: independent 2026 mathematics intake - symplectic LPN and exponential equations

**2026-10-22. External positive-research-lead triage plus an exact generic low-noise attack budget; NOT a MORPH candidate, independently verified security proof, unique new MORPH foundation, or cryptographic benchmark.** GLOBAL NO NOMINATION, H-A/H-B/H-C HOLD; planted-TI FROZEN comparator; D0/D1/D2/D3/D4 and public tensor-action no-gos unchanged. No new N1-60/F0-K/A-ID, code, executable samples, parameter recommendation or KEM/PKE branch.

**Source-exact 22 October follow-up:** [Full parity-check k=n versus k=n-1 and paired error-syndrome MITM](F0-symplpn-parity-check-mitm-audit.md). This preceding support enumeration is a correct conservative bound, NOT the best known or expected ISD attack complexity. Original decision distribution and changes to sparse search remain distinct.

## 1. Stronger external evidence than another renamed hard problem

**Quantum stabilizer decoding / symplectic LPN.** [Lu–Poremba–Quek–Ramkumar, *Post-Quantum Cryptography from Quantum Stabilizer Decoding*, arXiv:2603.19110, **v2 dated 6 October 2026**](https://arxiv.org/abs/2603.19110), develops a quantum-error-correction-native assumption and *conditional* reductions yielding OWF, PKE and OT. It invokes independent 2026 work [Poremba–Quek–Shor, *The Learning Stabilizers with Noise Problem*, ITCS 2026](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITCS.2026.108) and Khesin–Lu–Poremba–Ramkumar–Vaikuntanathan, *Average-case complexity of quantum stabilizer decoding* (STOC 2026, as cited by Lu et al.). The paper offers theoretical reasons that symplectic noisy-code assumptions may not simply coincide with classical LPN, but **it does not prove unconditional hardness against all polynomial quantum attacks**. Its cryptographic security theorems are conditional on precise average-case assumptions. These are **existing researchers'** mathematical results and constructions, not MORPH discoveries.

**Multivariate exponential equations with unknown coefficients.** [Trey Li, *Advances in Mathematics of Communications* 22 (2026), 75–105, DOI 10.3934/amc.2026001](https://doi.org/10.3934/amc.2026001), **early access 27 November 2025**, presents over Euclidean domains a class of exponent equations and reports in the abstract NP-hardness, average-case hardness, random self-reducibility, search-to-decision reductions and trapdoorizability. At this checkpoint those are **published author claims** whose full quantifiers, source distribution, reduction directions and output arithmetic costs have **not** been independently re-proved by MORPH. Do not transfer these results to an unstated concrete cryptographic source, and do not relabel this published problem as a new MORPH one.

**Evidence order:** the stabilizer work has an explicit average-case cryptographic decision formulation and conditional primitive reductions, thus makes the stronger **external comparator** for MORPH admission quality; the exponent-equation article is a potentially interesting **separate mathematical lead** but its concrete original-inversion source, arithmetic representation and quantum complexity are **NOT REVIEWED**. Neither passes independent MORPH Field 15, because adopting an already published assumption alone is not independent mathematical novelty.

## 2. Exact classical sympLPN source, without changing its probability law

Fix n physical qubits, an explicitly represented full-column-rank binary matrix \(A\in\mathbb F_2^{2n\times n}\) whose n columns form a **symplectically isotropic** subspace for the standard nondegenerate alternating bilinear form. For a fully specified **conditional** law of A over such matrices (e.g., the uniform law described in Lu et al.), sample a uniformly random \(x\in\mathbb F_2^n\), and n independent two-bit Pauli error coordinates \(e_i\) with
\[
\Pr[e_i=(0,0)]=1-p,\qquad
\Pr[e_i=(1,0)]=\Pr[e_i=(0,1)]=\Pr[e_i=(1,1)]=p/3
\quad(0<p<1).
\]
Publish **all** A and \(z=Ax+e\in\mathbb F_2^{2n}\). The paper's sympLPN **decision comparison** distinguishes this structured source from the **same sampled A** with independently uniform z. This is not the same as recovering the planted x or solving a newly invented public any-witness search task. Efficient exact generation of the conditioned isotropic A law must be established separately before MORPH admits it as a strict-polynomial original source; no hidden rejection-sampler complexity is assumed away in this note.

A proposed MORPH full public search verifier that accepts **any** pair \((x',e')\) with \(Ax'+e'=z\) and no noise constraint has an immediate polynomial accepted section: **output \(x'=0,e'=z\)** for every public tuple, both honest and null. This is a complete mathematical **NO-GO for that changed unrestricted witness relation only**, not a break of the paper's decision sympLPN security claim.

A changed sparse verifier \([Ax'+e'=z\ \wedge\ \operatorname{PauliWt}(e')\le t]\) is another precise problem, but the original depolarizing source has full support: for **every t<n**, the planted e fails this new check with strictly positive probability. In fact the number of nonzero two-bit error pairs \(W=\operatorname{PauliWt}(e)\) obeys **exactly**
\[
\boxed{W\sim\mathrm{Binomial}(n,p)},\qquad
\boxed{\Pr[\text{planted }e\text{ passes threshold }t]
=\sum_{j=0}^t {n\choose j}p^j(1-p)^{n-j}.}
\]
This is the completeness probability of the **specific sampled pair** \((x,e)\), not necessarily the probability that *some alternate* pair passes the verifier. Replacing depolarizing errors with a truncated/conditioned weight-t sampler to force universal honest completeness changes the source law and therefore **does not inherit** the paper's hardness results without a source-preserving reduction.

## 3. Rigorous generic low-noise classical attack upper bound

Let \(S_t=\sum_{j=0}^t {n\choose j}3^j\), the **exact number of possible Pauli errors with at most t corrupted coordinate pairs**. Publicly enumerate all those errors \(e'\); for each, Gaussian-solve \(Ax'=z-e'\). If one solves, output \((x',e')\) and optionally use the full changed sparse verifier. The cost is at most
\[
\boxed{S_t\operatorname{poly}(n)}
\]
for **each** presented A,z. It is a standard exhaustive-noise search strategy, not a novel MORPH cryptanalytic algorithm.

On a structured honest sample, whenever the planted error has \(W\le t\), the procedure finds an accepted pair. Hence the conditional success probability, over the **unfiltered original depolarizing source**, is **at least** the exact binomial CDF in §2, with no assertion of conditional independence between alternative witnesses.

For the **matching unrestricted null** with z uniformly random in \(\mathbb F_2^{2n}\) independently of A, even conditional on **each fixed full-rank isotropic A**, the set
\[
\bigcup_{\operatorname{PauliWt}(e')\le t}\left(e'+\operatorname{im}A\right)
\]
has at most \(S_t2^n\) elements. Thus the null false-positive probability of the same existence check obeys the exact union bound
\[
\boxed{\Pr_{\rm null}[\exists (x',e'):\ Ax'+e'=z,\ \operatorname{PauliWt}(e')\le t\mid A]\le\min(1,S_t2^{-n}).}
\]
No false assumption of disjoint noise cosets is made. This is a **distinguisher** for the paper's specified distribution if its runtime is affordable; it is not an efficient polynomial distinguisher in general.

Now take the low-noise regime in Lu et al., \(p=c/\sqrt n\) for any constant c>0 and sufficiently large n. Put \(\mu=np=c\sqrt n\) and \(t=\lceil2\mu\rceil\). The usual binomial Chernoff bound gives
\[
\Pr[W>t]\le\exp(-\mu/3)=\exp(-\Theta(\sqrt n)).
\]
The elementary support count \(S_t\le(t+1)(3n)^t\) yields
\[
\boxed{\log_2 S_t=O(\sqrt n\log n),\qquad
\mathrm{work}=2^{O(\sqrt n\log n)}\operatorname{poly}(n).}
\]
Consequently this **generic, classical, subexponential-time** procedure has honest-source success at least \(1-\exp(-\Theta(\sqrt n))\) and uniform-null false-positive at most \(2^{-n+O(\sqrt n\log n)}\). It solves a **generic low-noise noisy-linear search/detection gate**, relying on neither isotropy nor any claimed independent mathematical attack. It **does not invalidate polynomial-time assumed hardness, reduce subexponential work to polynomial, or contradict the cited PKE security theorem**. It is an attack-cost upper bound that any future claimed concrete security level must account for alongside stronger decoding/ISD, quantum, and source-specific methods.

For constant p, t is \(\Theta(n)\) and this enumeration can be exponential; neither regime proves that the quantum stabilizer problem is hard or easy in polynomial time.

## 4. Exact bitlength gate for exponential equations

Before applying Li's **existing** multivariate exponential-equation framework in MORPH, freeze the specific Euclidean domain, its finite representations, the degree/height or norm of coefficients and variables, exponent encoding, the full original public equation and any accepted-witness semantics, and the actual unconditional polynomial honest sampler. A general equation in a Euclidean domain **does not automatically** have a polynomial-bitlength output.

**Generic representation lemma, not a critique of Li's chosen constructions.** For an integer \(a\ge2\), with a binary l-bit exponent \(m=2^{l-1}\), the ordinary unmodded integer \(a^m\) has \(\lfloor m\log_2a\rfloor+1=\Omega(2^l)\) output bits. Therefore a promise to publish the **full integer result** of such a power does not give a polynomial-size public transcript solely from polynomial-bitlength base and binary exponent. Modular exponentiation in a fixed polynomial-size quotient can avoid this output blowup, **but changes the mathematical equivalence relation and its inverse problem**, which must be analyzed anew. The lemma does not say that Li's paper commits this mistake; it is a mandatory intake test because its abstract emphasizes general Euclidean domains.

**Disposition:** both quantum stabilizer/symplectic-noise and exponential-equation objects stay **EXTERNAL PRIOR-ART COMPARATORS / NOT ADMITTED as MORPH independent foundations**. There is more positive independently published theory here than in the earlier synthetic gluing and automata dead ends, but no MORPH construction, source-specific hardness demonstration, full Field-15 differentiation, candidate parameter set, experiment authorization, or post-quantum security assertion has been produced.
